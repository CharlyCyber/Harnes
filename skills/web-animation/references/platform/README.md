# Platform guides (vendorizadas, selectivas)

Subconjunto offline de **Modern Web Guidance** de Google Chrome — solo las
guías de motion/scroll/transitions que complementan a Framer Motion y GSAP en
este módulo. Los textos están **sin modificar** respecto al upstream.

- Fuente: `GoogleChrome/modern-web-guidance` @ `64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65` (v1.0.1, 2026-11-22), corpus en npm `modern-web-guidance@1.0.1`. Dos de las 16 guías seleccionadas se actualizaron verbatim desde ese commit.
- Licencia: **Apache-2.0** (ver `LICENSE-modern-web-guidance.txt`). © The Chromium Authors / Google.
- Vía canónica completa (fuera de este canon): `npx -y modern-web-guidance@latest search "<query>" --skill-version 2026_11_09-5bcc021b` + `retrieve <id>`; solo con autorización y red; para modernizar patrones legacy, su `legacy-scan` (≈20 % del corpus).

## Qué está vendorizado y por qué

Motion con la plataforma nativa (Baseline): scroll-driven animations
(`scroll-entry-exit-effects`), scrollytelling, parallax, scroll-snap, scroll
indicators/progress, sticky headers, scrollspy, tamaños intrínsecos animables y
propiedades individuales de transform; y View Transitions same/cross-document
y directional navigation. Son patrones que Framer Motion/GSAP resuelven con
librería pero que el Baseline ofrece sin dependencia; la skill `web-animation`
prefiere nativo cuando el proyecto no pide una librería concreta y el soporte
del objetivo del proyecto lo permite.

## Qué NO está (y cómo consultarlo)

El resto del corpus: accesibilidad completa (`accessibility/`), CSS general
(`css.md`), forms, HTML/Web Components, performance/CWV, security/passkeys,
privacy, PWA, UX, visual-design, built-in-AI, wasm, webmcp, chrome-extensions.
Para esos casos: consulta el upstream con `retrieve` (con autorización) o pide
al usuario que decida instalarlo como plugin externo; no lo repliques a mano
desde memoria.

## Política de soporte y fallbacks

Las guías asumen Baseline Widely available por defecto; para features no
Widely available, sigue los fallbacks que la propia guía indique, salvo que el
proyecto declare otra política de soporte (documéntala en su AGENTS.md/CLAUDE.md;
p. ej. "Allow Newly Available features with graceful degradation"). Si el
proyecto tiene Electron/Tauri/WebView restringido, pide la política antes de
elegir patrones.

## Actualización

Sube de versión copiando de nuevo las mismas rutas desde un commit/tag
posterior y actualiza el SHA en este fichero y en `skills/web/references/provenance.md`
y `skills/REGISTRO.md`. No edites los textos in situ; si una guía queda
obsoleta, sustitúyela entera.
