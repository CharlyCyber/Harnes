# Registro del Catálogo

Estado: **16 skills públicas**; `core` activa 12, `all`, 16. Los módulos internos se conservan en el canon sin enlazarse como skills públicas: 15 de vídeo y 4 de web (`charli-design`, `web-animation`, `3d-web-designer`, `scroll-film-studio`). Parte de la procedencia y licencias sigue pendiente de verificar.

## Adopciones propias

| Skill | Fuente / commit | Licencia | Comportamiento justificado |
|---|---|---|---|
| `charli-design` (módulo `design/` de `web`) | Fusión propia (2026-10-31): taste-skill (Leonxlnx @ `12af471f`) + Impeccable (pbakaus, derivado vendored) | MIT de taste (`LICENSE-upstream`); el upstream actual de Impeccable declara Apache-2.0, pero no se verificó la versión exacta vendorizada | Núcleo anti-slop: dirección de arte, bibliotecas de paletas/tipo, leyes de pulido (tipografía, OKLCH, motion físico) y verificación en navegador. |
| `find-skills` | vercel-labs/skills @ `57217cf86ba38148a57af9e90d14a4c049558330` (HEAD 2026-11-17; antes `92a9a34a`) | MIT (`skills/find-skills/LICENSE-upstream`) | Descubrir skills a demanda. Se conserva la adaptación Harnes que bloquea auto-confirmación e instalación global recomendadas por upstream. |

## Video unificado (2026-11-10)

`video` es la entrada única en ambos perfiles. Enruta edición, reels, análisis y
motion; consulta bajo demanda los 12 módulos HyperFrames, `video-use`,
`analizar-videos` y `brag` como referencias internas. Ninguno se expone por
separado mediante sync. La integración incorpora principios seleccionados de
Bang Motion y Huashu y un pequeño generador local de SVG inspirado por la idea
procedimental de Claude Drawing; no incluye los repos completos ni sus assets.
Commits, alcance y licencias: `video/references/provenance.md`. El router limita
instalaciones, actualización automática, servicios externos y marca de agua.
Se requiere verificar en cada proyecto las herramientas, derechos y resultados.

## Video unificado — ampliación (2026-11-15)

Se mantiene `video` como única skill de vídeo (14 en `core`; entrada única). Se
añaden cuatro referencias compactas bajo demanda: `beat-sync.md` (método de
cortar al ritmo adaptado de `video-shotcraft` @ `6700db2b`, Apache-2.0),
`sfx-sourcing.md` (especificación de cues y aprovisionamiento externo con
licencia CC0/BY; sin código vendorizado), `preflight-test.md` (test previo:
brief + entorno + render probe) y `lemo-opuscar.md` (puntero externo, sin
copiar docs CC BY-NC). `motion.md` gana una nota 3D/WebGL (adapter three del
canon; three.js MIT v0.187.0 no vendorizado; R3F descartado por alcance).
Ningún servicio, dependencia ni audio nuevo se instala; nada se registró como
skill pública. Procedencia y licencias: `video/references/provenance.md`.

## Video unificado — réplica de motion (2026-11-22)

Se amplía la única entrada `video` con `references/reverse-animation.md` y
herramientas locales vendorizadas desde `NiazMorshed2007/reanimate` @
`3f7a55a2986a84ca2173e86ee9127eefe31d046d` (MIT): captura DOM/canvas/WebGL,
extracción de fotogramas, ajuste de easing, comparación por fotograma y hojas
etiquetadas. Orientado a reconstrucción de animación de referencia con
especificación y evidencia; no sustituye los flujos existentes de creación,
edición o promo. El setup es optativo y protegido por confirmación de permiso;
no se instalaron dependencias al integrar. Ninguna nueva skill pública ni
cambio de perfiles. Procedencia, límites de revisión y aviso MIT:
`video/references/provenance.md` y `video/licenses/reanimate-MIT.txt`.

## Web unificada (2026-11-15)

`web` es la entrada única en `core` y `all` para diseño y desarrollo web.
**No mueve directorios**: `charli-design`, `web-animation`, `3d-web-designer`
y `scroll-film-studio` pasan a ser módulos internos del canon (como los de
vídeo) y se enlazan solo vía el router `web`. Añade `web/references/preflight-test.md`
(test previo web: tipo/estilo, stack, marca, a11y, performance, probe).
`web-animation` incorpora `references/platform/`: 16 guías verbatim de Modern
Web Guidance (Google Chrome, Apache-2.0, `GoogleChrome/modern-web-guidance` @
`64a6d708`, corpus `modern-web-guidance@1.0.1`) de motion nativo Baseline; el
resto del corpus no está incluido ni se consulta sin autorización. Provenance:
`web/references/provenance.md`. `chrome-devtools-mcp` (referencia de inventario/configuración contrastada con Apache-2.0 upstream @ `ab911a6dd71ed4960c1c679f831c7b5607bc5505`, 2026-11-21) y `context7` se mantienen
fuera de la fusión (MCP/transversal, no conocimiento de construcción).

