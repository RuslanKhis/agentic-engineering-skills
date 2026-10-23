#!/usr/bin/env python3
"""Apply a brand override to the house DESIGN.md and check its contrast.

Reads the house DESIGN.md (--design, default: this skill's assets/design/DESIGN.md)
and one brand file (--brand: a brand.yaml path, a brand directory, or the slug of a
shipped demo brand under assets/design/brands/). The brand file may set only the
Brand override surface of DESIGN.md: the accent ramp tokens and their dark- twins,
the sans, serif and mono font families with their @fontsource-variable packages,
logo files, and one control radius step (rounded.md: 4px, 6px or 8px). Any other
key is refused.

For every colour pair the override touches, the WCAG 2.x contrast is recomputed
against the house neutrals with this script's own OKLCH -> sRGB -> relative
luminance maths (gamut-clipped, rounded to 8 bits, as a browser paints it):
every DESIGN.md component pair at 4.5:1 (as the DESIGN.md linter checks them),
primary as link text on every surface at 4.5:1, and ring, input edge and chart-1
marks at 3:1 on the surfaces they sit on.

Default output is a JSON report, including the CSS variables for :root and .dark,
the @fontsource-variable imports and the radius setting to paste into the
project's theme file (--format css prints only that block).

Python 3.11+; standard library only. Read-only unless --out is given: then the
merged DESIGN.md is written there, and only when every check passes. --lint also
runs `npx -y @google/design.md@0.4.0 lint` on the merged file (network; never by
default). --dry-run reports what would be written and never writes or runs npx.
Exit codes: 0 every pair passes; 1 a pair, the gamut check or the lint fails;
2 invalid input (including a key outside the override surface).
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 11):
    print("error: apply_brand.py requires Python 3.11 or newer.", file=sys.stderr)
    raise SystemExit(2)

import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile

SKILL_ROOT = Path(__file__).resolve().parents[1]
HOUSE_DESIGN = SKILL_ROOT / "assets" / "design" / "DESIGN.md"
BRANDS_DIR = SKILL_ROOT / "assets" / "design" / "brands"
LINT_PACKAGE = "@google/design.md@0.4.0"
MAX_DESIGN_BYTES = 1_048_576
MAX_BRAND_BYTES = 65_536

RAMP = ("primary", "primary-hover", "primary-active", "primary-foreground",
        "accent", "accent-foreground", "ring", "chart-1")
COLOR_KEYS = RAMP + tuple(f"dark-{name}" for name in RAMP)
FONT_ROLES = ("sans", "serif", "mono")
FONT_KEYS = tuple(f"{role}{suffix}" for role in FONT_ROLES for suffix in ("", "-package", "-css"))
LOGO_KEYS = ("logo", "mark", "alt")
RADIUS_VALUES = ("4px", "6px", "8px")
SURFACE = {
    "brand": {"name", "fictional"},
    "colors": set(COLOR_KEYS),
    "fonts": set(FONT_KEYS),
    "logo": set(LOGO_KEYS),
    "rounded": {"md"},
}
TEXT_FLOOR, UI_FLOOR = 4.5, 3.0
# Extra pairs beyond the DESIGN.md components block: (foreground, [surfaces], floor, why).
# Surfaces missing from DESIGN.md are skipped, so new house tokens never break this list.
LIGHT_SURFACES = ["background", "card", "popover", "muted", "secondary", "sidebar", "sidebar-accent", "accent"]
EXTRA_PAIRS = [
    ("primary", ["background", "card", "popover", "muted", "sidebar"], TEXT_FLOOR, "primary as link text"),
    ("ring", LIGHT_SURFACES, UI_FLOOR, "focus outline"),
    ("input", ["accent"], UI_FLOOR, "field edge on the accent fill"),
    ("chart-1", ["background", "card", "popover", "muted"], UI_FLOOR, "chart mark"),
]
EXTRA_PAIRS += [("dark-" + fg, ["dark-" + s for s in surfaces], floor, why) for fg, surfaces, floor, why in EXTRA_PAIRS]
SEMANTIC = ("success", "warning", "destructive", "info")


class InputError(Exception):
    """Invalid input; the code is a stable identifier and detail is never user secret text."""

    def __init__(self, code: str, detail: str | None = None):
        super().__init__(code)
        self.code = code
        self.detail = detail


# --------------------------------------------------------------------------- reading

def read_bounded(path: Path, limit: int, code: str) -> str:
    if path.name.startswith(".env"):
        raise InputError(f"{code}_refused_env_file")
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    except FileNotFoundError:
        raise InputError(f"{code}_not_found") from None
    except OSError:
        raise InputError(f"{code}_unreadable_or_symlink") from None
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise InputError(f"{code}_not_a_regular_file")
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise InputError(f"{code}_too_large")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        raise InputError(f"{code}_not_utf8") from None


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_brand(text: str) -> dict:
    """Parse the brand file's YAML subset: `key: value` and one level of `  key: value` nesting."""
    data: dict = {}
    section: str | None = None
    for number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw:
            raise InputError("brand_file_tab_indent", f"line {number}")
        match = re.fullmatch(r"( *)([A-Za-z0-9_-]+):(?: +(.*?))?\s*", raw)
        if not match:
            raise InputError("brand_file_unparsed_line", f"line {number}")
        indent, key, value = len(match[1]), match[2], match[3]
        if value is not None:
            if value[:1] in "\"'":
                closing = value.find(value[0], 1)
                rest = value[closing + 1:].strip() if closing > 0 else "x"
                if closing < 0 or (rest and not rest.startswith("#")):
                    raise InputError("brand_file_bad_quoting", f"line {number}")
                value = value[1:closing]
            else:
                value = re.sub(r"\s+#.*$", "", value)
                if value[:1] in "[{&*!|>":
                    raise InputError("brand_file_unsupported_yaml", f"line {number}")
        if indent == 0:
            if value is None or value == "":
                if key not in SURFACE or key == "brand":
                    raise InputError("key_not_in_override_surface", key)
                if key in data:
                    raise InputError("brand_file_duplicate_key", key)
                data[key], section = {}, key
            else:
                if key not in SURFACE["brand"]:
                    raise InputError("key_not_in_override_surface", key)
                if key in data:
                    raise InputError("brand_file_duplicate_key", key)
                data[key], section = value, None
        elif indent == 2 and section is not None and value not in (None, ""):
            if key not in SURFACE[section]:
                raise InputError("key_not_in_override_surface", f"{section}.{key}")
            if key in data[section]:
                raise InputError("brand_file_duplicate_key", f"{section}.{key}")
            data[section][key] = value
        else:
            raise InputError("brand_file_unsupported_nesting", f"line {number}")
    return data


