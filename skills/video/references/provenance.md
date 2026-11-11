# Procedencia y alcance de la integración

Integración propia de principios generales, no copias de repositorios enteros ni instalación de skills externas. Las versiones inspeccionadas son:

- Bang Motion, `bangtutorial/bang-motion` @ `c1aa65e921c970d858705fcb4a53a8294d1a4131`, MIT, `../licenses/bang-motion-MIT.txt`. Influencia: continuidad, cámara, motion y revisión por fotogramas. No se incluyen starters ni exportadores.
- Huashu Design, `alchaincyf/huashu-design` @ `e8d1148a80d5a281d4247cffe320add3df017928`, MIT, `../licenses/huashu-design-MIT.txt`. Influencia: storyboard, lenguaje de cámara y revisión. No se incluyen assets, audio, stickers, marca de agua, integraciones cloud ni reglas de aprobación. Algunos stickers upstream tienen PolyForm Shield, no MIT; verificar derechos de cada asset antes de usarlo.
- Claude Drawing, `cloveric/claude-drawing-skill` @ `6af36dc717b63d6ddafb54d2eaa120cacd99ab4d`, MIT, `../licenses/claude-drawing-MIT.txt`. Influencia: generación local de gráficos y progresiones; la herramienta SVG es una implementación propia reducida, no copia de sus estilos o módulos. No se incluye el paquete, ni Pillow/NumPy, ni sus ejemplos.

Los repositorios fueron revisados estáticamente de forma parcial, no auditados ni probados visualmente de extremo a extremo. Ningún servicio, dependencia o audio de ellos queda instalado por esta integración.
