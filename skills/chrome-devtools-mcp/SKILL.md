---
name: chrome-devtools-mcp
description: Chrome DevTools for AI agents — MCP server que expone herramientas de DevTools para debugging, rendimiento, red, emulación, accesibilidad y automatización. 43 herramientas. Usar cuando necesites analizar/debuggear un sitio web, auditar performance o accesibilidad, inspeccionar red, o automatizar Chrome con precisión quirúrgica.
---

# Chrome DevTools MCP

Servidor MCP oficial de Chrome DevTools. Expone el poder completo de las Chrome DevTools como herramientas para agentes IA: debugging, performance, network, emulación, lighthouse, memoria, screenshots, automatización de navegador.

## Instalación (ya configurada)

El MCP ya está registrado en la config de OpenCode (`~\.config\opencode\opencode.json`):

```json
"chrome-devtools": {
  "command": "npx",
  "args": ["-y", "chrome-devtools-mcp@latest"]
}
```

## Requisitos

- Node.js LTS
- Google Chrome (stable o newer)
- npm

## Herramientas disponibles

La lista y las categorías del servidor han evolucionado; no asumir un recuento fijo ni fiarse de listas copiadas aquí. Consulta las herramientas que expone la conexión MCP activa. La referencia oficial [Tool Reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md) documenta la versión upstream, incluyendo depuración, automatización, rendimiento, red, heap, mocks de red, extensiones, terceros, WebMCP, PWA y WebAuthn.

Algunas categorías son opt-in y no aparecerán si el servidor no se inicia con su flag. La documentación oficial actual indica `--categoryExtensions` para extensiones y `--categoryMemory` para herramientas de memoria; `--categoryExperimentalWebmcp` habilita WebMCP. Comprueba [Configuration](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md) para los nombres y valores vigentes antes de cambiar la configuración. `--slim` expone un conjunto reducido de herramientas; no presupongas que mantiene el mismo alcance que el modo completo.

## Cuándo usarlo

- **Auditar performance** de un sitio web (Core Web Vitals: LCP, INP, CLS)
- **Debuggear** una página: console errors, network requests, snapshots
- **Automatizar** interacciones complejas en Chrome (más confiable que Playwright para debugging)
- **Auditar accesibilidad** con Lighthouse
- **Analizar memoria** (heap snapshots) para detectar memory leaks
- **Emular** dispositivos móviles, redes lentas, prefers-color-scheme
- **Capturar screenshots** para verificar visualmente el estado de una página

## Cuándo NO usarlo

- Tareas simples de scraping (usar Playwright MCP o Firecrawl)
- Necesitas interacción con navegadores no-Chromium (Firefox, Safari)
- Solo necesitas navegar sin debugging (Playwright MCP es más liviano)

## Configuración avanzada

```json
{
  "command": "npx",
  "args": [
    "-y",
    "chrome-devtools-mcp@latest",
    "--headless",
    "--isolated",
    "--no-usage-statistics"
  ]
}
```

Flags, defaults y categorías cambian entre versiones; no copies opciones de una instalación distinta sin verificar la [Configuration Guide](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md). Entre las categorías opcionales actuales: `--categoryExtensions`, `--categoryMemory` y `--categoryExperimentalWebmcp`; `--slim` ofrece un perfil reducido. Conserva solo las capacidades necesarias y revisa expresamente los permisos y efectos antes de habilitarlas. No assumes que una categoría experimental o una herramienta esté activa por defecto.

## Primer prompt de prueba

```
Check the performance of https://example.com
```

## Referencias

- Repo: https://github.com/ChromeDevTools/chrome-devtools-mcp
- Tool reference: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md
