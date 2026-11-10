#!/usr/bin/env python3
"""Heuristic secret check. Never print matching content or remote URLs."""
import argparse
import re
import subprocess
import sys
from pathlib import Path

PATTERNS = {
    'GitHub token': re.compile(rb'(?<![A-Za-z0-9_])(?:gh[opsur]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})'),
    'API key': re.compile(rb'(?<![A-Za-z0-9_])(?:sk-[A-Za-z0-9_-]{20,}|fc-[a-f0-9]{30,}|apify_api_[A-Za-z0-9]{20,}|ctx7sk-[a-z0-9-]{10,})'),
    'AWS': re.compile(rb'(?<![A-Za-z0-9])AKIA[A-Z0-9]{16}(?![A-Z0-9])'),
    'Google': re.compile(rb'AIza[A-Za-z0-9_-]{30,}'),
    'Slack': re.compile(rb'xox[baprs]-[A-Za-z0-9-]{10,}'),
    'Credenciales en URL': re.compile(rb'://[^\s/@:]+:[^\s/@]{8,}@'),
    'Clave privada': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
}


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout


def scan(repo, staged):
    problems = []
    if staged:
        names = git(repo, 'diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z').split(b'\0')
    else:
        names = git(repo, 'ls-files', '-z').split(b'\0')
    for raw in filter(None, names):
        name = raw.decode('utf-8', 'surrogateescape')
        try:
            if staged:
                content = git(repo, 'show', ':' + name)
            else:
                p = repo / name
                if p.is_symlink() or not p.is_file():
                    continue
                content = p.read_bytes()
        except (subprocess.CalledProcessError, OSError) as exc:
            problems.append(f'No se pudo inspeccionar {name}: {type(exc).__name__}')
            continue
        if b'\0' in content:  # Binary data; not a complete secret scanner.
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(content):
                problems.append(f'{name}: posible {label}')
    # --get-regexp searches every configured URL including pushurl without echoing it.
    remotes = subprocess.run(['git', '-C', str(repo), 'config', '--get-regexp', r'^remote\..*\.(url|pushurl)$'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if remotes.returncode not in (0, 1):
        problems.append('No se pudieron comprobar los remotes de Git')
    elif PATTERNS['Credenciales en URL'].search(remotes.stdout) or any(p.search(remotes.stdout) for p in PATTERNS.values()):
        problems.append('Posible credencial en un remote Git; revisa las URL localmente y rota el secreto.')
    return problems


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, default=Path.cwd())
    p.add_argument('--staged', action='store_true')
    args = p.parse_args()
    try:
        problems = scan(args.repo, args.staged)
    except (OSError, subprocess.CalledProcessError):
        print('No se pudo inspeccionar el repositorio Git.', file=sys.stderr)
        return 1
    if problems:
        print('Posibles secretos (sin mostrar valores):\n' + '\n'.join(problems), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
