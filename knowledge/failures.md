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

## 2026-10-30 — Purga de skills: el servidor era la fuente de verdad y las borradas al nivel local resucitan

| Fallo observado | Causa raíz | Mitigación adoptada |
|---|---|---|
| Al purgar 32 skills viejas de la cuenta, borrar el bundle local (`~/.config/freebuff-desktop/account-skills/`) y resetear `imported.json` no sirvió: el servidor (`www.codebuff.com`) mantenía su copia y la app re-materializa al relanzar. | Codebuff (backend) es la fuente de verdad del catálogo de skills de la cuenta; el bundle local de Freebuff es solo un caché materializado que se repone desde el server en cada fetch. | El borrado correcto es **server-side**: `PUT /api/v1/cloud/skills` con la revision vigente y la lista **completa** de skills ( el PUT reemplaza el catálogo entero, no hace merge ). Borrar cachés locales solo sirve después de ganar el server. |
| `curl.exe` / `Invoke-RestMethod` (SChannel) fallan con `SEC_E_DECRYPT_FAILURE` descargando respuestas grandes del API de codebuff.com (>~45KB corta el stream). | TLS de SChannel en PS 5.1 no sostiene el stream contra este host. | Para JSON grande usar Node con `fetch` (OpenSSL). Token leído desde `~/.config/manicode/credentials.json` sin imprimirse jamás (regla 3). |
| Primer `PUT` rechazado HTTP 400: `files[9].contents` "too_big". Y payload completo rebasaba el refine de 2.5MB total (`JSON.stringify ≤ 2,500,000` chars). | Límites hard del server: `instructions ≤ 50,000B`, `files[].contents ≤ 100,000B`, `files ≤ 100/skill`, total ≤ 2.5MB. Los `library/*.json` de design-taste-frontend (heroes 107KB, photos 168KB, sections 280KB, sites 857KB) los exceden. | Exclusión declarada del transporte (queda en canon local): `README.md`, `LICENSE-upstream`, `library/{sites,heroes,photos,sections}.json`. Payload resultante: 1.08MB, 33 files, HTTP 200 → revision 3. |
| `Remove-Item -Recurse` falló contra el bundle vencido: ruta interna > 260 chars (clásico MAX_PATH de Windows). | PowerShell 5.1 no maneja rutas largas. | Borrado vía Node con fs.rmSync y prefijo `\\?\` (si aplicare fallback: `robocopy /MIR` de un dir vacío). |
| `install.ps1` escrito en UTF-8 **sin BOM** rompió el parser de PowerShell 5.1 con acentos dentro de strings ("Token '}' inesperado"). | PS 5.1 lee archivos sin BOM como ANSI; los bytes UTF-8 multi-byte se moodian y una secuencia puede desbalancear strings. | Todo `.ps1` del harnés se escribe en UTF-8 con BOM. Verificación de sintaxis antes de ejecutar: `[Parser]::ParseFile(...) | % errores`. |

## 2026-10-30 — Fuga de token OAuth en la URL de un remote Git
