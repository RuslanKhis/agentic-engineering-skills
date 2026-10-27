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
