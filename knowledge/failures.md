# Registro de Fallos (el trinquete)

Cada fallo del agente (del Agente Universal o de este harnés) queda registrado aquí y, si procede, se convierte en una regla en AGENTS.md, un hook o una skill. Sin evidencia no se añade regla.

## 2026-10-29 — Postmortem del Agente Universal

| Fallo observado | Causa raíz | Mitigación adoptada |
|---|---|---|
| Mover/renombrar el proyecto rompió todo: AGENTS.md, skills, configs de Gemini/Kilo/DSH con rutas muertas. | Rutas absolutas en archivos copiados/vendoreados. | Regla 8 de AGENTS.md: solo rutas relativas. |
| El sync dejaba rastros en múltiples destinos (skills duplicadas en 3 ubicaciones, bundles cacheados) y la limpieza fue laboriosa. | El sync no era idempotente ni tenía un registro de lo instalado. | Pendiente: sync determinista e idempotente, con ledger de lo instalado (sync/). |
| Catálogo de 27 skills inflando el contexto antes del primer agente en actuar. | Skills sin justificación de comportamiento. | Catálogo inicial vacío; cada skill futura justifica el comportamiento que entrega. |
| Sin capa anti-destruccion: una limpieza global pudo dañar trabajo irreemplazable. | Cero hooks de seguridad. | Regla 9 (custodia de proyectos); hook destructivo cuando existan hooks. |
| Desconocimiento de dónde estaba instalado qué (skills viviendo en 3 ciudades). | Sin fuente única de verdad. | Este repo es canónico; las copias son derivadas reproducibles con sync. Si se rompe el canon, reconstruir limpio. |

## 2026-10-30 — Bloqueo de red hacia firecrawl.dev (key válida, ruta muerta)

| Fallo observado | Causa raíz | Mitigación adoptada |
|---|---|---|
| `api.firecrawl.dev` y `mcp.firecrawl.dev` se agotan a nivel TCP (DNS resuelve a IP GCP; google.com responde 200 en la misma sesión). El MCP de firecrawl sería aire. | Bloqueo de egress de la red local del operador (Mayabeque, Cuba) hacia las IPs GCP de Firecrawl. No es problema de la key ni de config. | Key guardada en env var de usuario (`FIRECRAWL_API_KEY`), config MCP instalada con `enabled: false` — lista para reactivar cuando cambie la red o haya VPN (`enabled: true` y reiniciar OpenCode). Apify (AWS) sí es alcanzable y quedó activo con su token. |

## 2026-10-30 — Fuga de token OAuth en la URL de un remote Git

| Fallo observado | Causa raíz | Mitigación adoptada |
|---|---|---|
| El remote `origin` del portafolio tenía un token GitHub OAuth incrustado en la URL (`https://CharlyCyber:gho_...@github.com/...`), visible en cualquier `git remote -v` o screenshot de config. | La app que configuró el remote incrustó credenciales en lugar de usar un credential helper. | Remote reseteado a URL limpia (la autenticación salió por Git Credential Manager desde entonces). Hook `hooks/check-secrets.ps1` para detectar el patrón en todo el árbol de trabajo antes de commitear. |

**Regla derivada:** jamás incrustar credenciales en URLs de remote; los secretos solo viven en variables de entorno o archivos locales no rastreados (ya elevado a regla 3 del canon con este fallo como prueba).
