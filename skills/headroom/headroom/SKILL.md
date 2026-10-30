---
name: headroom
description: Compresion de contexto para agentes IA con proxy, wrapper, MCP, memoria cross-agent y reduccion de tokens. Usar cuando se quiera bajar coste/contexto de workflows agenticos.
---

# headroom — Capa de Compresión de Contexto para Agentes IA

> Skill para integrar **Headroom**: compresión de contexto (60–95% menos tokens) vía librería, proxy, wrapper de agentes, MCP server y memoria cross-agent. Reversible (CCR). Local-first.

## Descripción

Headroom comprime **todo lo que el agente lee** — tool outputs, logs, RAG chunks, archivos, historial de conversación — **antes de llegar al LLM**. Mismas respuestas, fracción de los tokens.

**4 modos de uso:**
1. **Librería** — `compress(messages)` en Python/TypeScript, inline en cualquier app
2. **Proxy** — `headroom proxy --port 8787`, zero code changes, cualquier lenguaje
3. **Agent Wrapper** — `headroom wrap claude|codex|copilot|cursor|aider|opencode|...` en 1 comando
4. **MCP Server** — `headroom_compress`, `headroom_retrieve`, `headroom_stats` para cualquier MCP client

**Extras:** Memoria cross-agent (Claude, Codex, Gemini compartida, auto-dedup), `headroom learn` (minería de sesiones fallidas → `CLAUDE.local.md` / `AGENTS.md` / `GEMINI.md`), reducción de output tokens (verbosity steering + effort routing), CCR reversible (originales cacheados para retrieval on-demand).

---

## Instalación

```bash
# Python (todo incluido)
pip install "headroom-ai[all]"

# TypeScript / Node
npm install headroom-ai

# Docker
docker pull ghcr.io/chopratejas/headroom:latest
```

**Extras granulares:** `[proxy]`, `[mcp]`, `[ml]` (Kompress-v2-base), `[code]`, `[memory]`, `[vector]` (HNSW — necesita C++ toolchain, no en `[all]`), `[relevance]`, `[image]`, `[agno]`, `[langchain]`, `[evals]`, `[pytorch-mps]` (Apple GPU — `HEADROOM_EMBEDDER_RUNTIME=pytorch_mps`).

**Requiere:** Python 3.10+.

### Entornos corporativos / SSL inspection

Si `pip install` falla con `CERTIFICATE_VERIFY_FAILED`: tu red usa MITM proxy con CA corporativa. **Instala Rust primero** para que el build no lo descargue:

```bash
# macOS / Linux
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh && rustup default stable
# Windows
winget install Rustlang.Rustup && rustup default stable
```

Reinicia shell, luego `pip install "headroom-ai[all]"`. O usa wheel prebuilt: `pip install --only-binary headroom-ai headroom-ai`.

**Python 3.13+ strict mode** (CA sin `basicConstraints` critical — ej. Zscaler):
```bash
HEADROOM_TLS_STRICT=0 headroom proxy --port 8787
```
Solo desactiva el flag strict; validación de cadena, firma, expiración y hostname siguen activos.

**Assets runtime over TLS** (si bloqueados, trust CA via `REQUESTS_CA_BUNDLE` / `SSL_CERT_FILE` / `CURL_CA_BUNDLE`):
- `cdn.pyke.io` — ONNX Runtime (Rust core). Alternative: `ORT_STRATEGY=system` + `ORT_LIB_LOCATION=/path/to/onnxruntime`
- `huggingface.co` — modelo `kompress-base`. Alternative: `HF_HUB_OFFLINE=1` o `HF_ENDPOINT` a mirror trusted.

---

## Modos de uso

### 1. Librería (inline)

```python
# Python
from headroom import compress
compressed = compress(messages, model="claude-3-5-sonnet-20241022")
```

```typescript
// TypeScript
import { compress } from "headroom-ai";
const compressed = await compress(messages, { model: "claude-3-5-sonnet-20241022" });
```

