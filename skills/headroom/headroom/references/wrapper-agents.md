# Headroom Wrapper Agents

## Matrix de compatibilidad

| Agent | `headroom wrap` | Notas |
|---|:---:|---|
| **Claude Code** | ✅ | `--memory` · `--code-graph` · `--1m` · `--tool-search` |
| **Codex** | ✅ | Comparte memoria con Claude |
| **Cursor** | Manual | Inicia proxy e imprime base URLs para settings de Cursor |
| **Aider** | ✅ | Inicia proxy + lanza |
| **Copilot CLI** | ✅ | Inicia proxy + lanza |
| **OpenClaw** | ✅ | Instala como ContextEngine plugin |
| **OpenCode** | ✅ | Inyecta config · inicia proxy + lanza |
| **Cline** | ✅ | Inicia proxy + inyecta config |
| **Continue** | ✅ | Inicia proxy + inyecta config |
| **Goose** | ✅ | Inicia proxy + lanza |
| **OpenHands** | ✅ | Inicia proxy + lanza |
| **Mistral Vibe** | ✅ | Inicia proxy + lanza |
| **Cortex Code** | Library only | 60–65% savings (library mode; no `wrap`) |

Cualquier cliente OpenAI-compatible funciona via `headroom proxy`.

---

## Comandos

```bash
# Wrap (instala skill/config + inicia proxy + lanza agente)
headroom wrap claude
headroom wrap codex
headroom wrap opencode
headroom wrap copilot
headroom wrap aider
headroom wrap cline
headroom wrap continue
headroom wrap goose
headroom wrap openhands
headroom wrap openclaw
headroom wrap vibe

# Cursor — manual setup
headroom wrap cursor
# Output: imprime base URLs → copiar a Cursor settings

# Undo (remueve config duradera)
headroom unwrap claude
headroom unwrap copilot
headroom unwrap codex
headroom unwrap opencode
headroom unwrap openclaw
```

---

## GitHub Copilot CLI Subscription Mode

Intercepta tráfico OpenAI-compatible de Copilot CLI, aplica compresión, reenvía a Copilot hosted API.

```bash
# 1. Autentica (una vez)
headroom copilot-auth login
# Almacena Headroom-specific Copilot OAuth token (evita tokens genéricos rechazados por token-exchange endpoint)

# 2. Wrap con subscription flag
headroom wrap copilot --subscription -- --model gpt-4o
```

**Enterprise / GitHub Enterprise Server:**
```bash
export GITHUB_COPILOT_ENTERPRISE_DOMAIN=ghe.example.com
headroom wrap copilot --subscription -- --model gpt-4o
```

**GitHub.com Enterprise Cloud** (ej. `github.com/enterprises/your-enterprise`): **NO** setees enterprise-domain override. Usa token-exchange normal.

---

## Plataformas / Auth Discovery

| Plataforma | Estado | Notas |
|---|---|---|
| macOS | ✅ Smoke-tested | Keychain access via Copilot CLI |
| Windows | ⚠️ Implementado | Credential Manager — necesita validación real |
| Linux | ⚠️ Implementado | Secret Service / `secret-tool` — necesita validación |
| Docker / CI | ⚠️ Planeado | Prefer `GITHUB_COPILOT_TOKEN` o `GITHUB_COPILOT_GITHUB_TOKEN` explícitos |

---

## Variables de entorno para wrappers

```bash
# Output token reduction
export HEADROOM_OUTPUT_SHAPER=1
headroom wrap claude

# Measured savings (10% holdout)
export HEADROOM_OUTPUT_HOLDOUT=0.1
headroom wrap opencode

# TLS strict off (Python 3.13+ Zscaler)
export HEADROOM_TLS_STRICT=0
headroom wrap copilot

# Usar lean-ctx en vez de RTK
export HEADROOM_CONTEXT_TOOL=lean-ctx
headroom wrap claude
```

---

## Referencias

- [Quickstart](quickstart.md)
- [Proxy Config](proxy-config.md)
- [MCP Tools](mcp-tools.md)
- [Learn Guide](learn-guide.md)
- **Docs oficiales:** <https://headroom-docs.vercel.app/docs/proxy#agent-wrappers>