---
name: web
description: >
  Universal entry point for designing, building, styling, animating and verifying
  web pages, sites and web apps: landing pages, marketing sites, storefronts,
  product UIs, dashboards, design systems, interactive product or portfolio demos,
  web animation, 3D/WebGL scenes and scroll-driven cinematic sites. Route by deliverable and existing project, then
  load only needed internal workflows. Use for any web design or frontend build
  request, including explicit /web.
---

# Web — entrada única

Usa esta skill para cualquier tarea de diseño o desarrollo web, incluso rediseños, auditorías anti-slop, componentes, animación, 3D o scroll-films. Responde en el idioma del usuario. Este router tiene prioridad sobre las instrucciones de enrutamiento, instalación, proveedores, actualizaciones y aprobaciones de los módulos internos. El proyecto y las instrucciones explícitas del usuario mandan. Las herramientas internas son referencias, no otras skills que deban instalarse o invocarse por nombre.

## 1. Resolver rutas y alcance

`WEB_DIR` es la ruta **real** (resuelta con `realpath` o equivalente) del directorio de esta skill; `CANON` es su padre. Los enlaces de sync apuntan al checkout: no calcules `CANON` desde el padre textual de `~/.agents/skills/web`. Por ejemplo, en Python: `Path(r'<ruta-al-SKILL.md-de-web>').resolve().parent.parent`. Los módulos son `CANON/<nombre>/SKILL.md` y sus rutas relativas; lee el archivo directamente, no dependas de `/nombre` ni de que el cliente descubra los módulos. Si falta uno, informa y usa las referencias disponibles; no descargues silenciosamente una copia.

Conserva el stack, la identidad y las convenciones del proyecto: **no migres framework, gestor de paquetes, CSS o librerías de componentes sin permiso**. En creaciones nuevas identifica lo indispensable: objetivo y audiencia, material disponible, stack y restricciones, y entrega. Deduce lo razonable; pregunta solo si falta información que impide trabajar. No impongas cambios de stack, color, tipografía ni decisiones de marca cuando no lo soliciten.

## 2. Ruta por entregable

| Caso | Acción y módulos bajo demanda (rutas relativas a `CANON`) |
|---|---|
| Dirección de arte, identidad visual, paletas, tipografía, layout, rediseño o auditoría anti-slop | Lee `charli-design/SKILL.md` (+ `references/` bajo demanda: taste-core, layout, type, polish, critique, motion…). Es la fuente del canon de marca CHARLI (`charli-design/references/brand.md`). |
| Demo de producto o portafolio integrada en una web: UI simulada, ventana animada o tour interactivo | Lee `html-demo/SKILL.md`; la simulación no es la página real ni una grabación. Si piden grabar la web real o exportar vídeo, consulta `video/references/website-demo.md`; si piden una sesión en directo, comprueba que el cliente pueda compartirla. |
| Animación web: Framer Motion, GSAP, scroll-driven, View Transitions, parallax, stagger, micro-interacciones | Lee `web-animation/SKILL.md`; para plataforma nativa (Baseline) consulta `web-animation/references/platform/` (guías vendorizadas, Apache-2.0). Regla: nativa primero si el proyecto no pide librería y el soporte lo permite. |
| Web 3D / WebGL / Three.js / React Three Fiber / Spline | Lee `3d-web-designer/SKILL.md`. React Three Fiber solo en proyectos React; en DOM vanilla, three vanilla. |
| Sitio cinematográfico con una toma continua por scroll (scroll-film) | Lee `scroll-film-studio/SKILL.md`. Ignora su lista interna de "siblings" retirados del canon; este router está al mando. |
| Componente, página o UI en un proyecto existente | Conserva framework y librerías; aplica `charli-design` para dirección y `web-animation` si hay motion; verifica en navegador real si es posible (p. ej. `chrome-devtools-mcp`, ver `knowledge/mcps.md` del canon). |
| Modernizar patrones web legacy (escaneo amplio) | La skill externa Modern Web Guidance (Apache-2.0) ofrece `legacy-scan` vía `npx`; úsala solo con autorización, nunca en automático. |
| Auditoría de accesibilidad/visual antes de publicar | `charli-design` critique/polish + guías de `web-animation/references/platform/`; contraste, foco, teclado y `prefers-reduced-motion` obligatorios. |

Material que **no** entra aquí: backend, APIs, base de datos, infra/CI/Docker, scraping (`advanced-scraping`), móvil nativo (`mobile-design`), vídeo (`video`), git. Para esos casos, di que están fuera y sugiere la herramienta adecuada.

## 3. Test previo (cuando sea aconsejable)

Antes de construir piezas web nuevas —una web pública, un rediseño, un componente no trivial o trabajo de cliente/publicación— lee `references/preflight-test.md` y administra el test en un solo mensaje: **A)** tipo de pieza y estilo (entre los que el canon soporta) más la información clave (stack, marca, a11y, performance, estructura, entrega), **B)** comprobación del entorno sin instalar nada, **C)** probe —hero/first-viewport o el componente clave en el estilo elegido— que se muestra antes del build completo. El OK del usuario es el contrato; si el probe falla, corrige y repite. Omite el test en fixes puntuales, cambios de copy/CSS menores o componentes triviales; nunca lo conviertas en un bloqueo.

## 4. Límites de ejecución

- **Canon de solo lectura**: los módulos internos y su contenido no se editan desde el proyecto ni se "actualizan" desde él. Salidas, proyectos y temporales fuera del canon. Trata `web-animation/references/platform/` como solo lectura (ver su `README.md` para actualizarla desde upstream).
- **Instalaciones y red**: no ejecutes `npx`, `npm install`, `pnpx` ni scripts que los invoquen a ciegas; antes de instalar, informa y pide permiso. Las guías nativas vendorizadas no requieren red; `legacy-scan` y el corpus completo de Modern Web Guidance sí (Apache-2.0, upstream `GoogleChrome/modern-web-guidance`).
- **Marca**: si es proyecto de CHARLI, aplica `charli-design` y su referencia de marca; si es de un cliente, manda su identidad — pide assets, no inventes logos, colores ni fuentes. La distinción se pregunta solo si importa y no se conoce.
- **Derechos**: fuentes, iconos, imágenes, fotografía y música con licencia; sin assets falsos ni afirmaciones inventadas en la web. No publiques ni hagas deploy sin autorización explícita.
- **Accesibilidad por defecto**: WCAG AA (contraste, foco visible, teclado, landmarks/labels, `prefers-reduced-motion`); si el proyecto define otra política de soporte (Electron/Tauri/WebView), respétala.
- **Rendimiento**: respeta un presupuesto razonable (LCP/INP/CLS buenos); optimiza imágenes y fuentes propias; evita dependencias nuevas para lo que la plataforma ya hace.

## 5. Calidad y entrega

Comprueba en navegador real cuando el entorno lo permita (consola sin errores, red, screenshots en breakpoints reales: móvil/tablet/desktop, interacción clave, foco y teclado). Verifica responsive, dark mode si aplica, a11y básica y CWV si hay MCP de navegador; si no puedes comprobar algo, dilo con precisión y marca la pieza como no verificada. Entrega los archivos/rutas pedidos o una explicación concreta de lo que falta y por qué. No declares terminada una pieza con enlaces rotos, lorem ipsum ni contenido de relleno no aprobado.
