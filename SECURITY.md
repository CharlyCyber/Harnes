# Seguridad

No publiques credenciales ni detalles sensibles en issues o PR públicos. Reporta
los problemas de forma privada al propietario por un canal seguro; GitHub Private
Vulnerability Reporting puede usarse si está habilitado en el repositorio.

Los filtros de secretos son heurísticos y no comprueban el historial completo.
Rota inmediatamente cualquier credencial expuesta y revisa su alcance. Los
archivos de instrucciones, skills y MCP son código/datos de terceros potencialmente
activos: revisa su origen, permisos, scripts y dependencias antes de instalarlos.
Los patrones de hooks o permisos no sustituyen un sandbox ni permisos mínimos.

## Revisión de esta versión

- **Historial alcanzable:** `python skills/security-audit/scripts/history_scan.py .`
  revisa todos los refs y blobs alcanzables, sin imprimir valores. En el commit de esta revisión
  examinó 1.354 objetos, 1.062 blobs (775 de texto, 287 binarios omitidos), sin
  hallazgos con los patrones del hook. No cubre objetos inalcanzables, binarios,
  formatos desconocidos ni contenido cifrado; la ausencia de hallazgos no prueba
  que no existan credenciales.
- **Rotación:** si una credencial estuvo expuesta, bórrala del árbol no basta.
  El propietario debe revocarla y rotarla en el proveedor, revisar su uso y
  actualizar los gestores de secretos. Este repo no puede verificar la rotación.
- **Dependencias y código de terceros:** revisa fuente, scripts de instalación,
  licencia y versión fijada antes de ejecutar. No ejecutes `npx @latest`, `curl |
  bash` ni instaladores sin revisión; usa lockfiles y permisos mínimos.
- **Sandbox y aprobaciones:** se configuran en cada cliente. Las instrucciones y
  filtros por patrón no son una barrera. Para autonomía, usa un entorno
  desechable, red restringida, permisos mínimos y aprobación de comandos.
- **Protección de `main`:** la API de protección y rulesets devolvió 403 por
  límites del plan/permisos, así que no se pudo verificar desde aquí. El
  propietario debe activar la protección en GitHub y revisar revisiones
  obligatorias y quién puede fusionar. No se afirma que esté habilitada.

Los detalles operativos de la revisión están en `knowledge/decisions.md`.
