"""Synthetic fail-before/pass-after examples, not a production contract engine.

No SDK, PDF parsing, network or model inference. The tiny normal JSON route below
checks actual calls and persisted bytes. Its fixture oracle is an authored test
control, never a semantic judge or evidence of independent source review.
"""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock


ASSET = Path(__file__).resolve().parents[1] / "assets/contract-qualification.json"


class PreflightError(ValueError):
    pass


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")


def fingerprint(pack):
    # This synthetic producer depends on extraction, coordinates and selection.
    return hashlib.sha256(encoded({key: pack[key] for key in (
        "parser_version", "passages", "selected_pack", "required_ids"
    )})).hexdigest()


def compile_contract(pack):
    """One trusted source registry supplies the three concrete label boundaries."""
    sources = {row["id"]: row for row in pack["passages"]}
    labels = [sources[sid]["label"] for sid in pack["selected_pack"]]
    return {
        "prompt": "Select supplied labels only:\n" + "\n".join(labels),
        "schema": {"type": "array", "items": {"type": "string", "enum": labels}},
        "validator_catalog": {row["label"]: row["id"] for row in sources.values()
                              if row["id"] in pack["selected_pack"]},
        "max_refs": len(labels),
    }


def qualify(pack, contract, *, storage_limit):
    rows = pack["passages"]
    sources = {row["id"]: row for row in rows}
    if len(sources) != len(rows):
        raise PreflightError("duplicate source identity")
    selected = pack["selected_pack"]
    if len(selected) != len(set(selected)) or not set(selected) <= sources.keys():
        raise PreflightError("invalid selected identities")
    labels = [sources[sid]["label"] for sid in selected]
    if len(labels) != len(set(labels)):
        raise PreflightError("ambiguous source labels")
    expected = compile_contract(pack)
    if contract["prompt"] != expected["prompt"]:
        raise PreflightError("prompt omits or changes label convention")
    if (contract["schema"] != expected["schema"] or
            contract["validator_catalog"] != expected["validator_catalog"]):
        raise PreflightError("schema and validator disagree with registry")
    if not set(pack["required_ids"]) <= set(selected):
        raise PreflightError("missing required content")
    for sid in selected:
        row = sources[sid]
        if not set(row["requires"]) <= set(selected):
            raise PreflightError("missing qualification or neighbour")
        if row["text"] is None:
            raise PreflightError("unsupported unreviewed visual")
    if len(pack["required_ids"]) > contract["max_refs"]:
        raise PreflightError("required dense content is unrepresentable")
    # Honest offline storage reference, not an estimate of unknown model output.
    if len(encoded({"sources": rows, "source_hash": fingerprint(pack)})) > storage_limit:
        raise PreflightError("reference envelope exceeds storage limit")
    return sources


def fixture_support(observation, source_ids, sources, pack):
    """Test-only independent control; ignores model-declared support labels."""
    required = {"rule-head", "rule-tail", "note-1"}
    if (not required <= set(source_ids) or
            observation not in pack["fixture_meanings"]["workshop-rule"]):
        raise ValueError("unsupported meaning or incomplete operative evidence")
    return [sources[sid]["text"] for sid in source_ids]


def normal_route(pack, contract, provider, checkpoint, *, storage_limit=100_000,
                 expected_source_hash=None, reuse_saved=False, settings=None):
    """Toy normal entrypoint: preflight, counted generation, consume, save, reopen.

    The oracle expectations are withheld from generation. Authentication, atomic
    storage, actual Runner and remote-provider schema enforcement are outside it.
    """
    sources = qualify(pack, contract, storage_limit=storage_limit)
    if expected_source_hash is not None and expected_source_hash != fingerprint(pack):
        raise PreflightError("stale producer dependencies")
    if settings is None:
        settings = {"model": "synthetic-model", "output_limit": 4096}
    producer_hash = hashlib.sha256(encoded({"source_hash": fingerprint(pack),
                                           "contract": contract,
                                           "settings": settings})).hexdigest()
    if reuse_saved:
        saved = json.loads(checkpoint.read_bytes())
        if saved["producer_hash"] != producer_hash:
            raise PreflightError("stale saved-stage dependencies")
        resolved = fixture_support(saved["observation"], saved["source_ids"], sources, pack)
        if saved["literal_spans"] != resolved:
            raise PreflightError("saved projection differs from authoritative spans")
        return saved
    generated = provider({"prompt": contract["prompt"], "schema": contract["schema"],
                          "sources": [sources[sid] for sid in pack["selected_pack"]]})
    labels = generated["labels"]
    catalog = contract["validator_catalog"]
    if not labels or len(labels) != len(set(labels)) or not set(labels) <= catalog.keys():
        raise ValueError("invalid response identities")
    ids = [catalog[label] for label in labels]
    texts = fixture_support(generated["observation"], ids, sources, pack)
    envelope = {"source_hash": fingerprint(pack), "producer_hash": producer_hash,
                "source_ids": ids,
                "literal_spans": texts, "observation": generated["observation"],
                "warnings": ["Synthetic expectations lack independent domain review."]}
    payload = encoded(envelope)
    if len(payload) > storage_limit:
        raise ValueError("result envelope exceeds storage limit")
    checkpoint.write_bytes(payload)
    return json.loads(checkpoint.read_bytes())


