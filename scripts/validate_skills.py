#!/usr/bin/env python3
"""Check distributable skill packages offline without executing bundled code.

Agent Skills frontmatter rules: https://agentskills.io/specification
LICENSE and agents/openai.yaml are this repository's additional conventions.
Markdown links are resolved relative to the Markdown file that contains them.
This checks packaging, not instruction quality, routing, or runtime correctness.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import yaml
from yaml.constructor import ConstructorError


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loading with duplicate mapping keys rejected at every depth."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in mapping
            except TypeError as exc:
                raise ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    "found an unhashable key", key_node.start_mark,
                ) from exc
            if duplicate:
                raise ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    f"found duplicate key {key!r}", key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


@dataclass
class PackageStats:
    name: str
    lines: int = 0
    words: int = 0
    markdown_files: int = 0
    python_files: int = 0


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    packages: list[PackageStats] = field(default_factory=list)

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"{path}: {message}")


def read_text(path: Path, report: Report) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        report.error(path, f"cannot read UTF-8 text: {exc}")
        return None


def load_mapping(text: str, path: Path, report: Report) -> dict | None:
    try:
        value = yaml.load(text, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        report.error(path, f"invalid YAML: {exc}")
        return None
    if not isinstance(value, dict):
        report.error(path, "YAML must be a mapping")
        return None
    return value


def string_field(mapping: dict, key: str, path: Path, report: Report,
                 *, maximum: int | None = None) -> str | None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        report.error(path, f"{key} must be a non-empty string")
        return None
    if maximum is not None and len(value) > maximum:
        report.error(path, f"{key} exceeds {maximum} characters")
    return value


def check_frontmatter(text: str, path: Path, package: Path,
                      report: Report) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        report.error(path, "must begin with YAML frontmatter delimited by ---")
        return text
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        report.error(path, "YAML frontmatter has no closing --- delimiter")
        return ""
    body = "".join(lines[end + 1:])
    if not body.strip():
        report.error(path, "skill instructions are empty")
    data = load_mapping("".join(lines[1:end]), path, report)
    if data is None:
        return body
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    for key in data:
        if key not in allowed:
            report.error(path, f"unsupported frontmatter field {key!r}; put extensions in metadata")
    name = string_field(data, "name", path, report, maximum=64)
    if name is not None:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            report.error(path, "name must use lowercase letters/digits and single separating hyphens")
        if name != package.name:
            report.error(path, f"name {name!r} does not match directory {package.name!r}")
    string_field(data, "description", path, report, maximum=1024)
    for key, maximum in (("license", None), ("compatibility", 500), ("allowed-tools", None)):
        if key in data:
            string_field(data, key, path, report, maximum=maximum)
    if "metadata" in data:
        metadata = data["metadata"]
        if not isinstance(metadata, dict) or any(
            not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items()
        ):
            report.error(path, "metadata must map string keys to string values")
    return body


def contained_file(path: Path, package: Path, report: Report) -> bool:
    try:
        resolved = path.resolve(strict=True)
        if not resolved.is_relative_to(package.resolve()):
            report.error(path, "resource escapes its skill package")
            return False
        if not resolved.is_file():
            report.error(path, "resource must be a file")
            return False
    except (OSError, RuntimeError, ValueError) as exc:
        report.error(path, f"missing or unreadable resource: {exc}")
        return False
    return True


def check_interface(package: Path, report: Report) -> None:
    path = package / "agents" / "openai.yaml"
    if not contained_file(path, package, report):
        return
    text = read_text(path, report)
    data = load_mapping(text, path, report) if text is not None else None
    if data is None:
        return
    interface = data.get("interface")
    if not isinstance(interface, dict):
        report.error(path, "interface must be a mapping")
        return
    string_field(interface, "display_name", path, report)
    short = string_field(interface, "short_description", path, report, maximum=64)
    if short is not None and len(short) < 25:
        report.error(path, "short_description must have 25–64 characters")
    prompt = string_field(interface, "default_prompt", path, report)
    if prompt is not None and not re.search(r"\$" + re.escape(package.name) + r"(?![\w-])", prompt):
        report.error(path, f"default_prompt must explicitly invoke ${package.name}")
    if "policy" in data:
        policy = data["policy"]
        if not isinstance(policy, dict):
            report.error(path, "policy must be a mapping")
        elif "allow_implicit_invocation" in policy and not isinstance(policy["allow_implicit_invocation"], bool):
            report.error(path, "policy.allow_implicit_invocation must be a boolean")


def markdown_destinations(text: str):
    """Return actual CommonMark link/image destinations, excluding code examples."""
    def walk(tokens):
        for token in tokens:
            if token.type == "link_open":
                yield token.attrGet("href")
            elif token.type == "image":
                yield token.attrGet("src")
            if token.children:
                yield from walk(token.children)

    parser = MarkdownIt("commonmark")
    # Parse only, never render: retain file: links so non-portable paths are diagnosed.
    parser.validateLink = lambda destination: True
    yield from walk(parser.parse(text))


def check_markdown_links(text: str, path: Path, package: Path, report: Report) -> None:
    for destination in markdown_destinations(text):
        try:
            parsed = urlsplit(destination)
        except ValueError as exc:
            report.error(path, f"invalid link {destination!r}: {exc}")
            continue
        if parsed.scheme == "file":
            report.error(path, f"local link {destination!r} must be relative to its skill package")
            continue
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue  # External links are not fetched; heading fragments are not checked.
        local = Path(unquote(parsed.path))
        target = path.parent / local
        if local.is_absolute():
            report.error(path, f"local link {destination!r} must be relative to its skill package")
        elif not contained_file(target, package, report):
            report.error(path, f"invalid local link {destination!r}")


def package_files(package: Path, report: Report):
    """Never follow directory symlinks outside a package or execute its contents."""
    def walk_error(exc):
        report.error(Path(exc.filename) if exc.filename else package, f"cannot inspect directory: {exc}")

    for directory, dirs, files in os.walk(package, followlinks=False, onerror=walk_error):
        for name in dirs:
            path = Path(directory) / name
            if path.is_symlink():
                try:
                    if not path.resolve(strict=True).is_relative_to(package.resolve()):
                        report.error(path, "directory symlink escapes its skill package")
                except (OSError, RuntimeError, ValueError) as exc:
                    report.error(path, f"unreadable directory symlink: {exc}")
        for name in files:
            path = Path(directory) / name
            if contained_file(path, package, report):
                yield path


def validate_package(package: Path, report: Report) -> None:
    stats = PackageStats(package.name)
    report.packages.append(stats)
    entrypoint = package / "SKILL.md"
    body = None
    if contained_file(entrypoint, package, report):
        text = read_text(entrypoint, report)
        if text is not None:
            stats.lines = len(text.splitlines())
            stats.words = len(text.split())
            if stats.lines > 500:
                report.warnings.append(f"{entrypoint}: {stats.lines} lines; consider progressive disclosure (not a quality score)")
            body = check_frontmatter(text, entrypoint, package, report)
    license_path = package / "LICENSE"
    if contained_file(license_path, package, report):
        license_text = read_text(license_path, report)
        if license_text is not None and not license_text.strip():
            report.error(license_path, "bundled license is empty")
    check_interface(package, report)
    for path in package_files(package, report):
        if path.suffix.lower() == ".md":
            stats.markdown_files += 1
            text = body if path == entrypoint else read_text(path, report)
            if text is not None:
                check_markdown_links(text, path, package, report)
        elif path.suffix == ".py":
            stats.python_files += 1
            try:
                compile(path.read_bytes(), str(path), "exec")
            except (OSError, SyntaxError, ValueError) as exc:
                report.error(path, f"Python syntax check failed: {exc}")


def validate_repository(root: Path) -> Report:
    report = Report()
    skills = root / "skills"
    if not skills.is_dir():
        report.error(skills, "skills directory is missing")
        return report
    packages = sorted(path for path in skills.iterdir() if path.is_dir() or path.is_symlink())
    if not packages:
        report.error(skills, "no skill packages found")
    for package in packages:
        if package.is_symlink():
            report.error(package, "repository skill directories must not be symlinks")
            continue
        validate_package(package, report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="repository containing skills/ (default: this script's repository)")
    args = parser.parse_args(argv)
    report = validate_repository(args.root.resolve())
    for package in report.packages:
        print(f"{package.name}: SKILL.md {package.lines} lines / {package.words} words; "
              f"{package.markdown_files} Markdown files; {package.python_files} Python files")
    for warning in report.warnings:
        print(f"WARNING {warning}")
    for error in report.errors:
        print(f"ERROR {error}")
    print(f"Checked {len(report.packages)} skill packages: "
          f"{len(report.errors)} errors, {len(report.warnings)} warnings.")
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
