# Registro de Fallos (el trinquete)

Cada fallo del agente (del Agente Universal o de este harnés) queda registrado aquí y, si procede, se convierte en una regla en AGENTS.md, un hook o una skill. Sin evidencia no se añade regla.

## 2026-11-05 — Segunda fuente de verdad en OpenCode y bugs que solo aparecen en una máquina limpia

| Fallo observado | Causa raíz | Mitigación adoptada |
|---|---|---|
| `~/.config/opencode/skills` reapareció 22 minutos después de borrarla y de verificar que no existía: carpeta real con 5 skills de HyperFrames en versión condensada (7 KB frente a 20 KB del canon). | El CLI de HyperFrames escribe sus skills en esa ruta cuando detecta OpenCode y reconcilia el directorio, podando lo que no reconoce. [Likely] Es el mismo proceso que hizo desaparecer 7 skills del almacén universal. | Ruta declarada en `forbidden` dentro de `targets.json`; `doctor.ps1` falla si existe. Prohibido convertirla en junction: el proceso podaría las 34 skills del canon a través del enlace. |
| `sync.ps1 -Verify` marcaba drift permanente en una máquina sin `.qwen` ni `.factory`: la instalación saltaba esas instrucciones pero la verificación las contaba como desactualizadas. El doctor nunca habría salido verde fuera de este PC. | La guarda "cliente no instalado" estaba después del `Backup-Path`, no antes de comparar. | Guarda de directorio padre movida al inicio del bucle de instrucciones: lo que no se instala tampoco cuenta como drift. Detectado por el primer test con un HOME desechable. |
| La comprobación de rutas prohibidas no encontraba nada con una sola entrada en `targets.json`. | Envolver con `@()` la entrada de un `Where-Object` no envuelve su salida: la asignación se desenvuelve y `.Count` sobre un `PSCustomObject` no vale 1 en PowerShell 5.1. | Pipeline envuelto en `@()` al asignar. Cubierto por el test 7. |

Ambos bugs del motor llevaban tiempo ahí y ninguno se veía en la máquina del operador: los encontró el primer smoke test con `HARNES_HOME` desechable. De ahí que los tests y el CI pasen a ser parte del harnés, no un extra.

## 2026-11-05 — Siete skills desaparecen solas y el sync no converge

