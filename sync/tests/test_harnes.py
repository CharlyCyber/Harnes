import importlib.util
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('harnes', ROOT / 'sync/harnes.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.repo = base / 'repo'
        self.home = base / 'home'
        (self.repo / 'sync').mkdir(parents=True)
        (self.repo / 'skills/alpha').mkdir(parents=True)
        (self.repo / 'skills/beta').mkdir(parents=True)
        (self.repo / 'skills/alpha/SKILL.md').write_text('alpha', encoding='utf-8')
        (self.repo / 'skills/beta/SKILL.md').write_text('beta', encoding='utf-8')
        (self.repo / 'global.md').write_text('RULES', encoding='utf-8')
        cfg = {'universal': {'skills': '~/.agents/skills'},
               'instructions': [{'source': 'global.md', 'dest': '~/.agents/AGENTS.md', 'always': True},
                                {'source': 'global.md', 'dest': '~/.claude/CLAUDE.md'}],
               'clients': [{'id': 'claude', 'path': '~/.claude/skills'}],
               'profiles': {'core': ['alpha'], 'all': 'all'}}
        (self.repo / 'sync/targets.json').write_text(json.dumps(cfg), encoding='utf-8')
        (self.home / '.claude/skills').mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def sync(self, **kw):
        h.sync(self.repo, self.home, **kw)

    def test_install_idempotent_verify_and_instruction_preservation(self):
        doc = self.home / '.claude/CLAUDE.md'
        doc.write_text('My own rules\n', encoding='utf-8')
        self.sync()
        a = self.home / '.agents/skills/alpha'
        self.assertTrue(h.same_link(a, self.repo / 'skills/alpha'))
        self.assertTrue(h.same_link(self.home / '.claude/skills/alpha', self.repo / 'skills/alpha'))
        self.assertIn('My own rules', doc.read_text())
        self.sync(check=True)
        self.sync()
        self.assertEqual(doc.read_text().count(h.BEGIN), 1)
        (self.repo / 'global.md').write_text('NEW RULES', encoding='utf-8')
        with self.assertRaises(RuntimeError): self.sync(check=True)
        self.sync()
        self.assertIn('NEW RULES', doc.read_text())
        self.assertIn('My own rules', doc.read_text())

    def test_conflicts_fail_before_mutating_and_adopt_backs_up(self):
        foreign = self.home / '.agents/skills/alpha'
        foreign.mkdir(parents=True)
        (foreign / 'SKILL.md').write_text('not ours')
        with self.assertRaises(RuntimeError): self.sync()
        self.assertFalse((self.home / '.harnes/state.json').exists())
        self.assertEqual((foreign / 'SKILL.md').read_text(), 'not ours')
        self.sync(adopt=True)
        self.assertTrue(h.same_link(foreign, self.repo / 'skills/alpha'))
        self.assertEqual(len(list((self.home / '.harnes/backups').rglob('SKILL.md'))), 1)

    def test_foreign_unchanged_and_only_own_stale_links_removed(self):
        other = self.home / '.agents/skills/other'
        other.mkdir(parents=True)
        (other / 'SKILL.md').write_text('foreign')
        self.sync(profile='all')
        self.sync(profile='core')
        self.assertFalse(h.exists(self.home / '.agents/skills/beta'))
        self.assertEqual((other / 'SKILL.md').read_text(), 'foreign')
        self.assertTrue((self.repo / 'skills/beta/SKILL.md').exists())
        self.sync(check=True)

    def test_modified_owned_link_not_removed(self):
        self.sync(profile='all')
        p = self.home / '.agents/skills/beta'
        h.unlink_link(p)
        p.mkdir()
        (p / 'important').write_text('keep')
        with self.assertRaises(RuntimeError): self.sync(profile='core')
        self.assertEqual((p / 'important').read_text(), 'keep')

    def test_legacy_directory_and_instructions_are_backed_up(self):
        old = self.home / '.claude/skills'
        old.rmdir()
        oldtarget = self.home / 'old-store'
        oldtarget.mkdir()
        (oldtarget / 'precious').write_text('keep')
        h.make_link(old, oldtarget)
        doc = self.home / '.claude/CLAUDE.md'
        doc.write_text('<!-- charli-harness:managed v0.1 -->\nold rules')
        with self.assertRaises(RuntimeError): self.sync()
        self.sync(adopt=True)
        self.assertEqual((oldtarget / 'precious').read_text(), 'keep')
        self.assertTrue(h.same_link(old / 'alpha', self.repo / 'skills/alpha'))
        self.assertEqual(len(list((self.home / '.harnes/backups').rglob('CLAUDE.md'))), 1)
        self.sync(check=True)

    def test_broken_and_unowned_link_collision(self):
        p = self.home / '.agents/skills/alpha'
        p.parent.mkdir(parents=True)
        h.make_link(p, self.repo / 'skills/beta')
        with self.assertRaises(RuntimeError): self.sync()
        self.assertTrue(h.same_link(p, self.repo / 'skills/beta'))

    def test_identical_foreign_link_is_not_claimed_or_pruned(self):
        foreign = self.home / '.agents/skills/beta'
        foreign.parent.mkdir(parents=True)
        h.make_link(foreign, self.repo / 'skills/beta')
        self.sync(profile='all')
        state = json.loads((self.home / '.harnes/state.json').read_text())
        self.assertNotIn(str(foreign.relative_to(self.home)), state['links'])
        self.sync(profile='core')
        self.assertTrue(h.same_link(foreign, self.repo / 'skills/beta'))

    def test_malformed_markers_never_overwrite(self):
        doc = self.home / '.claude/CLAUDE.md'
        doc.write_text('mine\n' + h.BEGIN)
        with self.assertRaises(ValueError): self.sync()
        self.assertTrue(doc.read_text().endswith(h.BEGIN))

    def test_preserves_crlf_and_trailing_content(self):
        doc = self.home / '.claude/CLAUDE.md'
        before = b'My rules  \r\n\r\n'
        doc.write_bytes(before)
        self.sync()
        self.assertTrue(doc.read_bytes().startswith(before))
        self.assertIn(b'\r\n' + h.BEGIN.encode(), doc.read_bytes())
        self.sync(check=True)

    def test_refuses_linked_ancestor(self):
        target = self.home / 'outside'
        target.mkdir()
        claude = self.home / '.claude'
        (claude / 'skills').rmdir()
        claude.rmdir()
        h.make_link(claude, target)
        with self.assertRaisesRegex(ValueError, 'intermedio'):
            self.sync()
        self.assertEqual(list(target.iterdir()), [])

    def test_bad_inventory_is_not_replaced(self):
        state = self.home / '.harnes/state.json'
        state.parent.mkdir()
        state.write_text('{bad')
        with self.assertRaises(json.JSONDecodeError): self.sync()
        self.assertEqual(state.read_text(), '{bad')


class RepositoryCLITests(unittest.TestCase):
    def test_actual_catalog_in_disposable_home(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            (home / '.claude').mkdir()
            base = [sys.executable, str(ROOT / 'sync/harnes.py'), '--home', temp]
            for args in (['sync'], ['verify'], ['sync', '--profile', 'all'],
                         ['verify'], ['sync', '--profile', 'core'], ['verify']):
                result = subprocess.run(base + args, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(h.same_link(home / '.agents/skills/charli-design', ROOT / 'skills/charli-design'))
            self.assertFalse(h.exists(home / '.agents/skills/hyperframes'))


class SecretTests(unittest.TestCase):
    def test_staged_content_and_remote_redaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            def git(*args):
                return subprocess.run(['git', '-C', tmp, *args], check=True, capture_output=True)
            git('init')
            secret = 'ghp_' + 'A' * 30
            (repo / 'file.txt').write_text(secret)
            git('add', 'file.txt')
            # Scan the index, even if the working tree was subsequently cleaned.
            (repo / 'file.txt').write_text('clean')
            r = subprocess.run([sys.executable, str(ROOT / 'hooks/check_secrets.py'), '--repo', tmp, '--staged'], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertNotIn(secret, r.stderr)
            git('add', 'file.txt')
            r = subprocess.run([sys.executable, str(ROOT / 'hooks/check_secrets.py'), '--repo', tmp, '--staged'], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            git('remote', 'add', 'origin', 'https://alice:' + secret + '@example.com/repo.git')
            r = subprocess.run([sys.executable, str(ROOT / 'hooks/check_secrets.py'), '--repo', tmp, '--staged'], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertNotIn(secret, r.stderr)

    def test_install_hook_and_block_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            hooks = repo / 'hooks'
            hooks.mkdir()
            for name in ('install_hook.py', 'check_secrets.py', 'pre-commit'):
                shutil.copy2(ROOT / 'hooks' / name, hooks / name)
            def git(*args, check=True):
                return subprocess.run(['git', '-C', tmp, *args], check=check, capture_output=True, text=True)
            git('init')
            git('config', 'user.email', 'test@example.invalid')
            git('config', 'user.name', 'Test')
            first = subprocess.run([sys.executable, str(hooks / 'install_hook.py')], capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            hookpath = git('rev-parse', '--git-path', 'hooks/pre-commit').stdout.strip()
            hookpath = Path(hookpath) if Path(hookpath).is_absolute() else repo / hookpath
            original = hookpath.read_bytes()
            second = subprocess.run([sys.executable, str(hooks / 'install_hook.py')], capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(hookpath.read_bytes(), original)
            secret = 'ghp_' + 'Z' * 30
            (repo / 'example.txt').write_text(secret)
            git('add', 'example.txt')
            blocked = git('commit', '-m', 'test', check=False)
            self.assertNotEqual(blocked.returncode, 0)
            self.assertIn('posible GitHub token', blocked.stderr)
            self.assertNotIn(secret, blocked.stderr)
            (repo / 'example.txt').write_text('clean')
            git('add', 'example.txt')
            result = git('commit', '-m', 'test', check=False)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
