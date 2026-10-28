# Engineering articles: reading plan

28 October 2026. Part one of [the engineering-articles programme](../testing/engineering-articles-integration-prompt.md):
a ranked plan of practical articles by engineers and researchers at Google,
Anthropic and OpenAI, with what each would change in this toolkit. Nothing in
the skills has changed yet. Part two starts only after the plan is approved.

## How the plan was made

- **Phase 0.** Read the README, CONTRIBUTING, the quality-practices note,
  every skill's frontmatter and headings, and the source register. Listed the
  59 article links the toolkit already cites. Checked the worked example
  against the files. It holds, with one refinement:
  `adk-agent-evaluation/references/evaluation-design.md:9` already reports
  missed escalation and over-escalation as separate rates, so the seed
  article's "escalation as a relief valve" point is partly covered.
- **Phase 1.** Ten read-only scouts each searched one lane and quoted the
  skill text behind every claimed gap. They read about 150 candidates and
  kept 79 across lanes before merging.
- **Phase 2.** Merged duplicates: eleven articles were found by two or three
  lanes. Re-opened the files to confirm the main gaps.
  - **Gaps confirmed absent from skills/:** "standard error", "confidence
    interval" and "power analysis"; "ablation", "soak" and "per-model";
    programmatic tool calling; "inverse scaling"; a clarifying-question UI
    state; procedural memory.
  - **Text confirmed present:** the masking rule at
    `optimise-adk-on-google-cloud/references/context-window.md:136`; the
    content-replacing `guard_decision` at
    `adk-model-and-output-contracts/references/validation-and-repair.md:51-66`;
    the approve/reject-only transitions at
    `adk-operational-guardrails/references/human-review.md:40-47`.
  - **Ordering:** by how much each article would change what a coding agent
    does on a real project. Where two articles touch the same file, the
    stronger comes first and the second says what it builds on.

**Reading the table.**

- **Size:** S is a paragraph; M is a section or a reference change; L is a
  new reference or a changed workflow.
- **Access:** "readable" means a scout read the article in full. "needs paste"
  means you need to paste it. "mirror" means it was read from an unofficial
  copy; confirm the official copy, or paste it, before it is cited.
- **Tiers:** a suggestion for where to cut. The plan is long because the
  scouts were thorough. Tier 1 alone is about 25 sequential article runs.

## The plan

### Tier 1: broad changes to everyday work

