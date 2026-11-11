#!/usr/bin/env python3
"""Scan every blob reachable from Git refs without printing secret values.

Complements audit.py's `git log -p -n 100` pass. Binary blobs and blobs over the
size limit are counted and skipped, not silently treated as clean.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

MAX_BLOB_BYTES = 5_000_000
ROOT = Path(__file__).resolve().parents[3]


def load_patterns():
    path = ROOT / 'hooks/check_secrets.py'
    if not path.is_file():
        raise RuntimeError('no se encontró hooks/check_secrets.py; ejecuta desde el checkout del harnés')
    spec = importlib.util.spec_from_file_location('harness_patterns', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.PATTERNS


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def scan(repo):
    patterns = load_patterns()
    refs = git(repo, 'for-each-ref', '--format=%(refname)', 'refs/').stdout.decode().splitlines()
    listing = git(repo, 'rev-list', '--objects', '--all').stdout.splitlines()
    objects = {}
    for line in listing:
        oid, _, name = line.partition(b' ')
        if oid:
            objects.setdefault(oid, set()).add(name.decode('utf-8', 'replace'))
    report = {'refs': len(refs), 'objects': len(objects), 'blobs': 0, 'text_scanned': 0,
              'binary_skipped': 0, 'oversize_skipped': 0, 'findings': [], 'errors': []}
    proc = subprocess.Popen(['git', '-C', str(repo), 'cat-file', '--batch'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for oid in objects:
            proc.stdin.write(oid + b'\n')
            proc.stdin.flush()
            header = proc.stdout.readline().split()
            if len(header) != 3 or not header[0].startswith(oid) or header[1] not in (b'blob', b'tree', b'commit', b'tag'):
                report['errors'].append('objeto ilegible: ' + oid.decode()[:12])
                break
            kind, size = header[1], int(header[2])
            data = proc.stdout.read(size)
            terminator = proc.stdout.read(1)
            if kind != b'blob':
                continue
            report['blobs'] += 1
            if len(data) != size or terminator != b'\n':
                report['errors'].append('lectura truncada: ' + oid.decode()[:12])
                break
            if size > MAX_BLOB_BYTES:
                report['oversize_skipped'] += 1
                continue
            if b'\0' in data:
                report['binary_skipped'] += 1
                continue
            report['text_scanned'] += 1
            for label, pattern in patterns.items():
                if pattern.search(data):
                    paths = sorted(p for p in objects[oid] if p)
                    report['findings'].append({'object': oid.decode()[:12], 'type': label,
                                               'paths': paths[:3]})
    finally:
        if proc.stdin:
            proc.stdin.close()
        if proc.poll() is None:
            proc.terminate()
        proc.wait()
    if proc.returncode not in (0, -15):
        report['errors'].append('cat-file terminó con código ' + str(proc.returncode))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', nargs='?', default='.', type=Path)
    parser.add_argument('--json', action='store_true', help='salida JSON completa')
    args = parser.parse_args()
    try:
        report = scan(args.repo.resolve())
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print('Refs: {refs}; objetos: {objects}; blobs: {blobs}; texto: {text_scanned}; '
                  'binarios omitidos: {binary_skipped}; grandes omitidos: {oversize_skipped}.'.format(**report))
            for item in report['findings']:
                print('Hallazgo: {type} en objeto {object}; rutas: {paths}'.format(
                    type=item['type'], object=item['object'], paths=', '.join(item['paths']) or '(sin ruta histórica)'))
            for error in report['errors']:
                print('Error: ' + error, file=sys.stderr)
        if report['errors']:
            return 2
        return 1 if report['findings'] else 0
    except (OSError, RuntimeError, subprocess.CalledProcessError, ValueError) as exc:
        print('Escaneo fallido: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
