# Part 6: RAG + AI Agents — Connecting Agents to Your Own Knowledge Sources

> Part of the **AI Agents with Python 2026** series (Wednesdays).
> Companion article: *(add your LinkedIn/blog article link here)*

## What this covers

This part introduces retrieval-augmented generation. Instead of relying only on a model's memory, the agent can look up relevant information from a local knowledge base and answer with grounded context.

## Setup

```bash
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Notes

The sample keeps the knowledge base in memory so it's easy to understand the retrieve-and-answer pattern without adding a vector database.
