# Base vs Radix UI — shadcn/ui Layers

> shadcn/ui se construye sobre **Radix UI Primitives** (headless, accesibles). Entender las capas es clave para saber cuándo y cómo customizar.

## Las 3 Capas

```
┌──────────────────────┐
│    App (tu código)   │ ← Usa componentes shadcn o Radix directo
├──────────────────────┤
│   shadcn/ui (estilo) │ ← Tailwind styles + composición
├──────────────────────┤
│  Radix UI (headless) │ ← Accesibilidad, estado, comportamiento
├──────────────────────┤
│       React          │ ← Fundación
└──────────────────────┘
```

### Radix UI — Capa Base

Radix provee:
- Comportamiento accesible (WAI-ARIA compliant)
- Estado y lógica (open/close, selected, focus)
- Sin estilos (headless) — tú controlas la apariencia
- Portal, context, keyboard navigation

### shadcn/ui — Capa de Estilo

shadcn añade:
- Tailwind classes como default
- Convenciones de composición
- `cn()` para merging
- CSS variables para theming

### App — Tu Capa

Puedes:
- Usar componentes shadcn directamente
- Customizar via className o `cn()`
- Reemplazar estilos completamente
- Usar Radix directo + tus propios estilos

## Cuándo Usar Cada Capa

| Situación | Capa |
|---|---|
| UI estándar (button, input, card) | shadcn |
| Comportamiento complejo (dropdown, dialog) | shadcn + Radix |
| Necesitas comportamiento Radicalmente diferente | Radix directo + estilos custom |
| Animaciones avanzadas | Radix + Framer Motion |
| Componente 100% custom sin accesibilidad compleja | Solo React + Tailwind |

## Ejemplo: Override de Componente

```tsx
// 1. Usar shadcn con className override
<Button className="bg-blue-600 hover:bg-blue-700">
  Custom
</Button>

// 2. Usar shadcn + cn() para merging complejo
<Button className={cn(
  "bg-blue-600",
  condition && "bg-red-600",
)} />

// 3. Usar Radix directo (cuando shadcn no expone lo que necesitas)
import * as Dialog from "@radix-ui/react-dialog"

<Dialog.Root>
  <Dialog.Trigger className="...">Open</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="..." />
    <Dialog.Content className="...">
      <Dialog.Title className="..." />
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

## Buenas Prácticas

- Preferir shadcn para el 80% de casos
- Customizar via className antes de reemplazar capas
- Si necesitas comportamiento Radix no expuesto por shadcn, usa Radix directo
- No mezcles shadcn y Radix directo para el mismo componente en la misma app
- Documenta overrides complejos para mantener consistencia del equipo
- shadcn es copy-paste — puedes modificar el código fuente del componente si necesitas cambios profundos
