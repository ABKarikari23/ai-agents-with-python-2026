"""Simple local web interface for the Part 7 multi-agent system."""

from __future__ import annotations

import os

from flask import Flask, jsonify, render_template, request

from orchestrator import Orchestrator

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["TITLE"] = "AI Agent State Monitor"
app.config["PART"] = "Part 7"


@app.get("/")
def index():
    return render_template("index.html", title=app.config["TITLE"], part=app.config["PART"])


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
