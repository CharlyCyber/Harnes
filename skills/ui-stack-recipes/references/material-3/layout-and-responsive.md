# Layout y Responsive — Material Design 3

> MD3 introduce **Window Size Classes** (compact/medium/expanded) como framework responsive, reemplazando breakpoints tradicionales. Define **canonical layouts** para organizar contenido.

## Window Size Classes

| Clase | Width | Comportamiento |
|---|---|---|
| **Compact** | 0-599px | Una columna, navegación bottom |
| **Medium** | 600-839px | Dos columnas, navegación rail |
| **Expanded** | 840+ px | Multi-columna, drawer persistente |

### No son Breakpoints Fijos

Las clases son rangos — el layout debe fluir suavemente entre ellas, no saltar abruptamente en puntos específicos. Usar `WindowSizeClass` API:

```kotlin
// Jetpack Compose
val windowSizeClass = currentWindowAdaptiveInfo().windowSizeClass
when (windowSizeClass) {
    WindowWidthSizeClass.COMPACT -> // layout compacto
    WindowWidthSizeClass.MEDIUM  -> // layout medio
    WindowWidthSizeClass.EXPANDED -> // layout expandido
}
```

## Canonical Layouts

### List-Detail (Feed + Detail)

```
Compact:    Medium:         Expanded:
┌──────┐   ┌────┬─────┐    ┌──────┬──────────┐
│ List │   │List│Detail│    │ Nav  │ List     │
└──────┘   └────┴─────┘    │ Rail │ Detail   │
                            └──────┴──────────┘
```

### Supporting Pane

```
Compact:    Medium/Expanded:
┌──────┐   ┌──────────┬──────┐
│ Main │   │  Main    │ Side │
└──────┘   └──────────┴──────┘
```

Side pane es secundario (ej: propiedades, comentarios).

### Multi-pane

3+ paneles simultáneos. Solo en Expanded.

```
┌──────┬──────────┬──────┐
│ Nav  │  List    │Detail│
│ Rail │  Preview │ Edit │
└──────┴──────────┴──────┘
```

## Grid System

Basado en columns + gutter + margin:

| Clase | Columnas | Gutter | Margin |
|---|---|---|---|
| Compact | 4 | 16px | 16px |
| Medium | 8 | 24px | 32px |
| Expanded | 12 | 24px | 24px+ |

## Buenas Prácticas Responsive

- Diseñar para compact primero, luego expandir
- Usar `Spacer` + `Modifier.weight()` en vez de anchos fijos
- La navegación debe adaptarse (no solo ocultarse)
- En compact: un pane a la vez + transition
- En expanded: multi-pane + persistencia de estado
- Preferir `fillMaxWidth(0.5f)` sobre valores fijos en px
- Testing: probar en los 3 rangos ancho + portrait/landscape
