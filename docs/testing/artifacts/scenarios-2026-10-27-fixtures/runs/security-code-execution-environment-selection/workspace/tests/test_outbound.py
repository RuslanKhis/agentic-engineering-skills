"""Outbound traffic: what the tools may send, and where uploaded data can go."""
import sys
import types
import unittest
from unittest import mock

from app.tools import reports, uploads
from tests.helpers import NoNetworkTestCase


class EmailRecipientTests(NoNetworkTestCase):
    def send(self, to, subject="s", body="b"):
        with mock.patch("smtplib.SMTP") as smtp:
            result = reports.email_report(to, subject, body)
        return result, smtp

    def test_external_and_malformed_recipients_never_reach_smtp(self):
        bad = [
            "attacker@evil.example",
            "uw@fjord.example.evil.example",
            "uw@evilfjord.example",
            "uw@fjord.example, attacker@evil.example",
            "uw@fjord.example;attacker@evil.example",
            "Boss <uw@fjord.example>",
            "attacker@evil.example\r\nBcc: x@y",
            "uw@fjord.example\nBcc: attacker@evil.example",
            "a@b@fjord.example",
            "no-at-sign",
            "",
        ]
        for to in bad:
            with self.subTest(to=to):
                result, smtp = self.send(to)
                self.assertEqual(result["status"], "error")
                smtp.assert_not_called()

    def test_company_recipient_sends_exactly_one_message(self):
        result, smtp = self.send("Uw-Lead@Fjord.Example")
        self.assertEqual(result, {"status": "sent"})
        smtp.return_value.__enter__.return_value.send_message.assert_called_once()

    def test_subject_cannot_inject_headers(self):
        _, smtp = self.send("uw@fjord.example", subject="hi\r\nBcc: attacker@evil.example")
        sent = smtp.return_value.__enter__.return_value.send_message.call_args[0][0]
        self.assertIsNone(sent["Bcc"])
        self.assertNotIn("\n", sent["Subject"])


def _fake_sdk(blobs, state_files):
    """Fakes for google.cloud.storage and the ADK staging API; only the shapes this tool uses."""
    class File:
        def __init__(self, name, content, mime_type):
            self.name, self.content, self.mime_type = name, content, mime_type

    class CodeExecutorContext:
        def __init__(self, state):
            self.state = state

        def add_input_files(self, files):
            state_files.extend(files)

    class Client:
        def bucket(self, name):
            bucket = mock.Mock()
            bucket.name = name
            bucket.list_blobs.side_effect = lambda prefix: [b for b in blobs if b.name.startswith(prefix)]
            self.bucket_used = bucket
            return bucket

    def mod(name, **attrs):
        m = types.ModuleType(name)
        m.__dict__.update(attrs)
        return m

    return {
        "google": mod("google", __path__=[]),
        "google.adk": mod("google.adk", __path__=[]),
        "google.adk.code_executors": mod("google.adk.code_executors", __path__=[]),
        "google.adk.code_executors.code_execution_utils": mod("x", File=File),
        "google.adk.code_executors.code_executor_context": mod("y", CodeExecutorContext=CodeExecutorContext),
        "google.cloud": mod("google.cloud", __path__=[]),
        "google.cloud.storage": mod("google.cloud.storage", Client=Client),
    }


def _blob(name, data=b"a,b\n1,2\n", size=None):
    b = mock.Mock()
    b.name = name
    b.size = len(data) if size is None else size
    b.download_as_bytes.return_value = data
    return b


class DownloadStagingTests(NoNetworkTestCase):
    def run_tool(self, upload_id, blobs):
        staged = []
        with mock.patch.dict(sys.modules, _fake_sdk(blobs, staged)), \
                mock.patch("pathlib.Path.write_bytes") as wb, mock.patch("pathlib.Path.mkdir") as mk:
            result = uploads.download_upload(upload_id, mock.Mock(state={}))
        wb.assert_not_called()
        mk.assert_not_called()
        return result, staged

    def test_file_is_staged_in_session_state_not_on_disk(self):
        result, staged = self.run_tool("up-55120", [_blob("up-55120/claims.csv")])
        self.assertEqual(result, {"status": "ok", "file": "claims.csv"})
        self.assertEqual([f.name for f in staged], ["claims.csv"])
        self.assertEqual(staged[0].mime_type, "text/csv")

    def test_result_exposes_no_path_or_bucket(self):
        result, _ = self.run_tool("up-55120", [_blob("up-55120/claims.csv")])
        self.assertEqual(set(result), {"status", "file"})

    def test_malformed_upload_ids_are_refused_before_any_storage_call(self):
        for bad in ("", "up-", "../up-1", "up-1/../up-2", "up-1/", "up-55120\n", "UP-1", "up-1 ", "up-" + "9" * 13):
            with self.subTest(upload_id=bad):
                result, staged = self.run_tool(bad, [_blob("up-1/a.csv")])
                self.assertEqual(result["status"], "error")
                self.assertEqual(staged, [])

    def test_path_components_in_blob_name_are_dropped(self):
        result, staged = self.run_tool("up-1", [_blob("up-1/../../etc/passwd")])
        self.assertEqual(result["file"], "passwd")
        self.assertEqual(staged[0].name, "passwd")

    def test_oversized_upload_is_not_downloaded(self):
        big = _blob("up-1/big.csv", size=uploads.MAX_BYTES + 1)
        result, staged = self.run_tool("up-1", [big])
        self.assertEqual(result["status"], "error")
        big.download_as_bytes.assert_not_called()
        self.assertEqual(staged, [])

    def test_unknown_upload_is_an_error(self):
        result, _ = self.run_tool("up-9", [])
        self.assertEqual(result["status"], "error")


class OutboundSurfaceTests(unittest.TestCase):
    """Static inventory of outbound-capable code in app/: a new channel must be a conscious change."""

    def test_only_the_reviewed_modules_use_network_libraries(self):
        from tests.helpers import app_sources, imported_and_named, ROOT
        network = {"smtplib", "requests", "httpx", "urllib", "urllib3", "aiohttp", "socket", "http",
                   "ftplib", "websockets", "paramiko", "storage"}
        allowed = {"app/tools/reports.py": {"smtplib"}, "app/tools/uploads.py": {"storage"}}
        for path, source in app_sources().items():
            rel = str(path.relative_to(ROOT))
            used = {n.split(".")[0] for n in imported_and_named(source)} & network
            self.assertLessEqual(used, allowed.get(rel, set()), f"{rel} uses {used}")


if __name__ == "__main__":
    unittest.main()
