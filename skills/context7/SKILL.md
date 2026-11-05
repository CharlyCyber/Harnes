---
name: context7
description: Documentación actualizada de librerías para agentes IA. Context7 provee docs frescas y ejemplos de código versionados directamente desde la fuente oficial de cada librería.
---

# Context7

Context7 es un MCP server que provee documentación up-to-date de librerías directamente al contexto del agente. Elimina las APIs alucinadas y el código obsoleto basado en datos de entrenamiento viejos.

## MCP Tools disponibles

| Tool | Descripción |
|---|---|
| `resolve-library-id` | Resuelve nombre de librería a un ID compatible con Context7 |
| `query-docs` | Obtiene documentación para una librería dado su libraryId y query |

## Cuándo usar Context7

Usa Context7 **siempre** que necesites:

- **Documentación de APIs de librerías** — Next.js, React, Supabase, Prisma, Tailwind, etc.
- **Ejemplos de código actualizados** — No confíes en tu training data para sintaxis actual
- **Configuración y setup** — Pasos de instalación y configuración de librerías
- **Versiones específicas** — Por ejemplo "Next.js 14 middleware" o "Supabase v2 auth"
- **Parámetros de API** — Headers, opciones, firmas de funciones actuales

## Cómo usar

### Patrón 1: Activar automáticamente

Agrega `use context7` al final de tu prompt cuando hagas preguntas sobre librerías:

```
Crea un middleware en Next.js que verifique un JWT válido en cookies. use context7
```

### Patrón 2: Librería específica

Si ya sabes qué librería necesitas, usa `use library /namespace/repo`:

```
Implementa autenticación básica con Supabase. use library /supabase/supabase
```

### Patrón 3: Llamar tools directamente (MCP)

Usa las MCP tools nativamente:

1. `resolve-library-id` con `libraryName: "next.js"` y `query: "middleware with cookies"`
2. `query-docs` con el `libraryId` obtenido y el `query` específico

## Ejemplos

**Resolver librería y obtener docs:**
```
resolve-library-id({ libraryName: "prisma", query: "schema validation with zod" })
→ libraryId: "/prisma/docs"

query-docs({ libraryId: "/prisma/docs", query: "schema validation with zod" })
→ docs + code examples actualizados
```

**En prompting directo:**
```
Configura una Cloudflare Worker para cachear respuestas JSON por 5 minutos. use context7
```

## API Key

La API key está configurada vía variable de entorno `CONTEXT7_API_KEY` en el servidor MCP. No es necesario configurarla manualmente.
