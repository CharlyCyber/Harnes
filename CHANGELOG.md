# Cambios

## Sin publicar

- Comando `refresh` para agentes: valida el canon, hace fast-forward solo desde
  `main` con checkout limpio y sincroniza únicamente enlaces/instrucciones
  gestionados por Harnés. No cambia de rama ni usa `--adopt`; ante conflictos,
  se detiene y conserva las rutas afectadas. Las instrucciones globales enseñan
  a los agentes a ejecutar este flujo cuando el usuario pide "actualiza Harnés".
- Config MCP de OpenCode migrada a sintaxis V2 y documentada: servidores en
  `mcp.servers`, credenciales con `{env:VAR}` y `disabled` en lugar de
  `enabled`. `apify` vuelve al catálogo (el formato V1 dejaba el token literal)
  y `firecrawl` sale del inventario por egress bloqueado.
  `config/opencode.example.json` refleja la forma válida y `knowledge/mcps.md`
  explica la diferencia.
- Craft Anything documentado como alternativa opt-in (rebuild+check, early
  alpha): puntero en `reverse-engineer-anything/SKILL.md`, inventario opcional
  en `config/mcp.json` y nota con estado `no verificado` en
  `knowledge/mcps.md` (sección "Candidatos y opcionales"). No adoptado ni
  instalado por el canon; REA sigue siendo el motor de evidencia.
- `web` como entrada única de diseño/desarrollo web: consolida `charli-design`,
  `web-animation`, `3d-web-designer` y `scroll-film-studio` como módulos
  internos bajo demanda (sin mover directorios); test previo web (tipo/estilo,
  stack, marca, a11y, performance, probe) y guías nativas Baseline vendorizadas
  de Modern Web Guidance de Google Chrome (Apache-2.0,
  `web-animation/references/platform/`). `core` pasa a 12 skills; `all`, 16.
- `cavecrew` retirada: solapaba parcialmente con `caveman` y carecía de sus tres
  subagentes; `caveman` se conserva y la diferencia queda documentada.
- Init de HyperFrames limitado a un lanzador local verificado para `0.9.33`, sin
  `npx`, actualización de skills ni telemetría; versión distinta se rechaza.
- Sonda de descubrimiento de Codex sin credenciales y matriz de compatibilidad
  con evidencia y límites; Claude Code queda pendiente de sesión.
- Escáner de todo el historial alcanzable sin imprimir secretos y lista de
  seguridad/rotación; procedencia con commits y música de `brag` bloqueada.

- `video` como entrada única de vídeo en core y all: módulos internos bajo demanda,
  referencias de motion y edición, y generador opcional de trazos SVG locales.
  Migración conservadora de enlaces antiguos; fuentes y licencias documentadas.

- Sincronización multiplataforma con enlaces por skill, perfiles y protección del
  contenido ajeno; migración optativa con respaldos e inventario de propiedad.
- Instrucciones globales separadas de la guía de este repo y fusionadas por bloque.
- Validación real del formato de skills, comprobación de secretos del índice y
  remotes, hook opcional y pruebas aisladas en CI multiplataforma.
- Marca dentro de la skill de diseño; `cavecrew` quedó dormida hasta su retirada (véase arriba).
- MCP y permisos opcionales documentados, sin sustituir configuraciones existentes.

## 0.4 y anteriores

Véanse `knowledge/decisions.md` y el historial de Git.
