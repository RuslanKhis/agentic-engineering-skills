# Finite ADK answer adapter

`stream_adapter.collect_answer` consumes one finite asynchronous stream of decoded
ADK event dictionaries. Supply the trusted `invocation_id`, `answer_author`, and an
async `on_preview(snapshot)` callback. Python 3.11+ and only the standard library
are required.

Eligible partials are text deltas from the designated author with content role
`model`. The callback is awaited for each reconstructed snapshot, including empty
or whitespace deltas. Thought text and all narration in tool-bearing events are
excluded. Only one nonblank, nonpartial `STOP` answer can complete the invocation.
Its text replaces the preview; it is never appended or sent as a partial callback.

The answer returns only after clean exhaustion and successful iterator closure.
Reported errors, interruption, invocation mismatch, unsupported finish reasons,
missing completion, and additional eligible text after completion reject the
answer. Snake/camel metadata aliases are supported; conflicting aliases reject.
Protocol rejections remain failures while the rest of the finite stream is drained;
transport or callback exceptions stop consumption and trigger closure.

Commit only the returned string. On `AnswerRejected` or cancellation, mark any
preview incomplete. Errors use fixed messages without raw exception chains.
Caller cancellation remains `asyncio.CancelledError`. The obtained iterator's
`aclose()` is awaited when available, including after exhaustion and cancellation;
cleanup is shielded from repeated cancellation and joined before the call exits.
The producer, callback, and cleanup must cooperate asynchronously. The application
owns deadlines, transport decoding, raw-byte admission, and authentication.
Tool envelopes remain opaque: this adapter does not validate business outcomes.
This is a finite text profile, not a multimodal or multiple-answer protocol.

Run the offline tests from this directory:

```sh
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

Tests exercise the actual public adapter using synthetic events and controlled
async barriers, including early previews, late failures, and cancellation during
input, callbacks, and cleanup. They require no ADK installation or external calls
and make no live SDK, browser, deployment, or measured performance claim.

Validation and lifecycle patterns are adapted directly into `stream_adapter.py`
from the installed `optimise-adk-on-google-cloud/assets/finite_answer_stream.py`
skill asset. Its optional budgets, deadlines, and snapshot-input mode are omitted
for this contract. The MIT notice is retained in `LICENSE.finite-answer-stream`.
