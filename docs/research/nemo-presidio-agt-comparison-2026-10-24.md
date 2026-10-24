# NeMo Guardrails, Presidio and the agent governance toolkit compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of [NVIDIA/NeMo-Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) at commit `189b85f`,
[microsoft/presidio](https://github.com/microsoft/presidio) at commit
`4f0e236` (2026-10-19; MIT; PyPI 2.2.364),
[microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit)
at commit `70a4ab8` (release 4.1.0 of 2026-06-09; MIT; public preview) and the community
`AgentGovernancePlugin` in [google/adk-python-community](https://github.com/google/adk-python-community)
at `396da17` (PyPI google-adk-community 0.5.0), cloned on 24 October 2026
into their own directories and read, never run.

**Maintenance.** All active; the governance toolkit's last release is four
months old and in preview.

**Conclusion.** Of the memo's three items, one is useful and one needed a
warning. Presidio works as an offline test oracle for leaked PII, but it is
not offline by default: its spaCy engine downloads a model at run time, so
the harness must construct it with the no-op engine or a pinned wheel, and
credentials need custom recognisers. The community governance plugin is
real but weaker than the gate our security skill requires: it sees only the
tool name and arguments, skips unparsable policies unless strict, and its
sample policy allows by default. NeMo's YARA rules are too crude to adopt.

## Method

The download call, the plugin's decision path, `strict` default and sample
policy were confirmed in source before editing. One scenario case covers
the Presidio journey; the fresh-agent trials, one per changed journey, are
in the [testing record](../testing/nemo-presidio-agt-alignment-2026-10-24.md).

## Drift corrected

None; the skills did not mention these tools.

## Imported, by specialist

- **protect-adk-sensitive-data.** Presidio as an offline leak oracle with
  its offline construction, credential recognisers and its limits. After
  the trial: the Public Suffix List fetch its email recogniser makes and
  how to disable it, reserved canary domains it cannot see, scores and
  thresholds, how to capture each sink, and keeping the report from
  printing the value.
- **adk-agent-security.** What the community governance plugin can and
  cannot express, the settings to use if a team adds it, and the governance
  toolkit's `adk-agentmesh` callbacks not matching ADK's call signature on
  reading. After the trial: its separate engine and `fail_open`, why an
  approval or amount rule denies an approved call on resume, its denial
  shape, uncaught engine errors and the audit log of full arguments; a
  `SKILL.md` pointer; and two inspector rules (`governance_plugin_settings`,
  channel-named senders as egress).
- **adk-agent-evaluation.** `InMemoryRunner(plugins=)` is deprecated on
  2.12.0 in favour of `App`.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- NeMo's YARA rails (crude patterns; output only; the NeMo runtime).
- Presidio's anonymiser, image redactor and remote-model recognisers
  (compete with Sensitive Data Protection or call out).
- The governance toolkit's wider identity and mesh stack, `adk-agentmesh`,
  and the plugin's fail-open option and allow-by-default sample.

## Limits

Nothing was run; the `adk-agentmesh` signature mismatch is from reading.
