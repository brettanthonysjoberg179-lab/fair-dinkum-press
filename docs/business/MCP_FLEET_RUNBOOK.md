# MCP Fleet Runbook

Generated 2026-09-28 by the MCP Orchestrator, after auditing all three MCP servers.

## Read this first: none of these servers uses FastMCP

The FastMCP guide (`https://gofastmcp.com/deployment/running-server.md`, pattern
`from fastmcp import FastMCP` → `mcp.run()`) **does not apply to this fleet**.

| Server | Actual stack | FastMCP? |
| --- | --- | --- |
| RAGS Memory Agent | low-level MCP SDK `MCPServer` (`mcp.server.mcpserver`) | No |
| Content Generator Workforce | FastAPI + uvicorn; low-level `MCPServer` for the stdio path | No |
| Digital Product Workforce | FastAPI + hand-rolled JSON-RPC 2.0 over HTTP | No |

`fastmcp` is installed in the Content Generator and Digital Product venvs
(4.0.10 and 4.0.5) but **neither server imports it**. Do not write
`fastmcp run <file>` against these — it will not find a `FastMCP` instance.

Also note the transport-naming split: these servers spell Streamable HTTP
`streamable-http`, whereas FastMCP 4 spells it `http`.

---

## 1. RAGS Memory Agent

- **Entry point:** `rags_memory_db/mcp_server.py`
- **Transport:** stdio (default), `sse`, `streamable-http`
- **Interpreter:** **must** be the project venv. Base `python3` fails with
  `ModuleNotFoundError: No module named 'mcp'`.

```bash
cd /home/brettanthonysjoberg179/rags_memory_db
.venv/bin/python mcp_server.py --transport stdio
```

Recreate the environment:

```bash
cd /home/brettanthonysjoberg179/rags_memory_db
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

**Tools (6, verified by live handshake):** `store_memory`, `search_memory`,
`consolidate_memories`, `get_memory_stats`, `list_memories`, `delete_memory`

Verified: `get_memory_stats` returns 49 live memories
(28 fact / 18 semantic / 2 formfav_fetch / 1 working, embedding_dim 384).
`search_memory` returns ranked hits.

**Caveat:** `delete_memory` is destructive — confirm with the user first.

---

## 2. Content Generator Workforce

- **Entry point:** `contents-generator-workforce/mcp_server/main.py`
- **Transport:** stdio (explicit) or HTTP (default)

```bash
# stdio — for MCP host / agent integration
cd /home/brettanthonysjoberg179/contents-generator-workforce
.venv/bin/python mcp_server/main.py --transport stdio

# HTTP — for the Hermes integration (this is the default)
.venv/bin/python mcp_server/main.py --host 0.0.0.0 --port 8000
```

Both must use the project venv: base `python3` fails with
`ModuleNotFoundError: No module named 'fastapi'`.

**Tools (3, verified by live handshake):** `call_tool`, `list_tools`, `run_workflow`

This is a **meta-interface, not a flat tool list.** The 25 agents are not
individual MCP tools. Reach them with:

1. `list_tools` → returns every registered agent as `{name, description}`
2. `call_tool` with `{"tool": "<agent name>", "arguments": {...}}`
3. or `run_workflow` with `{"workflow_id": ..., "input_data": {...}}`

**Legacy invocations still supported** (verified, for backward compatibility):
`--stdio` (sentinel), a bare positional port (`main.py 9001`), and
`MCPSERVER_MODE=stdio`. Unrecognized flags now fail loudly instead of being
swallowed.

---

## 3. Digital Product Workforce

- **Entry point:** `digital_product_workforce/run.py` (uvicorn)
- **Transport:** HTTP only. **There is no stdio mode.**

```bash
SERVER_PORT=8000 /home/brettanthonysjoberg179/digital_product_workforce/.venv/bin/python \
  /home/brettanthonysjoberg179/digital_product_workforce/run.py
```

The ASGI app is `digital_product_workforce.app:app`. Its import path is rooted
at the **parent** of the package directory, so `cwd` must be
`/home/brettanthonysjoberg179` when invoking uvicorn directly:

```bash
cd /home/brettanthonysjoberg179
digital_product_workforce/.venv/bin/python -m uvicorn digital_product_workforce.app:app --port 8000
```

`run.py` now self-bootstraps `sys.path`, so it works from any directory.

**Endpoints:**
- `GET /health` → `{"status":"healthy"}`
- `POST /mcp` → JSON-RPC 2.0
- `POST /hitl/approve/{product_id}`, `POST /hitl/reject/{product_id}`,
  `GET /hitl/pending`

**Tools (2, verified via `tools/list`):** `save_product_asset`,
`publish_storefront_item`

⚠️ **`generate_product` and `evaluate_product` do not exist.** They are absent
from the entire package. Do not route product-generation requests here expecting
them; use the `digital-products` subagent or the Content Generator workforce.

`mcp_server.py` in this package is a **73-line reference schema module** — it
registers no tools and has no `run()`. The real server is `app.py`.

---

## Changes made during this audit

| File | Change |
| --- | --- |
| `rags_memory_db/.venv/` | **Created** — server was previously unrunnable (no `mcp`, `numpy`, or `huggingface_hub`) |
| `rags_memory_db/requirements.txt` | **Created** — pins `mcp==2.2.0`, `numpy==2.5.3`, `huggingface-hub==2.0.0` |
| `contents-generator-workforce/mcp_server/main.py` | Added project-root `sys.path` bootstrap (absolute-path invocation previously died on `No module named 'agents'`) |
| `contents-generator-workforce/mcp_server/main.py` | Replaced `int(sys.argv[1])` port parsing with `argparse` (`--transport`/`--host`/`--port`); old code crashed on *any* flag, including `--stdio` |
| `digital_product_workforce/run.py` | Added parent-dir `sys.path` bootstrap so it runs from any cwd |

Untouched: all agent/business logic, the Digital Product `app.py`, and every
tool implementation.

## Not changed, deliberately

The default transport for the Content Generator is still **http**, not stdio,
because the Hermes integration depends on it. `stdio` is now an explicit,
reliable option rather than the implicit default.
