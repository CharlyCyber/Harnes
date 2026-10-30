# Registro de Decisiones

Formato: fecha — decisión — razón — evidencia/fuente.

## 2026-10-30

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
