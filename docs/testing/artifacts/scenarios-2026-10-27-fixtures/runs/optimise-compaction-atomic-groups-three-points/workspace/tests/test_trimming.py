from dataclasses import dataclass, field
import unittest

from app.plugins.trimming import summary_line, trim_contents


@dataclass
class Part:
    text: str | None = None
    function_call: object | None = None
    function_response: object | None = None


@dataclass
class Content:
    role: str
    parts: list = field(default_factory=list)


def turn(role, text):
    return Content(role, [Part(text)])


def call(name):
    return Content("model", [Part(function_call={"name": name})])


def result(name):
    return Content("user", [Part(function_response={"name": name})])


def assert_no_split_pair(test, contents):
    calls = sum(1 for c in contents for p in c.parts if p.function_call)
    results = sum(1 for c in contents for p in c.parts if p.function_response)
    test.assertEqual(calls, results)
    if contents:
        test.assertFalse(any(p.function_response for p in contents[0].parts))


class AtomicGroupTests(unittest.TestCase):
    def history(self):
        return [turn("user", "q1"), call("a"), result("a"), turn("model", "a1"),
                turn("user", "q2"), call("b"), result("b"), turn("model", "a2"),
                turn("user", "q3"), call("c"), result("c")]

    def test_cut_never_lands_on_a_function_response(self):
        contents = self.history()
        for n in range(1, len(contents)):
            kept, dropped = trim_contents(contents, n)
            self.assertEqual(dropped + kept, contents)
            assert_no_split_pair(self, kept)
            assert_no_split_pair(self, dropped)
            self.assertGreaterEqual(len(kept), n)

    def test_budget_is_a_minimum_and_current_turn_is_kept(self):
        contents = self.history()
        kept, dropped = trim_contents(contents, 1)
        self.assertEqual([c.parts[0].text for c in kept][:1], ["q3"])
        self.assertEqual(len(kept), 3)

    def test_no_turn_start_means_nothing_dropped(self):
        contents = [turn("user", "q"), call("a"), result("a"), call("b"), result("b")]
        self.assertEqual(trim_contents(contents, 2), (contents, []))


class TrimmingTests(unittest.TestCase):
    def test_short_history_is_untouched(self):
        contents = [turn("user", "hi"), turn("model", "hello")]
        self.assertEqual(trim_contents(contents, 5), (contents, []))

    def test_keeps_newest(self):
        contents = [turn("user", str(i)) for i in range(10)]
        kept, dropped = trim_contents(contents, 4)
        self.assertEqual([c.parts[0].text for c in kept], ["6", "7", "8", "9"])
        self.assertEqual(len(dropped), 6)

    def test_summary_joins_dropped_text(self):
        self.assertEqual(summary_line([turn("user", "order HO-1"), turn("model", "found it")]),
                         "order HO-1 / found it")


if __name__ == "__main__":
    unittest.main()
