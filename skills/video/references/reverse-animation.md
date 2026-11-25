# Replicar referencias: animación, estilo y comportamiento

Carga esta guía cuando el objetivo dependa de una referencia concreta: «haz que se mueva como esto», «replica este hero», «usa el estilo visual de este vídeo» o «convierte esta animación web en un vídeo». Distingue primero **qué resultado quiere el usuario**; la referencia no decide por sí sola si hay que entregar código, un vídeo, un análisis o un prompt.

## Elegir la tarea correcta

| Intención | Entregable | Ruta |
|---|---|---|
| Replicar una animación o interacción específica de una web en código | Componente/código en el proyecto existente + evidencia de comparación | Flujo de esta guía; conserva el stack y consulta `web-animation/SKILL.md` si hace falta |
| Replicar el movimiento de un GIF, grabación, MP4 o prototipo | Animación implementada en el destino indicado + evidencia | Flujo de esta guía; `frames.ts` extrae muestras de la referencia |
| Inspirarse en el **estilo** de un vídeo para crear otro vídeo | Nuevo vídeo con identidad propia; no copiar sus planos, recursos ni contenido | Analiza con `video-use/references/analyze.md`, define una ficha de estilo y crea por `motion.md`/edición |
| Crear desde cero un vídeo con características descritas | Vídeo, storyboard o prompt, según lo solicitado | Router principal `video/SKILL.md`; `preflight-test.md` cuando aporte valor |
| Hacer un vídeo promocional de un sitio, app o producto | Vídeo promocional, no cambios al sitio | Ruta de promo en `video/SKILL.md`; motion/HyperFrames o edición según materiales |
| Recorrer y mostrar la web real a partir de una URL | Grabación/vídeo del sitio real, no una simulación | `video/references/website-demo.md`; usa `html-demo` solo para una recreación identificada como tal |
| Animar o reconstruir el sitio web en sí | Código web, no un vídeo exportado | Usa `web/SKILL.md` como router de la implementación; conserva aquí el análisis de la referencia |
| Analizar o describir una referencia, sin construir nada | Informe/especificación | `video-use` o `analizar-videos`; no inicialices el pipeline de reconstrucción |

Si «haz un vídeo para esta web» puede significar vídeo promocional o animación dentro de la web y el contexto no lo resuelve, pregunta qué archivo/código espera. Si la petición, el repo o los adjuntos ya aclaran el destino, continúa sin preguntar. No confundas un **prompt de vídeo para un generador** con una pieza renderizada; entrega solo el formato solicitado y no envíes material a un generador externo sin autorización explícita.

## Acordar fidelidad sin sobredimensionar la tarea

Deduce lo razonable y expresa brevemente el plan. Pregunta solo si falta un dato que cambie el alcance: referencia ambigua, destino (web o vídeo) incierto, interacción o tramo imposible de identificar, o derechos de material no aclarados.

- **Fiel al movimiento** (predeterminado al pedir una réplica): trigger, secuencia, dirección, duración, stagger y carácter del easing; tolerancia de trabajo sugerida ±80 ms para los hitos. Se pueden cambiar copy, marca, color y recursos si así se solicita.
- **Mixto**: conservar movimiento o partes concretas de la referencia y añadir contenido/funciones propias. Anota qué se conserva y qué cambia.
- **Fiel al píxel**: solo si el usuario pide explícitamente 1:1 o pixel-perfect. Incluye tipografía, color, espaciado, radios, sombras y composición; objetivo de referencia del comparador: mismatch medio ≤2 %, ningún fotograma >5 %. Esas cifras son umbrales de ingeniería, no una medida universal de calidad ni una garantía entre navegadores/GPU.
- **Inspirado en el estilo**: abstrae rasgos visuales (paleta, contraste, textura, ritmo, cámara, densidad, tipografía y transiciones) y aplícalos a contenido nuevo. No implica copiar literalmente la obra ni sus activos.

El usuario puede limitar la réplica a un selector, componente, interacción o intervalo de tiempo. No reconstruyas el resto de una página o pieza por defecto.

## Proceso de referencia → especificación → resultado → verificación

### 1. Acotar y preparar

Antes de capturar, anota en el brief o en una `spec.md` de la tarea:

