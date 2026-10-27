"""Run the bundled local retriever (unchanged limits) over the coverage fixture pages.

Usage: python -I probe_retriever.py SKILL_SCRIPTS_DIR FIXTURE
Prints, per question, the units the retriever actually returned. Evaluator-side
required sections are not passed to the retriever.
"""
import importlib.util
import json
import sys
from pathlib import Path


def load(path):
    spec = importlib.util.spec_from_file_location("local_retrieval", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["local_retrieval"] = module
    spec.loader.exec_module(module)
    return module


def pages_from_fixture(fixture):
    return [{"document": s["document"], "page": s["page"], "text": s["text"]}
            for s in fixture["segments"].values()]


def main():
    lr = load(Path(sys.argv[1]) / "local_retrieval.py")
    fixture = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    kept, screened = lr.screen_units(lr.chunk_by_heading(pages_from_fixture(fixture)))
    print("screened:", json.dumps(screened))
    for unit in kept:
        print("unit:", json.dumps(unit))
    conn = lr.build_index(kept)
    issues = [{"id": q, "query": v["question"]} for q, v in fixture["questions"].items()]
    report = lr.retrieve_for_issues(conn, issues)  # default k=4, default call budget
    print(json.dumps(report, indent=1))
    print("problems:", lr.sufficiency_problems(report))


main()
