# SFX externos (Freesound y similares)

Idea: los SFX se consiguen fuera del canon, con licencia comprobada, solo
cuando hacen falta y con autorización previa; el canon no incluye bibliotecas
de audio descargadas ni hace peticiones de red por su cuenta.

Protocolo:

1. **Especifica el cue antes de buscar**: plano/acción, fuente o material,
   duración objetivo, ataque y cola, tono y **licencia mínima aceptable**.
   Ejemplo: `paper slide, 0.2–0.8 s, seco, un solo golpe, sin cola, CC0`.
   Busca por fuente real (`paper slide`, `short cinematic impact`), no por
   emoción abstracta ni por `click` genérico.
2. **Licencia por defecto**: CC0; acepta CC BY solo si el usuario aprueba la
   atribución. Nunca BY-NC, Sampling+ ni licencias desconocidas para piezas
   comerciales. Las búsquedas no transfieren licencia: verifícala en la página
   del asset y guarda la URL.
3. **Descarga solo con autorización**: informa qué cue, de qué fuente, licencia,
   tamaño y coste (si lo hay); espera el OK. Descarga a la carpeta del
   proyecto (nunca al canon) y conserva un manifiesto: `audio-manifest.json`
   (id, título, autor, URL, licencia, sha256, bytes) y `FREESOUND-CREDITS.md`
   con la atribución cuando aplique.
4. **Selección**: prefiere fuente limpia y coincidente sobre popularidad
   (4.4 con miles de votos > 4.9 con 6 votos); no inventes cifras; descarta
   grabaciones multi-acción largas salvo recorte justificado. Separa UI de
   foley real según el tono del brief.
5. **Herramienta externa opcional** (bajo autorización): el proyecto
   `video-shotcraft` (Apache-2.0) incluye `assets/scripts/sfx-source.py`
   (Python stdlib, sin API key: busca, descarga, verifica `sha256` y escribe
   créditos/manifest). No está integrado en este canon a propósito: ejecutarlo
   o clonarlo es decisión del usuario por proyecto; revísalo antes (sin
   telemetría, pero hace red) y fija licencia CC0/BY con `--license cc0|by`.
6. **Contraste**: `hyperframes-audio` (mezcla/ducking/buses) y `media-use`
   (resolve de BGM/SFX desde catálogo local/generado) cubren la producción;
   esta referencia solo cubre el aprovisionamiento externo con derechos claros.
   (Sin API key no garantiza estabilidad del servicio: el HTML de Freesound
   puede cambiar; verifica antes de automatizar.)
