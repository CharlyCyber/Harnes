---
name: last30days
description: Investigacion social cross-platform de los ultimos 30 dias en Reddit, X, YouTube, TikTok, HN, Polymarket, GitHub y web. Usar para tendencias, reputacion, competidores y actividad reciente.
---

# Last30Days — Skill de Investigación Social Cross-Platform

> Motor de investigación que busca cualquier tema en Reddit, X, YouTube, TikTok, HN, Polymarket, GitHub y la web — y sintetiza un brief con scoring por engagement real de los últimos 30 días.

## Capacidades

- **Búsqueda cross-platform**: Reddit (threads + top comments), X/Twitter, YouTube (transcripts completos), TikTok, HN, Polymarket (odds en tiempo real), GitHub (PRs, issues, releases), Bluesky, Threads, Web
- **Síntesis con scoring**: Resultados rankeados por upvotes, likes y dinero real (Polymarket), no por SEO
- **Intelligent Search**: Resuelve handles, subreddits, canales YouTube y hashtags antes de buscar
- **Best Takes**: Detección de humor y viralidad separada del scoring de relevancia
- **Clustering cross-source**: Misma historia en Reddit + X + YouTube = un cluster
- **Competitor comparisons**: `/last30days "X vs Y"` single-pass comparison
- **ELI5 mode**: Síntesis en lenguaje simple
- **HTML briefs**: Reportes compartibles dark-mode offline
- **Trend monitoring**: Acumulación de hallazgos en SQLite con watchlists y briefings diarios/semanales

## Uso

Activa esta skill cuando:
- Necesites **investigar un tema** (persona, empresa, producto, tecnología) en redes sociales
- Quieras saber **qué dice la gente ahora** sobre algo (no blogs viejos)
- Antes de **reuniones con CEOs, ventas, entrevistas** — conocer activity reciente
- **Análisis de competidores** y tendencias de mercado
- **Due diligence** de productos, personas o startups

## Archivos de Referencia

| Archivo | Contenido |
|---|---|
| `references/sources.md` | Fuentes de búsqueda, APIs, configuración de keys |
| `references/workflow.md` | Pipeline de investigación: resolución → búsqueda → scoring → síntesis |
| `references/configuration.md` | Variables de entorno, keys, setup wizard |

## Quick Start

```bash
# Investigar una persona
/last30days Peter Steinberger

# Investigar producto o tecnología
/last30days OpenClaw

# Comparar competidores
/last30days "OpenClaw vs Hermes vs Paperclip"

# Output HTML para compartir
/last30days "Cursor IDE" --emit=html

# Análisis de señales de contratación
/last30days "Listen Labs" --hiring-signals
```

## Integración con Otras Skills

- **`analizar-videos`**: last30days busca contenido, analizar-videos profundiza en videos específicos
- **`advanced-scraping`**: last30days es research social, scraping es extracción estructurada
