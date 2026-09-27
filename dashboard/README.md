# AI Agents with Python: Main Dashboard

This is the canonical project display for the article series. It shows the published journey through Parts 1-7, the current Part 7 multi-agent milestone, and the upcoming Parts 8-10.

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

When a new article is published, update the matching entry in `dashboard/app.py` from `upcoming` to `published` or `current`, then update the article's README link if its folder changes. The dashboard is the only display app that needs to be maintained.

## API

- `GET /api/series` returns the series metadata.
- `POST /api/demo` runs the display workflow for a supplied `task`.