| # | Article | Org | Date | Skills and files it changes | Expected benefit | Size | Access |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Omran and Dixit, "Evaluation Precedes Evolution: Rubrics for Agents That Rewrite Themselves" (seed) | Google (Google Cloud AI FDE team) | 2026-06-15 | evaluation `evaluation-design.md`, `expert-review.md`; instructions `prompt-as-code.md` (Optimisers) | Rubrics shaped by verifiability, horizon and stakes; per-stage scoring; asymmetric re-checking in code; a business metric instead of a proxy score; a rubric before any optimiser loop | M–L | pasted |
| 2 | Miller, "A statistical approach to model evaluations" | Anthropic | 2024-11-19 | evaluation `evaluation-design.md:106`, `quality-iteration.md:12,45`; release `ci-eval-gates.md:55`; presenter `storyline.md:52-56`, `value-report.md:51-52`; discovery `opportunity-portfolio.md:75` | Paired differences with clustered standard errors; a minimum detectable difference before keeping a "win"; power analysis to size development, holdout and pilot samples | M | readable |
| 3 | Wimberly, Marker, Siegel and Kwatra, "Eval-driven system design: from prototype to production" | OpenAI cookbook (with Fractional AI) | undated, archived | evaluation `result-auditing.md:11`, `quality-iteration.md:36`; discovery `discovery-brief-template.md:96-106`, `technology-fit.md:39`; presenter `value-report.md:69-71` | A priced cost of each error type at volume, set against the current process, as the gate; per-stage graders fed the stage's actual input, reported beside the end-to-end score | M | readable |
| 4 | Melnyk and Dai, "Driving the Agent Quality Flywheel from Your Coding Agent" | Google | 2026-06-30 | instructions `prompt-as-code.md:202-218`; evaluation `live-evaluations.md:37`, `evaluation-design.md` | The party that proposes a fix never grades it; a categorical rubric with a not-applicable class and a rate gate; the trajectory rater must receive tool schemas | S–M | readable |
| 5 | "An update on recent Claude Code quality reports" (April 23 postmortem) | Anthropic | 2026-04-23 | release `versioning.md:30-36`, `SKILL.md:49`; instructions `SKILL.md:62`, `prompt-as-code.md:97-113`; observability `slo-and-alerting.md:27`, `export-paths.md:10`; evaluation `evaluation-design.md:9` | Thinking level and trimming, compaction or cache settings become release events with a soak; the full suite runs on every model that receives a prompt; line ablation for prompt regressions; a degraded-variant control; release-sliced SLIs | M | readable |
| 6 | McAllister, "A postmortem of three recent issues" | Anthropic | 2025-09-17 | observability `slo-and-alerting.md:73`, `debugging-runbook.md:44`; model contracts `model-selection.md:46` | A fixed probe set run through the deployed endpoint on a schedule; deterministic output-sanity metrics (unexpected script, malformed rate); "a pinned ID does not pin behaviour". Builds on 5 | M | readable |
| 7 | Kim, Liu et al., "Towards a science of scaling agent systems" (blog and arXiv 2512.08296) | Google Research, Google DeepMind | 2026-01-28 | interoperability `topology.md:40-52`, `evaluation-across-boundaries.md:107-109`; designer `design-decisions.md:116-117`; workflow `orchestration.md:12` | First controlled cross-vendor evidence: measure a single-agent baseline first; do not split sequential work; tool count is a cost of splitting; the fan-in must validate | M | readable |
| 8 | Rajasekaran, "Harness design for long-running application development" | Anthropic | 2026-03-24 | workflow `orchestration.md:13,43-46`; evaluation `expert-review.md` pointer; release `model-migration.md:35-42`; designer `design-decisions.md:112` | An in-loop critic is a judge and is calibrated like one; criteria are agreed in state before drafting, each with a hard threshold; scaffolding is ablated at each model migration. Builds on 4 and 7 | M | readable |
| 9 | McGuinness et al., "How we contain Claude across products" (with Dworken and Weller-Davies, "Making Claude Code safer with sandboxing", 2025-10-20, as its source) | Anthropic | 2026-05-25 | guardrails `human-review.md:145,157`, `SKILL.md:54`; security `threat-model.md:62`, `tool-supply-chain.md:140-141`, `agency-and-output.md:176,217-222`, `assets/adversarial-cases.json` | A coded bound before any approval prompt; approval share per gated tool as a load measure; "allowlists are capability grants" restated for `*.googleapis.com` (VPC-SC, own-principal egress); both filesystem and network isolation | M | readable |
| 10 | Martin, Cemaj and Cohen, "Scaling Managed Agents: Decoupling the brain from the hands" | Anthropic | 2026-04-08 | tool-auth `SKILL.md:53`, `gcp-credentials.md:7-14,28`; security `agency-and-output.md:176` | Scoping is not containment: credentials are never reachable from model-written code; a broker outside the sandbox attaches them; probe the sandbox for env vars, files and the metadata server. Builds on 9 | S–M | readable |
| 11 | Trębacz et al., "Auto-review of agent actions without synchronous human oversight" | OpenAI | 2026-04-30 | guardrails `human-review.md` (new subsection); security adversarial-suite cross-reference | A separate reviewer agent before the person for reversible, medium-tier calls outside the coded bound; a denial returns its reason; stop after N consecutive denials; never a stand-in on the irreversible tier. Builds on 9 | M–L | readable |
| 12 | Papapanagiotou, Malesevic, Heiser and Meshenberg, "AI in SRE" whitepaper (with the Cloud blog summary of 2026-05-29) | Google SRE | 2026 | guardrails `human-review.md:145`, `cost-controls.md:15` | Escalation that reads live production state; auto-approval granted per action class only on recorded missed- and over-escalation rates; an operator revoke switch separate from the cost kill switch; dry-run previews. Builds on 11 | M | readable |
| 13 | Wu et al., "Introducing advanced tool use on the Claude Developer Platform" | Anthropic | 2025-11-24 | tool-interface `tool-count-and-toolsets.md:111-118`, `naming-and-consolidation.md:99`, `results-and-errors.md:39`, new section; optimise `context-window.md:136` | When tool search is not worth it; resolve its conflict with "mask rather than add tools" by measured cache hits; one to five example calls per tool; programmatic tool calling as an option gated on executor controls | L | readable |
| 14 | Styer, Patlolla, Mohan and Diaz, "Agent Tools & Interoperability with MCP" (Kaggle whitepaper) | Google | 2025-11 | instructions `tool-use-guidance.md:33,100-106`; tool-interface `naming-and-consolidation.md:20-46`, `tool-count-and-toolsets.md:111-118`; security or interoperability (semantic shadowing) | Bind names for stable FunctionTools, describe actions for MCP and dynamic tools; record cross-tool side effects; check incoming MCP tools for semantic shadowing; build the tool-search index only from allow-listed tools. Builds on 13 | M | mirror |
| 15 | Rashtchian and Juan, "Deeper insights into retrieval augmented generation: the role of sufficient context" | Google Research | 2025-05-14 | memory `retrieval-strategy.md:120-135`; workflow `content-safeguards.md:96-105`; evaluation (error-analysis slice) | A calibrated, model-judged sufficiency label per issue (sufficient, incomplete, inconclusive, contradictory) that routes to abstention instead of a larger k; abstention reported as its own rate | M | readable |
| 16 | Chung, Kakkar, Gan, Milne and Özcan, "Is Long Context All You Need? Leveraging LLM's Extended Context for NL2SQL" | Google | 2025-06 (VLDB) | sql `implementation.md:23,27`, `acceptance-and-extensions.md` §3 | Measure schema-selection recall and err towards recall; put reviewed business definitions before example banks; prefer offline-generated, reviewed examples; note the latency knee near 32k tokens | M | readable |
| 17 | Jacobsson, "Getting AI to write good SQL", and Pourreza and Kubik, "A new top score: Advancing Text-to-SQL on the BIRD benchmark" (read as a pair) | Google Cloud | 2025-05 and 2025-11 | sql `execution-safety.md:33`, `compatibility.md:47`, `implementation.md` | Repair as a bounded loop fed only the parser or dry-run error; optional voting over execution results across N candidates, each passing the policy check and the bytes cap; an answerability check first. Builds on 16 | M | readable |
| 18 | Basu Mallick and Schmid, "New Gemini API updates for Gemini 3", with Flórez Fernández, "Migrating to Gemini 3: … Thought Signatures" | Google | 2025-11-25 and 2025-12-01 | model contracts `validation-and-repair.md:51-66`, `validation.md`; sensitive data `implementation-recipes.md:79-86` | A callback that replaces model content keeps thought parts and signatures, or a test records the loss; never rewrite a function-call part; a multi-turn test asserts it | S–M | readable |
| 19 | Gema et al., "Inverse Scaling in Test-Time Compute" (arXiv 2507.14417) | Anthropic | 2025-07 (TMLR) | model contracts `SKILL.md:66`, `reasoning-and-sampling.md:19`, `model-selection.md:34` | A measured sweep of `thinking_level` per agent on the dev set, including distractor-heavy cases; "higher is safer" becomes a hypothesis | M | readable |
| 20 | Nasr, Carlini et al., "The Attacker Moves Second" (arXiv 2510.09023), with Shi et al., "Lessons from Defending Gemini Against Indirect Prompt Injections" (arXiv 2505.14534) | Google DeepMind, Anthropic, OpenAI | 2025-10 and 2025-05 | security `agency-and-output.md:250-261,296-297`, `adversarial-testing.md:138-141,275-279`; sensitive data `production-policy.md:94-127` | Measured evidence that screens such as Model Armor are not the boundary; label every red-team result static or adaptive; no claim about a screen's contribution from static payloads | S–M | readable (verify affiliations) |
| 21 | Spânu and Shadwell, "Preventing URL-Based Data Exfiltration in Language-Model Agents" | OpenAI | published 2026-01-28 | security `tool-supply-chain.md:137-145`, `agency-and-output.md:232-236` | Fetch or render automatically only URLs with trusted provenance (typed by the user, returned by search, canonicalised); re-check every redirect host; otherwise return the link unfetched; bound distinct fetches | M | readable |
| 22 | g-AMIE: Stutz and Harris, "Enabling physician-centered oversight for AMIE" (blog), with arXiv 2507.15743 | Google DeepMind, Google Research | 2025-08-12 | guardrails `human-review.md:23,40-47,111-113`; frontend `agent-ui-states.md:17`, `DESIGN.md:618`; observability `feedback-capture.md` | "Approved with edits" and "follow-up requested" as review outcomes: the edited payload is re-validated, gets a new digest and is shown beside its source; per-field edit rate as a quality signal; review drafts kept short because review time was measured | M | readable |
| 23 | Patwardhan et al., "GDPval" (arXiv 2510.04374) | OpenAI | 2025-10-05 | discovery `discovery-brief-template.md:96-98`, `why-projects-stall.md:23`; presenter `value-report.md:59-65` | Review-adjusted savings for assist-then-review work: agent time + review time + (1 − acceptance) × manual time; the first goal measures review minutes and acceptance. Builds on 3 | M | readable |
| 24 | Saboo and Dong, "Build long-running AI agents that pause, resume, and never lose context with ADK" | Google | 2026-05-12 | workflow `orchestration.md:164-194` (new section), `runtime.md:56-60`; evaluation `live-evaluations.md:28` | Multi-day progress as an enumerated step in state, advanced by authenticated external events through `state_delta`; eval cases pre-seed state to simulate elapsed time. Keeps the skill's stricter durability and redelivery rules | M | readable |
| 25 | Young, "Effective harnesses for long-running agents" | Anthropic | 2025-11-26 | workflow (the same section as 24) | A task ledger with criteria that cannot change after creation; status changed only by an evidence-checking tool; a health check on resume; one item per invocation. Builds on 24 | M | readable |

### Tier 2: narrower but distinct

