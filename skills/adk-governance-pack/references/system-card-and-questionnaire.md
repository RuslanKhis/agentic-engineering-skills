# System card and security questionnaire

Read when writing the system card or the questionnaire answer bank. Both
describe one build to outsiders, so both use the plan's evidence vocabulary
and nothing warmer.

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
| Model provider data use and sub-processors | The DPIA input pack's provider section (one home; cite it) |
| Prompt injection and agency | SB17, SB18, the security-posture table, the adversarial suite's results |
| Output handling | SB10 |
| Abuse and cost | SB19, SB25, the cost contract |
| Vulnerability management | SB15, SB21, SB22–SB24 |
| Sensitive data | `protect-adk-sensitive-data` evidence with measured detector coverage |
| Certifications | The cloud provider's own reports, cited with a date; the application has none unless the client certified it |

Cite a certification from the provider's compliance page or the report the
client holds, with the date; when neither can be read, the answer is a
`gap:` for the client's vendor-risk team, not a remembered list.
A cloud provider's certification covers its infrastructure, not the
client's application: write "hosted on Google Cloud, which holds <report>
(source: <page>, <date>)", never "the system is ISO 27001 certified".
A rule marked Defer or a deferred SB row is answered "deferred" with its
trigger, which reviewers usually accept for a pilot and query for
production.