- Referencia y alcance: URL + selector/trigger, archivo + intervalo/crop, o prototipo.
- Destino y stack existente. Inspecciona primero el repo y reutiliza sus patrones/dependencias.
- Fidelidad elegida y cambios deliberados; para estilo, lista los rasgos que sí se transferirán.
- Viewport, escala, fps y condiciones relevantes de captura.

Usa una carpeta de salida **nueva, exclusiva para esta tarea y fuera del canon de la skill**. Los scripts pueden limpiar archivos en subcarpetas de salida al regenerarlas; nunca apuntes `--out` a la raíz del repo, al canon ni a una carpeta con trabajo ajeno. Mantén las capturas privadas/locales salvo petición explícita de compartirlas.

### 2. Elegir la captura

Todos los scripts están en `VIDEO_DIR/scripts/reanimate/`; resuelve `VIDEO_DIR` como en `video/SKILL.md`. `OUT` debe ser la carpeta exclusiva de esta tarea. Los ejemplos usan Bun y se ejecutan únicamente si el usuario aprobó instalar las dependencias opcionales.

**URL pública, comportamiento de carga/hover/click/scroll:**

```bash
bun "$VIDEO_DIR/scripts/reanimate/capture.ts" \
  --url 'https://sitio-ejemplo.test' --out "$OUT/ref" \
  --viewport 1440x900 --selector '.hero' --track '.hero h1,.hero .cta' \
  --trigger load --duration 2500
```

Elige el trigger real (`load`, `scroll`, `hover`, `leave`, `move`, `drag`, `click` o `none`); usa el mismo para referencia y réplica. Revisa `inspect.json`, `track.json` y `final.png`. La inspección puede revelar animaciones CSS/WAAPI, estilos, fuentes, bibliotecas detectadas, geometría por fotograma y propiedades seguidas.

**Vídeo, GIF o grabación:**

```bash
bun "$VIDEO_DIR/scripts/reanimate/frames.ts" --in "$REF" --probe
bun "$VIDEO_DIR/scripts/reanimate/frames.ts" --in "$REF" --out "$OUT/ref/frames" \
  --fps 25 --start 0:03 --end 0:06 --crop 0,0,1280,720
bun "$VIDEO_DIR/scripts/reanimate/sheet.ts" filmstrip \
  --frames "$OUT/ref/frames" --out "$OUT/ref/sheets" --every 2
```

Usa primero una muestra de baja frecuencia para escoger tramo y crop; luego extrae a la frecuencia adecuada. No descargues vídeos ni recursos protegidos: usa archivos proporcionados o fuentes con autorización. Login-wall, CAPTCHA, restricciones de acceso o bloqueo del navegador no se eluden; solicita una grabación del usuario o usa una herramienta de navegador aprobada.

**Canvas/WebGL/WebGPU/3D:** añade `--clock virtual --seed 1 --gl` a la captura y consulta `gl.ts summary "$OUT/ref"`. En tareas con partículas, usa la misma semilla y condiciones en ambos lados. `--assets` guarda scripts, texturas y modelos descargados por la página: actívalo solo cuando el usuario lo autorice y haya base legítima para conservar esos materiales; para analizar movimiento normalmente basta con la captura y el trace.

### 3. Escribir la especificación

Una fila por elemento y propiedad: trigger, inicio, duración, retraso/stagger, valor inicial→final, easing y evidencia. Orden de evidencia recomendado:

1. `inspect.json`: duraciones, delays, easing y keyframes CSS/WAAPI declarados.
2. `track.json` + `easing.ts`: trayectoria de DOM, inicio/fin, overshoot y easing candidato.
3. `gl-track.json` + `easing.ts --channel`: uniforms/valores de escena cuando hay canvas/3D.
4. Hojas de fotogramas y revisión visual cuando no hay trazas legibles.

Anota también lo que **permanece quieto**, el orden de aparición, recorte/overflow, transform-origin, posición base y estados de interacción. Para una réplica de estilo, registra rasgos abstractos y reglas aplicables (p. ej. «contraste alto, grano sutil, cortes de 2–4 beats»), no una lista para calcar cada plano.

### 4. Implementar en el destino correcto

