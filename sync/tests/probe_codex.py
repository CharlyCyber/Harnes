#!/usr/bin/env python3
"""Offline-oriented discovery probe; no model invocation or credential access."""
import argparse
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', required=True, help='path to an already installed Codex executable')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as temp:
        base = Path(temp)
        home = base / 'home'
        project = base / 'project'
        home.mkdir()
        project.mkdir()
        # Do not inherit API keys, account paths or user configuration.
        env = {k: os.environ[k] for k in ('PATH', 'SystemRoot', 'SYSTEMROOT', 'WINDIR', 'PATHEXT', 'TMP', 'TEMP') if k in os.environ}
        env.update(HOME=str(home), USERPROFILE=str(home), CODEX_HOME=str(home / '.codex'),
                   APPDATA=str(home / 'AppData/Roaming'), LOCALAPPDATA=str(home / 'AppData/Local'))
        sync = subprocess.run([sys.executable, str(ROOT / 'sync/harnes.py'), '--home', str(home), 'sync'],
                              env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if sync.returncode:
            raise RuntimeError('sync aislado falló: ' + sync.stderr)
        (home / '.codex').mkdir()
        executable = str(Path(args.codex).resolve())
        command = ([os.environ.get('COMSPEC', 'cmd.exe'), '/c', executable]
                   if os.name == 'nt' and executable.lower().endswith(('.cmd', '.bat')) else [executable])
        proc = subprocess.Popen(command + ['app-server'], env=env,
                                cwd=project, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, text=True, bufsize=1)
        messages = queue.Queue()
        def reader():
            for line in proc.stdout:
                messages.put(line)
        threading.Thread(target=reader, daemon=True).start()
        def send(obj):
            proc.stdin.write(json.dumps(obj) + '\n')
            proc.stdin.flush()
        def response(request_id):
            while True:
                try:
                    msg = json.loads(messages.get(timeout=30))
                except queue.Empty as exc:
                    raise RuntimeError('Codex no respondió en 30 segundos') from exc
                if msg.get('id') == request_id:
                    if 'error' in msg:
                        raise RuntimeError('Codex rechazó la solicitud: ' + str(msg['error']))
                    return msg['result']
        try:
            send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'harnes-probe', 'version': '1.0'}, 'capabilities': {}}})
            response(1)
            send({'method': 'initialized', 'params': {}})
            send({'id': 2, 'method': 'skills/list', 'params': {'cwds': [str(project)], 'forceReload': True}})
            data = response(2)['data'][0]
            skills = data['skills']
            video = [s for s in skills if s['name'] == 'video' and s.get('enabled')]
            cfg = json.loads((ROOT / 'sync/targets.json').read_text(encoding='utf-8'))
            internal = set(cfg['internal_skills'])
            expected = set(cfg['profiles']['core'])
            user_skills = {s['name'] for s in skills if s.get('scope') == 'user' and s.get('enabled')}
            leaked = internal.intersection(s['name'] for s in skills)
            if data.get('errors') or len(video) != 1 or leaked:
                raise RuntimeError('Descubrimiento inesperado: errores o módulos expuestos: ' + str(data.get('errors', [])) + ' ' + ', '.join(sorted(leaked)))
            if user_skills != expected:
                raise RuntimeError('Catálogo core inesperado: faltan ' + ', '.join(sorted(expected - user_skills)) + '; sobran ' + ', '.join(sorted(user_skills - expected)))
            if Path(video[0]['path']).resolve() != (ROOT / 'skills/video/SKILL.md').resolve():
                raise RuntimeError('video apunta a otra skill')
            system = len(skills) - len(user_skills)
            print(f'Codex: {len(user_skills)} skills core descubiertas, video una vez, {system} skills del sistema del cliente y ningún módulo interno.')
            print('No se invocó el modelo ni se verificó activación o acceso a referencias en una tarea.')
        finally:
            proc.terminate()
            proc.wait(timeout=10)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f'Probe falló: {exc}', file=sys.stderr)
        sys.exit(1)