| # | Article | Org | Date | Skills and files it changes | Expected benefit | Size | Access |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 26 | Shihipar, "The new rules of context engineering for Claude 5 generation models" | Anthropic | 2026-07-24 | instructions `instruction-structure.md:91-110`, `scripts/instruction_lint.py:159-170`, `model-notes.md:53-62`, `exemplars.md` | Review the recorded request across all instruction layers for directives that conflict; on a model upgrade, remove compensating rules one at a time against the eval; when not to use exemplars | M | readable |
| 27 | GPT-5.1 prompting guide, metaprompting section | OpenAI cookbook | undated | instructions `instruction-structure.md:99-100`; evaluation `quality-iteration.md:19-46` | From an error category to the prompt lines responsible (a diagnosis step), then a separate minimal-patch step with notes. Builds on 5 and 26; conflict noted below | M | readable |
| 28 | Wan, Sun, Nakhost and Arık, "Teach Better or Show Smarter?" (arXiv 2406.15708) | Google Cloud AI Research | 2024-11 (NeurIPS) | instructions `exemplars.md:18-26`, `prompt-as-code.md:202-218` | Search exemplar subsets taken from the model's own correct dev outputs, before or alongside instruction optimisation; confirm on the holdout | M | readable |
| 29 | Zhou, Wan, Sun et al., "Multi-Agent Design: Optimizing Agents with Better Prompts and Topologies" (MASS) | Google | 2026-01 (v2) | instructions `prompt-as-code.md:204-206`; interoperability `topology.md:40-46`; workflow `orchestration.md:60-61` | Optimise each agent's prompt before adding agents or topology; `adk optimize` touches only the root, so optimise sub-agents on their own cases. Builds on 7 and 28 | M | readable |
| 30 | Metwally and McDuff, "A scalable framework for evaluating health language models" | Google Research | 2025-08-26 | evaluation `expert-review.md:74-83` | Turn Likert scales into precise boolean questions; record per-case applicability as a measured decision; an altered-input twin must lower the score before a rubric gates anything | M | readable |
| 31 | Jacovi, Das et al., "The FACTS Grounding Leaderboard" (arXiv 2501.03200) | Google DeepMind, Google Research | 2025-01 | evaluation `source-support-calibration.md:13-27`; release `model-migration.md:51` | An eligibility check (did it answer the request?) before grounding; same-family judge self-preference named and measured; pick the judge template by Macro-F1 | S | readable |
| 32 | Arora et al., "HealthBench", and Starace et al., "PaperBench" | OpenAI | 2025-05 and 2025-04 | evaluation `expert-review.md:113-118,168-172`, `evaluation-design.md:51` | Accept a judge when its agreement with each expert is within the expert-to-expert band; choose the judge from an F1-against-cost table; a weighted rubric tree whose critical leaves stay hard gates | S | readable |
| 33 | Kalai, Nachum, Vempala and Zhang, "Why Language Models Hallucinate" (eval-scoring part only) | OpenAI | 2025-09-04 | evaluation `evaluation-design.md:9` | A confidence-target score for answer-or-escalate cases, with t set from the discovery cost ratio, kept beside the missed-escalation gate | S | readable |
| 34 | "Reasoning models don't always say what they think" | Anthropic | 2025-04-03 | model contracts `output-contracts.md:7-9,42-46`, `reasoning-and-sampling.md:47` | A `reason` field or thought summary is not evidence; require identifiers or quotes that code verifies; never show thought summaries as the explanation in review records. Builds on 1 | S | readable |
| 35 | Parker, "Architecting Security for Agentic Capabilities in Chrome" | Google | 2025-12-08 | security `injection-patterns.md:121-124`, `SKILL.md:130`; sensitive data `boundaries.md:126-128` | An alignment critic that sees only action metadata, with a bounded veto loop; per-session read sources and write destinations, set by trusted code | S–M | readable |
| 36 | Bagdasarian et al., "AirGapAgent" (arXiv 2405.05175) | Google Research, Google DeepMind | 2024-09 | sensitive data `boundaries.md:85-88,101-103` | A minimiser agent (no tools, `include_contents='none'`, schema of permitted fields) decides which of the user's data may go to a party the agent converses with | M | readable |
| 37 | Yan and Lee, "ReasoningBank: enabling agents to learn from experience" | Google Cloud | 2026-04-21 | memory `SKILL.md:63-69`, new reference section | Procedural (strategy) memory as its own mode: app scope, no user facts, written by code from judged trajectories, promoted by review, screened and roll-backable, measured | L | readable |
| 38 | Milam and Gulli, "Context Engineering: Sessions, Memory" (Kaggle whitepaper) | Google | 2025-11 | memory `memory-bank.md:19,39,103-107`, `retrieval-strategy.md:141` | A source-trust order for memories (tool output discouraged); instruction-versus-history placement with an over-influence case; extraction precision against golden memories; regenerate when one source is revoked | M | mirror |
| 39 | "Introducing Contextual Retrieval" | Anthropic | 2024-09-19 | memory `retrieval-strategy.md:93,100-103` | A concrete contextualiser contract (into both lexical and dense indexes, document cached during the batch, recall@k measured before and after) | S | readable |
| 40 | "Clio: privacy-preserving insights into real-world AI use" | Anthropic | 2024-12-12 | observability `trace-to-evaluation.md:20`, `bigquery-analytics.md`; sensitive data | Find unknown failure clusters in unrated production conversations, shown only above a minimum distinct-user count and after a PII audit | M | readable |
| 41 | Liu et al., "Budget-Aware Tool Use Enables Effective Agent Scaling" (arXiv 2511.17006) | Google DeepMind, Google Cloud AI Research | 2025-11 (COLM 2026) | guardrails `runtime-bounds.md:9`, `token-budgets.md` | Show the model its used and remaining tool budget from the same counters that enforce it; keep enforcement in code; measure | S–M | readable |
| 42 | Schaekermann and Sayres, "Towards better health conversations: … a 'wayfinding' AI agent" | Google Research | 2025-09-25 | frontend `agent-ui-states.md:11-24`, `DESIGN.md`; instructions (prompt rule) | A clarifying-question state: structured questions shown apart from a best-effort answer, at most three per turn | M | readable |
| 43 | Trębacz et al., "A Practical Approach to Verifying Code at Scale" | OpenAI | 2025-12-01 | evaluation `expert-review.md:183-185`; observability | An expected-utility threshold for anything that routes items to people; an acted-on rate per flag source. Builds on 11 | S | readable |
| 44 | "Deploying AI from pilot to production" (with Accenture) | Anthropic (organisational co-author, no byline) | 2026-09-14 | guardrails `human-review.md`; presenter `value-report.md:96-100` | Oversight tiers with audit cadences, including sampled review after the fact; a checkpoint audit (catch rate, change rate, cost); error cost at full volume before scaling. Builds on 3 and 12 | M | readable (weaker affiliation) |
| 45 | Papakonstantinou and Sherkat, "Optimizing AlloyDB AI text-to-SQL accuracy" | Google Cloud | 2025-12-19 | sql `SKILL.md:54-56`, `implementation.md:13` | Reviewed predicate fragments that compose with a template; a deterministic restatement of metric, grain, window and filters with every answer. Builds on 17 | S–M | readable |
| 46 | Segato, "Quantifying infrastructure noise in agentic coding evals" | Anthropic | 2026-02-05 | evaluation `live-evaluations.md:98-100`, `result-auditing.md:9`; security sandbox checklist | Record executor resource limits and the time window as variables of each run; a small difference is noise unless configurations match. Builds on 2 | S | readable |

### Tier 3: small additions

