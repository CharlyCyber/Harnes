# Inicialización controlada de HyperFrames

Los documentos upstream del canon pueden recomendar `npx hyperframes init`; ese comando puede instalar/actualizar skills. En su lugar usa `video/scripts/hyperframes_init.py`. No ejecutes directamente un init desde otros módulos, ni interpretes el flag `--skip-skills` como garantía para versiones arbitrarias.

El lanzador acepta exclusivamente un paquete **ya instalado localmente** `hyperframes@0.9.33`, cuyo opt-out se inspeccionó en el paquete npm y se probó en HOME temporal. Fuerza `HYPERFRAMES_SKIP_SKILLS=1`, `HYPERFRAMES_NO_UPDATE_CHECK=1` y `HYPERFRAMES_NO_TELEMETRY=1` (la prueba comprueba además que no aparece un directorio de skills en el HOME ni en el proyecto); llama a Node directamente, sin `npx`, para inicializar un proyecto nuevo con el ejemplo vacío. Rechaza otras versiones o un destino existente. Comprobación de versión **no verifica integridad del paquete ni dependencias**. Revisa la fuente y el lockfile del proyecto antes de usarlo; solicita permiso si hay que instalar paquetes. No instala nada.

```sh
python3 "<VIDEO_DIR>/scripts/hyperframes_init.py" \
  --package-dir "<ruta-local>/node_modules/hyperframes" "<ruta-proyecto-nuevo>"
```

Windows: usa `py -3` si hace falta. El comando puede crear estado de HyperFrames en el HOME y archivos en el proyecto. No es un sandbox ni un bloqueo de red del sistema; usa permisos nativos y restricciones de red. El `package.json` generado puede incluir comandos `npx` (descarga/ejecución y otras operaciones): revísalos y usa una instalación local fijada y autorizada. No ejecutes sus comandos de publicación sin autorización. Si el CLI falla, no conviertas su salida en éxito ni repitas sin revisar lo creado.

El control de esta versión se aplica **solo al init mediante este lanzador**, no garantiza que otro script o ejecución de HyperFrames conserve esas propiedades. Proyectos existentes con otra versión no deben actualizarse en silencio: conservarlos, informar y verificar primero su comportamiento en aislamiento. La integración funcional y el uso por agentes reales requieren pruebas adicionales.

Prueba reproducible (opt-in, sin descarga; requiere un paquete ya instalado):

```sh
HARNES_TEST_HYPERFRAMES_PACKAGE="/ruta/node_modules/hyperframes" \
  python -m unittest sync.tests.test_harnes.VideoTests
```

En Windows, define la variable con `set` o `$env:` y ejecuta `py -3`. La prueba usa un HOME temporal, conserva un marcador ajeno y comprueba que no aparecen skills en el HOME ni en el proyecto. Si no se define, se omite; el CI no instala HyperFrames.
