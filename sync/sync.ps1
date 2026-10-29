#Requires -Version 5.1
<#
  sync.ps1 — instalador del harnés de CHARLI (v0.1)
  Uso:
    sync.ps1                  # instala en todos los agentes con plan no vacío
    sync.ps1 -Agent opencode  # instala solo en uno
    sync.ps1 -Verify          # solo comprueba sincronización (cero cambios, exit 1 si desactualizado)
  Determinista e idempotente. Registra cada archivo instalado en ledger.json.
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
    @{
        'opencode' = @(
            @{ src = Join-Path $Canon 'AGENTS.md'; dest = Join-Path $Home_ '.config\opencode\AGENTS.md' }
        )
        'claude-code' = @()
        'gemini'      = @()
        'kilo'        = @()
        'antigravity' = @()
        'freebuff'    = @()
    }
}

$plan = if ($Agent) { @{ $Agent = (Get-InstallPlan)[$Agent] } } else { Get-InstallPlan }

$ledgerPath = Join-Path $PSScriptRoot 'ledger.json'
$ledger = if (Test-Path $ledgerPath) { Get-Content $ledgerPath -Raw | ConvertFrom-Json } else { [pscustomobject]@{ installs = @() } }

$stale = $false
$results = @()
foreach ($agentName in $plan.Keys) {
    foreach ($item in $plan[$agentName]) {
        $srcRel = $item.src.Substring($Canon.Length).TrimStart('\','/')
        $entry = "$agentName :: $srcRel"
        $same = (Test-Path $item.dest) -and ((Get-FileHash $item.src).Hash -eq (Get-FileHash $item.dest).Hash)
        if ($same) {
            $results += "$entry -> SINCRONIZADO"
            continue
        }
        $results += "$entry -> DESACTUALIZADO(en el install, se corrige)"
        if ($Verify) {
            $stale = $true
            continue
        }
        $dstDir = $item.dest | Split-Path -Parent
        if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Path $dstDir -Force | Out-Null }
        Copy-Item $item.src $item.dest -Force
        # ledger: una entrada por destino (idempotente, sin duplicados)
        $installs = @($ledger.installs | Where-Object { $_.agent -ne $agentName }) +
            [pscustomobject]@{ agent = $agentName; source = $srcRel; dest = $item.dest.Replace("$Home_\", '~\') }
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