| # | Article | Org | Date | Skills and files it changes | Expected benefit | Size | Access |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 47 | "Optimize Prompts" and "GPT-5 Prompt Migration and Improvement Using the New Optimizer" | OpenAI cookbook | undated | instructions `exemplars.md:71-78`, `instruction-structure.md:108-110` | Each exemplar must obey the instruction's explicit rules, and is re-checked after an instruction change; flag only genuine contradictions. Builds on 27 | S | readable |
| 48 | Agarwal, Singh et al., "Many-Shot In-Context Learning" | Google DeepMind | 2024 (NeurIPS) | instructions `exemplars.md:22-26,42-43` | Sweep the exemplar count, since the curve can turn down; exemplars can come from the model's own outputs, filtered by correctness. Builds on 28 | S | readable |
| 49 | Nardini and Lee, "Vertex AI Prompt Optimizer: New algorithm & SDK for the general availability" | Google | 2025-08-12 | instructions `prompt-as-code.md:214-218` | Zero-shot versus data-driven optimiser by labelled-set size; no data-driven runs on preview or global-only models; record the metric weights. Builds on 28 | S | readable |
| 50 | Agarwal, Blount and Guan, "Why we built ADK 2.0" | Google | 2026-07-01 | discovery `technology-fit.md:79`; designer `design-decisions.md:108-113` | A vendor-measured, single-scenario figure for workflow versus agent (tokens and seconds), as a reference point for the existing rule | S | readable |
| 51 | Skrzypek and Cannas, "Five lessons for moving agents into production" | Google Cloud Consulting | 2026-10-16 | designer `delivery-profiles.md`, `engagement-scoping.md:86` | A UAT goal before go-live, with tester hours as a client dependency in the SOW and an allowance for rework | S | readable |
| 52 | Tamkin and McCrory, "Estimating AI productivity gains from Claude conversations", and Huang et al., "How AI is transforming work at Anthropic" | Anthropic | 2025-11 and 2025-12 | presenter value report; discovery `opportunity-portfolio.md:20` | A survey-based or model-estimated time saving is an estimate; handling time comes from timestamps, as a distribution; new work is reported apart from time saved. Builds on 23 | S | readable |
| 53 | Schaekermann and Karthikesalingam, "Exploring the feasibility of conversational diagnostic AI in a real-world clinical study" | Google | 2026-03-11 | presenter `rollout-and-adoption.md:182-206` | For a high-stakes pilot: written stop criteria, a named supervisor for the first N conversations, and an intervention log feeding the hypercare exit | S | readable |
| 54 | Seroter, "How to force your custom agent to stop and seek human approval" | Google (personal blog) | 2026-05-06 | guardrails `human-review.md:101-103` | A "changes requested with notes, then revise" path; test structured payloads through the REST path because the dev UI may not drive them. Builds on 22 | S | readable |
| 55 | Allen, "How to Evaluate Live & Voice Agents in ADK" | Google | 2026-08-24 | evaluation (new section) | Voice eval cases with the speech and simulator models pinned, the transcript as what is graded, and voices as slices; config keys to be verified in ADK source | S–M | readable |
| 56 | Okcular, "Context Engineering for Personalization: State Management with Long-Term Memory Notes" | OpenAI cookbook (employer unconfirmed) | 2026-01-05 | memory `memory-bank.md:116-123` | Precedence at inference time (current message, then session, then recalled memory) with a contradiction test; write-rate and blocked-write counters. Builds on 38 | S | readable |
| 57 | Jin, Yoon, Han and Arık, "Long-Context LLMs Meet RAG" (arXiv 2410.05983) | Google Cloud AI Research | 2024-10 | memory `retrieval-strategy.md:171`; optimise `context-window.md:90` | Order evidence with the strongest passages at the edges when k is large; sweep k for a peak. Builds on 39 | S | readable |
| 58 | Schmid, "How Agents Manage Other Agents: Four Subagents Patterns in 2026" | Google DeepMind (from speaker bios) | 2026-05-05 | tool-interface `delegation-interfaces.md:12-18,47-60` | Recognise model-driven asynchronous fan-out and say what ADK offers, or move it into code-driven parallel work | M | readable |
| 59 | Schmid, "MCP is Not the Problem, It's your Server" | Google DeepMind (from speaker bios) | 2026-01-21 | interoperability `mcp-exposure.md:106-125` | An exposed MCP surface follows the tool-interface rules, with a per-server budget and servers split by persona | S | readable |
| 60 | Coleman, "Eval awareness in Claude Opus 4.6's BrowseComp performance" | Anthropic | 2026-03-06 | evaluation | The agent under test must not be able to reach gold labels; flag token-usage outliers for transcript review | S | readable |
| 61 | Melendez and Dalida, "Learn how to handle 429 resource exhaustion errors in your LLMs" | Google Cloud | 2024-11-22 | model contracts `failover-and-providers.md:21` | A circuit breaker in front of a failing primary model, since `FallbackModel` tries the primary on every request | S | readable |

## Entries

Each entry has the scout's findings in short form. Line numbers are as read
on 28 October 2026.

### 1. Evaluation Precedes Evolution (seed)

- **Authors and affiliation.** Pouya Ghiasnezhad Omran and Tanya Dixit,
  LinkedIn, 15 June 2026. Both are Forward Deployed Engineers on Google
  Cloud's AI FDE team in Sydney: the article's author note and Tanya Dixit's
  byline ("FDE @ Google") say so, and the user confirmed it. Pasted by the
  user on 28 October 2026.
- **What it teaches.** Three axes for shaping a rubric (verifiability,
  horizon, stakes) and four rules, each tied to code in google/adk-samples
  `python/agents/invoice-processing`: deterministic checks before any judge;
  name failure modes and score every stage; asymmetric verification enforced
  in Python; a business metric (share of cases needing no manual
  intervention) instead of a proxy score.
- **Already covered.**
  - Code checks before any judge: `evaluation-design.md:47`.
  - One calibrated judge per failure mode: `expert-review.md:159`.
  - TPR and TNR on a review queue: `expert-review.md:168-185`.
  - Missed escalation and over-escalation rates: `evaluation-design.md:9`.
- **Not covered.**
  - The three axes.
  - Per-stage scoring.
  - Asymmetric re-checking in code.
  - A business metric instead of a proxy, with its two gaming patterns.
  - A rubric as the precondition for an optimiser: `prompt-as-code.md:202`
    treats `adk optimize` as one reviewed pass.
- **No other source.** No Google, Anthropic or OpenAI article found by the
  scouts carries the three axes.

### 2. A statistical approach to model evaluations

- **Source.** Evan Miller, Anthropic research, 2024-11-19; paper arXiv
  2411.00640. Older than the preferred window but the reference others cite.
- **What it teaches.**
  - Report the standard error, clustered on the unit of randomisation.
    Clustered errors can be more than three times the naive ones.
  - Compare two systems with the paired-difference standard error.
  - Size a sample with a power formula. The worked example needs about 969
    cases to detect a 3-point difference.
- **What the skills say now.**
  - `evaluation-design.md:106`: "use uncertainty methods respecting repeated
    trials within cases". No method is named.
  - `quality-iteration.md:12`: five to twenty cases. `quality-iteration.md:45`:
    keep a change when the category shrinks, with no noise test.
  - `storyline.md:52-56`: a one-over-root-n rule of thumb.
  - None of the evaluation skills contain "standard error", "confidence
    interval" or "power analysis".
- **What a coding agent would do differently.**
  - Report a paired difference with an interval.
  - Label a small win "within noise".
  - Size the holdout, the CI set and pilot samples by power analysis.
- **Ownership.** adk-agent-evaluation computes these figures; presenter and
  discovery use them.
- **Size.** M.
- **Overlap.** 46.

### 3. Eval-driven system design (receipt inspection)

- **Source.** OpenAI cookbook, joint with Fractional AI. Shikhar Kwatra is
  OpenAI; the other authors are Fractional. Undated and archived.
- **What it teaches.**
  - A `calculate_costs(fp_rate, fn_rate, per_receipt_cost)` model prices each
    error type at a million receipts a year, against today's manual process.
  - "Not all evals matter": an 85% merchant-name error changed no audit
    decision.
  - 18 graders score each step on its actual input, as well as end to end.
- **What the skills say now.**
  - Error cost is recorded only in words: `discovery-brief-template.md:106`
    and `technology-fit.md:39`.
  - Error rates are never turned into cost.
  - Stage attribution exists (`result-auditing.md:11`, `quality-iteration.md:36`),
    but there is no per-stage grader.
- **What a coding agent would do differently.**
  - Multiply measured error rates by the brief's unit costs and use that as
    the gate.
  - Grade each stage on its own input.
  - In presenter, count error and review costs in cost per outcome.
- **Size.** M.
- **Overlap.** 1, 23, 44.

### 4. Driving the Agent Quality Flywheel from Your Coding Agent

- **Source.** Dima Melnyk (Product Manager, Cloud AI) and Jason Dai
  (Software Engineer), Google Developers Blog, 2026-06-30.
- **What it teaches.**
  - A five-step loop: prepare, infer, grade, analyse, optimise.
  - A custom categorical rubric, `revision_honored`, with an act-if-over-20%
    gate. The rate went from 21% to 5%.
  - The proposer never grades its own fix.
  - The managed trajectory rater false-flagged calls when it lacked the tool
    schemas.
- **What the skills say now.** "categorical", "proposer" and "never grades"
  appear nowhere. `prompt-as-code.md:202-218` says nothing about keeping the
  grader independent.
- **Size.** S–M.
- **Overlap.** 1, 8. Philipp Schmid's "Recursive Self-Improvement" (rejected
  below) makes the same independence point.

### 5. April 23 postmortem (Claude Code quality reports)

- **Source.** Anthropic Engineering, 2026-04-23, no named author.
- **What it teaches.** Three non-model changes degraded quality:
  - a lower default reasoning effort ("the wrong tradeoff");
  - a cache-trimming rule that fired every turn instead of once;
  - a length limit in the system prompt, found by ablation to cost 3%.
- **Why it was missed.** Each hit a different slice on a different schedule,
  so the result looked like broad, inconsistent degradation.
- **Commitments.** A per-model suite on every prompt change; line ablations;
  model-specific changes gated to their target model; soak and gradual
  rollout.
