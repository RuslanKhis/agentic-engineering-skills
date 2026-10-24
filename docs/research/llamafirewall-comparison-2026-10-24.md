# LlamaFirewall compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of `LlamaFirewall/` in [meta-llama/PurpleLlama](https://github.com/meta-llama/PurpleLlama)
at commit `d934ea2` (2026-10-12), cloned on 24 October 2026 into its own
directory and read, never run, with the Prompt Guard 2 model cards on
Hugging Face.

**Licence.** The scanner code is MIT. The repository root is under the Llama
3.2 Community License, and the Prompt Guard 2 weights are gated under the
Llama 4 Community License. The skills link to the weights and ship none, and
say that using them is a project's own licence decision.

**Maintenance.** The repository is active; the PyPI package (1.0.3,
2025-05-29) is old, so pin with care.

**Conclusion.** The memo's "local tool-result screening; AlignmentCheck" is
half right. Prompt Guard 2 can screen tool results in process, but only the
first 512 tokens unless results are chunked, its composite flattens scanner
errors into a successful allow, and its synchronous `scan()` fails inside
ADK's event loop. AlignmentCheck is not local at all: it sends the user's
message and the whole trace to a third-party endpoint under a static key
with a hard-coded temperature. The security skill now carries the local
option with those conditions, and the sensitive-data skill treats an
alignment check as a data boundary.

## Method

The truncation, `asyncio.run`, the default Together AI endpoint and key
variable, the temperature, the "when in doubt" prompt and the decision type
were confirmed in the source before editing; the trial's further claims
(`scan_async()`, per-scan construction, the weights path, the blocking
model call, the block reason, the base class's options and the judge's
error result) were confirmed in the same source before the fixes. One scenario case covers the
journey; the fresh-agent trial is in the
[testing record](../testing/llamafirewall-alignment-2026-10-24.md).

## Drift corrected

None; the skills did not mention LlamaFirewall.

## Imported, by specialist

- **adk-agent-security.** In "Screening is a layer": Prompt Guard 2 from
  `after_tool_callback`, called directly rather than through `LlamaFirewall`
  (whose `scan_async()` reports every error as a successful allow and whose
  composite reloads the model on each scan), through `asyncio.to_thread`,
  with tokenizer-counted overlapping windows, unknown-to-withhold mapping,
  no logging of the block reason (it embeds the text), startup loading from
  `$HF_HOME/meta-llama--Llama-Prompt-Guard-2-86M`, a fake with the scanner's
  interface for tests, the weights' licence and what it does not cover; a
  pointer from `SKILL.md`. `inspect_security_surface.py` no longer counts
  `urllib.parse` calls as network egress and reads "contract" as private.
- **protect-adk-sensitive-data.** In public tool results: AlignmentCheck as
  a third-party sink needing approval, not a gate; its base class can point
  at an in-project endpoint without changing what is sent; a judge error is
  reported as a successful human-review result; a pointer from `SKILL.md`.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- AlignmentCheck as shipped, PIICheck, the regex scanner's defaults, the
  framework demos, the interactive configuration and login flows, and the
  hidden-ASCII scanner (the skill's encoding policy already covers it).
- The weights themselves: licence decision for each project.

## Limits

Nothing was run; latency and detection quality were not measured.
