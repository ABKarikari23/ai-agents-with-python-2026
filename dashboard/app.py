"""Main project dashboard for the AI Agents with Python series."""

from __future__ import annotations

import os
from time import perf_counter

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

SERIES_PARTS = [
    {"number": 1, "title": "What Are AI Agents?", "folder": "01-what-are-ai-agents", "status": "published", "capability": "Goals and agent loops"},
    {"number": 2, "title": "How AI Agents Work", "folder": "02-how-ai-agents-work", "status": "published", "capability": "Models, tools, state, and memory"},
    {"number": 3, "title": "Building Your First Simple AI Agent", "folder": "03-first-simple-agent", "status": "published", "capability": "A working Python agent"},
    {"number": 4, "title": "Giving AI Agents Tools", "folder": "04-giving-agents-tools", "status": "published", "capability": "Functions, APIs, and services"},
    {"number": 5, "title": "Adding Memory and Context", "folder": "05-memory-and-context", "status": "published", "capability": "Persistent context"},
    {"number": 6, "title": "RAG + AI Agents", "folder": "06-rag-plus-agents", "status": "published", "capability": "Knowledge-grounded answers"},
    {"number": 7, "title": "Multi-Agent Systems", "folder": "07-multi-agent-systems", "status": "current", "capability": "Specialists and orchestration"},
    {"number": 8, "title": "AI Agents for Automation", "folder": "08-agents-for-automation", "status": "upcoming", "capability": "Scheduled workflows"},
    {"number": 9, "title": "Security, Guardrails and Reliability", "folder": "09-security-guardrails-reliability", "status": "upcoming", "capability": "Controlled autonomy"},
    {"number": 10, "title": "Building a Complete AI Agent Project", "folder": "10-complete-agent-project", "status": "upcoming", "capability": "Production-ready system"},
]


@app.get("/")
def index():
    return render_template("index.html", series_parts=SERIES_PARTS)


@app.get("/api/series")
def series():
    return jsonify({"total": len(SERIES_PARTS), "published": 7, "current": 7, "parts": SERIES_PARTS})


@app.post("/api/demo")
def demo():
    payload = request.get_json(silent=True) or {}
    task = (payload.get("task") or "Trace how the AI Agents with Python series grows from a simple agent to an orchestrated system.").strip()
    started = perf_counter()
    stages = [
        {"name": "Understand", "detail": "Identify the goal, state, and relevant parts."},
        {"name": "Compose", "detail": "Combine tools, memory, retrieval, and specialist workflows."},
        {"name": "Review", "detail": "Check the result for clarity, safety, and completeness."},
    ]
    return jsonify(
        {
            "task": task,
            "status": "completed",
            "elapsed_ms": round((perf_counter() - started) * 1000, 2),
            "active_parts": 7,
            "stages": stages,
            "answer": "The collection progresses from agent fundamentals in Part 1 to multi-agent orchestration in Part 7. Parts 8 to 10 are reserved for the next stages of the series.",
        }
    )


if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5001")),
        debug=os.environ.get("FLASK_DEBUG", "1") == "1",
    )
