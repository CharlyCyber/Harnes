# Control de calidad

- Verifica solicitud: duración, formato, dimensiones, FPS, orientación, códec, voz/audio/captions y derechos cuando aplique; no inventes requisitos de plataforma.
- Revisa al menos apertura, cierre, zonas de texto, cortes/transiciones y fotogramas representativos de cada plano; inspecciona a tamaño de reproducción y verifica safe areas según plataforma concreta.
- Comprueba que no haya negros inesperados, cortes de sonido, clipping, desincronización, fuentes sustituidas, desbordes ni información sensible. Escucha el resultado cuando haya audio y el entorno lo permita.
- HyperFrames: ejecuta `check` con la versión local fijada si está disponible; respeta sus límites y revisa fotogramas. Edición: inspecciona streams con `ffprobe`, reproduce y revisa cortes cuando se disponga de herramientas. Una validación técnica no sustituye revisión visual/sonora.
- Entrega archivo y datos realmente medidos; indica qué no se pudo probar. No prometas una calidad o compatibilidad no verificada.
