#Requires -Version 5.1
<#
  sync.ps1 — sincronizador neutral del harnés de CHARLI (v0.4)

  Modelo:
    canon (repo)  ->  almacén universal ~/.agents/skills  ->  junctions a cada cliente

  - El almacén universal es la única copia física de las skills activas.
  - Cada cliente detectado (destino cuyo directorio padre existe) recibe una
    junction al almacén: cero duplicación, cero drift entre agentes.
  - Sin nombres de agentes en el código: los destinos viven en targets.json.
  - Las skills retiradas del canon se podan del almacén y de las junctions.

  Uso:
    sync.ps1            instala/actualiza todo
    sync.ps1 -Verify    solo comprueba (exit 1 si hay drift)
#>
[CmdletBinding()]
param([switch]$Verify)

$ErrorActionPreference = 'Stop'
$Canon = Split-Path -Parent $PSScriptRoot
$HomeDir = [Environment]::GetFolderPath('UserProfile')
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'

$targetsPath = Join-Path $PSScriptRoot 'targets.json'
if (-not (Test-Path $targetsPath)) { throw "Falta sync\targets.json" }
$cfg = Get-Content $targetsPath -Raw | ConvertFrom-Json

$drift = $false
function Note-Drift([string]$msg) { Write-Host "DRIFT: $msg"; $script:drift = $true }
function Resolve-Home([string]$p) { return ($p -replace '^~', $HomeDir) -replace '/', '\' }

function Test-IsLink([string]$p) {
    if (-not (Test-Path -LiteralPath $p)) { return $false }
    $item = Get-Item -LiteralPath $p -Force
    return [bool]($item.Attributes -band [IO.FileAttributes]::ReparsePoint)
}
function Get-LinkTarget([string]$p) {
    $item = Get-Item -LiteralPath $p -Force
    return @($item.Target)[0]
}
function Remove-Link([string]$p) {
    # borra la junction, nunca su contenido
    [IO.Directory]::Delete((Resolve-Path -LiteralPath $p).ProviderPath, $false)
}
function Backup-Path([string]$p) {
    $bak = "$p.bak-$Stamp"
    Move-Item -LiteralPath $p -Destination $bak -Force
    Write-Host "backup: $p -> $bak"
}
function New-Junction([string]$link, [string]$target) {
    $parent = Split-Path -Parent $link
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    New-Item -ItemType Junction -Path $link -Target $target | Out-Null
}

function Get-Fingerprint([string]$path) {
    # huella barata: ruta relativa + tamaño + mtime. Robocopy preserva timestamps,
    # así que una edición real siempre cambia la huella; hashear 47 MB por pasada
    # hacía que el sync muriera por timeout del entorno.
    if (-not (Test-Path -LiteralPath $path)) { return $null }
    $blob = (Get-ChildItem -LiteralPath $path -Recurse -File -Force |
        Where-Object { $_.FullName -notmatch '\\__pycache__\\|\\node_modules\\|\\\.git\\' } |
        Sort-Object FullName | ForEach-Object {
            "$($_.FullName.Substring($path.Length))|$($_.Length)|$($_.LastWriteTimeUtc.Ticks)"
        }) -join "`n"
    return (Get-FileHash -InputStream ([IO.MemoryStream]::new([Text.Encoding]::UTF8.GetBytes($blob)))).Hash
}

# --- fuentes del canon -------------------------------------------------------
$canonSkills = @()
$skillsRoot = Join-Path $Canon 'skills'
foreach ($dir in Get-ChildItem -LiteralPath $skillsRoot -Directory) {
    $skillMd = Join-Path $dir.FullName 'SKILL.md'
    $dormida = Join-Path $dir.FullName '_DORMIDA.md'
    if ((Test-Path -LiteralPath $skillMd) -and -not (Test-Path -LiteralPath $dormida)) {
        $canonSkills += $dir.Name
    }
}
$canonSkills = $canonSkills | Sort-Object

# --- 1. almacén universal ----------------------------------------------------
$universal = Resolve-Home $cfg.universal.skills
if (-not (Test-Path -LiteralPath $universal)) {
    if ($Verify) { Note-Drift "falta el almacén universal $universal" }
    else { New-Item -ItemType Directory -Path $universal -Force | Out-Null }
}

$count = 0
foreach ($name in $canonSkills) {
    $src = Join-Path $skillsRoot $name
    $dst = Join-Path $universal $name
    $same = ((Get-Fingerprint $src) -eq (Get-Fingerprint $dst))
    if ($same) { continue }
    $count++
    if ($Verify) { Note-Drift "skill desactualizada: $name" ; continue }
    if (Test-Path -LiteralPath $dst) { Remove-Item -LiteralPath $dst -Recurse -Force }
    # /MIR y no /E: el almacén es una copia derivada, así que los archivos que ya
    # no existen en el canon (huérfanos dentro de una skill) deben desaparecer.
    # Con /E se acumulaban y la huella nunca convergía.
    robocopy $src $dst /MIR /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy falló copiando $name (exit $LASTEXITCODE)" }
    Write-Host "skill instalada: $name"
}

# poda de huérfanas en el almacén
if (Test-Path -LiteralPath $universal) {
    foreach ($dir in Get-ChildItem -LiteralPath $universal -Directory) {
        if ($canonSkills -notcontains $dir.Name) {
            if (Test-Path -LiteralPath (Join-Path $dir.FullName 'SKILL.md')) {
                if ($Verify) { Note-Drift "huérfana en almacén: $($dir.Name)" }
                else { Remove-Item -LiteralPath $dir.FullName -Recurse -Force; Write-Host "podada: $($dir.Name)" }
            }
        }
    }
}

# --- 2. instrucciones --------------------------------------------------------
$instructionDests = @($cfg.universal.instructions) + @($cfg.instructions | ForEach-Object { $_.dest })
foreach ($raw in $instructionDests) {
    $dst = Resolve-Home $raw
    $src = Join-Path $Canon 'AGENTS.md'
    $same = (Test-Path -LiteralPath $dst) -and ((Get-FileHash -LiteralPath $src).Hash -eq (Get-FileHash -LiteralPath $dst).Hash)
    if ($same) { continue }
    if ($Verify) { Note-Drift "instrucciones desactualizadas: $raw"; continue }
    if (Test-Path -LiteralPath $dst) { Backup-Path $dst }
    $parent = Split-Path -Parent $dst
    if (-not (Test-Path -LiteralPath $parent)) { continue }
    Copy-Item -LiteralPath $src -Destination $dst -Force
    Write-Host "instrucciones: $raw"
}

# --- 3. clientes -------------------------------------------------------------
foreach ($client in @($cfg.clients)) {
    $path = Resolve-Home $client.path
    $parent = Split-Path -Parent $path
    if (-not (Test-Path -LiteralPath $parent)) { continue }   # cliente no instalado

    if ($client.mode -eq 'dir-junction') {
        if (Test-Path -LiteralPath $path) {
            if (Test-IsLink $path) {
                $target = Get-LinkTarget $path
                if ($target -ne $universal) {
                    if ($Verify) { Note-Drift "junction con destino viejo: $($client.id)" ; continue }
                    Remove-Link $path; New-Junction $path $universal
                    Write-Host "junction reparada: $($client.id)"
                }
            } else {
                if ($Verify) { Note-Drift "copia real en vez de junction: $($client.id)" ; continue }
                Backup-Path $path; New-Junction $path $universal
                Write-Host "junction creada: $($client.id)"
            }
        } else {
            if ($Verify) { Note-Drift "falta junction: $($client.id)" ; continue }
            New-Junction $path $universal
            Write-Host "junction creada: $($client.id)"
        }
    }
    elseif ($client.mode -eq 'entry-junction') {
        if (-not (Test-Path -LiteralPath $path)) {
            if ($Verify) { Note-Drift "falta carpeta de cliente: $($client.id)" ; continue }
            New-Item -ItemType Directory -Path $path -Force | Out-Null
        }
        $preserve = @($client.preserve)
        foreach ($name in $canonSkills) {
            $link = Join-Path $path $name
            if (Test-Path -LiteralPath $link) {
                if (Test-IsLink $link) {
                    if ((Get-LinkTarget $link) -ne (Join-Path $universal $name)) {
                        if ($Verify) { Note-Drift "entry-junction rota: $($client.id)/$name" ; continue }
                        Remove-Link $link; New-Junction $link (Join-Path $universal $name)
                    }
                } else {
                    if ($Verify) { Note-Drift "copia real en $($client.id)/$name" ; continue }
                    Backup-Path $link; New-Junction $link (Join-Path $universal $name)
                }
            } else {
                if ($Verify) { Note-Drift "falta entry-junction: $($client.id)/$name" ; continue }
                New-Junction $link (Join-Path $universal $name)
            }
        }
        foreach ($dir in Get-ChildItem -LiteralPath $path -Directory -Force) {
            if ($canonSkills -contains $dir.Name) { continue }
            if ($preserve -contains $dir.Name) { continue }
            if (-not (Test-IsLink $dir.FullName)) { continue }
            if ($Verify) { Note-Drift "entry-junction huérfana: $($client.id)/$($dir.Name)" ; continue }
            Remove-Link $dir.FullName
            Write-Host "podada: $($client.id)/$($dir.Name)"
        }
    }
}

# --- resumen -----------------------------------------------------------------
if ($Verify) {
    if ($drift) { Write-Host 'resultado: DRIFT'; exit 1 }
    Write-Host 'resultado: todo sincronizado'; exit 0
}
Write-Host ("listo: {0} skills activas, {1} actualizadas" -f $canonSkills.Count, $count)
