---
name: video-use
description: Edicion de video asistida por IA con ffmpeg, transcripcion, timeline visual, overlays y generacion de final.mp4 desde lenguaje natural.
---

# video-use — Edición de Video Asistida por IA

> Skill para editar videos mediante agente IA. Drop raw footage en una carpeta, describe el resultado, obtén `final.mp4`. 100% open source.

## Descripción

`video-use` permite que un agente IA (Claude, Codex, Hermes, opencode) edite videos mediante comandos de lenguaje natural. Sin presets ni menús — el LLM razona sobre el contenido y produce cortes precisos.

## Stack técnico

- **ffmpeg** — required (cortes, fades, grading, subtítulos)
- **yt-dlp** — optional (descarga videos online)
- **ElevenLabs Scribe** — transcripción con timestamps word-level + diarización
- **uv / pip** — Python deps
- **HyperFrames / Remotion / Manim / PIL** — animation overlays (paralelo por animación)

## Cómo funciona

El LLM **lee** el video, no lo ve:

**Capa 1 — Transcripción de audio** (siempre cargada). ElevenLabs Scribe por fuente. Timestamps palabra por palabra, diarización de speakers, eventos de audio. Todas las tomas empaquetadas en un `takes_packed.md` (~12KB).

```
## C0103  (duration: 43.0s, 8 phrases)
  [002.52-005.36] S0 Ninety percent of what a web agent does is completely wasted.
  [006.08-006.74] S0 We fixed this.
```

**Capa 2 — Composite visual** (bajo demanda). `timeline_view` produce filmstrip + waveform + word labels PNG para cualquier rango temporal. Solo en puntos de decisión.

## Pipeline

```
Transcribe ──> Pack ──> LLM Razona ──> EDL ──> Render ──> Self-Eval
                                                              │
                                                              └─ issue? fix + re-render (max 3)
```

1. **Transcribe**: ElevenLabs Scribe por fuente → word timestamps + speakers + eventos
2. **Pack**: todas las tomas → `takes_packed.md`
3. **LLM razona**: propone estrategia de edición, espera aprobación
4. **EDL**: Edit Decision List — cortes precisos con word-boundary
5. **Render**: ffmpeg aplica cortes, fades, color grade, subtítulos
6. **Self-Eval**: `timeline_view` en output renderizado en cada cut boundary. Atrapa visual jumps, audio pops, subtítulos ocultos. Máx 3 re-renders.

## Capacidades

- Corta filler words (`umm`, `uh`, falsos arranques) y silencios entre tomas
- Auto color grading (warm cinematic, neutral punch, o custom ffmpeg chain)
- Fades de audio de 30ms en cada corte (sin pops)
- Subtítulos quemados (estilo configurable, 2-word UPPERCASE chunks default)
- Animation overlays via HyperFrames/Remotion/Manim/PIL (sub-agentes paralelos)
- Sesión persistente en `project.md` (retomar donde quedaste)
- Soporta: talking heads, montajes, tutoriales, travel, entrevistas

## Setup prompt

```text
Set up https://github.com/browser-use/video-use for me.
Read install.md first, register the skill, set up ElevenLabs API key.
After install, don't transcribe anything — tell me it's ready and wait.
```

## Uso

```bash
cd /path/to/tus/videos
cp .env.example .env   # ELEVENLABS_API_KEY=...
# abrir sesión de agente
> edita esto en un video de lanzamiento
```

Output en `<videos_dir>/edit/final.mp4`. El directorio skill se mantiene limpio.

## Principios de diseño

1. **Texto + visuales bajo demanda.** No frame-dumping. Transcript es la superficie.
2. **Audio es primario, visuales siguen.** Cortes basados en speech boundaries y silence gaps.
3. **Ask → confirm → execute → self-eval → persist.** Nunca tocar el cut sin aprobación de estrategia.
4. **Zero assumptions sobre tipo de contenido.** Look, ask, then edit.
5. **12 hard rules, libertad artística en lo demás.**

## Referencias

- Repo: <https://github.com/browser-use/video-use>
- HyperFrames: <https://github.com/heygen-com/hyperframes>
- Browser Use Box: <https://browser-use.com/bux>

## Complementa

**`references/analyze.md`** (READ) — analiza un video descargado: extrae frames, transcribe y responde preguntas sobre lo que se ve y se oye. Scripts en `scripts/` (`watch.py`, `download.py`, `frames.py`, `transcribe.py`).
**video-use** (WRITE) — edita y produce videos nuevos.
**hyperframes** — composiciones de video HTML, animations, overlays, captions.
