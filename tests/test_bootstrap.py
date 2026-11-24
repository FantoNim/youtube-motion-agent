import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('starter_bootstrap', ROOT / 'bootstrap.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


class BootstrapTests(unittest.TestCase):
    def test_safe_relative_path(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.assertEqual(b.safe_path(root, 'skills/example/SKILL.md'), root / 'skills/example/SKILL.md')

    def test_path_traversal_and_absolute_paths_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            for rel in ['', '../escape', '/etc/passwd', 'C:/Users/example/x', 'C:relative', 'a/../../escape', 'a' + chr(92) + 'b']:
                with self.subTest(path=rel), self.assertRaises(ValueError):
                    b.safe_path(Path(d), rel)

    def test_hash_success_missing_and_changed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            f = root / 'file.txt'
            f.write_bytes(b'approved bytes')
            (root / 'manifest.json').write_text(json.dumps({'files': {'file.txt': hashlib.sha256(f.read_bytes()).hexdigest()}}))
            self.assertEqual(len(b.integrity(root)['files']), 1)
            f.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'Hash mismatch'):
                b.integrity(root)
            f.unlink()
            with self.assertRaisesRegex(ValueError, 'Missing'):
                b.integrity(root)

    def test_manifest_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'manifest.json').write_text(json.dumps({'files': {'../escape': '0' * 64}}))
            with self.assertRaises(ValueError):
                b.integrity(root)

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as outside:
            root = Path(d)
            try:
                (root / 'link').symlink_to(Path(outside), target_is_directory=True)
            except OSError:
                self.skipTest('Symlink creation unavailable under this host policy')
            with self.assertRaises(ValueError):
                b.safe_path(root, 'link/file')

    def test_unlisted_resource_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'known.txt').write_bytes(b'known')
            (root / 'manifest.json').write_text(json.dumps({'files': {'known.txt': hashlib.sha256(b'known').hexdigest()}}))
            (root / 'helpers').mkdir()
            (root / 'helpers/unlisted.py').write_text('print("unexpected")')
            with self.assertRaisesRegex(ValueError, 'Unlisted'):
                b.integrity(root)

    def fixture_lock(self, root):
        (root / 'package.json').write_text(json.dumps({'dependencies': {'remotion': '4.0.538'}, 'overrides': {'zod': '4.6.6'}}))
        lock = {'packages': {'': {}, 'node_modules/remotion': {'version': '4.0.538', 'resolved': 'https://registry.npmjs.org/remotion/-/remotion-4.0.538.tgz', 'integrity': 'sha512-fixture'}}}
        (root / 'package-lock.json').write_text(json.dumps(lock))
        return lock

    def test_reviewed_lock_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.fixture_lock(root)
            self.assertEqual(b.audit_lock(root)['packages'], 1)

    def test_unexpected_lock_origin_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            lock = self.fixture_lock(root)
            lock['packages']['node_modules/remotion']['resolved'] = 'https://unapproved.invalid/pkg.tgz'
            (root / 'package-lock.json').write_text(json.dumps(lock))
            with self.assertRaisesRegex(ValueError, 'origin'):
                b.audit_lock(root)

    def test_missing_integrity_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            lock = self.fixture_lock(root)
            del lock['packages']['node_modules/remotion']['integrity']
            (root / 'package-lock.json').write_text(json.dumps(lock))
            with self.assertRaises(ValueError):
                b.audit_lock(root)

    def test_wrong_pin_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            lock = self.fixture_lock(root)
            lock['packages']['node_modules/remotion']['version'] = '4.0.999'
            (root / 'package-lock.json').write_text(json.dumps(lock))
            with self.assertRaisesRegex(ValueError, 'pin mismatch'):
                b.audit_lock(root)

    def test_empty_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'manifest.json').write_text('{"files": {}}')
            with self.assertRaisesRegex(ValueError, 'Empty'):
                b.integrity(root)


if __name__ == '__main__':
    unittest.main()
