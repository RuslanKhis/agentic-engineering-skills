# Working on this repository

- Python 3.12, pip with `requirements.txt` (pinned). No other package manager.
- Tests: `python -m unittest discover -s tests -t .`.
- Keep `google.adk` imports out of `app/__init__.py`, `app/tools/` and `app/clients/`.
- Public interfaces: the `/summary` and `/chat` HTTP routes and their JSON shapes, and
  `app.summary.build_summary_flow()`. Deployment is `Dockerfile` + `deploy/service.yaml`.
- The user ID comes from the verified principal (`app/auth.py`), never from the request body.