- **What the skills say now.**
  - `versioning.md:30-36` omits generation and context-management settings
    as release events.
  - "ablat" and "soak" appear nowhere.
  - SLIs are sliced by agent, tool and model only (`slo-and-alerting.md:27`).
  - Only the do-nothing control exists (`evaluation-design.md:9`); there is no
    known-broken variant.
- **What a coding agent would do differently.**
  - Treat thinking level and trimming, compaction or caching settings as
    release events with a soak.
  - Test that a trimming rule fires once per trigger.
  - Run the full suite on each model that receives the prompt, including
    FallbackModel members.
  - Ablate line by line when a regression is unexplained.
  - Set `service.version` on Cloud Run and GKE, and slice SLIs by release.
  - Treat a length limit as a measured, broad-risk change (instructions
    `SKILL.md:62`).
- **Size.** M.

### 6. A postmortem of three recent issues

- **Source.** Sam McAllister, Anthropic Engineering, 2025-09-17.
- **What it teaches.**
  - Three serving bugs degraded output with no change to the model ID.
  - Standard evals missed them because the model recovers from isolated
    mistakes.
  - Fixes: continuous quality evals on production; detection tests for
    unexpected characters; privacy-preserving debugging.
- **What the skills say now.**
  - Production quality comes only from sampled judges
    (`slo-and-alerting.md:73`).
  - The nightly run is a release gate (`ci-eval-gates.md:11`).
  - `model-selection.md:46` treats the resolved `model_version` as the
    identity check.
- **What a coding agent would do differently.**
  - Add a "fixed-probe quality" SLI and output-sanity alerts.
  - Check the change log against symptom onset (`debugging-runbook.md:44`).
  - Count unexpected-script output as a contract failure.
- **Size.** M.
- **Builds on.** 5.

### 7. Towards a science of scaling agent systems

- **Source.** Yubin Kim, Xin Liu and others. Google Research, Google
  DeepMind and MIT. Blog 2026-01-28; arXiv 2512.08296 (100k of 169k
  characters read).
- **What it teaches.** 180 configurations compared:
  - centralised multi-agent setups gained +80.8% on parallel finance work;
  - every multi-agent setup lost 39–70% on sequential planning;
  - errors amplified 17.2× in independent setups against 4.4× centralised;
  - coordination overhead ranged from 58% to 515%;
  - adding agents tends to hurt once a single agent already scores about 45%;
  - a predictive model picked the best architecture for 87% of held-out
    configurations.
- **Caveat.** The error-amplification main effect is not significant once
  other metrics are controlled (p = 0.441), so treat those figures as
  descriptive.
- **What the skills say now.** `topology.md:40-52` has only Anthropic,
  Cognition and MAST, and says they agree on "the mechanism … not on a
  universal rule".
- **What a coding agent would do differently.**
  - Measure a single-agent baseline first.
  - Record how far the task splits into parallel parts, and its tool count.
  - Decline a split when the work is sequential or the baseline is already
    high.
  - Make the fan-in validate the branches, not just concatenate them.
- **Size.** M.
- **Note.** Found by three lanes. Put it in interoperability's evidence table
  and point to it from designer and workflow; do not repeat it.

### 8. Harness design for long-running application development

- **Source.** Prithvi Rajasekaran, Anthropic Labs, 2026-03-24.
- **What it teaches.**
  - A planner, a generator and a separate evaluator. A standalone evaluator
    is easier to make sceptical; out of the box it "talked itself into
    approving".
  - It was calibrated by reading its logs, with few-shot examples carrying
    score breakdowns.
  - "Sprint contracts" agree the criteria before work starts. Each criterion
    has a hard threshold, and failing any one fails the round.
  - On a newer model, components were removed one at a time. Each component
    encodes an assumption about what the model cannot do, and those
    assumptions go stale.
- **What the skills say now.** `orchestration.md:43-46` covers only the loop
  mechanics. No skill says an in-loop critic needs judge calibration
  ("skeptic" and "lenien" have no hits).
- **What a coding agent would do differently.**
  - Write the criteria to state before the generator runs.
  - Have the critic return one pass or fail per criterion; code decides the
    exit.
  - Calibrate the critic on labelled examples.
  - Record whether the loop beats a single pass.
  - Ablate the scaffolding at each model migration (`model-migration.md:35-42`).
- **Size.** M.
- **Not imported.** No Claude model names or dollar figures.

### 9. How we contain Claude across products

- **Source.** Max McGuinness, Mikaela Grace, Jiri De Jonghe, Jake Eaton and
  Abel Ribbink, Anthropic, 2026-05-25. Read with its source, Dworken and
  Weller-Davies (2025-10-20).
- **What it teaches.**
  - About 93% of permission prompts were approved, and attention drops as
    prompts pile up.
  - A sandbox cut prompts by 84%.
  - A phished exfiltration prompt succeeded 24 of 25 times; only the egress
    and filesystem boundaries held.
  - An allowlisted API domain carried data into an attacker's account. The
    fix was a proxy that passes only the VM's own session token.
  - Rules: "treat allowlists as capability grants"; match isolation to the
    user's capacity for oversight; prefer standard primitives to custom
    proxies.
- **What the skills say now.**
  - Reviewer fatigue routes only to escalation rules (guardrails
    `SKILL.md:54`).
  - Nothing treats an allowed host as a capability (`threat-model.md:62`,
    `tool-supply-chain.md:140-141`).
  - Egress in the Horizon sandbox is all or nothing
    (`agency-and-output.md:217-222`).
- **What a coding agent would do differently.**
  - Bound gated tools in code first, so only calls outside the bound ask.
  - Track the approval share and prompts per session for each tool.
  - Put a VPC-SC perimeter, or own-principal egress, on access to
    `*.googleapis.com`.
  - Require both isolations for `EnvironmentToolset` and `BashTool`.
  - Add two adversarial seeds: an attacker key in a document, and a
    user-typed exfiltration request.
- **Size.** M.

### 10. Scaling Managed Agents

- **Source.** Lance Martin, Gabe Cemaj and Michael Cohen, Anthropic,
  2026-04-08.
- **What it teaches.**
  - With credentials in the same container as generated code, an injection
    had only to read the environment.
  - Narrow token scoping was rejected because it "encodes an assumption".
    Tokens are made unreachable instead: kept in a vault behind a proxy.
  - Separately, it measured time-to-first-token falling about 60% at p50.
    That result is out of scope here.
- **What the skills say now.** `gcp-credentials.md:14` relies on tier-scoped
  credentials and mentions a broker only for scale (`:28`).
- **What a coding agent would do differently.**
  - Add an authority row for model-written code that calls an authenticated
    service: a placeholder inside the sandbox, a broker outside it.
  - Extend the in-sandbox probe beyond Cloud Run.
- **Size.** S–M.

### 11. Auto-review of agent actions

- **Source.** Maja Trębacz and others, OpenAI Alignment blog, 2026-04-30.
- **What it teaches.**
  - Three layers: in-sandbox actions get no review; boundary-crossing
    requests go to a reviewer agent; a person comes last.
  - In 10,000 actions, 720 were reviewed and 7 denied, about 200 times fewer
    interruptions.
  - Synthetic recall: 90.3% for overeager actions and 99.3% for injection.
  - A denial returns its rationale, and the run stops after repeated
    denials.
  - The reviewer could be misled.
- **What the skills say now.** "auto-review" and "repeated denials" appear
  nowhere.
- **ADK restatement.**
  - A Gemini reviewer runs inside `require_confirmation` or
    `before_tool_callback`, only for reversible, medium-tier calls outside
    the bound.
  - A denial is returned as a tool error carrying the reason.
  - A consecutive-denial counter sits in state.
  - The irreversible tier always goes to a person.
  - False approvals are measured on the security adversarial suite first.
- **Not imported.** OpenAI model names or rates.
- **Size.** M–L.

### 12. AI in SRE

- **Source.** Papapanagiotou, Malesevic, Heiser and Meshenberg, sre.google
  (undated). Cloud blog summary 2026-05-29; Carlesso and Medrano Llamas,
  Gemini CLI outages post, 2026-01-23.
