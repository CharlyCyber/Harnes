# MCPs del harnés

Estado de `~\.config\opencode\opencode.json` tras la auditoría 2026-10-30 (7 → 4).
Cada MCP justifica su existencia con comportamiento observable; los eliminados tienen registro en `decisions.md`.

## Activos

| MCP | Qué entrega | Necesita | Estado |
|---|---|---|---|
| `chrome-devtools` | Debugging/automatización de navegador real: consola, red, performance, screenshots, interacción (43 tools). Herramienta primaria de inspección web y del loop anti-slop de `design-taste-frontend`. | Nada (lanza Chrome local) | ✅ operativo |
| `context7` | Documentación fresca y versionada de librerías, directo de la fuente. | Key opcional (free tier funcional) | ✅ operativo |
| `apify` | Actores de scraping a demanda (plataformas con login, paginación pesada, redes). | `APIFY_TOKEN` (env user, validado: cuenta `regal_crane`, plan FREE) | ✅ operativo |
| `firecrawl` | Crawling/scraping estructurado de sitios (research, investigación de competidores). | `FIRECRAWL_API_KEY` (env user, key válida) | ⛔ `enabled: false` — bloqueo de egress de la red local hacia `*.firecrawl.dev` (detail en `failures.md`). Reactivar cuando cambie la red o haya VPN: `enabled: true` + reiniciar OpenCode. |

## Keys del operador (2026-10-30)

- `FIRECRAWL_API_KEY` y `APIFY_TOKEN` inyectadas como variables de usuario (`setx`) por el operador. Jamás en archivos rastreados (regla 3).
- Nunca pegar las keys en `opencode.json` ni en el canon: la config usa placeholders `${VAR}` resueltos por la env del proceso.
- Validación: Apify OK directa vía API; Firecrawl key no verificable online por el bloqueo de red (queda para verificar cuando haya ruta).

## Pendiente del operador (2 minutos cada una)

Las keys NO existen en ningún scope (Process/User/Machine) — los placeholders `${VAR}` quedan vacíos:

1. Crear `FIRECRAWL_API_KEY` en firecrawl.dev (free tier) → `setx FIRECRAWL_API_KEY "fc-..."`.
2. Crear `APIFY_TOKEN` en apify.com → `setx APIFY_TOKEN "apify_api_..."`.
3. `CONTEXT7_API_KEY` opcional: si algún día hay rate limits, key en dashboard.upstash.com.

Sin ellas, los MCPs agrican herramientas que fallan al invocarse (contexto gastado sin beneficio). Si las keys nunca llegan, la próxima auditoría los saca.

## Eliminados (2026-10-30, justificación ratchet)

| MCP | Razón |
|---|---|
| `playwright` | Duplicado funcional de `chrome-devtools` (dos servidores de navegador = doble gasto de contexto por request para la misma capacidad). |
| `markitdown` | Nicho estrecho (conversión de docs a markdown) sin uso real; `webfetch` builtin cubre lo esencial. |
| `motion` (motion-studio) | Instalado desde `api.motion.dev/registry.tgz` a 4.1.1 — servidor remoto dinámico que la sesión nunca termino de cargar; riesgo de suministro sin beneficio observable. |

Backup pre-auditoría: `~\.config\opencode\opencode.json.bak` (local, no rastreado).

## Política anti-inflación

- Menos tools = menos contexto por request, mejor foco del modelo.
- Todo MCP futuro: se canonicaliza aquí con justificación de comportamiento + su env key; si deja de usarse en 2 auditorías seguidas, fuera.
