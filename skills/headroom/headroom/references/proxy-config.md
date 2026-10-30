# Headroom Proxy Configuration

## Básico

```bash
headroom proxy --port 8787
```

Cliente → `http://localhost:8787` (OpenAI-compatible endpoint).

## Environment Variables

| Variable | Default | Descripción |
|---|---|---|
| `HEADROOM_OUTPUT_SHAPER` | `0` | Activa output token reduction (verbosity steering + effort routing) |
| `HEADROOM_OUTPUT_HOLDOUT` | `0` | Fracción 0.0–1.0 de conversaciones sin shaping (control group para measured savings) |
| `HEADROOM_UPDATE_CHECK` | `on` | `off` desactiva check de updates en startup (también off en `--stateless` y CI) |
| `HEADROOM_TLS_STRICT` | `1` | `0` desactiva strict cert validation (Python 3.13+ OpenSSL 3.x strict mode, Zscaler) |
| `HEADROOM_CONTEXT_TOOL` | `rtk` | `lean-ctx` usa lean-ctx en vez de RTK para CLI context rewriting |
| `HEADROOM_EMBEDDER_RUNTIME` | `auto` | `pytorch_mps` para Apple GPU offload (requiere `[pytorch-mps]` extra) |
| `GITHUB_COPILOT_ENTERPRISE_DOMAIN` | — | GitHub Enterprise Server domain para Copilot CLI subscription mode |
| `REQUESTS_CA_BUNDLE` / `SSL_CERT_FILE` / `CURL_CA_BUNDLE` | — | Trust corporate CA para `cdn.pyke.io` (ONNX) y `huggingface.co` (modelo) |
| `HF_HUB_OFFLINE` | `0` | `1` + pre-download model para air-gapped |
| `HF_ENDPOINT` | — | Mirror HF trusted (ej. `https://hf-mirror.com`) |
| `ORT_STRATEGY` | `auto` | `system` + `ORT_LIB_LOCATION` para ONNX Runtime pre-provisioned |

## Runtime Env Override (sin restart)

`headroom wrap` hot-syncs settings al proxy running via loopback `POST /admin/runtime-env`.

```bash
# Ejemplo: activar output shaper en proxy ya running
export HEADROOM_OUTPUT_SHAPER=1
headroom wrap claude  # reusa proxy existente, aplica override inmediato
```

**Nota:** En shared proxy, último setting explícito gana (global).

## Dashboard

```bash
headroom dashboard
```

Requiere proxy running. Muestra:
- Input tokens saved (compression ratio)
- Proxy $ Saved (via LiteLLM pricing — **requiere Python 3.13 o menor**, 3.14+ = `$0.00`)
- Output Tokens Saved (estimated/measured con confidence band)
- Cross-agent memory stats
- Pipeline latency

## Verificación

```bash
headroom doctor   # health check: routing, compressors, cache aligner, CCR
headroom perf     # benchmark suite
```

## Modos especiales

### Stateless (no cache, no memory, no updates)
```bash
headroom proxy --port 8787 --stateless
```

### Detached / Background
```bash
headroom proxy --port 8787 --detach
```

### Custom host
```bash
headroom proxy --host 0.0.0.0 --port 8787
```

---

## Troubleshooting Proxy

| Síntoma | Causa | Fix |
|---|---|---|
| Puerto ocupado | Otro proceso en 8787 | Cambia `--port` |
| `CERTIFICATE_VERIFY_FAILED` | SSL inspection corporativo | Instala Rust primero; trust CA via `REQUESTS_CA_BUNDLE` |
| `Basic Constraints...` Python 3.13+ | CA sin critical bit | `HEADROOM_TLS_STRICT=0` |
| `$0.00` en dashboard | Python 3.14+ (LiteLLM incompatible) | `pipx reinstall headroom-ai --python python3.13` |
| Modelo no carga | `huggingface.co` bloqueado | `HF_HUB_OFFLINE=1` + pre-download, o `HF_ENDPOINT` |
| ONNX no descarga | `cdn.pyke.io` bloqueado | `ORT_STRATEGY=system` + `ORT_LIB_LOCATION` |
| Wrapper no detecta proxy | Proxy no running / puerto equivocado | `headroom doctor` verifica |

---

## Referencias

- [Quickstart](quickstart.md)
- [Wrapper Agents](wrapper-agents.md)
- [MCP Tools](mcp-tools.md)
- [Learn Guide](learn-guide.md)
- **Docs oficiales:** <https://headroom-docs.vercel.app/docs/proxy>