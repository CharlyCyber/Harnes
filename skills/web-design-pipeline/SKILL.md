---
name: web-design-pipeline
description: >
  Pipeline orquestador de diseño y desarrollo web de nivel mundial: la puerta de
  entrada única a TODO trabajo web. Usar cuando el operador pide una landing page,
  portfolio, sitio de producto, dashboard, e-commerce, rediseño, "diseña una página",
  "hazme una web", web design, UI, frontend o interfaz. Encadena por fases las skills
  especializadas de diseño (estrategia → UI → componentes → motion → inmersión →
  pulido) garantizando que no se pasa nada por alto, cargando cada SKILL.md solo en
  su fase para no inflar el contexto.
---

# Web Design Pipeline — Orquestador de Diseño Web

Esta skill NO contiene técnicas de diseño: es el **conductor** que garantiza que ningún
trabajo web se salta una fase. En cada fase, lee el `SKILL.md` de la skill indicada y aplica
sus reglas íntegras antes de avanzar. Carga una sola skill por fase (progressive disclosure).

## Reglas del pipeline

1. Ejecuta las fases en orden. Una fase solo se cierra cuando su entregable existe.
2. Lee únicamente el `SKILL.md` de la fase activa; no precargues el resto.
3. Una fase opcional solo se omite con justificación explícita al operador.
4. Si el encargo es una modificación puntual, no reinicies: entra por la fase que
   corresponde al cambio y recorre desde ahí hasta el final.

## Fases

| # | Fase | Skill a leer | Entregable |
|---|---|---|---|
| 1 | Estrategia | `skills/web-design-strategist/SKILL.md` | Objetivo, audiencia, narrativa y estructura de páginas. |
| 2 | Dirección visual | `skills/ui-ux-pro-max/SKILL.md` | Estilo, paleta y tipografía decididos (consulta su base de datos). |
| 3 | Componentes | `skills/shadcn/SKILL.md` | Sistema de componentes. Solo si el stack es React/Next; si no, aplica sus principios al stack real. |
| 4 | Motion | `skills/web-animation/SKILL.md` | Animaciones: micro-interacciones, scroll triggers, transiciones de página. |
| 5 | Inmersión (opcional) | `skills/3d-web-designer/SKILL.md`, `skills/hyperframes/SKILL.md`, `skills/scroll-film-studio/SKILL.md` | 3D interactivo, escenas de video en HTML o scrollytelling, según lo pida el proyecto. |
| 6 | Pulido final | `skills/frontend-polish/SKILL.md` | Auditoría anti-slop, tipografía, colorimetría, rendimiento y "Test AI Slop" superado. |

## Cierre

- Verifica responsive, accesibilidad y `prefers-reduced-motion` (reglas de las fases 4 y 6).
- Skills complementarias fuera del pipeline (`material-3`, `mobile-design`) se activan
  bajo demanda si el proyecto lo exige.
- Reporta al operador qué fases corrieron, cuáles se omitieron y por qué.