- **What it teaches.**
  - A risk check against live production context downgrades an autonomous
    request to one that needs approval.
  - Autonomy levels L0–L4 are promoted only on sustained, statistically
    significant success.
  - Required `dry_run`.
  - A "Red Button" revokes autonomy.
  - Post-actuation polling checks that a mitigation worked.
  - About 44% lower time to mitigate.
- **What the skills say now.** Static rules only (`human-review.md:145`); the
  kill switch is cost-only (`cost-controls.md:15`).
- **What a coding agent would do differently.**
  - The confirmation callable reads a trusted state snapshot.
  - An action class is promoted to auto-approval on recorded missed- and
    over-escalation rates.
  - Operators get a revoke control.
  - Write tools offer a preview variant.
- **Size.** M.

### 13. Introducing advanced tool use

- **Source.** Bin Wu and others, Anthropic, 2025-11-24.
- **What it teaches.**
  - **Tool search:** 85% fewer definition tokens; MCP-eval accuracy rose from
    49% to 74%.
  - **Programmatic tool calling:** 37% fewer tokens. Opt in only tools that
    are parallel-safe and idempotent, with documented return formats.
  - **Tool use examples:** one to five per tool; accuracy on complex
    parameters rose from 72% to 90%.
  - "Layer by bottleneck."
- **What the skills say now.**
  - The `find_tools` pattern (`tool-count-and-toolsets.md:111-118`) has no
    "not worth it" rule. It conflicts with "mask rather than add or remove
    tools mid-task" (`context-window.md:136`), because a growing `get_tools`
    set changes the cache prefix.
  - Example values are covered (`naming-and-consolidation.md:99`), but whole
    example calls are not.
  - Programmatic calling is not covered. The 2026-10-21 integration report
    (line 321) assigned it to tool-interface, gated on executor controls.
- **What a coding agent would do differently.**
  - Choose masking or dynamic loading by measured cache hits and
    declaration bytes.
  - Add one to five example calls only where the schema is ambiguous.
  - Offer programmatic calling only behind the security skill's executor
    rules.
  - Whether ADK 2.8.0 lets an executor call FunctionTools must be checked in
    the pinned source.
- **Not imported.** Vendor parameter names (`defer_loading`,
  `allowed_callers`, `input_examples`).
- **Size.** L.

### 14. Agent Tools & Interoperability with MCP

- **Source.** Styer, Patlolla, Mohan and Diaz, Google (Kaggle five-day
  course), November 2025.
- **How it was read.** The Kaggle page renders no body; the full 55-page PDF
  was read from an unofficial mirror. Confirm the official copy or paste it.
- **What it teaches.**
  - Instructions should "describe actions, not implementations".
  - Document cross-tool side effects.
  - Tool shadowing through description triggers, with a semantic collision
    check against trusted tools.
  - A tool-retrieval index is an attack surface.
- **What the skills say now.**
  - `tool-use-guidance.md:33,100-106` binds exact tool names.
  - The docstring template (`naming-and-consolidation.md:20-46`) does not
    ask for side effects.
  - Shadowing checks catch exact names only (`mcp-consumption.md:124`).
- **Conflict.** It disagrees with the instructions skill on binding names.
  The plan is to keep both rules, each with a stated scope.
- **Size.** M.
- **Overlap.** Most of the whitepaper's tool practices are already covered by
  writing-tools-for-agents.

### 15. Sufficient context

- **Source.** Cyrus Rashtchian and Da-Cheng Juan, Google Research,
  2025-05-14. Paper: Joren et al., ICLR 2025, arXiv 2411.06037. The blog was
  read in full.
- **What it teaches.**
  - Relevant context can still be insufficient.
  - An autorater agreed with experts at least 93% of the time.
  - Insufficient context raised one model's wrong-answer rate from 10% to
    66%.
  - Combining the sufficiency label with confidence improved selective
    accuracy by up to 10%.
