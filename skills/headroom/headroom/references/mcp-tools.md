# Headroom MCP Tools

## Instalación

```bash
headroom mcp install
```

Registra el MCP server en tu cliente (Claude Desktop, Cursor, Continue, etc.).

---

## Tools expuestas

### `headroom_compress`

Comprime mensajes antes de enviarlos al LLM.

**Parámetros:**
```json
{
  "messages": [...],           // array de mensajes (OpenAI/Anthropic format)
  "model": "string",           // model ID para tokenizer-aware compression
  "compression_level": "auto"  // "auto" | "low" | "medium" | "high"
}
```

**Retorna:**
```json
{
  "compressed_messages": [...],
  "original_tokens": 12345,
  "compressed_tokens": 1234,
  "savings_pct": 90.0,
  "ccr_ids": ["ccr_abc123", ...]  // IDs para retrieval
}
```

### `headroom_retrieve`

Recupera contenido original via CCR (Content-Addressable Cache Retrieval).

**Parámetros:**
```json
{
  "ccr_ids": ["ccr_abc123", ...]  // IDs desde headroom_compress
}
```

**Retorna:**
```json
{
  "retrieved": [
    {"ccr_id": "ccr_abc123", "content": "original content..."}
  ]
}
```

### `headroom_stats`

Estadísticas de compresión de la sesión actual.

**Parámetros:** `{}`

**Retorna:**
```json
{
  "total_requests": 42,
  "total_original_tokens": 500000,
  "total_compressed_tokens": 45000,
  "avg_savings_pct": 91.0,
  "cross_agent_memory_entries": 17,
  "cache_hit_rate": 0.73
}
```

---

## Uso desde agente (ejemplo Claude)

```
Usuario: "Comprime este contexto y dime el savings"
Agente: llama headroom_compress con messages + model
→ retorna compressed_messages + savings_pct + ccr_ids

Usuario: "Recupera el original del ccr_abc123"
Agente: llama headroom_retrieve con ccr_ids
→ retorna contenido original
```

---

## Configuración MCP

El server respeta env vars del proxy:
- `HEADROOM_OUTPUT_SHAPER`
- `HEADROOM_TLS_STRICT`
- `HEADROOM_CONTEXT_TOOL`
- etc.

---

## Referencias

- [Quickstart](quickstart.md)
- [Proxy Config](proxy-config.md)
- [Wrapper Agents](wrapper-agents.md)
- [Learn Guide](learn-guide.md)
- **Docs oficiales:** <https://headroom-docs.vercel.app/docs/mcp>