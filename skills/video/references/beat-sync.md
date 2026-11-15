# Cortes y motion al beat (música)

Para piezas cuya fuerza viene del ritmo —ads, promos, reels, promos de producto,
videoclips, motion explainers con BGM pautado— el ritmo se mide antes de diseñar,
no se siente sobre la marcha. Si el usuario no eligió música, decide con él; no
fuerces sincronía rítmica en piezas sin pulso.

**Regla de oro: la música primero.** Registra instantes en segundos flotantes t;
convierte a frames solo al entrar al motor (render). Redondear antes hace
bola de nieve el error en el pipeline.

## 1. Mide la rejilla

Con Python disponible, `librosa` + `scipy` vía `uv` (sin instalar nada global):

```sh
uv run --with librosa --with scipy --python 3.11 python analisis.py
```

```python
import numpy as np, librosa
y, sr = librosa.load("bgm.mp3", sr=None, mono=True)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, tightness=400, units="time")
# No confíes en el escalar tempo (desvía >2%); ajusta una recta a los beats:
i = np.arange(len(beats))
T, t0 = np.linalg.lstsq(np.vstack([i, np.ones_like(i)]).T, beats, rcond=None)[0]
bpm = 60.0 / T
print(f"BPM={bpm:.2f} t0={t0:.4f}s T={T:.5f}s residuo±{np.abs(beats-(t0+i*T)).max()*1000:.0f}ms")
```

Criterios de aceptación de la rejilla: residuo ≤ ±15 ms (batería machine-punched;
en música orgánica, menos estricto pero declarado); si hay tramo a otro tempo,
ajusta por segmentos (§4). Sin Python,
`npx hyperframes beats <proyecto> --json` da una rejilla simple con fuerza por
beat (suelo práctico, ≥ HyperFrames 0.6.99); `skills/brag/scripts/analyze_music_cues.py`
da el análisis rico (beats + strongCues) para cualquier pista.

**Ambigüedad 0.5x/1x/2x — obligatoria.** Prepara las tres rejillas y
quédate con la que cubra mejor los onsets reales de bombo; el `tempo` escalar
no la resuelve. En música con batería electrónica, los golpes fuertes casi
siempre caen en beats enteros.

**Mezclas densas (voz/bajo):** separa percusión antes de medir —
`librosa.effects.hpss(y)` y mide sobre el componente percusivo; si aún no es
limpio, Demucs (`uvx --from demucs demucs --two-stems=drums -n htdemucs bgm.mp3`)
y mide sobre `drums.wav`.

Archivos de análisis junto al proyecto: `beat_data.json` (bpm, t0, T, beats[],
hits[{t,s,k}], rms[], sections[]) y `grid_drift.json` (candidatas y motivo de
elección). Tiempos siempre en flotante; los campos son el contrato aguas abajo.

## 2. Qué es golpe fuerte y qué no

Detecta transientes por banda (sobre el stem o el componente percusivo):

| Pista | Banda | Conduce |
|-------|-------|---------|
| kick | 40–160 Hz | golpes/“slam”: 2–3 como máximo en toda la pieza |
| snare | 150–500 Hz + 1–3 kHz | cambios de plano/“algo nuevo” |
| hihat | 6–14 kHz | densidad de micro-motion; si escasea, recárgala |

Lista los hits como candidatas `{t, s, k}`; **candidatas, no disparadores**:
que haya kick en cada beat no autoriza un golpe visual por beat. Usa RMS +
densidad de batería para segmentar (intro/breakdown/alta energía); en
breakdown mete un respiro de marca, en alta energía permite capas paralelas.
Los 2–3 slams mayores (apertura/clímax/cierre) deben clavar los kicks
más fuertes — nunca "entre beats" (p. ej. b52.5) si el kick real está en
b52: fuera de rejilla sólo con datos de energía que lo justifiquen.

## 3. Escribe la timeline en beats, no en cuadros

