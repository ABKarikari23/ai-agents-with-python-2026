# Part 2: How AI Agents Work — Models, Tools, State, Memory and Agent Loops

> Part of the **AI Agents with Python 2026** series (Wednesdays).
> Companion article: *(add your LinkedIn/blog article link here)*

## What this covers

This part explains the mechanics behind an agent: the model, the tool layer, short-term state, memory, and the ongoing loop that decides what to do next based on the current task and results.

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

The code here keeps the logic local and readable so the agent loop remains understandable before you connect it to real models or APIs.
