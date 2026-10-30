---
name: ui-stack-recipes
description: Recetas de implementacion por stack (shadcn/ui, Material Design 3, Three.js/React Three Fiber, mobile nativo) con sus reglas, APIs y trampas. Usar cuando el proyecto ya tiene un stack UI definido y necesitas la receta concreta, no criterio de diseño general.
---

# ui-stack-recipes — recetas por stack

Este archivo es un **router**. La doctrina de diseño (tipografía, color, jerarquía, anti-slop) vive en `frontend-polish`. Aquí solo está lo que depende del stack.

## Qué leer

| Pila | Lee | Cuándo |
|---|---|---|
| shadcn/ui (React, Next.js) | `references/shadcn/` | Componentes Radix, `cn()`, formularios con react-hook-form + zod, theming, iconos Lucide, CLI y registry. |
| Material Design 3 | `references/material-3/` | Color dinámico (Monet), type y shape scale, catálogo de componentes, theming, navegación y window size classes. |
| Three.js / React Three Fiber | `references/three.md` | Escenas 3D, pipeline de modelos GLB, scroll-driven 3D, anti-patrones (3D por el 3D, 3D solo desktop, sin estado de carga). |
| Mobile nativo | `references/mobile/` | iOS y Android: táctil, navegación, tipografía, color, rendimiento, testing, backend y `scripts/mobile_audit.py`. |

## Reglas de uso

1. **El stack lo decide el proyecto, no la receta.** Si el proyecto no tiene stack definido, no elijas tú: pregunta o usa `frontend-polish`.
2. **Una receta, un archivo.** Lee solo la fila que aplica; las referencias son autocontenidas.
3. **Los ejemplos son de referencia, no de copia.** Adapta al código y a las convenciones reales del repo.
4. **Móvil y 3D tienen coste de runtime.** Aplica los guardarraíles de la referencia (fallback estático, `prefers-reduced-motion`, calidad reducida en móvil) aunque el diseño los ignore.
5. **Cuando la receta y `frontend-polish` chocan**, manda `frontend-polish` para criterio estético y la receta para la API concreta.
