import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('starter_integrate', ROOT / 'integrate.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class IntegrationTests(unittest.TestCase):
    def source(self, root, names=('first-skill', 'second-skill')):
        for name in names:
            p = root / 'skills' / name / 'SKILL.md'
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('---\nname: ' + name + '\ndescription: "A portable test skill"\n---\nRead references from the canonical skill.\n', encoding='utf-8')
        return root

    def test_explicit_agents(self):
        self.assertEqual(m.choose_agent('hermes', {}), 'hermes')
        self.assertEqual(m.choose_agent('openclaw', {}), 'openclaw')

    def test_auto_detection_requires_unambiguous_runtime(self):
        self.assertEqual(m.choose_agent('auto', {'HERMES_HOME': 'example'}), 'hermes')
        self.assertEqual(m.choose_agent('auto', {'OPENCLAW_STATE_DIR': 'example'}), 'openclaw')
        for env in [{}, {'HERMES_HOME': 'a', 'OPENCLAW_STATE_DIR': 'b'}]:
            with self.assertRaisesRegex(ValueError, 'ambiguous'):
                m.choose_agent('auto', env)

    def test_openclaw_requires_actual_workspace(self):
        with self.assertRaisesRegex(ValueError, 'ACTUAL'):
            m.target_root('openclaw', env={})

    def test_openclaw_workspace_isolation(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(m.target_root('openclaw', workspace=d), Path(d).resolve() / 'skills')

    def test_hermes_requires_real_home_if_environment_absent(self):
        with self.assertRaisesRegex(ValueError, 'do not guess'):
            m.target_root('hermes', env={})

    def test_hermes_profile_home_override(self):
        with tempfile.TemporaryDirectory() as d:
            home = Path(d) / 'isolated-profile'
            self.assertEqual(m.target_root('hermes', env={'HERMES_HOME': str(home)}), home.resolve() / 'skills')
            self.assertEqual(m.target_root('hermes', hermes_home=d, env={'HERMES_HOME': str(home)}), Path(d).resolve() / 'skills')

    def test_explicit_skills_root(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(m.target_root('openclaw', skills_dir=d), Path(d).resolve())

    def test_plan_is_read_only(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.source(Path(d) / 'kit')
            target = Path(d) / 'profile/skills'
            entries = m.plan(root, target, 'hermes')
            self.assertFalse(target.exists())
            self.assertEqual([e['status'] for e in entries], ['create-entrypoint'] * 2)

    def test_install_and_idempotent_rerun(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.source(Path(d) / 'kit')
            target = Path(d) / 'profile/skills'
            self.assertEqual(len(m.apply(m.plan(root, target, 'hermes'))), 2)
            again = m.plan(root, target, 'hermes')
            self.assertTrue(all(e['status'] == 'identical-entrypoint-already-installed' for e in again))
            self.assertEqual(m.apply(again), [])

    def test_conflict_blocks_all_writes(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.source(Path(d) / 'kit')
            target = Path(d) / 'profile/skills'
            existing = target / 'second-skill/SKILL.md'
            existing.parent.mkdir(parents=True)
            existing.write_text('personal skill remains')
            entries = m.plan(root, target, 'hermes')
            with self.assertRaisesRegex(ValueError, 'No writes made'):
                m.apply(entries)
            self.assertEqual(existing.read_text(), 'personal skill remains')
            self.assertFalse((target / 'first-skill').exists())

    def test_existing_empty_skill_directory_is_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.source(Path(d) / 'kit', ('first-skill',))
            target = Path(d) / 'skills'
            (target / 'first-skill').mkdir(parents=True)
            self.assertEqual(m.plan(root, target, 'hermes')[0]['status'], 'conflict-preserved')

    def test_source_native_no_copy(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.source(Path(d))
            entries = m.plan(root, root / 'skills', 'openclaw')
            self.assertTrue(all(e['status'] == 'native-source-already-in-place' for e in entries))
            self.assertEqual(m.apply(entries), [])

    def test_hermes_wrapper_resolves_canonical_resources(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.source(Path(d))
            text = m.entrypoint(root, 'first-skill', 'hermes')
            self.assertIn('skill_view', text)
            self.assertIn(json.dumps(str(root / 'skills/first-skill/SKILL.md')), text)
            self.assertIn('CANONICAL skill directory', text)
            self.assertIn('Do not call OpenClaw functions from Hermes', text)

    def test_openclaw_wrapper_tool_boundary(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.source(Path(d))
            self.assertIn('Code Mode JavaScript', m.entrypoint(root, 'first-skill', 'openclaw'))

    def test_bad_name_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.source(Path(d), ('first-skill',))
            p = root / 'skills/first-skill/SKILL.md'
            p.write_text('---\nname: different-name\ndescription: Test\n---\n')
            with self.assertRaisesRegex(ValueError, 'mismatched'):
                m.entrypoint(root, 'first-skill', 'hermes')

    def test_symlink_destination_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'real').mkdir()
            try:
                (root / 'link').symlink_to(root / 'real', target_is_directory=True)
            except OSError:
                self.skipTest('Symlink creation unavailable under host policy')
            with self.assertRaisesRegex(ValueError, 'symlink'):
                m.real_path(root / 'link')

    def test_source_description_is_preserved(self):
        self.assertEqual(m.scalar('---\nname: a\ndescription: "Quoted: useful"\n---\n', 'description'), 'Quoted: useful')
        with self.assertRaises(ValueError):
            m.scalar('---\nname: a\ndescription: |\n  hidden multiline\n---\n', 'description')


if __name__ == '__main__':
    unittest.main()
