#Requires -Version 5.1
param([switch]$Verify, [ValidateSet('core', 'all')][string]$Profile = '', [switch]$Adopt)
$script = Join-Path $PSScriptRoot 'harnes.py'
$arguments = @($script)
if ($env:HARNES_HOME) { $arguments += @('--home', $env:HARNES_HOME) }
if ($Verify) { $arguments += 'verify' } else { $arguments += 'sync' }
if ($Profile) { $arguments += @('--profile', $Profile) }
if ($Adopt -and -not $Verify) { $arguments += '--adopt' }
& python @arguments
exit $LASTEXITCODE
