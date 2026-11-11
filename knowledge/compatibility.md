# Matriz de compatibilidad y evidencia

Solo se marca lo que se probó en una versión concreta, con HOME temporal y sin
credenciales. Un resultado verde en una prueba no demuestra todas las rutas del
producto ni sustituye las pruebas en el cliente real del operador.

| Cliente / versión | Qué se probó | Resultado observado | Límites |
|---|---|---|---|
| Codex CLI 0.167.1 (`@openai/codex`) | `sync` en HOME aislado y `skills/list` por `app-server`, sin sesión | Descubrió exactamente las 14 skills de `core`, `video` una sola vez, 5 skills del sistema del cliente y ningún módulo interno; sin errores de catálogo | No prueba activación por descripción, lectura de referencias, sandbox, MCP, modelo, Windows ni sesión autenticada |
| Claude Code 2.1.322 (`@anthropic-ai/claude-code`) | Ejecutable y versión; `sync` en HOME aislado | Enlaces creados; `auth status` indicó no autenticado | Descubrimiento y activación **no verificados**: requieren una sesión del operador. La documentación de Claude describe symlinks por entrada, pero no demuestra este canon |
| HyperFrames 0.9.33 (paquete npm local) | `video/scripts/hyperframes_init.py` con HOME y proyecto temporales | Proyecto generado, sin skills nuevas y con un marcador ajeno intacto | Solo el `init` del lanzador; no cubre otras versiones, `render`, red del sistema, dependencias ni comportamiento de agentes |
| Sync por enlaces | Pruebas unitarias y CI Linux/macOS/Windows en el commit anterior | Verde en ese commit; doctor local actual: 34 entradas válidas | Los cambios posteriores deben pasar el CI de la rama. Enlaces requieren symlinks o junctions y acceso al checkout |
| Otros clientes | No probado en esta revisión | Sin afirmación | Un enlace de repo no garantiza descubrimiento ni instalación automática |

## Reproducir sin credenciales

Codex, con una ruta a un binario ya instalado; el script crea HOME y proyecto
temporales, y no invoca al modelo:

```sh
python sync/tests/probe_codex.py --codex /ruta/a/codex
```

Claude: no se puede comprobar descubrimiento sin sesión; no reutilices
credenciales del operador. Si se autoriza, ejecuta en una máquina desechable y
un HOME aislado, revisa los permisos y no envíes prompts con datos reales.

HyperFrames: instala una versión revisada de forma local y autorizada, y usa el
lanzador documentado en `skills/video/references/hyperframes-init.md`. No uses
`npx @latest` ni el HOME real para probar. Una versión distinta exige nueva
revisión del paquete y de sus efectos.

## Criterio para añadir un cliente

1. Documentación oficial de su ruta global y precedencia.
2. Prueba de descubrimiento con HOME aislado y catálogo mínimo.
3. Confirmación de que los módulos internos no se exponen.
4. Prueba de activación por descripción y de lectura de una referencia.
5. Revisión de permisos, sandbox, red y manejo de secretos.
6. Registro de versión, fecha, evidencia y límites aquí y en `skills/REGISTRO.md`.
