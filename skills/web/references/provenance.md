# Procedencia y alcance de la integración web

Skill `web` como entrada única (2026-11-15). No mueve directorios: los cuatro
módulos viven en su sitio como **módulos internos** del canon (no se enlazan
como skills públicas), como en `video`. Contenido propio sin reescritura.

- `charli-design` (fusión propia 2026-10-31): taste-skill (Leonxlnx @ `12af471f`, MIT; ver `skills/charli-design/LICENSE-upstream`) + Impeccable/frontend-polish (upstream actual declara Apache-2.0; versión exacta vendorizada no verificada). Es el núcleo anti-slop y de marca CHARLI; su procedencia detallada está en `skills/REGISTRO.md` ("Adopciones propias").
- `web-animation`: skill del canon (Framer Motion y GSAP). Origen exacto no verificado; se conserva con nota en REGISTRO pendiente de atribución. Añadido el 2026-11-15 el corpus nativo `references/platform/` (Modern Web Guidance de Google Chrome, Apache-2.0; `LICENSE-modern-web-guidance.txt` incluido). Actualizado selectivamente el 2026-11-22 de v1.0.0 (`4dd968349e54ca45a05dd5c818fb035c9054b022`) a v1.0.1 (`64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65`): las mismas 16 guías vendorizadas siguen copiadas verbatim, y dos guías de motion/scroll se reemplazaron completas; el resto del corpus no está incluido y su consulta exige red y autorización (ver `platform/README.md`).
- `3d-web-designer`: `vibeship-spawner-skills` (Apache-2.0, indicada en su frontmatter). Se conserva verbatim como módulo; no se ha auditado el upstream completo.
- `scroll-film-studio`: fuente y licencia **no verificadas**; se conserva como módulo interno y no se expone como skill pública. Verificar antes de cualquier distribución externa.

Los módulos fueron revisados estáticamente de forma parcial, no auditados ni
probados de extremo a extremo. Ningún servicio, MCP, dependencia ni binario se
instala por esta integración. `npx`/`pnpx` y red quedan fuera del flujo salvo
autorización explícita (ver `platform/README.md` y la skill `web`).
