# Forms — shadcn/ui

> Sistema de formularios type-safe basado en **react-hook-form** + **zod** + componentes shadcn Form.

## Stack

| Capa | Rol |
|---|---|
| `zod` | Schema de validación y tipos |
| `react-hook-form` | Manejo de estado del formulario |
| `@hookform/resolvers` | Bridge zod → react-hook-form |
| shadcn Form | Componentes UI con errores integrados |

## Estructura

```tsx
// 1. Definir schema
const formSchema = z.object({
  username: z.string().min(2).max(50),
  email: z.string().email(),
})

// 2. Inferir tipos
type FormValues = z.infer<typeof formSchema>

// 3. Componente Form
export function ProfileForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: { username: "", email: "" },
  })

  function onSubmit(values: FormValues) {
    // values es type-safe
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input placeholder="shadcn" {...field} />
              </FormControl>
              <FormDescription>This is your public display name.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

## Componentes del Sistema Form

| Componente | Propósito |
|---|---|
| `<Form>` | Provider del contexto |
| `<FormField>` | Campo individual con control |
| `<FormItem>` | Wrapper del campo |
| `<FormLabel>` | Label automático con errores |
| `<FormControl>` | Renderiza el input + aria attributes |
| `<FormDescription>` | Texto de ayuda |
| `<FormMessage>` | Mensaje de error automático |

## Validación Avanzada

```ts
// Validación condicional
const schema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("user"), name: z.string() }),
  z.object({ type: z.literal("admin"), role: z.string() }),
])

// Transformación
const schema = z.object({
  date: z.string().transform((val) => new Date(val)),
})

// Array de campos
const schema = z.object({
  items: z.array(z.object({ name: z.string(), qty: z.number().min(1) })),
})
```

## Buenas Prácticas

- Siempre tipar `useForm<T>` con el tipo inferido del schema
- `zodResolver` es el resolver recomendado
- `defaultValues` es obligatorio para evitar uncontrolled → controlled warnings
- Usar `FormField` para cada campo — no inputs sueltos
- `onSubmit` recibe valores ya validados y tipados
- Errores de servidor: `form.setError("field", { message })`
- Reset post-submit: `form.reset(values)`
