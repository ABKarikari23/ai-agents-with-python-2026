"""Simple local web interface for the Part 7 multi-agent system."""

from __future__ import annotations

import os

from flask import Flask, jsonify, render_template, request

from orchestrator import Orchestrator

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["TITLE"] = "AI Agents with Python"
app.config["PART"] = "Part 1 to 7 collection"
app.config["SERIES_PARTS"] = [
    {
        "number": 1,
        "title": "What Are AI Agents?",
        "folder": "01-what-are-ai-agents",
        "status": "available",
    },
    {
        "number": 2,
        "title": "How AI Agents Work",
        "folder": "02-how-ai-agents-work",
        "status": "available",
    },
    {
        "number": 3,
        "title": "Building Your First Simple AI Agent",
        "folder": "03-first-simple-agent",
        "status": "available",
    },
    {
        "number": 4,
        "title": "Giving AI Agents Tools",
        "folder": "04-giving-agents-tools",
        "status": "available",
    },
    {
        "number": 5,
        "title": "Adding Memory and Context",
        "folder": "05-memory-and-context",
        "status": "available",
    },
    {
        "number": 6,
        "title": "RAG + AI Agents",
        "folder": "06-rag-plus-agents",
        "status": "available",
    },
    {
        "number": 7,
        "title": "Multi-Agent Systems",
        "folder": "07-multi-agent-systems",
        "status": "active",
    },
]


@app.get("/")
def index():
    return render_template(
        "index.html",
        title=app.config["TITLE"],
        part=app.config["PART"],
        series_parts=app.config["SERIES_PARTS"],
    )


@app.post("/run")
def run_workflow():
    payload = request.get_json(silent=True) or {}
    task = payload.get("task") or "Explain how AI agents use Python tools safely and effectively."

    result = Orchestrator().run(task)

    return jsonify(
        {
            "task": result.task,
            "status": result.status,
            "research": result.research,
            "draft": result.draft,
            "review": result.review,
            "errors": result.errors,
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(debug=debug, host=host, port=port)
