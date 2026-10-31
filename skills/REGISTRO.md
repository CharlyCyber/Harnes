# Registro del Catálogo

Cada skill del canon, su procedencia exacta, licencia y el comportamiento que justifica su existencia (ratchet). Las skills ya instaladas en los agentes antes de este registro viven en la sección "Stack base activo" abajo — no se duplican en el canon; se reproducen desde su upstream o se adoptarán bajo demanda.

## Adopciones propias del harnés

| Skill | Fuente / commit | Licencia | Comportamiento justificado |
|---|---|---|---|
| `find-skills` | vercel-labs/skills @ `92a9a34a` | MIT (LICENSE-upstream) | Descubrir/instalar skills del ecosistema abierto a demanda, sin inflar el catálogo canónico |
| `charli-design` | Fusión propia (2026-10-31): taste-skill (Leonxlnx @ `12af471f`) + Impeccable (pbakaus, derivado vendored) | MIT (LICENSE-upstream de taste; Impeccable sin licencia en el derivado, uso interno) | Núcleo de la propuesta de valor CHARLI: dirección de arte anti-slop con biblioteca de direcciones/paletas/tipo + leyes de pulido (tipografía, OKLCH, motion físico) + verificación real en navegador. Una sola skill en vez de dos competidoras |

Notas:
- **A/B cerrado (2026-10-31, decisión del operador):** el test doble ciego (`design-taste-frontend` vs `frontend-polish`) se resuelve por fusión: la biblioteca pesada de taste (2.4MB: direcciones, paletas, inspector de navegador, scripts) queda como cuerpo técnico; las leyes destiladas de Impeccable quedan como doctrina en `references/polish.md`. Retiradas ambas con sus bytes preservados en la fusión.
- `charli-design`: `SKILL.md` es router leve (~4KB); el cuerpo técnico está en `references/taste-core.md` (38KB) y `references/polish.md` (4.6KB). Cumple el estándar `<500 líneas`.
- **Difidas (no instaladas, on-demand):** `security-audit` de Cloudflare (53k★, audit de 6 fases — adoptar en el primer proyecto cliente que aseguremos); `browser-testing-with-devtools` + `frontend-ui-engineering` de addyosmani/agent-skills; `diagnosing-bugs` + `code-review` de mattpocock/skills.
- **Descartadas con razón:** ECC (duplica infraestructura, sistema de harnés paralelo), notfound-security-audit (redundante con la de Cloudflare y sin track record), Open-Generative-UI (plataforma, no skill; posición uncensored inaceptable), Vibe-Trading (fuera de perfil), raptor (ofensiva, fuera de perfil), GSAP/anime.js/three.js (librerías de proyecto, no skills del harnés), crowd de diseño UI (ver retiradas abajo: quedan cubiertas por `charli-design` + context7/docs).
- **Retiradas (ex-instaladas; sin bytes destruidos: lo fusionado se conserva en `charli-design`, el restante vive en upstream):** `ui-ux-pro-max`, `web-design-pipeline`, `web-design-strategist`, `shadcn`, `material-3`, `ui-stack-recipes`, `headroom` (7× dormidas→eliminadas 2026-10-31, decisión del operador); `design-taste-frontend` + `frontend-polish` (absorbidas por `charli-design`).

## Stack base activo (heredado del harnés anterior, válido)

Instaladas en `~\.config\opencode\skills` y `~\.agents\skills` desde antes de este registro. Se mantienen; procedencia documentada aquí:

- **hyperframes family** (core, cli, animation, audio, creative, keyframes, registry, studio, general-video) — upstream: heygen-com/hyperframes. Stack de vídeo HTML→MP4: el flujo principal de trabajo creativo.
- **brag** (latent-spaces/brag @ fd7de7e4) — vídeo de lanzamiento en un comando.
- **last30days** (mvanhorn/last30days-skill) — investigación social de los últimos 30 días.
- **reverse-engineer-anything** (morluto/rea) — ingeniería inversa con agentes.
- **media-use** — resolución BGM/SFX/TTS/voiceover para proyectos de vídeo.
- **caveman, cavecrew, security-audit, ship, no-mistakes, web-animation, mobile-design, context7, analizar-videos, chrome-devtools-mcp, scroll-film-studio, 3d-web-designer y demás web/helpers genéricos** — utilitarias, conservadas en la purga de 2026-10-29.
