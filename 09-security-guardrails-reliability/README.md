# Part 9: Security, Guardrails and Reliability in AI Agents

> Part of the **AI Agents with Python 2026** series (Wednesdays).
> Companion article: *(add your LinkedIn/blog article link here)*

## What this covers

This part covers the safeguards that matter most when agents become more autonomous: permission checks, prompt injection defenses, validation rules, and reliability patterns that keep systems within safe operating bounds.

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

The demo registers a read-only metrics tool and an approval-gated service
restart. It demonstrates role-based authorization, allowlisted arguments, and
a limit on total tool proposals. The approval flag is simulated locally; a
production system must verify a trusted approval record tied to the exact
action and resource.

Run the guardrail tests with:

```bash
python -m unittest test_part9.py
```

## Notes

View this part alongside the full collection in the [main project dashboard](../dashboard).

This example illustrates guardrails in code so you can see how to validate inputs, limit actions, and fail safely when a request is unsafe or ambiguous.