**Integraciones framework:**
- Anthropic/OpenAI SDK: `withHeadroom(new Anthropic())` · `withHeadroom(new OpenAI())`
- Vercel AI SDK: `wrapLanguageModel({ model, middleware: headroomMiddleware() })`
- LiteLLM: `litellm.callbacks = [HeadroomCallback()]`
- LangChain: `HeadroomChatModel(your_llm)`
- Agno: `HeadroomAgnoModel(your_model)`
- Strands: ver [guía](https://headroom-docs.vercel.app/docs/strands)
- ASGI apps: `app.add_middleware(CompressionMiddleware)`

### 2. Proxy (drop-in, zero code changes)

```bash
headroom proxy --port 8787
```

Configura tu cliente para usar `http://localhost:8787` como base URL. Funciona con **cualquier cliente OpenAI-compatible**.

**Verificar:**
```bash
headroom doctor      # health check — confirma routing funciona
headroom perf        # benchmark de compresión
headroom dashboard   # live savings dashboard (proxy debe estar running)
```

**Env vars proxy:**
| Variable | Descripción |
|---|---|
| `HEADROOM_OUTPUT_SHAPER=1` | Activa output token reduction (verbosity steering + effort routing) |
| `HEADROOM_OUTPUT_HOLDOUT=0.1` | 10% conversaciones sin shaping como control group (measured savings) |
| `HEADROOM_UPDATE_CHECK=off` | Desactiva check de updates en startup |
| `HEADROOM_TLS_STRICT=0` | Desactiva strict cert validation (Python 3.13+ Zscaler) |
| `HEADROOM_CONTEXT_TOOL=lean-ctx` | Usa lean-ctx en vez de RTK para CLI context |

**Runtime env override (sin restart):** `headroom wrap` hot-syncs settings al proxy running via `POST /admin/runtime-env`.

### 3. Agent Wrapper (1 comando)

```bash
headroom wrap claude        # Claude Code
headroom wrap codex         # Codex
headroom wrap opencode      # opencode
headroom wrap copilot       # GitHub Copilot CLI
headroom wrap aider         # Aider
headroom wrap cursor        # Cursor (manual setup — imprime base URLs)
headroom wrap cline         # Cline
headroom wrap continue      # Continue
headroom wrap goose         # Goose
headroom wrap openhands     # OpenHands
headroom wrap openclaw      # OpenClaw (instala como ContextEngine plugin)
headroom wrap vibe          # Mistral Vibe
headroom wrap cortex        # Cortex Code (library only, 60–65% savings)
```

**Deshacer:** `headroom unwrap <tool>` (soporta: `claude`, `copilot`, `codex`, `opencode`, `openclaw`).

**GitHub Copilot CLI subscription mode:**
```bash
headroom copilot-auth login
headroom wrap copilot --subscription -- --model gpt-4o
```
Intercepta tráfico OpenAI-compatible de Copilot CLI, aplica compresión, reenvía a Copilot hosted API.

**Enterprise:** `export GITHUB_COPILOT_ENTERPRISE_DOMAIN=ghe.example.com` antes de launch.

### 4. MCP Server

```bash
headroom mcp install
```

Expone 3 tools para cualquier MCP client:
- `headroom_compress` — comprime mensajes
- `headroom_retrieve` — recupera originales via CCR
- `headroom_stats` — estadísticas de compresión

---

## Pipeline Internals (30 seg)

```
Tu agente/app → Headroom (local) → LLM provider
     │                    │
     │  prompts · tool outputs · logs · RAG · files
     ▼
┌────────────────────────────────────────────────┐
│ CacheAligner → ContentRouter → Compressors     │
│                    ├─ SmartCrusher   (JSON)    │
│                    ├─ CodeCompressor (AST)     │
│                    └─ Kompress-v2-base (text)  │
│                                                │
│ Cross-agent memory · headroom learn · MCP      │
└────────────────────────────────────────────────┘
     │  compressed prompt + retrieval tool
     ▼
LLM provider (Anthropic · OpenAI · Bedrock · …)
```

- **ContentRouter** — detecta tipo de contenido, selecciona compressor
- **CacheAligner** — estabiliza prefixes para KV cache hits (Anthropic/OpenAI)
- **CCR** — almacena originales localmente; LLM llama `headroom_retrieve` si los necesita
- **Reversible** — originales recuperables dentro de TTL configurado

---

## headroom learn

```bash
# Preview (dry run)
headroom learn --verbosity

# Aplicar: escribe nivel de verbosidad óptimo al proxy
headroom learn --verbosity --apply

# Target files (default: CLAUDE.local.md — gitignored)
headroom learn --target CLAUDE.md      # shared team file
headroom learn --target AGENTS.md
headroom learn --target GEMINI.md
```

Minera sesiones fallidas, detecta patrones, escribe correcciones. El proxy usa el nivel aprendido automáticamente.

---

## Output Token Reduction (recorta lo que el modelo ESCRIBE)

En modelos Opus-class, output cuesta 5× input. Mucho output es waste: preámbulos ("Great, let me…"), re-imprimir código, "thinking" profundo en pasos rutinarios.

Headroom lo recorta **desde el proxy**, sin cambiar código:

1. **Verbosity steering** — appends "be terse, don't restate context" al system prompt (cache hit preservado)
2. **Effort routing** — en turns que solo resume tras tool result (file read, passing test), diala thinking effort down. Preguntas nuevas y errores mantienen full effort.

```bash
export HEADROOM_OUTPUT_SHAPER=1
headroom proxy --port 8787
```

**Measured savings:** `headroom output-savings` reporta estimate con confidence range. Para measured real: `HEADROOM_OUTPUT_HOLDOUT=0.1` (10% control group). Dashboard muestra card "Output Tokens Saved" labelled `measured` o `estimated` con banda de confianza.

---

## Memoria Cross-Agent

`SharedContext().put / .get` — contexto comprimido pasando entre multi-agent workflows. Provenance tracking, auto-dedup. Compartida entre Claude, Codex, Gemini.

---

## Compresores incluidos

| Compresor | Tipo | Detalle |
|---|---|---|
| **SmartCrusher** | JSON universal | arrays of dicts, nested objects, mixed types |
| **CodeCompressor** | AST-aware | Python, JS/TS, Go, Rust, Java, C/C++, Perl |
| **Kompress-v2-base** | HF model | entrenado en agentic traces |
| **Image compression** | ML router | 40–90% reduction |

---

## Troubleshooting

| Problema | Solución |
|---|---|
| `CERTIFICATE_VERIFY_FAILED` | Instala Rust primero; o `--only-binary headroom-ai`; trust CA via `REQUESTS_CA_BUNDLE` |
| `Basic Constraints of CA cert not marked critical` (Python 3.13+) | `HEADROOM_TLS_STRICT=0` |
| Proxy no arranca / puerto ocupado | Cambia `--port`; verifica `headroom doctor` |
| Dollar savings `$0.00` en dashboard | Python 3.14+ no soporta LiteLLM. Usa 3.13: `pipx reinstall headroom-ai --python python3.13` |
| Modelo no descarga (huggingface.co bloqueado) | `HF_HUB_OFFLINE=1` + pre-download, o `HF_ENDPOINT` a mirror |
| ONNX Runtime no descarga (cdn.pyke.io bloqueado) | `ORT_STRATEGY=system` + `ORT_LIB_LOCATION` |

---

## Integraciones con skills existentes

| Skill | Sinergia |
|---|---|
| **opencode** | Wrapper nativo en matrix (`headroom wrap opencode`) |
| **graphify** | Contexto compartido / knowledge graph — Headroom comprime graph context antes de LLM |
| **ponytail** | Filosofía token savings alineada — "lazy senior dev" = compresión automática |
| **ai-agents-architect** | Infra para agentes autónomos — Headroom reduce costo de tool use / memory / planning |
| **performance** | Benchmarks/profiling complementarios — Headroom = token-level optimization |
| **rag-implementation** — retrieval, Headroom = compression layer encima |
| **prompt-engineering-patterns** — prompting craft, Headroom = runtime token reduction |

---

## Referencias

- **Quickstart:** `references/quickstart.md`
- **Proxy Config:** `references/proxy-config.md`
- **Wrapper Agents:** `references/wrapper-agents.md`
- **MCP Tools:** `references/mcp-tools.md`
- **Learn Guide:** `references/learn-guide.md`

**Documentación oficial:** <https://headroom-docs.vercel.app/docs>
**Repo:** <https://github.com/chopratejas/headroom> (org: headroomlabs-ai)
**Model card:** <https://huggingface.co/chopratejas/kompress-v2-base>
**Discord:** <https://discord.gg/yRmaUNpsPJ>
**Benchmarks:** <https://headroom-docs.vercel.app/docs/benchmarks>
