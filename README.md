# Harnás de CHARLI v0.4

Harnés agéntico portable multi-agente, disk-first. Canon único; las copias instaladas son derivadas reproducibles.

## Estructura

```
AGENTS.md            reglas ratchet (cada línea trazable a knowledge/failures.md)
knowledge/           memoria disk-first: identity, decisions, failures
skills/              catálogo canónico (34 activas; estándar agentskills.io)
hooks/               enforcement (éxito silencioso, fallos verbosos)
sync/                sync.ps1 (almacén universal + junctions) y doctor.ps1
sync/tests/          smoke tests del motor (HOME y canon desechables)
.github/workflows/   CI: tests + sync + doctor en cada push y PR
```

## Principios

1. **Agente = Modelo + Harnés** (Trivedy/Osmani). Cada componente existe porque un fallo o comportamiento lo justifica.
2. **Ratchet:** cada fallo del agente → regla / hook / skill. Sin evidencia, no se añade nada.
3. **Éxito silencioso, fallos verbosos.**
4. **Solo rutas relativas.** El harnés funciona desde cualquier ruta.
5. Simple primero; complejidad solo cuando la evidencia la pida.

## Sincronización con cualquier agente (neutro)

**Cualquier agente del mundo**, con solo el enlace del repo:

```powershell
irm https://raw.githubusercontent.com/CharlyCyber/Harnes/main/install.ps1 | iex
```

Contrato neutro: al abrir el repo, un agente lee `AGENTS.md` (reglas) + este README. `install.ps1` clona/actualiza el canon y corre `sync\sync.ps1`, que deja **una sola copia física** de las skills en `~\.agents\skills\` y enlaza cada cliente detectado con una junction (cero duplicación, cero drift). Los destinos viven en `sync\targets.json`, no en el código. Verificación: `sync\doctor.ps1`. Detalles: `sync/README.md`.

## Referencia de diseño

Véase knowledge/decisions.md.
