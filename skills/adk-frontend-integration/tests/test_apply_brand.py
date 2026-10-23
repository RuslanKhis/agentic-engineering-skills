"""Offline public-boundary tests for the brand override helper and the shipped demo brands."""

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "apply_brand.py"
HOUSE = SKILL / "assets" / "design" / "DESIGN.md"
BRANDS = SKILL / "assets" / "design" / "brands"
SHIPPED = ("kelderwick-bank", "marrowby", "veldmark-industrial", "avenhale-health")

GOOD_BRAND = """name: Test Brand
fictional: true
colors:
  primary: "oklch(0.40 0.11 350)"
  primary-hover: "oklch(0.33 0.095 350)"
  dark-primary: "oklch(0.78 0.075 350)"
fonts:
  sans: Figtree
  sans-package: "@fontsource-variable/figtree@5.3.0"
rounded:
  md: 8px
"""


def front_matter_colors(text):
    block = text.split("\n---\n", 1)[0]
    colors = {}
    section = None
    for line in block.splitlines():
        top = re.fullmatch(r"([A-Za-z]+):\s*(.*)", line)
        if top:
            section = top[1]
            continue
        entry = re.fullmatch(r"  ([A-Za-z0-9-]+): \"?(.*?)\"?", line)
        if entry and section == "colors":
            colors[entry[1]] = entry[2]
    return colors