def parse_front_matter(text: str) -> tuple[list[str], int, dict]:
    """Index the DESIGN.md front matter: colors, typography, rounded and components, with line numbers."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise InputError("design_front_matter_missing")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise InputError("design_front_matter_unterminated") from None
    index: dict = {"top": {}, "colors": {}, "typography": {}, "rounded": {}, "components": {}}
    section = sub = None
    for i in range(1, end):
        line = lines[i]
        match = re.fullmatch(r"( *)([^:#][^:]*?):(?: +(.*?))?\s*", line)
        if not match or line.lstrip().startswith("#"):
            continue
        indent, key, value = len(match[1]), match[2].strip(), match[3]
        value = unquote(value) if value else None
        if indent == 0:
            section, sub = key, None
            if value is not None:
                index["top"][key] = (value, i)
        elif indent == 2 and section in index:
            sub = key
            if value is not None:
                index[section][key] = (value, i)
            else:
                index[section].setdefault(key, {})
        elif indent == 4 and section in ("typography", "components") and isinstance(index[section].get(sub), dict):
            index[section][sub][key] = (value, i)
    if not index["colors"]:
        raise InputError("design_has_no_colors")
    return lines, end, index


def house_fonts(body: str) -> dict:
    """Read the house family, fallbacks, package and CSS file for each role from the Typography table."""
    fonts = {}
    for line in body.splitlines():
        match = re.search(r"--font-(sans|serif|mono):\s*([^`|]+?)\s*`", line)
        if not match:
            continue
        stack = [part.strip() for part in match[2].split(",")]
        family = re.sub(r"\s+Variable$", "", unquote(stack[0]))
        package = re.search(r"`(@fontsource-variable/[a-z0-9-]+)@([0-9][0-9.]*)`", line)
        css = re.search(r"import `([a-z0-9-]+\.css)`", line)
        fonts[match[1]] = {
            "family": family,
            "fallbacks": stack[1:],
            "package": f"{package[1]}@{package[2]}" if package else None,
            "css": css[1] if css else None,
        }
    if set(fonts) != set(FONT_ROLES):
        raise InputError("design_font_stacks_not_found")
    return fonts


# --------------------------------------------------------------------------- colour maths

def parse_colour(value: str) -> tuple[float, float, float]:
    """Return linear-light sRGB (unclipped) for oklch(L C h) or #rrggbb."""
    value = value.strip()
    match = re.fullmatch(r"oklch\(\s*([0-9.]+)(%?)\s+([0-9.]+)\s+([0-9.]+)(?:deg)?\s*\)", value, re.I)
    if match:
        lightness = float(match[1]) / (100 if match[2] else 1)
        chroma, hue = float(match[3]), math.radians(float(match[4]))
        a, b = chroma * math.cos(hue), chroma * math.sin(hue)
        l_ = lightness + 0.3963377774 * a + 0.2158037573 * b
        m_ = lightness - 0.1055613458 * a - 0.0638541728 * b
        s_ = lightness - 0.0894841775 * a - 1.2914855480 * b
        l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
        return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
                -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
                -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    match = re.fullmatch(r"#([0-9a-f]{6})", value, re.I)
    if match:
        return tuple(_decode(int(match[1][i:i + 2], 16) / 255) for i in (0, 2, 4))
    raise ValueError(value)


