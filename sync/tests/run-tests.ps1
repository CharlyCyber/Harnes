#Requires -Version 5.1
<#
  run-tests.ps1 — smoke tests del motor de sincronización (v0.4)

  Qué cubre:
    1. Instalación desde cero (almacén, junctions, instrucciones).
    2. Idempotencia (la segunda pasada no copia nada).
    3. Poda de huérfanos: archivo sobrante dentro de una skill (/MIR) y skill
       retirada del canon.
    4. Reparación de una junction de cliente que se convirtió en carpeta real.
    5. Entry-junctions de codex: recrear la que falta, sustituir la copia real y
       podar la huérfana.
    6. -Verify detecta el drift y vuelve a verde tras reparar.
    7. doctor.ps1: -SkipSync, y fallo cuando existe una ruta prohibida.

  No toca el HOME real ni el canon real: usa HARNES_HOME y HARNES_CANON con un
  directorio temporal desechable y el canon mínimo de sync\tests\fixture.

  Uso: powershell -ExecutionPolicy Bypass -File sync\tests\run-tests.ps1 [-Keep]
       exit 0 = todo verde, exit 1 = algún fallo.
#>
[CmdletBinding()]
param([switch]$Keep)

$ErrorActionPreference = 'Stop'

$Repo    = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Sync    = Join-Path $Repo 'sync\sync.ps1'
$Doctor  = Join-Path $Repo 'sync\doctor.ps1'
$Fixture = Join-Path $PSScriptRoot 'fixture'
$Root    = Join-Path ([IO.Path]::GetTempPath()) ("harnes-sync-tests-" + [guid]::NewGuid().ToString('N').Substring(0, 8))

foreach ($f in @($Sync, $Doctor, $Fixture)) {
    if (-not (Test-Path -LiteralPath $f)) { throw "falta una pieza del test: $f" }
}
New-Item -ItemType Directory -Path $Root -Force | Out-Null

$script:passed = 0
$script:failed = 0
function Ok([string]$m)  { Write-Host "  ok   $m"; $script:passed++ }
function Bad([string]$m) { Write-Host "  FAIL $m"; $script:failed++ }
function Assert([bool]$cond, [string]$m) { if ($cond) { Ok $m } else { Bad $m } }

