from pathlib import Path
import tempfile
import unittest

from pipeline.blobs import PrivateBlobStore
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

    def test_oversized_meta_goes_to_blobs_and_reopens_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            blobs = PrivateBlobStore(Path(tmp) / "blobs")
            store = CheckpointStore(Path(tmp) / "runs", limit_bytes=2000, blobs=blobs)
            frame = "source text " * 500
            payload = {"decision": "refuse"}
            path = store.save("r1", "writer", payload, {"frame": frame, "attempt": "a1"}, owner="team-east")
            self.assertLessEqual(path.stat().st_size, 2000)
            record = store.reopen("r1", "writer", "team-east")
            self.assertEqual(record["meta"], {"frame": frame, "attempt": "a1"})
            self.assertEqual(record["payload"], payload)
            self.assertFalse((Path(tmp) / "runs" / "r1" / "writer.rejected.json").exists())

    def test_still_too_large_after_offload_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CheckpointStore(Path(tmp) / "runs", limit_bytes=500,
                                    blobs=PrivateBlobStore(Path(tmp) / "blobs"))
            with self.assertRaises(StoreLimitExceeded):
                store.save("r1", "writer", {"x": "y" * 1000}, {"frame": "z" * 1000}, owner="team-east")
            self.assertTrue((Path(tmp) / "runs" / "r1" / "writer.rejected.json").exists())


if __name__ == "__main__":
    unittest.main()
