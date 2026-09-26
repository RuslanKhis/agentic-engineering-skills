"""Synthetic transport counterexample, not evidence of a provider restriction."""

import dataclasses
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ASSET = Path(__file__).resolve().parents[1] / "assets/provider_schema_probe.py"
SPEC = importlib.util.spec_from_file_location("provider_schema_probe", ASSET)
probe = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = probe
SPEC.loader.exec_module(probe)


def serialized_request(values):
    # Illustrative envelope only: real applications capture their SDK's wire bytes.
    return json.dumps({"output_limit": 256, "response_schema": {
        "type": "object", "properties": {"selection": {
            "type": "string", "enum": values}}}}, ensure_ascii=False).encode()


def has_multiline_enum(node):
    if isinstance(node, dict):
        values = node.get("enum", [])
        return (any(isinstance(v, str) and "\n" in v for v in values)
                or any(has_multiline_enum(v) for v in node.values()))
    if isinstance(node, list):
        return any(has_multiline_enum(v) for v in node)
    return False


def rejecting_transport(route, wire):
    accepted = not has_multiline_enum(json.loads(wire))
    return probe.Observation(route, probe.request_hash(wire), "controlled_transport", accepted)


class ProviderSchemaProbeTests(unittest.TestCase):
    def setUp(self):
        self.route = probe.Route("synthetic", "https://example.invalid/review", "model-a", "adapter-1", "strict")
        self.literal = serialized_request(["Access width?\n3 metres"])
        self.selection = serialized_request(["span-01"])

    def gate(self, requests, observations, boundary="controlled_transport"):
        return probe.require_compatible(self.route, requests, observations, boundary=boundary)

    def test_actual_multiline_schema_blocks_gate(self):
        with self.assertRaises(ValueError):
            self.gate([self.literal], [rejecting_transport(self.route, self.literal)])

    def test_id_shape_passes_only_its_own_request(self):
        observation = rejecting_transport(self.route, self.selection)
        self.gate([self.selection], [observation])
        with self.assertRaises(ValueError):
            self.gate([self.literal], [observation])

    def test_success_on_another_route_or_boundary_is_not_substituted(self):
        observation = rejecting_transport(self.route, self.selection)
        other = dataclasses.replace(self.route, model="model-b")
        with self.assertRaises(ValueError):
            self.gate([self.selection], [dataclasses.replace(observation, route=other)])
        with self.assertRaises(ValueError):
            self.gate([self.selection], [observation], boundary="live_provider")

    def test_all_shapes_need_evidence(self):
        observation = rejecting_transport(self.route, self.selection)
        for requests, observations in (([], []), ([self.selection], []),
                                        ([self.selection, self.literal], [observation]),
                                        ([self.selection, self.literal], [observation, observation])):
            with self.subTest(requests=requests), self.assertRaises(ValueError):
                self.gate(requests, observations)

    def test_response_uncertainty_is_not_success(self):
        observation = rejecting_transport(self.route, self.selection)
        with self.assertRaises(ValueError):
            self.gate([self.selection], [dataclasses.replace(observation, accepted=None)])


if __name__ == "__main__":
    unittest.main()
