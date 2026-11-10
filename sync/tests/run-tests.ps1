#Requires -Version 5.1
# Compatibility wrapper; tests always use disposable temporary homes.
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
& python -m unittest discover -s (Join-Path $root 'sync/tests') -p 'test_*.py'
exit $LASTEXITCODE
