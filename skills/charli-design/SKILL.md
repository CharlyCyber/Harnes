---
name: charli-design
description: >
  Núcleo de diseño del harnés CHARLI: dirección de arte anti-slop para páginas web,
  landings, portfolios y producto. Fusión (2026-10-31) de taste-skill [dirección de arte,
  bibliotecas de direcciones/paletas/tipo, verificación real en navegador] e
  Impeccable/frontend-polish [leyes tipográficas, colorimetría OKLCH, motion físico,
  aceleración CSS]. Usar para diseñar, auditar o refactorizar cualquier interfaz
  pública o de producto; también cuando alguien diga que una página se ve genérica,
  templada o "AI-made".
---

# charli-design — dirección de arte del harnés

Skill única de diseño del canon. Nació de la fusión de dos fuentes (procedencia y licencias en `skills/REGISTRO.md`):

| Aporta | Fuente | Dónde vive |
|---|---|---|
| Flujo completo de dirección de arte (investigación → dirección → secciones → verificación) | taste-skill @ `12af471f` (MIT) | `references/taste-core.md` |
| Bibliotecas: direcciones, paletas, tipografía, motions | taste-skill | `library/*.json` |
| Leyes de pulido: escala tipográfica, OKLCH, spacing, motion físico, rendimiento CSS, anti-slop | Impeccable (Paul Bakaus), derivado vendored | `references/polish.md` |
| Inspector de navegador real + escenas | taste-skill | `scripts/`, `assets/` |

## Contrato

1. **La identidad va antes que la superficie.** Primero dirección (qué mundo visual se podría defender), después paleta y tipo, después layout. Nunca al revés.
2. **Nada genérico = no entregado** (regla 10 del canon). Criterios de aceptación obligatorios: `references/brand.md` (7 criterios gradables) + el test final de esta skill.
3. **Verificación en navegador real.** El loop anti-slop solo cuenta con evidencia visual: construir → capturar → comparar → iterar usa `scripts/inspect.mjs` con el MCP `chrome-devtools`.
4. **Un registro por pantalla.** Landing/portfolio = el diseño ES la experiencia (asimetría, display audaz, motion). App/dashboard = el diseño SIRVE (velocidad de escaneo, jerarquía de datos, cero fricción). Mezclarlos es slop.

## Routing

| Necesidad | Lee |
|---|---|
| Empezar un diseño desde cero o re-dirigir uno | `references/taste-core.md` (flujo completo) |
| Elegir paleta / tipografía / dirección visual | `library/palettes.json`, `library/type.json`, `library/directions.json`, `library/motions.json` |
| Auditoría de pulido o refactor de UI existente | `references/polish.md` (leyes + prohibiciones) |
| Verificar una página ya construida | `scripts/` (inspector) + criterios de esta skill |
| CSS base / escenas de referencia | `assets/` |

## El test final (inherente a toda entrega)

Un experto mira la interfaz: **si puede predecir la plantilla o decir "esto lo generó una IA", el diseño ha fallado.** Prohibiciones duras (ley completa y remedios en `references/polish.md`): grids de 3 columnas idénticas, hero-métrica sin contexto, gradientes morado/azul de chatbot, glassmorphism por defecto, emojis como iconografía profesional, bounce/elastic en motion de UI seria.

> Si esta skill y otra de diseño del stack chocan, la ganadora es la del proyecto (el cliente manda); esta skill es el suelo CHARLI, no el techo del diseñador.