| Fallo observado | Causa raíz | Mitigación adoptada |
|---|---|---|
| 7 skills del stack HyperFrames (`general-video`, `hyperframes-animation`, `hyperframes-audio`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-studio`) desaparecieron de `~/.agents/skills` con el canon intacto; el catálogo del agente pasó de 34 a 27 sin error visible. | Un proceso externo al harnés escribe en `~/.agents/skills` (el importador de la app de skills reconcilia ese directorio con su cuenta y borra lo que no reconoce). [Likely] No hay log del harnés porque el borrado no lo hace el harnés. | `sync.ps1 -Verify` lo detecta como drift y `sync.ps1` restaura desde el canon; `doctor.ps1` lo reporta como fallo. Pendiente: ejecutar `-Verify` tras cualquier arranque de esa app, o excluir el directorio del importador. |
| `sync.ps1 -Verify` seguía marcando 4 skills como "desactualizada" después de copiarlas. | `robocopy /E` copia pero no borra: un archivo huérfano dentro de la skill (`remotion-to-hyperframes/scripts/tests/boxSizing.test.mjs`) hacía que la huella del destino nunca coincidiera con la del canon. | Copia del almacén universal pasa a `robocopy /MIR`: el destino es derivado y debe quedar idéntico, huérfanos incluidos. |

## 2026-11-05 — Consolidación del canon: copias anidadas, junctions colgantes y secretos repartidos

| Fallo observado | Causa raíz | Mitigación adoptada |
|---|---|---|
| 18 skills del árbol de OpenCode contenían una copia de sí mismas (`skill/skill/`), duplicando su peso (p. ej. `brag` 31,6 MB → 15,8 MB reales). | Vendoreo con `Copy-Item -Recurse` sobre un destino ya existente, sin sanear antes. | Canon reconstruido sin anidados; `doctor.ps1` falla si detecta `skills/<n>/<n>`. |
| `.kilocode/skills` tenía 12 junctions apuntando a `~/.agents/skills/<n>` que ya no existían (skills fantasma que contaban como "exclusivas"). | La purga anterior borró los destinos pero no los enlaces. | Kilocode eliminado por completo (CLI, extensión, `~/.kilocode`, `~/.config/kilo`); backup en `Documents\Backups`. `sync.ps1` borra enlaces con `Directory.Delete(false)` para no seguir nunca el destino. |
| Keys de Firecrawl, Apify, Context7 y GitHub OAuth en texto plano repartidas por `~/.gemini/settings.json`, tres `mcp_config.json` de Antigravity y decenas de logs de sesión. | Cada agente mantiene su propia copia de config; los secretos se pegaron a mano en cada una. | Configs reescritas con placeholders `${VAR}`; logs redactados; `doctor.ps1` escanea el perfil y falla si aparece un patrón de key. Rotación pendiente del operador. |
| El sync moría por timeout del entorno: hasheaba ~47 MB (SHA-256 por archivo) en cada pasada. | Fingerprint criptográfico innecesario para comparar árboles. | Huella barata (ruta + tamaño + mtime UTC); `robocopy` preserva timestamps, así que una edición real siempre se detecta. |

## 2026-11-05 — Apagón total de MCPs, config legacy que resucita lo retirado y keys en texto plano

| Fallo observado | Causa raíz | Mitigación adoptada |
|---|---|---|
| Los 7 MCP declarados fallaban en cada arranque con `Request timed out` a los ~36 s; sesión sin una sola herramienta MCP. | `npx` resolvía e instalaba el paquete en cada arranque (41.7 s medidos para context7) y el inicializador de OpenCode corta a los ~30 s. | Paquetes MCP instalados globalmente (`npm i -g`); con caché, `npx -y paquete@version` arranca en 1.3–8.9 s. Prerrequisito documentado en `mcps.md`. |
| `markitdown`, `playwright` y `motion` seguían intentando conectar pese a la auditoría que los retiró, y `firecrawl` se activaba aunque la canónica lo apaga. | `~\.opencode\opencode.json` (ubicación heredada) se fusiona con la canónica; la auditoría del 2026-10-30 solo limpió `~\.config\opencode\opencode.json`. | Config legacy reducida a `{"$schema": ...}`; fuente única de MCP en la ruta canónica. |
| `FIRECRAWL_API_KEY`, `APIFY_TOKEN` y `CONTEXT7_API_KEY` estaban escritas en texto plano en esa config. | Se escribieron antes de adoptar el patrón `${VAR}` y nunca se revisó la ubicación heredada. | Claves borradas del archivo; las keys reales viven solo en env de usuario. Recomendada rotación de Apify y Firecrawl (coste 5 min vs. auditar alcance). |
| `knowledge/mcps.md` documentaba "4 operativos" y keys "ausentes en todo scope" cuando la realidad era la contraria. | El documento se escribió como estado puntual y no se revalidó al cambiar el entorno. | Estado re-medido (arranques, keys, egress) y `mcps.md` reescrito con fecha y evidencia. |

## 2026-10-31 — Vendoreo sin saneo y deslices de tipeo del agente

| Fallo observado | Causa raíz | Mitigación adoptada |
|---|---|---|
| El vendoreo de ayer trajo copias anidadas de sí mismas (`skills/shadcn/shadcn/`, `skills/headroom/headroom/`...) por no sanear al copiar (hoy quedó sin efecto tras la eliminación de las dormidas; la regla queda para el próximo vendoreo). | Copia tal cual de installs heredados sin inspección previa. | Regla de vendoreo: verificar la estructura antes y después de copiar — no puede existir `{dest}/{name}` anidada. |
| Deslices míos de tipeo en archivos del canon (caracteres fuera de idioma y frases corrompidas a mitad de edición) en 4+ archivos hoy. | Escritura rápida sin relectura del resultado. | Cada escritura/edición en un archivo del canon cierra con relectura del bloque escrito (misma disciplina que el parse-check de .ps1: BOM + Parser). |

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
| `Remove-Item -Recurse` falló contra el bundle vencido: ruta interna > 260 chars (clásico MAX_PATH de Windows). | PowerShell 5.1 no maneja rutas largas. | Borrado vía Node con fs.rmSync y prefijo `\\?\` (si se aplica el fallback: `robocopy /MIR` de un dir vacío). |
| `install.ps1` escrito en UTF-8 **sin BOM** rompió el parser de PowerShell 5.1 con acentos dentro de strings ("Token '}' inesperado"). | PS 5.1 lee archivos sin BOM como ANSI; los bytes UTF-8 multi-byte se modifican y una secuencia puede desbalancear strings. | Los scripts con texto no ASCII requieren UTF-8 con BOM en PS 5.1; los wrappers actuales son ASCII. Verificación de sintaxis antes de ejecutar: `[Parser]::ParseFile(...) | % errores`. |
