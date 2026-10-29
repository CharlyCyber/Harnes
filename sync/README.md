# sync/ — instalador del harnés

Instala el canon (AGENTS.md, skills) en cada agente soportado.

- `sync.ps1` — instalador. Parámetros: `-Agent <nombre>` (o sin parámetro = todos), `-Verify`.
- `ledger.json` — registro determinista de cada archivo instalado y su destino (fuente única de verdad para actualizar o limpiar).

Soportados en v0.1: `opencode`. Próximos (añadir según se use): `claude-code` (CLAUDE.md), `gemini` (GEMINI.md), `kilo` (instructions en kilo.jsonc), `antigravity`, `freebuff`.
