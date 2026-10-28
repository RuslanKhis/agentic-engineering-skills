"""Offline checks for the source freshness report; no network calls."""

from contextlib import redirect_stderr, redirect_stdout
from datetime import date
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_source_freshness.py"
spec = importlib.util.spec_from_file_location("check_source_freshness", SCRIPT)
freshness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(freshness)

TODAY = "2026-10-24"


def source(**overrides):
    value = {"id": "example", "repo": "owner/example", "pinned": "abc1234",
             "read": "2026-10-22", "licence": "MIT", "note": "docs/note.md",
             "used_by": ["example-skill"]}
    value.update(overrides)
    return value


def article(**overrides):
    value = {"id": "an-article", "kind": "article", "url": "https://example.org/post",
             "pinned": None, "read": "2026-10-28",
             "licence": "n/a (article; cited, not copied)", "note": "docs/note.md",
             "used_by": ["example-skill"]}
    value.update(overrides)
    return value


def github(repo="owner/example", last="2026-10-20T10:00:00Z", archived=False,
           licence="MIT", release=True, compare_status=200, ahead=3):
    """A fake GitHub keyed by request path, shaped like the REST responses."""
    responses = {
        f"/repos/{repo}": (200, {"full_name": repo, "archived": archived,
                                 "license": {"spdx_id": licence}, "default_branch": "main"}),
        f"/repos/{repo}/commits?per_page=1&sha=main":
            (200, [{"commit": {"committer": {"date": last}}}]),
        f"/repos/{repo}/releases/latest":
            (200, {"tag_name": "v1.0.0", "published_at": "2026-10-01T00:00:00Z"})
            if release else (404, None),
        f"/repos/{repo}/compare/abc1234...main": (compare_status, {"ahead_by": ahead}),
    }
    calls = []

    def fetch(path):
        calls.append(path)
        return responses.get(path, (404, None))
    fetch.calls = calls
    return fetch


class FreshnessTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        (self.root / "skills/example-skill").mkdir(parents=True)
        (self.root / "skills/example-skill/SKILL.md").touch()
        (self.root / "docs").mkdir()
        (self.root / "docs/note.md").touch()
        self.register = self.root / "docs/register.json"
        self.write([source()])

    def tearDown(self):
        self.directory.cleanup()

    def write(self, sources):
        self.register.write_text(json.dumps({"version": 1, "sources": sources}))

    def run_main(self, *extra, fetch=None):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = freshness.main(["--root", str(self.root), "--register", str(self.register),
                                   "--today", TODAY, *extra], fetch=fetch)
        return code, out.getvalue(), err.getvalue()

    def test_active_source_with_release_and_pin_needs_nothing(self):
        code, out, _ = self.run_main(fetch=github())
        self.assertEqual(code, 0)
        self.assertIn("active", out)
        self.assertIn("+3 since read", out)
        self.assertIn("release v1.0.0 (2026-10-01)", out)

    def test_quiet_source_is_reported_but_not_flagged(self):
        code, out, _ = self.run_main(fetch=github(last="2026-08-04T00:00:00Z"))
        self.assertEqual(code, 0)
        self.assertIn("quiet", out)

    def test_stale_source_needs_attention(self):
        code, out, _ = self.run_main(fetch=github(last="2025-06-20T00:00:00Z"))
        self.assertEqual(code, 1)
        self.assertIn("stale", out)
        self.assertIn("no commit for 491 days", out)

    def test_thresholds_are_arguments(self):
        code, out, _ = self.run_main("--quiet-after-days", "2", "--stale-after-days", "3",
                                     fetch=github())
        self.assertEqual(code, 1)
        self.assertIn("stale", out)

    def test_archived_renamed_and_relicensed_need_attention(self):
        fetch = github(archived=True, licence="Apache-2.0")

        def both(path):
            if path == "/repos/owner/example":
                status, meta = fetch(path)
                return status, dict(meta, full_name="neworg/example")
            return fetch(path)
        code, out, _ = self.run_main(fetch=both)
        self.assertEqual(code, 1)
        self.assertIn("archived", out)
        self.assertIn("renamed to neworg/example", out)
        self.assertIn("licence changed from MIT to Apache-2.0", out)

    def test_missing_pin_and_missing_repository_need_attention(self):
        code, out, _ = self.run_main(fetch=github(compare_status=404))
        self.assertEqual(code, 1)
        self.assertIn("pinned commit abc1234 not found", out)
        code, out, _ = self.run_main(fetch=lambda path: (404, None))
        self.assertEqual(code, 1)
        self.assertIn("repository not found", out)

    def test_unpinned_source_skips_the_comparison(self):
        self.write([source(pinned=None)])
        fetch = github()
        code, out, _ = self.run_main(fetch=fetch)
        self.assertEqual(code, 0)
        self.assertNotIn("since read", out)
        self.assertFalse(any("/compare/" in call for call in fetch.calls))

    def test_rate_limit_marks_the_rest_unchecked_without_more_calls(self):
        self.write([source(), source(id="second", repo="owner/second")])
        calls = []

        def limited(path):
            calls.append(path)
            raise freshness.RateLimited("GitHub rate limit (403)")
        code, out, _ = self.run_main(fetch=limited)
        self.assertEqual(code, 3)
        self.assertEqual(len(calls), 1)
        self.assertEqual(out.count("UNCHECKED"), 2)

    def test_server_error_is_unchecked_not_clean(self):
        code, out, _ = self.run_main(fetch=lambda path: (500, None))
        self.assertEqual(code, 3)
        self.assertIn("HTTP 500", out)

    def test_json_output_and_only_filter(self):
        self.write([source(), source(id="second", repo="owner/second")])
        code, out, _ = self.run_main("--json", "--only", "example", fetch=github())
        self.assertEqual(code, 0)
        results = json.loads(out)
        self.assertEqual([r["id"] for r in results], ["example"])
        self.assertEqual(results[0]["band"], "active")

    def test_invalid_register_and_arguments_exit_2_without_fetching(self):
        def never(path):
            raise AssertionError("fetched")
        bad = [
            [source(), source(repo="owner/other")],
            [source(repo="not a repo")],
            [source(pinned="zzz")],
            [source(read="22 October")],
            [source(note="docs/missing.md")],
            [source(used_by=["no-such-skill"])],
            [dict(source(), extra=1)],
        ]
        for sources in bad:
            with self.subTest(sources=sources):
                self.write(sources)
                code, _, err = self.run_main(fetch=never)
                self.assertEqual(code, 2)
                self.assertTrue(err)
        self.write([source()])
        self.assertEqual(self.run_main("--only", "nope", fetch=never)[0], 2)
        self.assertEqual(self.run_main("--quiet-after-days", "400", fetch=never)[0], 2)
        self.assertEqual(self.run_main("--no-such-flag", fetch=never)[0], 2)

    def test_validate_only_never_fetches(self):
        def never(path):
            raise AssertionError("fetched")
        code, out, _ = self.run_main("--validate-only", fetch=never)
        self.assertEqual(code, 0)
        self.assertIn("nothing was fetched", out)

    def test_article_row_is_validated_but_never_fetched(self):
        self.write([source(), article()])
        fetch = github()
        code, out, _ = self.run_main(fetch=fetch)
        self.assertEqual(code, 0)
        self.assertIn("article", out)
        self.assertIn("checked by date only (read 2026-10-28)", out)
        self.assertFalse(any("example.org" in call or "an-article" in call
                             for call in fetch.calls))

    def test_article_alone_needs_no_network_and_survives_a_rate_limit(self):
        def never(path):
            raise AssertionError("fetched")
        self.write([article()])
        code, out, _ = self.run_main("--json", fetch=never)
        self.assertEqual(code, 0)
        result = json.loads(out)[0]
        self.assertEqual((result["band"], result["url"], result["repo"]),
                         ("article", "https://example.org/post", None))

        self.write([source(), article()])

        def limited(path):
            raise freshness.RateLimited("GitHub rate limit (403)")
        code, out, _ = self.run_main(fetch=limited)
        self.assertEqual(code, 3)
        self.assertEqual(out.count("UNCHECKED"), 1)
        self.assertIn("checked by date only", out)

    def test_invalid_article_rows_exit_2(self):
        def never(path):
            raise AssertionError("fetched")
        bad = [
            [article(kind="blog")],
            [article(url="http://example.org/post")],
            [article(url="not a url")],
            [article(pinned="abc1234")],
            [dict(article(), repo="owner/example")],
            [{k: v for k, v in article().items() if k != "url"}],
            [article(licence="")],
            [article(), article()],
        ]
        for sources in bad:
            with self.subTest(sources=sources):
                self.write(sources)
                code, _, err = self.run_main(fetch=never)
                self.assertEqual(code, 2)
                self.assertTrue(err)

    def test_repository_register_is_valid(self):
        sources, errors = freshness.load_register(
            ROOT / "docs/research/source-register.json", ROOT)
        self.assertEqual(errors, [])
        self.assertTrue(sources)

    def test_band_boundaries(self):
        self.assertEqual(freshness.band(30, 30, 365), "active")
        self.assertEqual(freshness.band(31, 30, 365), "quiet")
        self.assertEqual(freshness.band(366, 30, 365), "stale")
        self.assertEqual(date.fromisoformat(TODAY).year, 2026)


if __name__ == "__main__":
    unittest.main()
