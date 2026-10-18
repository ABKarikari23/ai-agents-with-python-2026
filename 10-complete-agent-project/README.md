# Part 10: Build a Complete AI Agent with Python

The final part of the **AI Agents with Python 2026** series brings the earlier
lessons together in a provider-neutral IT knowledge assistant. It validates a
request, retrieves local guidance and user-scoped memory, offers a limited set
of registered tools, enforces authorization and argument schemas, and bounds
the agent loop.

## Project structure

```text
app/
  agent.py          bounded workflow orchestration
  controller.py     task state
  knowledge.py      local lexical document retrieval
  memory.py         user-scoped SQLite memory
  model_adapter.py  provider contract and offline demo adapter
  security.py       tool authorization and Pydantic validation
  tools.py          allowlisted demo capabilities
data/knowledge/     sample troubleshooting documents
tests/              security, memory, and agent tests
main.py             command-line entry point
```

The metrics tool returns sample data only, and the support-ticket tool creates a
draft without submitting it. The default model adapter is deterministic and
offline; it does not call a model provider. Implement `ModelAdapter` for your
chosen provider, and keep tool execution inside `execute_authorized_tool`.

## Setup and run

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux or macOS
# source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Pass a question to the assistant as an optional command-line argument:

```bash
python main.py "Show the CPU metrics for the server."
```

The demo creates `data/agent_memory.db` when it runs. Do not use the example
identity or local SQLite database as a substitute for production authentication
or storage controls.

## Test

```bash
pytest -q
```

Tests use temporary SQLite databases and do not write user memories to the
project database.

## Scope and production considerations

Knowledge search uses lexical overlap rather than embeddings. The sample
metrics are not live; the tool role is fixed for this local demo; and the
workflow does not provide durable recovery, semantic retrieval, provider
timeouts, rate limiting, cost controls, or production authentication. Add and
test those controls before connecting the agent to real systems. Retrieved
documents are reference data and must never override application policy.

Explore this final project alongside the full collection in the
[main project dashboard](../dashboard).
