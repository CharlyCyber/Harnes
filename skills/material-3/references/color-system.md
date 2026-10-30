# Sistema de Color — Material Design 3

> MD3 introduce un sistema de color basado en **tokens** con 5 roles de color clave, cada uno con variantes light y dark. Soporta color dinámico (Material You / Monet) y colores personalizados.

## Roles de Color

| Rol | Uso principal |
|---|---|
| **Primary** | Componentes clave, botones rellenos, active states |
| **Secondary** | Componentes menos prominentes, chips, filtros |
| **Tertiary** | Acento opuesto a primary (complementario), inputs, badges |
| **Neutral** | Fondos, superficies, texto |
| **Neutral Variant** | Superficies elevadas, outlines, texto secundario |
| **Error** | Estados de error, validación |

## Esquema de Color (Light / Dark)

```
primary
onPrimary
primaryContainer
onPrimaryContainer
primaryFixed
primaryFixedDim
onPrimaryFixed
onPrimaryFixedVariant

secondary
onSecondary
secondaryContainer
onSecondaryContainer
secondaryFixed
secondaryFixedDim
onSecondaryFixed
onSecondaryFixedVariant

tertiary
onTertiary
tertiaryContainer
onTertiaryContainer
tertiaryFixed
tertiaryFixedDim
onTertiaryFixed
onTertiaryFixedVariant

error
onError
errorContainer
onErrorContainer

surface
onSurface
surfaceVariant
onSurfaceVariant
surfaceContainerHighest
surfaceContainerHigh
surfaceContainer
surfaceContainerLow
surfaceContainerLowest
surfaceBright
surfaceDim

outline
outlineVariant

shadow
scrim

inverseSurface
inverseOnSurface
inversePrimary
```

## Dynamic Color (Monet)

Algoritmo que genera esquema de color desde un wallpaper:
1. Extrae colores semilla de la imagen
2. Aplica tonal spot colors para cada rol
3. Genera 5 tonos clave por color
4. Produce paletas light y dark automáticamente
5. El usuario puede fijar colores específicos (customization)

### Tonal Spot Colors

```
primary   ← tono más vibrante del color semilla
secondary ← versión más suave (misma familia cromática)
tertiary  ← tono complementario opuesto
neutral   ← versión desaturada del fondo
```

## Tokens de Color

Usar tokens semánticos, no valores fijos:

```kotlin
// ❌ Mal
Box(background = Color(0xFF6750A4))

// ✅ Bien
Box(background = MaterialTheme.colorScheme.primary)
```

```css
/* ❌ Mal */
.button { background: #6750A4; }

/* ✅ Bien */
.button { background: var(--md-sys-color-primary); }
```

## Buenas Prácticas

- Siempre definir esquemas light + dark completos
- Usar `surfaceContainer*` para elevaciones moduladas (no `elevation` en todos lados)
- `outline` para bordes pasivos, `outlineVariant` para bordes sutiles
- `primaryFixed` / `primaryFixedDim` para variantes de contenedor en light mode
- Contraste mínimo 4.5:1 para texto, 3:1 para elementos grandes
