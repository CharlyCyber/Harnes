import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('harnes_update', ROOT / 'sync/harnes.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.bare = base / 'origin.git'
        self.source = base / 'source'
        self.checkout = base / 'checkout'
        self.home = base / 'home'
        self.git(base, 'init', '--bare', str(self.bare))
        self.git(base, 'init', str(self.source))
        self.git(self.source, 'checkout', '-b', 'main')
        self.git(self.source, 'config', 'user.name', 'Harnes test')
        self.git(self.source, 'config', 'user.email', 'harnes-test@example.invalid')
        (self.source / 'version.txt').write_text('one\n', encoding='utf-8')
        (self.source / 'skills/alpha').mkdir(parents=True)
        (self.source / 'skills/alpha/SKILL.md').write_text('alpha skill\n', encoding='utf-8')
        (self.source / 'instructions').mkdir()
        (self.source / 'instructions/global.md').write_text('rules one\n', encoding='utf-8')
        (self.source / 'sync').mkdir()
        cfg = {'universal': {'skills': '~/.agents/skills'},
               'instructions': [{'source': 'instructions/global.md', 'dest': '~/.agents/AGENTS.md', 'always': True}],
               'clients': [], 'profiles': {'core': ['alpha'], 'all': 'all'}, 'internal_skills': []}
        (self.source / 'sync/targets.json').write_text(json.dumps(cfg), encoding='utf-8')
        self.git(self.source, 'add', '.')
        self.git(self.source, 'commit', '-m', 'initial')
        self.git(self.source, 'remote', 'add', 'origin', str(self.bare))
        self.git(self.source, 'push', '-u', 'origin', 'main')
        self.git(self.bare, 'symbolic-ref', 'HEAD', 'refs/heads/main', git_dir=True)
        self.git(base, 'clone', '--branch', 'main', str(self.bare), str(self.checkout))

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def git(cwd, *args, git_dir=False):
        command = ['git'] + (['--git-dir', str(cwd)] if git_dir else []) + list(args)
        result = subprocess.run(command, cwd=None if git_dir else str(cwd), capture_output=True, text=True)
        if result.returncode:
            raise AssertionError(f'git {args[0]} failed: {result.stderr}')
        return result.stdout.strip()

    def advance_remote(self):
        (self.source / 'version.txt').write_text('two\n', encoding='utf-8')
        self.git(self.source, 'add', 'version.txt')
        self.git(self.source, 'commit', '-m', 'update')
        self.git(self.source, 'push', 'origin', 'main')

    def test_fast_forwards_clean_main_checkout(self):
        self.advance_remote()
        changed, commit = h.update_checkout(self.checkout)
        self.assertTrue(changed)
        self.assertEqual((self.checkout / 'version.txt').read_text(encoding='utf-8'), 'two\n')
        self.assertEqual(self.git(self.checkout, 'rev-parse', 'HEAD'), commit)
        changed_again, same_commit = h.update_checkout(self.checkout)
        self.assertFalse(changed_again)
        self.assertEqual(same_commit, commit)

    def test_update_verifies_without_mutating_home(self):
        h.sync(self.checkout, self.home)
        self.advance_remote()
        result = h.update(self.checkout, self.home)
        self.assertEqual(result, 0)
        self.assertEqual((self.checkout / 'version.txt').read_text(encoding='utf-8'), 'two\n')
        self.assertIn('rules one', (self.home / '.agents/AGENTS.md').read_text(encoding='utf-8'))

    def test_update_reports_drift_without_running_sync(self):
        h.sync(self.checkout, self.home)
        (self.source / 'instructions/global.md').write_text('rules two\n', encoding='utf-8')
        self.git(self.source, 'add', 'instructions/global.md')
        self.git(self.source, 'commit', '-m', 'update instructions')
        self.git(self.source, 'push', 'origin', 'main')
        result = h.update(self.checkout, self.home)
        self.assertEqual(result, 2)
        self.assertIn('rules one', (self.home / '.agents/AGENTS.md').read_text(encoding='utf-8'))
        self.assertNotIn('rules two', (self.home / '.agents/AGENTS.md').read_text(encoding='utf-8'))

    def test_refuses_dirty_checkout_without_touching_work(self):
        local_file = self.checkout / 'version.txt'
        local_file.write_text('my local edits\n', encoding='utf-8')
        head_before = self.git(self.checkout, 'rev-parse', 'HEAD')
        with self.assertRaisesRegex(RuntimeError, 'cambios locales'):
            h.update_checkout(self.checkout)
        self.assertEqual(self.git(self.checkout, 'rev-parse', 'HEAD'), head_before)
        self.assertEqual(local_file.read_text(encoding='utf-8'), 'my local edits\n')

    def test_refuses_non_main_branch_without_switching(self):
        self.git(self.checkout, 'switch', '-c', 'work')
        with self.assertRaisesRegex(RuntimeError, 'rama work'):
            h.update_checkout(self.checkout)
        self.assertEqual(self.git(self.checkout, 'branch', '--show-current'), 'work')


if __name__ == '__main__':
    unittest.main()
