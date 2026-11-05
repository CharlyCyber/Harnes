# Fuentes de Búsqueda — Last30Days

## Fuentes Gratuitas (sin API key)

| Fuente | Qué obtiene |
|---|---|
| **Reddit** | Threads + top comments con upvote counts. Free via public JSON |
| **Hacker News** | Posts + comments con puntos |
| **Polymarket** | Odds en tiempo real respaldadas por dinero real |
| **GitHub** | PRs, issues, releases, star counts |
| **YouTube** | Transcripts completos via yt-dlp |

## Fuentes con Browser Cookies (gratis)

| Fuente | Setup |
|---|---|
| **X / Twitter** | Login en x.com en cualquier browser, o set `XQUIK_API_KEY` / `XAI_API_KEY` |

## Fuentes con API Key

| Fuente | Key | Costo |
|---|---|---|
| **TikTok + Instagram + Threads + Pinterest + YouTube comments** | `SCRAPECREATORS_API_KEY` | 10K calls free, luego PAYG |
| **Perplexity Sonar / Deep Research** | `PERPLEXITY_API_KEY` o `OPENROUTER_API_KEY` | Pay-as-you-go |
| **Web search** | `BRAVE_SEARCH_API_KEY` | 2K queries/mes gratis |

## Bluesky

App password desde bsky.app — gratis.

## Flujo de Activación

1. Sin keys: Reddit + HN + Polymarket + GitHub funcionan inmediatamente
2. Run `/last30days` una vez → setup wizard unlocks más fuentes en 30 segundos
3. Keys opcionales se guardan en `~/.config/last30days/.env` o macOS Keychain
