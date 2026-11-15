# Test previo a producir (cuando sea aconsejable)

Un test es un gate barato antes del gasto grande: se hace cuando aporta y se
salta cuando no. No es un requisito universal ni un trámite.

## Cuándo es aconsejable

- Piezas nuevas (>20 s), promos/anuncios para publicación o cliente.
- Cualquier pieza con música rítmica o cortes al beat (junto con `beat-sync.md`).
- Dirección de arte estilizada o poco definida; dudas de material, marca o derechos.
- El usuario pide explícitamente un test o un vistazo previo.

## Cuándo se omite

- Recortes puntuales, fixes, ajustes de color/audio, re-exportar.
- Análisis sin edición (ruta `analizar-videos`).
- Cambios mínimos en proyectos existentes conservando stack y estilo.
- Iteración sobre un probe ya aprobado en esta misma sesión.

Si dudas, haz el test; nunca pidas permiso para un test ligero.

## Formato del test

Un solo mensaje con las partes necesarias. Numera las preguntas y permite
responder en corto (`1a, 2 premium, 5: lo que comparta`). Deduce lo que el
proyecto o el encargo ya respondan y **no lo preguntes**. Ofrece por defecto
razonable lo que falte ("si no dices FPS, usaré 30"). Objetivo: información
suficiente para no iterar a ciegas, no un interrogatorio. Guarda las respuestas
en `brief.md` dentro de la carpeta del proyecto para trazabilidad.

## A. Test de tipo y estilo de vídeo

### A1. ¿Qué quieres hacer? (elige una o más)

| # | Tipo de pieza | Motor/ruta en el canon |
|---|---------------|--------------------------|
| a | Motion explainer / gráfico animado (una idea por escena) | HyperFrames HTML + `hyperframes-*` |
| b | Promo de producto o app (capturas reales, "brag") | Ruta motion; `brag/SKILL.md` como inspiración |
| c | Reel vertical / clip social (9:16, gancho ≤2 s) | Edición o motion según material |
| d | Película estilizada con arte dirigido ("en el estilo X") | HyperFrames o externo `lemo-opuscar.md` (solo con autorización) |
| e | Edición de metraje existente (entrevista, doc, montaje) | `editing.md` + FFmpeg |
| f | Motion 3D / WebGL | HyperFrames adapter `three` (nota en `motion.md`) |
| g | Pieza musical / al beat | Motion o edición + `beat-sync.md` |
| h | Tarjetas estáticas, loops o montaje libre | `general-video/SKILL.md` |
| i | Otro (describe) | El router decide |

El agente mapea la elección a la ruta del router y avisa si cambia el plan
(p. ej. d o g suelen depender de autorización/herramientas).

### A2. Estilos de animación disponibles en el canon

Títulos cinéticos y kinetic type · motion 2D vectorial (HTML/CSS/GSAP/Lottie
vía HyperFrames) · product UI/screencast walkthrough · infografía y diagramas
animados · motion 3D in-browser · canvas procedimental (SVG local) · looks
retro/analog (vía `media-use`, con licencias) · edición cinematográfica de
metraje (cortes, ritmo, color, LUTs). Fuera del canon, los cortometrajes por
estilo artístico de Lemo-Opuscar son opcionales y autorizados caso por caso.
**Pregunta cuál de estos siente el usuario, o pide 1–3 referencias (links/vídeos).**

### A3. Sensación y energía (elige una o dos)

Minimal/premium · corporativo limpio · playful/bold · cinemático ·
energético/hype (al beat) · elegante/lujo · retro/analog · documental ·
técnico/riguroso (data) · íntimo/acústico · otra.

### A4. Objetivo y audiencia

Qué debe lograr la pieza (informar, lanzar, vender, reclutar, emocionar…) y a
quién va dirigida. Una frase basta.

### A5. Plataforma y formato

Orientación (16:9 / 9:16 / 1:1 / 4:5) · plataforma (YouTube, TikTok/Reels,
LinkedIn, web, evento/TV) · duración objetivo · FPS (24/30/60; default 30 para
motion, 24 para cine) · entrega (MP4 H.264, WebM, otro) · loudness (default
−14 LUFS si hay audio).

### A6. Material y derechos

¿Hay footage, fotos, logo, voz, música o datos propios? ¿Qué puedes usar y qué
no? Material ajeno exige permiso y licencia; no asumas derechos. Si hay que
conseguir música/SFX, di si habrá presupuesto (ver `sfx-sourcing.md`).

### A7. Marca y estilo visual

Colores y tipografía de marca · logo y variantes · tono de voz · referencias
que le gustan y las que no · qué evitar (p. ej. "nada corporativo", "nada de
gradientes morado-azul"). Si hay proyecto web/branding disponible, léelo.

### A8. Audio

Voz: ninguna / TTS / grabación propia / locutor externo. · Música: ninguna /
alguna concreta (nombre) / elegir / al beat (`beat-sync.md` o `hyperframes
beats`). · SFX: sí/no/cuántos. · Captions: idioma y estilo; ¿quemados o `.srt`?

### A9. Estructura deseada

¿Gancho en los primeros 2 s? · arco apertura–desarrollo–cierre · ¿escenas
obligatorias o mensajes que deben quedar? · ¿número aproximado de escenas? ·
¿un CTA final y cuál?

### A10. Puertas de aprobación

¿Quieres storyboard rápido antes del build? · ¿probe de 2–3 s antes del render
completo (ver parte C)? · ¿revisar fotogramas intermedios o solo aprobado
final? · plazo de entrega.

## B. Test del entorno (silencioso, sin instalar nada)

Comprueba y reporta en pocas líneas: `ffmpeg`/`ffprobe` y versiones; `node`;
`python3`/`uv`; fuentes para subtítulos (`fc-list` si existe); espacio en
disco; herramientas del proyecto existente. Lo que falte degrada el plan (sin
FFmpeg, los renders se declaran no verificados); **no instales ni actualices
nada sin autorización**.

## C. Test de render (probe)

Genera el menor artefacto que pruebe las decisiones de riesgo y enséñaselo
antes de la pieza completa, ajustado al tipo elegido en A1:

- a/b/f/h: 2–3 s de la escena más exigente, o 3–5 fotogramas clave/contact
  sheet en el estilo real.
- c/e: 10–15 s del tramo más denso de cortes, o fotogramas alrededor de cada
  transición crítica; incluye el encuadre vertical/horizontal final.
- d: un styleframe en el estilo elegido (si depende de Lemo-Opuscar, con
  autorización).
- g: la rejilla validada y un fragmento corte-al-beat con música.

Criterios de aprobado: legibilidad (tipografía, contraste, safe areas),
paleta/marca, ritmo, sincronía A/V, sin artefactos (banding, flicker,
clipping), duración y formato dentro de lo pedido. Si el probe falla en algo
bloqueante, corrige y repite; si pasa, el OK del usuario es el contrato para la
pieza completa. Declara tiempo y coste del probe; piezas largas pueden tener un
segundo probe tras ajustes.

El test previo es por proyecto y no sustituye la evaluación A/B de la skill
(`knowledge/video-evaluation.md`), que es por versión del harnés.
