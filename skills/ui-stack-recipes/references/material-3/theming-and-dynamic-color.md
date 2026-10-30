# Theming y Dynamic Color — Material Design 3

> MD3 introduce un sistema de theming basado en **tokens de diseño** que abarca color, tipografía, forma, elevación y motion. El dynamic color (Monet) genera esquemas automáticos desde una imagen.

## Arquitectura de Theming

```
Theme
├── colorScheme      (light / dark / dynamic)
├── typography       (type scale, font families)
├── shapes           (shape scale)
└── tokens           (M3 tokens: elevation, motion, state)
```

## Dynamic Color (Material You)

### Algoritmo Monet

1. **Extracción**: toma colores dominantes del wallpaper
2. **Seed color**: el color más representativo como semilla
3. **Tonal palette**: genera 13 tonos por color (0-100 luminosidad)
4. **Roles**: asigna tonos específicos a cada rol cromático
5. **Esquemas**: produce light + dark automáticamente

### Implementación

```kotlin
// Jetpack Compose — Dynamic Color
val colorScheme = when {
    Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
        val context = LocalContext.current
        if (darkTheme) dynamicDarkColorScheme(context)
        else dynamicLightColorScheme(context)
    }
    else -> if (darkTheme) darkColorScheme() else lightColorScheme()
}
```

```flutter
// Flutter — Dynamic Color
final colorScheme = ColorScheme.fromSeed(
  seedColor: seedColor,
  brightness: brightness,
);
```

```css
/* Web — CSS Custom Properties */
:root {
  --md-sys-color-primary: #6750A4;
  --md-sys-color-on-primary: #FFFFFF;
  /* ... todos los tokens del esquema */
}
```

### Light / Dark

Ambos esquemas deben definirse — el sistema alterna según preferencia del usuario o manualmente.

| Propiedad | Light | Dark |
|---|---|---|
| surface | `#FFFBFF` (light) | `#1C1B1F` (dark) |
| primary | vibrante | versión más clara |
| shadow | visible | sutil (elevación invertida) |

## Tokens de Diseño

### Elevation

| Nivel | Uso |
|---|---|
| 0 | Surface base |
| 1 | Cards, Navigation Bar |
| 2 | FAB (resting), Search |
| 3 | FAB (pressed), Menu, Dialog |
| 4 | Navigation Drawer, Modal Bottom Sheet |
| 5 | Snackbar, Date Picker |

En dark mode, la elevación se representa con surfaceContainer (brightness inversa), no sombras.

### Motion Tokens

| Token | Duración | Easing |
|---|---|---|
| `motion-duration-short1` | 100ms | `emphasized-accelerate` |
| `motion-duration-short2` | 200ms | `emphasized-decelerate` |
| `motion-duration-medium1` | 300ms | `emphasized-accelerate` |
| `motion-duration-medium2` | 400ms | `emphasized-decelerate` |
| `motion-duration-long1` | 500ms | `standard` |
| `motion-duration-long2` | 600ms | `standard` |

### State Layers

Los componentes usan state layers para hover, focus, press y drag.

| Estado | Opacidad (light) | Opacidad (dark) |
|---|---|---|
| Hover | 8% | 8% |
| Focus | 12% | 12% |
| Press | 12% | 24% |
| Drag | 16% | 16% |

## Buenas Prácticas

- No mezclar dynamic color con paletas customizadas — elegir uno
- En dark mode, evitar sombras — usar surfaceContainer para elevación
- Probar esquemas generados en condiciones reales de luz ambiente
- Incluir opción manual de tema si usas dynamic color
- Los tokens deben ser consistentes cross-platform