## Stack HyperFrames — módulos internos (12)

Instaladas vía CLI de skills en su adopción histórica (`~/.agents/.skill-lock.json`, v3); upstream `heygen-com/hyperframes`, plugin `core-skills`. Versiones iniciales registradas entre 2026-09-29 y 2026-10-05. El 2026-11-22 se actualizaron por archivo las referencias comunes verificadas contra HEAD `79e43a33a87dc3b178c7969c6ceaae7efd33b8b4` (Apache-2.0; aviso en `skills/hyperframes/LICENSE-upstream`): docs de CLI/registry, referencias de media y port Remotion, launcher y pruebas. Se retuvieron los routers Harnes, módulos y referencias locales que upstream retiró o reestructuró. El launcher añade la política Harnes: no instalar skills, ejecutar npm fuera del proyecto y bloquear subcomandos de gestión de skills.

| Skill | Rol |
|---|---|
| `hyperframes` | Router upstream consultado para composiciones HyperFrames; `video` tiene prioridad |
| `hyperframes-core` | Contrato de composición HTML + timing |
| `hyperframes-cli` | init / check / preview / render / publish |
| `hyperframes-animation` | Motion atómico, blueprints, runtimes |
| `hyperframes-audio` | Mezcla, ducking, efectos, buses |
| `hyperframes-creative` | Dirección creativa, paletas, narración, beats |
| `hyperframes-keyframes` | Zooms, reframes, máscaras, morph |
| `hyperframes-registry` | Bloques y componentes del registro |
| `hyperframes-studio` | Flujo de trabajo en Studio |
| `media-use` | BGM, SFX, TTS, voz, LUTs, captions |
| `general-video` | Composiciones libres y montajes |
| `remotion-to-hyperframes` | Port de Remotion (solo ese caso) |

## Herramientas con upstream declarado (6)

| Skill | Fuente | Licencia |
|---|---|---|
| `web-animation` (`references/platform/`) | GoogleChrome/modern-web-guidance @ `64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65` (v1.0.1; antes `4dd968349e54ca45a05dd5c818fb035c9054b022`, v1.0.0) | Apache-2.0 (`web-animation/references/platform/LICENSE-modern-web-guidance.txt`); selección fija de 16 guías; dos guías sustituidas verbatim el 2026-11-22; solo motion/scroll/transitions |
| `brag` | latent-spaces/brag @ `06379432a9243c951dfcc051153be18d2d261044` (HEAD observado 2026-11-22; actualización selectiva desde base declarada `fd7de7e418334876b3ea4e9258231a66a2c2a38d`) | MIT para código (`LICENSE.upstream`); música Sascha Ende CC BY 4.0, atribución “Music: Sascha Ende, ende.app (CC BY 4.0)” según upstream README. Cambios funcionales seleccionados portados sin sobrescribir adaptación Harnés. |
| `last30days` | mvanhorn/last30days-skill @ `e63f8e8732f1b934449b363f211b3654531b8ef2` (v4.5.0, HEAD 2026-11-21) | MIT (`skills/last30days/LICENSE-upstream`) | Guía Harnes compacta y segura; el motor upstream no se vendoriza y no se afirma que sus capacidades estén disponibles. Hash del material histórico previo no verificado. |
| `reverse-engineer-anything` | morluto/rea @ `e726f89bcb5d07af5699301856454aff9416d482` (HEAD 2026-11-22) | MIT (`skills/reverse-engineer-anything/LICENSE-upstream`) | Skills y referencias sincronizados al upstream actual; usar solo herramientas anunciadas por la conexión. |
| `video-use` | `browser-use/video-use` @ `43cfc566833548093455c9d4a46bd69913b7e552` (HEAD 2026-10-08) | MIT (`skills/video-use/LICENSE-upstream`); scripts locales adicionales no verificados | Se portaron reglas de privacidad y seguridad del upstream. El árbol local y sus scripts no coinciden con el checkout actual; no se reemplazaron. |
| `security-audit` | Fusión 2026-11-05: checklist de 19 puntos propio + motor `nfaudit` de notfound404es/notfound-security-audit @ `c5d7c0e` | MIT (`LICENSE-upstream`) |

