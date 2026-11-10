#!/usr/bin/env python3
"""Install this repository's optional pre-commit without overwriting existing hooks."""
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
configured = subprocess.run(['git', '-C', str(root), 'config', '--get', 'core.hooksPath'], capture_output=True, text=True)
if configured.returncode not in (0, 1) or configured.stdout.strip():
    sys.exit('Ya existe core.hooksPath (o no se pudo consultar): intégralo manualmente; no se modificó.')
result = subprocess.run(['git', '-C', str(root), 'rev-parse', '--git-path', 'hooks/pre-commit'], capture_output=True, text=True, check=True)
dest = Path(result.stdout.strip())
if not dest.is_absolute():
    dest = root / dest
dest.parent.mkdir(parents=True, exist_ok=True)
try:
    # O_EXCL refuses existing hooks and dangling symlinks, even under races.
    fd = os.open(str(dest), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o755)
except FileExistsError:
    sys.exit(f'Ya existe {dest}; intégralo manualmente. No se modificó.')
try:
    with os.fdopen(fd, 'wb') as out:
        out.write((root / 'hooks/pre-commit').read_bytes())
except Exception:
    dest.unlink(missing_ok=True)
    raise
print(f'Hook instalado en {dest}. Solo afecta a este repositorio.')
