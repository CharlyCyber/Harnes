# Registro del Catálogo

Estado: **19 skills públicas** y 15 módulos internos de vídeo; `cavecrew` dormida por dependencias ausentes. `core` activa 14; `all`, 19. Los módulos internos se conservan en el canon sin enlazarse como skills públicas. Parte de la procedencia y licencias sigue pendiente de verificar.

## Adopciones propias

| Skill | Fuente / commit | Licencia | Comportamiento justificado |
|---|---|---|---|
| `charli-design` | Fusión propia (2026-10-31): taste-skill (Leonxlnx @ `12af471f`) + Impeccable (pbakaus, derivado vendored) | MIT (LICENSE-upstream de taste) | Núcleo anti-slop: dirección de arte, bibliotecas de paletas/tipo, leyes de pulido (tipografía, OKLCH, motion físico) y verificación en navegador. |
| `find-skills` | vercel-labs/skills @ `92a9a34a` | MIT | Descubrir/instalar skills del ecosistema a demanda sin inflar el catálogo. |

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

## Stack HyperFrames — módulos internos (12)

Instaladas vía CLI de skills (`~/.agents/.skill-lock.json`, v3); upstream `heygen-com/hyperframes`, plugin `core-skills`. Versiones registradas entre 2026-09-29 y 2026-10-05.

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

## Herramientas con upstream declarado (4)

| Skill | Fuente | Licencia |
|---|---|---|
| `brag` | latent-spaces/brag @ `fd7de7e4` | MIT para código (`LICENSE.upstream`); licencia de música pendiente de verificar |
| `last30days` | mvanhorn/last30days-skill | — |
| `reverse-engineer-anything` | morluto/rea | — |
| `security-audit` | Fusión 2026-11-05: checklist de 19 puntos propio + motor `nfaudit` de notfound404es/notfound-security-audit @ `c5d7c0e` | MIT (`LICENSE-upstream`) |

**`security-audit` — qué se fusionó:** se conserva el checklist propio de 19 puntos (P1–P19) y `scripts/audit.py` (incluye la pasada de secretos sobre el historial de git, que el motor externo no hace). Se incorporó el escáner `nfaudit` (stack, dependencias, patrones de inyección, configs, Docker, CI, runtimes), su base de reglas (`rules/`, 40 KB), los avisos locales (`data/`), las tres referencias (`references/`) y su licencia. Auditoría del código antes de adoptarlo: stdlib puro, sin `eval`/`exec`/`pickle`; red solo a `api.osv.dev` (opt-in `--osv`) y una petición GET a un dominio del usuario (opt-in `headers`). No se adoptó ninguna otra skill de los repos evaluados.

## Stack base heredado (16; cavecrew dormida)

Sin upstream verificado todavía; provienen del stack anterior y se conservan por uso real. **Antes de modificar una, registrar su fuente.**

`3d-web-designer`, `advanced-scraping`, `analizar-videos`, `cavecrew`, `caveman`, `chrome-devtools-mcp`, `context7`, `git-advanced-workflows`, `github-integration`, `mobile-design`, `no-mistakes`, `scroll-film-studio`, `ship`, `triage`, `video-use`, `web-animation`.

## Retiradas

| Fecha | Skill(s) | Razón |
|---|---|---|
| 2026-11-05 | 47 skills de `.kilocode` (30 exclusivas) | Eliminación completa de Kilocode por decisión del operador. 12 de esas 30 eran junctions colgantes a `~/.agents/skills` (ya inexistentes). Backup: `Documents\Backups\kilocode-backup-20261105.zip` (5,5 MB, 704 entradas). |
| 2026-10-31 | `ui-ux-pro-max`, `web-design-pipeline`, `web-design-strategist`, `shadcn`, `material-3`, `ui-stack-recipes`, `headroom` | Dormidas sin uso; absorbidas por `charli-design` + docs. |
| 2026-10-31 | `design-taste-frontend`, `frontend-polish` | Fusión en `charli-design`. |

## Notas de mantenimiento

- **Bug de vendoreo corregido (2026-11-05):** 18 skills del árbol de OpenCode tenían una copia anidada de sí mismas (`skill/skill/`), duplicando su peso. El canon se reconstruyó sin anidados y `doctor.ps1` falla si reaparecen.
- **`brag`:** pesaba 31,6 MB por la copia anidada; quedó en 15,8 MB. Los MP3 de `assets/music` se conservan porque son parte real de la skill (BGM del vídeo de lanzamiento). Si el repo crece demasiado, el siguiente paso es Git LFS, no borrar la música.
- **Diferidas:** `security-audit` de Cloudflare ya está instalada; se reevalúa en el primer proyecto cliente. `browser-testing-with-devtools` y `frontend-ui-engineering` (addyosmani) siguen en la lista de candidatas.
