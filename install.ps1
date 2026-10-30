#Requires -Version 5.1
<#
  install.ps1 — bootstrap de una línea del harnés de CHARLI (v0.1)

  Uso (desde cualquier shell, fuera o dentro del repo):
    irm https://raw.githubusercontent.com/CharlyCyber/Harnes/main/install.ps1 | iex

  Qué hace:
    1. Si el canon no existe: clona el repo a $Docs\Proyectos\Harnés.
    2. Si existe: actualiza con pull --ff-only (cero destrucción; si diverge, aborta).
    3. Ejecuta sync\sync.ps1 (instalador determinista e idempotente de cada agente).

  Reglas del canon respetadas:
    - Regla 8 (portabilidad): destino derivado de [Environment]::GetFolderPath,
      no de rutas fijas de una máquina concreta.
    - Regla 9 (custodia): si el destino existe y no es el repo del harnés, se
      aborta sin tocar nada; si el pull diverge, se aborta sin reset.
#>
$ErrorActionPreference = 'Stop'
$RepoUrl = 'https://github.com/CharlyCyber/Harnes.git'
$Canon = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Proyectos\Harnés'

function Fail([string]$msg) {
    Write-Host "install: FALLO — $msg" -ForegroundColor Red
    exit 1
}

# 0. prerrequisito: git en PATH
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Fail 'git no está en PATH. Instala Git for Windows y reejecuta.'
}

# 1-2. clonar o actualizar el canon (custodia: nunca destruir)
if (Test-Path $Canon) {
    if (-not (Test-Path (Join-Path $Canon '.git'))) {
        Fail "existe '$Canon' pero no es un repo git — no lo toco (regla 9). Muévelo o cambia de destino."
    }
    $remote = git -C $Canon remote get-url origin 2>$null
    if ($remote -and ($remote -notmatch [regex]::Escape('github.com/CharlyCyber/Harnes'))) {
        Fail "el remote de '$Canon' apunta a '$remote', no al harnés — no lo toco (regla 9)."
    }
    git -C $Canon pull --ff-only 2>&1 | ForEach-Object { Write-Host "  $_" }
    if ($LASTEXITCODE -ne 0) {
        Fail "el pull divergió ($Canon) — resuelto a mano (regla 9: sin reset automático)."
    }
    Write-Host "install: canon actualizado en $Canon" -ForegroundColor Green
}
else {
    New-Item (Split-Path $Canon -Parent) -ItemType Directory -Force | Out-Null
    git clone $RepoUrl $Canon 2>&1 | ForEach-Object { Write-Host "  $_" }
    if ($LASTEXITCODE -ne 0) {
        Fail "clon fallido. Si el repo es privado necesitas credencial de GitHub válida (GCM/SSH)."
    }
    Write-Host "install: canon clonado en $Canon" -ForegroundColor Green
}

# 3. instalar en los agentes
Write-Host "install: ejecutando sync de agentes..." -ForegroundColor Cyan
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Canon 'sync\sync.ps1')
if ($LASTEXITCODE -ne 0) { Fail 'sync\sync.ps1 terminó con error — revisa su salida arriba.' }

Write-Host 'install: listo. Los agentes con plan no vacío ya llevan el canon.' -ForegroundColor Green
