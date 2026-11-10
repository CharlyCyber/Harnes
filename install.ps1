#Requires -Version 5.1
# Run from an already cloned, authenticated checkout. Never downloads and executes code.
param([ValidateSet('core', 'all')][string]$Profile = 'core')
& python (Join-Path $PSScriptRoot 'sync/harnes.py') sync --profile $Profile
exit $LASTEXITCODE
