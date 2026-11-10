# Skills

Catálogo canónico con perfiles en `sync/targets.json`; ver `REGISTRO.md` para
procedencia y límites. Cada skill usa `SKILL.md` y recursos opcionales en
`scripts/`, `references/` o `assets/`. Un `_DORMIDA.md` la excluye del sync.

Antes de adoptar una: justificar su utilidad, inspeccionar instrucciones y código,
verificar licencia, fijar el commit y registrar procedencia. Popularidad no implica
seguridad. Preferir referencias bajo demanda y descripciones breves; validar con
`python sync/harnes.py doctor --skip-sync`. No instalar directamente con gestores
globales si se pretende que el canon la gestione.
