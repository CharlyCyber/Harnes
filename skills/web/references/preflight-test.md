# Test previo a producir (cuando sea aconsejable)

Un test es un gate barato antes del gasto grande: se hace cuando aporta y se
salta cuando no. No es un requisito universal ni un trámite.

## Cuándo es aconsejable

- Webs nuevas públicas (landing, tienda, institucional, portfolio), rediseños
  completos o trabajo de cliente/publicación.
- Componentes o features no triviales en un proyecto existente (con alcance y
  criterios de aceptación poco claros).
- Dirección de arte poco definida, dudas de marca, assets o derechos.
- El usuario pide explícitamente un test o un mock previo.

## Cuándo se omite

- Fixes puntuales, ajustes de CSS/copy/contraste, re-deploy.
- Componentes triviales y aislados con especificación clara.
- Iteración sobre un probe ya aprobado en esta misma sesión.

Si dudas, haz el test; nunca pidas permiso para un test ligero.

## Formato del test

Un solo mensaje con las partes necesarias. Numera las preguntas y permite
responder en corto (`1a, 2 editorial, 5: tailwind existente`). Deduce lo que el
repo o el encargo ya respondan y **no lo preguntes** (lee `package.json`, el
lockfile, la config, la guía de marca si existe). Ofrece defaults razonables
("si no dices breakpoints, uso los estándar"). Guarda las respuestas en
`brief.md` dentro de la carpeta del proyecto para trazabilidad.

## A. Test de tipo y estilo web

### A1. ¿Qué vas a construir? (elige una)

| # | Tipo de pieza | Ruta en el canon |
|---|---------------|--------------------|
| a | Landing / marketing one-pager | design + animation |
| b | Sitio institucional / corporativo | design |
| c | Tienda / e-commerce | design (+animation en PDP) |
| d | App web / dashboard / SaaS | design + animation (+context7 para libs) |
| e | Portfolio / personal / showcase | design (+3d si procede) |
| f | Blog / editorial / contenido | design (tipografía editorial) |
| g | Docs / centro de ayuda | design (mínimo visual) |
| h | Microsite de evento/campaña | design + animation |
| i | Web 3D o inmersiva | `3d-web-designer` |
| j | Scroll-film cinematográfica | `scroll-film-studio` |
| k | Otro (describe) | el router decide |

### A2. Sensación y estilo (elige una o dos)

Minimal/premium · editorial/tipográfico · corporativo limpio · brutalista ·
retro/analog · playful · elegante/lujo · técnico/dev · artesanal · otra.
**Pide 1–3 referencias (links) y qué evitar.** Si es proyecto CHARLI aplica el
canon de marca; si es cliente, su identidad.

### A3. Objetivo y audiencia

Qué debe lograr la pieza (convertir, informar, reclutar, vender, emocionar…) y
a quién va dirigida. Una frase basta.

### A4. Plataforma y responsive

Mobile-first o desktop-first · breakpoints (default: 480/768/1024/1440) ·
dark mode sí/no · destino (web normal, webview, PWA).

### A5. Stack y proyecto

¿Proyecto existente o greenfield? · framework (React/Next, Vue, Astro, Svelte,
vanilla…) · CSS (Tailwind, CSS modules, vanilla…) · librería de componentes
(shadcn, MUI, propia…) · **respeta el stack; no migres sin permiso**. En
greenfield, propón uno con criterio y pregunta.

### A6. Marca y contenido

¿Del cliente o CHARLI? · assets disponibles: logo, colores, fuentes, iconos
(sube o enlaza; verifica licencia de fuentes/iconos/imágenes/fotografía). ·
¿Copy final, esqueleto o lorem aprobado? · ¿idioma(s)?

### A7. Accesibilidad y soporte

WCAG AA por defecto (contraste, foco, teclado, labels, `prefers-reduced-motion`).
¿El proyecto define política de browsers (Electron/Tauri/WebView o lista)? Si
no la hay, asume Baseline Widely available + fallbacks de las guías nativas.

### A8. Presupuesto de rendimiento

CWV objetivo (por defecto: LCP ≤2.5 s, INP ≤200 ms, CLS ≤0.1) o "sin
presupuesto" (demo interna). ¿Imágenes/fonts propios para optimizar? ¿Peso
crítico (hero/video)?

### A9. Estructura y CTA

Secciones/bloques clave · CTA principal · formularios (¿a dónde van?) ·
navegación/footer · integraciones (analytics, embeds, pagos).

### A10. Puertas de aprobación

¿Mock/styleframe del hero antes del build completo? · ¿Revisión sobre preview
deploy o sobre screenshots? · ¿Quién aprueba y para cuándo?

## B. Test del entorno (silencioso, sin instalar nada)

Comprueba y reporta en pocas líneas: runtime (`node --version`, gestor de
paquetes por lockfile: pnpm/yarn/npm/bun), framework del proyecto (`package.json`),
`git status` breve, navegador disponible (Chrome/Chromium), MCP de navegador
(`chrome-devtools-mcp`) u otra vía de verificación real, espacio en disco. Lo
que falte degrada el plan y se declara; **no instales ni actualices nada sin
autorización**.

## C. Test de render (probe)

Genera el menor artefacto que pruebe las decisiones de riesgo y enséñaselo
antes de la pieza completa, ajustado al tipo elegido en A1:

- a/b/c/f/g/h: hero o primera viewport (y dark mode si aplica) con el estilo
  real —colores, tipo, espaciado, motion clave— como mock o como código del
  proyecto (preferible, para que el OK sea sobre lo real).
- d/e: componente clave aislado en el estado más representativo.
- i: scene three vanilla mínima (o la escena central) renderizando el frame
  clave.
- j: styleframe de la escena crítica en el estilo artístico elegido.

Criterios de aprobado: jerarquía y legibilidad, fidelidad de marca, responsive
real (al menos móvil y desktop), estados vacíos/largos (textos largos, imágenes
faltantes), sin contenido de relleno no aprobado ni enlaces muertos, contraste
AA. Si el probe falla en algo bloqueante, corrige y repite; si pasa, el OK del
usuario es el contrato para el build completo. Declara tiempo y coste; piezas
grandes pueden tener un segundo probe tras los ajustes.

Tras el build, verificación final: navegador real (consola, red, screenshots en
breakpoints, teclado/foco, reduced-motion, CWV si el MCP lo permite); lo que no
puedas verificar, se declara. El test previo es por proyecto y no sustituye la
evaluación de la skill (si existiera un protocolo equivalente para web).
