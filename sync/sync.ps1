#Requires -Version 5.1
<#
  sync.ps1 — instalador del harnés de CHARLI (v0.3, NEUTRO)

  Estándar universal (sin planes por agente):
    - Instrucciones: ~\.agents\AGENTS.md
    - Skills activas del canon: ~\.agents\skills\<nombre>

  Puentes (cero nombres de agentes): cada instalación previa registrada en
  ledger.json se refresca desde el canon si su destino aún existe. Así, los
  agentes ya configurados en tiempo pasado (p. ej. OpenCode) quedan al día sin
  que este script conozca su nombre. Si el canon RETIRÓ una fuente, la copia
  puente queda obsoleta y se elimina: el canon es la única fuente de verdad.

  Uso:
    sync.ps1        # instala/actualiza todo
    sync.ps1 -Verify  # solo comprueba (sin cambios; exit 1 si desfasado)
#>
[CmdletBinding()]
param([switch]$Verify)

$ErrorActionPreference = 'Stop'
$Canon = $PSScriptRoot | Split-Path -Parent
$Home_ = [Environment]::GetFolderPath('UserProfile')
$agentsskillDir = Join-Path $Home_ '.agents\skills'

# --- fuentes del canon -------------------------------------------------------
function Get-CanonSources {
    $items = @(
        @{ rel = 'AGENTS.md'; kind = 'archivo' }
    )
    $skillsRoot = Join-Path $Canon 'skills'
    if (Test-Path $skillsRoot) {
        foreach ($dir in Get-ChildItem $skillsRoot -Directory) {
            if ((Test-Path (Join-Path $dir.FullName 'SKILL.md')) -and -not (Test-Path (Join-Path $dir.FullName '_DORMIDA.md'))) {
                $items += @{ rel = "skills\$($dir.Name)"; kind = 'carpeta' }
            }
        }
    }
    return $items
}

# destino universal para una fuente
function Get-UniversalDest($rel) {
    if ($rel -eq 'AGENTS.md') { return Join-Path $Home_ '.agents\AGENTS.md' }
    return Join-Path $agentsskillDir (($rel -split '\\')[-1])
}

# puente: destino preexistente (ledger) → misma fuente relativa del canon
function Get-BridgeDest([string]$storeDest, [string]$rel) {
    # el dest del ledger se guarda tal cual, relativo a ~, jamás absoluto (regla 8)
    return $storeDest -replace '^~\\', ($Home_ + '\')
}

function Get-Fingerprint([string]$path, [string]$kind) {
    if ($kind -eq 'archivo') {
        if (-not (Test-Path $path)) { return $null }
        return (Get-FileHash $path).Hash
    }
    if (-not (Test-Path $path)) { return $null }
    $blob = (Get-ChildItem $path -Recurse -File | Sort-Object FullName | ForEach-Object {
        "$($_.FullName.Substring($path.Length))|$($_.Length)|$((Get-FileHash $_.FullName).Hash)"
    }) -join "`n"
    return (Get-FileHash -InputStream ([System.IO.MemoryStream]::new([Text.Encoding]::UTF8.GetBytes($blob)))).Hash
}

function Install-Copy($srcAbs, $destAbs, $kind) {
    $dstDir = $destAbs | Split-Path -Parent
    if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Path $dstDir -Force | Out-Null }
    if ($kind -eq 'archivo') { Copy-Item $srcAbs $destAbs -Force; return }
    if (Test-Path $destAbs) { Remove-Item $destAbs -Recurse -Force }
    Copy-Item $srcAbs $dstDir -Recurse -Force
    foreach ($j in @('__pycache__','node_modules','.git')) {
        Get-ChildItem $destAbs -Recurse -Force -Directory -Filter $j -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
    }
}

# --- ejecución ---------------------------------------------------------------
$ledgerPath = Join-Path $PSScriptRoot 'ledger.json'
$ledger = if (Test-Path $ledgerPath) { Get-Content $ledgerPath -Raw | ConvertFrom-Json } else { [pscustomobject]@{ installs = @() } }

$sources = Get-CanonSources
$srcMap = @{}   # rel -> @{ kind; src }
foreach ($s in $sources) { $srcMap[$s.rel] = $s }
$targets = @{}
foreach ($s in $sources) {
    $targets[$s.rel] = @{ src = $s.rel; dest = (Get-UniversalDest $s.rel); kind = $s.kind }
}

# puentes del ledger: destinos que ya existen y mapean a una fuente canónica
$keepInstalls = @()
foreach ($inst in @($ledger.installs)) {
    $destAbs = Get-BridgeDest $inst.dest ''
    $srcRel = $inst.source
    # fuentes renombradas: el nombre del dest dir manda para buscar en canon\skills\
    if ($srcMap.ContainsKey($srcRel)) {
        if ($srcRel -eq 'AGENTS.md' -or (-not ($destAbs -match [regex]::Escape((Join-Path $Home_ '.agents'))))) {
            # puente solo para destinos distintos del universal (evita duplicar la fila)
            if ($targets[$srcRel].dest -ne $destAbs) {
                $targets["$srcRel|bridge:" + (Get-Random)] = @{ src = $srcRel; dest = $destAbs; kind = $inst.kind; inst = $inst }
            } else { $keepInstalls += $inst }
        } else { $keepInstalls += $inst }
    } else {
        # retirada: el canon ya no tiene esta fuente -> copia puente obsoleta
        if (Test-Path $destAbs) {
            if (-not $Verify) { Remove-Item $destAbs -Recurse -Force -ErrorAction SilentlyContinue; Write-Host "retirada: $($inst.dest)" }
            else { Write-Host "retirada pendiente: $($inst.dest)"; exit 1 }
        }
        # y su entrada del ledger muere
    }
}

$stale = $false
foreach ($key in $targets.Keys) {
    $t = $targets[$key]
    $srcAbs = Join-Path $Canon $t.src
    $entry = "$($t.dest.Replace("$Home_\", '~\')) <- $($t.src)"
    $same = ((Get-Fingerprint $srcAbs $t.kind) -eq (Get-Fingerprint $t.dest $t.kind))
    if ($same) {
        Write-Host "SINCRONIZADO: $entry"
        if ($t.inst) { $keepInstalls += $t.inst }
        continue
    }
    Write-Host "DESACTUALIZADO: $entry"
    if ($Verify) { $stale = $true; continue }
    Install-Copy $srcAbs $t.dest $t.kind
    if ($t.inst) { $keepInstalls += $t.inst }
    else {
        $keepInstalls += [pscustomobject]@{
            agent = 'universal'; source = $t.src; kind = $t.kind
            dest = $t.dest.Replace("$Home_\", '~\')
        }
    }
    Write-Host "instalado: $entry"
}

# reconstrucción limpia del ledger (des-duplicada)
$ledger = [pscustomobject]@{ installs = @($keepInstalls | Group-Object dest, source | ForEach-Object { $_.Group[0] }) }

if ($Verify) {
    if ($stale) { exit 1 } else { Write-Host 'todo sincronizado'; exit 0 }
}
else {
    $ledger | ConvertTo-Json -Depth 4 | Set-Content $ledgerPath -Encoding utf8
    Write-Host 'ledger actualizado.'
}
