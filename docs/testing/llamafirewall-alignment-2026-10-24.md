# LlamaFirewall alignment — 24 October 2026

Source note: [comparison](../research/llamafirewall-comparison-2026-10-24.md).

## Changed journey

`adk-agent-security`, screening tool results locally when they may not
leave the project; `protect-adk-sensitive-data`, an alignment check as a
data boundary.

## Fresh-agent trial

A first trial was stopped part-way when work was paused and was discarded;
the trial below was run again from scratch on 25 October 2026 in a new
directory. A fresh agent with only the skill packages added, offline,
LlamaFirewall screening and an alignment check to a synthetic ADK 2.12 agent
(`fetch_url`, `read_contract`, `send_email`) whose documents may not leave
the project. It installed google-adk 2.12.0 and llamafirewall 1.0.3 without
its dependencies, for reading the API only; no weights were downloaded and
no remote model was called.

Result: a tool-result screen in `after_tool_callback` that calls the scanner
directly over overlapping windows and withholds on a block, a human-review
hold, an error, an exception or an oversized result; a `before_tool_callback`
on `send_email` with an application-owned recipient allowlist and a taint
check on values from allowed results; https-only `fetch_url`; and its own
alignment hook, off by default, that sends a judge only the user's goal and
the proposed call. It declined the stock AlignmentCheck (it would send the
contract text off the project) and chose no approver for `send_email`.

`pytest`: **23 passed, 0 failed**, with outbound network blocked. Scripted-
model Runner tests ran with screening on and off: the injected page never
reached the model or the stored session, and the attacker email was refused
either way. Three deliberate breaks (no windowing, no gate, unknown as
allow) failed 2, 3 and 4 tests. The security inventory's
`write_tool_without_gate` finding cleared.

Ease: 3 of 5.

## Frictions and fixes (same day)

Each claim was checked in the LlamaFirewall source before the fix.

1. "Call `scan_async()` or the scanner directly" was wrong: `scan_async()`
   returns a successful `ALLOW` for an `ERROR`. Fixed: call one
   `PromptGuardScanner` directly.
2. "Load the classifier once" is impossible through `LlamaFirewall`, which
   builds a scanner, and loads the model, on every scan. Fixed.
3. No window guidance. Fixed: count with the classifier's tokenizer, stay
   under 512 tokens, overlap, and test across a boundary; the sizes stay the
   project's choice.
4. No weights path. Fixed: `$HF_HOME/meta-llama--Llama-Prompt-Guard-2-86M`,
   the process-wide `HF_HOME` default and the download-and-login fallback.
5. The scanner blocks the event loop and its block reason embeds the text.
   Fixed: `asyncio.to_thread`; log decision and score only.
6. "No constructor option to change the model or endpoint" held only for
   `AlignmentCheckScanner`. Fixed: the base class's options, which change the
   destination and not the payload; a judge error is reported as a
   successful human-review result, and a trace with no user message as
   `ALLOW` with `ERROR`.
7. Neither `SKILL.md` led to the guidance. Fixed: a pointer in each.
8. The security inspector missed `read_contract` as private and counted
   `urllib.parse.urlsplit` as network egress. Fixed, with a test.
9. The scripted `BaseLlm` lives in `adk-agent-evaluation`. Not changed: the
   security reference already links its deterministic-tests page.
10. No fake scanner interface. Fixed: the interface and the cases a fake
    returns.

## Limits

No Prompt Guard weights ran, so detection quality and latency were not
measured; no judge was called.
