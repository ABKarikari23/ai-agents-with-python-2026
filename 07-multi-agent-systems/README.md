# Part 7: Multi-Agent Systems — How Specialized Agents Coordinate

> Part of the **AI Agents with Python 2026** series (Wednesdays).
> Companion article: *(add your LinkedIn/blog article link here)*

## What this covers

This part explains how multiple specialized agents can work together: one planning, one researching, one writing, and one checking quality. The idea is to split tasks across roles instead of putting everything into one model.

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

The sample demonstrates coordination patterns without needing a distributed runtime or external orchestration framework.