Define constantes y deriva todo lo demás (los nombres son contrato):

```
SOURCE_BEAT0 = t0        // verdad del análisis; no la edites nunca
BEAT_INT     = T         // segundos por beat
OUTPUT_AUDIO_OFFSET_SEC  // desfase medido de la salida (§5); 0 si no hay
beatT(n) = SOURCE_BEAT0 + OUTPUT_AUDIO_OFFSET_SEC + n*BEAT_INT
beatF(n) = round(beatT(n) * FPS)   // conversión a frames sólo aquí
```

Cortes en beat entero; escaleras de aceleración con fracciones (p. ej.
48, 49.5, 50.5, 51, 51.25). Reglas de anclaje:

- Cortes densos (cada 1–2 beats) → rejilla ganadora `beatF(n)`.
- Acentos aislados y freezes → **clava el transiente real**, no un punto
  interpolado de la rejilla (el drift mínimo se amplifica en un solo golpe).
- Corte final → último transiente real + silencio RMS confirmado (no el rabo).
- Fuentes ajenas (footage, SFX) se alinean por **su pico interno**: `inicio =
  beat_objetivo − (t_pico − recorte)`; localiza el pico por envolvente de
  energía, no por cabecera del archivo.

Diseño: tomas de 4/8 beats; subidas en medio o cuarto de beat; piezas con
batería densa → SFX comedidos (sólo acciones propiamente visuales, slams
máximo 2–3); los slams de cuadro completo con tope duro (≤3 por pieza,
separados ≥16 beats, y un solo “bombeo” sostenido ≤4 beats); el motion por
beat va en el **elemento protagonista** (tarjeta/título/número), no en
cámara ni cuadro; estructura (morph/cámara/pose) con funciones continuas,
impactos como conmutadores en la frame elegida; múltiples capas en la misma
frame forman el acento — desalinea sólo 1–2 frames y sólo si es intención.

## 4. Pistas con tempo variable

Localiza los puntos de cambio con un tempogram local (~5 s); ajusta la
recta por segmento de energía (cada tramo con su t0/T). Si librosa y dos
métodos alternativos (p. ej. Essentia RhythmExtractor2013, madmom RNN+DBN)
no convergen, gana la rejilla con mayor cobertura de transientes; no adivines.

## 5. Verificación post-render (obligatoria en piezas al beat)

`ffmpeg -i final.mp4 -vn -acodec pcm_s16le /tmp/render-audio.wav` y repite
el ajuste de rejilla **sobre ese audio** (así se verifica también el
desfase de encapsulado, no sólo el análisis). Compara por corte:

| Veredicto | Error |
|-----------|-------|
| ideal | ≤1.5f |
| correcto | ≤3f (umbral perceptible) |
| obligado a corregir | >3f |

Si el error es un **desfase sistemático en la misma dirección** (+N frames
en todos los cortes), la causa casi siempre es el desfase de la salida
(priming de AAC; ~1.3f típico en 48 kHz), no el análisis: mídelo por
correlación cruzada contra la pista original y escríbelo en
`OUTPUT_AUDIO_OFFSET_SEC`. Nunca lo dejes en `SOURCE_BEAT0` — si cambias
codec o reanalizas, compensarías dos veces. A 30 fps, el cuantizado de
frame es ±16.7 ms (±8.3 a 60 fps): no afirmes precisión <5 ms a 30 fps;
si la tabla de errores supera la tolerancia, sube FPS, no retoques la
medición. Cualquier corte >3f: corrige beat/frame, re-renderiza y vuelve
a medir hasta que toda la tabla pase.

Adaptado (compacto, en español) del método de `music-beat-sync.md` de
**video-shotcraft** (Apache-2.0, github.com/Vincentwei1021/video-shotcraft,
inspeccionado 2026-11-15). No se incorpora su pipeline Remotion ni sus
tarjetas de shots.
