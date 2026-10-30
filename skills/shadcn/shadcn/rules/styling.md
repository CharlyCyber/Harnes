# Styling — shadcn/ui

> shadcn/ui usa **Tailwind CSS** como motor de estilos con **`cn()`** para merging de clases y **CSS variables** para theming.

## cn() Helper

```ts
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

- `clsx` — condicionales, arrays, objetos
- `twMerge` — resuelve conflictos de Tailwind

## CSS Variables para Theming

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
  }
}
```

Formato HSL (hue saturation lightness) para máxima flexibilidad.

## Theme Config

```ts
// tailwind.config.ts
export default {
  darkMode: ["class"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        // ...secondary, destructive, muted, accent, popover, card
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
}
```

## Buenas Prácticas

- `cn()` siempre como wrapper de className
- Nunca usar Tailwind classes inline sin cn()
- CSS variables en HSL para permitir alpha channel
- Preferir `@layer base` para variables globales
- Dark mode via clase `.dark` en `<html>`
- Radio de bordes: --radius variable base (default 0.5rem)
- Colores: prefijo `--` con nombre descriptivo
