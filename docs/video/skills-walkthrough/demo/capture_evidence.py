"""Replay the real local HTTP endpoints and extract verbatim source excerpts."""
import http.client
import inspect
import json
import platform
import textwrap
import threading
from pathlib import Path

from app import App, make_server

ROOT = Path(__file__).parent


def excerpt(method):
    return {"file": "app.py", "lines": textwrap.dedent(inspect.getsource(method)).strip().splitlines()}


def main():
    app = App()
    server = make_server(app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def request(method, path, body):
        connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
        connection.request(method, path, json.dumps(body),
                           {"Authorization": "Bearer demo-alice", "Content-Type": "application/json"})
        response = connection.getresponse()
        assert response.status == 200, response.read()
        data = response.read().decode()
        connection.close()
        return data

    try:
        question = "Where is my order?"
        first = [json.loads(line) for line in request("POST", "/api/chat", {"message": question}).splitlines()]
        saved = json.loads(request("PUT", "/api/preference", {"language": "Spanish", "consent": True}))
        second = [json.loads(line) for line in request("POST", "/api/chat", {"message": question}).splitlines()]
        assert first[0]["session_id"] != second[0]["session_id"]
        frontend_lines = (ROOT / "Chat.jsx").read_text().splitlines()
        start = frontend_lines.index("        if (e.type === 'text')")
        frontend = textwrap.dedent("\n".join(frontend_lines[start:start + 6])).splitlines()
        ownership_lines = inspect.getsource(App.prepare_chat).splitlines()
        owner_start = ownership_lines.index("        with self.lock:")
        ownership = textwrap.dedent("\n".join(
            ownership_lines[owner_start:owner_start + 7]
        )).splitlines()
        backend = {"file": "app.py", "lines": ownership}
        assert "Ran 19 tests" in (ROOT / "test-report.txt").read_text()
        assert (ROOT / "test-report.txt").read_text().strip().endswith("OK")
        assert "# pass 6" in (ROOT / "client-test-report.txt").read_text()
        evidence = {
            "backend": backend,
            "frontend": {"file": "Chat.jsx", "lines": frontend, "scope": "Integration excerpt, not compiled"},
            "memory_save": excerpt(App.remember),
            "memory_load": excerpt(App.language_for),
            "replay": {"question": question,
                       "progress": next(e["label"] for e in first if e["type"] == "tool"),
                       "answer": "".join(e.get("text", "") for e in first).strip(),
                       "spanish_answer": "".join(e.get("text", "") for e in second).strip()},
            "tests": {"passed": 25, "http_python": 19, "javascript_stream_helper": 6},
            "python_version": platform.python_version(),
            "scope": "Real localhost HTTP, SQLite and JS stream helper; deterministic model/ADK event double. React rendering not tested.",
            "first_conversation": first,
            "saved_preference": saved,
            "new_conversation": second,
        }
        (ROOT / "video-evidence.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(evidence["replay"], ensure_ascii=False))
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
        app.db.close()


if __name__ == "__main__":
    main()
