---
name: deploy-adk-on-google-cloud
description: Select, implement, adapt or audit deployment of Python Google ADK agents on Cloud Run, Agent Runtime or GKE, including identity, packaging, browser validation, recovery and owned-resource cleanup. Use for ADK hosting decisions and deployment lifecycle work. Do not activate for general Kubernetes administration, non-ADK applications, prompt-only changes, or RAG and memory design without a deployment task.
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "3"
  last-tested: "2026-09-15"
---

# Deploy ADK on Google Cloud

Produce a deployment design, focused implementation or evidence-based audit that fits the existing project. Keep Cloud Run, Agent Runtime and GKE as modes of this one skill. The outcome includes an explicit resource and identity plan, meaningful verification and a separate cleanup procedure.

## Inspect before choosing

1. Read the project's instructions, dependency declarations and lockfiles, configuration templates, deployment definitions and tests. Establish the requested outcome: recommend, implement, review, deploy, recover or clean up. Preserve existing customisations and package management.
2. Run `python /path/to/skill/scripts/inspect_project.py --root /path/to/project --dry-run` using an available Python 3.11+ interpreter. Substitute the actual paths. This is a bounded, offline inventory; it neither loads `.env` values nor executes project code or cloud commands. Inspect files outside its reported coverage manually. Read [compatibility.md](references/compatibility.md) when assessing versions, interpreting its output or changing an SDK integration.
3. Check the selected environment's Python and installed distribution versions as well as declared pins. Use package metadata without importing agent code. Record conflicts and uncertain compatibility. Preserve the target's versions; a different version requires contract validation, not an automatic upgrade or downgrade.
4. Locate the existing agent export, server factory, model/backend selection, tool effects, session/artefact services, user-authentication boundary and build context. Record configuration **keys and provenance**, keeping secret values out of reports. A root `.env` does not replace nested configuration. Treat hosting, inference, session storage and build locations separately.
5. Establish the operator, build, runtime and caller identities; on GKE add node and Kubernetes service-account identities. CLI login, ADC, ADC quota project and deployed workload identity are distinct. Discover project/billing/API access with explicitly scoped reads; denied access is unknown state, not proof of absence.

Inspection is complete when the current architecture, constraints, version status, missing prerequisites and intended scope are recorded. Missing credentials do not block local implementation or a reviewable plan.

## Choose the mode

| Workload requirement | Mode and reference |
| --- | --- |
| Managed HTTP service, custom web/API integration or control of the container | [Cloud Run](references/cloud-run.md). Choose native ADK deployment for an uncustomised server, or a custom container for an existing server and runtime requirements. |
| ADK package fits managed agent hosting and platform sessions | [Agent Runtime](references/agent-runtime.md). Legacy CLI/API identifiers still include `agent_engine` and `reasoningEngines`. |
| Existing Kubernetes platform or requirements needing Kubernetes controls | [GKE](references/gke.md). Prefer adapting the existing workload; a fresh cluster is an explicit infrastructure decision. |
| Request asks which platform to choose | Compare only the relevant modes against HTTP integration, existing operations, state, identity, network and lifecycle needs. Deliver a recommendation without provisioning. |

These choices are not a maturity ladder. Keep the user's selected platform unless evidence shows a blocking requirement. Load only the selected mode's reference; read another when comparing alternatives.

## Implement or adapt

1. Present a short plan with the affected files, retained interfaces and validation steps. Read [lifecycle.md](references/lifecycle.md) before preparing provisioning, recovery or deletion. The plan must separate local code changes, cloud reads, mutations and paid tests.
2. Make the smallest coherent change. Reuse the existing agent and tools; do not replace the application with a support-ticket demonstration. Preserve package manager, locks, test framework, ports and naming conventions where compatible.
3. Prepare an allowlisted source package, explicit model/backend configuration, workload identity, authenticated access and selected state services. Review generated native-ADK files as well as authored files. Bind the application to the container's configured port and provide cheap health checks that do not call a model.
4. Prepare a data-only ownership journal or extend the existing lifecycle system: exact target, source fingerprint, original resource identities and IAM baseline, submitted operation IDs and created identities. On repeats, reconcile state before submitting more work. Use the lifecycle reference for uncertain outcomes and concurrency.
5. Complete the implementation and offline checks before asking for approval of a concrete cloud action. Production changes such as external state, user authorisation, IAP, distributed locking and release promotion need their own implementation and tests; historical lab success does not validate them.

## Permission boundary

Repository and cloud inspection are read-only by default. Code-generation permission does not authorise deployment. Before enabling APIs, changing IAM, creating secrets or resources, migrating data, deploying, deleting, or running paid tests, present the **exact project, region, resource names, identities, commands, limits and cleanup scope**, then obtain explicit approval. Existing approval applies only while that exact scope remains valid. Confirm cleanup separately. Never infer approval from elapsed time, a budget balance or a previous campaign.

Use ADC or workload identity, with Secret Manager for application secrets where needed. Keep credentials and customer data out of source, logs, examples and reports. Configuration examples contain placeholders only. Derive the narrow required permissions; Owner, Editor, public unauthenticated access and wildcard grants are not troubleshooting shortcuts.

Bound retries, polling, request counts and wall-clock time. Reserve capacity for cleanup and independent inspection. Stop optional tests before consuming that reserve; a safe refusal can itself consume requests. Cleanup may delete only resources demonstrably created by the current workflow. Preserve pre-existing resources and grants.

## Validate and report

Read [validation.md](references/validation.md) for the relevant acceptance checks, evidence levels and retry cases. Always run applicable local tests first. Check real tool output and final grounded text, not just HTTP status. Verify session recall explicitly; health does not prove model access or persistence.

For live work, use an approved isolated target and synthetic data. Record the submitted model/build/control work, deployed identity and cleanup result. An accepted timeout requires reconciliation; automatic replay can repeat tool effects. Completed deletion must be safe to repeat and independently checked within the caller's visibility.

Finish with files changed, commands actually executed, test results labelled **local**, **mocked**, **live** or **not run**, exact versions, manual steps and remaining uncertainty. Name retained resources and retention/visibility limits. Do not claim production readiness, cross-user authorisation, absence of all future charges, or coding-agent compatibility beyond the evidence.

For provenance and the distinction between verified behaviour and recommendations, read [evidence.md](references/evidence.md). For this package's validation and forward tests, see [skill-validation.md](references/skill-validation.md).

Independent community project; not affiliated with or endorsed by Google.
