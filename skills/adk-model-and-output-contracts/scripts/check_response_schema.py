#!/usr/bin/env python3
"""Check a JSON Schema against the Gemini structured-output subset. Read-only; never imports the schema's Python source."""

import argparse
import json
import os
from pathlib import Path
import stat


# Keywords listed on https://ai.google.dev/gemini-api/docs/structured-output (page dated
# 2026-09-23) plus the OpenAPI-style spellings the google-genai Schema type carries.
SUPPORTED = {"type", "title", "description", "properties", "required", "additionalProperties",
             "enum", "format", "minimum", "maximum", "items", "prefixItems", "minItems",
             "maxItems", "anyOf", "$ref", "$defs", "definitions", "nullable",
             "propertyOrdering", "default", "$schema", "$id", "examples", "example"}
# Keywords Google's documented subset leaves out. Presence yields exit code 1.
UNSUPPORTED = {"pattern", "minLength", "maxLength", "oneOf", "allOf", "not", "const",
               "patternProperties", "dependentRequired", "dependentSchemas", "uniqueItems",
               "multipleOf", "exclusiveMinimum", "exclusiveMaximum", "if", "then", "else",
               "contains", "minContains", "maxContains", "minProperties", "maxProperties",
               "propertyNames", "unevaluatedProperties", "unevaluatedItems", "contentEncoding",
               "contentMediaType", "contentSchema", "$dynamicRef", "$dynamicAnchor", "$anchor"}
ANNOTATIONS = {"title", "description", "default", "examples", "example", "$schema", "$id", "deprecated",
               "readOnly", "writeOnly", "$comment"}


