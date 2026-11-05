# Registro de Decisiones

Formato: fecha — decisión — razón — evidencia/fuente.

## 2026-11-05 (endurecimiento: CI, tests y rutas prohibidas)

- **CI en cada push/PR.** `.github/workflows/doctor.yml` (runner Windows) corre los smoke tests, instala el harnés en un HOME limpio, pasa `-Verify`, `doctor.ps1` y compila los scripts Python de las skills. Razón: el sistema dependía de que el operador ejecutara el doctor a mano; un canon roto o una ruta prohibida que reaparece no se detectaban solos.
- **Smoke tests con HOME y canon desechables.** `sync/tests/run-tests.ps1` (29 comprobaciones) usa `HARNES_HOME` y `HARNES_CANON` con un canon fixture de 2 skills: rápido, determinista y sin tocar el perfil real. Razón: los dos bugs del motor encontrados al escribirlos (drift falso en máquinas sin `.qwen`/`.factory`, y `.Count` desenvuelto en PS 5.1) eran invisibles en esta máquina.
- **Rutas prohibidas declarativas.** `targets.json` gana `forbidden`; `doctor.ps1` falla si existen y `-SkipSync` permite auditar en entornos sin clientes. Razón: `~/.config/opencode/skills` es una segunda fuente de verdad que el CLI de HyperFrames repuebla; convertirla en junction permitiría podar el canon a través del enlace.
- **`sync.ps1` sale con exit 0 explícito en modo instalación.** Antes el código de salida era el último de `robocopy` (1 = copiado), así que un pipeline no podía distinguir éxito de fallo.

## 2026-11-05 (evaluación de 6 repos externos)

- **Solo se adopta `notfound-security-audit`, fusionado en `security-audit`.** Era el único que aportaba una capacidad inexistente: escáner real con reglas, dependencias y estados de confianza. Se conserva el checklist propio de 19 puntos y `audit.py`; se añade el motor `nfaudit` con su licencia MIT y atribución.
- **`addyosmani/agent-skills` (25) y `mattpocock/skills` (40): no se instalan.** Solapan entre sí en la mitad de sus skills (TDD, review, spec, triage) y con el canon (`ship`, `git-advanced-workflows`, `security-audit`, `triage`). Quedan documentados como candidatos, no instalados: el ratchet exige un fallo real, no una skill buena.
- **`affaan-m/ECC`: rechazado.** 4 701 archivos, 60 MB y 1 068 `SKILL.md` con la misma skill repetida por cliente (`.agents` 47, `.kiro` 43, `pi/core` 134) y por idioma (ja-JP 228, zh-CN 183). Sincronizarlo multiplicaría el catálogo por 30 y metería decenas de miles de tokens de descripciones en cada sesión.
- **`HKUDS/Vibe-Trading` y `Anil-matcha/Open-Generative-AI`: no son repos de skills.** El primero es una app de trading con 90 skills de dominio financiero; el segundo no contiene ni un `SKILL.md`. No hay nada que sincronizar.

## 2026-11-05 (cierre)

