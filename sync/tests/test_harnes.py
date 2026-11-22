import importlib.util
import io
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import call, patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('harnes', ROOT / 'sync/harnes.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.repo = base / 'repo & proyecto'
        self.home = base / 'home & prueba'
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


class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.repo = Path('/tmp/harnes-refresh-repo')
        self.home = Path('/tmp/harnes-refresh-home')

    def _git(self, cwd, *args):
        result = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def _git_fixture(self, base):
        remote, seed, checkout, home = (base / name for name in ('origin.git', 'seed', 'checkout', 'home'))
        self._git(base, 'init', '--bare', str(remote))
        seed.mkdir()
        self._git(seed, 'init')
        self._git(seed, 'checkout', '-b', 'main')
        self._git(seed, 'config', 'user.name', 'Harnes Test')
        self._git(seed, 'config', 'user.email', 'harnes-test@example.invalid')
        (seed / 'skills/alpha').mkdir(parents=True)
        (seed / 'skills/alpha/SKILL.md').write_text('alpha', encoding='utf-8')
        (seed / 'sync').mkdir()
        (seed / 'sync/targets.json').write_text(json.dumps({
            'universal': {'skills': '~/.agents/skills'},
            'instructions': [{'source': 'global.md', 'dest': '~/.agents/AGENTS.md', 'always': True},
                             {'source': 'global.md', 'dest': '~/.claude/CLAUDE.md'}],
            'clients': [{'id': 'claude', 'path': '~/.claude/skills'}],
            'profiles': {'core': ['alpha'], 'all': 'all'},
            'internal_skills': [],
        }), encoding='utf-8')
        (seed / 'global.md').write_text('managed rules v1', encoding='utf-8')
        self._git(seed, 'add', '.')
        self._git(seed, 'commit', '-m', 'initial')
        self._git(seed, 'remote', 'add', 'origin', str(remote))
        self._git(seed, 'push', '-u', 'origin', 'main')
        subprocess.run(['git', '--git-dir', str(remote), 'symbolic-ref', 'HEAD', 'refs/heads/main'], check=True)
        self._git(base, 'clone', str(remote), str(checkout))
        home.mkdir()
        (home / '.claude').mkdir()
        (home / '.agents').mkdir()
        (home / '.agents/AGENTS.md').write_text('my personal rules\n', encoding='utf-8')
        return remote, seed, checkout, home

    def test_refresh_fast_forwards_and_syncs_while_preserving_personal_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            remote, seed, checkout, home = self._git_fixture(Path(tmp))
            (seed / 'global.md').write_text('managed rules v2', encoding='utf-8')
            self._git(seed, 'add', 'global.md')
            self._git(seed, 'commit', '-m', 'update managed rules')
            expected = self._git(seed, 'rev-parse', 'HEAD')
            self._git(seed, 'push', 'origin', 'main')
            with patch.object(h, 'doctor'):
                with redirect_stdout(io.StringIO()):
                    result = h.refresh(checkout, home)
            self.assertEqual(result, 0)
            self.assertEqual(self._git(checkout, 'rev-parse', 'HEAD'), expected)
            self.assertTrue(h.same_link(home / '.agents/skills/alpha', checkout / 'skills/alpha'))
            managed = (home / '.agents/AGENTS.md').read_text(encoding='utf-8')
            self.assertIn('my personal rules', managed)
            self.assertIn('managed rules v2', managed)
            h.sync(checkout, home, check=True)

    def test_refresh_conflict_leaves_foreign_files_intact_without_adopt(self):
        with tempfile.TemporaryDirectory() as tmp:
            remote, seed, checkout, home = self._git_fixture(Path(tmp))
            (seed / 'global.md').write_text('managed rules v2', encoding='utf-8')
            self._git(seed, 'add', 'global.md')
            self._git(seed, 'commit', '-m', 'update managed rules')
            expected = self._git(seed, 'rev-parse', 'HEAD')
            self._git(seed, 'push', 'origin', 'main')
            foreign = home / '.agents/skills/alpha'
            foreign.mkdir(parents=True)
            (foreign / 'valuable.txt').write_text('keep this', encoding='utf-8')
            with patch.object(h, 'doctor'):
                stderr = io.StringIO()
                with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
                    result = h.refresh(checkout, home)
            self.assertEqual(result, 1)
            self.assertEqual(self._git(checkout, 'rev-parse', 'HEAD'), expected)
            self.assertEqual((foreign / 'valuable.txt').read_text(encoding='utf-8'), 'keep this')
            self.assertFalse((home / '.harnes/state.json').exists())
            self.assertIn('No se usó --adopt', stderr.getvalue())

    def test_refresh_validates_then_updates_syncs_and_verifies_without_adopt(self):
        with patch.object(h, 'assert_clean_checkout', return_value=self.repo) as preflight, \
             patch.object(h, 'doctor') as doctor, \
             patch.object(h, 'update_checkout', return_value=(True, '0123456789abcdef')) as update, \
             patch.object(h, 'sync') as sync:
            with redirect_stdout(io.StringIO()):
                result = h.refresh(self.repo, self.home)
        self.assertEqual(result, 0)
        preflight.assert_called_once_with(self.repo, 'main')
        doctor.assert_has_calls([call(self.repo, self.home, skip_sync=True),
                                 call(self.repo, self.home, skip_sync=True)])
        update.assert_called_once_with(self.repo, 'main')
        sync.assert_has_calls([call(self.repo, self.home),
                               call(self.repo, self.home, check=True)])

    def test_refresh_stops_on_managed_path_conflict_without_adopting(self):
        conflict = RuntimeError('conflicto, conservado: ~/.agents/skills/video')
        with patch.object(h, 'assert_clean_checkout', return_value=self.repo), \
             patch.object(h, 'doctor'), \
             patch.object(h, 'update_checkout', return_value=(True, '0123456789abcdef')), \
             patch.object(h, 'sync', side_effect=conflict) as sync:
            stderr = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
                result = h.refresh(self.repo, self.home)
        self.assertEqual(result, 1)
        sync.assert_called_once_with(self.repo, self.home)
        self.assertIn('No se usó --adopt', stderr.getvalue())
        self.assertIn('conservado', stderr.getvalue())

    def test_refresh_does_not_fetch_when_preflight_validation_fails(self):
        with patch.object(h, 'assert_clean_checkout', return_value=self.repo), \
             patch.object(h, 'doctor', side_effect=RuntimeError('validador ausente')) as doctor, \
             patch.object(h, 'update_checkout') as update, \
             patch.object(h, 'sync') as sync:
            stderr = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
                result = h.refresh(self.repo, self.home)
        self.assertEqual(result, 1)
        doctor.assert_called_once_with(self.repo, self.home, skip_sync=True)
        update.assert_not_called()
        sync.assert_not_called()


class RepositoryCLITests(unittest.TestCase):
    def test_refresh_command_is_exposed(self):
        result = subprocess.run([sys.executable, str(ROOT / 'sync/harnes.py'), 'refresh', '--help'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('clean main checkout', result.stdout)
        self.assertIn('safely syncs', result.stdout)

    def test_actual_catalog_in_disposable_home(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            (home / '.claude').mkdir()
            base = [sys.executable, str(ROOT / 'sync/harnes.py'), '--home', temp]
            for args in (['sync'], ['verify'], ['sync', '--profile', 'all'],
                         ['verify'], ['sync', '--profile', 'core'], ['verify']):
                result = subprocess.run(base + args, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                if args == ['sync', '--profile', 'all']:
                    for internal in json.loads((ROOT / 'sync/targets.json').read_text())['internal_skills']:
                        self.assertFalse(h.exists(home / '.agents/skills' / internal), internal)
                    self.assertTrue(h.exists(home / '.agents/skills/video'))
            self.assertTrue(h.same_link(home / '.agents/skills/web', ROOT / 'skills/web'))
            self.assertTrue(h.same_link(home / '.agents/skills/video', ROOT / 'skills/video'))
            for internal in json.loads((ROOT / 'sync/targets.json').read_text())['internal_skills']:
                self.assertFalse(h.exists(home / '.agents/skills' / internal), internal)
            # The real skill location still exposes its sibling modules through the checkout.
            self.assertTrue((home / '.agents/skills/video').resolve().parent.joinpath('hyperframes/SKILL.md').is_file())


class VideoTests(unittest.TestCase):
    def test_draw_on_is_deterministic_and_does_not_overwrite(self):
        script = ROOT / 'skills/video/scripts/draw_on.py'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'input.json'
            source.write_text(json.dumps({'width': 100, 'height': 200, 'strokes': [
                {'color': '#ffcc00', 'points': [[0, 0], [1, 1], [1, 0]]}]}))
            for name in ('a', 'b'):
                result = subprocess.run([sys.executable, str(script), str(source), str(root / name), '--frames', '3', '--fps', '2'], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((root / 'a/frame_0001.svg').read_bytes(), (root / 'b/frame_0001.svg').read_bytes())
            self.assertNotIn('<path', (root / 'a/frame_0000.svg').read_text())
            self.assertEqual((root / 'a/frame_0002.svg').read_text().count('<path'), 2)
            self.assertEqual(json.loads((root / 'a/manifest.json').read_text())['duration_seconds'], 1.5)
            result = subprocess.run([sys.executable, str(script), str(source), str(root / 'a')], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(len(list((root / 'a').glob('frame_*.svg'))), 3)
            source.write_text(json.dumps({'strokes': [{'points': [[0, 0], [1, 1]], 'color': '<bad>'}]}))
            result = subprocess.run([sys.executable, str(script), str(source), str(root / 'bad')], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / 'bad').exists())

    @unittest.skipUnless(shutil.which('node'), 'Node required for launcher test')
    def test_hyperframes_init_guard(self):
        wrapper = ROOT / 'skills/video/scripts/hyperframes_init.py'
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            package = base / 'package'
            (package / 'bin').mkdir(parents=True)
            (package / 'package.json').write_text(json.dumps({'name': 'hyperframes', 'version': '0.9.33'}))
            (package / 'bin/hyperframes.mjs').write_text(
                "import fs from 'node:fs'; fs.writeFileSync('calls.json', JSON.stringify({args:process.argv.slice(2),skip:process.env.HYPERFRAMES_SKIP_SKILLS,update:process.env.HYPERFRAMES_NO_UPDATE_CHECK,telemetry:process.env.HYPERFRAMES_NO_TELEMETRY}));")
            command = [sys.executable, str(wrapper), '--package-dir', str(package), str(base / 'new-project')]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            calls = json.loads((base / 'calls.json').read_text())
            self.assertEqual(calls['args'], ['init', 'new-project', '--non-interactive', '--example=blank'])
            self.assertEqual((calls['skip'], calls['update'], calls['telemetry']), ('1', '1', '1'))
            (base / 'new-project').mkdir()
            (base / 'calls.json').unlink()
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertFalse((base / 'calls.json').exists())
            (package / 'package.json').write_text(json.dumps({'name': 'hyperframes', 'version': '99.0.0'}))
            self.assertNotEqual(subprocess.run(command[:-1] + [str(base / 'other')], capture_output=True).returncode, 0)
            self.assertFalse((base / 'calls.json').exists())

    @unittest.skipUnless(os.environ.get('HARNES_TEST_HYPERFRAMES_PACKAGE'), 'optional real HyperFrames package not configured')
    def test_real_hyperframes_init_preserves_home_skills(self):
        wrapper = ROOT / 'skills/video/scripts/hyperframes_init.py'
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            home = base / 'home'
            skills = home / '.agents/skills'
            (skills / 'foreign').mkdir(parents=True)
            (skills / 'foreign/SKILL.md').write_text('sentinel')
            env = dict(os.environ, HOME=str(home), USERPROFILE=str(home),
                       APPDATA=str(home / 'AppData/Roaming'), LOCALAPPDATA=str(home / 'AppData/Local'))
            result = subprocess.run([sys.executable, str(wrapper), '--package-dir',
                                     os.environ['HARNES_TEST_HYPERFRAMES_PACKAGE'], str(base / 'film')],
                                    env=env, capture_output=True, text=True, timeout=90)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue((base / 'film/hyperframes.json').is_file())
            self.assertEqual(sorted(p.name for p in skills.iterdir()), ['foreign'])
            self.assertEqual((skills / 'foreign/SKILL.md').read_text(), 'sentinel')
            self.assertFalse((home / '.claude/skills').exists())
            self.assertFalse((home / '.codex/skills').exists())
            film = base / 'film'
            for unwanted in ('.agents', '.claude', 'skills'):
                self.assertFalse((film / unwanted).exists())

    def test_migrates_owned_internal_links_but_preserves_unmanaged(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            cfg = json.loads((ROOT / 'sync/targets.json').read_text())
            root = home / '.agents/skills'
            root.mkdir(parents=True)
            old = root / 'hyperframes'
            h.make_link(old, ROOT / 'skills/hyperframes')
            external = root / 'video-use'
            external.mkdir()
            (external / 'SKILL.md').write_text('third party')
            state = home / '.harnes/state.json'
            state.parent.mkdir()
            state.write_text(json.dumps({'version': 1, 'profile': 'all', 'links': {
                '.agents/skills/hyperframes': str((ROOT / 'skills/hyperframes').resolve())}}))
            h.sync(ROOT, home)
            self.assertFalse(h.exists(old))
            self.assertEqual((external / 'SKILL.md').read_text(), 'third party')
            self.assertTrue(h.same_link(root / 'video', ROOT / 'skills/video'))
            for name in cfg['internal_skills']:
                if name != 'video-use':
                    self.assertFalse(h.exists(root / name), name)
            h.sync(ROOT, home, check=True)


class HistoryScanTests(unittest.TestCase):
    def test_reachable_history_is_scanned_without_printing_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            def git(*args):
                return subprocess.run(['git', '-C', tmp, *args], check=True, capture_output=True)
            git('init')
            git('config', 'user.email', 'test@example.invalid')
            git('config', 'user.name', 'Test')
            secret = 'AKIA' + 'A' * 16
            (Path(tmp) / 'old.txt').write_text('clave ' + secret)
            (Path(tmp) / 'binary.bin').write_bytes(b'\x00' + secret.encode())
            git('add', '.')
            git('commit', '-m', 'first')
            (Path(tmp) / 'old.txt').unlink()
            git('add', '-A')
            git('commit', '-m', 'second')
            result = subprocess.run([sys.executable, str(ROOT / 'skills/security-audit/scripts/history_scan.py'), tmp],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn('AWS', result.stdout)
            self.assertNotIn(secret, result.stdout + result.stderr)
            self.assertIn('binarios omitidos: 1', result.stdout)
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['git', '-C', tmp, 'init'], check=True, capture_output=True)
            (Path(tmp) / 'safe.txt').write_text('sin credenciales')
            subprocess.run(['git', '-C', tmp, 'add', '.'], check=True, capture_output=True)
            subprocess.run(['git', '-C', tmp, '-c', 'user.name=T', '-c', 'user.email=t@example.invalid',
                            'commit', '-m', 'safe'], check=True, capture_output=True)
            result = subprocess.run([sys.executable, str(ROOT / 'skills/security-audit/scripts/history_scan.py'), tmp],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)


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
