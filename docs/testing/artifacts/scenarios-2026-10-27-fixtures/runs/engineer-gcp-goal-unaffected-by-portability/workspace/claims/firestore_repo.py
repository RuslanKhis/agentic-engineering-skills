from __future__ import annotations


class FirestoreClaims:
    def __init__(self, client):
        self.col = client.collection("claims")

    def get(self, claim_id):
        snap = self.col.document(claim_id).get()
        return snap.to_dict() if snap.exists else None

    def add_note(self, claim_id, note):
        from google.cloud import firestore

        self.col.document(claim_id).update({"notes": firestore.ArrayUnion([note])})


class FirestoreMemorySettings:
    """Account setting `memory_declined` on `policyholders/{id}`; a missing document or field means not declined."""

    def __init__(self, client):
        self.col = client.collection("policyholders")

    def memory_declined(self, user_id):
        snap = self.col.document(user_id).get()
        return bool(snap.exists and snap.to_dict().get("memory_declined", False))
