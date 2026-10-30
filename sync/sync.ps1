#Requires -Version 5.1
<#
  sync.ps1 — instalador del harnés de CHARLI (v0.2)
  Uso:
    sync.ps1                  # instala en todos los agentes con plan no vacío
    sync.ps1 -Agent opencode  # instala solo en uno
    sync.ps1 -Verify          # solo comprueba sincronización (cero cambios, exit 1 si desactualizado)
  Determinista e idempotente. Registra cada archivo/carpeta instalada en ledger.json.
  Regla 9 del canon: el ledger guarda destinos relativos al perfil (~\), jamás rutas absolutas.
#>
[CmdletBinding()]
param(
    [ValidateSet('opencode','claude-code','gemini','kilo','antigravity','freebuff')]
    [string]$Agent = '',
    [switch]$Verify
)

$ErrorActionPreference = 'Stop'
$Canon = $PSScriptRoot | Split-Path -Parent
$Home_ = [Environment]::GetFolderPath('UserProfile')

function Get-InstallPlan {
    # Plan = lista de items:
    #  archivo:  { src, dest }  -> copia un archivo del canon al destino
    #  carpeta:  { dir, name }  -> copia la carpeta entera del canon a skills del agente
    $plan = @{
        'opencode' = @(
            @{ src = Join-Path $Canon 'AGENTS.md'; dest = Join-Path $Home_ '.config\opencode\AGENTS.md' }
        )
        'claude-code' = @()
        'gemini'      = @()
        'kilo'        = @()
        'antigravity' = @()
        'freebuff'    = @()
    }
    # skills canónicas (cada carpeta con SKILL.md) -> .config\opencode\skills\<nombre>\
    $skillsRoot = Join-Path $Canon 'skills'
    if (Test-Path $skillsRoot) {
        foreach ($dir in Get-ChildItem $skillsRoot -Directory) {
            if (Test-Path (Join-Path $dir.FullName 'SKILL.md')) {
                $plan['opencode'] += @{ dir = $dir.FullName; name = $dir.Name }
            }
        }
    }
    return $plan
}

# destino de un item según el agente
function Resolve-Dest([string]$agent, [hashtable]$item) {
    if ($item.dest) { return $item.dest }
    switch ($agent) {
        'opencode' { return Join-Path $Home_ (Join-Path '.config\opencode\skills' $item.name) }
        default    { return $null }
    }
}

$plan = if ($Agent) { @{ $Agent = (Get-InstallPlan)[$Agent] } } else { Get-InstallPlan }

$ledgerPath = Join-Path $PSScriptRoot 'ledger.json'
$ledger = if (Test-Path $ledgerPath) { Get-Content $ledgerPath -Raw | ConvertFrom-Json } else { [pscustomobject]@{ installs = @() } }

$stale = $false
$results = @()
foreach ($agentName in $plan.Keys) {
    foreach ($item in $plan[$agentName]) {
        $dest = Resolve-Dest $agentName $item
        if (-not $dest) { continue }
        $isFolder = [bool]$item.dir
        $src = if ($isFolder) { $item.dir } else { $item.src }
        $srcRel = $src.Substring($Canon.Length).TrimStart('\','/')
        $entry = "$agentName :: $srcRel"
        $same = (Test-Path $dest) -and ((Get-FileHash $src).Hash -eq (Get-FileHash $dest).Hash)
        if ($same) { $results += "$entry -> SINCRONIZADO"; continue }
        $results += "$entry -> DESACTUALIZADO"
        if ($Verify) { $stale = $true; continue }
        $dstDir = $dest | Split-Path -Parent
        if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Path $dstDir -Force | Out-Null }
        if ($isFolder) {
            # copia espejo de la carpeta, sin basuras
            $junk = '__pycache__','node_modules','.git'
            Copy-Item $src $dstDir -Recurse -Force
            foreach ($j in $junk) {
                Get-ChildItem $dstDir -Recurse -Force -Directory -Filter $j -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
            }
        } else {
            Copy-Item $src $dest -Force
        }
        $installs = @($ledger.installs | Where-Object { $_.agent -ne $agentName -or $_.source -ne $srcRel }) +
            [pscustomobject]@{
                agent = $agentName; source = $srcRel
                kind = if ($isFolder) { 'carpeta' } else { 'archivo' }
                dest = $dest.Replace("$Home_\", '~\')
            }
        $ledger = [pscustomobject]@{ installs = $installs }
        Write-Host "instalado: $entry"
    }
}

$results | ForEach-Object { Write-Host $_ }

if ($Verify) {
    if ($stale) { exit 1 } else { Write-Host 'todo sincronizado'; exit 0 }
}
else {
    $ledger | ConvertTo-Json -Depth 4 | Set-Content $ledgerPath -Encoding utf8
}
