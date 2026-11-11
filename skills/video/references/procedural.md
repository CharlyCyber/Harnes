# Dibujos procedimentales locales

Para un recurso gráfico sencillo que se dibuja progresivamente, `video/scripts/draw_on.py` genera SVG transparentes deterministas a partir de trazos definidos por el agente o usuario. No incluye los estilos de Claude Drawing ni genera automáticamente ilustraciones complejas. No necesita Pillow, NumPy, red ni credenciales. No ejecutar desde el canon como directorio de salida.

Ejemplo de entrada `strokes.json` en el proyecto (coordenadas de 0 a 1):

```json
{"width": 1080, "height": 1920, "strokes": [
  {"color": "#ffffff", "width": 8, "points": [[0.2, 0.5], [0.5, 0.3], [0.8, 0.5]]},
  {"color": "#ffcc00", "width": 5, "points": [[0.3, 0.6], [0.7, 0.6]]}
]}
```

```sh
python "<VIDEO_DIR>/scripts/draw_on.py" strokes.json ./draw-frames --frames 60 --fps 30
```

El destino debe ser nuevo; se producen `frame_0000.svg` en adelante y un `manifest.json` con FPS y duración. El primer frame está vacío y el último contiene todos los trazos. Importa los frames con duración de `1/fps` cada uno en el editor o conviértelos con una herramienta disponible; el script no crea GIF ni MP4. Comprueba compatibilidad SVG, alpha, sincronización y rendimiento en el flujo real antes de usarlo. Si necesitas otro estilo, decide si conviene una ilustración manual o evaluar Claude Drawing por separado, con sus dependencias y licencia.
