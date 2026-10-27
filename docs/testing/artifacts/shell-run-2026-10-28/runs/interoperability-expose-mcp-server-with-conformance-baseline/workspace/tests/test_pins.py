"""Fails with a readable message when the installed SDK or ADK moves off the versions the
conformance baselines were recorded on. Update conformance/PINS.json together with the baselines."""
import importlib.metadata as md
import json
import pathlib
import unittest

PINS = json.loads((pathlib.Path(__file__).parent.parent / "conformance" / "PINS.json").read_text())


class PinTests(unittest.TestCase):
    def test_recorded_versions(self):
        for dist, want in PINS["python"].items():
            try:
                have = md.version(dist)
            except md.PackageNotFoundError:
                self.skipTest(f"{dist} not installed")
            self.assertEqual(have, want, f"{dist} is {have}, baselines were recorded on {want}: "
                             "rerun scripts/conformance.sh, review the diff, update baselines and PINS.json")


if __name__ == "__main__":
    unittest.main()
