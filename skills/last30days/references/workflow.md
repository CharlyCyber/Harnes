# Pipeline de Investigación — Last30Days

## Fase 1: Resolución Inteligente

Antes de buscar, el motor entiende el tema:
- Persona → resuelve @handle en X, repos GitHub, subreddits, canales YouTube
- Producto → resuelve founder, company, comunidades
- Bidireccional: persona→compañía, producto→fundador, nombre→perfil GitHub

## Fase 2: Búsqueda Paralela Multi-Fuente

Todas las fuentes se consultan simultáneamente:
- Multi-query expansion por fuente
- Timeout budgets por fuente (una lenta no mata el run)
- Per-author cap (máx 3 items por autor)

## Fase 3: Scoring por Engagement Real

Resultados rankeados por:
- Upvotes (Reddit, HN)
- Likes (X, YouTube)
- Views (TikTok, YouTube)
- Odds respaldadas por dinero (Polymarket)
- Engagement rate compuesto

## Fase 4: Clustering Cross-Source

Misma historia en múltiples fuentes = un cluster
- Entity-based overlap detection
- Títulos diferentes pero mismo contenido → merge automático

## Fase 5: Síntesis con AI Judge

El juez AI sintetiza todo en un brief:
- Narrative con citas por fuente
- Best Takes: detección de humor y viralidad
- Scoring de relevancia + entretenimiento
- ELI5 mode disponible

## Outputs

| Formato | Descripción |
|---|---|
| Markdown en chat | Brief completo con citas |
| HTML | Dark-mode, offline, shareable (--emit=html) |
| SQLite | Trend monitoring (--store) |
