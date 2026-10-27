import tempfile
import unittest

from review_app.storage import EnvelopeError, EnvelopeStore


class StorageTests(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EnvelopeStore(tmp)
            envelope = {"run_id": "t1", "stage": "group", "producer": {"grouper": "x"}, "inputs": [],
                        "payload": {"units": [{"key": "DMP:4.1", "text": "4.1 Respect the street."}]}}
            envelope_id = store.put(envelope)
            self.assertEqual(store.get(envelope_id), envelope)

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EnvelopeStore(tmp)
            envelope = {"run_id": "t1", "stage": "group", "producer": {}, "inputs": [], "payload": {}}
            store.put(envelope)
            with self.assertRaises(EnvelopeError):
                store.put(envelope)


if __name__ == "__main__":
    unittest.main()