- **Canon completo y reproducible:** 34 skills activas (23,5 MB) viven en `skills/`. El sync ya no depende de lo que hubiera en disco: reconstruye desde el canon.
- **Sync v0.4 con junctions:** una sola copia física en `~/.agents/skills`; claude, gemini, continue, qwen, factory, crush, devin y goose reciben junction de directorio; codex recibe junction por entrada (preserva `.system`). OpenCode lee el almacén universal de forma nativa, así que se eliminó `~/.config/opencode/skills` (backup en `skills.bak-20261105-125445`). Beneficio medido: 16 skills duplicadas en hasta 8 sitios → 1 copia.
- **`sync/ledger.json` retirado:** el modelo de "puentes por ledger" se sustituye por `targets.json` (datos declarativos). Menos estado, misma neutralidad.
- **Kilocode eliminado por completo:** `@kilocode/cli` (npm global), extensión `kilocode.kilo-code-7.3.1`, `~/.kilocode` y `~/.config/kilo`. Backup de las skills y settings en `Documents\Backups\kilocode-backup-20261105.zip`.
- **Instrucciones unificadas:** `AGENTS.md` se replica a `~/.agents/AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `~/.codex/AGENTS.md`, `QWEN.md` y `~/.factory/AGENTS.md`. El `GEMINI.md` legacy (prompt del sistema anterior, UTF-8 corrupto) quedó reemplazado y respaldado.
- **Secretos:** todas las configs MCP del perfil usan `${VAR}`; logs redactados. Queda pendiente que el operador rote las keys y las fije con `setx`.

## 2026-11-05

- **Reparación del stack MCP (7 intentos → 3 operativos):** se conserva `chrome-devtools`, `context7` y `apify`; `firecrawl` sigue en `enabled: false` por egress bloqueado. El problema no era la red ni las keys sino el arranque en frío de `npx`: los paquetes se instalan globalmente y la config mantiene `npx -y paquete@version` (portable, sin rutas absolutas). Evidencia y mediciones en `failures.md` y `mcps.md`.
- **Config legacy `~\.opencode\opencode.json` neutralizada:** era la que resucitaba `markitdown`/`playwright`/`motion` y la que guardaba tres API keys en texto plano. Queda solo `$schema`; única fuente de verdad en `~\.config\opencode\opencode.json`.
- **Familia HyperFrames: no se fusiona.** 9 skills, 1 237 líneas y ~132 KB de cuerpo: fusionarlas obligaría a cargar todo el stack en cada tarea de vídeo (~35k tokens) y rompería el router (`hyperframes` → workflow). El coste real del catálogo son las descripciones (~1 línea por skill), no los cuerpos, que se cargan solo al invocar. Decisión: se mantiene la arquitectura router + dominio.

## 2026-10-31

- **Tres órdenes del operador ejecutadas en una tanda:** (1) las 7 skills dormidas **eliminadas del canon por completo** (`ui-ux-pro-max`, `web-design-pipeline`, `web-design-strategist`, `shadcn`, `material-3`, `ui-stack-recipes`, `headroom`) — sin rastros; (2) **A/B de diseño cerrado por fusión:** `design-taste-frontend` + `frontend-polish` → **`charli-design`** (biblioteca de taste como cuerpo técnico + leyes de Impeccable como doctrina; veredicto: ninguna skill existente cubría mejor la dirección de arte, así que la fusión en 1 es lo correcto); (3) **sync v0.3 neutro:** estándar universal (`~\.agents\AGENTS.md` + `~\.agents\skills\`) + puentes gobernados por `ledger.json` — cero nombres de agentes; cualquier agente del mundo sincroniza con el enlace del repo (`README` → `install.ps1` → `sync`; y si su cliente no lee el estándar universal, él mismo copia y se registra en el ledger). Protocolo Codebuff documentado en `sync/README.md` (re-PUT manual con revision; riesgo anotado: los dirs locales de skills alimentan el importer de Freebuff al arrancar).

## 2026-10-30 (tarde)

- **7 skills vendoreadas al canon como dormidas** (`ui-ux-pro-max`, `web-design-pipeline`, `web-design-strategist`, `shadcn`, `material-3`, `ui-stack-recipes`, `headroom`): salen de las ubicaciones de agentes (`~\.config\opencode\skills`, `~\.agents\skills`) y viven solo en `skills/` del repo con marcador `_DORMIDA.md`, que `sync.ps1` respeta (no instala). Razón del operador: reducir el contexto cargado en los agentes; nada destruido (bytes intactos en canon). Reactivar = borrar marcador + sync.

- **Bootstrap de una línea (`install.ps1` + documentación en README).** Compartir el repo ya es "pegar y sincronizado": `irm https://raw.githubusercontent.com/CharlyCyber/Harnes/main/install.ps1 | iex` → clona (o actualiza con `pull --ff-only`) el canon a `Documents\Proyectos\Harnés` y ejecuta `sync\sync.ps1`. Respeto de reglas: 8 (portabilidad, destino derivado de GetFolderPath, no rutas fijas) y 9 (custodia: si el destino existe y no es este repo, aborta; si el pull diverge, aborta sin reset automático). El `irm | iex` requiere Git en PATH + credencial GitHub válida (repo privado).

