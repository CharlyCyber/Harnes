# Tipografía y Forma — Material Design 3

> MD3 define un **type scale** jerárquico de 15 tamaños y un **shape scale** de 6 niveles. Ambos son parte del sistema de tokens de diseño.

## Type Scale

| Token | Tamaño | Weight | Line Height | Tracking | Uso |
|---|---|---|---|---|---|
| **display** large | 57px | 400 | 64px | -0.25 | Hero text |
| display medium | 45px | 400 | 52px | 0 | Títulos grandes |
| display small | 36px | 400 | 44px | 0 | Títulos sección |
| **headline** large | 32px | 400 | 40px | 0 | Encabezados |
| headline medium | 28px | 400 | 36px | 0 | Subtítulos |
| headline small | 24px | 400 | 32px | 0 | Card titles |
| **title** large | 22px | 400 | 28px | 0 | Top app bar |
| title medium | 16px | 500 | 24px | 0.15 | Navigation, list |
| title small | 14px | 500 | 20px | 0.1 | Botones |
| **body** large | 16px | 400 | 24px | 0.5 | Texto largo |
| body medium | 14px | 400 | 20px | 0.25 | Texto general |
| body small | 12px | 400 | 16px | 0.4 | Legal, captions |
| **label** large | 14px | 500 | 20px | 0.1 | Botones |
| label medium | 12px | 500 | 16px | 0.5 | Chips, tabs |
| label small | 11px | 500 | 16px | 0.5 | Badges, tooltips |

### Font Families

| Familia | Uso |
|---|---|
| **Default** (system) | Roboto, SF Pro, etc. |
| **Brand** | Tipografía corporativa personalizada |
| **Code** | Monoespaciada (opcional) |

## Shape Scale

| Token | Valor | Uso |
|---|---|---|
| **shape-none** | 0px | Full-width banners, dividers |
| **shape-extra-small** | 4px | Chips, switches, sliders |
| **shape-small** | 8px | Cards, dialogs, menus |
| **shape-medium** | 12px | Bottom sheets, FAB |
| **shape-large** | 16px | Navigation drawer, search |
| **shape-extra-large** | 28px | Dialog full-screen, modals |
| **shape-full** | 50% | FAB circular, avatars |

### Topografía de Shape

```
none       [______________]
extra-small [____    ____]
small       [____    ____]
medium      [____    ____]
large       [____    ____]
extra-large [____    ____]
full        (____    ____)
```

## Buenas Prácticas

- Jerarquía tipográfica: máx 3 niveles por pantalla
- display solo para landing pages o estados vacíos
- body large para párrafos >50 palabras, body medium para <50
- label large es el token estándar para botones
- shape medium es el default para la mayoría de contenedores
- En cards informativas, usar headline small + body medium
- No mezclar weights distintos en el mismo nivel jerárquico
