# Semantic contracts and collected context

Read this when defining a metric, resolving business values, changing schema
collection, or diagnosing plausible SQL with wrong answers. The examples are
adaptable offline recipes, not additional companion features. Historical evidence
is identified explicitly; [compatibility.md](compatibility.md) records its scope.

## 1. Write the meaning before choosing SQL

Record the following decisions for each reviewed operation or generated-question
acceptance case. Reuse an existing approved definition when one exists.

| Contract field | Decision that SQL cannot safely invent |
| --- | --- |
| Metric and units | Amount, count, rate or average; currency, scale and conversion rule |
| Population | Eligible entities/events, exclusions and treatment of pending outcomes |
| Output grain | One row per customer, contract, decision, period or cohort |
| Denominator | Decisions, distinct clients, all eligible clients or active clients |
| Relationships | Approved paths, key uniqueness, cardinality and orphan-row treatment |
| Time meaning | Event date, effective date, current state or historical state |
| Window | Inclusive start, exclusive end, reporting timezone and timestamp conversion |
| Nulls and zeros | Missing measurement, no activity and unknown state are distinct |
| Exactness | Exact aggregation or a specifically approved approximation/error bound |
| Ranking | Selection metric, top-N scope, tie rule and presentation order |
| Output | Every requested metric, permitted dimensions and empty-result behaviour |

Changing any of these can require a different template or clarification. For
example, a current `is_active` flag cannot establish whether a client was active
during a past quarter. A decision-based renewal rate and a client-cohort comparison
can disagree without either SQL statement being syntactically wrong.

Currency labels are part of meaning: reporting an AUD amount as USD requires an
approved exchange-rate source, effective date and rounding policy. Preserve
decimal values through calculation and serialisation; a float conversion can
destroy the precision that an exact result checker expects. An approximate
distinct count is a different contract from an exact count.

**Completion criterion:** the expected answer, eligibility rules and unresolved
questions can be written without depending on the model's proposed SQL. If the
business owner has not supplied a necessary decision, prepare independent work
and ask for that decision before executing the ambiguous interpretation.

## 2. Establish dates and grain with an adversarial fixture

The following small fixture illustrates a client-cohort contract. It uses generic
logical names; adapt types and binding syntax to the target database.

- Window: `2026-04-01 <= reporting_date < 2026-07-01`.
- Eligibility: a client dimension row plus exactly one final renewal decision in
  the window. Final means `Renewed` or `Churned`; pending-only clients are excluded.
- Grain: one eligible client before the final cohort aggregation.
- Metric: tickets created in the same window, retaining eligible zero-ticket clients.
- The current active flag is irrelevant to this particular contract.

| Client dimension | Current active | Q2 renewal |
| --- | --- | --- |
| A | false | Renewed, 10 May |
| B | true | Renewed, 20 May |
| C | true | Churned, 1 June |
| D | true | Pending, 15 June |

Create three in-window tickets for A, zero for B, three for C and two for D.
Put one of A's three tickets exactly on 1 April. Add an extra A ticket on
31 March and another on 1 July; these two are outside the window.

The expected result is fixed before authoring:

| Cohort | Clients | Tickets | Tickets per client |
| --- | ---: | ---: | ---: |
| Churned | 1 | 3 | 3 |
| Renewed | 2 | 3 | 1.5 |

Build one ticket-count row per client, establish one final outcome per eligible
client, join through the approved relationship, then aggregate by cohort. Use the
eligible-client population as the denominator, including B's zero. Retaining D
would violate the population rule; excluding A because its current flag is false
would introduce an unrequested historical interpretation.

Apply each mutation independently, starting again from the baseline:

| Mutation | Required observation |
| --- | --- |
| Add a fourth in-window ticket for A | Renewed = 2 clients, 4 tickets, average 2 |
| Remove all A tickets in the window | Renewed = 2 clients, 0 tickets, average 0 |
| Add a second final renewal for A | One-final-decision invariant fails before relying on cohort SQL |
| Duplicate A's dimension row | Dimension-key uniqueness fails; totals must not silently double |
| Add a ticket on the exclusive endpoint | Cohort totals remain unchanged |
| Add an eligible final renewal for a missing client | Follow the explicit orphan policy; the stated fixture contract excludes it |

The repeated-renewal case also distinguishes metrics. Under a separately approved
decision-based definition, adding another `Renewed` decision changes the renewal
rate from `2/3` to `3/4`; it does not establish a new client-cohort policy. Choosing
the latest decision needs an effective timestamp and a reviewed tie rule. A
lexicographically greatest status or arbitrary identifier is insufficient.

For timestamp facts, derive local boundaries as offset-aware instants. In
Australia/Sydney, Q2 2026 begins at `2026-03-31T13:00:00Z` and ends at
`2026-06-30T14:00:00Z`; the offsets differ because daylight saving changes.
Use the timezone database to derive both endpoints. For a source `DATE`, document
how ingestion converted timestamps to dates; the query cannot reconstruct that
meaning from the column type alone. Test exact endpoints and immediately adjacent
instants. Add today/future rows when implementing a completed-day rolling window.

