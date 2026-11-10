# MCPs del harnés

> Este documento conserva observaciones históricas de una máquina (2026-11-05), no demuestra el estado actual de ninguna instalación. El inventario portable vive en `config/mcp.json` y `config/opencode.example.json` es opt-in; el sync no cambia MCPs. Verifica y rota las claves expuestas manualmente.

Estado de `~\.config\opencode\opencode.json` tras la reparación 2026-11-05.
Cada MCP justifica su existencia con comportamiento observable; los eliminados tienen registro en `decisions.md`.

## Activos

| MCP | Qué entrega | Necesita | Arranque medido | Estado |
|---|---|---|---|---|
| `chrome-devtools` | DevTools real: consola, red, performance, screenshots, interacción (29 tools en v1.6.0). Herramienta primaria de inspección web del loop anti-slop de `charli-design`. | Nada (lanza Chrome local) | 1.3 s | ✅ operativo |
| `context7` | Documentación fresca y versionada de librerías, directo de la fuente. | Key opcional (free tier funcional, verificado sin key) | 3.7 s | ✅ operativo |
| `apify` | Actores de scraping a demanda (plataformas con login, paginación pesada, redes). | `APIFY_TOKEN` (env user, cuenta `regal_crane`, plan FREE) | 8.9 s | ✅ operativo |
| `firecrawl` | Crawling/scraping estructurado de sitios (research, competidores). | `FIRECRAWL_API_KEY` (env user, key presente) | — | ⛔ `enabled: false` — egress bloqueado hacia `*.firecrawl.dev` (ver `failures.md`). Reactivar con `enabled: true` + reiniciar cuando haya VPN o cambie la red. |

## Causa raíz del apagón total (2026-10-31 → 2026-11-05)

Los 7 servidores fallaban con `Request timed out` a los ~36 s. No era la red ni las keys: **era `npx` arrancando en frío**. Medición real:

| Comando | Antes (sin caché global) | Después (paquete instalado global) |
|---|---|---|
| `npx -y @upstash/context7-mcp@3.2.5` | 41.7 s | 3.7 s |
| `npx -y chrome-devtools-mcp@1.6.0` | > 30 s (timeout) | 5.1 s |

El inicializador de OpenCode corta a los ~30 s; con `npx` resolviendo e instalando en cada arranque, todos morían antes del handshake. **Prerrequisito de la config:**

```powershell
npm i -g "@upstash/context7-mcp@3.2.5" "@apify/actors-mcp-server@0.13.0" "chrome-devtools-mcp@1.6.0"
```

Con los paquetes en caché global, `npx -y paquete@version` arranca en < 9 s y la config sigue siendo portable (sin rutas absolutas). Si algún día se limpia la caché global de npm, repetir el comando.

## Config legacy eliminada

`~\.opencode\opencode.json` (ubicación heredada) se fusionaba con la canónica y **resucitaba** `markitdown`, `playwright` y `motion` — los tres que la auditoría del 2026-10-30 había retirado — además de reactivar `firecrawl` (sin `enabled:false`) y guardar tres API keys en texto plano. Quedó reducido a `{"$schema": ...}`. Toda la config MCP vive ahora solo en `~\.config\opencode\opencode.json` con placeholders `${VAR}`.

## Keys del operador

- `FIRECRAWL_API_KEY` y `APIFY_TOKEN` viven como variables de usuario (`setx`); nunca en archivos rastreados (regla 3).
- `CONTEXT7_API_KEY` no existe y no hace falta: el free tier respondió el handshake sin key.
- Las tres keys estuvieron en texto plano en el archivo legacy. Ese archivo nunca fue un repo Git, así que no hay fuga versionada; el riesgo es local (backups, sincronización de perfil, otro proceso del usuario). **Recomendación: rotar `APIFY_TOKEN` y `FIRECRAWL_API_KEY` cuando haya 5 minutos** — cuesta menos que auditar el alcance.

## Política anti-inflación

- Menos tools = menos contexto por request, mejor foco del modelo.
- Ojo con el solape: el cliente ya trae un toolset `browser` nativo (45 tools de Review pane). `chrome-devtools` se justifica solo por lo que el nativo no da (network/performance/a11y/CDP fino); nunca cargar ambos para la misma tarea.
- Todo MCP futuro: se canonicaliza aquí con justificación de comportamiento + su env key; si deja de usarse en 2 auditorías seguidas, fuera.
