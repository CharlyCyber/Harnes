# Procedencia y alcance de la integración

Integración propia de principios generales, no copias de repositorios enteros ni instalación de skills externas. Las versiones inspeccionadas son:

- Bang Motion, `bangtutorial/bang-motion` @ `c1aa65e921c970d858705fcb4a53a8294d1a4131`, MIT, `../licenses/bang-motion-MIT.txt`. Influencia: continuidad, cámara, motion y revisión por fotogramas. No se incluyen starters ni exportadores.
- Huashu Design, `alchaincyf/huashu-design` @ `e8d1148a80d5a281d4247cffe320add3df017928`, MIT, `../licenses/huashu-design-MIT.txt`. Influencia: storyboard, lenguaje de cámara y revisión. No se incluyen assets, audio, stickers, marca de agua, integraciones cloud ni reglas de aprobación. Algunos stickers upstream tienen PolyForm Shield, no MIT; verificar derechos de cada asset antes de usarlo.
- Claude Drawing, `cloveric/claude-drawing-skill` @ `6af36dc717b63d6ddafb54d2eaa120cacd99ab4d`, MIT, `../licenses/claude-drawing-MIT.txt`. Influencia: generación local de gráficos y progresiones; la herramienta SVG es una implementación propia reducida, no copia de sus estilos o módulos. No se incluye el paquete, ni Pillow/NumPy, ni sus ejemplos.

Repositorios externos evaluados el 2026-11-15 (inspección estática, sin instalación):

- video-shotcraft, `Vincentwei1021/video-shotcraft` @ `6700db2ba80572ebc777b99d72049679fed9840c` (2026-11-12, Apache-2.0), `references/music-beat-sync.md`. Influencia: método de rejilla de beat por mínimos cuadrados, clasificación kick/snare/hihat, anclaje de cuts, verificación post-render; adaptación propia en español y compactada en `references/beat-sync.md`. No se incorpora su pipeline Remotion, sus 124 tarjetas de shots (derivadas de vídeos ajenos sin licencia explícita), su `sfx-source.py` (solo documentado como herramienta externa en `references/sfx-sourcing.md`) ni assets.
- Lemo-Opuscar, `lemomo-ai/lemo-opuscar` @ `3a7132b996be0241c1ea0ab180d519f06e6f10b6` (2026-11-12; código MIT, docs CC BY-NC 4.0, films CC BY 4.0). Influencia: ninguna directa; solo un puntero externo en `references/lemo-opuscar.md`. No se copia ni adapta ninguna doc (STYLE.md, DIRECTOR.md, TECHNIQUE.md) dentro del canon; haría falta licencia comercial expresa.
- three.js, `mrdoob/three.js` @ `6281ce3fd4c3e8c4b4b204dd5a942f77ab313f6f` (v0.187.0, MIT). Ya se usa vía adapter HyperFrames (`hyperframes-animation/adapters/three.md`, pineado a 0.181.2 por CDN); solo se añade nota sobre pin local en `references/motion.md`. No se vendoriza.
- React Three Fiber, `pmndrs/react-three-fiber` @ `d74622ea8ed717f7212d7e19d65ff3e325508389` (MIT). Optado fuera: solo aplica a proyectos Remotion; en HyperFrames la escena se porta a three vanilla (nota en `references/motion.md`). No se vendoriza.
- librosa, `librosa/librosa` @ `76f10b8d2d00870fed47b4698927a4e7e78d1fb4` (ISC). Ya es dependencia opcional del canon (`brag/scripts/analyze_music_cues.py`, pin >=0.10.2); ningún cambio de dependencias. La metodología de análisis vive en `references/beat-sync.md`.

Los repositorios fueron revisados estáticamente de forma parcial, no auditados ni probados visualmente de extremo a extremo. Ningún servicio, dependencia o audio de ellos queda instalado por esta integración.