- **What the skills say now.** The sufficiency report is deterministic only
  (`retrieval-strategy.md:120-135`, "an empty problem list is the admission
  condition for drafting"). Abstention covers only "no operative policy"
  (`content-safeguards.md:96-105`).
- **What a coding agent would do differently.**
  - Add a model-judged label per issue, calibrated through the evaluation
    skill.
  - Route "insufficient" to abstention rather than raising k.
- **Size.** M.

### 16. Is Long Context All You Need? (NL2SQL)

- **Source.** Chung, Kakkar, Gan, Milne and Özcan, Google, VLDB 2025. Read
  to 100k of 109k characters.
- **What it teaches** (on BIRD):
  - Schema recall matters more than precision: 38% with the top table, 55%
    with the top seven, 62% with all tables.
  - Business-definition hints added 16 points; self-correction about 3.
  - Real training examples hurt.
  - Latency rises sharply beyond about 32k tokens.
- **What the skills say now.** `implementation.md:27` sets a three-table
  limit with no direction about which way to err, and recall is not
  measured.
- **What a coding agent would do differently.**
  - Measure table and column recall of the router.
  - Widen the selection within the approved domain.
  - Prioritise reviewed definitions.
- **Caveat.** Measured on Gemini 1.5; re-measure on the pinned model.
- **Size.** M.

### 17. Text-to-SQL techniques (a pair)

- **Sources.** Per Jacobsson (Principal Software Engineer, Google Cloud),
  2025-05. Pourreza and Kubik (Google Cloud), 2025-11.
- **What they teach.**
  - Deterministic parse or dry-run signals feed a second pass.
  - An answerability check comes first, then a clarifying question.
  - Self-consistency: execute the candidates, cluster them by result, and
    take the largest cluster (one to seven candidates).
  - The training step in the second post is not imported.
- **What the skills say now.** Repair is budgeted but "Not established"
  (`execution-safety.md:33`, `compatibility.md:47`), and self-consistency is
  absent.
- **What a coding agent would do differently.**
  - A bounded repair loop that takes only the error as input.
  - Optional voting, where every candidate passes the policy check and the
    dry-run cap, results are compared with exact decimals, and voting cost
    counts against the bytes budget.
- **Size.** M.

### 18. Thought signatures in callbacks

- **Sources.** Shrestha Basu Mallick and Philipp Schmid, Google Developers
  Blog, 2025-11-25. David Flórez Fernández (Google Cloud Customer Engineer,
  per his Medium bio), Google Cloud Community, 2025-12-01; his code uses the
  older SDK. Gemini thinking documentation, updated 2026-10-14.
- **What they teach.**
  - A missing signature on a function call returns a 400.
  - On text, a missing signature degrades quality without an error.
  - Treat the signature as an immutable blob, and test three or more
    function-call turns.
- **What the skills say now.** `guard_decision` (`validation-and-repair.md:51-66`)
  returns a new `LlmResponse` built from text only. This drops thought parts
  and any signature from what reaches history (confirmed by reading the
  code). `safe_stop` in protect-adk-sensitive-data has the same shape.
  `reasoning-and-sampling.md:21` covers carrying signatures between turns
  only.
- **What a coding agent would do differently.**
  - Carry the original thought parts forward, or record the loss.
  - Add a scripted multi-turn test.
- **Size.** S–M.

### 19. Inverse Scaling in Test-Time Compute

- **Source.** Gema and others, Anthropic Fellows and Anthropic, TMLR 12/2025.
  About half was read.
- **What it teaches.**
  - Accuracy falls as reasoning grows on tasks with distractors, spurious
    features or constraint tracking.
  - Few-shot examples largely removed the effect.
  - No Gemini model was tested, so the method transfers, not the numbers.
- **What the skills say now.** `SKILL.md:66` prefers low thinking for
  classification and keeps thinking on for decisions; no sweep is
  prescribed.
- **What a coding agent would do differently.**
  - Sweep the supported `thinking_level` values on dev cases that include
    distractors.
  - Choose the lowest level that meets the bar, recording accuracy, invalid
    schemas and thought tokens at each level.
- **Size.** M.

### 20. The Attacker Moves Second, with Lessons from Defending Gemini

- **Sources.**
  - Nasr, Carlini, Hayes, Schulhoff, Pluto, Song, Thakurta and others, arXiv
    2510.09023. The affiliation lines were scrambled in the fetch; verify
    them when the article is read in part two.
  - Shi and others, all Google DeepMind, arXiv 2505.14534.
- **What they teach.**
  - Adaptive search reached over 90% attack success against detectors
    including Model Armor.
  - Spotlighting went from about 1% to over 95% under adaptive attack.
  - A human red team broke every defence.
  - In 16 of 24 pairs, adaptive attacks did as well as or better than static
    ones.
- **What the skills say now.** `agency-and-output.md:250-261` says screening
  is a layer but gives no measured result. Live red-team results are not
  labelled static or adaptive (`adversarial-testing.md:275-279`).
- **What a coding agent would do differently.**
  - Label every result static or adaptive.
  - Never credit a screen from static payloads alone.
  - Treat scores returned to a caller as an oracle for attackers. This is
    the scout's inference, not the paper's rule.
- **Size.** S–M.

### 21. Preventing URL-Based Data Exfiltration

- **Source.** Adrian Spânu and Thomas Shadwell, OpenAI PDF, published with
  OpenAI's 2026-01-28 post. The last page was cut off in extraction.
- **What it teaches.**
  - A curated allowlist covered about 10% of real URLs, and open redirects
    bypassed it.
  - Replacement rule: fetch automatically only exact (canonicalised) matches
    to URLs seen by a crawler with no user data, plus URLs the user typed or
    search returned. Anything else gets a warning.
  - Residual risk: a "keyboard attack" that pre-seeds per-character URLs.
- **What the skills say now.** `tool-supply-chain.md:137-145`: allowlist, strip
  query strings, refuse redirects only to private ranges.
- **What a coding agent would do differently.** Apply the provenance rule,
  re-check every redirect hop's host, and bound distinct fetches per
  session. Using Google Search grounding as the independent index is
  unverified.
- **Size.** M.

### 22. g-AMIE: physician-centred oversight

- **Sources.** David Stutz (Google DeepMind) and Natalie Harris (Google
  Research), blog 2025-08-12. Paper arXiv 2507.15743, read to 100k of 265k
  characters.
- **What it teaches.**
  - The agent hands over a draft. The reviewer sees it beside the
    transcript, edits any section, and signs off or requests a follow-up.
  - About 40% of sections needed edits.
  - Oversight took about 60% of a full consultation's time.
  - Verbose drafts lengthened review.
- **What the skills say now.** Approve or reject only
  (`human-review.md:40-47`); the approval card has Deny and Approve only
  (`agent-ui-states.md:17`, `DESIGN.md:618`).
- **What a coding agent would do differently.**
  - Add "approved with edits": on ADK 2.12.0 the edit returns through
    `tool_confirmation.payload` (`:111-113`), is re-validated, and gets a new
    payload digest.
  - Add "follow-up requested".
  - Record a per-field edit rate.
  - Keep review drafts short.
- **Caveat.** Health domain.
- **Size.** M.

### 23. GDPval

- **Source.** Patwardhan and others, OpenAI, arXiv 2510.04374. The last
  roughly 6k characters were not read.
- **What it teaches.**
  - Expected time = model time + review time + (1 − w) × human time, where w
    is the rate at which experts preferred the model's output.
  - Naive speed-ups of 90–327× fall to about 0.87–1.39× once review and
    redo are counted.
- **What the skills say now.** Discovery and the value report ask for
  acceptance rates (`value-report.md:59-65`) but never add review time.
- **Size.** M.
- **Not imported.** Facts about OpenAI's models; only the method.

### 24. Long-running ADK agents that pause and resume

- **Source.** Shubham Saboo and Eric Dong, Google Developers Blog,
  2026-05-12.
- **What it teaches.**
  - `current_step` and `pending_signals` in state, seeded by a
    `before_agent_callback`.
  - A webhook calls `run_async` with a `state_delta`, so the container can
    scale to zero between steps.
  - Golden cases pre-seed state to simulate a 48-hour gap; a pause-gate case
    asserts no tool call.
- **What the skills say now.** Only `RequestInput` and the Pub/Sub ambient
  agent are covered (`orchestration.md:164-194`).
- **Keep the skill's stricter rules.**
  - The article's "automatic checkpoint" claim is weaker than `runtime.md:56-60`.
  - The article ignores duplicate webhooks; keep the redelivery rule.
- **Size.** M.

### 25. Effective harnesses for long-running agents

- **Source.** Justin Young, Anthropic, 2025-11-26.
- **What it teaches.**
  - An initialiser writes a JSON feature list and a progress log.
  - Each session reads them, runs a health check, and works on exactly one
    item.
  - Only the pass field may change.
  - No quantitative results.
- **ADK restatement** (for the application's own runs, not the engineer's
  plan): a ledger whose criteria cannot change; status changed through an
  evidence-checking tool; a health check on resume; one item per
  invocation.
- **Size.** M. Best written into the same section as 24.

### 26–61. Tier 2 and tier 3 entries

The table rows above carry the scout findings for these; the full notes are
in the session scratchpad and go to each article agent.

Points that bear on how they are integrated:

- **27 (GPT-5.1 metaprompting).** It recommends concrete length limits; 5
  showed such a limit cost 3%. Integrate 27 after 5, so that length limits
  stay a measured change.
- **28, 29, 48, 49.** These come from older or mixed model generations
  (PaLM 2, Gemini 1.5, Gemma). Their numbers are recorded as the source's,
  to be re-measured on the pinned model.
- **38 and 14.** Both were read from unofficial mirrors.
- **44.** Co-branded and promotional. Only its three mechanisms are imported.
- **55.** Its config keys must be checked against installed ADK source before
  they are written into a skill.
- **58, 59 (Schmid).** Affiliation comes from speaker bios, not the posts.
- **61.** Older (2024); only the circuit breaker is new.

## Already cited, not re-read

These articles were cited before this programme (from the Phase 0 grep);
none was proposed again:

- **Anthropic.** "Building effective agents", "Writing tools for agents",
  "Effective context engineering for AI agents", "Demystifying evals for AI
  agents", "How we built our multi-agent research system", "Code execution
  with MCP", "Claude Code auto mode", "Measuring agent autonomy", "Prompt
  injection defenses".
- **OpenAI.**
  - Guides: "A practical guide to building agents"; "Identifying and
    scaling AI use cases".
  - Developer documentation: evaluation best practices, function calling and
    structured outputs.
  - Developer blog: "Testing Agent Skills Systematically with Evals".
  - Prompting guides: the GPT-5 and GPT-4.1 guides.
  - Codex and Apps SDK documentation.
- **Google.**
  - Google Cloud blog: "Where to use sub-agents versus agents as tools",
    "Five guides to building and scaling production-ready AI agents", the
    Agent Factory security recap, the AI adoption framework, and Agent
    Sandbox on GKE.
  - Google Developers Blog: "Architecting efficient context-aware
    multi-agent framework for production", "Scaling AI agent infrastructure
    with the MCP stateless updates", "Three layers, one repo: a tour of
    google/adk-recipes", and agent and model evaluations GA.
  - Google Research: "An introduction to Google's approach for secure AI
    agents" and the HEART metrics paper.
  - Google Cloud Community on Medium: context compaction and context caching.
- **arXiv.** 2207.08815, 2307.03172, 2403.14720, 2404.12272, 2405.00623,
  2406.16964, 2408.15066, 2501.01303, 2502.01390, 2502.08554, 2502.11830,
  2503.18813, 2505.18215, 2509.18361, 2602.11988, 2602.12670, 2604.06183.

## Needs paste, not assessed

openai.com returned 403 to the fetch tool, and Kaggle whitepaper pages render
no text. Nothing below has been read, so nothing below is described beyond its
title. Paste any you want assessed. The scouts flagged the first four as
likely to matter.

| Article | Org | Date | Lane it would join |
| --- | --- | --- | --- |
| "Sycophancy in GPT-4o" and "Expanding on what we missed with sycophancy" | OpenAI | 2025-04-29, 2025-05-02 | release gates, feedback capture |
| "Inside our in-house data agent" | OpenAI | 2026-01-29 | SQL agents |
| "Designing AI agents to resist prompt injection" | OpenAI | 2026-03-11 | security |
| "How we monitor internal coding agents for misalignment" | OpenAI | 2026-03 | observability |
| "Running Codex safely at OpenAI" | OpenAI | 2026-05-08 | security |
| "Continuously hardening ChatGPT Atlas against prompt injection attacks" | OpenAI | 2025-12-22 | security (may be training-only) |
| "Harness engineering" | OpenAI | — | workflow |
| "Unrolling the Codex agent loop" (Michael Bolin) | OpenAI | 2026-01-23 | tools, caching |
| "How evals drive the next chapter in AI for businesses" | OpenAI | 2025-11-19 | field delivery |
| "How enterprises are scaling AI" | OpenAI | 2026-05-11 | field delivery |
| "AI in the Enterprise" (PDF; text could not be extracted) | OpenAI | 2025-04 | field delivery |
| "Introduction to Agents", "Prototype to Production", "Agent Quality", "Agents Companion" (Kaggle whitepapers) | Google | 2025 | architecture, release, evaluation |
| Colin Jarvis talks on forward-deployed engineering (transcript needed) | OpenAI | — | field delivery |
| Anthropic Applied AI talk on context engineering and memory (transcript needed) | Anthropic | 2026 | memory |

## Rejected

Each with its reason. Several were found by more than one lane.

- **Already covered by the skills.**
  - "Developer's guide to multi-agent patterns in ADK" (Saboo).
  - Agent Factory recap on evaluation and multi-agent systems.
  - Google layered prompt-injection defence (blog.google, 2025-06): also
    already cited.
  - Google Workspace continuous mitigation of indirect prompt injection.
  - "How to build AI agents with Google-managed MCP servers".
  - "Dev Signal Part 1: Tools".
  - Quartly's A2A tutorial.
  - "Equipping agents for the real world with Agent Skills".
  - "Optimizing RAG retrieval: test, tune, succeed".
  - "Remember this: agent state and memory with ADK".
  - OpenAI's "Short-term memory management with sessions" cookbook.
  - "Building resilient prompts using an evaluation flywheel".
  - "From vibe checks to continuous evaluation": its one new point is folded
    into 4.
- **Superseded by its own update.** "The 'think' tool" (Anthropic,
  2025-03-20).
- **Conceptual, opinion or no mechanism.**
  - "Intelligent AI Delegation", and "How agents can delegate better".
  - "Building collaborative AI".
  - The business-forecasting multi-agent post.
  - "Beyond the pilot: five hard-won lessons": its proxy-metric advice also
    conflicts with the presenter's no-vanity-metrics rule.
  - "Agent Security is a Systems Problem".
  - Google's agentic privacy research agenda.
  - "Our framework for developing safe and trustworthy agents".
  - "Building connected agents with MCP and A2A".
  - "Beyond static prompts".
  - "A methodical approach to agent evaluation": its letter grades also
    conflict with critical-rule gating.
  - ROI-of-AI surveys and trend reports.
  - "From experiments to deployments" (OpenAI PDF): mostly an operating
    model that overlaps the cited use-case guide.
- **Product launches.**
  - "Introducing A2UI".
  - "Introducing QueryData".
  - BigQuery Agent Analytics launch.
  - Memory Bank preview.
  - The Interactions API post.
  - "Improving structured outputs in the Gemini API".
  - "Mastering controlled generation with Gemini 1.5".
  - OpenAI Structured Outputs launch.
  - Desktop Extensions.
  - "Agent Factory: GKE Agent Sandbox and Pod Snapshots".
- **Another vendor's API, or no author or date.**
  - OpenAI "Safety in building agents" documentation. Its idea is real and
    uncovered; see "Found along the way".
  - OpenAI "Reasoning best practices".
  - The o3/o4-mini function-calling guide.
  - The MCP tool guide.
  - GPT-5 new parameters and tools.
  - "Building governed AI agents".
  - "Self-evolving agents": its lenient pass rule also conflicts with the
    skills' critical-failure rule.
  - "Optimizing customer support agents for cost and quality".
  - "Build an agent improvement loop with traces, evals and Codex".
  - The GPT-5.4 vision tips: mostly vendor parameters.
  - "Run long horizon tasks with Codex", and the PLANS.md cookbook.
- **Needs training, not an application change.**
  - CHASE-SQL's fine-tuned selector.
  - arXiv 2605.14443.
  - "Language model cascades": needs model internals.
  - Speculative cascades.
- **Not read in full or only secondary sources.** Not described.
  - Self-consistency (2023): abstract only.
  - "Logprobs on Vertex AI": deferred; logprobs are reported missing on
    Gemini 3.x, so check availability first.
  - Chain of Agents.
  - OPRO.
  - Bloom.
  - "AI Agent Traps".
  - Project Vend.
  - Anthropic Interviewer.
  - "Designing AI-resistant technical evaluations".
  - "Inference scaling for long-context RAG".
  - The Gemini-SQL2 reports.
  - The Google RCT on developer speed: abstract only, and already covered by
    `speech.md:90`.
- **Older and not the reference others cite.**
  - The PAIR "Building the plane while flying it" case study (2024, nothing
    measured).
  - Google's "Prompt Engineering" whitepaper (read from a mirror): its
    sampling defaults contradict current Gemini 3 guidance.
- **Affiliation not Google, Anthropic or OpenAI.**
  - Text-to-SQL tutorials by a Google Developer Expert and partners.
  - Tool-retrieval and benchmark papers without these affiliations.
  - "Structure Tax".
  - "Silent Egress".
  - The CHI papers on confirmation frequency.
  - "15 lessons building ChatGPT Apps" (Alpic).
  - gepa-adk.
  - Loop-cost write-ups.
- **Coding-assistant harnesses, not ADK applications.**
  - "Building a C compiler with a team of parallel Claudes".
  - "Claude Code: best practices for agentic coding".
  - "Scaling agentic coding across your organization".
- **Covered by a kept item.** Philipp Schmid, "Recursive Self-Improvement",
  covered by 4.

## Decisions after the plan

28 October 2026: the user confirmed that Omran and Dixit both work at Google,
pasted the seed article, and chose to paste the remaining articles one at a
time, so part two integrates each article as it is pasted rather than working
through a pre-approved list.

## Found along the way (not from an eligible article)

- **Garbled sentence (fixed 28 October 2026).**
  `optimise-adk-on-google-cloud/references/context-window.md:259` read "It
  which is the just-in-time identifier"; it now reads "This is the
  just-in-time identifier pattern".
- **Untrusted text in templated instructions (fixed 28 October 2026).** A
  `{key}` placeholder in a string instruction puts whatever is in state into
  the instruction; in google-adk 2.8.0 both `instruction` and
  `global_instruction` go through `inject_session_state` and
  `append_instructions` (`flows/llm_flows/instructions.py`, checked
  28 October 2026). adk-agent-security `injection-patterns.md` now has
  "State placeholders are prompt text too", and
  `adk-agent-instructions/references/adk-instruction-mechanics.md` points to
  it. Made as an ordinary change from the source, not an article import.
- **Schema order versus the reason field.** The `Decision` example
  (`output-contracts.md:42-46`) puts `status` before `reason`, while line 30
  says the model generates properties in schema order. The scout's evidence
  came from an ineligible paper. Worth a separate, measured decision.

## Conflicts to settle during part two

- **Tool masking versus tool search (13).** "Mask rather than add or remove
  tools mid-task" (`context-window.md:136`) against dynamic `get_tools`.
  Proposal: decide by measured cache hits and declaration bytes; both skills
  name the trade-off.
- **Bind tool names versus describe actions (14).** Proposal: stable
  FunctionTools keep bound names and the linter; MCP and dynamic toolsets
  describe actions.
- **Length limits in prompts (27 against 5).** Proposal: a length limit is a
  measured change, run on every model that receives the prompt.
- **Durability claims (24).** Keep `runtime.md:56-60` and the redelivery
  rule over the article's wording.