def positive(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a positive integer") from None
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


class Analysis:
    def __init__(self, root, args):
        self.root = root
        self.args = args
        self.findings = []
        self.stats = {"max_depth": 0, "property_count": 0, "required_count": 0,
                      "optional_count": 0, "enum_total": 0, "enum_max": 0, "ref_count": 0,
                      "unresolved_ref_count": 0, "recursive_ref_count": 0,
                      "nullable_styles": {"type_array_null": 0, "nullable_keyword": 0, "anyof_null": 0}}

    def finding(self, path, label, detail=None, severity="review"):
        row = {"path": path, "finding": label, "severity": severity}
        if detail is not None:
            row["detail"] = detail
        self.findings.append(row)

    def resolve(self, ref):
        if not isinstance(ref, str) or not ref.startswith("#/"):
            return None
        node = self.root
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return None
        return node if isinstance(node, dict) else None

    def visit(self, node, path, depth, active_refs):
        if not isinstance(node, dict):
            if isinstance(node, bool):
                return
            self.finding(path, "schema_not_an_object", severity="unsupported")
            return
        self.stats["max_depth"] = max(self.stats["max_depth"], depth)
        for key in sorted(node):
            if key in UNSUPPORTED:
                self.finding(path, "unsupported_keyword", key, severity="unsupported")
            elif key not in SUPPORTED and key not in ANNOTATIONS:
                self.finding(path, "unrecognised_keyword", key, severity="info")
        types = node.get("type")
        type_list = types if isinstance(types, list) else [types] if types else []
        if isinstance(types, list) and "null" in types:
            self.stats["nullable_styles"]["type_array_null"] += 1
        if node.get("nullable") is True:
            self.stats["nullable_styles"]["nullable_keyword"] += 1
        if "$ref" in node:
            self.stats["ref_count"] += 1
            target = node["$ref"]
            if target in active_refs:
                self.stats["recursive_ref_count"] += 1
                self.finding(path, "recursive_ref", target, severity="info")
            else:
                resolved = self.resolve(target)
                if resolved is None:
                    self.stats["unresolved_ref_count"] += 1
                    self.finding(path, "unresolved_ref", target if isinstance(target, str) else None,
                                 severity="unsupported")
                else:
                    self.visit(resolved, path, depth, active_refs | {target})
        enum = node.get("enum")
        if isinstance(enum, list):
            self.stats["enum_total"] += len(enum)
            self.stats["enum_max"] = max(self.stats["enum_max"], len(enum))
            if len(enum) > self.args.max_enum:
                self.finding(path, "enum_cardinality_exceeds_limit", len(enum))
            for value in enum:
                if isinstance(value, str) and len(value) > self.args.max_name_length:
                    self.finding(path, "long_enum_value", len(value))
        any_of = node.get("anyOf")
        if isinstance(any_of, list):
            if any(isinstance(option, dict) and option.get("type") == "null" for option in any_of):
                self.stats["nullable_styles"]["anyof_null"] += 1
            for index, option in enumerate(any_of):
                self.visit(option, f"{path}/anyOf/{index}", depth, active_refs)
        properties = node.get("properties")
        if isinstance(properties, dict):
            required = node.get("required") if isinstance(node.get("required"), list) else []
            if "object" not in type_list and types is not None:
                self.finding(path, "properties_without_object_type", severity="info")
            for name in sorted(properties):
                self.stats["property_count"] += 1
                if name in required:
                    self.stats["required_count"] += 1
                else:
                    self.stats["optional_count"] += 1
                if len(name) > self.args.max_name_length:
                    self.finding(f"{path}/properties/{name}", "long_property_name", len(name))
                self.visit(properties[name], f"{path}/properties/{name}", depth + 1, active_refs)
            missing = sorted(set(required) - set(properties))
            if missing:
                self.finding(path, "required_names_not_in_properties", missing, severity="unsupported")
        for key in ("items", "additionalProperties"):
            if isinstance(node.get(key), dict):
                self.visit(node[key], f"{path}/{key}", depth + 1, active_refs)
        if isinstance(node.get("prefixItems"), list):
            for index, item in enumerate(node["prefixItems"]):
                self.visit(item, f"{path}/prefixItems/{index}", depth + 1, active_refs)

    def finish(self):
        if self.stats["max_depth"] > self.args.max_depth:
            self.finding("#", "nesting_depth_exceeds_limit", self.stats["max_depth"])
        if self.stats["property_count"] > self.args.max_properties:
            self.finding("#", "property_count_exceeds_limit", self.stats["property_count"])
        styles = [name for name, count in self.stats["nullable_styles"].items() if count]
        if len(styles) > 1:
            self.finding("#", "mixed_nullable_styles", styles, severity="info")
        if self.stats["optional_count"] > self.stats["required_count"]:
            self.finding("#", "optional_fields_outnumber_required", self.stats["optional_count"], severity="info")
        self.findings.sort(key=lambda item: json.dumps(item, sort_keys=True))


def load_schema(path, max_bytes, parser):
    try:
        if path.is_symlink():
            parser.error("schema must be a regular file, not a symlink")
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(fd, "rb") as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                parser.error("schema must be a regular file")
            raw = source.read(max_bytes + 1)
    except OSError:
        parser.error("schema file is unreadable")
    if len(raw) > max_bytes:
        parser.error("schema file exceeds --max-bytes")
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)
    except (UnicodeError, ValueError):
        parser.error("schema file is not valid JSON without duplicate keys")
    if not isinstance(document, dict):
        parser.error("schema document must be a JSON object")
    return document


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Exit 0: inspected, no unsupported keywords. Exit 1: unsupported keywords or unresolved refs. "
               "Exit 2: bad arguments or unreadable schema. Limits are yardsticks (Google publishes no numeric "
               "limits); findings direct inspection and do not certify provider acceptance.")
    parser.add_argument("--schema", required=True, help="JSON Schema file (raw dict schema, or the output of model_json_schema())")
    parser.add_argument("--pydantic-json", action="store_true", help="the file was produced by Pydantic model_json_schema(); report Pydantic's anyOf-null Optional style as expected")
    parser.add_argument("--max-depth", type=positive, default=10, help="nesting depth yardstick (default: 10)")
    parser.add_argument("--max-properties", type=positive, default=100, help="total property count yardstick (default: 100)")
    parser.add_argument("--max-enum", type=positive, default=100, help="per-enum cardinality yardstick (default: 100)")
    parser.add_argument("--max-name-length", type=positive, default=64, help="property name or enum value length yardstick (default: 64)")
    parser.add_argument("--max-bytes", type=positive, default=1048576, help="maximum schema file size (default: 1048576)")
    args = parser.parse_args()
    document = load_schema(Path(args.schema), args.max_bytes, parser)
    analysis = Analysis(document, args)
    analysis.visit(document, "#", 0, frozenset())
    analysis.finish()
    unsupported = [row for row in analysis.findings if row["severity"] == "unsupported"]
    report = {"schema_version": 1, "read_only": True, "source": "pydantic_model_json_schema" if args.pydantic_json else "json_schema",
              "limits": {"max_depth": args.max_depth, "max_properties": args.max_properties,
                         "max_enum": args.max_enum, "max_name_length": args.max_name_length},
              "status": "unsupported_keywords" if unsupported else "inspected",
              "stats": analysis.stats, "findings": analysis.findings,
              "note": "Documented subset only; the live backend, model and google-genai version decide acceptance."}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if unsupported else 0


if __name__ == "__main__":
    raise SystemExit(main())
