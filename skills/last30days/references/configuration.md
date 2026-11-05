# Configuración — Last30Days

## Variables de Entorno

```bash
# --- Fuentes ---
XQUIK_API_KEY=           # X/Twitter search
XAI_API_KEY=             # X/Twitter alternativo
SCRAPECREATORS_API_KEY=  # TikTok, Instagram, Threads, Pinterest, YT comments
PERPLEXITY_API_KEY=      # Perplexity Sonar / Deep Research
OPENROUTER_API_KEY=      # Fallback Perplexity via OpenRouter
BRAVE_SEARCH_API_KEY=    # Web search (2K free/mes)

# --- Almacenamiento ---
LAST30DAYS_MEMORY_DIR=~/Documents/Last30Days  # Donde se guardan briefs

# --- Exclusión ---
EXCLUDE_SOURCES=tiktok,instagram,threads      # Deshabilitar fuentes
INCLUDE_SOURCES=perplexity                     # Habilitar fuentes pagas
```

## macOS Keychain (opcional)

En macOS, las keys pueden ir en el Keychain del sistema en vez de `.env`:

```bash
bash skills/last30days/scripts/setup-keychain.sh   # Setup interactivo
security add-generic-password -a "$USER" -s last30days-XAI_API_KEY -w "xai-..."
```

## Trend Monitoring

```bash
# Acumular hallazgos en SQLite
/last30days "topic" --store

# Watchlist para runs scheduleados
python3 scripts/watchlist.py

# Briefings diarios/semanales
python3 scripts/briefing.py
```

## Instalación en el Proyecto

El skill referencia el repo oficial: `github.com/mvanhorn/last30days-skill`

```bash
# Claude Code (recomendado)
/plugin marketplace add mvanhorn/last30days-skill

# Codex, Cursor, Copilot, Gemini CLI (vía Agent Skills)
npx skills add mvanhorn/last30days-skill -g
```
