# Harnés de CHARLI

Un canon para instrucciones y skills, con sincronización conservadora para varios
agentes. El objetivo es que puedas dar el enlace de este repo a un agente para
que siga estas instrucciones; **un enlace no puede garantizar acceso, instalación
ni compatibilidad con todos los productos**. Se necesita acceso al repo, un entorno
con sistema de archivos y un cliente que admita instrucciones y/o skills locales.
Los agentes exclusivamente web o con configuración del servidor requieren otro adaptador.

## Empezar desde el enlace

El repositorio es privado: autoriza Git/GitHub en la máquina o entorno del agente
antes de clonar. Nunca pegues tokens en el chat o en la URL. Con Git y Python 3.9+:

```sh
git clone https://github.com/CharlyCyber/Harnes.git
cd Harnes
python sync/harnes.py sync
python sync/harnes.py verify
```

En Windows usa `py -3` si `python` no está disponible. Revisa el código y pide
permiso antes de ejecutar el sync: modifica configuración del usuario. No uses
`curl | bash` ni `irm | iex`. No clona ni ejecuta automáticamente código remoto.

## Actualizar y sincronizar una instalación

Después de fusionar cambios a `main`, usa el comando seguro en cada máquina o
entorno que mantenga su propio checkout:

```sh
python sync/harnes.py refresh
```

`refresh` valida el canon, exige checkout limpio en la rama local `main`, hace
fetch de `origin/main` y fast-forward únicamente; después sincroniza solo los
enlaces e instrucciones declarados por Harnés y verifica el resultado. No cambia
de rama, no guarda/restaura cambios, no instala dependencias y nunca usa
`--adopt`. Si detecta un conflicto, se detiene sin adoptar contenido ajeno y
muestra qué revisar. El checkout puede haber avanzado si el conflicto se detecta
después del fast-forward, pero la sincronización no lo resolverá sobrescribiendo
la ruta. Si falta el validador, instálalo una vez con
`python -m pip install -r sync/requirements.txt`.

Si solo quieres actualizar el checkout y verificar sin sincronizar la
configuración del usuario, usa `python sync/harnes.py update`. Para comprobar el
canon sin modificar el HOME, usa `python sync/harnes.py doctor --skip-sync`.

Al terminar, reinicia o recarga los agentes para que relean las skills. Si varios
agentes de una máquina comparten los mismos enlaces al checkout, actualízalo una
vez; máquinas y entornos aislados se actualizan por separado. El checkout debe
permanecer en su lugar: las skills apuntan a él; si se mueve, vuelve a ejecutar
`refresh` desde su nueva ruta. Las actualizaciones upstream (por ejemplo,
HyperFrames) no se importan con este comando: se revisan e integran en Harnés
mediante cambios versionados y un PR.

En una instalación anterior de este harnés, ejecuta **solo después de revisar**:

```sh
python sync/harnes.py sync --adopt
```

Sin `--adopt`, un conflicto se detiene sin reemplazarlo. Con `--adopt`, las
colisiones y los enlaces de directorio antiguos se mueven a respaldos individuales
en `~/.harnes/backups/`, sin borrar sus destinos. Revisa esos respaldos y los
antiguos `~/.codex/skills` / `~/.gemini/skills`: el sync **no elimina** enlaces o
skills ajenos ni migraciones que no pueda atribuir. Puede ser necesaria limpieza
manual, previa revisión. El respaldo de una junction antigua sigue siendo un
**enlace**, no una copia independiente de su destino.

## Skills y perfiles

- Por defecto, `core` activa 12 skills, incluidas `video` y `web`, las entradas únicas para vídeo y diseño/desarrollo web; el protocolo A/B de cuatro tareas está en [knowledge/video-evaluation.md](knowledge/video-evaluation.md). `python sync/harnes.py sync --profile all` activa 16 skills públicas; para volver, usa `--profile core`. Los módulos internos de vídeo y web se cargan bajo demanda desde el checkout, no se registran como skills independientes. `web` incorpora guías nativas Baseline vendorizadas de Modern Web Guidance (Apache-2.0) para motion y View Transitions.
- Los enlaces por skill apuntan directamente al checkout. No hay copia física
  duplicada gestionada por el harnés. Las skills de otros gestores se conservan.
- `~/.agents/skills` es la ruta interoperable para clientes que la soportan;
  Claude y otros clientes detectados reciben enlaces por entrada en sus rutas
  nativas según `sync/targets.json`. Gemini y Codex usan la ruta universal, sin
  segundo enlace de skills. Un cliente nuevo se añade ahí solo tras comprobar su
  documentación y comportamiento de descubrimiento. Se requiere soporte de
  enlaces simbólicos o junctions y acceso al checkout.
- Cambiar archivos a través de un enlace **modifica el canon**. Trátalos como
  solo lectura durante el trabajo normal. Los enlaces no son una frontera de
  seguridad. No dejes que otros gestores sin revisar administren esos destinos.
- `cavecrew` se retiró por su solapamiento parcial con `caveman` y por faltar
  sus tres subagentes; sus funciones no eran idénticas. La procedencia y límites
  del catálogo están en `skills/REGISTRO.md`, y la evidencia por cliente en
  [knowledge/compatibility.md](knowledge/compatibility.md).

Las instrucciones se actualizan dentro de un bloque delimitado en archivos
compatibles, preservando el contenido externo. No se cambia ninguna configuración
MCP ni permiso automáticamente. Las rutas, detección y migración se explican en
[sync/README.md](sync/README.md).

## Verificación y seguridad

```sh
python -m pip install -r sync/requirements.txt
python sync/harnes.py doctor             # validación + sync + secretos
python -m unittest discover -s sync/tests -p 'test_*.py'
python hooks/install_hook.py              # opcional, solo para este repo
```

El hook examina lo preparado para commit y los remotes; no sustituye un gestor
de secretos ni una auditoría del historial. Para revisar todos los blobs
alcanzables sin imprimir valores: `python skills/security-audit/scripts/history_scan.py .`
Véanse [hooks/README.md](hooks/README.md) y [SECURITY.md](SECURITY.md).
Las credenciales que hayan estado expuestas deben rotarse manualmente; no se
puede demostrar su revocación desde este repo. Configura sandbox y aprobaciones
nativas de cada cliente antes de dar autonomía: las reglas de texto y filtros
por patrón no son barreras de seguridad.

La inicialización de HyperFrames no se ejecuta con `npx`: usa el lanzador limitado
que se describe en `skills/video/references/hyperframes-init.md`, después de revisar
y autorizar la instalación local. La matriz de lo realmente probado, con sus
límites, está en [knowledge/compatibility.md](knowledge/compatibility.md).

`config/mcp.json` inventaría servidores opcionales y versiones; el ejemplo de
OpenCode debe revisarse y fusionarse manualmente. `knowledge/mcps.md` documenta
sus claves y limitaciones. El CI prueba Linux, macOS y Windows, además de validar
skills y ejecutar pruebas. No garantiza el comportamiento de cada agente.

## Organización

`AGENTS.md`: guía del repo · `instructions/`: preferencias globales · `skills/`:
capacidades · `knowledge/`: decisiones y fallos · `sync/`: motor y tests ·
`hooks/`: comprobaciones opcionales · `config/`: ejemplos, no configuración aplicada.
