# Headroom Learn Guide

`headroom learn` analiza sesiones fallidas o costosas y propone ajustes persistentes para reducir tokens sin perder precision. Su uso principal es aprender el nivel de verbosidad adecuado y escribirlo en archivos de instrucciones del agente.

## Modo seguro: preview

```bash
headroom learn --verbosity
```

Este comando no modifica archivos. Revisa sesiones disponibles, estima patrones de sobre-respuesta y muestra la configuracion recomendada.

## Aplicar al proxy local

```bash
headroom learn --verbosity --apply
```

Por defecto escribe en `CLAUDE.local.md` o en el target local equivalente. Es apropiado para preferencias personales y ajustes que no deben commitearse.

## Targets compartidos

```bash
headroom learn --target AGENTS.md
headroom learn --target GEMINI.md
headroom learn --target CLAUDE.md
```

Usa targets compartidos solo cuando la regla aprendida sea estable para todo el equipo o para todos los agentes del repo. Para experimentos, prefiere archivos locales gitignored.

## Casos de uso

| Caso | Comando recomendado |
|---|---|
| Reducir respuestas largas tras lecturas de archivos | `headroom learn --verbosity` |
| Persistir verbosidad personal | `headroom learn --verbosity --apply` |
| Entrenar reglas cross-agent del repo | `headroom learn --target AGENTS.md` |
| Auditar antes de escribir | Ejecutar sin `--apply` |

## Relacion con output shaper

`headroom learn` puede alimentar el proxy cuando `HEADROOM_OUTPUT_SHAPER=1` esta activo. El proxy usa el nivel aprendido para aplicar verbosity steering y effort routing en turnos rutinarios.

```bash
export HEADROOM_OUTPUT_SHAPER=1
headroom proxy --port 8787
headroom learn --verbosity --apply
```

## Buenas practicas

- Ejecuta primero en preview.
- No escribas secretos ni rutas privadas en targets compartidos.
- Revisa el diff antes de commitear cambios en `AGENTS.md`, `GEMINI.md` o `CLAUDE.md`.
- Mantén reglas aprendidas cortas, concretas y accionables.

## Referencias

- [Quickstart](quickstart.md)
- [Proxy Config](proxy-config.md)
- [Wrapper Agents](wrapper-agents.md)
- [MCP Tools](mcp-tools.md)
- Docs oficiales: <https://headroom-docs.vercel.app/docs>
