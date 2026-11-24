#!/usr/bin/env python3
"""Local-only evidence-led clip planning, accurate encoding and objective verification.
Python stdlib + existing ffmpeg/ffprobe. No source overwrite, downloads or inference.
"""
import argparse
from array import array
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

EXTENSIONS = {'.mp4', '.mov', '.mkv', '.webm', '.avi', '.m4v'}
SKILL = Path(__file__).resolve().parents[1]

class ClipError(Exception):
    pass


def run(argv, binary=False, timeout=1800):
    try:
        p = subprocess.run([str(x) for x in argv], shell=False, capture_output=True,
                           timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise ClipError('Local executable failed or timed out; run is not complete.') from e
    if p.returncode:
        raise ClipError('Local media operation failed; no completion report written. Private stderr: ' +
                        p.stderr.decode('utf-8', 'replace')[-3000:])
    return p.stdout if binary else p.stdout.decode('utf-8', 'replace')


def executable(name):
    p = shutil.which(name)
    if not p:
        raise ClipError('Missing existing executable: ' + name)
    return p


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def number(n, label):
    if isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n):
        raise ClipError(label + ' must be a finite number.')
    return float(n)


def source_file(value):
    if '://' in str(value) or str(value).startswith(('http:', 'https:', 'file:', 'concat:')):
        raise ClipError('Use a local file, not a URL/protocol/playlist. Download needs separate permission.')
    p = Path(value).expanduser().resolve(strict=True)
    if not p.is_file() or p.suffix.lower() not in EXTENSIONS:
        raise ClipError('Use an existing conventional local video file; no playlists.')
    return p


def within(path, root):
    return path == root or root in path.parents


def new_output(value, source, protected=()):
    raw = Path(value).expanduser()
    if '..' in raw.parts or raw.exists() or raw.is_symlink():
        raise ClipError('Output must be NEW, without traversal or overwrite.')
    # Resolve before confinement, including symlink/junction parents.
    p = raw.resolve()
    roots = [source.parent, SKILL.parent, *[Path(x).expanduser().resolve(strict=True) for x in protected]]
    # Reject conventional model/cache directories, plus explicitly supplied cached model roots.
    if any(x.lower() in {'models', 'model', '.cache', 'huggingface', 'hub'} for x in p.parts):
        raise ClipError('Output cannot be inside a model/cache directory.')
    if any(within(p, r) or within(r, p) for r in roots):
        raise ClipError('Output must be outside source, skills and protected/model folders.')
    if not p.parent.is_dir():
        raise ClipError('Output parent must already exist.')
    return p