**`security-audit` — qué se fusionó:** se conserva el checklist propio de 19 puntos (P1–P19) y `scripts/audit.py` y `scripts/history_scan.py` (historial de git; el motor externo no lo cubre). Se incorporó el escáner `nfaudit` (stack, dependencias, patrones de inyección, configs, Docker, CI, runtimes), su base de reglas (`rules/`, 40 KB), los avisos locales (`data/`), las tres referencias (`references/`) y su licencia. Auditoría del código antes de adoptarlo: stdlib puro, sin `eval`/`exec`/`pickle`; red solo a `api.osv.dev` (opt-in `--osv`) y una petición GET a un dominio del usuario (opt-in `headers`). No se adoptó ninguna otra skill de los repos evaluados.

`craft-anything` (`storytold/craft-anything` @ `2e7dfa5e`): **documentada, no adoptada ni instalada**. Alternativa opt-in a REA para rebuild+check (webs/apps/juegos, ~320 tools CLI+MCP, MIT OR Apache-2.0, **early alpha**); puntero en `reverse-engineer-anything/SKILL.md`, inventario opcional en `config/mcp.json`, estado `no verificado` en `knowledge/mcps.md`. No se vendoriza; no se modifica ninguna config MCP.

## Stack base heredado (15; cavecrew retirada)

Sin upstream verificado todavía; provienen del stack anterior y se conservan por uso real. **Antes de modificar una, registrar su fuente.** Las entradas `3d-web-designer`, `scroll-film-studio` y `web-animation` se conservan como módulos internos de `web` (ver "Web unificada"); siguen sin upstream verificado.

`3d-web-designer`, `advanced-scraping`, `analizar-videos`, `caveman`, `chrome-devtools-mcp`, `context7`, `git-advanced-workflows`, `github-integration`, `mobile-design`, `no-mistakes`, `scroll-film-studio`, `ship`, `triage`, `video-use`, `web-animation`.

## Retiradas

| Fecha | Skill(s) | Razón |
|---|---|---|
| 2026-11-10 | `cavecrew` | Retirada a petición del usuario: solapa parcialmente con la compresión de `caveman`; no era idéntica, ya que se centraba en delegar a tres subagentes que faltaban. Estaba dormida. |
| 2026-11-05 | 47 skills de `.kilocode` (30 exclusivas) | Eliminación completa de Kilocode por decisión del operador. 12 de esas 30 eran junctions colgantes a `~/.agents/skills` (ya inexistentes). Backup: `Documents\Backups\kilocode-backup-20261105.zip` (5,5 MB, 704 entradas). |
| 2026-10-31 | `ui-ux-pro-max`, `web-design-pipeline`, `web-design-strategist`, `shadcn`, `material-3`, `ui-stack-recipes`, `headroom` | Dormidas sin uso; absorbidas por `charli-design` + docs. |
| 2026-10-31 | `design-taste-frontend`, `frontend-polish` | Fusión en `charli-design`. |

## Procedencia y cuarentena

Cada skill adoptada debe registrar: fuente y URL, commit/tag o versión exacta,
licencia (archivo y fecha de consulta), archivos o directorios vendorizados,
hash de la copia local si se modificó, dependencias y comandos que ejecuta. Lo
que no se haya verificado se marca **desconocido**; no se deduce del README ni de
la licencia del repo anfitrión.

Antes de usar material dudoso: aíslalo, no lo sincronices a perfiles ni lo
redistribuyas, revisa scripts y binarios, y pide autorización. Una licencia de
código no cubre automáticamente fuentes, música, imágenes, marcas ni datos de
terceros. Para retirar una skill, elimina su directorio del canon, actualiza
`targets.json`, este registro y las referencias, y ejecuta `sync` y `doctor`;
los enlaces inventariados se retiran, pero copias ajenas pueden permanecer.

## Notas de mantenimiento

- **Bug de vendoreo corregido (2026-11-05):** 18 skills del árbol de OpenCode tenían una copia anidada de sí mismas (`skill/skill/`), duplicando su peso. El canon se reconstruyó sin anidados y `doctor.ps1` falla si reaparecen.
- **`brag`:** la música de Sascha Ende se documenta como CC BY 4.0, con atribución obligatoria según `skills/brag/assets/music/README.md`; la licencia de la música es independiente de la MIT del código. Pesaba 31,6 MB por la copia anidada; quedó en 15,8 MB. Los MP3 de `assets/music` se conservan porque son parte real de la skill (BGM del vídeo de lanzamiento). Si el repo crece demasiado, el siguiente paso es Git LFS, no borrar la música.
- **Diferidas:** `security-audit` de Cloudflare ya está instalada; se reevalúa en el primer proyecto cliente. `browser-testing-with-devtools` y `frontend-ui-engineering` (addyosmani) siguen en la lista de candidatas.
