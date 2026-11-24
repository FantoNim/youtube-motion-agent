"""Local capability setup. Standard library only; no agent/config/account mutations."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import platform
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent


def safe_path(root: Path, value: str) -> Path:
    posix, win = PurePosixPath(value), PureWindowsPath(value)
    if not value or chr(92) in value or posix.is_absolute() or win.is_absolute() or win.drive or '..' in posix.parts:
        raise ValueError('Unsafe manifest path: ' + value)
    p = root.joinpath(*posix.parts)
    if not p.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path escapes kit: ' + value)
    for q in [p, *p.parents]:
        if q == root.parent:
            break
        if q.is_symlink() or (hasattr(q, 'is_junction') and q.is_junction()):
            raise ValueError('Links/junctions are not permitted: ' + str(q))
    return p


def integrity(root=ROOT):
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    hashes = manifest['files']
    if not hashes:
        raise ValueError('Empty file manifest')
    errors = []
    for rel, expected in hashes.items():
        p = safe_path(root, rel)
        if not p.is_file():
            errors.append('Missing: ' + rel)
        elif hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            errors.append('Hash mismatch: ' + rel)
    for top in ['skills', 'helpers', 'scripts']:
        directory = root / top
        if not directory.exists():
            continue
        for p in directory.rglob('*'):
            rel = p.relative_to(root).as_posix()
            if '__pycache__' in p.parts or p.suffix == '.pyc':
                continue
            safe_path(root, rel)
            if p.is_file() and rel not in hashes:
                errors.append('Unlisted executable/resource file: ' + rel)
    if errors:
        raise ValueError('\n'.join(errors))
    return manifest


def audit_lock(project):
    package = json.loads((project / 'package.json').read_text())
    lock = json.loads((project / 'package-lock.json').read_text())
    entries = lock['packages']
    lifecycle = []
    for name, item in entries.items():
        if not name:
            continue
        url = item.get('resolved', '')
        if not url.startswith('https://registry.npmjs.org/') or not item.get('integrity', '').startswith('sha512-'):
            raise ValueError('Unexpected origin or missing SHA512 integrity: ' + name)
        if item.get('link'):
            raise ValueError('Linked dependency: ' + name)
        if item.get('hasInstallScript'):
            lifecycle.append(name)
    for name, version in {**package.get('dependencies', {}), **package.get('devDependencies', {})}.items():
        if entries.get('node_modules/' + name, {}).get('version') != version:
            raise ValueError('Top-level pin mismatch: ' + name)
        if (name == 'remotion' or name.startswith('@remotion/')) and version != '4.0.538':
            raise ValueError('Unreviewed Remotion version: ' + name)
    if package.get('overrides', {}).get('zod') != '4.6.6':
        raise ValueError('Expected reviewed Zod override')
    return {'packages': len(entries) - 1, 'installScriptsDisabled': True, 'packagesWithInstallScripts': lifecycle}


def run(args, cwd, log, env=None):
    # No shell interpolation; Windows .cmd delivery is handled by subprocess/CreateProcess.
    args = [str(a) for a in args]
    print('RUN ' + json.dumps(args), flush=True)
    with open(log, 'a', encoding='utf-8') as out:
        out.write('\nCOMMAND ' + json.dumps(args) + '\n')
        out.flush()
        result = subprocess.run(args, cwd=cwd, env=env, stdout=out, stderr=subprocess.STDOUT, timeout=3600)
    if result.returncode:
        raise RuntimeError('Command exited %s; inspect %s' % (result.returncode, log))


def preflight():
    checks = {'python': {'path': sys.executable, 'version': platform.python_version(), 'ok': sys.version_info >= (3, 12)}}
    for name, command, flag in [('node', 'node', '--version'), ('npm', 'npm.cmd' if os.name == 'nt' else 'npm', '--version'), ('git', 'git', '--version'), ('ffmpeg', 'ffmpeg', '-version'), ('ffprobe', 'ffprobe', '-version')]:
        executable = shutil.which(command)
        item = {'path': executable, 'ok': False}
        if executable:
            try:
                p = subprocess.run([executable, flag], capture_output=True, text=True, timeout=30)
                item.update(ok=p.returncode == 0, version=(p.stdout or p.stderr).splitlines()[0])
                if name == 'node' and int(item['version'].lstrip('v').split('.')[0]) < 22:
                    item.update(ok=False, note='Use a supported Node >=22; reference Node 26.12.1')
            except (OSError, subprocess.SubprocessError, IndexError, ValueError) as e:
                item['error'] = str(e)
        checks[name] = item
    return checks


def fresh_run(mode):
    base = safe_path(ROOT, '.starter')
    base.mkdir(exist_ok=True)
    runs = safe_path(ROOT, '.starter/runs')
    runs.mkdir(exist_ok=True)
    dest = runs / (dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8])
    dest.mkdir()
    report = {'mode': mode, 'status': 'running', 'platform': platform.platform(), 'runDirectory': str(dest), 'stages': {}, 'visualReview': 'pending-agent-review', 'listening': 'not-performed', 'agentSkillDiscovery': 'not-tested', 'optionalServices': 'not-connected'}
    (base / 'latest.json').write_text(json.dumps({'report': str(dest / 'report.json'), 'runDirectory': str(dest)}, indent=2))
    save_report(dest, report)
    return dest, report


def save_report(dest, report):
    (dest / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


def copy_project(skill, dest):
    source = ROOT / 'skills' / skill / 'assets/template'
    audit = audit_lock(source)
    # Full integrity/link traversal has already checked every copied file.
    shutil.copytree(source, dest)
    for sub in ['notes', 'proof', 'exports', 'public', 'scripts']:
        (dest / sub).mkdir(exist_ok=True)
    if not (dest / 'LICENSE').exists() and (ROOT / 'skills' / skill / 'LICENSE').exists():
        shutil.copyfile(ROOT / 'skills' / skill / 'LICENSE', dest / 'LICENSE')
    return audit


def setup(args, checks):
    dest, report = fresh_run('setup')
    report['prerequisites'] = checks
    try:
        missing = [k for k, v in checks.items() if not v['ok']]
        if missing:
            raise RuntimeError('Missing/unsupported prerequisites: ' + ', '.join(missing) + '. Use START-HERE.md; no system installations are made by bootstrap.')
        if not args.browser and not args.download_browser:
            raise RuntimeError('Supply --browser ABSOLUTE_PATH or explicitly allow --download-browser')
        browser = str(Path(args.browser).expanduser().resolve()) if args.browser else None
        if browser and not Path(browser).is_file():
            raise RuntimeError('Browser executable does not exist: ' + browser)
        node, npm = checks['node']['path'], checks['npm']['path']
        motion, three = dest / 'motion', dest / 'three'
        report['stages']['motionLock'] = copy_project('remotion-motion-graphics', motion)
        report['stages']['threeLock'] = copy_project('remotion-3d-scenes', three)
        shutil.copyfile(ROOT / 'helpers/motion-smoke.mjs', motion / 'scripts/kit-smoke.mjs')
        log = dest / 'setup.log'
        for project in [motion, three]:
            run([npm, 'ci', '--ignore-scripts', '--no-fund', '--no-audit'], project, log)
            run([npm, 'run', 'typecheck'], project, log)
            report['stages'][project.name + 'Dependencies'] = 'installed-typechecked'
            save_report(dest, report)
        run([node, 'scripts/generate-fixture.mjs'], motion, log)
        browser_env = os.environ.copy()
        if browser:
            browser_env['REMOTION_BROWSER_EXECUTABLE'] = browser
        else:
            browser_env.pop('REMOTION_BROWSER_EXECUTABLE', None)
        run([node, 'scripts/kit-smoke.mjs', '--download-browser' if args.download_browser else '--existing-browser'], motion, log, browser_env)
        browser = json.loads((motion / 'notes/browser.json').read_text())['path']
        report['stages']['motion'] = json.loads((motion / 'proof/verification-report.json').read_text())
        save_report(dest, report)
        env = os.environ.copy()
        env.update(REMOTION_BROWSER_EXECUTABLE=browser, REMOTION_GL=args.gl)
        for command in [[npm, 'test'], [node, 'scripts/render-test.mjs', '--stills'], [npm, 'run', 'render'], [npm, 'run', 'verify']]:
            run(command, three, log, env)
        evidence = json.loads((three / 'proof/verification-report.json').read_text())
        report['stages']['three'] = {'status': evidence['readiness'], 'report': str(three / 'proof/verification-report.json'), 'sha256': evidence['sha256'], 'encodedParallaxPixels': evidence['encodedParallax']['relativeHorizontalPixels'], 'actualBackends': evidence['actualBackends']}
        report['status'] = 'machine-tests-passed-visual-review-pending'
        report['exports'] = [str(motion / 'exports/kit-motion-test.mp4'), str(three / 'exports/coffee-shop-3d-silent-technical-test-v001.mp4')]
    except (Exception, KeyboardInterrupt) as error:
        report.update(status='blocked', blocker=str(error) or 'Interrupted; preserve run and logs')
        print('BLOCKED: ' + report['blocker'], file=sys.stderr)
    finally:
        save_report(dest, report)
        print('REPORT ' + str(dest / 'report.json'), flush=True)
    return 0 if report['status'].startswith('machine-tests-passed') else 1


def media():
    dest, report = fresh_run('media')
    try:
        venv = dest / 'venv'
        log = dest / 'media.log'
        run([sys.executable, '-m', 'venv', venv], ROOT, log)
        py = venv / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        run([py, '-m', 'pip', 'install', '-r', ROOT / 'requirements-media-observed.txt', '-r', ROOT / 'retrieval/requirements.txt'], ROOT, log)
        run([py, '-c', 'import PIL,numpy,faster_whisper,ctranslate2,huggingface_hub,av,onnxruntime,tokenizers,pypdf; print("Imports passed; models and inference NOT tested")'], ROOT, log)
        report.update(status='installed-import-tested-models-not-installed', interpreter=str(py), asr='blocked-until-approved-local-model-and-speech-test', research='needs-supplied-corpus-and-fresh-index')
    except (Exception, KeyboardInterrupt) as error:
        report.update(status='blocked', blocker=str(error) or 'Interrupted')
    finally:
        save_report(dest, report)
        print('REPORT ' + str(dest / 'report.json'))
    return 1 if report['status'] == 'blocked' else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='Read-only integrity/lock/prerequisite check (default)')
    mode.add_argument('--setup', action='store_true', help='New isolated npm projects + fresh 2D/3D encodes')
    mode.add_argument('--media', action='store_true', help='Optional isolated Python package installation; NO model download')
    parser.add_argument('--browser', help='Existing inspected compatible Chromium executable')
    parser.add_argument('--download-browser', action='store_true', help='Explicitly permit matching Chromium retrieval')
    parser.add_argument('--gl', choices=['angle', 'swangle'], default='angle')
    args = parser.parse_args(argv)
    try:
        manifest = integrity()
        locks = {name: audit_lock(ROOT / 'skills' / name / 'assets/template') for name in ['remotion-motion-graphics', 'remotion-3d-scenes']}
        checks = preflight()
        print(json.dumps({'filesVerified': len(manifest['files']), 'locks': locks, 'prerequisites': checks}, indent=2), flush=True)
        if args.setup:
            return setup(args, checks)
        if args.media:
            return media()
        return 0 if all(v['ok'] for v in checks.values()) else 1
    except (Exception, KeyboardInterrupt) as error:
        print('BLOCKED: ' + (str(error) or 'Interrupted'), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
