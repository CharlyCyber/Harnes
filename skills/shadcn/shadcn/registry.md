# Registry — shadcn/ui

> El **registry** es el sistema de distribución de componentes shadcn. Puedes publicar componentes propios o usar registros comunitarios. Se accede via CLI.

## Registry Oficial

```
https://ui.shadcn.com/r/[component].json
```

Ejemplo: `https://ui.shadcn.com/r/button.json` responde con:

```json
{
  "name": "button",
  "type": "registry:ui",
  "dependencies": ["@radix-ui/react-slot"],
  "registryDependencies": [],
  "files": [{
    "path": "ui/button.tsx",
    "content": "...",
    "type": "registry:ui"
  }]
}
```

## Tipos de Registry

| Tipo | Descripción |
|---|---|
| `registry:ui` | Componente UI (se copia a components/ui) |
| `registry:lib` | Utilitario (se copia a lib/) |
| `registry:hook` | React hook (se copia a hooks/) |
| `registry:block` | Bloque de UI (sección completa) |
| `registry:theme` | Tema (variables CSS) |
| `registry:page` | Página completa |

## Registry Personalizado

```json
// components.json
{
  "registry": [
    "https://tu-dominio.com/registry"
  ]
}
```

```bash
# Instalar desde registry personalizado
npx shadcn@latest add componente-custom
```

## Estructura de Registry.json

```json
{
  "$schema": "https://ui.shadcn.com/schema/registry.json",
  "name": "mis-componentes",
  "version": "1.0.0",
  "homepage": "https://mis-componentes.com",
  "items": [
    {
      "name": "super-button",
      "type": "registry:ui",
      "title": "Super Button",
      "description": "Botón con superpoderes",
      "dependencies": [
        "@radix-ui/react-slot",
        "lucide-react"
      ],
      "registryDependencies": [
        "button"
      ],
      "files": [{
        "path": "ui/super-button.tsx",
        "type": "registry:ui",
        "content": "// contenido del componente"
      }]
    }
  ]
}
```

## Buenas Prácticas

- Versionar el registry con semver
- `dependencies`: npm packages
- `registryDependencies`: otros componentes shadcn que necesita
- `files[].type`: siempre especificar el tipo correcto
- Probar instalación en proyecto limpio antes de publicar
- Incluir README con ejemplos de uso
- Documentar `dependencies` y `registryDependencies`
