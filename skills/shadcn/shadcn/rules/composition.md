# Composición — shadcn/ui

> Los componentes shadcn siguen el patrón de **composición**: componentes pequeños y enfocados que se combinan para crear UI complejas. Heredan esta filosofía de Radix UI.

## Patrón de Composición

```tsx
// Composición > Configuración
<Dialog>
  <DialogTrigger>Open</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
      <DialogDescription>Description</DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button>Action</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

Cada subcomponente tiene una responsabilidad única.

## Componentes Compuestos Comunes

### Dialog

```
Dialog
├── DialogTrigger
├── DialogContent
│   ├── DialogHeader
│   │   ├── DialogTitle
│   │   └── DialogDescription
│   └── DialogFooter
└── DialogClose (implícito en X button)
```

### Select

```
Select
├── SelectTrigger
│   └── SelectValue
├── SelectContent
│   ├── SelectGroup
│   │   ├── SelectLabel
│   │   └── SelectItem
│   └── SelectSeparator
└── SelectScrollUpButton/SelectScrollDownButton
```

### Table

```
Table
├── TableHeader
│   └── TableRow
│       └── TableHead
└── TableBody
    └── TableRow
        └── TableCell
```

### Accordion

```
Accordion (type="single" | "multiple")
└── AccordionItem
    ├── AccordionTrigger
    └── AccordionContent
```

## Reglas de Composición

1. **Cada subcomponente importa individualmente** — no `import *`
2. **El padre SIEMPRE provee contexto** vía React Context
3. **Los hijos leen contexto**, no reciben props directas del padre
4. **Orden de hijos importa** — los subcomponentes esperan estructura específica
5. **Slot pattern** — `asChild` prop para delegar render a otro elemento

## asChild (Slot Pattern)

```tsx
// En lugar de:
<Button asChild>
  <a href="/dashboard">Go to Dashboard</a>
</Button>

// El slot transpila a:
<a href="/dashboard" className={buttonStyles}>...</a>
```

Usar `asChild` cuando necesites cambiar el elemento raíz manteniendo estilos y comportamiento del componente shadcn.

## Buenas Prácticas

- No anidar componentes compuestos unos dentro de otros (ej: Dialog dentro de Dialog)
- Siempre proveer `key` cuando renders dinámicos de items
- Mantener la estructura plana — no añadir divs entre padre e hijo directo
- Los componentes compuestos heredan el tema via CSS variables, no via props
- `asChild` solo cuando sea necesario — el default HTML element suele ser correcto
