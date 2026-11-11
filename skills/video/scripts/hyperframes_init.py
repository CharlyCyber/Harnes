#!/usr/bin/env python3
"""Scaffold a blank project with an explicitly reviewed, locally installed CLI.

Not a sandbox: the CLI and its dependencies execute with the caller's permissions.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

# Only versions whose init opt-out has been checked in the npm package and in a
# disposable HOME may be listed here. Version is not a package integrity check.
SUPPORTED_VERSION = '0.9.33'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package-dir', type=Path, required=True,
                        help='local node_modules/hyperframes directory, already installed')
    parser.add_argument('project', type=Path, help='new project directory; parent must exist')
    args = parser.parse_args()
    try:
        package = args.package_dir.resolve(strict=True)
        info = json.loads((package / 'package.json').read_text(encoding='utf-8'))
        if info.get('name') != 'hyperframes' or info.get('version') != SUPPORTED_VERSION:
            raise ValueError(f'se requiere hyperframes local {SUPPORTED_VERSION}; no se descargará otra versión')
        # Hardcode this release's entrypoint instead of trusting package.json bin.
        entry = package / 'bin/hyperframes.mjs'
        if not entry.is_file() or not entry.resolve().is_relative_to(package):
            raise ValueError('falta el ejecutable local esperado')
        node = shutil.which('node')
        if not node:
            raise ValueError('Node.js no está disponible')
        path = args.project.absolute()
        if not path.name or path.name in ('.', '..') or os.path.lexists(path):
            raise ValueError('el proyecto debe ser un directorio nuevo')
        parent = path.parent.resolve(strict=True)
        if not parent.is_dir():
            raise ValueError('el directorio padre no existe')
        env = os.environ.copy()
        env.update(HYPERFRAMES_SKIP_SKILLS='1', HYPERFRAMES_NO_UPDATE_CHECK='1',
                   HYPERFRAMES_NO_TELEMETRY='1')
        print('HyperFrames local: sin skills, sin comprobación de actualizaciones ni telemetría; no es sandbox.', flush=True)
        result = subprocess.run([node, str(entry), 'init', path.name, '--non-interactive',
                                 '--example=blank'], cwd=parent, env=env, check=False)
        return result.returncode if result.returncode >= 0 else 1
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f'No se inició HyperFrames: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
