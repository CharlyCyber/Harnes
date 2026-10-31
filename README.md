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

## Sincronización con cualquier agente (neutro)

**Cualquier agente del mundo**, con solo el enlace del repo:

```powershell
irm https://raw.githubusercontent.com/CharlyCyber/Harnes/main/install.ps1 | iex
```

Contrato neutro: al abrir el repo, un agente lee `AGENTS.md` (reglas) + este README. `install.ps1` clona/actualiza el canon y corre `sync/sync.ps1`, que instala el estándar universal (`~\.agents\AGENTS.md` + `~\.agents\skills\`) y refresca los puentes previos por `ledger.json` — sin planes hardcodeados por IDE. Detalles: `sync/README.md`.

## Referencia de diseño

Véase knowledge/decisions.md.
