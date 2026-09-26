"""Score synthetic extraction/retrieval observations, never PDF or answer quality.

Expected sections stay evaluator-side. Observations are adapter records, not
model-produced claims of coverage. See references/local-document-coverage.md.
"""

import argparse
import json
from pathlib import Path


FIXTURE = Path(__file__).resolve().parents[1] / "assets" / "document-coverage.json"


def score(fixture, question_id, observation):
    """Return separate coverage metrics and actionable missing-evidence reasons."""
    segments = fixture["segments"]
    required_sections = set(fixture["questions"][question_id]["required_sections"])
    known_sections = {segment["section"] for segment in segments.values()}
    if not required_sections or not required_sections <= known_sections:
        raise ValueError("expected sections must be nonempty and present in the inventory")
    required = {key: value for key, value in segments.items()
                if value["section"] in required_sections}
    required_documents = {value["document"] for value in required.values()}
    available = set(observation["available_documents"])
    extracted = observation["extracted_segments"]
    valid_hits = {}
    invalid_hits = []
    for hit in observation["hits"]:
        key = hit.get("segment")
        source = segments.get(key)
        text = hit.get("text")
        if (source is None or source["document"] not in available
                or not isinstance(text, str) or not text.strip()
                or text not in extracted.get(key, "")
                or text not in source["text"]):
            invalid_hits.append(key)
            continue
        valid_hits.setdefault(key, []).append(text)

    returned_documents = {segments[key]["document"] for key in valid_hits}
    complete_segments = set()
    diagnoses = []
    for key, source in required.items():
        reasons = []
        if source["document"] not in available or key not in extracted:
            reasons.append("absent_content")
        elif source.get("visual_required"):
            # There are deliberately no image bytes in this fixture. A caller's
            # claimed review cannot turn the placeholder into reviewed evidence.
            if not extracted[key].strip():
                reasons.append("empty_extraction")
            reasons.append("unviewed_visuals")
        elif not extracted[key].strip():
            reasons.append("empty_extraction")
        elif source["text"] not in extracted[key]:
            reasons.append("section_truncation")
        elif key not in valid_hits:
            reasons.append("query_miss")
        elif not any(source["text"] in text for text in valid_hits[key]):
            reasons.append("section_truncation")
        else:
            complete_segments.add(key)
        for reason in reasons:
            diagnoses.append({"segment": key, "document": source["document"],
                              "page": source["page"], "reason": reason})

    complete_sections = {
        section for section in required_sections
        if all(key in complete_segments for key, source in required.items()
               if source["section"] == section)
    }
    covered_documents = required_documents & returned_documents
    retrieval_pass = (covered_documents == required_documents
                      and complete_sections == required_sections
                      and not invalid_hits)
    return {
        "question": question_id,
        "document_coverage": {"covered": len(covered_documents),
                              "required": len(required_documents)},
        "operative_section_coverage": {"covered": len(complete_sections),
                                       "required": len(required_sections)},
        "diagnoses": diagnoses,
        "invalid_hit_segments": invalid_hits,
        "query_origin": observation["query_origin"],
        "queries": observation["queries"],
        "retrieval_pass": retrieval_pass,
        "agent_query_exercised": (observation["query_origin"] == "agent"
                                  and isinstance(observation["queries"], list)
                                  and bool(observation["queries"])
                                  and all(isinstance(q, str) and q.strip()
                                          for q in observation["queries"])),
        "evidence_result": "complete_fixture_spans" if retrieval_pass else "unresolved_evidence",
        "answer_support": "not_scored",
        "pdf_extraction": "not_exercised",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", required=True)
    parser.add_argument("--observation", type=Path, required=True)
    args = parser.parse_args()
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    observation = json.loads(args.observation.read_text(encoding="utf-8"))
    report = score(fixture, args.question, observation)
    print(json.dumps(report, indent=2))
    return 0 if report["retrieval_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
