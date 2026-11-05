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

## Herramientas (43 total)

### Automatización de entrada (10)
`click`, `drag`, `fill`, `fill_form`, `handle_dialog`, `hover`, `press_key`, `type_text`, `upload_file`, `click_at`

### Navegación (6)
`list_pages`, `new_page`, `navigate_page`, `close_page`, `select_page`, `wait_for`

### Debugging (8)
`evaluate_script`, `take_snapshot`, `take_screenshot`, `list_console_messages`, `get_console_message`, `lighthouse_audit`, `screencast_start`, `screencast_stop`

### Performance (3)
`performance_start_trace`, `performance_stop_trace`, `performance_analyze_insight`

### Network (2)
`list_network_requests`, `get_network_request`

### Emulación (2)
`emulate`, `resize_page`

### Memoria (5)
`take_heapsnapshot`, `get_heapsnapshot_class_nodes`, `get_heapsnapshot_details`, `get_heapsnapshot_retainers`, `get_heapsnapshot_summary`

### Extensiones (5)
`install_extension`, `list_extensions`, `reload_extension`, `trigger_extension_action`, `uninstall_extension`

### WebMCP (2)
`list_webmcp_tools`, `execute_webmcp_tool`

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
    "--no-usage-statistics",
    "--viewport=1920x1080"
  ]
}
```

### Flags útiles

| Flag | Descripción |
|---|---|
| `--headless` | Modo sin interfaz gráfica |
| `--isolated` | Perfil temporal que se limpia al cerrar |
| `--channel=canary` | Usar Chrome Canary |
| `--slim` | Solo 3 herramientas básicas (nav, script, screenshot) |
| `--experimental-vision` | Herramientas por coordenadas `click_at(x,y)` |
| `--experimental-memory` | Herramientas de memoria |
| `--experimental-screencast` | Grabación de pantalla (requiere ffmpeg) |
| `--no-usage-statistics` | Desactivar estadísticas de uso |

## Primer prompt de prueba

```
Check the performance of https://example.com
```

## Referencias

- Repo: https://github.com/ChromeDevTools/chrome-devtools-mcp
- Tool reference: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md
