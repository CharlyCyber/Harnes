#Requires -Version 5.1
param([switch]$SkipSync)
$arguments = @((Join-Path $PSScriptRoot 'harnes.py'))
if ($env:HARNES_HOME) { $arguments += @('--home', $env:HARNES_HOME) }
$arguments += 'doctor'
if ($SkipSync) { $arguments += '--skip-sync' }
& python @arguments
exit $LASTEXITCODE
