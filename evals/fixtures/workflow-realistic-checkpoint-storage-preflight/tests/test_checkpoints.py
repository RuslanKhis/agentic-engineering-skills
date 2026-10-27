from pathlib import Path
import tempfile
import unittest

from pipeline.blobs import PrivateBlobStore
from pipeline.checkpoints import CheckpointStore


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


if __name__ == "__main__":
    unittest.main()
