# Evaluación de vídeo: protocolo reproducible

Objetivo: comparar resultados con y sin el harnés sin inventar métricas. La
evaluación mide el resultado observable y el coste, no la preferencia del autor.

## Condiciones

- Misma versión de cliente y modelo en A (base, sin skills del harnés) y B (con
  el harnés), mismos permisos, red, resolución y duración objetivo.
- Prompts idénticos y entregados sin edición posterior. Tres repeticiones por
  celda; si el coste lo impide, una y se declara.
- Activos con derechos verificados; no se usan pistas de `brag/assets/music`
  hasta aclarar su licencia. Nada de datos personales ni material de clientes.
- Registro previo de versión, fecha, sistema, Node/FFmpeg, tiempo y tokens o
  coste. Sin FFmpeg instalado, los renders deben declararse no verificados.

## Cuatro tareas

1. **Motion explainer (16:9, 20–30 s):** concepto abstracto con 3 escenas,
   transiciones, texto legible y una idea por escena.
2. **Reel vertical (9:16, 15–20 s):** gancho en 2 s, subtítulos seguros, ritmo
   y encuadre para móvil.
3. **Promo de producto (1:1 o 16:9):** producto, beneficio, CTA; sin marcas ni
   afirmaciones no comprobadas.
4. **Edición de un vídeo existente:** recortar, subtitular y sustituir audio
   conservando sincronía; se documenta el material de origen.

## Rúbrica (0–4 por criterio)

- **Corrección:** reproduce lo pedido, sin elementos rotos, fuera de lienzo ni
  texto cortado.
- **Calidad visual:** composición, jerarquía, tipografía, color y motion con
  intención; sin slop evidente.
- **Audio y sincronía:** voz/música inteligibles, sin clipping; cortes y
  subtítulos alineados.
- **Portabilidad:** archivo reproducible en el entorno declarado, sin
  dependencias ocultas.
- **Eficiencia:** tiempo y coste para llegar a un resultado aceptable, incluidos
  reintentos.
- **Seguridad y derechos:** sin descargas no autorizadas, telemetría inesperada,
  credenciales ni activos sin licencia.

## Registro

Tabla por tarea y versión: `A/B | repetición | rúbrica | defectos | tiempo |
coste | evidencia (ruta, hash) | estado`. Un vídeo sin reproducción verificada
se marca `no verificado`, no `aprobado`. La decisión se toma con los datos; si
A y B empatan, se conserva la opción con menos superficie de dependencias.

No hay resultados de esta evaluación en el repositorio: requieren un cliente
autenticado, FFmpeg y activos autorizados.