- **Purga server-side de Freebuff/codebuff completada — la cuenta queda con solo el harnés.** Reemplazo total vía `PUT /https://www.codebuff.com/api/v1/cloud/skills` con revision 2 → **revision 3: solo `find-skills` y `design-taste-frontend`** (32 skills viejas eliminadas server-side). Caché local alineado: dir materializado vencido borrado (ruta MAX_PATH, vía `\\?\` con Node), `current.json` reescrito con la revision 3 verificada por GET, `imported.json` reseteado a `[]`. Backup pre-purga conservado en `~/.config/freebuff-desktop/account-skills.bak-20261030`. Postmortem completo en `failures.md` (fallo key: el server es la fuente de verdad; los cachés locales resucitan si solo se borra del lado local). Nota de límites del server: `instructions ≤ 50KB`, `files[].contents ≤ 100KB`, `files ≤ 100/skill`, total ≤ 2.5MB → se excluyó del transporte `library/{sites,heroes,photos,sections}.json` (payload de 2.6MB → 1.08MB); el canon local conserva la skill completa.
- **Regla 5 (YAGNI) retirada a petición del operador.** El canon queda en 10 reglas renumeradas; referencias cruzadas actualizadas (`failures.md`, `sync.ps1`, `decisions.md`). Nota ratchet: era la única regla de estilo sin fallo directo que la respone — su retirada es coherente con la trazabilidad. Las reglas 8 (portabilidad) y 9 (custodia de proyectos) se mantienen: son la mitigación de los dos fallos graves del postmortem del AU.

- **Config de Firecrawl y keys:** el operador aprovisionó keys (`FIRECRAWL_API_KEY`, `APIFY_TOKEN`) como env vars de usuario vía setx; config de MCPs usa placeholders `${VAR}` (regla 3). Apify validado por API (FREE, cuenta `regal_crane`) y activo. Firecrawl tiene key válida pero su red es inalcanzable por egress desde el ISP del operador (`failures.md` 2026-10-30) → MCP `enabled: false` hasta haya VPN/ruta alternativa. Descartadas las alternativas oficiales de Firecrawl (OAuth hosted, CLI, skills pack): OAuth exige navegador y el CLI/skills inflarían el catálogo contra la política anti-inflación.

- **Marca reconstruida desde el portafolio:** `knowledge/brand.md` compilado íntegramente de `CharlyCyber/Charli-AI-Portfolio` (tokens Cosmos del CSS, 4 familias tipográficas self-hosted, motion físico del hero, copy real, 7 criterios de aceptación gradables). De ahí nace la **regla 10** del canon (validación antiruina: "genérico = no entregado"). La carpeta `Proyectos\Charli AI Brand OS` queda descartada como fuente (solo logos/PDF).
- **Fuga de token:** fuga real en el remote del portafolio (token OAuth en URL, saneado) → registrada en `failures.md` + primer hook del harnés: `hooks/check-secrets.ps1` (8 patrones, verificado: 0 fugas en 50 archivos). Regla 3 queda trazada a evidencia.
- **Auditoría MCPs (7 → 4):** eliminados `playwright` (duplicado de chrome-devtools), `markitdown` (nicho sin uso), `motion/motion-studio` (registry remoto dinámico, nunca cargó). Activos: `chrome-devtools`, `context7`, `firecrawl`, `apify` — canónicos en `knowledge/mcps.md`. Pendiente del operador: keys `FIRECRAWL_API_KEY` y `APIFY_TOKEN` (no existen en ninguna scope; sin ellas esos dos MCPs quedan degradables). Backup pre-auditoría en `opencode.json.bak`.

## 2026-10-30

- **Remote canónico creado:** `github.com/CharlyCyber/Harnes` (privado). Canon versionado en GitHub; sync/local sigue siendo la fuente de verdad de trabajo. Privado por contener identidad, decisiones y planes del operador.
  - Nota: se usó la credencial almacenada de Git Credential Manager (PAT clásico); el token del keyring de `gh` CLI sigue inválido (pendiente `gh auth login`).
- **Primeras adopciones al catálogo canónico:** `find-skills` (Vercel) y `design-taste-frontend` (taste-skill). Instaladas en `skills/`, sincronizadas a OpenCode. Procedencia, commit y prueba design en `skills/REGISTRO.md`.
  - Razón: find-skills resuelve un comportamiento real (descubrir skills bajo demanda sin inflar catálogo) con 1 archivo; taste-skill es el núcleo de la propuesta de valor CHARLI (dirección de arte anti-slop).
- **Stack base activo declarado:** las ~30 skills heredadas (hyperframes family, brag, last30days, rea, media-use, etc.) quedan documentadas y vigentes; el catálogo canónico lleva solo adiciones nuevas (minimalismo sin destruir herramientas reales).
- **Diferidas con vista:** security-audit de Cloudflare (para el primer proyecto cliente asegurado) y selectivas de addyosmani/mattpocock. Descartadas con razón las demás (ver REGISTRO).
- **debate abierto:** design-taste-frontend vs frontend-polish (Impeccable) se resuelve con test doble ciego en el próximo trabajo real de diseño; el perdedor sale del stack.

## 2026-10-29

- **Nace el harnás "Harnés"** tras eliminar por completo el Agente Universal (repo, carpeta, copias y configs).
  - Razón: reestructurar de cero imitando las mejores prácticas documentadas.
- **Harnás portable multi-agente** (no monolítico en un solo IDE): el repo canónico se sincroniza a OpenCode, Claude Code, Antigravity, Freebuff, etc.
  - Evidencia: el operador usa 10+ agentes; el fallo del AU no fue el concepto de sync sino su implementación (rutas absolutas rígidas → todo se rompió al mover la carpeta).
- **Mono-agente interactivo al inicio.** Sin orquestación compleja.
  - Fuente: Anthropic "Building Effective Agents" — solución más simple posible, complejidad solo cuando se necesite. Si algún día hay builds autónomos multi-hora, se añade modo planner→generator→evaluator como añadido.
- **Memoria disk-first en markdown** (este directorio). Sin servicios externos de memoria.
- **Cero skills al inicio.** Catálogo nace vacío; skills se añaden bajo demanda con estándar agentskills.io (SKILL.md + scripts/ + references/; <500 líneas, disclosure progresiva).
- **Git-gate cómo única capa de hooks inicial** (éxito silencioso, fallos verbosos), el resto de hooks nace de fallos reales (ratchet).
- **Estructura mínima:** AGENTS.md + knowledge/ + skills/ + hooks/ + sync/. Nada más hasta que la evidencia lo justifique.

## 2026-10-30

- **Purga completa del Freebuff:** carpeta del proyecto AU borrada, 3 referencias limpiadas de `state.json` (recentProjects, espacio de trabajo, collapsedProjects), `adopt-harness` retirada del bundle de skills y mención neutralizada en `chrome-devtools-mcp`. Freebuff queda sin rastros a nivel de configuración; solo persisten bases de datos de historiales de conversación (decisión: no tocar, son chats del usuario, no configs).

## Fuentes de diseño consultadas (2026-10-29)

- Anatomy of an Agent Harness — Vivek Trivedy (LangChain)
- Agent Harness Engineering — Addy Osmani (Anthropic)
- Harness design for long-running application development — Anthropic Engineering
- Building Effective Agents — Anthropic
- Agent Skills specification — agentskills.io
