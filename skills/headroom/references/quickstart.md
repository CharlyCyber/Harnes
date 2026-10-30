# Headroom Quickstart (60 segundos)

## 1. Instalación

```bash
# Python — todo incluido
pip install "headroom-ai[all]"

# TypeScript / Node
npm install headroom-ai

# Docker
docker pull ghcr.io/chopratejas/headroom:latest
```

## 2. Elige tu modo

```bash
# A) Wrapper de agente (recomendado para coding agents)
headroom wrap claude        # o codex, opencode, copilot, aider, cline, continue, goose, openhands, openclaw, vibe

# B) Proxy drop-in (cualquier cliente OpenAI-compatible)
headroom proxy --port 8787
# Configura tu cliente para usar http://localhost:8787 como base URL

# C) Librería inline (Python/TS)
# from headroom import compress  /  import { compress } from "headroom-ai"

# D) MCP Server
headroom mcp install
```

## 3. Verifica

```bash
headroom doctor    # health check — routing OK?
headroom perf      # benchmark compresión
headroom dashboard # live savings (proxy running)
```

## 4. Output token reduction (opcional)

```bash
export HEADROOM_OUTPUT_SHAPER=1
headroom proxy --port 8787
```

Para measured savings (no estimated): `HEADROOM_OUTPUT_HOLDOUT=0.1`

## 5. headroom learn (opcional)

```bash
headroom learn --verbosity          # preview
headroom learn --verbosity --apply  # save to CLAUDE.local.md
```

---

## Entornos corporativos / SSL inspection

```bash
# 1. Instala Rust ANTES (evita descarga en build)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh && rustup default stable
# Windows: winget install Rustlang.Rustup && rustup default stable

# 2. Luego instala headroom
pip install "headroom-ai[all]"
```

Si Python 3.13+ con Zscaler/CA sin `basicConstraints` critical:
```bash
HEADROOM_TLS_STRICT=0 headroom proxy --port 8787
```

---

## Undo

```bash
headroom unwrap claude   # o copilot, codex, opencode, openclaw
```

---

## Próximos pasos

- [Proxy Config](proxy-config.md) — env vars, runtime overrides, dashboard
- [Wrapper Agents](wrapper-agents.md) — detalles por agente, Copilot subscription mode
- [MCP Tools](mcp-tools.md) — headroom_compress, headroom_retrieve, headroom_stats
- [Learn Guide](learn-guide.md) — mining fallos, verbosidad, targets
- **Docs completas:** <https://headroom-docs.vercel.app/docs>