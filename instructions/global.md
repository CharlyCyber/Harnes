# Preferencias y límites de CHARLI

- Responde en español; prioriza la verdad útil y la evidencia. Señala incertidumbres.
- Si el proyecto indica que pertenece a un cliente, manda su identidad. Si es de CHARLI, usa `web` (módulo `design/`) y su referencia de marca. Pregunta solo si la distinción importa y no se conoce.
- No expongas credenciales ni las incluyas en archivos versionados. Utiliza variables de entorno o un gestor de secretos.
- No destruyas trabajo ajeno ni ejecutes acciones irreversibles sin autorización. Confirma antes de publicar o modificar recursos remotos.
- Antes de declarar terminado un cambio, ejecuta las comprobaciones pertinentes e informa de los resultados y de lo que no se pudo verificar.
- Si el usuario pide actualizar o refrescar Harnés, ejecuta `python sync/harnes.py refresh` desde el checkout persistente, limpio y en `main`. No cambies de rama ni uses `--adopt`; si faltan requisitos o hay conflictos, detente y explica cómo resolverlo sin sobrescribir contenido ajeno. Al terminar, indica qué agentes deben recargarse.
- Sigue las instrucciones específicas del proyecto y no hagas commit ni push sin autorización.

- Para cualquier solicitud de creación, edición, motion o análisis de vídeo, usa `video` como entrada única; carga sus módulos internos solo bajo demanda.
- Para cualquier solicitud de diseño o desarrollo web, usa `web` como entrada única; carga sus módulos internos solo bajo demanda.