**Historical observation:** the companion's Q2 fixture checks the same aggregate
values shown above, but its verifier does not enforce a general one-final-decision
invariant. Its reviewed rolling template has only a lower date bound and no
secondary tie key. These stronger tests require coordinated contract/code changes;
they are not established by those historical fixture results.

## 3. Test relationships independently of equal totals

An outcome oracle and a relationship policy answer different questions. A tiny
dataset may produce identical rows for a dimension-to-fact join and a direct
fact-to-fact shortcut, even when only the former is approved.

For each supported question, record required and forbidden relationship paths,
then check the actual candidate against the implemented join policy. Add orphan
facts and duplicated dimension keys to expose accidental equivalence. An inner
join on an arbitrary condition does not become approved merely because a cross
join guard accepts it. If relationship enforcement is absent, report that gap
separately from numerical correctness.

**Historical limitation:** the companion's offline candidate and fixture verifier
join renewal and ticket facts directly, while its semantic map lists relationships
through the client dimension. Their passing totals demonstrate fixture arithmetic,
not comprehensive adherence to the authored join map. Treat copied examples as
evidence for their stated scope; approve any shortcut explicitly in a new target.

## 4. Ground a value within its approved field

Use a key such as `(domain, table, column)` to select the permitted value source.
Require the table to be selected and authorised before consulting that source.
Give the router compact identifiers for fields it can request, rather than
requiring it to guess where value grounding is available.

| Input or condition | Resolution and downstream transition |
| --- | --- |
| Exact canonical value or one approved alias | `OK`: carry one canonical value to authoring |
| Approved ticket alias `unresolved` | `Open`, if that mapping belongs to this field |
| `unpaid` with only `paid` approved | Unresolved; do not extract the embedded substring |
| Approved renewal alias `did not renew` | `Churned`, under that explicit business mapping |
| Unapproved `not renewed` or competing canonical matches | Clarification before schema retrieval or authoring |
| Misspelling with fuzzy suggestions | Clarification; suggestions are not accepted values |
| Unknown field or field on an unselected table | Reject selection before lookup, metadata or SQL |
| Excessive lookup requests or unavailable value source | Controlled refusal/error with no author or query calls |

Bound both raw request counts and value sizes, including duplicate requests that
would otherwise disappear during deduplication. Choose limits for the target;
the companion used at most eight value requests, not a universal required limit.

When compiling aliases, normalise consistently and invert the mapping. If one
normalised phrase belongs to two canonical values, reject that catalogue revision
or retain an explicit ambiguity set. A dictionary assignment that overwrites an
earlier mapping would hide the collision. Test whitespace/case, word boundaries,
approved negative aliases, remaining negation and contradictory phrases.

**Historical observation:** the companion accepts a single approved phrase within
a longer input, with word boundaries and negation checks; it is not an exact-only
resolver or a general Boolean-language interpreter. An exact-whole-input policy
is a possible stricter adaptation. Dynamic dimension/search services are extensions:
bound their scans and returned candidates, preserve caller scope, and define
freshness. Arbitrary sample rows neither cover the value domain nor grant access.

## 5. Forward a collected-context contract

This illustrative SQLite envelope shows responsibilities, not mandatory field
names. Preserve the target's existing interfaces. Trusted application code owns
the original question, authorisation and reporting interpretation.

```json
{
  "status": "READY",
  "original_question": "Count closed tickets in Q2 2026",
  "domain": "support",
  "selected_tables": ["tickets"],
  "dialect": "sqlite",
  "schemas": {
    "tickets": {
      "physical_name": "tickets",
      "grain": "one ticket",
      "columns": [
        {"name": "ticket_id", "type": "TEXT", "nullable": false},
        {"name": "ticket_created_date", "type": "DATE", "nullable": false},
        {"name": "ticket_status", "type": "TEXT", "nullable": true}
      ]
    }
  },
  "resolved_values": [
    {"table": "tickets", "column": "ticket_status", "canonical": "Resolved"}
  ],
  "reporting_window": {"start": "2026-04-01", "end_exclusive": "2026-07-01"},
  "reporting_timezone": "Australia/Sydney",
  "approved_relationships": [],
  "correctness_rules": ["Exact ticket count", "Bind categorical and date values"]
}
```

Resolve values first. Then validate that every selected schema arrived with the
required names/types, and forward exact retrieved metadata without a model-written
summary. Keep trusted selection/schema records independently of the author's copy;
the execution boundary compares SQL with those records. Treat descriptions as data.
Where supplied by the provider, retain field modes, descriptions, physical paths
and partition requirements. Mark unavailable provenance as unknown rather than
inventing a schema version or source-freshness watermark.

**Production extension:** nested RECORD/STRUCT and repeated fields require recursive
child metadata and approved path/cardinality rules. A top-level `RECORD` type is
insufficient to author a nested-field query. Either preserve the necessary children
and test their scope, or reject that unsupported surface. Test a removed child,
changed type and repeated-field expansion; compare reviewed metadata with deployed
views, and invalidate scoped caches when schema or permissions change.

**Completion criterion:** public-path tests prove selected-schema-only retrieval,
exact metadata delivery, bounded field lookup, and zero author/query calls for
unresolved values or failed/incomplete metadata. The companion's changed-description
sentinel establishes fresh metadata delivery; it does not establish column-drift,
nested-schema support or cache invalidation. Keep those claims separate.
