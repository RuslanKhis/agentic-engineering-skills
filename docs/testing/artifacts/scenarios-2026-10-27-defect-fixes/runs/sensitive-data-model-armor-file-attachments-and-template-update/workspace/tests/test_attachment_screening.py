import base64
import io
import unittest
import zipfile
from types import SimpleNamespace

from claims_agent import config, screening
from claims_agent.attachments import AttachmentRejected, accept_attachment, detect_kind
from claims_agent.screening import ALLOW, BLOCK, INDETERMINATE, screen_attachments, screen_file, screen_inline_files
from tests.armor_double import FakeArmorClient, FilterMatchState, InvocationResult, sdk

DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
PDF = b"%PDF-1.7\n" + b"x" * 100


def make_docx(extra=()):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("word/document.xml", "<w:document/>")
        for name in extra:
            z.writestr(name, "x")
    return buf.getvalue()


def make_xlsx():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("xl/workbook.xml", "<workbook/>")
    return buf.getvalue()


class UploadTests(unittest.TestCase):
    def test_pdf_and_docx_accepted_with_kind(self):
        self.assertEqual(accept_attachment("a.pdf", "application/pdf", PDF).kind, "PDF")
        self.assertEqual(accept_attachment("a.docx", DOCX, make_docx()).kind, "WORD_DOCUMENT")

    def test_declared_type_must_match_contents(self):
        with self.assertRaises(AttachmentRejected):
            accept_attachment("a.pdf", "application/pdf", make_docx())
        with self.assertRaises(AttachmentRejected):
            accept_attachment("a.docx", DOCX, make_xlsx())  # a zip, but not a Word file
        with self.assertRaises(AttachmentRejected):
            accept_attachment("a.docx", DOCX, b"PK\x03\x04 not really a zip")

    def test_photos_refused_until_template_has_image_modality(self):
        with self.assertRaises(AttachmentRejected):
            accept_attachment("a.png", "image/png", b"\x89PNG\r\n\x1a\n" + b"0" * 100)

    def test_documents_outside_screenable_size_refused(self):
        with self.assertRaises(AttachmentRejected):
            accept_attachment("t.pdf", "application/pdf", b"%PDF-1.7")  # under 69 bytes
        big = b"%PDF-1.7\n" + b"0" * config.SCREENABLE_FILE_MAX_BYTES
        self.assertLess(len(big), config.MAX_ATTACHMENT_BYTES)
        with self.assertRaises(AttachmentRejected):
            accept_attachment("big.pdf", "application/pdf", big)

    def test_detect_kind(self):
        self.assertEqual(detect_kind(PDF), "PDF")
        self.assertIsNone(detect_kind(b"MZ" + b"0" * 100))


