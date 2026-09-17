import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest

from app import App, DemoRunner, make_server


class DemoTests(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.server = make_server(self.app)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.app.db.close()

    def request(self, method, path, body=None, token="demo-alice"):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        headers = {"Content-Type": "application/json"}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        connection.request(method, path, None if body is None else json.dumps(body), headers)
        response = connection.getresponse()
        payload = response.read().decode()
        status = response.status
        connection.close()
        return status, payload

    def chat(self, body=None, token="demo-alice"):
        status, data = self.request("POST", "/api/chat", body or {"message": "Where is my order?"}, token)
        return status, [json.loads(line) for line in data.splitlines()]

    def test_complete_reply_and_tool(self):
        status, events = self.chat()
        self.assertEqual(status, 200)
        self.assertEqual(events[-1], {"type": "done"})
        self.assertIn({"type": "tool", "label": "Order checked"}, events)
        self.assertEqual("".join(e.get("text", "") for e in events).strip(),
                         "Your order arrives on Friday.")

    def test_no_thought_or_duplicated_aggregate(self):
        _, events = self.chat()
        self.assertNotIn("Private", json.dumps(events))
        self.assertEqual(sum(e.get("text", "").count("Friday") for e in events), 1)

    def test_missing_auth_never_invokes(self):
        self.assertEqual(self.chat(token=None)[0], 401)
        self.assertEqual(self.app.runner.calls, 0)
        self.assertEqual(self.app.sessions, {})

    def test_invalid_auth_never_invokes(self):
        self.assertEqual(self.chat(token="forged")[0], 401)
        self.assertEqual(self.app.runner.calls, 0)

    def test_client_cannot_select_owner(self):
        status, _ = self.chat({"message": "Hi", "owner": "bob"})
        self.assertEqual(status, 422)
        self.assertEqual(self.app.runner.calls, 0)

    def test_foreign_session_is_unavailable(self):
        _, events = self.chat()
        status, _ = self.chat({"message": "Hi", "session_id": events[0]["session_id"]}, "demo-bob")
        self.assertEqual(status, 404)
        self.assertEqual(self.app.runner.calls, 1)

    def test_unknown_session_is_not_created(self):
        status, _ = self.chat({"message": "Hi", "session_id": "missing"})
        self.assertEqual(status, 404)
        self.assertEqual(self.app.sessions, {})
        self.assertEqual(self.app.runner.calls, 0)

    def test_owned_session_continues(self):
        _, first = self.chat()
        _, second = self.chat({"message": "Hi", "session_id": first[0]["session_id"]})
        self.assertEqual(first[0], second[0])

    def test_input_limits_reject_before_invocation(self):
        for message in ("", " " * 10, "x" * 2001, None):
            self.assertEqual(self.chat({"message": message})[0], 422)
        self.assertEqual(self.app.runner.calls, 0)

    def test_consent_denial_does_not_persist(self):
        status, _ = self.request("PUT", "/api/preference", {"language": "Spanish", "consent": False})
        self.assertEqual(status, 422)
        self.assertEqual(self.app.language_for("alice"), "English")

    def test_truthy_strings_are_not_consent(self):
        status, _ = self.request("PUT", "/api/preference", {"language": "Spanish", "consent": "true"})
        self.assertEqual(status, 422)
        self.assertEqual(self.app.language_for("alice"), "English")

    def test_preference_restored_for_new_conversation(self):
        _, first = self.chat()
        self.request("PUT", "/api/preference", {"language": "Spanish", "consent": True})
        _, second = self.chat()
        self.assertNotEqual(first[0], second[0])
        self.assertEqual("".join(e.get("text", "") for e in second).strip(),
                         "Tu pedido llega el viernes.")

    def test_preference_does_not_cross_users(self):
        self.request("PUT", "/api/preference", {"language": "Spanish", "consent": True})
        _, events = self.chat(token="demo-bob")
        self.assertIn("Your order", "".join(e.get("text", "") for e in events))

    def test_preference_correction_and_erasure(self):
        self.request("PUT", "/api/preference", {"language": "Spanish", "consent": True})
        self.request("PUT", "/api/preference", {"language": "English", "consent": True})
        self.assertEqual(self.app.language_for("alice"), "English")
        self.request("DELETE", "/api/preference")
        self.assertEqual(self.app.db.execute("SELECT count(*) FROM preferences").fetchone()[0], 0)

    def test_invalid_preference_is_not_stored(self):
        status, _ = self.request("PUT", "/api/preference", {"language": "garbage", "consent": True})
        self.assertEqual(status, 422)
        self.assertEqual(self.app.language_for("alice"), "English")

    def test_profile_persists_after_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "profile.sqlite")
            first = App(path)
            first.save_preference("alice", {"language": "Spanish", "consent": True})
            first.db.close()
            second = App(path)
            self.assertEqual(second.language_for("alice"), "Spanish")
            second.db.close()

    def test_late_error_never_emits_done(self):
        class BrokenRunner:
            def run(self, **kwargs):
                yield {"kind": "text", "text": "A partial reply"}
                yield {"kind": "error", "message": "PRIVATE_PROVIDER_DIAGNOSTIC"}
        self.app.runner = BrokenRunner()
        _, events = self.chat()
        self.assertEqual(events[-1]["type"], "error")
        self.assertNotIn({"type": "done"}, events)
        self.assertNotIn("PRIVATE_PROVIDER", json.dumps(events))

    def test_empty_provider_is_error(self):
        class EmptyRunner:
            def run(self, **kwargs):
                yield {"kind": "thought", "text": "Hidden"}
        self.app.runner = EmptyRunner()
        _, events = self.chat()
        self.assertEqual(events[-1]["type"], "error")

    def test_first_frame_arrives_before_provider_completion(self):
        release = threading.Event()
        class PausedRunner:
            def run(self, **kwargs):
                yield {"kind": "text", "text": "Hello"}
                release.wait(2)
        self.app.runner = PausedRunner()
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)
        try:
            connection.request("POST", "/api/chat", json.dumps({"message": "Hi"}),
                               {"Authorization": "Bearer demo-alice", "Content-Type": "application/json"})
            response = connection.getresponse()
            first = json.loads(response.readline())
            second = json.loads(response.readline())
            self.assertEqual(first["type"], "session")
            self.assertEqual(second["type"], "text")
            self.assertFalse(release.is_set())
            release.set()
            self.assertIn(b'"done"', response.read())
        finally:
            release.set()
            connection.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
