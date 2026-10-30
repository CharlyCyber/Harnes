#Requires -Version 5.1
<#
  check-secrets.ps1 — hook anti-fugas del harnes de CHARLI (v0.1)
  Origen: fuga real registrada en knowledge/failures.md (2026-10-30,
  token OAuth incrustado en la URL de un remote de Git).

  Escanea el arbol de trabajo con patrones ASCII de secretos comunes y
  exit 1 si encuentra algo. Pensado para correr manualmente o como
  pre-commit. Jamas commitea ni modifica nada: puramente detectivo.

  Nota: patrones ASCII a proposito (el patron de regex con acentos
  corrupciona en Windows PowerShell 5.1 - fallo ya conocido).

  Uso:
    powershell -File hooks\check-secrets.ps1            # escaneo del repo (~PSScriptRoot\..)
    powershell -File hooks\check-secrets.ps1 -Path X    # escaneo de otra carpeta
#>
[CmdletBinding()]
param(
    [string]$Path = ''
)

$ErrorActionPreference = 'Stop'
if (-not $Path) { $Path = Join-Path $PSScriptRoot '..' }
$Path = (Resolve-Path $Path).Path

# Archivos de texto a escanear, excluyendo binarios, .git y node_modules
$excludeDirs = @('\.git\', '\node_modules\', '\__pycache__\')
$extInclude  = @('.ps1', '.psm1', '.md', '.json', '.ts', '.tsx', '.js', '.mjs',
                 '.py', '.yml', '.yaml', '.toml', '.txt', '.env', '.sh', '.html')

# Patrones: nombre descriptivo -> regex ASCII
$patterns = [ordered]@{
    'token GitHub OAuth  (gho_)'   = 'gho_[A-Za-z0-9]{20,}'
    'PAT fino GitHub    (github_)' = 'github_pat_[A-Za-z0-9_]{20,}'
    'PAT clasico GitHub (ghp_)'    = 'ghp_[A-Za-z0-9]{20,}'
    'OpenAI/Anthropic   (sk-)'     = 'sk-[A-Za-z0-9][A-Za-z0-9-]{16,}'
    'AWS access key     (AKIA)'    = 'AKIA[A-Z0-9]{12,}'
    'credencial en URL'            = '://[A-Za-z0-9._%+-]+:[^@\s/]{8,}@'   # esquema://user:pass@host
    'Google API key'               = 'AIza[A-Za-z0-9_-]{30,}'
    'Slack token'                  = 'xox[baprs]-[A-Za-z0-9-]{10,}'
}

$files = Get-ChildItem $Path -Recurse -File -Force |
    Where-Object {
        $full = $_.FullName
        -not ($excludeDirs | Where-Object { $full -like "*$_*" }) -and
        ($extInclude -contains $_.Extension.ToLower())
    }

$hits = @()
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    foreach ($name in $patterns.Keys) {
        $m = [regex]::Matches($content, $patterns[$name])
        foreach ($x in $m) {
            # ofusco lo encontrado al reportar: solo primeros 6 chars
            $preview = $x.Value.Substring(0, [Math]::Min(10, $x.Value.Length)) + '...(ofuscado)'
            $hits += "FUGA [$name] -> $($f.FullName.Substring($Path.Length + 1)) : $preview"
        }
    }
}

if ($hits.Count -gt 0) {
    Write-Host 'FUGAS DETECTADAS - no commitees nada hasta sanear:'
    $hits | ForEach-Object { Write-Host "  $_" }
    Write-Host ''
    Write-Host 'Saneado tipico: si es un remote -> git remote set-url; si es archivo -> '
    Write-Host 'mueve el secreto a una env var / .env no rastreado y registra el fallo en knowledge/failures.md.'
    exit 1
}

Write-Host 'check-secrets: 0 fugas (archivos escaneados:' $files.Count ')'
exit 0
