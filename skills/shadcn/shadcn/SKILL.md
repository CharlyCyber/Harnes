---
name: shadcn
description: Componentes shadcn/ui para React y Next.js con Radix UI, Tailwind CSS, formularios, theming, iconos, CLI y registry. Usar al implementar o auditar UI shadcn.
---

# shadcn/ui — Skill de Componentes y UI System

> Skill especializada en **shadcn/ui**, el sistema de componentes para React basado en Radix UI + Tailwind CSS. Cubre instalación, composición, styling, forms, icons, CLI, registro de componentes y personalización.

## Capacidades

- **Composición**: Componentes headless (Radix UI) + estilos (Tailwind) = control total. Pattern `cn()` para merging de clases.
- **CLI**: `npx shadcn@latest add [component]` — añade solo lo que usas, sin bundler overhead.
- **Styling**: className-based, `tailwind.config.ts` via `cn()` helper, CSS variables para temas.
- **Forms**: Integración react-hook-form + zod para validación type-safe. Componentes Form, Field, Fieldset.
- **Icons**: Lucide React como icon set por defecto. Árbol shakeable, tree de importación explícito.
- **Base vs Radix**: Capas: Radix UI (headless) → shadcn/ui (estilizado) → App (custom). Te permite overridear cualquier capa.
- **Registro**: Componentes publicables via registry. npm package o URL remota.
- **Customización**: Theme global con CSS variables, component-level overrides, recetas CSS.

## Uso

Activa esta skill cuando:
- Implementes componentes **shadcn/ui** en proyectos React/Next.js
- Necesites **formularios type-safe** con validación
- Configures **theming y dark mode** con shadcn
- Quieras **publicar componentes** via registry
- Migres o estructures **sistemas de diseño** con shadcn/ui

## Archivos de Referencia

| Archivo | Contenido |
|---|---|
| `rules/styling.md` | Styling con Tailwind, cn(), CSS variables, themes |
| `rules/forms.md` | Formularios: react-hook-form + zod + shadcn Form |
| `rules/composition.md` | Patrones de composición de componentes |
| `rules/icons.md` | Sistema de iconos con Lucide React |
| `rules/base-vs-radix.md` | Capas Radix UI → shadcn → App |
| `cli.md` | Comandos y workflow de shadcn CLI |
| `registry.md` | Publicación de componentes via registry |
| `customization.md` | Personalización de temas y componentes |

## Integración con Otras Skills

- **`frontend-polish`**: UI/UX engineering — shadcn como base de interfaz
- **`web-animation`**: Animación con Framer Motion — compatible con componentes shadcn
- **`material-3`**: Sistema de diseño alternativo — elegir según proyecto
