"""Offline public-boundary tests for the shadcn leftover-defaults theme checker."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_theme.py"

# shadcn 4.22.1 `init --base base --preset nova --template vite` output (src/index.css), verbatim.
STOCK_CSS = '''@import "tailwindcss";
@import "tw-animate-css";
@import "shadcn/tailwind.css";
@import "@fontsource-variable/geist";

@custom-variant dark (&:is(.dark *));

@theme inline {
    --font-heading: var(--font-sans);
    --font-sans: 'Geist Variable', sans-serif;
    --color-sidebar-ring: var(--sidebar-ring);
    --color-sidebar-border: var(--sidebar-border);
    --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
    --color-sidebar-accent: var(--sidebar-accent);
    --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
    --color-sidebar-primary: var(--sidebar-primary);
    --color-sidebar-foreground: var(--sidebar-foreground);
    --color-sidebar: var(--sidebar);
    --color-chart-5: var(--chart-5);
    --color-chart-4: var(--chart-4);
    --color-chart-3: var(--chart-3);
    --color-chart-2: var(--chart-2);
    --color-chart-1: var(--chart-1);
    --color-ring: var(--ring);
    --color-input: var(--input);
    --color-border: var(--border);
    --color-destructive: var(--destructive);
    --color-accent-foreground: var(--accent-foreground);
    --color-accent: var(--accent);
    --color-muted-foreground: var(--muted-foreground);
    --color-muted: var(--muted);
    --color-secondary-foreground: var(--secondary-foreground);
    --color-secondary: var(--secondary);
    --color-primary-foreground: var(--primary-foreground);
    --color-primary: var(--primary);
    --color-popover-foreground: var(--popover-foreground);
    --color-popover: var(--popover);
    --color-card-foreground: var(--card-foreground);
    --color-card: var(--card);
    --color-foreground: var(--foreground);
    --color-background: var(--background);
    --radius-sm: calc(var(--radius) * 0.6);
    --radius-md: calc(var(--radius) * 0.8);
    --radius-lg: var(--radius);
    --radius-xl: calc(var(--radius) * 1.4);
    --radius-2xl: calc(var(--radius) * 1.8);
    --radius-3xl: calc(var(--radius) * 2.2);
    --radius-4xl: calc(var(--radius) * 2.6);
}

:root {
    --background: oklch(1 0 0);
    --foreground: oklch(0.145 0 0);
    --card: oklch(1 0 0);
    --card-foreground: oklch(0.145 0 0);
    --popover: oklch(1 0 0);
    --popover-foreground: oklch(0.145 0 0);
    --primary: oklch(0.205 0 0);
    --primary-foreground: oklch(0.985 0 0);
    --secondary: oklch(0.97 0 0);
    --secondary-foreground: oklch(0.205 0 0);
    --muted: oklch(0.97 0 0);
    --muted-foreground: oklch(0.556 0 0);
    --accent: oklch(0.97 0 0);
    --accent-foreground: oklch(0.205 0 0);
    --destructive: oklch(0.577 0.245 27.325);
    --border: oklch(0.922 0 0);
    --input: oklch(0.922 0 0);
    --ring: oklch(0.708 0 0);
    --chart-1: oklch(0.87 0 0);
    --chart-2: oklch(0.556 0 0);
    --chart-3: oklch(0.439 0 0);
    --chart-4: oklch(0.371 0 0);
    --chart-5: oklch(0.269 0 0);
    --radius: 0.625rem;
    --sidebar: oklch(0.985 0 0);
    --sidebar-foreground: oklch(0.145 0 0);
    --sidebar-primary: oklch(0.205 0 0);
    --sidebar-primary-foreground: oklch(0.985 0 0);
    --sidebar-accent: oklch(0.97 0 0);
    --sidebar-accent-foreground: oklch(0.205 0 0);
    --sidebar-border: oklch(0.922 0 0);
    --sidebar-ring: oklch(0.708 0 0);
}

.dark {
    --background: oklch(0.145 0 0);
    --foreground: oklch(0.985 0 0);
    --card: oklch(0.205 0 0);
    --card-foreground: oklch(0.985 0 0);
    --popover: oklch(0.205 0 0);
    --popover-foreground: oklch(0.985 0 0);
    --primary: oklch(0.922 0 0);
    --primary-foreground: oklch(0.205 0 0);
    --secondary: oklch(0.269 0 0);
    --secondary-foreground: oklch(0.985 0 0);
    --muted: oklch(0.269 0 0);
    --muted-foreground: oklch(0.708 0 0);
    --accent: oklch(0.269 0 0);
    --accent-foreground: oklch(0.985 0 0);
    --destructive: oklch(0.704 0.191 22.216);
    --border: oklch(1 0 0 / 10%);
    --input: oklch(1 0 0 / 15%);
    --ring: oklch(0.556 0 0);
    --chart-1: oklch(0.87 0 0);
    --chart-2: oklch(0.556 0 0);
    --chart-3: oklch(0.439 0 0);
    --chart-4: oklch(0.371 0 0);
    --chart-5: oklch(0.269 0 0);
    --sidebar: oklch(0.205 0 0);
    --sidebar-foreground: oklch(0.985 0 0);
    --sidebar-primary: oklch(0.488 0.243 264.376);
    --sidebar-primary-foreground: oklch(0.985 0 0);
    --sidebar-accent: oklch(0.269 0 0);
    --sidebar-accent-foreground: oklch(0.985 0 0);
    --sidebar-border: oklch(1 0 0 / 10%);
    --sidebar-ring: oklch(0.556 0 0);
}

@layer base {
  * {
    @apply border-border outline-ring/50;
    }
  body {
    @apply bg-background text-foreground;
    }
  html {
    @apply font-sans;
    }
}'''

# The house theme generated from assets/design/DESIGN.md (theme blocks only; utilities omitted).
HOUSE_CSS = '''@import "tailwindcss";
@import "tw-animate-css";
@import "shadcn/tailwind.css";
@import "@fontsource-variable/inter";
@import "@fontsource-variable/source-serif-4/opsz.css";
@import "@fontsource-variable/jetbrains-mono";

@custom-variant dark (&:is(.dark *));

@theme inline {
  --font-sans: "Inter Variable", ui-sans-serif, system-ui, sans-serif;
  --font-serif: "Source Serif 4 Variable", Georgia, "Times New Roman", serif;
  --font-mono: "JetBrains Mono Variable", ui-monospace, SFMono-Regular, Menlo, monospace;
  --font-heading: var(--font-sans);
  --radius-sm: 4px;
  --radius-md: 4px;
  --radius-lg: 6px;
  --radius-xl: 8px;
  --radius-2xl: 8px;
  --radius-3xl: 8px;
  --radius-4xl: 8px;
}

:root {
  --background: oklch(0.988 0.003 85);
  --foreground: oklch(0.205 0.006 85);
  --card: oklch(0.997 0.0015 85);
  --card-foreground: oklch(0.205 0.006 85);
  --popover: oklch(0.997 0.0015 85);
  --popover-foreground: oklch(0.205 0.006 85);
  --primary: oklch(0.40 0.085 250);
  --primary-hover: oklch(0.33 0.07 250);
  --primary-active: oklch(0.27 0.055 250);
  --primary-foreground: oklch(0.985 0.003 85);
  --secondary: oklch(0.955 0.005 85);
  --secondary-foreground: oklch(0.24 0.008 85);
  --muted: oklch(0.962 0.004 85);
  --muted-foreground: oklch(0.47 0.008 85);
  --accent: oklch(0.948 0.012 250);
  --accent-foreground: oklch(0.30 0.07 250);
  --destructive: oklch(0.50 0.15 27);
  --destructive-foreground: oklch(0.985 0.003 85);
  --success: oklch(0.47 0.09 150);
  --warning: oklch(0.50 0.10 65);
  --info: oklch(0.48 0.07 220);
  --border: oklch(0.905 0.005 85);
  --input: oklch(0.62 0.008 85);
  --ring: oklch(0.50 0.10 250);
  --chart-1: oklch(0.50 0.095 250);
  --chart-2: oklch(0.50 0.08 185);
  --chart-3: oklch(0.52 0.10 70);
  --chart-4: oklch(0.50 0.02 85);
  --chart-5: oklch(0.52 0.13 30);
  --sidebar: oklch(0.972 0.004 85);
  --sidebar-foreground: oklch(0.205 0.006 85);
  --sidebar-primary: oklch(0.40 0.085 250);
  --sidebar-primary-foreground: oklch(0.985 0.003 85);
  --sidebar-accent: oklch(0.935 0.006 85);
  --sidebar-accent-foreground: oklch(0.205 0.006 85);
  --sidebar-border: oklch(0.905 0.005 85);
  --sidebar-ring: oklch(0.50 0.10 250);
  --radius: 0.375rem;
}

.dark {
  --background: oklch(0.185 0.004 85);
  --foreground: oklch(0.945 0.004 85);
  --card: oklch(0.215 0.005 85);
  --card-foreground: oklch(0.945 0.004 85);
  --popover: oklch(0.245 0.005 85);
  --popover-foreground: oklch(0.945 0.004 85);
  --primary: oklch(0.78 0.075 250);
  --primary-hover: oklch(0.84 0.06 250);
  --primary-active: oklch(0.72 0.08 250);
  --primary-foreground: oklch(0.20 0.03 250);
  --secondary: oklch(0.275 0.006 85);
  --secondary-foreground: oklch(0.93 0.004 85);
  --muted: oklch(0.255 0.005 85);
  --muted-foreground: oklch(0.735 0.008 85);
  --accent: oklch(0.29 0.03 250);
  --accent-foreground: oklch(0.91 0.025 250);
  --destructive: oklch(0.72 0.13 25);
  --destructive-foreground: oklch(0.20 0.03 25);
  --success: oklch(0.76 0.10 150);
  --warning: oklch(0.80 0.10 75);
  --info: oklch(0.76 0.07 220);
  --border: oklch(0.30 0.005 85);
  --input: oklch(0.57 0.008 85);
  --ring: oklch(0.74 0.09 250);
  --chart-1: oklch(0.74 0.09 250);
  --chart-2: oklch(0.74 0.08 185);
  --chart-3: oklch(0.80 0.10 75);
  --chart-4: oklch(0.72 0.015 85);
  --chart-5: oklch(0.72 0.12 30);
  --sidebar: oklch(0.205 0.005 85);
  --sidebar-foreground: oklch(0.945 0.004 85);
  --sidebar-primary: oklch(0.78 0.075 250);
  --sidebar-primary-foreground: oklch(0.20 0.03 250);
  --sidebar-accent: oklch(0.27 0.006 85);
  --sidebar-accent-foreground: oklch(0.945 0.004 85);
  --sidebar-border: oklch(0.30 0.005 85);
  --sidebar-ring: oklch(0.74 0.09 250);
}

@layer base {
  * {
    @apply border-border;
  }
}

:focus-visible {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}
'''

STOCK_ROOT = {"--radius", "--background", "--foreground", "--card", "--card-foreground", "--popover",
              "--popover-foreground", "--primary", "--primary-foreground", "--secondary",
              "--secondary-foreground", "--muted", "--muted-foreground", "--accent", "--accent-foreground",
              "--destructive", "--border", "--input", "--ring", "--chart-1", "--chart-2", "--chart-3",
              "--chart-4", "--chart-5", "--sidebar", "--sidebar-foreground", "--sidebar-primary",
              "--sidebar-primary-foreground", "--sidebar-accent", "--sidebar-accent-foreground",
              "--sidebar-border", "--sidebar-ring"}
SECRET = "PRIVATE_TOKEN_DO_NOT_ECHO"


class VersionGuardTests(unittest.TestCase):
    def test_python_version_guard_exits_2_before_any_work(self):
        code = ('import sys, runpy; sys.version_info = (3, 10, 0); '
                'runpy.run_path(sys.argv[1], run_name="__main__")')
        result = subprocess.run([sys.executable, "-I", "-B", "-c", code, str(SCRIPT), "--css", "x.css"],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "error: check_theme.py requires Python 3.11 or newer.\n")


@unittest.skipIf(sys.version_info < (3, 11), "check_theme.py requires Python 3.11 or newer")
class CheckThemeTests(unittest.TestCase):
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
        result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), *args],
                                cwd=self.root, capture_output=True, text=True, timeout=15)
        data = json.loads(result.stdout) if "--json" in args and result.stdout else None
        return result, data

    def leftovers(self, data):
        return {(item["scope"], item["variable"]) for item in data["leftovers"]}

    def test_help_describes_interface_and_exit_codes(self):
        result, _ = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        for text in ("--project", "--css", "--dry-run", "--json", "Exit codes", "4.22.1"):
            self.assertIn(text, result.stdout)

    def test_stock_default_theme_fails_and_lists_every_default(self):
        css = self.write("index.css", STOCK_CSS)
        result, data = self.run_cli("--css", str(css), "--json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data["status"], "defaults_remain")
        found = self.leftovers(data)
        self.assertTrue({(":root", name) for name in STOCK_ROOT} <= found)
        self.assertTrue({(".dark", name) for name in STOCK_ROOT - {"--radius"}} <= found)
        self.assertIn(("@theme", "--font-sans"), found)
        self.assertIn(("top-level", "@import"), found)
        self.assertIn(("@layer base > *", "outline-ring/50"), found)
        self.assertEqual(len(data["leftovers"]), 66)
        for item in data["leftovers"]:
            self.assertEqual(set(item), {"variable", "scope", "value"})
        self.assertEqual(data["reference"]["version"], "4.22.1")
        self.assertTrue(data["reference"]["commit"].startswith("3d98900"))

    def test_text_output_names_leftovers(self):
        css = self.write("index.css", STOCK_CSS)
        result, _ = self.run_cli("--css", str(css))
        self.assertEqual(result.returncode, 1)
        self.assertIn(":root --background: oklch(1 0 0)", result.stdout)
        self.assertIn(".dark --input: oklch(1 0 0 / 15%)", result.stdout)

    def test_house_theme_passes(self):
        css = self.write("app.css", HOUSE_CSS)
        result, data = self.run_cli("--css", str(css), "--json")
        self.assertEqual(result.returncode, 0, data)
        self.assertEqual(data["status"], "clean")
        self.assertEqual(data["leftovers"], [])
        self.assertGreater(data["custom_properties_checked"][":root"], 30)
        self.assertGreater(data["custom_properties_checked"][".dark"], 30)

    def test_partly_edited_theme_lists_only_the_leftovers(self):
        css = self.write("app.css", """
