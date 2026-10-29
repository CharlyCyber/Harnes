# Registro de Fallos (el trinquete)

Cada fallo del agente (del Agente Universal o de este harnés) queda registrado aquí y, si procede, se convierte en una regla en AGENTS.md, un hook o una skill. Sin evidencia no se añade regla.

## 2026-10-29 — Postmortem del Agente Universal

| Fallo observado | Causa raíz | Mitigación adoptada |
|---|---|---|
| Mover/renombrar el proyecto rompió todo: AGENTS.md, skills, configs de Gemini/Kilo/DSH con rutas muertas. | Rutas absolutas en archivos copiados/vendoreados. | Regla 9 de AGENTS.md: solo rutas relativas. |
| El sync dejaba rastros en múltiples destinos (skills duplicadas en 3 ubicaciones, bundles cacheados) y la limpieza fue laboriosa. | El sync no era idempotente ni tenía un registro de lo instalado. | Pendiente: sync determinista e idempotente, con ledger de lo instalado (sync/). |
| Catálogo de 27 skills inflando el contexto antes del primer agente en actuar. | Skills sin justificación de comportamiento. | Catálogo inicial vacío; cada skill futura justifica el comportamiento que entrega. |
| Sin capa anti-destruccion: una limpieza global pudo dañar trabajo irreemplazable. | Cero hooks de seguridad. | Regla 10 (custodia de proyectos); hook destructivo cuando existan hooks. |
| Desconocimiento de dónde estaba instalado qué (skills viviendo en 3 ciudades). | Sin fuente única de verdad. | Este repo es canónico; las copias son derivadas reproducibles con sync. Si se rompe el canon, reconstruir limpio. |
