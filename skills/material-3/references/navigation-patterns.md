# Patrones de Navegación — Material Design 3

> MD3 define patrones de navegación responsive adaptados al tamaño de pantalla: Navigation Bar (mobile), Navigation Rail (tablet), Navigation Drawer (desktop).

## Estrategia de Navegación Adaptativa

### Por Window Size Class

| Clase | Ancho | Componente de navegación primario |
|---|---|---|
| **Compact** | < 600px | Navigation Bar |
| **Medium** | 600-840px | Navigation Rail |
| **Expanded** | > 840px | Navigation Drawer |

### Jerarquía de Navegación

1. **Top-level** — destinos principales (3-5 items)
2. **Section-level** — dentro de una sección (tabs, list)
3. **Detail-level** — contenido específico (back navigation)

## Componentes de Navegación

### Navigation Bar (mobile)

```
[icon] [icon] [icon] [icon] [icon]
  label   label   label   label   label
```

- 3-5 destinos
- Activo = primary + selected state
- Badges opcionales para notificaciones
- FAB centrado opcional

### Navigation Rail (tablet)

```
[icon]
[icon]
[icon]
[icon]
[FAB]
```

- 3-7 destinos
- Icono + label (expandible)
- FAB al final (opcional)
- Alineado a la izquierda

### Navigation Drawer (desktop)

```
┌─────────────┐
│ Header      │
│ [icon] Item │
│ [icon] Item │
│ [icon] Item │
│ ─────────── │
│ [icon] Item │
│ [icon] Item │
└─────────────┘
```

- Modal (overlay) o Standard (persistente)
- Standard: siempre visible en expanded
- Modal: toggle con hamburger menu
- Soporta secciones, headers, dividers

### Navegación Interna

| Patrón | Uso |
|---|---|
| **Tabs** | Contenido relacionado, misma jerarquía |
| **Search** | Descubrimiento de contenido |
| **Carousel** | Navegación horizontal entre items |
| **Pagination** | Contenido secuencial (wizard, onboarding) |

## Buenas Prácticas

- No mezclar Navigation Bar y Bottom Navigation
- Navigation Bar siempre arriba (no bottom nav)
- La navegación primaria debe ser predecible — no reordenar
- Back navigation: visible cuando hay historial, oculto en home
- Search: implementar como full-screen en mobile, dialog en desktop
- Drawer header: usar información de sesión (avatar + nombre)
- Mantener consistencia cross-platform en la estructura de navegación
