# Registro del Catálogo

Cada skill del canon, su procedencia exacta, licencia y el comportamiento que justifica su existencia (ratchet). Las skills ya instaladas en los agentes antes de este registro viven en la sección "Stack base activo" abajo — no se duplican en el canon; se reproducen desde su upstream o se adoptarán bajo demanda.

## Adopciones propias del harnés

| Skill | Fuente / commit | Licencia | Comportamiento justificado |
|---|---|---|---|
| `find-skills` | vercel-labs/skills @ `92a9a34a` | MIT (LICENSE-upstream) | Descubrir/instalar skills del ecosistema abierto a demanda, sin inflar el catálogo canónico |
| `design-taste-frontend` | Leonxlnx/taste-skill @ `12af471f` | MIT (LICENSE-upstream) | Dirección de arte + verificación real en navegador contra páginas AI-genéricas (anti-slop). Núcleo de la propuesta de valor CHARLI |

Notas:
- `design-taste-frontend`: `SKILL.md` tiene 542 líneas (recomendación del estándar: <500) — se vendoreó tal cual upstream; si crece más, fragmentar en `references/`.
- Pendiente de test doble ciego contra `frontend-polish` (derivado vendored de pbakaus/impeccable): el perdedor sale del stack activo.
- **Difidas (no instaladas, on-demand):** `security-audit` de Cloudflare (53k★, audit de 6 fases — adoptar en el primer proyecto cliente que aseguremos); `browser-testing-with-devtools` + `frontend-ui-engineering` de addyosmani/agent-skills; `diagnosing-bugs` + `code-review` de mattpocock/skills.
- **Descartadas con razón:** ECC (duplica infraestructura, sistema de harnés paralelo), notfound-security-audit (redundante con la de Cloudflare y sin track record), Open-Generative-AI (plataforma, no skill; posición uncensored inaceptable), Vibe-Trading (fuera de perfil), raptor (ofensiva, fuera de perfil), GSAP/anime.js/three.js (librerías de proyecto, no skills del harnés), brag/rea/last30days/hyperframes/impeccable (ya instaladas en el stack activo).

## Stack base activo (heredado del harnés anterior, válido)

Instaladas en `~\.config\opencode\skills` y `~\.agents\skills` desde antes de este registro. Se mantienen; procedencia documentada aquí:

- **hyperframes family** (core, cli, animation, audio, creative, keyframes, registry, studio, general-video) — upstream: heygen-com/hyperframes. Stack de vídeo HTML→MP4: el flujo principal de trabajo creativo.
- **brag** (latent-spaces/brag @ fd7de7e4) — vídeo de lanzamiento en un comando.
- **last30days** (mvanhorn/last30days-skill) — investigación social de los últimos 30 días.
- **reverse-engineer-anything** (morluto/rea) — ingeniería inversa con agentes.
- **frontend-polish** (derivado vendored de pbakaus/impeccable) — vocabulario de diseño anti-slop. Compitiendo con design-taste-frontend.
- **media-use** — resolución BGM/SFX/TTS/voiceover para proyectos de vídeo.
- **caveman, cavecrew, shadcn, ui-ux-pro-max, security-audit, ship, no-mistakes, ui-stack-recipes, web-animation, mobile-design, context7, headroom, analizar-videos, chrome-devtools-mcp, material-3, html-based helpers y demás skills genéricas** — utilitarias, conservadas en la purga de 2026-10-29.
