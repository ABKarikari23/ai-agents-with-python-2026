# AI Agents with Python: Main Dashboard

This is the canonical project display for the article series. It shows Parts 1-9 as published and Part 10 as the current final chapter: a complete, knowledge-powered agent project.

The dashboard is intentionally independent from an individual article so it can be tested locally now and deployed online after the series is complete.

## Run locally

From the repository root:

```bash
cd dashboard
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5001`.

## Deploy

The app reads `HOST`, `PORT`, and `FLASK_DEBUG` from the environment. A production WSGI command is:

```bash
waitress-serve --listen=*:5001 app:app
```

For a platform that supplies its own port, use:

```bash
waitress-serve --listen=*:$(PORT) app:app
```

## Updating each week

When an article is published, update its entry in `dashboard/app.py` and keep the published/current counts derived from the series metadata.

## API

- `GET /api/series` returns the series metadata.
- `POST /api/demo` runs the display workflow for a supplied `task`.
