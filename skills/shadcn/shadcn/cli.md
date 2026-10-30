# CLI — shadcn/ui

> La CLI de shadcn/ui gestiona la instalación, actualización y configuración de componentes. Los componentes se copian directamente a tu proyecto — no son una dependencia npm.

## Comandos Principales

```bash
# Inicializar shadcn en el proyecto
npx shadcn@latest init

# Añadir componentes
npx shadcn@latest add button
npx shadcn@latest add button card dialog
npx shadcn@latest add -a        # todos los componentes

# Actualizar componentes
npx shadcn@latest update button

# Ver información de componente
npx shadcn@latest info button

# Listar componentes disponibles
npx shadcn@latest list
```

## init — Configuración Inicial

`init` configura:

| Pregunta | Descripción |
|---|---|
| Style | Default o New York (diferente radii) |
| Base color | Neutral, Gray, Zinc, Stone, Slate, Red, Rose, Orange, Green, Blue, Yellow, Violet |
| CSS variables | Sí / No (recomendado: Sí) |
| src directory | Para proyectos con carpeta src/ |
| Components path | `@/components/ui` (default) |
| Utils path | `@/lib/utils` (contiene cn()) |
| React Server Components | Sí / No |
| Tailwind config | ts / js |
| Import alias | @/ para imports |
| Package manager | npm / yarn / pnpm / bun |

## add — Instalación de Componentes

```bash
# Componente específico
npx shadcn@latest add alert-dialog

# Varios
npx shadcn@latest add toast dropdown-menu popover

# Con flags
npx shadcn@latest add button --yes        # skip prompts
npx shadcn@latest add card --overwrite    # overwrite existing
```

Cada comando `add`:
1. Descarga el código fuente del componente
2. Detecta dependencias (Radix, lucide-react, etc.)
3. Las instala automáticamente
4. Añade el archivo a `components/ui/`
5. Actualiza `tailwind.config.ts` si es necesario

## update — Actualización

```bash
# Actualizar componente específico
npx shadcn@latest update button

# Todos los componentes
npx shadcn@latest update --all
```

Mantiene tus modificaciones vía merge inteligente.

## Config File

```json
// components.json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "src/app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

## Buenas Prácticas

- Ejecutar `init` al inicio del proyecto (no migrar después)
- Los componentes se modifican in-place — trata `components/ui/` como source code
- `add --overwrite` para resetear un componente a default
- Versionar `components.json` en el repo
- No editar componentes Radix directamente — customizar via className
- Usar `npx` siempre (no instalar shadcn global)
