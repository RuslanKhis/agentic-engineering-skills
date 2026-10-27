from dataclasses import dataclass, field
import unittest

from app.plugins.trimming import summary_line, trim_contents


@dataclass
class Part:
    text: str | None = None


@dataclass
class Content:
    role: str
    parts: list = field(default_factory=list)


def turn(role, text):
    return Content(role, [Part(text)])


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
