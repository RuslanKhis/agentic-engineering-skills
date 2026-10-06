# Exemplars as data

Read this when adding, trimming or reordering few-shot examples in an
instruction. Leave-one-out selection for development cases and the measured
loop live in adk-agent-evaluation's quality-iteration reference; this
reference covers what makes an exemplar set sound and how to keep it as data.

## What the evidence says

Few-shot behaviour is sensitive to choice, order and format. Independent
studies summarised by Lilian Weng (2023-03-15,
[link](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/))
found that "choice of prompt format, training examples, and the order of the
examples can lead to dramatically different performance, from near random
guess to near SoTA" (Zhao et al. 2021), that permutation variance does not
shrink with model size or example count (Lu et al. 2021/2022), and that
majority-label and recency bias skew predictions toward frequent and
last-seen labels; selecting semantically similar examples helps (Liu et al.
2021). These are independent evidence on older models; re-measure on the
pinned model.

Vendors disagree on count: Anthropic suggests three to five diverse,
relevant examples (prompting best practices, vendor guidance); Eugene Yan
argues for a dozen or more in production prompts
([link](https://eugeneyan.com/writing/prompting/), practitioner). Treat the
count as an experiment variable on the development set.

## Selection rules

- **Few and canonical.** Each exemplar shows one shape the output must take.
  Two exemplars that teach the same thing cost tokens and bias the label
  distribution.
- **Diverse across labels and situations.** Balance the outcomes so the set
  does not teach "the answer is usually approve".
- **Structurally identical.** Same delimiters, same field order, same length
  class as the required output. The model copies structure before content.
- **Never the case's own label.** A development case never sees its own
  answer; adk-agent-evaluation's `exemplars_for` helper selects from other
  cases.
- **Trimmed to the parts whose shape matters.** Shorten case-specific facts;
  keep the reasoning structure and the output format.
- **Ordered deliberately.** Random or deliberately balanced order avoids
  recency bias; record the order as part of the prompt version.

## Keep exemplars as data with stable IDs

Store exemplars outside the prose, one file each, and render them into the
instruction through the loader (see [prompt as code](prompt-as-code.md)):

```json
{
  "id": "ex-refund-002",
  "purpose": "refund refused because the order is outside the window",
  "input": "Order 1234 from 14 months ago, customer asks for a refund.",
  "output": {"decision": "refuse", "reason": "outside the 12-month window", "next_step": "offer store credit"},
  "source_case": "dev-017",
  "added": "2026-10-06"
}
```

Stable IDs let an evaluation run record which exemplars were in the prompt,
let error analysis attribute a bias to a specific example, and let a review
remove one without rewriting prose. `source_case` keeps the leave-one-out
check mechanical: the loader excludes any exemplar whose `source_case`
matches the case under evaluation.

Where a library of standard outputs exists (conditions, templates, canned
answers), supply it as data with IDs and let the model select and adapt
instead of writing it into the prompt.

## Observable checks

- A contract test renders the instruction with the exemplar set and asserts
  the count, that no two exemplars share a `purpose`, and that each exemplar
  parses against the output schema.
- The evaluation run records exemplar IDs with the prompt version.
- Removing an exemplar is one change per iteration; its effect shows in the
  category counts, not in a reviewer's impression.

Completion: the exemplar set is small, balanced and recorded by ID; the
development run with the set beats the run without it on the targeted
category and does not worsen the others.
