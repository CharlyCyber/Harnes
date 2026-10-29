# hooks/

Capa de enforcement (reglas que el sistema impone, no solo sugiere). Principios:

- **Éxito silencioso, fallos verbosos:** exit 0 sin ruido; fallar imprime el error accionable en el bucle.
- Cada hook nace de un fallo real registrado en `knowledge/failures.md`.

## Pendiente v0.2 (primeros hooks previstos)

- `check.ps1`: gate de calidad (lint/format/test) que se dispara tras edits relevantes y commits.
- Bloqueo de comandos destructivos (`rm -rf`, `git push --force`) sobre el canon del harnés.

Un hook sin fallo real que lo justifique no se escribe; primero llega el fallo al registro de trinquete.