def _encode(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def _decode(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def in_gamut(value: str) -> bool:
    return all(-1e-4 <= c <= 1 + 1e-4 for c in parse_colour(value))


def to_8bit(value: str) -> tuple[int, int, int]:
    return tuple(round(max(0.0, min(1.0, _encode(max(0.0, min(1.0, c))))) * 255) for c in parse_colour(value))


def hex_of(value: str) -> str:
    return "#" + "".join(f"{c:02X}" for c in to_8bit(value))


def luminance(value: str) -> float:
    r, g, b = (_decode(c / 255) for c in to_8bit(value))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def oklab_distance(a: str, b: str) -> float | None:
    def lab(value):
        match = re.fullmatch(r"oklch\(\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s*\)", value.strip())
        if not match:
            return None
        lightness, chroma, hue = (float(x) for x in match.groups())
        return lightness, chroma * math.cos(math.radians(hue)), chroma * math.sin(math.radians(hue))
    pa, pb = lab(a), lab(b)
    return None if pa is None or pb is None else math.dist(pa, pb)


# --------------------------------------------------------------------------- merge and checks

def resolve(colors: dict, name: str, seen: tuple = ()) -> tuple[str, tuple[str, ...]]:
    """Return (literal value, chain of token names) for a colour token or {colors.x} reference."""
    if name in seen or name not in colors:
        raise InputError("design_colour_reference_unresolved", name)
    value = colors[name]
    match = re.fullmatch(r"\{colors\.([A-Za-z0-9_-]+)\}", value.strip())
    if match:
        literal, chain = resolve(colors, match[1], seen + (name,))
        return literal, (name,) + chain
    return value, (name,)


def ref_name(value: str | None) -> str | None:
    match = re.fullmatch(r"\{colors\.([A-Za-z0-9_-]+)\}", (value or "").strip())
    return match[1] if match else None


def validate_brand(brand: dict, house_colors: dict, brand_dir: Path | None) -> dict:
    if not isinstance(brand.get("name"), str) or not brand["name"].strip():
        raise InputError("brand_name_missing")
    fictional = brand.get("fictional", "false")
    if fictional not in ("true", "false"):
        raise InputError("brand_fictional_must_be_true_or_false")
    colors = brand.get("colors", {})
    for key, value in colors.items():
        if key not in house_colors:
            raise InputError("design_token_missing_for_override", f"colors.{key}")
        try:
            parse_colour(value)
        except ValueError:
            raise InputError("brand_colour_not_oklch_or_hex", f"colors.{key}") from None
    fonts = brand.get("fonts", {})
    for role in FONT_ROLES:
        given = [k for k in fonts if k == role or k.startswith(role + "-")]
        if given and (role not in fonts or f"{role}-package" not in fonts):
            raise InputError("brand_font_needs_family_and_package", f"fonts.{role}")
        if role in fonts:
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 ]{0,62}", fonts[role]):
                raise InputError("brand_font_family_invalid", f"fonts.{role}")
            if not re.fullmatch(r"@fontsource-variable/[a-z0-9-]+@\d+\.\d+\.\d+", fonts[f"{role}-package"]):
                raise InputError("brand_font_package_must_be_pinned_fontsource_variable", f"fonts.{role}-package")
            if f"{role}-css" in fonts and not re.fullmatch(r"[a-z0-9-]+\.css", fonts[f"{role}-css"]):
                raise InputError("brand_font_css_invalid", f"fonts.{role}-css")
    rounded = brand.get("rounded", {})
    if "md" in rounded and rounded["md"] not in RADIUS_VALUES:
        raise InputError("brand_radius_must_be_4px_6px_or_8px", "rounded.md")
    logo = brand.get("logo", {})
    resolved_logo = {}
    for key in ("logo", "mark"):
        if key not in logo:
            continue
        relative = Path(logo[key])
        if relative.is_absolute() or ".." in relative.parts or relative.suffix.lower() not in (".svg", ".png", ".webp"):
            raise InputError("brand_logo_path_invalid", f"logo.{key}")
        if brand_dir is None or not (brand_dir / relative).is_file() or (brand_dir / relative).is_symlink():
            raise InputError("brand_logo_file_missing", f"logo.{key}")
        resolved_logo[key] = relative.as_posix()
    if resolved_logo and not logo.get("alt", "").strip():
        raise InputError("brand_logo_needs_alt", "logo.alt")
    if logo.get("alt"):
        resolved_logo["alt"] = logo["alt"]
    return {"name": brand["name"].strip(), "fictional": fictional == "true", "colors": dict(colors),
            "fonts": dict(fonts), "rounded": dict(rounded), "logo": resolved_logo}


def contrast_checks(colors: dict, components: dict, overridden: set[str]) -> list[dict]:
    pairs: dict[tuple[str, str], dict] = {}

    def add(fg: str, bg: str, floor: float, source: str) -> None:
        if fg not in colors or bg not in colors:
            return
        fg_value, fg_chain = resolve(colors, fg)
        bg_value, bg_chain = resolve(colors, bg)
        if not (set(fg_chain) | set(bg_chain)) & overridden:
            return
        key = (fg_chain[-1], bg_chain[-1])
        try:
            ratio = contrast(fg_value, bg_value)
        except ValueError:
            raise InputError("design_colour_unsupported", fg if fg_value == fg else bg) from None
        current = pairs.get(key)
        sources = current["sources"] if current else []
        if source not in sources:
            sources.append(source)
        if current and current["floor"] >= floor:
            return
        pairs[key] = {"foreground": fg, "background": bg, "kind": "text" if floor >= TEXT_FLOOR else "ui",
                      "floor": floor, "ratio": round(ratio, 2), "pass": ratio >= floor,
                      "foreground_hex": hex_of(fg_value), "background_hex": hex_of(bg_value),
                      "sources": sources}

    for name, props in components.items():
        if not isinstance(props, dict):
            continue
        fg, bg = ref_name(props.get("textColor", (None,))[0]), ref_name(props.get("backgroundColor", (None,))[0])
        if fg and bg:
            add(fg, bg, TEXT_FLOOR, f"components.{name}")
    for fg, surfaces, floor, why in EXTRA_PAIRS:
        for bg in surfaces:
            add(fg, bg, floor, why)
    return sorted(pairs.values(), key=lambda p: (p["foreground"].startswith("dark-"), p["foreground"], p["background"]))


def separation(colors: dict, house_colors: dict) -> dict:
    """Informational OKLab distances: chart-1 from the other series, primary from the semantic colours
    and from the house primary."""
    out = {}
    literal = {k: resolve(colors, k)[0] for k in colors}
    for prefix in ("", "dark-"):
        token = prefix + "primary"
        if token in colors:
            distance = oklab_distance(literal[token], resolve(house_colors, token)[0])
            if distance is not None:
                out[f"{token}_from_house"] = round(distance, 3)
        charts = [k for k in colors if re.fullmatch(prefix + r"chart-\d+", k) and k != prefix + "chart-1"]
        semantic = [prefix + s for s in SEMANTIC if prefix + s in colors]
        for token, others in ((prefix + "chart-1", charts), (prefix + "primary", semantic)):
            if token not in colors:
                continue
            found = [(oklab_distance(literal[token], literal[o]), o) for o in others]
            found = [f for f in found if f[0] is not None]
            if found:
                distance, nearest = min(found)
                out[token] = {"nearest": nearest, "oklab_distance": round(distance, 3)}
    return out


def css_block(brand: dict, colors: dict, house_colors: dict, fonts: dict, house_font: dict) -> tuple[str, dict]:
    """Paste-ready CSS: every variable whose value changes, imports, font stacks and radius."""
    changed = {":root": {}, ".dark": {}}
    for name in house_colors:
        before, after = resolve(house_colors, name)[0], resolve(colors, name)[0]
        if before != after:
            scope = ".dark" if name.startswith("dark-") else ":root"
            changed[scope]["--" + name.removeprefix("dark-")] = after
    imports, packages, stacks = [], [], {}
    for role in FONT_ROLES:
        family = fonts.get(role, house_font[role]["family"])
        package = fonts.get(f"{role}-package", house_font[role]["package"])
        css = fonts.get(f"{role}-css", None if role in fonts else house_font[role]["css"])
        bare = package.rsplit("@", 1)[0] if package else None
        if bare:
            imports.append(f'@import "{bare}/{css}";' if css and css != "index.css" else f'@import "{bare}";')
            packages.append(package)
        stacks[f"--font-{role}"] = ", ".join([f'"{family} Variable"'] + house_font[role]["fallbacks"])
    radius = brand["rounded"].get("md")
    radius_vars = {}
    if radius:
        px = int(radius.removesuffix("px"))
        radius_vars = {"--radius": f"{px / 16:g}rem", "--radius-lg": radius}
    lines = [f"/* {brand['name']}{' (fictional demo brand)' if brand['fictional'] else ''}: generated by "
             "apply_brand.py. Replace the matching house values; keep every other house variable. */"]
    lines += imports + [""]
    for scope in (":root", ".dark"):
        entries = dict(changed[scope])
        if scope == ":root" and radius_vars:
            entries["--radius"] = radius_vars["--radius"]
        lines.append(scope + " {")
        lines += [f"  {k}: {v};" for k, v in entries.items()]
        lines.append("}")
        lines.append("")
    lines.append("@theme inline {")
    lines += [f"  {k}: {v};" for k, v in stacks.items()]
    if radius_vars:
        lines.append(f"  --radius-lg: {radius}; /* rounded.md, controls; keep the other house radius pins */")
    lines.append("}")
    return "\n".join(lines) + "\n", {
        "variables": changed, "font_stacks": stacks, "font_imports": imports,
        "npm_install": "npm install " + " ".join(packages), "radius": radius_vars or None,
    }


def merge(lines: list[str], end: int, index: dict, brand: dict, house_font: dict) -> str:
    out = list(lines)
    for key, value in brand["colors"].items():
        _, line = index["colors"][key]
        indent = re.match(r" *", out[line])[0]
        out[line] = f'{indent}{key}: "{value}"'
    for role in FONT_ROLES:
        if role not in brand["fonts"]:
            continue
        old, new = house_font[role]["family"], brand["fonts"][role]
        for props in index["typography"].values():
            if isinstance(props, dict) and "fontFamily" in props and unquote(props["fontFamily"][0]) == old:
                line = props["fontFamily"][1]
                out[line] = re.sub(r"(fontFamily:\s*).*$", lambda m: m[1] + new, out[line])
    if "md" in brand["rounded"]:
        if "md" not in index["rounded"]:
            raise InputError("design_rounded_md_missing")
        line = index["rounded"]["md"][1]
        out[line] = re.sub(r"(md:\s*).*$", lambda m: m[1] + brand["rounded"]["md"], out[line])
    if "name" in index["top"]:
        line = index["top"]["name"][1]
        out[line] = "name: " + json.dumps(f"{unquote(index['top']['name'][0])} with {brand['name']} brand")
    note = (f"> **Brand applied: {brand['name']}"
            + (" (fictional demo brand).**" if brand["fictional"] else ".**")
            + " Generated by `apply_brand.py`. The accent ramp, font families and control radius in the front matter"
            " are the brand's and win over any house value quoted in the prose below; everything else is the house"
            " system unchanged.")
    for i in range(end + 1, len(out)):
        if out[i].startswith("# "):
            out[i + 1:i + 1] = ["", note]
            break
    return "\n".join(out)


def write_out(path: Path, text: str, design_path: Path) -> None:
    if path.name.startswith(".env"):
        raise InputError("out_refused_env_file")
    if path.is_symlink():
        raise InputError("out_is_symlink")
    if path.exists() and (not path.is_file() or path.resolve() == design_path.resolve()):
        raise InputError("out_would_overwrite_source_or_non_file")
    if not path.parent.is_dir():
        raise InputError("out_parent_missing")
    fd, temp = tempfile.mkstemp(prefix=".apply_brand-", suffix=".md", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(text)
        os.replace(temp, path)
    except OSError:
        Path(temp).unlink(missing_ok=True)
        raise InputError("out_write_failed") from None


def run_lint(path: Path) -> dict:
    npx = shutil.which("npx")
    if not npx:
        raise InputError("npx_not_found")
    try:
        done = subprocess.run([npx, "-y", LINT_PACKAGE, "lint", str(path)], capture_output=True, text=True,
                              timeout=600, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise InputError("lint_did_not_run") from None
    start = done.stdout.find("{")
    try:
        summary = json.loads(done.stdout[start:])["summary"] if start >= 0 else None
    except (ValueError, KeyError, TypeError):
        summary = None
    if not isinstance(summary, dict):
        raise InputError("lint_output_unreadable")
    return {"package": LINT_PACKAGE, "exit_code": done.returncode, "summary": summary,
            "pass": summary.get("errors", 1) == 0 and summary.get("warnings", 1) == 0}


def locate_brand(arg: str) -> tuple[Path, Path]:
    path = Path(arg)
    if not path.exists() and re.fullmatch(r"[a-z0-9-]{1,64}", arg):
        path = BRANDS_DIR / arg
    if path.is_dir():
        path = path / "brand.yaml"
    return path, path.parent


# --------------------------------------------------------------------------- CLI

class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, "error: invalid arguments; use --help for the accepted interface.\n")


def main(argv: list[str] | None = None) -> int:
    parser = SafeArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--brand", required=True, help="brand.yaml path, brand directory, or shipped brand slug.")
    parser.add_argument("--design", type=Path, default=HOUSE_DESIGN, help="House DESIGN.md (default: this skill's).")
    parser.add_argument("--out", type=Path, help="Write the merged DESIGN.md here (only when every check passes).")
    parser.add_argument("--format", choices=("json", "css"), default="json", help="json report (default) or css block only.")
    parser.add_argument("--lint", action="store_true", help=f"Also run npx -y {LINT_PACKAGE} lint (network).")
    parser.add_argument("--dry-run", action="store_true", help="Report only; never write or run npx.")
    args = parser.parse_args(argv)

    def fail(exc: InputError) -> int:
        payload = {"schema_version": 1, "error": exc.code}
        if exc.detail:
            payload["key" if exc.code == "key_not_in_override_surface" else "detail"] = exc.detail
        if args.format == "json":
            print(json.dumps(payload))
        print(f"error: {exc.code}" + (f": {exc.detail}" if exc.detail else ""), file=sys.stderr)
        return 2

    try:
        brand_path, brand_dir = locate_brand(args.brand)
        design_text = read_bounded(args.design, MAX_DESIGN_BYTES, "design")
        lines, end, index = parse_front_matter(design_text)
        house_colors = {k: v for k, (v, _) in index["colors"].items()}
        house_font = house_fonts("\n".join(lines[end + 1:]))
        brand = validate_brand(parse_brand(read_bounded(brand_path, MAX_BRAND_BYTES, "brand")), house_colors, brand_dir)
        colors = {**house_colors, **brand["colors"]}
        pairs = contrast_checks(colors, index["components"], set(brand["colors"]))
        css, css_parts = css_block(brand, colors, house_colors, brand["fonts"], house_font)
        merged = merge(lines, end, index, brand, house_font)
    except InputError as exc:
        return fail(exc)

    gamut = [{"token": k, "value": v, "in_srgb_gamut": in_gamut(v)} for k, v in brand["colors"].items()]
    failing = [p for p in pairs if not p["pass"]]
    out_of_gamut = [g["token"] for g in gamut if not g["in_srgb_gamut"]]
    passed = not failing and not out_of_gamut
    written = lint = None
    try:
        if args.out and passed and not args.dry_run:
            write_out(args.out, merged, args.design)
            written = str(args.out)
        if args.lint and passed and not args.dry_run:
            if written:
                lint = run_lint(args.out)
            else:
                with tempfile.TemporaryDirectory(prefix="apply_brand-") as temp:
                    target = Path(temp) / "DESIGN.md"
                    target.write_text(merged, encoding="utf-8")
                    lint = run_lint(target)
    except InputError as exc:
        return fail(exc)
    status = "pass" if passed and (lint is None or lint["pass"]) else "fail"

    report = {
        "schema_version": 1,
        "read_only": written is None and lint is None,
        "status": status,
        "brand": {"name": brand["name"], "fictional": brand["fictional"], "file": brand_path.as_posix()},
        "design": args.design.as_posix(),
        "overrides": {k: brand[k] for k in ("colors", "fonts", "rounded", "logo")},
        "checks": {
            "floors": {"text": TEXT_FLOOR, "ui": UI_FLOOR},
            "pairs_checked": len(pairs),
            "failing": [f"{p['foreground']} on {p['background']}: {p['ratio']} < {p['floor']}" for p in failing],
            "out_of_srgb_gamut": out_of_gamut,
            "pairs": pairs,
        },
        "separation": separation(colors, house_colors),
        "css": css,
        **css_parts,
        "written": written,
        "would_write": str(args.out) if args.out and args.dry_run else None,
        "lint": lint,
        "limitations": [
            "Contrast is computed, not measured in a rendered page; hover and active states are checked for text only.",
            "Separation distances are informational; colour-blind simulation is not run.",
            "Without --lint the DESIGN.md linter is not run; the merged file is written only with --out.",
        ],
    }
    if args.format == "css":
        print(css, end="")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    for item in report["checks"]["failing"]:
        print(f"fail: {item}", file=sys.stderr)
    for token in out_of_gamut:
        print(f"fail: {token} is outside the sRGB gamut", file=sys.stderr)
    if lint and not lint["pass"]:
        print(f"fail: lint reported {lint['summary']}", file=sys.stderr)
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
