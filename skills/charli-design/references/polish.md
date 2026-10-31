
# Frontend Polish (Impeccable Edition)

Skill unificada para diseñar, auditar, pulir y optimizar interfaces frontend al más alto nivel estético y técnico. Integra los principios del toolchain **Impeccable** (Paul Bakaus) con aceleración por hardware CSS, tipografía armónica y motion fluido.

---

## 1. Toolchain & Inicialización Rápida

Para proyectos frontend nuevos o refactors integrales, apóyate en el CLI determinista de Impeccable:
```bash
# Inicializar escaneo del proyecto y generar DESIGN.md con tokens reales:
npx -y impeccable init

# Auditar la interfaz actual buscando anti-patrones visuales:
npx -y impeccable audit
```
Si se trabaja sin CLI, seguir manualmente las leyes y comandos descritos abajo.

---

## 2. Los Comandos y Heurísticas de Diseño (Impeccable Core)

### A. `/typeset` — Escala Modular y Ritmo Tipográfico
- **Escala armónica:** Aplicar ratios matemáticos estrictos (Major Third `1.25` para dashboards o Perfect Fourth `1.33` para marketing).
- **Tracking inverso:** A mayor tamaño de fuente, menor tracking. Display (`tracking-tight` o `tracking-tighter`), body (`tracking-normal`).
- **Longitud de línea:** Límite estricto de lectura cómoda: `max-w-[65ch]`.
- **Familias premium:** Outfit, Geist, Cabinet Grotesk, Satoshi. **BAN absoluto:** Inter (genérico) y serif en paneles operativos.

### B. `/colorize` — Colorimetría Intencional (OKLCH)
- **Matriz de roles:** Background, Surface, Primary, Accent (≤10% de la pantalla), Muted y Border.
- **Cero blanco/negro puro:** Nunca `#000` ni `#fff`. Neutros teñidos sutilmente hacia el matiz de marca (croma 0.005–0.01).
- **Contraste:** Garantizar legibilidad WCAG AAA / APCA.
- **BAN:** Gradientes morado/azul estilo "AI chatbot". Bases neutras sofisticadas (Zinc/Slate) con acentos de alto contraste.

### C. `/spacing` — Densidad y Ritmo Vertical
- **Escala de 4px/8px:** Usar múltiplos consistentes (4, 8, 12, 16, 24, 32, 48, 64px).
- **Evitar la "sopa de padding":** No aplicar el mismo padding a todo. Variar densidad: compacta en paneles de datos, espaciosa en landings.
- **Cards con propósito:** No encapsular todo en tarjetas con bordes. Usar espacio en blanco y tipografía para agrupar antes que bordes pesados. Prohibidas las cards anidadas.

### D. `/animate` — Motion con Propósito Físico
- **Librería estándar:** GSAP como motor primordial (`npm install gsap`), complementado con Framer Motion si es React puro.
- **Tiempos de respuesta:** Micro-interacciones ≤ 150–200ms; transiciones de pantalla ≤ 350–400ms.
- **Curvas físicas:** Exponenciales suaves (`power2.out`, `expo.out`). Cero rebotes de caricatura (*bounce* o *elastic* prohibidos en UI seria).
- **Accesibilidad:** Respetar siempre `@media (prefers-reduced-motion: reduce)`.

---

## 3. Prohibiciones Absolutas (Anti-Slop)

1. **Card grids de 3 columnas idénticas:** Cliché de plantilla SaaS. Variar jerarquía y layout.
2. **Hero-metric template:** Número gigante centrado + label genérico sin contexto visual.
3. **Bordes stripe lateral:** `border-l-4` decorativo como falso acento.
4. **Gradient text decorativo:** `background-clip: text` en párrafos o titulares sin propósito semántico.
5. **Glassmorphism por defecto:** Raro, sutil y con propósito óptico real, o nada.
6. **Emojis en interfaces profesionales:** Usar exclusivamente iconografía SVG primitiva o librerías consistentes (Lucide, Radix, Phosphor).
7. **Modales automáticos:** Agotar alternativas inline, paneles laterales o revelación progresiva antes de bloquear la pantalla con un modal.

---

## 4. Guardarraíles de Rendimiento CSS

- **Aceleración por Hardware:** Animar **únicamente** `transform` y `opacity`. Jamás animar `top`, `left`, `width`, `height` o `margin`.
- **Estabilidad de Viewport:** Usar `min-h-[100dvh]` en lugar de `h-screen` para evitar saltos de layout en navegadores móviles (iOS Safari).
- **Coste de DOM y Filtros:** Filtros de ruido (`backdrop-blur`, SVG grain) solo en pseudo-elementos fijos con `pointer-events: none`, jamás en elementos con scroll continuo.
- **CSS Grid sobre Flex-math:** Nunca calcular anchos manuales con porcentajes (`w-[calc(33%-1rem)]`); usar CSS Grid nativo.

---

## 5. El Test "AI Slop"

Si un observador experto mira la interfaz y puede predecir la plantilla o decir "esto lo generó una IA", el diseño ha fallado.
- **Registro Brand (Landing/Portfolio):** El diseño ES la experiencia; atreverse con asimetría, tipografía display audaz y motion fluido.
- **Registro Product (App/Dashboard):** El diseño SIRVE a la tarea; priorizar velocidad de escaneo, jerarquía de datos y cero fricción cognitiva.