function New-Home([string[]]$dirs = @('.claude', '.gemini', '.codex')) {
    $h = Join-Path $Root ([guid]::NewGuid().ToString('N').Substring(0, 8))
    New-Item -ItemType Directory -Path $h -Force | Out-Null
    foreach ($d in $dirs) { New-Item -ItemType Directory -Path (Join-Path $h $d) -Force | Out-Null }
    return $h
}
function Test-Link([string]$p) {
    if (-not (Test-Path -LiteralPath $p)) { return $false }
    return [bool]((Get-Item -LiteralPath $p -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)
}
function Get-Target([string]$p) { return @((Get-Item -LiteralPath $p -Force).Target)[0] }
function Remove-Junction([string]$p) { [IO.Directory]::Delete((Resolve-Path -LiteralPath $p).ProviderPath, $false) }

function Invoke-Sync([string]$fakeHome, [switch]$Verify) {
    $env:HARNES_HOME  = $fakeHome
    $env:HARNES_CANON = $Fixture
    # *>&1: captura también Write-Host (stream de información), que 2>&1 no toca.
    if ($Verify) { $out = & $Sync -Verify *>&1 | Out-String } else { $out = & $Sync *>&1 | Out-String }
    return [pscustomobject]@{ Out = $out; Code = $LASTEXITCODE }
}
function Invoke-Doctor([string]$fakeHome, [switch]$SkipSync) {
    $env:HARNES_HOME  = $fakeHome
    $env:HARNES_CANON = $Fixture
    if ($SkipSync) { $out = & $Doctor -SkipSync *>&1 | Out-String } else { $out = & $Doctor *>&1 | Out-String }
    return [pscustomobject]@{ Out = $out; Code = $LASTEXITCODE }
}

try {
    # --- 1 -----------------------------------------------------------------
    Write-Host '[1] instalación desde cero'
    $h = New-Home
    $u = Join-Path $h '.agents\skills'
    $r = Invoke-Sync $h
    Assert ($r.Code -eq 0) 'sync termina con exit 0'
    Assert (Test-Path -LiteralPath (Join-Path $u 'alpha\SKILL.md')) 'almacén: alpha instalada'
    Assert (Test-Path -LiteralPath (Join-Path $u 'beta\notes.md')) 'almacén: archivos auxiliares copiados'
    Assert ((Get-ChildItem -LiteralPath $u -Directory).Count -eq 2) 'almacén: solo las 2 skills del canon'
    Assert (Test-Link (Join-Path $h '.claude\skills')) 'claude: junction de directorio creada'
    Assert ((Get-Target (Join-Path $h '.claude\skills')) -eq $u) 'claude: apunta al almacén universal'
    Assert ((Get-ChildItem -LiteralPath (Join-Path $h '.codex\skills') -Force).Count -eq 2) 'codex: 2 entry-junctions'
    Assert (Test-Path -LiteralPath (Join-Path $h '.codex\skills\alpha\SKILL.md')) 'codex: alpha legible a través del enlace'
    Assert (((Get-FileHash -LiteralPath (Join-Path $h '.gemini\GEMINI.md')).Hash) -eq ((Get-FileHash -LiteralPath (Join-Path $Fixture 'AGENTS.md')).Hash)) 'instrucciones: GEMINI.md idéntico al canon'
    $v = Invoke-Sync $h -Verify
    Assert ($v.Code -eq 0) '-Verify verde tras instalar'

    # --- 2 -----------------------------------------------------------------
    Write-Host '[2] idempotencia'
    $r = Invoke-Sync $h
    Assert ($r.Code -eq 0) 'segunda pasada exit 0'
    Assert ($r.Out -match '0 actualizadas') 'segunda pasada: 0 skills actualizadas'

    # --- 3 -----------------------------------------------------------------
    Write-Host '[3] poda de huérfanos'
    Set-Content -LiteralPath (Join-Path $u 'alpha\extra.txt') -Value 'huerfano' -Encoding utf8
    New-Item -ItemType Directory -Path (Join-Path $u 'ghost') -Force | Out-Null
    Set-Content -LiteralPath (Join-Path $u 'ghost\SKILL.md') -Value 'retirada' -Encoding utf8
    $v = Invoke-Sync $h -Verify
    Assert ($v.Code -eq 1) '-Verify detecta archivo sobrante y skill huérfana'
    Invoke-Sync $h | Out-Null
    Assert (-not (Test-Path -LiteralPath (Join-Path $u 'alpha\extra.txt'))) 'archivo sobrante borrado (/MIR)'
    Assert (-not (Test-Path -LiteralPath (Join-Path $u 'ghost'))) 'skill huérfana podada'

    # --- 4 -----------------------------------------------------------------
    Write-Host '[4] reparación de junction de cliente'
    $claude = Join-Path $h '.claude\skills'
    Remove-Junction $claude
    New-Item -ItemType Directory -Path $claude -Force | Out-Null
    Set-Content -LiteralPath (Join-Path $claude 'stray.txt') -Value 'copia real' -Encoding utf8
    $r = Invoke-Sync $h
    Assert (Test-Link $claude) 'claude: copia real sustituida por junction'
    Assert ((Get-Target $claude) -eq $u) 'claude: junction apunta al almacén'
    Assert (-not (Test-Path -LiteralPath (Join-Path $claude 'stray.txt'))) 'claude: la copia real se movió a un backup'
    Assert (@(Get-ChildItem -LiteralPath (Join-Path $h '.claude') -Force -Filter 'skills.bak-*').Count -eq 1) 'claude: backup conservado'

    # --- 5 -----------------------------------------------------------------
    Write-Host '[5] entry-junctions de codex'
    $cx = Join-Path $h '.codex\skills'
    Remove-Junction (Join-Path $cx 'alpha')
    Remove-Junction (Join-Path $cx 'beta')
    New-Item -ItemType Directory -Path (Join-Path $cx 'beta') -Force | Out-Null
    Set-Content -LiteralPath (Join-Path $cx 'beta\stray.txt') -Value 'copia real' -Encoding utf8
    New-Item -ItemType Junction -Path (Join-Path $cx 'ghost') -Target (Join-Path $u 'alpha') | Out-Null
    $r = Invoke-Sync $h
    Assert (Test-Link (Join-Path $cx 'alpha')) 'codex: entry-junction faltante recreada'
    Assert (Test-Link (Join-Path $cx 'beta')) 'codex: copia real sustituida por junction'
    Assert (-not (Test-Path -LiteralPath (Join-Path $cx 'ghost'))) 'codex: entry-junction huérfana podada'

    # --- 6 -----------------------------------------------------------------
    Write-Host '[6] -Verify detecta drift y se repara'
    Add-Content -LiteralPath (Join-Path $u 'alpha\SKILL.md') -Value 'drift' -Encoding utf8
    $v = Invoke-Sync $h -Verify
    Assert ($v.Code -eq 1) '-Verify sale con 1'
    Assert ($v.Out -match 'DRIFT') '-Verify imprime DRIFT'
    Invoke-Sync $h | Out-Null
    $v = Invoke-Sync $h -Verify
    Assert ($v.Code -eq 0) '-Verify vuelve a verde tras el sync'

    # --- 7 -----------------------------------------------------------------
    Write-Host '[7] doctor.ps1'
    $d = Invoke-Doctor $h -SkipSync
    Assert ($d.Code -eq 0) 'doctor -SkipSync sale con 0 en un home limpio'
    $forbidden = Join-Path $h '.config\opencode\skills'
    New-Item -ItemType Directory -Path $forbidden -Force | Out-Null
    $d = Invoke-Doctor $h -SkipSync
    Assert ($d.Code -eq 1) 'doctor falla si existe una ruta prohibida'
    Assert ($d.Out -match 'ruta prohibida existe') 'doctor explica la ruta prohibida'
    Remove-Item -LiteralPath $forbidden -Recurse -Force
    $d = Invoke-Doctor $h
    Assert ($d.Code -eq 0) 'doctor completo sale con 0 (sync incluido)'
}
finally {
    if (-not $Keep) {
        # rmdir no sigue junctions: borra el enlace, nunca el destino.
        & cmd /c rmdir /s /q "$Root" 2>&1 | Out-Null
    } else {
        Write-Host "conservado: $Root"
    }
    Remove-Item Env:\HARNES_HOME -ErrorAction SilentlyContinue
    Remove-Item Env:\HARNES_CANON -ErrorAction SilentlyContinue
}

Write-Host ''
if ($script:failed -gt 0) {
    Write-Host ("RESULTADO: {0} ok, {1} fallo(s)" -f $script:passed, $script:failed)
    exit 1
}
Write-Host ("RESULTADO: {0} comprobaciones ok, 0 fallos" -f $script:passed)
exit 0
