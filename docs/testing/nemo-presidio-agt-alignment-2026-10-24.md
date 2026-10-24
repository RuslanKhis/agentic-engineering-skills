# NeMo Guardrails, Presidio and governance toolkit alignment — 24 October 2026

Source note: [comparison](../research/nemo-presidio-agt-comparison-2026-10-24.md).

## Changed journeys

`protect-adk-sensitive-data`, an offline leak check in CI; and
`adk-agent-security`, whether a shared policy plugin can replace an
agent's tool gate. One fresh-agent trial each, run on 25 October 2026.

## Trial 1: offline leak oracle

A fresh agent with only the skill packages added an offline check to a
synthetic ADK 2.12 support agent's scripted-model tests that fails the
build on any leak into model requests, session events, tool calls or logs.
It installed google-adk 2.12.0, presidio-analyzer 2.2.364 and pytest, then
ran everything with outbound sockets and DNS blocked.

Result: a pytest plugin that records the four sinks and, at teardown, runs
exact canaries and then Presidio (no-op engine, built-in pattern
recognisers, six credential recognisers), reporting location and entity
type, never the value. **5 passed**; a deliberate-leak suite produced **5
errors** (an unprotected email, an invented phone number, a key in a tool
argument, a canary only in a log, an unregistered email), each for the
right reason. It declined real SDP calls and a spaCy model, and said the
guard does not replace the SDP tests. Ease 3 of 5.

Frictions and fixes:

1. The documented offline construction still reached the network: the
   email recogniser's `tldextract` fetches the Public Suffix List on first
   match (confirmed in the installed tldextract 5.4.0). Fixed: set
   `TLDEXTRACT_PUBLIC_SUFFIX_LIST_URLS` empty before import.
2. Canaries under `.test`, `.invalid` or `.internal` are invisible to
   Presidio. Fixed.
3. No way given to capture the sinks; wrapping both session-service classes
   double-counts. Fixed.
4. pytest's captured-log section printed the leaked value. Fixed:
   `--show-capture=no`.
5. No construction code. Fixed: the registry and loader calls.
6. The no-op engine still installs and imports spaCy. Fixed.
7. Scores and thresholds (phone numbers at 0.4 without context; some valid
   formats rejected). Fixed.
8. "Do not install dependencies" against "pin presidio-analyzer", and no
   pattern for proving it bites. Fixed: a test dependency with the
   project's agreement; one deliberate leak per sink.
9. The compatibility baseline is 2.8.0, and `InMemoryRunner(plugins=)` is
   deprecated on 2.12.0. The deprecation is fixed in the evaluation skill's
   signatures; the baseline is unchanged because it records the last full
   verification.

## Trial 2: community governance plugin

A fresh agent asked whether `AgentGovernancePlugin` (google-adk-community
0.5.0) can replace a finance agent's gate (`read_invoice`, `pay_invoice`
needing approval above 1,000, `email_vendor`). It installed google-adk
2.12.0, google-adk-community 0.5.0 and pytest, but not `agentmesh-platform`,
so the plugin tests used a stand-in engine and no real policy was
evaluated.

Result: the skill's answer held (no, an extra layer only). It built the
agent's own gate, a strict-bool confirmation on the stored amount, body
re-checks and a deny-default plugin set-up. **19 passed**; with the gate
removed 1 failed (the injected-memo email). The plugin tests showed:
building it without the engine raises; with `fail_open=True` it stops
nothing; its denial skips the agent's gate and the tool; an approval rule
comes back as a denial; the approved payment is denied again on resume;
an understated amount passes its amount rule; an engine error ends the run.
Ease 4 of 5.

Frictions and fixes:

1. The separate engine and `fail_open` were not mentioned. Fixed.
2. No rule syntax. Fixed by saying the syntax is the engine's and was not
   evaluated here.
3. An amount or approval rule denies the approved call on resume. Fixed:
   keep thresholds and approvals out of its policy.
4. The inspector missed `email_vendor` as egress, so the trifecta looked
   resolved. Fixed: a tool named for its channel counts as egress.
5. The inspector did not check the plugin's settings. Fixed:
   `governance_plugin_settings`.
6. Its denial shape differs from the gate's. Fixed.
7. Engine exceptions end the run. Fixed.
8. Its audit log records full arguments. Fixed, as a data sink.
9. `InMemoryRunner(plugins=)` deprecation. Fixed (as above).
10. The 2.8.0 frontmatter. Not changed (as above).

Every claim in both trials' fixes was checked in the installed packages
before editing.

## Limits

No spaCy model, cloud API or live model ran; the governance engine was not
installed and no YAML policy was evaluated.