def broken_pack_adjacent(pack, first, second):
    return pack["selected_pack"].index(second) == pack["selected_pack"].index(first) + 1


def physically_adjacent(pack, first, second):
    sources = {row["id"]: row for row in pack["passages"]}
    left, right = sources[first], sources[second]
    return ((left["document"], left["version"]) == (right["document"], right["version"])
            and right["page"] == left["page"] + 1)


class ContractQualificationExamples(unittest.TestCase):
    def setUp(self):
        self.pack = json.loads(ASSET.read_text())
        self.contract = compile_contract(self.pack)
        self.provider = Mock(return_value={
            "labels": ["policy-v1/p2/1.2(a)(i)",
                       "policy-v1/p3/1.2(a)(i)-continued", "policy-v1/p3/footnote-1"],
            "observation": "A ramp is required on a raised floor even for a low-risk workshop.",
        })
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.checkpoint = Path(self.workspace.name) / "checkpoint.json"

    def run_route(self, **kwargs):
        return normal_route(self.pack, self.contract, self.provider, self.checkpoint, **kwargs)

    def assert_preflight(self, message, **kwargs):
        with self.assertRaisesRegex(PreflightError, message):
            self.run_route(**kwargs)
        self.provider.assert_not_called()
        self.assertFalse(self.checkpoint.exists())

    def test_prompt_defect_fails_before_dispatch_then_canonical_contract_passes(self):
        self.contract["prompt"] = "Explain workshop policy."
        self.assert_preflight("prompt omits")
        self.contract = compile_contract(self.pack)
        result = self.run_route()
        self.assertIn("except where the floor is raised", result["literal_spans"][1])
        self.provider.assert_called_once()
        self.assertNotIn("fixture_meanings", self.provider.call_args.args[0])

    def test_duplicate_labels_fail_then_distinct_occurrences_pass(self):
        self.pack["passages"][5]["label"] = self.pack["passages"][4]["label"]
        self.contract = compile_contract(self.pack)
        self.assert_preflight("ambiguous source labels")
        self.pack["passages"][5]["label"] = "policy-v1/p4/table-A/r2/c2"
        self.contract = compile_contract(self.pack)
        self.run_route()
        catalog = self.provider.call_args.args[0]["schema"]["items"]["enum"]
        self.assertIn("policy-v1/p4/table-A/r1/c2", catalog)
        self.assertIn("policy-v1/p4/table-A/r2/c2", catalog)

    def test_wire_schema_disagreement_blocks_the_normal_route(self):
        self.contract["schema"]["items"]["enum"] = ["invented-label"]
        self.assert_preflight("schema and validator disagree")

    def test_validator_disagreement_blocks_the_normal_route(self):
        self.contract["validator_catalog"]["policy-v1/p4/table-A/r1/c2"] = "cell-2"
        self.assert_preflight("schema and validator disagree")

    def test_dense_representation_fails_then_complete_capacity_passes(self):
        self.contract["max_refs"] = 3
        self.assert_preflight("unrepresentable")
        self.contract = compile_contract(self.pack)
        self.run_route()

    def test_missing_cross_page_qualification_blocks_before_generation(self):
        self.pack["selected_pack"].remove("rule-tail")
        self.contract = compile_contract(self.pack)
        self.assert_preflight("missing required content")

    def test_missing_footnote_link_blocks_even_if_required_list_is_incomplete(self):
        self.pack["selected_pack"].remove("note-1")
        self.pack["required_ids"].remove("note-1")
        self.contract = compile_contract(self.pack)
        self.assert_preflight("missing qualification")

    def test_unreviewed_image_is_a_preflight_result_not_model_failure(self):
        self.pack["selected_pack"].append("image-1")
        self.contract = compile_contract(self.pack)
        self.assert_preflight("unreviewed visual")

    def test_pack_adjacency_fails_both_directions_source_coordinates_pass(self):
        self.assertTrue(broken_pack_adjacent(self.pack, "rule-head", "table-head"))
        self.assertFalse(physically_adjacent(self.pack, "rule-head", "table-head"))
        self.assertFalse(broken_pack_adjacent(self.pack, "rule-head", "rule-tail"))
        self.assertTrue(physically_adjacent(self.pack, "rule-head", "rule-tail"))

    def test_regenerated_quote_fails_but_bound_literal_and_paraphrase_pass(self):
        literal = self.pack["passages"][0]["text"]
        regenerated = literal.replace("low-\nrisk", "low-risk")
        self.assertNotEqual(regenerated, literal)  # Retained broken exact-quote check.
        result = self.run_route()
        self.assertEqual(result["literal_spans"][0], literal)
        self.assertIn("low-risk", result["observation"])

    def test_other_supported_wording_passes_without_changing_authoritative_spans(self):
        self.provider.return_value["observation"] = self.pack["fixture_meanings"]["workshop-rule"][0]
        result = self.run_route()
        self.assertEqual(result["literal_spans"][2], self.pack["passages"][2]["text"])

    def test_valid_ids_and_self_declared_support_cannot_accept_unsupported_meaning(self):
        self.provider.return_value.update(observation="A low-risk workshop never requires a ramp.",
                                          supports=True)
        with self.assertRaisesRegex(ValueError, "unsupported meaning"):
            self.run_route()
        self.provider.assert_called_once()
        self.assertFalse(self.checkpoint.exists())

    def test_unknown_or_duplicate_response_identity_cannot_persist(self):
        for labels in (["unknown"], ["policy-v1/p2/1.2(a)(i)"] * 2):
            with self.subTest(labels=labels):
                self.provider.return_value["labels"] = labels
                with self.assertRaisesRegex(ValueError, "invalid response identities"):
                    self.run_route()
                self.assertFalse(self.checkpoint.exists())

    def test_parser_content_and_coordinate_mutations_reject_stale_reuse(self):
        original = deepcopy(self.pack)
        source_hash = fingerprint(original)
        mutations = [lambda p: p.update(parser_version="synthetic-parser-v2"),
                     lambda p: p["passages"][0].update(text="Mutated policy text"),
                     lambda p: p["passages"][0].update(page=9)]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                self.pack = deepcopy(original)
                mutate(self.pack)
                self.contract = compile_contract(self.pack)
                self.assert_preflight("stale producer", expected_source_hash=source_hash)
        self.pack = original
        self.contract = compile_contract(self.pack)
        self.run_route(expected_source_hash=source_hash)

    def test_sized_envelopes_write_reopen_without_truncation_and_preflight_overflow(self):
        self.pack["passages"][0]["text"] += "\nDense supplemental qualification." * 2000
        self.contract = compile_contract(self.pack)
        self.assert_preflight("storage limit", storage_limit=1024)
        result = self.run_route(storage_limit=200_000)
        self.assertEqual(result["literal_spans"][0], self.pack["passages"][0]["text"])
        reopened = json.loads(self.checkpoint.read_bytes())
        self.assertEqual(reopened, result)
        self.assertEqual(reopened["warnings"],
                         ["Synthetic expectations lack independent domain review."])

    def test_unchanged_saved_stage_reuses_without_another_provider_call(self):
        original = self.run_route()
        before = self.checkpoint.read_bytes()
        self.provider.reset_mock()
        self.assertEqual(self.run_route(reuse_saved=True), original)
        self.provider.assert_not_called()
        self.assertEqual(self.checkpoint.read_bytes(), before)

    def test_changed_settings_reject_reuse_without_dispatch_or_rewriting_original(self):
        self.run_route()
        before = self.checkpoint.read_bytes()
        self.provider.reset_mock()
        with self.assertRaisesRegex(PreflightError, "stale saved-stage"):
            self.run_route(reuse_saved=True, settings={"model": "different-model"})
        self.provider.assert_not_called()
        self.assertEqual(self.checkpoint.read_bytes(), before)

    def test_mutated_saved_literal_projection_is_rejected_before_dispatch(self):
        saved = self.run_route()
        saved["literal_spans"][1] = "No exception applies."
        self.checkpoint.write_bytes(encoded(saved))
        retained_failure = self.checkpoint.read_bytes()
        self.provider.reset_mock()
        with self.assertRaisesRegex(PreflightError, "saved projection differs"):
            self.run_route(reuse_saved=True)
        self.provider.assert_not_called()
        self.assertEqual(self.checkpoint.read_bytes(), retained_failure)


if __name__ == "__main__":
    unittest.main()