class VersionGuardTests(unittest.TestCase):
    def test_python_version_guard_exits_2_before_any_work(self):
        code = ("import runpy, sys; sys.version_info = (3, 10, 0); sys.argv = sys.argv[1:]; "
                "runpy.run_path(sys.argv[0], run_name='__main__')")
        result = subprocess.run([sys.executable, "-I", "-B", "-c", code, str(SCRIPT), "--brand", "marrowby"],
                                capture_output=True, text=True, timeout=30, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("requires Python 3.11", result.stderr)


class ApplyBrandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run_cli(self, *args):
        result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), *map(str, args)],
                                capture_output=True, text=True, timeout=60, check=False, cwd=self.root)
        return result.returncode, result.stdout, result.stderr

    def report(self, *args):
        code, out, err = self.run_cli(*args)
        return code, json.loads(out), err

    def test_help_describes_interface_and_exit_codes(self):
        code, out, _ = self.run_cli("--help")
        self.assertEqual(code, 0)
        for text in ("--brand", "--out", "--dry-run", "--lint", "Exit codes", "override surface"):
            self.assertIn(text, out)

    def test_each_shipped_brand_applies_and_every_pair_passes(self):
        for slug in SHIPPED:
            with self.subTest(slug=slug):
                code, data, err = self.report("--brand", slug)
                self.assertEqual(code, 0, err)
                self.assertEqual(data["status"], "pass")
                self.assertTrue(data["read_only"])
                self.assertTrue(data["brand"]["fictional"])
                self.assertEqual(data["checks"]["failing"], [])
                self.assertEqual(data["checks"]["out_of_srgb_gamut"], [])
                pairs = data["checks"]["pairs"]
                self.assertGreaterEqual(len(pairs), 30)
                self.assertTrue(all(p["pass"] and p["ratio"] >= p["floor"] for p in pairs))
                kinds = {(p["foreground"], p["background"]): p["floor"] for p in pairs}
                self.assertEqual(kinds[("primary-foreground", "primary")], 4.5)
                self.assertEqual(kinds[("dark-primary-foreground", "dark-primary")], 4.5)
                self.assertEqual(kinds[("input", "accent")], 3.0)
                self.assertEqual(kinds[("dark-ring", "dark-accent")], 3.0)
                self.assertEqual(set(data["overrides"]["logo"]), {"logo", "mark", "alt"})
                self.assertIn("fictional demo brand", data["overrides"]["logo"]["alt"])

    def test_shipped_brand_files_use_only_the_override_surface_and_ship_logos(self):
        for slug in SHIPPED:
            with self.subTest(slug=slug):
                folder = BRANDS / slug
                text = (folder / "brand.yaml").read_text(encoding="utf-8")
                self.assertIn("fictional: true", text)
                for name in ("logo.svg", "mark.svg"):
                    svg = (folder / name).read_text(encoding="utf-8")
                    self.assertIn("ISC License", svg)
                    self.assertIn("lucide-static@1.61.0", svg)
                    self.assertIn("(fictional demo brand)</title>", svg)
                    self.assertNotIn("<script", svg.lower())
                    self.assertNotRegex(svg, r"#[0-9A-Fa-f]{6}")  # theme colours only, never fixed fills

    def test_css_output_has_root_dark_imports_fonts_and_radius(self):
        code, data, _ = self.report("--brand", "kelderwick-bank")
        self.assertEqual(code, 0)
        css = data["css"]
        root = css.split(":root {", 1)[1].split("}", 1)[0]
        dark = css.split(".dark {", 1)[1].split("}", 1)[0]
        self.assertIn("--primary: oklch(0.40 0.11 350);", root)
        self.assertIn("--sidebar-primary: oklch(0.40 0.11 350);", root)
        self.assertIn("--radius: 0.25rem;", root)
        self.assertIn("--primary: oklch(0.78 0.075 350);", dark)
        self.assertIn("--primary-foreground: oklch(0.20 0.03 350);", dark)
        self.assertNotIn("--background", css)
        self.assertIn('@import "@fontsource-variable/instrument-sans";', css)
        self.assertIn('@import "@fontsource-variable/newsreader/opsz.css";', css)
        self.assertIn('--font-sans: "Instrument Sans Variable", ui-sans-serif, system-ui, sans-serif;', css)
        self.assertIn('--font-serif: "Newsreader Variable", Georgia', css)
        self.assertIn("--radius-lg: 4px;", css)
        self.assertIn("@fontsource-variable/newsreader@5.3.0", data["npm_install"])
        code, out, _ = self.run_cli("--brand", "kelderwick-bank", "--format", "css")
        self.assertEqual(code, 0)
        self.assertEqual(out, css)

    def test_disallowed_keys_exit_2_and_name_the_key(self):
        cases = {
            "colors.background": GOOD_BRAND.replace("colors:\n", 'colors:\n  background: "oklch(1 0 0)"\n'),
            "spacing": GOOD_BRAND + "spacing:\n  md: 10px\n",
            "rounded.lg": GOOD_BRAND.replace("  md: 8px", "  lg: 12px"),
            "fonts.weight": GOOD_BRAND.replace("fonts:\n", "fonts:\n  weight: 700\n"),
            "description": "description: hello\n" + GOOD_BRAND,
        }
        for key, text in cases.items():
            with self.subTest(key=key):
                brand = self.write(f"{key}/brand.yaml", text)
                code, data, err = self.report("--brand", brand)
                self.assertEqual(code, 2)
                self.assertEqual(data, {"schema_version": 1, "error": "key_not_in_override_surface", "key": key})
                self.assertIn(key, err)

    def test_too_light_primary_exits_1_and_names_the_pair(self):
        brand = self.write("light/brand.yaml", GOOD_BRAND.replace("oklch(0.40 0.11 350)", "oklch(0.70 0.11 350)"))
        out = self.root / "DESIGN.md"
        code, data, err = self.report("--brand", brand, "--out", out)
        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "fail")
        self.assertTrue(any(f.startswith("primary-foreground on primary:") for f in data["checks"]["failing"]))
        self.assertIn("fail: primary-foreground on primary", err)
        self.assertFalse(out.exists(), "nothing is written when a pair fails")

    def test_out_writes_brand_values_and_keeps_house_neutrals(self):
        out = self.root / "docs" / "DESIGN.md"
        out.parent.mkdir()
        code, data, err = self.report("--brand", "marrowby", "--out", out)
        self.assertEqual(code, 0, err)
        self.assertEqual(data["written"], str(out))
        self.assertFalse(data["read_only"])
        house_text = HOUSE.read_text(encoding="utf-8")
        merged = out.read_text(encoding="utf-8")
        house, brand = front_matter_colors(house_text), front_matter_colors(merged)
        self.assertEqual(set(house), set(brand))
        overridden = set(data["overrides"]["colors"])
        for token, value in house.items():
            if token in overridden:
                self.assertEqual(brand[token], data["overrides"]["colors"][token])
            else:
                self.assertEqual(brand[token], value, token)
        self.assertEqual(brand["primary"], "oklch(0.42 0.08 120)")
        self.assertEqual(brand["background"], house["background"])
        self.assertEqual(brand["dark-muted"], house["dark-muted"])
        self.assertIn("    fontFamily: Figtree", merged)
        self.assertIn("    fontFamily: Fraunces", merged)
        self.assertNotIn("fontFamily: Inter", merged)
        self.assertRegex(merged, r"\nrounded:\n  sm: 4px\n  md: 8px\n")
        self.assertIn("Brand applied: Marrowby (fictional demo brand)", merged)
        self.assertEqual(merged.count("\n"), house_text.count("\n") + 2)

    def test_out_refuses_to_overwrite_the_house_file(self):
        design = self.write("DESIGN.md", HOUSE.read_text(encoding="utf-8"))
        code, data, _ = self.report("--brand", "marrowby", "--design", design, "--out", design)
        self.assertEqual(code, 2)
        self.assertEqual(data["error"], "out_would_overwrite_source_or_non_file")
        self.assertEqual(design.read_text(encoding="utf-8"), HOUSE.read_text(encoding="utf-8"))

    def test_dry_run_equals_default_and_writes_nothing(self):
        default = self.run_cli("--brand", "avenhale-health")
        dry = self.run_cli("--brand", "avenhale-health", "--dry-run")
        self.assertEqual(default, dry)
        out = self.root / "DESIGN.md"
        code, data, _ = self.report("--brand", "avenhale-health", "--out", out, "--dry-run", "--lint")
        self.assertEqual(code, 0)
        self.assertEqual(data["would_write"], str(out))
        self.assertIsNone(data["written"])
        self.assertIsNone(data["lint"])
        self.assertFalse(out.exists())

    def test_new_house_tokens_and_components_are_handled(self):
        text = HOUSE.read_text(encoding="utf-8")
        text = text.replace('  success: "', '  success-subtle: "oklch(0.95 0.02 150)"\n  success: "', 1)
        text = text.replace("components:\n", "components:\n  callout-new:\n"
                            '    backgroundColor: "{colors.accent}"\n    textColor: "{colors.ring}"\n', 1)
        design = self.write("DESIGN.md", text)
        brand = self.write("c/brand.yaml", GOOD_BRAND.replace("colors:\n", 'colors:\n  accent: "oklch(0.948 0.014 350)"\n'
                                                              '  ring: "oklch(0.50 0.12 350)"\n'))
        code, data, err = self.report("--brand", brand, "--design", design)
        self.assertEqual(code, 0, err)
        sources = [s for p in data["checks"]["pairs"] for s in p["sources"]]
        self.assertIn("components.callout-new", sources)

    def test_out_of_gamut_colour_exits_1(self):
        brand = self.write("g/brand.yaml", GOOD_BRAND.replace('primary-hover: "oklch(0.33 0.095 350)"',
                                                              'primary-hover: "oklch(0.33 0.30 150)"'))
        code, data, _ = self.report("--brand", brand)
        self.assertEqual(code, 1)
        self.assertEqual(data["checks"]["out_of_srgb_gamut"], ["primary-hover"])

    def test_invalid_brand_files_exit_2(self):
        cases = {
            "tab": ("name: X\ncolors:\n\tprimary: \"oklch(0.4 0.1 350)\"\n", "brand_file_tab_indent"),
            "flow": ("name: X\nfonts: {sans: Figtree}\n", "brand_file_unsupported_yaml"),
            "deep": ("name: X\nfonts:\n  sans:\n    family: Figtree\n", "brand_file_unsupported_nesting"),
            "noname": ("colors:\n  primary: \"oklch(0.4 0.1 350)\"\n", "brand_name_missing"),
            "notcolour": ("name: X\ncolors:\n  primary: red\n", "brand_colour_not_oklch_or_hex"),
            "cdn": ("name: X\nfonts:\n  sans: Figtree\n  sans-package: figtree\n",
                    "brand_font_package_must_be_pinned_fontsource_variable"),
            "halffont": ("name: X\nfonts:\n  sans: Figtree\n", "brand_font_needs_family_and_package"),
            "radius": ("name: X\nrounded:\n  md: 12px\n", "brand_radius_must_be_4px_6px_or_8px"),
            "logo": ("name: X\nlogo:\n  logo: logo.svg\n  alt: X\n", "brand_logo_file_missing"),
            "escape": ("name: X\nlogo:\n  logo: ../logo.svg\n  alt: X\n", "brand_logo_path_invalid"),
            "dup": ("name: X\nname: Y\n", "brand_file_duplicate_key"),
        }
        for label, (text, error) in cases.items():
            with self.subTest(label=label):
                brand = self.write(f"{label}/brand.yaml", text)
                code, data, _ = self.report("--brand", brand)
                self.assertEqual(code, 2)
                self.assertEqual(data["error"], error)
        code, data, _ = self.report("--brand", self.root / "missing.yaml")
        self.assertEqual((code, data["error"]), (2, "brand_not_found"))
        code, _, err = self.run_cli("--nonsense", "sk-secret-value")
        self.assertEqual(code, 2)
        self.assertNotIn("sk-secret-value", err)


if __name__ == "__main__":
    unittest.main()
