#!/usr/bin/env python3
"""Small, conservative cross-platform harness installer. No third-party runtime deps."""
import argparse
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import uuid

REPO = Path(__file__).resolve().parent.parent
BEGIN = '<!-- charli-harness:begin -->'
END = '<!-- charli-harness:end -->'


def exists(path):
    return os.path.lexists(str(path))


def is_link(path):
    try:
        info = os.lstat(path)
        return stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & 0x400)
    except FileNotFoundError:
        return False


def same_link(path, target):
    return is_link(path) and os.path.normcase(os.path.realpath(path)) == os.path.normcase(os.path.realpath(target))


def unlink_link(path):
    if not is_link(path):
        raise RuntimeError(f'No es un enlace: {path}')
    # A junction is removed as a directory, never recursively.
    if os.name == 'nt' and path.is_dir():
        os.rmdir(path)
    else:
        os.unlink(path)


def make_link(path, target):
    if os.name == 'nt':
        # Junctions do not require Developer Mode or elevation on Windows.
        env = dict(os.environ, HARNES_JUNCTION_LINK=str(path), HARNES_JUNCTION_TARGET=str(target))
        # On Windows, pass one command line: list2cmdline escapes embedded quotes
        # for C programs, but cmd.exe interprets those backslashes literally.
        # Paths are passed through quoted environment variables; Windows paths
        # cannot contain a quote, and delayed expansion is explicitly disabled.
        command = 'cmd.exe /d /v:off /c mklink /J "%HARNES_JUNCTION_LINK%" "%HARNES_JUNCTION_TARGET%"'
        result = subprocess.run(command, env=env, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(f'No se pudo crear junction {path}: {result.stderr or result.stdout}')
    else:
        os.symlink(str(target), str(path), target_is_directory=True)


def atomic_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
    fd, tmp = tempfile.mkstemp(prefix='.harnes-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as out:
            out.write(text)
        if mode is not None:
            os.chmod(tmp, mode)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def home_path(home, value):
    if not value.startswith('~/'):
        raise ValueError(f'Destino debe empezar por ~/: {value}')
    rel = Path(value[2:])
    if rel.is_absolute() or rel.drive or '..' in rel.parts:
        raise ValueError(f'Destino inseguro: {value}')
    return home / rel


def source_path(repo, value):
    rel = Path(value)
    if rel.is_absolute() or rel.drive or '..' in rel.parts:
        raise ValueError(f'Fuente insegura: {value}')
    path = repo / rel
    if not path.resolve().is_relative_to(repo.resolve()):
        raise ValueError(f'Fuente fuera del canon: {value}')
    return path


def merge_block(existing, content):
    newline = '\r\n' if '\r\n' in existing else '\n'
    block = BEGIN + newline + content.strip().replace('\r\n', '\n').replace('\n', newline) + newline + END
    if BEGIN in existing or END in existing:
        if existing.count(BEGIN) != 1 or existing.count(END) != 1:
            raise ValueError('marcadores de instrucciones ambiguos')
        start, end = existing.index(BEGIN), existing.index(END)
        if end < start:
            raise ValueError('marcadores de instrucciones invertidos')
        return existing[:start] + block + existing[end + len(END):]
    separator = '' if not existing else (newline if existing.endswith(('\n', '\r')) else newline + newline)
    return existing + separator + block + newline


def ensure_safe_parent(path, home):
    # Do not follow a redirected ancestor when writing or pruning an entry.
    current = home
    for part in path.relative_to(home).parts[:-1]:
        current = current / part
        if is_link(current):
            raise ValueError(f'Directorio intermedio es enlace: {current}; conservado')


def load_state(path):
    if is_link(path):
        raise ValueError('Inventario es un enlace; no se modificará')
    if not path.exists():
        return {'version': 1, 'links': {}}
    state = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(state, dict) or state.get('version') != 1 or not isinstance(state.get('links'), dict) or not all(isinstance(k, str) and isinstance(v, str) and Path(v).is_absolute() for k, v in state.get('links', {}).items()):
        raise ValueError('Inventario inválido; no se modificará nada')
    return state


def save_state(path, state):
    atomic_text(path, json.dumps(state, ensure_ascii=False, indent=2) + '\n')


def sync(repo, home, profile=None, check=False, adopt=False):
    cfg = json.loads((repo / 'sync/targets.json').read_text(encoding='utf-8-sig'))
    state_path = home / '.harnes/state.json'
    ensure_safe_parent(state_path, home)
    state = load_state(state_path)
    profile = profile or state.get('profile', 'core')
    if profile not in cfg['profiles']:
        raise ValueError('Perfil desconocido: ' + profile)
    skills = repo / 'skills'
    active = {p.name: p for p in skills.iterdir() if p.is_dir() and (p / 'SKILL.md').is_file() and not (p / '_DORMIDA.md').exists()}
    for name, src in active.items():
        if not src.resolve().is_relative_to(skills.resolve()):
            raise ValueError(f'Skill fuera del canon: {name}')
    internal = set(cfg.get('internal_skills', []))
    missing_internal = internal - active.keys()
    if missing_internal:
        raise ValueError('Módulos internos ausentes o dormidos: ' + ', '.join(sorted(missing_internal)))
    active = {k: v for k, v in active.items() if k not in internal}
    selected = cfg['profiles'][profile]
    if selected != 'all':
        missing = set(selected) - active.keys()
        if missing:
            raise ValueError('Skills del perfil ausentes o dormidas: ' + ', '.join(sorted(missing)))
        active = {k: active[k] for k in selected}
    skill_roots = [home_path(home, cfg['universal']['skills'])]
    for client in cfg['clients']:
        path = home_path(home, client['path'])
        if path.parent.is_dir():
            skill_roots.append(path)
    errors = []
    migrate_roots = []
    # Refuse whole-directory links: they might make writes hit an external manager's tree.
    for root in skill_roots:
        ensure_safe_parent(root, home)
        if is_link(root):
            if adopt and not check:
                migrate_roots.append(root)
            else:
                errors.append(f'{root}: enlace de directorio antiguo; usa --adopt para respaldarlo y migrar')
        elif exists(root) and not root.is_dir():
            errors.append(f'{root}: destino no es una carpeta; conservado')
    expected = {}
    for root in skill_roots:
        for name, src in active.items():
            dest = root / name
            expected[str(dest.relative_to(home))] = str(src.resolve())
    for rel, target in expected.items():
        path = home_path(home, '~/' + rel.replace('\\', '/'))
        if path.parent in migrate_roots:
            continue
        if exists(path) and not same_link(path, target) and not (rel in state['links'] and same_link(path, state['links'][rel])) and not adopt:
            errors.append(f'conflicto, conservado: {path} (usa --adopt para respaldarlo)')
        if check and not same_link(path, target):
            errors.append(f'DRIFT: {path}')
    instructions = []
    for item in cfg['instructions']:
        dst = home_path(home, item['dest'])
        ensure_safe_parent(dst, home)
        if not item.get('always') and not dst.parent.is_dir():
            continue
        src = source_path(repo, item['source'])
        if is_link(dst):
            errors.append(f'instrucciones son enlace, no se modifican: {dst}')
            continue
        if dst.exists():
            with dst.open('r', encoding='utf-8', newline='') as f:
                previous = f.read()
        else:
            previous = ''
        legacy = previous.lstrip('\ufeff \t\r\n').startswith('<!-- charli-harness:managed v0.1 -->')
        if legacy and not adopt:
            errors.append(f'instrucciones antiguas {dst}: usa --adopt para respaldarlas y migrar')
        desired = merge_block('' if legacy else previous, src.read_text(encoding='utf-8-sig'))
        instructions.append((dst, previous, desired, legacy))
        if check and previous != desired:
            errors.append(f'DRIFT: instrucciones {dst}')
    if check and state.get('profile') != profile:
        errors.append(f'DRIFT: perfil {profile} no instalado')
    for rel, oldtarget in state['links'].items():
        if rel in expected:
            continue
        p = home_path(home, '~/' + rel.replace('\\', '/'))
        ensure_safe_parent(p, home)
        if same_link(p, oldtarget):
            if check:
                errors.append(f'DRIFT: enlace obsoleto {p}')
        elif exists(p):
            errors.append(f'enlace gestionado modificado externamente, conservado: {p}')
    if errors:
        raise RuntimeError('\n'.join(errors))
    if check:
        print(f'Sincronizado: perfil {profile}, {len(active)} skills.')
        return
    state_path.parent.mkdir(parents=True, exist_ok=True)
    def backup_path(p):
        backup = home / '.harnes/backups' / uuid.uuid4().hex / p.relative_to(home)
        ensure_safe_parent(backup, home)
        backup.parent.mkdir(parents=True, exist_ok=True)
        # Same volume: rename the entry itself, never traverse a junction.
        os.replace(p, backup)
        print(f'Respaldo: {backup}')
    for root in migrate_roots:
        backup_path(root)
        root.mkdir(parents=True)
    state['profile'] = profile
    save_state(state_path, state)
    for rel, oldtarget in list(state['links'].items()):
        if rel not in expected:
            p = home_path(home, '~/' + rel.replace('\\', '/'))
            if same_link(p, oldtarget):
                unlink_link(p)
            del state['links'][rel]
            save_state(state_path, state)
    for rel, target in expected.items():
        p = home_path(home, '~/' + rel.replace('\\', '/'))
        if same_link(p, target):
            # Never claim ownership of another manager's identical link.
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        if exists(p):
            if rel in state['links'] and same_link(p, state['links'][rel]):
                unlink_link(p)
            else:
                backup_path(p)
        make_link(p, target)
        state['links'][rel] = target
        save_state(state_path, state)
    for dst, previous, desired, legacy in instructions:
        if previous != desired:
            if legacy and dst.exists():
                backup_path(dst)
            atomic_text(dst, desired)
    print(f'Listo: perfil {profile}, {len(active)} skills enlazadas al canon. Reinicia el agente.')


def doctor(repo, home, skip_sync=False):
    errors = []
    skills = [p for p in (repo / 'skills').iterdir() if p.is_dir() and (p / 'SKILL.md').exists() and not (p / '_DORMIDA.md').exists()]
    try:
        from skills_ref.validator import validate
        from skills_ref.parser import read_properties
    except ImportError:
        errors.append('Falta el validador: python -m pip install -r sync/requirements.txt')
    else:
        cfg = json.loads((repo / 'sync/targets.json').read_text(encoding='utf-8-sig'))
        descriptions = {}
        for skill in sorted(skills):
            issues = validate(skill)
            errors.extend(f'{skill.name}: {e}' for e in issues)
            if not issues:
                prop = read_properties(skill)
                descriptions[skill.name] = len(prop.name) + len(prop.description)
        internal = set(cfg.get('internal_skills', []))
        missing = internal - {p.name for p in skills}
        if missing:
            errors.append('Módulos internos ausentes o dormidos: ' + ', '.join(sorted(missing)))
        for profile, names in cfg['profiles'].items():
            if names != 'all' and internal.intersection(names):
                errors.append(f'Perfil {profile} expone módulos internos: ' + ', '.join(sorted(internal.intersection(names))))
            names = set(descriptions) - internal if names == 'all' else names
            size = sum(descriptions.get(name, 0) for name in names)
            if size > 8000:
                print(f'AVISO: perfil {profile}: {size} caracteres en nombres y descripciones; algunos clientes pueden truncar el catálogo.')
    for skill in skills:
        if (skill / skill.name).exists():
            errors.append(f'Carpeta duplicada: {skill.name}/{skill.name}')
    if not skip_sync:
        cfg = json.loads((repo / 'sync/targets.json').read_text(encoding='utf-8-sig'))
        universal = home_path(home, cfg['universal']['skills'])
        for raw in cfg.get('duplicate_sources', []):
            candidate = home_path(home, raw)
            if candidate.is_dir() and universal.is_dir():
                shared = sorted(p.name for p in candidate.iterdir()
                                if (p / 'SKILL.md').is_file() and (universal / p.name / 'SKILL.md').is_file())
                if shared:
                    print(f'AVISO: {len(shared)} nombres también en {raw}; revisar antes de retirar contenido ajeno.')
        try:
            sync(repo, home, check=True)
        except (RuntimeError, ValueError, OSError) as exc:
            errors.append(str(exc))
    try:
        result = subprocess.run([sys.executable, str(repo / 'hooks/check_secrets.py'), '--repo', str(repo)], check=False)
        if result.returncode:
            errors.append('Posibles secretos; revisa el aviso anterior.')
    except OSError as exc:
        errors.append(str(exc))
    if errors:
        raise RuntimeError('\n'.join(errors))
    print(f'Doctor: {len(skills)} entradas del canon válidas (incluidos módulos internos); sin errores detectados.')


def main():
    parser = argparse.ArgumentParser(description='Instala o verifica el harnés sin destruir contenido ajeno.')
    parser.add_argument('--home', type=Path, default=Path(os.environ.get('HARNES_HOME', str(Path.home()))))
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('sync', 'verify'):
        p = sub.add_parser(command)
        p.add_argument('--profile', choices=('core', 'all'), default=None)
        if command == 'sync':
            p.add_argument('--adopt', action='store_true', help='respaldar colisiones antes de instalar')
    p = sub.add_parser('doctor')
    p.add_argument('--skip-sync', action='store_true')
    args = parser.parse_args()
    home = args.home.expanduser().absolute()
    try:
        if args.command == 'doctor':
            doctor(REPO, home, args.skip_sync)
        else:
            sync(REPO, home, args.profile, args.command == 'verify', getattr(args, 'adopt', False))
        return 0
    except (RuntimeError, ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
