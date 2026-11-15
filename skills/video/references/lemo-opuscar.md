# Dirección de arte estilizada — Lemo-Opuscar (externo, opcional)

Puntero a un recurso externo; **no hay ni habrá contenido suyo copiado en este
canon**. Úsalo solo con autorización explícita del usuario y caso por caso; el
predeterminado de la skill sigue siendo HyperFrames.

Qué es: librería de 100 estilos cinematográficos (`STYLE.md`: Neon Tubes,
Ukiyo-e, Swiss Motion, Chalkboard…) más `DIRECTOR.md` (metodología de dirección:
sonido → ritmo → cámara → actuación) y `TECHNIQUE.md` (canvas/WebGL renderizado
frame a frame, TTS, score desde bibliotecas libres, mezcla a −14 LUFS). Cada
película la "dirige, dibuja, puntúa y mezcla" el agente escribiendo código; no
genera vídeo generativo ni stock.

Coste real: ~30–60 min y muchos tokens por película; Node 20+, ffmpeg **7+**
(Ubuntu 24.04 trae 6.1: no vale), Python 3.11+ (o uv), `playwright-core`; tres
estilos piden un generador de imágenes externo. Pensada para Claude con
esfuerzo alto. Por defecto 1920×1080 @ 24 fps (algunos estilos fijan 30/60).

Licencia (lo que permite y lo que no):

- Código: MIT. Films y pósters: CC BY 4.0.
- Docs (los `STYLE.md`, guías): **CC BY-NC 4.0** + permiso adicional limitado a
  *hacer* tus películas (staff y cliente incluidos; puedes readaptar para tu
  pieza y quedártelas en sus project files). **No** autoriza incrustar las
  docs adaptadas en un producto/servicio ni redistribuirlas a terceros.
- Incrustar estilos en este canon exigiría licencia comercial:
  lemomo.studio@gmail.com. No asumas que existe.

Cuándo encaja: cortos con identidad de arte fuerte (festival/social, promos de
marca, piezas artísticas) cuando el usuario quiere "una película EN ese estilo",
en la línea de "Make a 45-second film in the watercolor style about…".

Cuándo no: edición de metraje; entregas rápidas; publicidad genérica donde
HyperFrames + `general-video` es suficiente; material con derechos dudosos.

Cómo usarlo (si el usuario lo autoriza): por su propio canal, nunca por copia
del canon — `claude plugin marketplace add lemomo-ai/lemo-opuscar` y
`claude plugin install lemo-opuscar@lemolab`, o clone del repo y su flujo
documentado; las salidas van fuera del canon. Tras usarlo, verifica el
resultado con `quality.md` como cualquier otra pieza; no asumas que "está
probado" por venir del upstream.

Alternativa interna: la dirección de arte general (motion.md) y los estilos de
`web` (módulo `design/`, fuente `charli-design`) cubren muchos briefs sin salir
del canon.