def save(path, data):
    with path.open('x', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write('\n')


def probe(path, ffprobe):
    data = json.loads(run([ffprobe, '-v', 'error', '-protocol_whitelist', 'file,pipe',
                           '-show_streams', '-show_format', '-of', 'json', path]))
    if not data.get('streams'):
        raise ClipError('No streams.')
    return data


def select(data, kind, explicit):
    streams = [s for s in data['streams'] if s.get('codec_type') == kind and
               not s.get('disposition', {}).get('attached_pic')]
    if explicit is not None:
        if type(explicit) is not int:
            raise ClipError('Absolute stream indexes must be integers.')
        chosen = next((s for s in streams if s['index'] == explicit), None)
        if chosen is None:
            raise ClipError('Explicit ' + kind + ' stream index does not exist.')
        return chosen
    if len(streams) == 1:
        return streams[0]
    if not streams and kind == 'audio':
        return None
    # Never drop alternate tracks based only on default flag.
    raise ClipError('Ambiguous/missing ' + kind + ' stream: supply explicit absolute stream index and mapping_reason.')


def rate(s):
    try:
        return float(Fraction(s['avg_frame_rate']))
    except (ValueError, ZeroDivisionError, KeyError):
        raise ClipError('Unknown frame cadence.')


def compatible(data, v, a):
    """Deliberately conservative: no hidden VFR/offset/HDR/orientation conversion."""
    for obj in [data.get('format', {}), v, *([a] if a else [])]:
        try:
            start = float(obj.get('start_time', 'nan'))
        except ValueError:
            start = math.nan
        if not math.isfinite(start) or abs(start) > .000001:
            raise ClipError('Nonzero/unknown start offset unsupported; deliberate synchronized edit plan required.')
    if v.get('codec_name') != 'h264' or v.get('pix_fmt') != 'yuv420p':
        raise ClipError('Default supports SDR 8-bit yuv420p H264 only; deliberate codec/color plan required.')
    # Never infer progressive from missing/unknown metadata or flatten woven fields.
    if v.get('field_order') != 'progressive':
        raise ClipError('Interlaced/unknown field order unsupported; explicit progressive metadata required. No automatic deinterlace.')
    if v.get('color_transfer') in {'smpte2084', 'arib-std-b67'} or v.get('color_primaries') == 'bt2020':
        raise ClipError('HDR/wide-gamut requires a deliberate plan; no automatic tone map or retag.')
    allowed_color = {'unknown', 'unspecified', 'bt709', 'bt470bg', 'smpte170m'}
    for k in ('color_transfer', 'color_space', 'color_primaries'):
        if v.get(k, 'unknown') not in allowed_color:
            raise ClipError('Unreviewed color characteristic: deliberate plan required.')
    if v.get('color_range', 'unknown') not in {'tv', 'unknown', 'unspecified'}:
        raise ClipError('Full-range conversion requires a deliberate plan.')
    if v.get('side_data_list') or str(v.get('tags', {}).get('rotate', '0')) != '0':
        raise ClipError('Rotation/display/HDR side data requires a deliberate plan; default does not discard it.')
    if v.get('width', 0) % 2 or v.get('height', 0) % 2:
        raise ClipError('Odd dimensions unsupported by default H264 encoder.')
    fps = rate(v)
    if not 1 <= fps <= 240:
        raise ClipError('Unsupported frame rate.')
    if a and a.get('codec_name') != 'aac':
        raise ClipError('Default supports AAC audio only; deliberate audio plan required.')
    if a and (a.get('channels', 0) not in {1, 2} or a.get('channel_layout') not in {'mono', 'stereo'}):
        raise ClipError('Unsupported audio layout; no silent downmix.')
    # MP4 reported stream duration is the authoritative playable bound here.
    try:
        duration = float(v['duration'])
        if a:
            duration = min(duration, float(a['duration']))
    except (ValueError, KeyError):
        raise ClipError('Unknown stream duration unsupported.')
    if not math.isfinite(duration) or duration <= 0:
        raise ClipError('Invalid stream duration.')
    return fps, duration


def frames(path, index, ffprobe):
    obj = json.loads(run([ffprobe, '-v', 'error', '-protocol_whitelist', 'file,pipe',
                          '-select_streams', str(index), '-show_frames',
                          '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', path]))
    pts = [float(f['best_effort_timestamp_time']) for f in obj.get('frames', [])]
    if len(pts) < 2 or any(not math.isfinite(p) for p in pts):
        raise ClipError('Insufficient or invalid decoded frame timestamps.')
    return pts


def check_audio_timeline(path, index, ffprobe):
    data = json.loads(run([ffprobe, '-v', 'error', '-protocol_whitelist', 'file,pipe',
                           '-select_streams', str(index), '-show_frames',
                           '-show_entries', 'frame=best_effort_timestamp_time,nb_samples,sample_rate',
                           '-of', 'json', path]))
    rows = data.get('frames', [])
    meta = probe(path, ffprobe)
    selected = next(s for s in meta['streams'] if s['index'] == index)
    hz = int(selected['sample_rate'])
    if not rows or abs(float(rows[0]['best_effort_timestamp_time'])) > 1/hz + .000002:
        raise ClipError('Audio decoded start offset unsupported.')
    for left,right in zip(rows,rows[1:]):
        expected = float(left['best_effort_timestamp_time']) + int(left['nb_samples']) / hz
        if abs(float(right['best_effort_timestamp_time'])-expected) > 1/hz + .000002:
            raise ClipError('Audio decoded timestamp gap/overlap unsupported; preserve source synchronization deliberately.')
    return {'decoded_audio_frames':len(rows),'timeline':'continuous at original sample rate'}


def check_cfr(pts, fps):
    step = 1 / fps
    if abs(pts[0]) > .0001 or any(abs((b-a)-step) > .0001 for a,b in zip(pts, pts[1:])):
        raise ClipError('VFR/gapped/nonzero video timestamps unsupported; no forced CFR conversion.')


def load_manifest(value):
    with Path(value).open(encoding='utf-8') as f:
        obj = json.load(f, parse_constant=lambda x: (_ for _ in ()).throw(ClipError('Nonfinite JSON number.')))
    if not isinstance(obj, dict):
        raise ClipError('Manifest must be an object.')
    allowed = {'schema_version','source_sha256','requested_count','duration_seconds','allow_overlap',
               'overlap_reason','explicit_ranges','range_authorization','clips','video_stream','audio_stream',
               'mapping_reason','coverage','selection_basis','length_mode'}
    if set(obj) - allowed:
        raise ClipError('Unknown manifest fields; arbitrary FFmpeg arguments/output paths are forbidden.')
    return obj


def plan(manifest, duration, fps, source_hash):
    if manifest.get('schema_version') != 1 or manifest.get('source_sha256') != source_hash:
        raise ClipError('Manifest schema/hash must match inspected source.')
    count = manifest.get('requested_count')
    if type(count) is not int or not 1 <= count <= 100:
        raise ClipError('requested_count must be an explicit integer 1..100.')
    rows = manifest.get('clips')
    if not isinstance(rows, list) or len(rows) != count:
        raise ClipError('Clip count must match requested_count exactly.')
    for key in ('allow_overlap', 'explicit_ranges'):
        if key in manifest and type(manifest[key]) is not bool:
            raise ClipError(key + ' must be Boolean.')
    overlap = manifest.get('allow_overlap', False)
    explicit = manifest.get('explicit_ranges', False)
    if overlap and not manifest.get('overlap_reason'):
        raise ClipError('Overlap needs explicit user permission recorded in overlap_reason.')
    if explicit and not manifest.get('range_authorization'):
        raise ClipError('Explicit user ranges need user timestamp authorization recorded.')
    # Backward compatible explicit duration/ranges; an untimed request is thought-led.
    # Generic clipping authorizes agent-selected semantic boundaries, not a claim that
    # the user supplied timestamps. The deterministic helper never guesses meaning.
    inferred_mode = 'user_ranges' if explicit else ('fixed' if 'duration_seconds' in manifest else 'thought_led')
    mode = manifest.get('length_mode', inferred_mode)
    if not isinstance(mode, str) or mode not in {'thought_led', 'fixed', 'user_ranges'}:
        raise ClipError('length_mode must be thought_led, fixed or user_ranges.')
    if mode != inferred_mode:
        raise ClipError('length_mode conflicts with explicit duration/ranges; honor the user timing constraint, not a silent override.')
    length = None
    if 'duration_seconds' in manifest:
        length = number(manifest['duration_seconds'], 'duration_seconds')
        if length <= 0:
            raise ClipError('Duration must be positive.')
    if mode == 'fixed' and not overlap and count * length > duration + 1e-6:
        raise ClipError('Insufficient unique source duration for %d clips of %g seconds. Ask: fewer clips, shorter clips, or authorized overlap?' % (count, length))
    if not manifest.get('selection_basis') or not manifest.get('coverage'):
        raise ClipError('Record editorial selection basis and complete coverage/evidence, not fabricated highlights.')
    result = []
    for row in rows:
        if not isinstance(row, dict) or set(row) - {'start','end','title','reason','evidence'}:
            raise ClipError('Clip fields must be start/end/title/reason/evidence only.')
        if any(not isinstance(row.get(k), str) or not row[k].strip() for k in ('title','reason','evidence')):
            raise ClipError('Every clip requires a title, editorial reason and traceable evidence.')
        start = number(row.get('start'), 'start')
        if mode == 'fixed':
            end = start + length
            if 'end' in row and abs(number(row['end'], 'end') - end) > 1e-6:
                raise ClipError('Requested fixed duration differs from end; ask the smallest timing/complete-idea tradeoff, no silent extension.')
        else:
            if 'end' not in row:
                raise ClipError('Incomplete plan: %s requires each selected start/end; review complete context and choose a coherent thought. No implicit fixed duration or automatic thought detection.' % mode)
            end = number(row['end'], 'end')
        if not 0 <= start < end <= duration + 1e-6:
            raise ClipError('Require 0 <= start < end <= selected playable duration.')
        # Fixed cadence cannot encode arbitrary fractional-frame lengths without rounding.
        # Require frame-grid starts rather than quietly shifting source timestamps.
        if abs(start * fps - round(start * fps)) > .0001:
            raise ClipError('Start must lie on the source frame grid; explicitly select a nearby frame-aligned start.')
        # Selected lengths at fractional cadence may not be integer frame counts:
        # permit only unavoidable sub-frame quantization, not editorial extension.
        if end - start < 2 / fps:
            raise ClipError('Clip must contain at least two frames.')
        if any(abs(start-r['start']) < 1e-6 and abs(end-r['end']) < 1e-6 for r in result):
            raise ClipError('Duplicate ranges forbidden even with overlap permission.')
        if not overlap and any(start < r['end'] - 1e-6 and end > r['start'] + 1e-6 for r in result):
            raise ClipError('Overlapping clips require explicit permission.')
        result.append(dict(row, start=start, end=end))
    return result


def decode_frame(path, index, timestamp, ffmpeg):
    return run([ffmpeg, '-nostdin','-v','error','-threads','1','-protocol_whitelist','file,pipe',
                '-ss', str(timestamp), '-i', path, '-map', '0:'+str(index), '-frames:v','1',
                '-threads','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'], binary=True)


def compare_frames(source, vindex, clip, outindex, start, duration, fps, ffmpeg):
    rows = []
    for t in (0, math.floor(duration * fps / 2) / fps, duration - 1/fps):
        before = decode_frame(source, vindex, start+t, ffmpeg)
        after = decode_frame(clip, outindex, t, ffmpeg)
        if not before or len(before) != len(after):
            raise ClipError('Decoded frame dimensions/availability mismatch.')
        mae = sum(abs(x-y) for x,y in zip(before,after)) / len(before)
        if mae > 16:
            raise ClipError('Source/output sampled decoded frame mismatch; investigate timeline or encode.')
        rows.append({'output_seconds':t,'source_seconds':start+t,'rgb_mean_absolute_error':mae})
    return rows


def audio_excerpt(path, index, start, ffmpeg, seconds=.2):
    raw = run([ffmpeg,'-nostdin','-v','error','-threads','1','-protocol_whitelist','file,pipe',
               '-ss',str(start),'-i',path,'-map','0:'+str(index),'-t',str(seconds),
               '-ar','16000','-f','f32le','pipe:1'],binary=True)
    values=array('f')
    values.frombytes(raw)
    if not values or any(not math.isfinite(x) for x in values):
        raise ClipError('Missing/nonfinite decoded audio excerpt.')
    return values


def compare_audio(source, aindex, clip, start, duration, ffmpeg):
    result=[]
    seconds=min(.2,duration/4)
    for t in (seconds, duration/2, duration-2*seconds):
        before=audio_excerpt(source,aindex,start+t,ffmpeg,seconds)
        after=audio_excerpt(clip,1,t,ffmpeg,seconds)
        if len(before)!=len(after):
            raise ClipError('Audio excerpt sample count differs.')
        power=sum(x*x for x in before)/len(before)
        other=sum(x*x for x in after)/len(after)
        corr=None
        if power > 1e-8 and other > 1e-8:
            corr=sum(x*y for x,y in zip(before,after))/len(before)/math.sqrt(power*other)
            if corr < .9:
                raise ClipError('Sampled source/output audio content mismatch; investigate timing/encode.')
        elif max(power,other)>1e-7:
            raise ClipError('Sampled audio silence/content mismatch.')
        result.append({'output_seconds':t,'source_seconds':start+t,'pcm_correlation':corr,
                       'note':'Sampled original-channel interleaved PCM; null correlation for near-silence'})
    return result


def verify(path, v, a, length, fps, ffprobe, ffmpeg):
    data = probe(path, ffprobe)
    ov = select(data, 'video', None)
    oa = select(data, 'audio', None)
    if len(data['streams']) != (2 if a else 1) or bool(oa) != bool(a):
        raise ClipError('Unexpected output stream count.')
    if any(ov.get(k) != v.get(k) for k in ('width','height','sample_aspect_ratio','display_aspect_ratio')):
        raise ClipError('Dimensions/aspect changed.')
    if ov.get('codec_name') != 'h264' or ov.get('pix_fmt') != v.get('pix_fmt'):
        raise ClipError('Unexpected video format.')
    if v.get('field_order') != 'progressive' or ov.get('field_order') != v.get('field_order'):
        raise ClipError('Output field order changed or source is not explicitly progressive.')
    for k in ('color_range','color_space','color_transfer','color_primaries'):
        if ov.get(k) != v.get(k):
            raise ClipError('Output color metadata changed: '+k)
    pts = frames(path, ov['index'], ffprobe)
    check_cfr(pts, fps)
    expected = math.ceil(length*fps - 1e-7)
    if len(pts) != expected or abs(float(ov['duration'])-length) > 1/fps + .0002:
        raise ClipError('Video frame count/duration mismatch.')
    audio_tolerance = None
    audio_timeline = None
    if a:
        audio_timeline = check_audio_timeline(path,oa['index'],ffprobe)
        if any(oa.get(k) != a.get(k) for k in ('channels','channel_layout','sample_rate')):
            raise ClipError('Audio layout/rate changed.')
        audio_tolerance = 1024/int(a['sample_rate']) + .002
        if abs(float(oa.get('start_time','nan'))) > .002 or abs(float(oa['duration'])-length) > audio_tolerance:
            raise ClipError('Audio start/duration sync mismatch.')
    run([ffmpeg,'-nostdin','-v','error','-xerror','-threads','1','-protocol_whitelist','file,pipe',
         '-i',path,'-map','0:v:0',*(['-map','0:a:0'] if a else []),'-threads','1','-f','null','-'])
    return {'status':'passed','metadata':data,'video_frames':len(pts),'frame_tolerance_seconds':1/fps,
            'audio_packet_tolerance_seconds':audio_tolerance,'audio_timeline':audio_timeline,'full_decode':'passed',
            'sync_check':'aligned starts/durations; not human perceptual lip-sync review'}


def execute(args):
    source = source_file(args.input)
    ffprobe, ffmpeg = executable(args.ffprobe), executable(args.ffmpeg)
    before = digest(source)
    data = probe(source, ffprobe)
    if args.action == 'probe':
        report = {'status':'inspected','source_path':str(source),'source_sha256':before,
                  'metadata':data,'note':'Raw private metadata; compatibility checked by plan/render.'}
        if args.output:
            output = new_output(args.output, source, args.protect)
            output.mkdir()
            save(output/'probe.json',report)
        print(json.dumps(report, indent=2))
        if digest(source) != before:
            raise ClipError('Source changed during probe.')
        return
    if not args.manifest or not args.output:
        raise ClipError('plan/render require --manifest and NEW --output.')
    output = new_output(args.output, source, args.protect)
    manifest = load_manifest(args.manifest)
    v = select(data,'video',manifest.get('video_stream'))
    a = select(data,'audio',manifest.get('audio_stream'))
    if any(len([s for s in data['streams'] if s.get('codec_type') == kind and
                not s.get('disposition',{}).get('attached_pic')]) > 1 for kind in ('video','audio')):
        if not manifest.get('mapping_reason'):
            raise ClipError('Alternate tracks require an evidenced/user-authorized mapping_reason; no silent dropping.')
    fps, duration = compatible(data,v,a)
    rows = plan(manifest,duration,fps,before)
    pts = frames(source,v['index'],ffprobe)
    check_cfr(pts,fps)
    if a:
        check_audio_timeline(source,a['index'],ffprobe)
    if abs(len(pts)/fps - float(v['duration'])) > 1/fps:
        raise ClipError('Source decoded duration differs from metadata.')
    versions = {name: run([tool,'-version']).splitlines()[0] for name,tool in [('ffmpeg',ffmpeg),('ffprobe',ffprobe)]}
    output.mkdir()
    report = {'schema_version':1,'status':'incomplete','source_path':str(source),'source_sha256':before,
              'tools':versions,'request':manifest,'selected_clips':rows,'source_metadata':data,
              'selected_stream_indexes':{'video':v['index'],'audio':a['index'] if a else None},
              'output_spec':{'container':'mp4','video':'libx264 CRF18 original geometry/cadence',
                             'audio':'AAC 192k original rate/layout (lossy reencode)' if a else 'none',
                             'fps':fps,'dimensions':[v['width'],v['height']],
                             'color':'no retag/tone map; verified metadata unchanged'},
              'privacy':'Private source content/evidence; no upload/publication performed.', 'clips':[]}
    save(output/'manifest.incomplete.json',report)
    if args.action == 'plan':
        if digest(source) != before:
            raise ClipError('Source changed during planning.')
        report['status']='planned_not_rendered'
        report['source_hash_unchanged']=True
        save(output/'plan.json',report)
        print('Validated plan only: '+str(output/'plan.json'))
        return
    for i,row in enumerate(rows,1):
        length = row['end']-row['start']
        name = 'clip-%03d.mp4' % i
        path = output/name
        # Accurate input seeking decodes/discards before selected boundary. Only supported zero-origin
        # synchronous streams are accepted, so shared -ss keeps original relative timing intact.
        cmd = [ffmpeg,'-nostdin','-v','error','-xerror','-n','-threads','1',
               '-protocol_whitelist','file,pipe','-ss',str(row['start']),'-noautorotate','-i',source,
               '-t',str(length),'-map','0:'+str(v['index'])]
        if a:
            cmd += ['-map','0:'+str(a['index'])]
        cmd += ['-map_metadata','-1','-map_chapters','-1','-c:v','libx264','-preset','fast','-crf','18',
                '-threads','1','-fps_mode','passthrough']
        if a:
            cmd += ['-c:a','aac','-b:a','192k','-ar',a['sample_rate']]
        cmd += ['-movflags','+faststart',path]
        run(cmd)
        qa = verify(path,v,a,length,fps,ffprobe,ffmpeg)
        qa['sampled_source_frame_comparison'] = compare_frames(source,v['index'],path,0,row['start'],length,fps,ffmpeg)
        if a:
            qa['sampled_source_audio_comparison'] = compare_audio(source,a['index'],path,row['start'],length,ffmpeg)
        proofs=[]
        for label,t in zip(('first','middle','end'),(0,math.floor(length*fps/2)/fps,length-1/fps)):
            proof = output/('clip-%03d-%s.jpg' % (i,label))
            run([ffmpeg,'-nostdin','-v','error','-n','-threads','1','-protocol_whitelist','file,pipe',
                 '-ss',str(t),'-i',path,'-map','0:v:0','-frames:v','1','-threads','1','-q:v','2','-update','1',proof])
            if not proof.is_file() or not proof.stat().st_size:
                raise ClipError('Missing proof image.')
            proofs.append({'path':str(proof),'output_seconds':t})
        report['clips'].append({'file':str(path),'sha256':digest(path),'selection':row,'verification':qa,'proofs':proofs})
        save(output/('clip-%03d-verification.json'%i),report['clips'][-1])
    if len(report['clips']) != manifest['requested_count'] or digest(source) != before:
        raise ClipError('Count/source preservation check failed; no complete report.')
    report['source_hash_after']=digest(source)
    report['source_hash_unchanged']=True
    report['status']='complete'
    report['human_playback']='not performed by helper; sampled objective checks are not semantic/privacy clearance'
    save(output/'report.json',report)
    print('Complete: %d verified local clips. Report: %s' % (len(rows),output/'report.json'))


def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['probe','plan','render'])
    p.add_argument('--input',required=True)
    p.add_argument('--manifest')
    p.add_argument('--output',help='NEW directory; existing parent outside source/skills/model folders')
    p.add_argument('--protect',action='append',default=[],help='Existing cached model or other protected root; repeatable')
    p.add_argument('--ffmpeg',default='ffmpeg')
    p.add_argument('--ffprobe',default='ffprobe')
    return p

if __name__=='__main__':
    try:
        execute(parser().parse_args())
    except (ClipError,OSError,ValueError,KeyError,TypeError) as e:
        print('ERROR (private diagnostics): '+str(e),file=sys.stderr)
        sys.exit(2)
