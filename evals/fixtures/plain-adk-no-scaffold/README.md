# Support assistant

Customer-support assistant for Harbour Outfitters, built on Google ADK. The account summary
flow reads a customer's recent orders and open support tickets and summarises them for the
customer.

- `app/summary.py`: the account summary flow (two readers, then the summary agent).
- `app/tools/`: tool functions (no ADK imports, so the unit tests load them without the SDK).
- `app/http_server.py`: our own small HTTP front end (standard library `http.server`), run
  by `Dockerfile` on Cloud Run with `deploy/service.yaml`.

Install with `pip install -r requirements.txt`. Tests: `python -m unittest discover -s tests -t .`
google-adk is pinned in requirements.txt but is not installed in this environment.