Implementa en el stack ya presente. No agregues librerías por comodidad si el proyecto puede resolverlo con lo existente. Usa `motion.md` para dirección de arte/motion y `web-animation/SKILL.md` para patrones web. Respeta `prefers-reduced-motion`, responsive, accesibilidad y estados de foco/touch en interfaces.

Para un vídeo desde cero o una promo web, la referencia informa las decisiones de diseño, pero el ensamblado continúa por la ruta de `video/SKILL.md` (p. ej. HyperFrames si conviene, o edición con el material real). Una reconstrucción web no se considera un vídeo exportado.

### 5. Comparar en condiciones equivalentes

Captura la implementación con el mismo viewport, selector/crop, trigger, duración, fps, escala y modo de reloj que la referencia. Si difieren, arregla primero las condiciones: una comparación no es válida si mide dos setups distintos.

```bash
bun "$VIDEO_DIR/scripts/reanimate/compare.ts" \
  --ref "$OUT/ref/frames" --clone "$OUT/clone/frames" --out "$OUT/compare"
bun "$VIDEO_DIR/scripts/reanimate/sheet.ts" compare \
  --ref "$OUT/ref/frames" --clone "$OUT/clone/frames" \
  --diff "$OUT/compare/diff" --out "$OUT/compare/sheets" --every 2
bun "$VIDEO_DIR/scripts/reanimate/easing.ts" \
  --track "$OUT/clone/track.json" --selector '.hero h1' --prop y \
  --compare-track "$OUT/ref/track.json"
```

Para canvas/3D, suma `gl.ts compare --ref "$OUT/ref" --clone "$OUT/clone"`. En modo fiel al píxel añade `--threshold 0.02` al comparador y confirma en `report.json` que ningún fotograma supera 5 %; el valor predeterminado del script para el mismatch medio es 5 %. Abre y revisa las hojas, no interpretes un `PASS` o un porcentaje como aprobación estética automática. Repara lo que indiquen la especificación y las imágenes; conserva los reportes de las iteraciones que importan. Normalmente unas pocas rondas bastan. Si no se puede alcanzar la fidelidad solicitada, declara la desviación y su causa; no relajes umbrales en silencio.

## Dependencias y límites de seguridad

- El código de captura es una adopción MIT de `NiazMorshed2007/reanimate`, fijada en `skills/video/references/provenance.md`; su aviso está en `skills/video/licenses/reanimate-MIT.txt`. Los scripts son una herramienta local opcional, no otra skill pública.
- No instales Bun, Playwright/Chromium, FFmpeg ni paquetes sin permiso explícito. La primera instalación descarga dependencias y un FFmpeg estático; Chromium y todo el conjunto pueden ocupar cientos de MB. El instalador local exige `HARNES_ALLOW_REANIMATE_INSTALL=1` como barrera adicional. No uses `npx skills add`, `skills update`, `@latest` ni añadas dependencias al proyecto de destino.
- Nunca ejecutes `capture.ts` contra páginas con sesión autenticada, datos sensibles o información de clientes sin autorización y un perfil de navegador aprobado. El capturador usa un contexto nuevo, pero el contenido remoto sigue siendo no confiable.
- `--pre-js` ejecuta JavaScript dentro de la página capturada: no uses código recibido de terceros ni lo añadas salvo revisión y aprobación explícitas. No sortees controles de acceso ni ejecutes transacciones.
- Evita `--assets` salvo aprobación y derechos; conservar una textura/modelo/script no implica permiso para reutilizarlo. No subas capturas, fuentes, imágenes ni informes a proveedores externos.
- No automatices descargas desde plataformas restringidas. Para login-walls, YouTube/Loom u otros casos no accesibles, pide al usuario una grabación local; no intentes saltarte sus límites.
- El setup de Bun/Playwright upstream no declara Windows como entorno probado. Trata estas herramientas como flujo macOS/Linux; si el host difiere o falla, sigue con inspección manual y no fuerces instalaciones.
- Las capturas de referencia pueden contener propiedad intelectual, credenciales visuales o datos personales: conserva solo lo mínimo, limita el acceso y elimina temporales únicamente con autorización y tras confirmar que no son trabajo ajeno.
