# Sincronización

`harnes.py` usa Python 3.9+ de biblioteca estándar, sin Git ni PowerShell en
runtime. En POSIX crea enlaces simbólicos; en Windows, junctions por skill. Cada
enlace apunta a la carpeta del canon, no a una copia. Los wrappers `sync.ps1` y
`doctor.ps1` siguen disponibles en PowerShell 5.1 y 7, con Python en PATH.

## Comandos

```sh
python sync/harnes.py sync                 # instala el último perfil elegido, core al principio
python sync/harnes.py sync --profile all   # catálogo completo
python sync/harnes.py sync --profile core  # vuelve al mínimo
python sync/harnes.py sync --adopt         # respalda colisiones y migra enlaces antiguos
python sync/harnes.py verify               # solo lectura; exit 1 con drift
python sync/harnes.py doctor --skip-sync   # valida canon sin instalación
```

`--home RUTA` antes del subcomando permite pruebas aisladas. `HARNES_HOME` es
alternativa para los wrappers. El `doctor` necesita `skills-ref`:
`python -m pip install -r sync/requirements.txt`.

## Modelo y custodia

`targets.json` declara perfiles, rutas, fuentes de instrucciones y rutas antiguas que el doctor revisa por posibles duplicados (sin modificarlas). El directorio
padre debe existir para detectar un cliente; la ruta universal se crea siempre.
El inventario `~/.harnes/state.json` registra **solo enlaces creados por el
harnés**. Al cambiar de perfil, se quitan solo enlaces inventariados que siguen
apuntando al destino registrado. Contenido ajeno, enlaces cambiados y enlaces
idénticos de otro gestor no se borran. El sync se detiene si encuentra conflictos,
ancestros enlazados, marcadores malformados o un inventario inválido.

`--adopt` mueve cada colisión a `~/.harnes/backups/<id>/...`; no fusiona su
contenido. Los enlaces antiguos de directorio se respaldan como enlaces, no se
copian sus destinos. Las instrucciones del harnés anterior se respaldan antes
de sustituirlas; las demás conservan su contenido externo en torno al bloque
`charli-harness:begin/end`. No se adopta ni limpia un enlace individual cuyo
propietario se desconoce. `--adopt` es una operación de migración explícita, no
una política de borrado.

El estado se guarda por operación para facilitar recuperación tras interrupciones;
no es una transacción completa. Haz backup propio antes de migrar. Si un enlace o
el checkout cambia durante el sync, vuelve a verificar. No ejecutes dos sync en
paralelo. El inventario y los backups deben ser privados y fiables.

## Extender a otro agente

Comprueba su documentación, ubicación global, descubrimiento de enlaces,
precedencia, versión y permisos. Si lee `~/.agents/skills`, no añadas otro
puente; si no, declara su ruta nativa en `clients`. Añade instrucciones solo
cuando el cliente las cargue realmente. Prueba con HOME desechable y con el
cliente real. Algunos productos solo aceptan configuraciones remotas o no pueden
seguir enlaces: necesitan un adaptador distinto, no una promesa de soporte.
No se instala ni modifica el servidor de Codebuff/Freebuff.

## Pruebas con clientes reales

`python sync/tests/probe_codex.py --codex /ruta/a/codex` crea HOME y proyecto
temporales, sincroniza y consulta el catálogo por `app-server`; no inicia sesión
ni invoca el modelo. Verifica que `video` aparece una vez y que los módulos
internos no se exponen. Claude y otros clientes requieren una sesión del
operador y no se prueban con credenciales del repo.

El test opcional de HyperFrames (`test_real_hyperframes_init_preserves_home_skills`)
se ejecuta solo si `HARNES_TEST_HYPERFRAMES_PACKAGE` apunta a un paquete local ya
revisado. No descarga nada y no forma parte del CI.

## Video unificado y migración

`video` está en `core` y `all`; `internal_skills` enumera módulos del canon que
se consultan desde ella, pero no se enlazan como skills públicas. En el siguiente
`sync` se retiran solo los enlaces anteriores inventariados que aún apuntan a sus
destinos originales. Copias y enlaces de terceros se conservan y pueden competir;
revísalos manualmente. El checkout debe seguir accesible y el cliente debe poder
leer referencias fuera del directorio de la skill a través de la ruta real resuelta;
clientes que lo impidan necesitan otro adaptador. Reinicia el agente.
