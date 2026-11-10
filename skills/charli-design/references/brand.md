# Marca CHARLI AI — extraída del portafolio

Fuente única: `CharlyCyber/Charli-AI-Portfolio` (v1.44, `portafolio-charli.vercel.app`).
Toda declaración aquí abajo proviene del copy real, los tokens CSS o el código del sitio.
Fuente: `src/app/globals.css`, `src/app/layout.tsx`, `src/components/site/*`, `README.md`.
La carpeta `Proyectos\Charli AI Brand OS` NO es fuente (descartada por el operador 2026-10-30).

## Posicionamiento

- **Título declarado (layout.tsx):** "CHARLI AI — Tecnólogo Creativo en IA | Portafolio y Brief Comercial".
- **Propuesta (layout.tsx / hero):** "Experiencias digitales, sistemas creativos y automatizaciones potenciadas por inteligencia artificial" — "con la precisión de la ingeniería y el criterio del oficio".
- **Slides de perfil (about-horizontal):** AUTODIDACTA · PROMPTING · AGENTES · CÓDIGO · DISEÑO.
- **Enfoque diferencial (autodidact.tsx):** "No-Low-Code: trabajo directamente con código y construyo soluciones personalizadas — la IA acelera el flujo, pero el criterio técnico y la revisión de resultados siempre son humanos."
- **Tesis sobre IA (dark-statement.tsx):** "Integrarla ya no es una ventaja: es una necesidad obligatoria."
- **Servicios (services.tsx):** (1) Sistemas creativos con IA — conceptos visuales y dirección artística; (2) Automatización y agentes — bots, workflows, integración de APIs; (3) Experiencias web — landings, sitios, producto digital; (4) Investigación y redacción.
- **Tarifas (pricing.tsx):** USD $250/$400/$600 (Básica/Professional/Premium) y CUP 20.000/40.000/60.000. Copy: "Precios claros, sin sorpresas".
- **Contacto:** charlicharli984@gmail.com · +53 53463755 · propuesta en "menos de 24 horas" (cta.tsx).
- **Proyectos exhibidos (works.tsx):** Telegram Intelligence Bot (2025), AI Intelligence Agent / Ranking-IA (2026), Diseños Webs (2026). Todo con repos públicos en CharlyCyber.

## Identidad visual (valores exactos, no adjetivos)

- **Tokens de marca "Cosmos" (globals.css):**
  - `ink: #0f1011` (negro cálido), `ink-soft: #5c5f63` (texto secundario)
  - `paper: #ffffff`, `paper-dim: #f3f4f6`
  - `lime: #c8f24e` (acento único), `lime-deep: #9fd600`
  - Hero (liquid-hero CONFIG): fondo `#EBE9E5` (papel cálido), fg `#151514`.
- **Paleta funcional:** 2 caras contrastadas — secciones claras papel/ink y secciones oscuras #0f1011 (Threads interactivas, statement). El lime aparece SOLO como acento (enlaces, subrayados, iconos, chips): jamás como fondo masivo.
- **Tipografía (4 familias self-hosted, globals.css):**
  - `Switzer` 400–700 — sans principal (todo el cuerpo).
  - `Anton` — palabras gigantes display en versales (YEAR WORDS del carrusel, marquees).
  - `Instrument Serif` italic — énfasis editorial (palabras con interludio cursiva).
  - `Geist` variable — auxiliar.
- **Radios y puertas:** radius vía `--radius` (shadcn/Tailwind), dark mode por clase.
- **Lenguaje visual declarado (README):** inspirado en cosmos.studio. Referencias reimplementadas: Liquid Sculpture Hero (gughigug, MIT), scroll horizontal de Matt Perry/21st.dev, Skiper 17 (tarjetas apiladas), Skiper 19 (trazo con scroll), Obsidian UI (hover-img), React Bits (Threads, Lanyard, FlowingMenu, Squares), KokonotUI (trazo manuscrito).

## Motion (criterio firma)

- **El hero es una experiencia física:** escultura de partículas que se licúa bajo el cursor (WebGL2), con estela de fluido, remolino, intro y retorno elástico. Degradación controlada: `lowPower`, DPR cap, `reducedMotion` respetado, fallback si no hay WebGL2.
- **Scroll como narrador:** smooth scroll (Lenis), scroll horizontal anidado en "Quién soy", tarjetas sticky que encogen/rotan al avanzar (GSAP ScrollTrigger scrub 0.5), trazo manuscrito que se dibuja al bajar y retrocede al subir.
- **Microdetalle sistémico:** efecto scramble/decode en TODAS las letras pequeñas del sitio; flip letra a letra en letras grandes y botones.
- **Feedback físico en UI:** tarjeta elástica 3D (cuelga, se estira, regresa con física), menús que se expanden con marquee Anton, hilos que apartan al cursor + giroscopio en móvil.
- **Regla implícita:** cada sección tiene un efecto interactivo único; nunca dos vecinas comparten el mismo truco. Motion siempre funcional/reactivo, jamás decorativo sin interacción.

## Tono de voz (reglas extraídas del copy real)

1. **Español íntegro, incluido el UI técnico** (hints, botones, cookies): "Mueve el cursor sobre la forma", "Toca la forma".
2. **Directo y concreto, sin hype:** "Precios claros, sin sorpresas", "Te preparo... esta semana" — promesas con plazo y alcance.
3. **Tecnología explicada en beneficio, no en jerga:** "La IA acelera el flujo, pero el criterio técnico y la revisión de resultados siempre son humanos."
4. **Em-dash " — " como puntuación firma** (presente en todo el copy del sitio).
5. **Primera persona del estudio, segunda persona del cliente:** "Empieza tu proyecto con CHARLI", "Cuéntame tu idea".
6. **Afirmaciones rotundas permitidas si hay sustancia:** "ya no es una ventaja: es una necesidad obligatoria".

## Criterios de aceptación (gradable — rúbrica para futuros builds)

Un resultado de CHARLI AI está "aprobado" cuando:

1. **Paleta:** usa el sistema ink/paper + lime como único acento, o deriva coherente de él (fondo #0f1011 / #EBE9E5 / blanco). No introduce accents de color no canonizados.
2. **Tipografía:** una sans geométrica + una display condensada en versales para palabras gigantes; máximo 2–3 familias con roles claros. Jamás system-ui como identidad.
3. **Motion:** hay al menos un efecto interactivo físico (reacción a cursor/scroll/dispositivo) por página; respeta `prefers-reduced-motion` y tiene fallback sin WebGL.
4. **Layout:** ritmo editorial claro (hero full-viewport → secciones alternando claro/oscuro), jerarquía por tamaño extremo (words gigantes vs. texto pequeño preciso), no por decoración.
5. **Copy:** español, concreto, con beneficio medible; em-dash firma; sin verbos de hype vacío ("revolucionario", "game-changing").
6. **Rendimiento:** fuentes self-hosted con `font-display: swap`, degradación en dispositivos bajos, sin CLS en el hero (estándar ya alcanzado en v1.44).
7. **Cero slop:** nada de gradientes morados genéricos, ni emoji como bullets, ni placeholder lorem, ni layouts de plantilla Dribbble reconocibles.
