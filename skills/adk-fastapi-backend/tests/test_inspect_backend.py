"""Exercise the backend inspector through its CLI on synthetic projects."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_backend.py"

LOCK = """version = 1
[[package]]
name = "fastapi"
version = "{fastapi}"
[[package]]
name = "google-adk"
version = "2.12.0"
"""

UNSAFE_MAIN = """from fastapi import FastAPI, BackgroundTasks
from google.adk.cli.fast_api import get_fast_api_app
from fastapi.middleware.cors import CORSMiddleware
app = get_fast_api_app(agents_dir=".", web=True)
app.add_middleware(CORSMiddleware, allow_origins=["*"])
async def run(body, tasks: BackgroundTasks):
    email = request.headers["X-Goog-Authenticated-User-Email"]
    runner.run_async(user_id=body.user_id, session_id=body.session_id)
"""

SAFE_MAIN = """from fastapi import FastAPI
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
assertion = request.headers.get("x-goog-iap-jwt-assertion")
runner.run_async(user_id=request.state.principal.subject, session_id=sid)
app.frontend("/", directory="dist")
"""


class InspectBackendTests(unittest.TestCase):
    def run_tool(self, project, *extra):
        proc = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "--project", str(project), *extra],
                              capture_output=True, text=True)
        return proc.returncode, proc.stdout, proc.stderr

    def project(self, root, files):
        for name, text in files.items():
            path = Path(root) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        return Path(root)

    def test_feature_matrix_follows_the_locked_fastapi(self):
        with tempfile.TemporaryDirectory() as root:
            self.project(root, {"uv.lock": LOCK.format(fastapi="0.141.1"),
                                "pyproject.toml": '[project]\nname="x"\ndependencies=["fastapi>=0.138", "google-adk==2.12.0"]\n'})
            code, out, err = self.run_tool(root)
            self.assertEqual(code, 0, err)
            report = json.loads(out)
            self.assertEqual(report["project"]["resolved"], {"fastapi": "0.141.1", "google-adk": "2.12.0"})
            self.assertEqual(report["project"]["declared"]["fastapi"], {"pyproject.toml": ">=0.138"})
            available = {f["needs"]: f["available"] for f in report["fastapi_features"]}
            self.assertEqual(available, {"0.135": True, "0.138": True, "0.142": False, "0.143": False})
            self.assertTrue(any("opentelemetry-api<=1.42.1" in n for n in report["notes"]))

    def test_unknown_version_leaves_features_undecided(self):
        with tempfile.TemporaryDirectory() as root:
            self.project(root, {"requirements.txt": "fastapi\n"})
            report = json.loads(self.run_tool(root)[1])
            self.assertEqual({f["available"] for f in report["fastapi_features"]}, {None})
            self.assertEqual(report["project"]["declared"]["fastapi"], {"requirements.txt": "(any)"})

    def test_unsafe_backend_patterns_are_reported(self):
        with tempfile.TemporaryDirectory() as root:
            self.project(root, {"app/main.py": UNSAFE_MAIN,
                                "Dockerfile": 'CMD ["fastapi", "run", "--workers", "4"]\n',
                                "Makefile": "dev:\n\tadk api_server --allow_origins='*' .\n",
                                "migrations/env.py": "context.configure(target_metadata=Base.metadata)\n",
                                "app/sessions.py": "svc = DatabaseSessionService(db_url)\n"})
            report = json.loads(self.run_tool(root)[1])
            rules = {(f["rule"], f["file"]) for f in report["project"]["findings"]}
            for expected in [("adk_server_exposed", "app/main.py"), ("wildcard_cors", "app/main.py"),
                             ("background_tasks", "app/main.py"), ("unsigned_iap_header", "app/main.py"),
                             ("client_user_id", "app/main.py"), ("multiple_workers", "Dockerfile"),
                             ("adk_cli_server", "Makefile"), ("wildcard_cors", "Makefile"),
                             ("migrations_without_filter", "migrations/env.py"),
                             ("database_sessions", "app/sessions.py")]:
                self.assertIn(expected, rules)

    def test_safe_backend_has_only_the_frontend_pointer(self):
        with tempfile.TemporaryDirectory() as root:
            self.project(root, {"app/main.py": SAFE_MAIN,
                                "migrations/env.py": "context.configure(include_object=include_object)\n"})
            report = json.loads(self.run_tool(root)[1])
            self.assertEqual([f["rule"] for f in report["project"]["findings"]], ["frontend_fallback"])
            self.assertEqual(report["project"]["signals"]["iap_assertion"], ["app/main.py"])
            self.assertTrue(report["project"]["alembic_env_found"])

    def test_env_files_symlinks_and_vendored_dirs_are_never_read(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as outside:
            secret = "sk-test-DO-NOT-PRINT"
            self.project(root, {".env": f"APP_KEY={secret}\nallow_origins=['*']\n",
                                "node_modules/pkg/x.py": UNSAFE_MAIN, ".venv/lib/y.py": UNSAFE_MAIN})
            Path(outside, "evil.py").write_text(UNSAFE_MAIN)
            Path(root, "link.py").symlink_to(Path(outside, "evil.py"))
            code, out, _ = self.run_tool(root)
            self.assertEqual(code, 0)
            self.assertNotIn(secret, out)
            self.assertEqual(json.loads(out)["project"]["findings"], [])

    def test_dry_run_is_identical_and_invalid_input_exits_2(self):
        with tempfile.TemporaryDirectory() as root:
            self.project(root, {"app/main.py": SAFE_MAIN})
            self.assertEqual(self.run_tool(root)[1], self.run_tool(root, "--dry-run")[1])
            self.assertEqual(self.run_tool(Path(root) / "missing")[0], 2)
            proc = subprocess.run([sys.executable, str(SCRIPT), "--project", root, "--token=secret"],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 2)
            self.assertNotIn("secret", proc.stderr)

    def test_unparseable_manifest_marks_inspection_incomplete(self):
        with tempfile.TemporaryDirectory() as root:
            self.project(root, {"pyproject.toml": "[project\n"})
            code, out, _ = self.run_tool(root)
            self.assertEqual(code, 4)
            self.assertIn("manifest_unparsed", json.loads(out)["project"]["warnings"])


if __name__ == "__main__":
    unittest.main()
