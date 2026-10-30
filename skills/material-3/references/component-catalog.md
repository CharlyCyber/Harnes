# Catálogo de Componentes — Material Design 3

> Componentes MD3 organizados por categoría. Cada componente especifica tokens de color, tipografía, forma y estados.

## Action

| Componente | Variantes | Tokens Clave |
|---|---|---|
| **FAB** | Normal, Small, Large, Extended, Surface | primary/tertiary container, elevation 3→6 |
| **Icon Button** | Standard, Outlined, Filled, Filled+Tonal | onSurface variant, state layer |
| **Button** | Text, Outlined, Filled, Filled+Tonal, Elevated | primary/surface containers |

## Communication

| Componente | Variantes | Tokens Clave |
|---|---|---|
| **Badge** | Normal, Large | error, onError |
| **Snackbar** | Standard | inverseSurface, inverseOnSurface |
| **Dialog** | Alert, Simple, Full-screen | surface, onSurface, scrim |

## Containment

| Componente | Variantes | Tokens Clave |
|---|---|---|
| **Card** | Elevated, Filled, Outlined | surface/outline, shape medium |
| **Sheet** | Bottom Sheet, Side Sheet | surface, surfaceTint |
| **List** | Single-line, Two-line, Three-line | onSurface, variant |
| **Divider** | Full, Inset, Middle, Subheader | outlineVariant |

## Navigation

| Componente | Tokens Clave |
|---|---|
| **Navigation Bar** | 3-5 items, surfaceContainer, primary/secondary |
| **Navigation Rail** | 3-7 items, surfaceContainer, icon+label |
| **Navigation Drawer** | Modal / Standard, surfaceContainer, scrim |
| **Top App Bar** | Center-aligned / Small / Medium / Large |
| **Search** | Full, Docked, Dialog expandable |
| **Tabs** | Primary / Secondary, scrollable, fixed |

## Selection

| Componente | Variantes |
|---|---|
| **Checkbox** | Selected / Unselected / Indeterminate |
| **Chip** | Assist, Filter, Input, Suggestion |
| **Switch** | Selected / Unselected, with icons |
| **Slider** | Continuous / Discrete, Range |
| **Radio Button** | Selected / Unselected |

## Text Input

| Componente | Variantes |
|---|---|
| **Text Field** | Filled / Outlined, with/without icon, counter |
| **Text Area** | Multi-line, auto-grow |
| **Dropdown** | Exposed / Auto-complete / Select |

## Chips — Clasificación Detallada

| Tipo | Acción | Salida |
|---|---|---|
| **Assist** | Tap → acción helper | No persiste |
| **Filter** | Tap → toggle filter | Persiste (icono check) |
| **Input** | Tap → nueva entrada | Persiste + botón cerrar |
| **Suggestion** | Tap → completa input | No persiste, sirve auto-completado |

## Buenas Prácticas

- Cards deben tener solo 1 acción primaria
- Navigation Bar: máx 5 items, Navigation Rail: máx 7
- FAB no debe acompañarse de icon button similar adyacente
- Chips dentro de contenedor con scroll horizontal
- Text Fields: mostrar siempre label flotante
