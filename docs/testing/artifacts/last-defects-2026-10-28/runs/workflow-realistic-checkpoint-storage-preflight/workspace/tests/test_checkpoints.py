from pathlib import Path
import tempfile
import unittest

from pipeline.blobs import BlobForbidden, PrivateBlobStore
from pipeline.checkpoints import CheckpointStore, StoreLimitExceeded


class CheckpointTests(unittest.TestCase):
    def test_small_record_round_trips(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CheckpointStore(tmp)
            store.save("r1", "writer", {"decision": "approve"}, {"warnings": []})
            self.assertEqual(store.load("r1", "writer")["payload"], {"decision": "approve"})

    def test_blob_reference_reopens_for_its_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            blobs = PrivateBlobStore(Path(tmp) / "blobs")
            store = CheckpointStore(Path(tmp) / "runs", blobs=blobs)
            ref = blobs.put("team-east", b'{"frame": "sources"}')
            store.save("r1", "writer", {"decision": "approve"}, {"frame": {"$blob": ref}})
            record = store.reopen("r1", "writer", "team-east")
            self.assertEqual(record["meta"]["frame"], {"frame": "sources"})

    def test_oversize_record_spills_to_blobs_without_losing_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            blobs = PrivateBlobStore(Path(tmp) / "blobs")
            store = CheckpointStore(Path(tmp) / "runs", limit_bytes=5_000, blobs=blobs, owner="team-east")
            payload = {"decision": "refuse", "citations": [{"span_id": f"S{i}", "quote": "q" * 50} for i in range(200)]}
            meta = {"frame": "f" * 20_000, "raw_response": "r" * 20_000, "attempt": "a1"}
            path = store.save("r1", "writer", payload, meta)
            self.assertLessEqual(path.stat().st_size, 5_000)
            self.assertEqual(store.load("r1", "writer")["meta"]["attempt"], "a1")
            record = store.reopen("r1", "writer", "team-east")
            self.assertEqual(record["payload"], payload)
            self.assertEqual(record["meta"], meta)
            self.assertFalse((Path(tmp) / "runs" / "r1" / "writer.rejected.json").exists())
            with self.assertRaises(BlobForbidden):
                store.reopen("r1", "writer", "team-west")

    def test_oversize_record_without_blob_store_is_still_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CheckpointStore(Path(tmp), limit_bytes=200)
            with self.assertRaises(StoreLimitExceeded):
                store.save("r1", "writer", {"text": "x" * 500}, {})
            self.assertTrue((Path(tmp) / "r1" / "writer.rejected.json").exists())


if __name__ == "__main__":
    unittest.main()
