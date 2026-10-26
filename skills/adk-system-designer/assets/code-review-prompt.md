# Independent plan-versus-code review

Give this to a reviewer with a fresh context before a phase review: a
subagent where the host supports one, otherwise a new session the user
starts. The reviewer did not write the code or the tickets. Replace the
paths and the base commit before sending.

```text
Review whether the code still does what a plan's records say. Read the
design <design path>, the plan <plan path> and the tickets <tickets dir>, then
the code changed since <base commit> (git diff <base commit>..HEAD) and the
tests each acceptance item cites. Do not edit any file, run anything that
writes, or tick any box. A ticked box or a passing command is a claim, not
evidence: read the code and the test behind it.

For every contract the phase evidenced, and every contract a ticket withdrew:

1. Missing: the contract or acceptance item has no code or no test behind it.
2. Partial: the code or the test covers less than the contract says (a test
   that only reads the instruction text, a skipped test, one path of several).
3. Contradicting: the code does the opposite (a later commit undid it, a
   withdrawn tool or sub-agent is still bound, a scope is still granted).
4. Unrequested: code no ticket asked for, especially anything that widens
   identity, data access or what the agent can do.

Also list manual verification items marked confirmed without a named person
and a date, and evidence that a check ran where it could not have (a test
that cannot import, a command for code that does not exist).

Grade each finding CRITICAL (a contract or security rule is broken or a
withdrawn capability is reachable), WARNING (evidence is weaker than claimed)
or SUGGESTION. Report a check you could not perform as not verified, never as
passed. Return a table: finding, grade, class, evidence (file:line and
commit), and the contract or acceptance item it concerns.
```

The findings go on the next checkpoint's agenda; none is fixed during the
review. A CRITICAL finding keeps the phase open.