class ScreenFileTests(unittest.TestCase):
    def setUp(self):
        screening._allowed_files.clear()

    def test_allow_sends_typed_bytes_to_the_input_template(self):
        client = FakeArmorClient()
        self.assertEqual(screen_file("PDF", PDF, client, sdk).decision, ALLOW)
        request = client.requests[0]
        self.assertEqual(request.name, config.INPUT_TEMPLATE)
        item = request.user_prompt_data.byte_item
        self.assertEqual(item.byte_data_type, sdk.ByteDataItem.ByteItemType.PDF)
        self.assertEqual(item.byte_data, PDF)
        self.assertEqual(client.kwargs[0], {"timeout": config.SCREEN_FILE_TIMEOUT_S})

    def test_base64_encoding_is_a_single_switch(self):
        old, config.BYTE_DATA_ENCODING = config.BYTE_DATA_ENCODING, "base64"
        try:
            client = FakeArmorClient()
            screen_file("PDF", PDF, client, sdk)
        finally:
            config.BYTE_DATA_ENCODING = old
        self.assertEqual(client.requests[0].user_prompt_data.byte_item.byte_data, base64.b64encode(PDF))

    def test_match_blocks(self):
        client = FakeArmorClient(FilterMatchState.MATCH_FOUND)
        self.assertEqual(screen_file("PDF", PDF, client, sdk).decision, BLOCK)

    def test_anything_unproven_is_indeterminate(self):
        cases = {
            "error": FakeArmorClient(error=TimeoutError()),
            "empty": FakeArmorClient(empty=True),
            "unspecified": FakeArmorClient(FilterMatchState.FILTER_MATCH_STATE_UNSPECIFIED),
            "partial": FakeArmorClient(invocation=InvocationResult.PARTIAL),
            "no filter results": FakeArmorClient(filter_results={}),
            "sdp missing": FakeArmorClient(filter_results={"rai": 1, "pi_and_jailbreak": 1, "malicious_uris": 1}),
        }
        for name, client in cases.items():
            with self.subTest(name):
                self.assertEqual(screen_file("PDF", PDF, client, sdk).decision, INDETERMINATE)

    def test_unscreenable_files_never_reach_the_service(self):
        client = FakeArmorClient()
        for kind, data in [("IMAGE", PDF), ("", PDF), ("PDF", b"%PDF-"),
                           ("PDF", b"0" * (config.SCREENABLE_FILE_MAX_BYTES + 1))]:
            self.assertEqual(screen_file(kind, data, client, sdk).decision, INDETERMINATE)
        self.assertEqual(client.requests, [])

    def test_only_allowed_files_are_cached(self):
        blocked = FakeArmorClient(FilterMatchState.MATCH_FOUND)
        screen_file("PDF", PDF, blocked, sdk)
        again = FakeArmorClient(FilterMatchState.MATCH_FOUND)
        self.assertEqual(screen_file("PDF", PDF, again, sdk).decision, BLOCK)
        self.assertEqual(len(again.requests), 1)
        ok = FakeArmorClient()
        screen_file("PDF", PDF, ok, sdk)
        screen_file("PDF", PDF, ok, sdk)
        self.assertEqual(len(ok.requests), 1)


class BoundaryCanaryTests(unittest.TestCase):
    """A blocked or unscreened file must stop the turn before anything is built from its bytes."""

    def setUp(self):
        screening._allowed_files.clear()

    def test_one_bad_attachment_stops_the_batch(self):
        good = accept_attachment("a.pdf", "application/pdf", PDF)
        bad = accept_attachment("b.docx", DOCX, make_docx(["word/other.xml"]))
        client = FakeArmorClient(FilterMatchState.MATCH_FOUND)
        self.assertEqual(screen_attachments([good, bad], client, sdk).decision, BLOCK)
        self.assertEqual(len(client.requests), 1)

    def test_screening_outage_withholds(self):
        att = accept_attachment("a.pdf", "application/pdf", PDF)
        client = FakeArmorClient(error=ConnectionError())
        self.assertEqual(screen_attachments([att], client, sdk).decision, INDETERMINATE)

    def test_no_attachments_makes_no_call(self):
        client = FakeArmorClient()
        self.assertEqual(screen_attachments([], client, sdk).decision, ALLOW)
        self.assertEqual(client.requests, [])

    def test_history_files_are_screened_before_the_model(self):
        blob = SimpleNamespace(data=PDF, mime_type="application/pdf")
        contents = [SimpleNamespace(role="user", parts=[SimpleNamespace(text="hi", inline_data=None),
                                                        SimpleNamespace(text=None, inline_data=blob)])]
        client = FakeArmorClient(FilterMatchState.MATCH_FOUND)
        self.assertEqual(screen_inline_files(contents, client, sdk).decision, BLOCK)
        self.assertEqual(screen_inline_files([SimpleNamespace(role="user", parts=[
            SimpleNamespace(text=None, inline_data=SimpleNamespace(data=b"junk", mime_type="x"))])],
            client, sdk).decision, INDETERMINATE)

    def test_text_only_requests_are_untouched(self):
        client = FakeArmorClient()
        contents = [SimpleNamespace(role="user", parts=[SimpleNamespace(text="hi", inline_data=None)])]
        self.assertEqual(screen_inline_files(contents, client, sdk).decision, ALLOW)
        self.assertEqual(client.requests, [])


if __name__ == "__main__":
    unittest.main()
