#Requires -Version 5.1
param([string]$Path = '')
if (-not $Path) { $Path = Split-Path -Parent $PSScriptRoot }
& python (Join-Path $PSScriptRoot 'check_secrets.py') --repo $Path
exit $LASTEXITCODE
