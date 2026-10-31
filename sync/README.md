# sync/ — instalador neutro del harnés (v0.3)

Un solo estándar universal, sin planes por agente. Cualquier agente del mundo sincroniza con solo tener el enlace del repo.

## Destinos universales

- `~\.agents\AGENTS.md` — instrucciones del canon (estándar abierto de agentes).
- `~\.agents\skills\<skill>\` — skills activas del canon.

## Puentes sin nombres

Cada instalación previa registrada en `ledger.json` se refresca desde el canon si su destino aún existe (así los agentes ya configurados — p. ej. OpenCode — quedan al día sin hardcodear nombres). Si el canon retiró una fuente, la copia puente obsoleta se elimina: el canon es la única fuente de verdad.

## Comandos

- `sync.ps1` — instala/actualiza universal + puentes.
- `sync.ps1 -Verify` — solo comprueba (exit 1 si desfasado).

## Cómo sincronizar otro agente cualquiera

1. Le pasas el enlace del repo; al abrirlo lee `AGENTS.md` y `README.md` (sección Instalación).
2. `install.ps1` → clona/actualiza canon + corre `sync.ps1` → universal + puentes ledger.
3. Si el agente NO lee `~\.agents\skills\` ni `AGENTS.md` global: se le pide a sí mismo que copie lo que su cliente necesite desde el canon (es agente, sabe lo suyo) y que registre el destino en `ledger.json` (una fila con `kind`, `source` relativo, `dest` relativo a `~\`). El próximo sync lo mantiene.

## Protocolo Codebuff/Freebuff (manual, por fuera del sync)

La cuenta de skills server-side (codebuff.com, `PUT /api/v1/cloud/skills`) es controlada aparte: cuando el canon cambie de skills activas, re-PUT con revision vigente + lista completa. Límites: `instructions ≤ 50KB`, `files[].contents ≤ 100KB`, `files ≤ 100/skill`, total ≤ 2.5MB. Riesgo conocido: `~\.agents\skills` y `~\.claude\skills` alimentan el importer de Freebuff — al arrancar, la app re-añade al server lo que exista en esos dirs locales (verificar contra este protocolo en el próximo relaunch).
