# Working with Google's Cloud skills

*Our skills decide what the application needs; Google's skills operate the product.*

[Google's skills collection](https://github.com/google/skills) (`google/skills`,
Apache-2.0) holds about 170 skills for Google products and technologies:
gcloud recipes, IAM and deny policies, Cloud Run and GKE operations, Terraform
alert policies, PromQL, trace and log queries, database administration, and
the Agent Platform services (evaluation, tuning, RAG Engine, Agent Gateway).
About ten are agent-specific. None of them covers the journey this toolkit
owns: discovery, system design, contracts, the engineering of an ADK
application, its evaluation, release and presentation. Google's own ADK
lifecycle skills live in a different repository,
[Agents CLI](agents-cli.md).

The combination is therefore a division of labour, not an overlap. This
toolkit's specialist chooses the mechanism and its contracts (which identity,
which ingress, which SLI, which store). Google's product skill carries the
mechanism out (the role binding, the deploy flags, the alert policy, the
instance). Neither replaces the other, and installing both establishes no
automatic integration; the plan goals and the entry skill connect them.

## Install them together

Install all of Google's skills, or only the ones a plan names:

```bash
npx skills@latest add google/skills --skill '*' -a claude-code
npx skills@latest add google/skills --skill cloud-run-basics -a claude-code
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a claude-code
```

For Codex use `-a codex`; for Google's coding agents `-a gemini-cli`,
`-a antigravity` or `-a antigravity-cli`, in the same project scope. Restart
the coding-agent session if the new skills do not appear.

Installing everything is rarely necessary. Google's `finding-google-skills`
router fetches the published catalogue (`index.json`) and only the matching
skill when a request names a Google product, so one installed skill gives
access to the rest on demand. It does not detect what is installed; the entry
skill does that part.

## How the plan names them

The designer writes a Google product skill into a goal's supporting skills
when the goal's route needs a product provisioned, queried or administered:

```text
- **Primary skill:** deploy-adk-on-google-cloud
- **Supporting skills:** adk-tool-auth-and-secrets (runtime identity);
  google/skills:cloud-run-basics (service and ingress provisioning);
  google/skills:iam-helper-for-policy-management (the two role bindings)
```

`adk-engineer` reads that line like a missing specialist: it looks for the
skill in the host's catalogue, shows the install command or asks the router
when it is absent, continues the local work, and records the product step as
an execution-scope prerequisite until the user authorises it. Google's
command examples are proposals; provisioning, IAM changes, API enablement and
paid runs still need the user's approval for that scope.

The mapping from each specialist to the product skills it pulls in, with the
triggers, is in the engineer's
[composition reference](../../skills/adk-engineer/references/composition.md#use-googles-product-skills-for-the-mechanism)
and, by implementation route, in the designer's
[handoff reference](../../skills/adk-system-designer/references/implementation-handoff.md#name-the-google-product-skill-a-route-needs).

## Three practical requests

A goal whose product skill is installed:

```text
/adk-engineer Carry out G04 from docs/plans/warranty.md. Use
deploy-adk-on-google-cloud for the packaging, identity and readback plan and
the installed cloud-run-basics skill for the service and ingress commands.
Deploy nothing until I approve the exact command.
```

An operational question that is the product's, not the application's:

```text
/adk-engineer Our Cloud Run agent returns 403 from the orders API since the
service account change. Diagnose with adk-tool-auth-and-secrets; use the
installed iam-helper-for-troubleshooting skill for the policy check and
propose the narrowest binding, without applying it.
```

Alert policies after the SLIs are decided:

```text
/adk-engineer The observability goal G07 names our SLIs. Use
adk-agent-observability for which ADK signal each SLI reads and the installed
agent-platform-alert-configuration skill to generate the Terraform alert
policies. Keep content capture off.
```

## What stays ours

Google's skills were written for an operator at a terminal, and several open
with habits this toolkit's floor replaces: global `gcloud config set project`,
`gcloud auth login` in the middle of a task, downloaded service-account keys,
`--allow-unauthenticated` as the headline deploy, `gcloud services enable`
without approval, and a fail-open authorization callout in one gateway
template. Keep scoped `--project` and `--region` flags, platform identity,
private by default and approval per scope. Their
`CLOUDSDK_METRICS_REQUEST_ATTRIBUTION` prefix is optional attribution.

Where a Google skill carried a fact that changes an ADK decision (the Agent
Identity mechanism for Agent Runtime, the Cloud Monitoring names of ADK
metrics, the Agent Gateway egress policy on MCP tool names, the managed
scorer's judge-pinning contract, BigQuery's cost controls), the relevant
specialist now records it with its source and date. The
[comparison note](../research/google-skills-comparison-2026-10-21.md)
lists what was imported, what is routed and what was deliberately left out.
