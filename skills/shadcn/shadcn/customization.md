# Customización — shadcn/ui

> shadcn/ui es diseñado para ser customizado. Al ser copy-paste (no una dependencia npm), cada componente es tuyo para modificar.

## Niveles de Customización

| Nivel | Qué cambia | Cómo |
|---|---|---|
| 1. Theme global | Colores, bordes, fuentes | CSS variables |
| 2. Tailwind config | Spacing, breakpoints, animations | tailwind.config.ts |
| 3. Component override | Variante o estilo específico | cn() + className |
| 4. Component edit | Estructura o lógica | Editar el .tsx directamente |

## Nivel 1: Theme Global

```css
/* globals.css — cambiar paleta completa */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 240 10% 3.9%;
    --foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 240 5.9% 10%;
  }
}
```

## Nivel 2: Tailwind Config

```ts
// tailwind.config.ts
export default {
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui"],
      },
      keyframes: {
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
      },
      animation: {
        "fade-in": "fade-in 0.3s ease-out",
      },
    },
  },
}
```

## Nivel 3: Component Override via cn()

```tsx
// Uso con override de clases
<Button
  className={cn(
    "rounded-full",          // override shape
    "text-base px-8 py-6",   // override size
    "shadow-lg",             // extra style
    variant === "destructive" && "animate-pulse"
  )}
>
  Custom Button
</Button>
```

## Nivel 4: Editar Componente Directamente

```tsx
// components/ui/button.tsx — editar el source
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  // Cambiar estilos base aquí
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

## Recetas Comunes

### Brand Colors

```css
:root {
  --primary: 262 83% 58%;  /* purple-500 */
  --primary-foreground: 0 0% 100%;
}
```

### Border Radius Redondeado

```css
:root {
  --radius: 0.75rem;  /* de 0.5rem a 0.75rem */
}
```

### Fuente Personalizada

```tsx
// app/layout.tsx
import { Inter } from "next/font/google"
const inter = Inter({ subsets: ["latin"], variable: "--font-inter" })

<html className={inter.variable}>
```

```css
/* globals.css */
:root {
  --font-sans: "var(--font-inter)";
}
```

## Buenas Prácticas

- Preferir Nivel 1-3 sobre Nivel 4 (mantiene actualizaciones más fáciles)
- Si editas el source (Nivel 4), considera forkear o documentar los cambios
- Los cambios de theme via CSS variables persisten tras `shadcn update`
- Las animaciones custom: registrarlas en tailwind.config.ts como keyframes
- No modifiques los componentes Radix subyacentes — customizar via props
- Mantén un tema unificado: si cambias `--primary`, actualiza todos los usos semánticos
