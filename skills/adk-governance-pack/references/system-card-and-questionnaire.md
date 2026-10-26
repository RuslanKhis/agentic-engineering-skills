# System card and security questionnaire

<!-- verified: 2026-10-26; re-check every 180 days -->

Read when writing the system card or the questionnaire answer bank. Both
describe one build to outsiders, so both use the plan's evidence vocabulary
and nothing warmer.

Sources: the status vocabulary is this toolkit's own. The legal duties
named below were read on 26 October 2026 at the sources listed in
[Australia](australia.md), [United States](united-states.md),
[EU AI Act](eu-ai-act.md), [privacy and records](privacy-and-records.md) and
[United Kingdom](united-kingdom.md); cite those references' dates, not this
file.

## Status words

Every capability or control is one of:

| Word | Means | Cite |
| --- | --- | --- |
| in place | Evidence recorded at local, live or release tier | The contract or rule ID and the goal's acceptance (`C2 evidenced, local, G01/A3`) |
| planned | A goal will build or prove it | The goal ID |
| deferred | Waits for a trigger in the design | `deferred: <trigger>` |
| n/a | The component does not exist | `n/a: <reason>` |
| gap | Nothing enforces it | `gap: <what is missing>` and the proposed goal |

Write the tier: a control evidenced only offline or locally is "in place,
tested locally", not "in production". A questionnaire answers for the build
named in its front matter; a later build needs a new pass.

## System card

- **Intended use** comes from the requirements and contracts, in the
  client's words. **Out-of-scope use** lists what the design excludes and
  the reasonably foreseeable misuse with the control that limits it; a
  misuse with no control is a gap.
- **Limits** come from evaluation results, incident records and the failure
  review, not from general statements about language models.
- **Evaluation results** cite measurement records (`M1`) and evaluation
  reports by path, with sample, window and build. A measure planned but not
  run says "not yet measured" and names the goal. Never round a result into
  a better one or drop the counter-metric.
- **Human oversight** names the review points, the share of outputs a
  person sees (an M record when measured), how someone contests an output,
  and who can stop the system.
- **Contact** is confirmed by the client; cite who confirmed it and when.
  In the UK it also names the route for data protection complaints (DPA
  2018 s 164A).
- **Automated-decision disclosure** is the plain-language information the
  client's privacy policy, notices and explanations draw on. One block
  serves every regime in scope: the APP 1.8 entries (kinds of personal
  information, decisions made solely by the program, decisions it does
  something substantially and directly related to; from 10 December 2026,
  checked 2026-10-26), which the OAIC expects vendors to supply as "clear,
  high-level information"; GDPR Articles 13(2)(f), 14(2)(g) and 15(1)(h)
  meaningful information about the logic and the explanation the design can
  produce, and the Article 22(3) human intervention route; UK Article 22C
  information, representations, human intervention and contest; and the
  facts for California's ADMT pre-use notice (purpose, logic, opt-out or
  appeal, alternative process) and Colorado's adverse-outcome explanation.
  The card supplies facts; the client writes the notices. Write `n/a:` with
  the reason when no output decides or feeds a decision about a person.
- **AI disclosure and hand-off** records when and how the agent says it is
  an AI, how it answers "are you a human?", and, for an agent acting for
  someone, on whose behalf (EU AI Act Article 50(1) and the Commission's
  July 2026 guidelines; Utah on request; California AB 1609 for large
  businesses from 1 January 2027, checked 2026-10-26, with a good-faith
  connection to a human within 15 minutes; the OAIC's recommendation; the
  CMA's AI-agent guidance). Record the hand-off route and its measured time
  as an M record. A persona, memory of the user or relationship features can
  bring companion chatbot laws in: record the disclosure cadence and the
  self-harm protocol. Every public capability or accuracy claim the client
  will make cites an M record (FTC Section 5; Australian Consumer Law ss 18
  and 29).

`adk-presenter` may cite the system card in a technical or production
deck; keep its figures identical to the plan's M records so the two never
disagree.

## Security questionnaire answer bank

Client questionnaires (vendor risk, CAIQ-style, SIG-style or their own)
ask the same questions in different words. Answer each topic once in the
bank from the design's contracts and security baseline, then paste.

| Topic | Draw the answer from |
| --- | --- |
| Identity and access | SB01–SB04, SB20 and the identity contracts |
| Secrets | SB16 and credential decisions |
| Logging and retention | SB14, retention contracts, observability decisions |
| Model provider data use and sub-processors | The privacy impact input pack's provider section (one home; cite it) |
| Prompt injection and agency | SB17, SB18, the security-posture table, the adversarial suite's results |
| Output handling | SB10 |
| Abuse and cost | SB19, SB25, the cost contract |
| Vulnerability management | SB15, SB21, SB22–SB24 |
| Sensitive data | `protect-adk-sensitive-data` evidence with measured detector coverage |
| Certifications | The cloud provider's own reports, cited with a date; the application has none unless the client certified it |
| Overseas access | The input pack's recipients table and the transfer assessment annex |
| Incident notification | The clocks of the regimes in scope (below), and the contract flow-down from the agency to the client |
| AI security baseline | For UK clients who ask, the DSIT Code of Practice for the Cyber Security of AI mapped principle by principle to SB and C IDs |

Incident notification clocks to list, only for the regimes in scope (read
26 October 2026; see the regime references): the agency notifies the client
without undue delay under its contract; GDPR and UK GDPR, 72 hours to the
authority; Australia, an eligible data breach assessed within 30 days and
notified to the OAIC and individuals as soon as practicable, APRA CPS 234
material incidents within 72 hours, and a ransomware payment reported within
72 hours under the Cyber Security Act 2024; United States, the GLBA
Safeguards Rule's 30-day FTC notice for financial institutions; EU NIS2 24
and 72 hours when the client is in scope, the Cyber Resilience Act 24 and
72 hours when a product is made available on the market, and AI Act Article
73 for high-risk providers. For a NSW agency, the agency contains an
eligible data breach immediately, assesses it within 30 days and notifies
the Privacy Commissioner immediately (PPIP Act Part 6A), cyber incidents go
to Cyber Security NSW within 24 hours of detection and classification, and
ICTA asks the supplier for immediate notice then details within 48 hours.
New Zealand: the Privacy Commissioner as soon as practicable (the OPC asks
for 72 hours). Singapore: the data intermediary tells the client without
undue delay, and the client notifies the PDPC within 3 calendar days of
determining a breach notifiable; MAS-regulated clients notify MAS within 1
hour. Canada: PIPEDA as soon as feasible, with a 24-month record of every
breach; Quebec, the CAI and an incident register; Alberta, without
unreasonable delay; BC, none. Which entity notifies is `counsel:`.

For government clients, the questionnaire's "Government security policy"
row names the policy the system is measured against: the NSW Cyber Security
Policy (Essential Eight Maturity Level One baseline) for NSW agencies, the
agency's ISM and PSPF direction for Commonwealth agencies, NZISM
certification and accreditation for the New Zealand public service.

Cite a certification from the provider's compliance page or the report the
client holds, with the date; when neither can be read, the answer is a
`gap:` for the client's vendor-risk team, not a remembered list.
A cloud provider's certification covers its infrastructure, not the
client's application: write "hosted on Google Cloud, which holds <report>
(source: <page>, <date>)", never "the system is ISO 27001 certified".
A rule marked Defer or a deferred SB row is answered "deferred" with its
trigger, which reviewers usually accept for a pilot and query for
production.
