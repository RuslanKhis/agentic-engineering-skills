"""Loads and validates the semantic map kept in reviewed YAML under `semantic/`.

Layout (models and relationships follow WrenAI's MDL; domains are ours, MDL has no such construct):
    semantic/models/<table>.yml      physical table, primary key, columns
    semantic/relationships.yml       named joins: models, join_type (cardinality), condition
    semantic/domains/<domain>.yml    tables and exposed columns, relationships, derived SQL

`problems()` is the CI gate. It fails on anything structural; `wren context validate` only warns on
several of these and is not a substitute.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from analytics.checks import RejectedSQL, check_candidate

ROOT = Path(__file__).resolve().parent.parent / "semantic"
JOIN_TYPES = {"ONE_TO_ONE", "ONE_TO_MANY", "MANY_TO_ONE", "MANY_TO_MANY"}
CONDITION = re.compile(r"^\s*(\w+)\.(\w+)\s*=\s*(\w+)\.(\w+)\s*$")
LEGACY_TYPES = {"INTEGER": "INT64", "FLOAT": "FLOAT64", "BOOLEAN": "BOOL", "RECORD": "STRUCT"}


def normalise_type(name: str | None) -> str | None:
    return LEGACY_TYPES.get(name.upper(), name.upper()) if name else None


def _read(path: Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _load(root: Path):
    models = {p.stem: _read(p) for p in sorted((root / "models").glob("*.yml"))}
    relationships = (_read(root / "relationships.yml") or {})
    domains = {p.stem: _read(p) for p in sorted((root / "domains").glob("*.yml"))}
    return models, relationships, domains


def _parse_condition(rel: dict):
    """Returns {table: column} for the two sides of an equality condition, or None."""
    m = CONDITION.match(str(rel.get("condition", "")))
    if not m or m.group(1) == m.group(3):
        return None
    return {m.group(1): m.group(2), m.group(3): m.group(4)}


def problems(root: Path = ROOT, require_review: bool = True, check_sql: bool = True) -> list[str]:
    errors: list[str] = []
    try:
        models, rel_file, domains = _load(root)
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot read semantic files: {exc}"]

    def review(label: str, doc: dict) -> None:
        if require_review and not (doc.get("reviewed_by") and doc.get("reviewed_on")):
            errors.append(f"{label}: reviewed_by and reviewed_on are required")

    for stem, model in models.items():
        label = f"model {stem}"
        if not isinstance(model, dict) or model.get("name") != stem:
            errors.append(f"{label}: name must equal the file name")
            continue
        review(label, model)
        ref = model.get("table_reference") or {}
        if not all(ref.get(k) for k in ("project", "dataset", "table")):
            errors.append(f"{label}: table_reference needs project, dataset and table")
        names = [c.get("name") for c in model.get("columns") or []]
        if not names or len(set(names)) != len(names):
            errors.append(f"{label}: columns missing or duplicated")
        pk = model.get("primary_key") or []
        if not pk:
            errors.append(f"{label}: no primary_key")
        elif not set(pk) <= set(names):
            errors.append(f"{label}: primary_key names an unknown column")

    rels: dict[str, dict] = {}
    review("relationships.yml", rel_file)
    for rel in rel_file.get("relationships") or []:
        name = rel.get("name")
        label = f"relationship {name}"
        if not name or name in rels:
            errors.append(f"{label}: name missing or duplicated")
            continue
        rels[name] = rel
        pair = rel.get("models") or []
        if len(pair) != 2 or any(m not in models for m in pair) or pair[0] == pair[1]:
            errors.append(f"{label}: models must be two distinct known models")
            continue
        join_type = rel.get("join_type")
        if join_type not in JOIN_TYPES:
            errors.append(f"{label}: join_type missing or not one of {sorted(JOIN_TYPES)}")
            continue
        if join_type == "MANY_TO_MANY":
            errors.append(f"{label}: MANY_TO_MANY needs a reviewed fan-out test before it is allowed")
        sides = _parse_condition(rel)
        if sides is None or set(sides) != set(pair):
            errors.append(f"{label}: condition must be `a.col = b.col` over exactly its two models")
            continue
        known = True
        for table, col in sides.items():
            if col not in {c.get("name") for c in models[table].get("columns") or []}:
                errors.append(f"{label}: {table}.{col} is not a column of the model")
                known = False
        if not known:
            continue
        one_side = {"MANY_TO_ONE": [pair[1]], "ONE_TO_MANY": [pair[0]], "ONE_TO_ONE": pair}.get(join_type, [])
        for table in one_side:
            if set(models[table].get("primary_key") or []) != {sides[table]}:
                errors.append(f"{label}: the one side {table} must join on its primary key")

    for stem, dom in domains.items():
        label = f"domain {stem}"
        if not isinstance(dom, dict) or dom.get("name") != stem:
            errors.append(f"{label}: name must equal the file name")
            continue
        review(label, dom)
        tables = dom.get("tables") or {}
        if not tables:
            errors.append(f"{label}: no tables")
        for table, cols in tables.items():
            if table not in models:
                errors.append(f"{label}: unknown table {table}")
                continue
            have = {c.get("name") for c in models[table].get("columns") or []}
            missing = set(cols or []) - have
            if missing or not cols:
                errors.append(f"{label}: {table} exposes unknown or no columns {sorted(missing)}")
        for name in dom.get("relationships") or []:
            rel = rels.get(name)
            if rel is None:
                errors.append(f"{label}: unknown relationship {name}")
            elif not set(rel.get("models") or []) <= set(tables):
                errors.append(f"{label}: relationship {name} uses a table outside the domain")
            else:
                for table, col in (_parse_condition(rel) or {}).items():
                    if col not in (tables.get(table) or []):
                        errors.append(f"{label}: relationship {name} uses unexposed column {table}.{col}")
        for name, sql in (dom.get("derived") or {}).items():
            if name in tables:
                errors.append(f"{label}: derived table {name} shadows a table")
            if not check_sql:
                continue
            try:
                check_candidate(str(sql), set(tables))
            except RejectedSQL as exc:
                errors.append(f"{label}: derived {name} rejected by the SQL policy: {exc}")
            except Exception as exc:  # unparseable SQL, or sqlglot missing: fail, never skip
                errors.append(f"{label}: derived {name} cannot be checked: {exc}")
    return errors


def build_domains(root: Path = ROOT) -> dict:
    """Builds the `DOMAINS` shape the metadata collector and generated route consume."""
    # Import-time load is structural only; the SQL policy and review gates run in CI (`main`).
    errors = problems(root, require_review=False, check_sql=False)
    if errors:
        raise ValueError("invalid semantic map: " + "; ".join(errors))
    models, rel_file, domains = _load(root)
    rels = {r["name"]: r for r in rel_file.get("relationships") or []}
    out = {}
    for name, dom in domains.items():
        tables = {}
        for table, cols in dom["tables"].items():
            declared = {c["name"]: normalise_type(c.get("type")) for c in models[table]["columns"]}
            tables[table] = {"key": list(models[table]["primary_key"]), "columns": list(cols),
                             "types": {c: declared[c] for c in cols}}
        relationships = []
        for rel_name in dom.get("relationships") or []:
            rel = rels[rel_name]
            first, second = rel["models"]
            sides = _parse_condition(rel)
            relationships.append({"from": f"{first}.{sides[first]}", "to": f"{second}.{sides[second]}",
                                  "cardinality": rel["join_type"].lower()})
        out[name] = {"description": dom["description"], "tables": tables, "relationships": relationships,
                     "derived": dict(dom.get("derived") or {})}
    return out


def main() -> int:
    errors = problems()
    for e in errors:
        print(f"FAIL {e}")
    print("semantic map OK" if not errors else f"{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
