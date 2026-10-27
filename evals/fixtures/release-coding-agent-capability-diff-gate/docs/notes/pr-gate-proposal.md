# Gate for agent-authored PRs (proposal, Lena, 2026-10-23)

Most PRs are now opened by coding agents. Last week one PR added the weekly
reporting agent, which emails refund data, and nobody noticed it in review
until after merge.

Proposal from the platform channel: add `agents-shipgate diff --application`
(1.2.0) to CI against `main` and block the PR when it reports a change. Is that
enough on its own?
