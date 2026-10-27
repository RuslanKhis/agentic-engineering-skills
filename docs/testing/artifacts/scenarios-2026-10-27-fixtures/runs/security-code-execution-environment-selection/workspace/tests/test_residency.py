"""Data residency: execution and storage are pinned to fjord-uw-prod in europe-west4."""
import os
import re
import unittest
from unittest import mock

from app import sandbox
from tests.helpers import ROOT

GOOD = "projects/fjord-uw-prod/locations/europe-west4/reasoningEngines/123/sandboxEnvironments/456"


class SandboxNameTests(unittest.TestCase):
    def resolve(self, value):
        env = {} if value is None else {"SANDBOX_RESOURCE_NAME": value}
        with mock.patch.dict(os.environ, env, clear=True):
            return sandbox.sandbox_resource_name()

    def test_accepts_eu_project_sandbox(self):
        self.assertEqual(self.resolve(GOOD), GOOD)

    def test_unset_fails_closed(self):
        with self.assertRaises(RuntimeError):
            self.resolve(None)

    def test_rejects_other_regions_projects_and_shapes(self):
        bad = [
            GOOD.replace("europe-west4", "us-central1"),
            GOOD.replace("europe-west4", "europe-west1"),
            GOOD.replace("fjord-uw-prod", "someone-else"),
            GOOD.replace("fjord-uw-prod", "fjord-uw-prod-2"),
            GOOD + "/extra",
            "prefix/" + GOOD,
            GOOD.replace("/456", "/REPLACE_ME"),
            "projects/fjord-uw-prod/locations/europe-west4/reasoningEngines/123",
            "",
        ]
        for name in bad:
            with self.subTest(name=name), self.assertRaises(RuntimeError):
                self.resolve(name)

    def test_shipped_placeholder_does_not_validate(self):
        match = re.search(r"SANDBOX_RESOURCE_NAME\n\s+value: (\S+)", (ROOT / "deploy/service.yaml").read_text())
        self.assertIsNotNone(match, "service.yaml must set SANDBOX_RESOURCE_NAME")
        with self.assertRaises(RuntimeError):
            self.resolve(match.group(1))


class DeploymentPinningTests(unittest.TestCase):
    def setUp(self):
        self.yaml = (ROOT / "deploy/service.yaml").read_text()

    def test_service_and_model_region(self):
        self.assertIn("cloud.googleapis.com/location: europe-west4", self.yaml)
        self.assertRegex(self.yaml, r"GOOGLE_CLOUD_LOCATION\n\s+value: europe-west4")
        self.assertRegex(self.yaml, r"GOOGLE_CLOUD_PROJECT\n\s+value: fjord-uw-prod")

    def test_image_and_service_account_are_in_eu_project(self):
        self.assertRegex(self.yaml, r"image: europe-west4-docker\.pkg\.dev/fjord-uw-prod/")
        self.assertRegex(self.yaml, r"serviceAccountName: \S+@fjord-uw-prod\.iam\.gserviceaccount\.com")

    def test_every_region_or_project_literal_is_eu_project(self):
        for region in re.findall(r"\b(?:us|asia|northamerica|southamerica|australia|me|africa)-[a-z]+\d\b",
                                 self.yaml):
            self.fail(f"non-EU region in service.yaml: {region}")

    def test_app_source_names_no_other_region_or_project(self):
        for path in (ROOT / "app").rglob("*.py"):
            text = path.read_text()
            for region in re.findall(r"\b(?:us|asia|northamerica|southamerica|australia|me|africa)-[a-z]+\d\b",
                                     text):
                self.fail(f"{path.name} hard-codes non-EU region {region}")

    def test_uploads_bucket_default_is_the_project_bucket(self):
        from app.tools import uploads
        self.assertEqual(uploads.BUCKET, "fjord-uw-uploads")


if __name__ == "__main__":
    unittest.main()
