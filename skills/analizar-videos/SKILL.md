---
name: analizar-videos
description: Analiza cualquier video (URL o archivo local). Descarga con yt-dlp, extrae frames con ffmpeg, obtiene transcripción (captions nativos o Whisper API), y responde preguntas sobre el contenido visual y auditivo.
---

# Analizar Videos

Descarga un video, extrae frames como JPEGs, obtiene transcripción (captions nativos primero, luego Whisper API), y combina ambos para responder preguntas.

## Dependencias

- **yt-dlp** ✅ instalado
- **ffmpeg** ✅ instalado
- **Python 3.14** ✅
- **Whisper API key** ❌ No configurada (solo captions nativos disponibles)

## Cómo invocar

**Paso 1 — parsear input.** Separar source (URL o path) de la pregunta.

Sources soportados: YouTube, Vimeo, X/Twitter, TikTok, Instagram, Twitch clips, Loom, archivos locales `.mp4`/`.mov`/`.mkv`/`.webm`.

**Paso 2 — ejecutar script** (desde la raíz de esta skill):
```powershell
python scripts/watch.py "<source>"
```

Flags opcionales:
- `--start T` / `--end T` — enfocar sección (`SS`, `MM:SS`, `HH:MM:SS`)
- `--max-frames N` — límite de frames (default 80, max 100)
- `--resolution W` — ancho en px (default 512; 1024 para texto en pantalla)
- `--fps F` — override auto-fps (clamped a 2 fps max)
- `--no-whisper` — desactivar transcripción (solo frames si no hay captions)

Ejemplos:
```powershell
python "...\scripts\watch.py" "https://youtu.be/dQw4w9WgXcQ"
python "...\scripts\watch.py" "video.mp4" --start 2:15 --end 2:45
```

**Paso 3 — leer cada frame.** Usar Read tool (JPEGs como imágenes). Leer todos en paralelo. Los frames están en orden cronológico con timestamp `t=MM:SS`.

**Paso 4 — responder.** Combinar frames (qué se ve) + transcripción (qué se dice). Citar timestamps si hay pregunta específica.

**Paso 5 — cleanup.** El script muestra el directorio temporal. Si no hay seguimiento, borrarlo.

## Frame budgets

| Duración | Frames default |
|---|---|
| ≤30s | ~30 |
| 30s-1min | ~40 |
| 1-3min | ~60 |
| 3-10min | ~80 |
| >10min | 100 (sparse) |

Hard caps: 2 fps, 100 frames max.

## Transcripción

1. **Captions nativos** (gratis, preferido) — yt-dlp extrae subs manuales o auto-generados.
2. **Whisper fallback** — si no hay captions, extrae audio y envía a Groq/OpenAI API. Requiere API key.
3. **`--no-whisper`** — saltar fallback. Solo frames si no hay captions.

## Modos de fallo

- **Sin yt-dlp/ffmpeg** — reinstalar: `pip install yt-dlp` / `winget install ffmpeg`
- **Sin transcripción** — captions ausentes + sin Whisper key. Proceder solo frames.
- **Video largo** — ofrecer re-run enfocado con `--start`/`--end`
- **Descarga falla** — probablemente login requerido o region-lock. Informar.
