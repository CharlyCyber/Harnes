# Registro de Decisiones

Formato: fecha — decisión — razón — evidencia/fuente.

## 2026-10-30 (tarde)

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
