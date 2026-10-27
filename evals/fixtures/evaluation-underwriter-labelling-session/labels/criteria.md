# Labelling criteria

Each case gets pass or fail on three criteria. A critique sentence is required for every fail.

## fraud_flags_correct
- v01 (2026-10-13): pass when every fraud indicator present in the claim is flagged.
- v02 (2026-10-16): pass when every indicator is flagged **and** no indicator is flagged that the
  claim does not support (false flags now fail).

## fast_track_correct
- v01 (2026-10-13): pass when the fast-track decision matches the underwriting guide.

## note_grounded
- v01 (2026-10-13): pass when every statement in the triage note is supported by a claim field.
