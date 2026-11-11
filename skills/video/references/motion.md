# Motion y dirección visual

Aplicar según el brief; no son efectos obligatorios. Mantener la composición determinista y seguir el contrato de `hyperframes-core` al usar HyperFrames.

1. **Una idea visual**: define mensaje, sujeto, audiencia, duración y un arco de apertura-desarrollo-cierre. Planifica beats y jerarquía antes de añadir efectos. Cada plano debe comunicar una idea en un tiempo legible.
2. **Continuidad antes que diapositivas**: cuando tenga sentido, conserva uno o dos elementos protagonistas entre escenas y cambia su estado, escala o posición; usa el corte cuando sirva mejor a la narración. No encadenes por defecto páginas idénticas de texto con fade.
3. **Cámara motivada**: piensa en un espacio continuo y en un objetivo por movimiento (revelar, comparar, seguir, enfatizar). Planea escala, encuadre, trayectoria y ritmo de entrada/salida. Limita los movimientos simultáneos; evita mareo, recortes involuntarios y zooms sin propósito.
4. **Tipografía cinética**: destaca palabras importantes siguiendo significado y ritmo de voz o música; mantén contraste, tamaños legibles y tiempos suficientes para leer. Respeta el formato y zonas de interfaz de la plataforma.
5. **Storyboard ligero**: anota por beat el plano, duración, sujeto, acción, texto, sonido si procede y un fotograma de control. Para UI verifica estado real, fidelidad de capturas y privacidad; representa el cursor solo si aporta claridad.
6. **Construcción**: jerarquía, profundidad y materialidad antes de adornos. Usa easing coherente, entradas y salidas coordinadas, y variación de ritmo. Nunca sacrifiques claridad por densidad.
7. **Render reproducible**: fuentes y medios locales/licenciados; movimiento consultable por tiempo, sin reloj en tiempo real ni azar sin semilla. Para HyperFrames usa `data-composition-id`, clases/atributos temporales y una timeline pausada en `window.__timelines`, conforme a `hyperframes-core`. El contrato `window.OPENER` de Bang Motion no es interoperable sin adaptación.
8. **Revisión visual**: inspecciona el primer y último frame, antes y después de cortes y transiciones, momentos de texto y puntos de máxima cercanía a bordes. Comprueba que no hay parpadeos, colisiones ni planos vacíos inesperados.

Adaptación original de ideas generales de Bang Motion (cámara, continuidad y anti-PPT) y Huashu Design (storyboard y revisión); fuentes y licencias en `provenance.md`. No incluye sus starters ni scripts.
