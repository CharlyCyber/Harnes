# Iconos — shadcn/ui

> shadcn/ui usa **Lucide React** como icon set por defecto. Lucide es árbol shakeable, open-source, y compatible con el sistema de composición de shadcn.

## Instalación

```bash
npm install lucide-react
```

## Uso Básico

```tsx
import { ChevronDown, Menu, X } from "lucide-react"

// Como componente JSX
<Menu className="h-4 w-4" />
<X className="h-4 w-4" />

// En componentes shadcn
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"

<Button>
  <Plus className="mr-2 h-4 w-4" /> Add Item
</Button>
```

## Convenciones de Tamaño

| Contexto | Tamaño |
|---|---|
| Botones | `h-4 w-4` (16px) |
| Iconos solitarios | `h-5 w-5` (20px) |
| Navigation | `h-5 w-5` |
| Dialog close (X) | `h-4 w-4` |
| Chevrons | `h-4 w-4` |

## Patrones

```tsx
// Icono + texto en botón
<Button variant="outline">
  <Upload className="mr-2 h-4 w-4" />
  Upload File
</Button>

// Icono + spinner loading
<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  Saving...
</Button>

// Icono en input
<div className="relative">
  <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
  <Input className="pl-10" placeholder="Search..." />
</div>
```

## Iconos que Lucide NO tiene

Lucide evita iconos muy específicos de marca (logos de empresas). Para esos casos:

1. Usar `<img>` o `<svg>` inline
2. Añadir icono personalizado como componente React envuelto en `lucide-react` API
3. Usar `@radix-ui/react-icons` como alternativa (menos opciones pero headless-ready)

## Buenas Prácticas

- Importar solo los iconos que usas (tree-shaking automático)
- Consistencia de tamaño dentro del mismo contexto
- `className` para color: `text-muted-foreground`, `text-primary`, etc.
- Espaciado: `mr-2` cuando precede texto, `ml-2` cuando sigue
- Spinners: `Loader2` + `animate-spin`
- En botones icon-only: `aria-label` es obligatorio
- Preferir Lucide sobre Font Awesome o SVG inline
