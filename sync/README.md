# sync/ — sincronizador neutral del harnés (v0.4)

Un solo estándar universal y un solo origen físico. Cualquier agente del mundo sincroniza con el enlace del repo; los agentes instalados en esta máquina reciben una **junction** al mismo almacén, no una copia.

## Modelo

```
canon (repo/skills)  ->  ~/.agents/skills  ->  junctions a cada cliente
```

- `~/.agents/AGENTS.md` — instrucciones (estándar abierto de agentes).
- `~/.agents/skills/` — **única copia física** de las 34 skills activas.
- Cada cliente detectado apunta ahí con una junction: editar una skill en el canon (y sincronizar) la cambia para todos a la vez.

## Destinos

Los destinos viven en `targets.json` (datos, no código): el script no conoce nombres de agentes.

| Cliente | Ruta | Modo |
|---|---|---|
| universal | `~/.agents/skills` | copia desde el canon |
| claude | `~/.claude/skills` | junction de directorio |
| gemini | `~/.gemini/skills` | junction de directorio |
| continue | `~/.continue/skills` | junction de directorio |
| qwen | `~/.qwen/skills` | junction de directorio |
| factory | `~/.factory/skills` | junction de directorio |
| crush | `~/.config/crush/skills` | junction de directorio |
| devin | `~/.config/devin/skills` | junction de directorio |
| goose | `~/.config/goose/skills` | junction de directorio |
| codex | `~/.codex/skills` | junction por entrada (preserva `.system`) |

OpenCode no necesita puente: lee `~/.agents/skills` de forma nativa. Por eso `~/.config/opencode/skills` ya no existe (se movió a `skills.bak-*` al migrar).

Instrucciones: `AGENTS.md` se copia a `~/.agents/AGENTS.md`, `~/.gemini/GEMINI.md`, `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.qwen/QWEN.md` y `~/.factory/AGENTS.md`.

## Comandos

```powershell
sync\sync.ps1            # instala/actualiza almacén, instrucciones y junctions
sync\sync.ps1 -Verify    # solo comprueba (exit 1 si hay drift)
sync\doctor.ps1          # auditoría integral (skills, JSON, sync, secretos)
```

`-Verify` es la verdad operativa: si devuelve 0, canon y clientes son idénticos.

## Reglas de seguridad

- Las junctions se borran con `[IO.Directory]::Delete(path, $false)`; nunca se sigue el enlace al borrar.
- Un destino que existe como carpeta real se **mueve** a `<ruta>.bak-<fecha>` antes de sustituirse por junction. Nada se destruye.
- Las skills retiradas del canon se podan del almacén y de las junctions del cliente; las copias reales de un cliente no se tocan.

## Cómo sincronizar otro agente cualquiera

1. Le pasas el enlace del repo; lee `AGENTS.md` + `README.md`.
2. `install.ps1` clona/actualiza el canon y ejecuta `sync\sync.ps1`.
3. Si su cliente no lee `~/.agents/skills`, se añade su ruta a `targets.json` (una fila) y el próximo sync crea la junction. Si no soporta junctions, se usa `"mode": "copy"`… que hoy no está implementado: en ese caso, copia manual desde el canon y documenta la excepción.

## Protocolo Codebuff/Freebuff (manual, por fuera del sync)

La cuenta de skills server-side (codebuff.com, `PUT /api/v1/cloud/skills`) se controla aparte: cuando el canon cambie de skills activas, re-PUT con revision vigente + lista completa. Límites: `instructions ≤ 50KB`, `files[].contents ≤ 100KB`, `files ≤ 100/skill`, total ≤ 2.5MB. Riesgo conocido: `~/.agents/skills` y `~/.claude/skills` alimentan el importer de Freebuff — al arrancar, la app re-añade al server lo que exista en esos dirs locales. Con junctions, el importer sigue viendo las 34 skills del canon: si se retira una, hay que re-PUT para que no resucite.
