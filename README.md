# Harnás de CHARLI v0.1

Harnés agéntico portable multi-agente, disk-first. Canon único; las copias instaladas son derivadas reproducibles.

## Estructura

```
AGENTS.md            reglas ratchet (cada línea trazable a knowledge/failures.md)
knowledge/           memoria disk-first: identity, decisions, failures
skills/              catálogo (vacío al inicio; estándar agentskills.io)
hooks/               enforcement (éxito silencioso, fallos verbosos)
sync/                instalador determinista e idempotente para cada agente
```

## Principios

1. **Agente = Modelo + Harnés** (Trivedy/Osmani). Cada componente existe porque un fallo o comportamiento lo justifica.
2. **Ratchet:** cada fallo del agente → regla / hook / skill. Sin evidencia, no se añade nada.
3. **Éxito silencioso, fallos verbosos.**
4. **Solo rutas relativas.** El harnés funciona desde cualquier ruta.
5. Simple primero; complejidad solo cuando la evidencia la pida.

## Sinchronización

Instalar en todos los agentes soportados ejecuta sync/sync.ps1 (ver sync/README.md).

## Referencia de diseño

Véase knowledge/decisions.md.
