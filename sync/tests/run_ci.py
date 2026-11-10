"""Run the smoke tests and expose failure details as a GitHub annotation."""
import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, '-m', 'unittest', 'discover', '-s', 'sync/tests', '-p', 'test_*.py'],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace',
    env={**os.environ, 'PYTHONUTF8': '1'},
)
print(result.stdout, end='')
print(result.stderr, end='', file=sys.stderr)
if result.returncode and os.environ.get('GITHUB_ACTIONS') == 'true':
    message = result.stderr.replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
    print('::error::' + message)
sys.exit(result.returncode)
