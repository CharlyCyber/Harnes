# Edición de metraje, reels y cine

1. Inspecciona los archivos originales sin modificarlos: duración, FPS, resolución, orientación, audio, rotación y posibles tasas variables con `ffprobe` si existe. Revisa algunos fotogramas y escucha rangos representativos; no atribuyas contenido que no viste/escuchaste.
2. Aclara el objetivo y la plataforma; organiza un mapa de tomas y selecciona momentos fuertes. Para voz, una transcripción local o autorizada ayuda a localizar cortes, pero no reemplaza la revisión visual ni es requisito para un montaje musical.
3. Diseña el ritmo: gancho acorde al encargo, progresión, pausas, continuidad de mirada y movimiento, y cierre. Usa cortes en acción o sonido cuando ayuden; evita transiciones gratuitas. El plano debe tener tiempo para leerse.
4. Para vertical, reencuadra cada toma por sujeto y movimiento, no recortes el centro a ciegas. Protege texto y rostros de la interfaz de la plataforma; revisa en el tamaño real. Para horizontal o cuadrado conserva la intención de encuadre.
5. Corrige exposición y balance antes del look. Ajusta entre tomas, conserva detalle y tonos de piel; no prometas HDR ni apliques LUTs sin verificar compatibilidad y derechos. Comprueba flicker y banding.
6. Si hay audio, evita pops y cortes bruscos, nivela inteligibilidad de voz, música y efectos, revisa estéreo y clipping. Si es silencioso, respeta el silencio. No impongas música, narración, captions o marca de agua. Asegura derechos de música y footage.
7. Los subtítulos solicitados deben reflejar lo dicho, ser legibles, estar sincronizados y en safe areas. Revisa nombres y palabras dudosas; no confundas una transcripción automática con verdad.
8. Produce una lista de cortes o proyecto reproducible cuando el alcance lo justifique; exporta en formato, dimensiones y FPS solicitados. Evita reescribir originales. Verifica duración, streams, primer/último frame, cortes y reproducción del archivo final.

FFmpeg y ffprobe son opcionales según el entorno. Si faltan, explica la limitación; no ejecutes instalaciones sin autorización. No envíes material a una API sin consentimiento.
