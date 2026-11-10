# Hooks y permisos

`python hooks/check_secrets.py --repo .` escanea archivos rastreados del árbol y
URLs de remotes; `--staged` escanea el contenido del índice, no el árbol. Emite
solo nombres de archivo y tipo de hallazgo, nunca valores. Es heurístico: omite
binarios, no revisa historial ni secretos ignorados, puede fallar o dar falsos
positivos. Usa además un escáner de historial y rota cualquier credencial
comprometida. No publica ni altera remotes.

`python hooks/install_hook.py` instala `pre-commit` **solo en este repo**, si no
existe otro hook ni `core.hooksPath`; no pisa configuración. Para otros proyectos,
integra su propia herramienta de secretos y sus hooks existentes. Un pre-commit
puede omitirse y ocurre solo al hacer commit: aplica también comprobaciones en CI.

Las instrucciones en Markdown no bloquean herramientas. Usa sandbox de sistema,
aprobaciones y permisos nativos de cada cliente; prueba sus reglas antes de
operar en datos reales. `config/opencode.example.json` es un ejemplo opcional
con aprobación por defecto y algunos bloqueos, no se instala ni sustituye la
configuración del usuario. Sus patrones de texto no cubren todas las variantes
de comandos y **no son una barrera de seguridad**.
