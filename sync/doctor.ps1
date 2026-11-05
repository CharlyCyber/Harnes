#Requires -Version 5.1
<#
  doctor.ps1 — verificación integral del harnés (v0.4)

  Comprueba, sin modificar nada:
    1. Canon: SKILL.md presente, frontmatter mínimo, <500 líneas, sin carpetas anidadas.
    2. JSON válido: sync\targets.json y la config de OpenCode si existe.
    3. Sincronización: canon == almacén universal == clientes (delegado en sync.ps1 -Verify).
    4. Rutas prohibidas declaradas en targets.json (deben estar ausentes).
    5. Secretos: hook del repo + patrones de API key en configs del perfil.

  Uso: doctor.ps1 [-SkipSync]   (exit 0 = todo bien, exit 1 = fallos)

  -SkipSync: omite la verificación de sincronización (útil en entornos sin
  clientes instalados, p. ej. CI o un HOME desechable).
#>
[CmdletBinding()]
param([switch]$SkipSync)

$ErrorActionPreference = 'Stop'
# Overrides de test/CI, igual que en sync.ps1.
$Canon = if ($env:HARNES_CANON) { $env:HARNES_CANON } else { Split-Path -Parent $PSScriptRoot }
$HomeDir = if ($env:HARNES_HOME) { $env:HARNES_HOME } else { [Environment]::GetFolderPath('UserProfile') }
$fail = 0
$warn = 0

function Ok([string]$m) { Write-Host "OK   $m" }
function Fail([string]$m) { Write-Host "FAIL $m"; $script:fail++ }
function Warn([string]$m) { Write-Host "WARN $m"; $script:warn++ }

# --- 1. canon ----------------------------------------------------------------
$skillsRoot = Join-Path $Canon 'skills'
$skills = Get-ChildItem -LiteralPath $skillsRoot -Directory | Sort-Object Name
if ($skills.Count -eq 0) { Fail 'el canon no tiene skills' }

foreach ($s in $skills) {
    $md = Join-Path $s.FullName 'SKILL.md'
    if (-not (Test-Path -LiteralPath $md)) {
        if (Test-Path -LiteralPath (Join-Path $s.FullName '_DORMIDA.md')) { continue }
        Fail "sin SKILL.md: $($s.Name)"
        continue
    }
    $lines = (Get-Content -LiteralPath $md | Measure-Object -Line).Lines
    if ($lines -ge 500) { Fail "SKILL.md >= 500 líneas: $($s.Name) ($lines)" }
    $head = (Get-Content -LiteralPath $md -TotalCount 20) -join "`n"
    if ($head -notmatch 'name\s*:' -or $head -notmatch 'description\s*:') {
        Fail "frontmatter incompleto: $($s.Name)"
    }
    if (Test-Path -LiteralPath (Join-Path $s.FullName $s.Name)) {
        Fail "carpeta anidada (bug de vendoreo): $($s.Name)/$($s.Name)"
    }
}
if ($fail -eq 0) { Ok "canon: $($skills.Count) skills válidas" }

# --- 2. JSON ---------------------------------------------------------------
foreach ($j in @((Join-Path $PSScriptRoot 'targets.json'), (Join-Path $HomeDir '.config\opencode\opencode.json'))) {
    if (-not (Test-Path -LiteralPath $j)) { Warn "no existe: $j"; continue }
    try { Get-Content -LiteralPath $j -Raw | ConvertFrom-Json | Out-Null; Ok "JSON válido: $($j.Replace($HomeDir,'~'))" }
    catch { Fail "JSON inválido: $($j.Replace($HomeDir,'~'))" }
}

# --- 3. rutas prohibidas --------------------------------------------------
# Una ruta prohibida es una segunda fuente de verdad conocida (p. ej. el CLI de
# HyperFrames repoblando una carpeta local de skills en OpenCode). Si reaparece,
# el doctor falla: significa que algo volvió a escribir donde no debe.
$targetsPath = Join-Path $PSScriptRoot 'targets.json'
if (Test-Path -LiteralPath $targetsPath) {
    $tcfg = $null
    try { $tcfg = Get-Content -LiteralPath $targetsPath -Raw | ConvertFrom-Json } catch { $tcfg = $null }
    # @() envolviendo el pipeline: con un solo elemento la asignación se
    # desenvuelve y un PSCustomObject no responde a .Count en PS 5.1.
    $forbiddenCfg = @(@($tcfg.forbidden) | Where-Object { $_ -and $_.path })
    if ($forbiddenCfg.Count -gt 0) {
        $found = 0
        foreach ($f in $forbiddenCfg) {
            $p = ($f.path -replace '^~', $HomeDir) -replace '/', '\'
            if (Test-Path -LiteralPath $p) {
                $found++
                Fail "ruta prohibida existe: $($f.path) — $($f.reason)"
            }
        }
        if ($found -eq 0) { Ok "rutas prohibidas: ausentes ($($forbiddenCfg.Count) declaradas)" }
    }
}

# --- 4. sincronización -----------------------------------------------------
if ($SkipSync) {
    Ok 'sincronización: omitida (-SkipSync)'
} else {
    $sync = Join-Path $PSScriptRoot 'sync.ps1'
    $out = & $sync -Verify 2>&1 | Out-String
    if ($LASTEXITCODE -eq 0) { Ok 'sincronización: canon == universal == clientes' }
    else {
        Fail 'sincronización con drift'
        ($out -split "`n" | Where-Object { $_ -match 'DRIFT' }) | ForEach-Object { Write-Host "     $($_.Trim())" }
    }
}

# --- 5. secretos -----------------------------------------------------------
$hook = Join-Path $Canon 'hooks\check-secrets.ps1'
if (Test-Path -LiteralPath $hook) {
    $r = & $hook 2>&1 | Out-String
    if ($LASTEXITCODE -eq 0) { Ok 'repo: 0 secretos' } else { Fail "repo: posibles secretos`n$r" }
}
$patterns = 'fc-[a-f0-9]{30,}|apify_api_[A-Za-z0-9]{20,}|ctx7sk-[a-z0-9-]{10,}|gh[opsu]_[A-Za-z0-9]{20,}'
$scanRoots = @("$HomeDir\.agents", "$HomeDir\.gemini", "$HomeDir\.config\opencode", "$HomeDir\.claude", "$HomeDir\.codex")
$leaks = 0
foreach ($root in $scanRoots) {
    if (-not (Test-Path -LiteralPath $root)) { continue }
    Get-ChildItem -LiteralPath $root -Recurse -File -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.Length -lt 2MB -and @('.json','.jsonc','.md','.yaml','.yml','.toml','.txt','.log','.ps1') -contains $_.Extension.ToLower() -and $_.FullName -notmatch '\\node_modules\\' } |
        ForEach-Object {
            $t = [IO.File]::ReadAllText($_.FullName)
            if ($t -match $patterns) { $leaks++; Fail "posible key en $($_.FullName.Replace($HomeDir,'~'))" }
        }
}
if ($leaks -eq 0) { Ok 'perfil: 0 claves en texto plano' }

# --- resumen ---------------------------------------------------------------
Write-Host ''
if ($fail -gt 0) { Write-Host "RESULTADO: $fail fallo(s), $warn aviso(s)"; exit 1 }
Write-Host "RESULTADO: sano ($warn aviso(s))"
exit 0