@import "tailwindcss";
@import "@fontsource-variable/inter";
@theme inline { --font-sans: "Inter Variable", sans-serif; }
:root {
  --radius: 0.375rem;
  --background: oklch(0.988 0.003 85);
  --primary: oklch(0.205 0 0);
  --ring: oklch(0.50 0.10 250);
}
.dark {
  --primary: oklch(0.78 0.075 250);
  --ring: oklch(0.556 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
}
""")
        result, data = self.run_cli("--css", str(css), "--json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.leftovers(data), {(":root", "--primary"), (".dark", "--ring"), (".dark", "--chart-1")})

    def test_values_are_compared_after_normalisation(self):
        css = self.write("app.css", ":root {\n  --background:OKLCH( 1   0 0 );\n  --primary: oklch(0.2050 0.0 0);\n"
                                    "  --radius: 0.6250REM;\n}\n.dark { --border: oklch(1 0 0/10%) !important; }\n")
        result, data = self.run_cli("--css", str(css), "--json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.leftovers(data), {(":root", "--background"), (":root", "--primary"),
                                                (":root", "--radius"), (".dark", "--border")})

    def test_default_values_in_comments_or_other_variables_are_ignored(self):
        css = self.write("app.css", "/* --background: oklch(1 0 0); */\n:root {\n  --surface: oklch(1 0 0);\n"
                                    "  --background: oklch(0.99 0.003 85);\n}\n")
        result, data = self.run_cli("--css", str(css), "--json")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data["leftovers"], [])

    def test_project_resolves_css_from_components_json(self):
        self.write("project/components.json", json.dumps({"style": "base-nova", "tailwind": {"css": "src/styles/app.css"}}))
        self.write("project/src/styles/app.css", STOCK_CSS)
        result, data = self.run_cli("--project", str(self.root / "project"), "--json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data["css"], "src/styles/app.css")
        self.write("project/src/styles/app.css", HOUSE_CSS)
        result, data = self.run_cli("--project", str(self.root / "project"), "--json")
        self.assertEqual(result.returncode, 0)

    def test_css_relative_to_project(self):
        self.write("project/theme.css", HOUSE_CSS)
        result, data = self.run_cli("--project", str(self.root / "project"), "--css", "theme.css", "--json")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data["css"], "theme.css")

    def test_invalid_inputs_exit_2(self):
        self.write("outside.css", STOCK_CSS)
        self.write("escape/components.json", json.dumps({"tailwind": {"css": "../outside.css"}}))
        self.write("nocss/components.json", json.dumps({"tailwind": {}}))
        self.write("badjson/components.json", "{not json")
        self.write("empty/components.json", json.dumps({"tailwind": {"css": "src/index.css"}}))
        self.write("nothemes.css", "body { color: red; }\n")
        self.write("unbalanced.css", ":root { --background: oklch(1 0 0);\n")
        self.write("big.css", ":root { --x: 1; }\n" + "/*" + "x" * 1_100_000 + "*/\n")
        self.write(".env", ":root { --background: oklch(1 0 0); }\n")
        cases = {
            "missing css": ("--css", str(self.root / "missing.css")),
            "missing components.json": ("--project", str(self.root)),
            "missing project": ("--project", str(self.root / "nope")),
            "css outside project": ("--project", str(self.root / "escape")),
            "no tailwind.css field": ("--project", str(self.root / "nocss")),
            "invalid components.json": ("--project", str(self.root / "badjson")),
            "css named in components.json missing": ("--project", str(self.root / "empty")),
            "no theme blocks": ("--css", str(self.root / "nothemes.css")),
            "unbalanced braces": ("--css", str(self.root / "unbalanced.css")),
            "too large": ("--css", str(self.root / "big.css")),
            "env file refused": ("--css", str(self.root / ".env")),
            "nothing given": (),
        }
        for label, args in cases.items():
            with self.subTest(label):
                result, data = self.run_cli(*args, "--json")
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("error", data)

    def test_invalid_arguments_never_echo_input(self):
        result, _ = self.run_cli("--unknown-" + SECRET)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(SECRET, result.stdout + result.stderr)

    def test_dry_run_equals_normal_run_and_writes_nothing(self):
        css = self.write("index.css", STOCK_CSS)
        before = sorted(p.name for p in self.root.iterdir())
        for extra in ((), ("--json",)):
            normal, _ = self.run_cli("--css", str(css), *extra)
            dry, _ = self.run_cli("--css", str(css), "--dry-run", *extra)
            self.assertEqual((normal.returncode, normal.stdout), (dry.returncode, dry.stdout))
            self.assertIn("--dry-run is deprecated", dry.stderr)
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), before)
        self.assertEqual(css.read_text(encoding="utf-8"), STOCK_CSS)


if __name__ == "__main__":
    unittest.main()
