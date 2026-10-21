# Case study: a public story built from recorded results

Read for the `case-study` stage: a public write-up of a finished agent
project, often shared with Google for co-marketing. It reuses the evidence
every other stage uses and adds two things the other stages do not need: an
approval trail for every sentence and Google's brand rules. Sources were read
on 15 October 2026 and are cited with URLs in the repository's research note
`docs/research/case-studies-and-google-programs.md`; re-read a Google page
before quoting a program detail, because programs and portals change.

## What a company may say without asking

Google Cloud's terms (section 9, Publicity) let a customer state publicly
that it is a Google Cloud customer and display brand features according to
the branding guidelines; Google may likewise name the customer in its
promotion. Anything else (the other party's logo, a press release, a blog
post, a talk, a social post about the services) needs the other party's
written consent. Enterprise customers on a negotiated agreement may have
different terms; ask.

The customer co-branding guidelines (PDF, updated April 2026) allow a plain
text mention of Google Cloud and its product names with no approval, and give
the attribution phrases to choose from:

| Phrase | When it applies |
| --- | --- |
| Built on Google Cloud, Developed on Google Cloud | Google Cloud products used, no implementation guidance from Google |
| Built with Google Cloud | Several products, some guidance from Google |
| Built with AI from Google Cloud | Several AI products, not only Gemini |
| Built with Google Gemini | A Gemini model through Vertex AI, AI Studio or open source |

Never: "Powered by" (reserved for co-engineering and needs brand approval),
"with Google Cloud AI", "GCP" or "GC", "a partner of Google Cloud",
"preferred by Google Cloud", "the <Company> Google Cloud solution", or the
Google Cloud name or logo combined with the company's own. Write "Google
Cloud Agent Development Kit (ADK)" on first mention. A headline that names
the customer and carries the attribution phrase as a separate clause
("Acme cuts order entry by half, built with Google Gemini") is plain text;
fusing the names into one brand ("the Acme Google Cloud assistant") is the
combination the guidelines forbid. Use marks as adjectives
with the exact spelling from Google's trademark list (Google Cloud, Gemini,
Vertex AI); ADK is not on that list. Logos go through the company's Google
Cloud contact to the Cloud Brand team; a Partner Advantage member follows the
partner brand guidelines in Partner Marketing Studio instead. The deck check
flags the banned phrases on a `case-study` deck; the rule for the prose
draft is the same.

When a partner or an IT firm holds the Google Cloud account on the
customer's behalf, the contact is that firm's partner manager, both the
customer and the account holder consent to publicity, and the account
holder is named as a partner only in the wording its own agreement allows.

## There is no form; there is a contact

Google's customer stories page has no "share your story" route, and its
customer reference program has no public application. The step is to send a
submission pack to the Google Cloud account team (or the partner manager, or
the startup program contact where enrolled) and ask them to route it to
customer reference marketing and the Cloud Brand team. Say so in the draft's
status line: the pack is an ask, not a submission. What Google asks a
customer to supply, the timeline and selection are not documented; record
them when the contact says.

Other channels reuse the technical half of the story and have documented
rules: a sanitised sample under `contrib/` in `google/adk-recipes` by pull
request with a Google CLA; a post in Google Cloud's Medium publication (writers
added on request); the ADK Agent Directory listed on the community page; a
regional Google Cloud Next speaker call (Next Tokyo published one with a
deadline; the Las Vegas event shows none and customer sessions are arranged
through account teams). Cloud Marketplace is a product-distribution path with
Partner Network membership, an A2A agent card and three reviews, not a story
channel; mention it under "what's next" only when the agent is a product.
Agent Garden shows no contribution path; treat it as Google-only.

## The shape Google publishes, and what to do better

Published Google agent stories share a shape: a headline with the outcome, a
results box of three or four quantified bullets, the challenge, the solution
with named products, one or two quotes with name and title, and a footer of
industry, location and products. They rarely state a baseline or a
measurement method. The draft here keeps the shape and requires more of each
number: baseline, window, sample size, method, data owner, and whether it may
be published as is, as a range, or not at all. A shorter public version is
derived from the full draft, never written first, so every public sentence
has a sourced ancestor.

Projected impact is not a result. If the project has only a plan and a demo,
the honest artefact is an announcement with the hypothesis, not a case study;
say so and offer the production-approval or final-results deck instead.

## Draft, then the pack

The prose draft is the deliverable; a companion `case-study` deck is made
only when the user wants a meeting version, and it is the final-results deck
in public wording. Run the wording lint on the prose with
`check_deck.py --prose <file>`. Use the [case-study template](../assets/case-study-template.md). Each number
cites the plan's evidence line (G ID and acceptance). Each quote is marked
"approved in writing by <name>, <date>" or "draft, not approved". Each
sentence that names a Google product carries the chosen attribution phrase or
a plain-text mention. The diagram is reviewed for secrets, internal hostnames
and customer data before it leaves the repository.

The submission pack lists, with an owner and a date each:

1. The relationship: agreement type, Partner Advantage tier, startup program
   enrolment, and the named Google contact.
2. Internal approvals: executive sponsor, legal, communications, security
   (diagram and data flows).
3. Numbers: baseline, window, sample, method, owner, publishable as is, as
   a range, or omitted.
4. Quotes: text, speaker, title, written approval, media clearance.
5. The diagram, scrubbed.
6. The timeline: start, launch, measurement window, publication target.
7. Attribution language chosen from the approved list, and the wording lint
   passed.
8. Open asks for Google, each marked "requires Google consent": logo use,
   joint announcement, story production, a Next session, Marketplace
   interest.
9. Derived assets the user asks for, with the sentences they reuse: the
   one-page leave-behind by default; a talk proposal (title, 150-word
   abstract, audience, three takeaways, demo plan, speaker bio), a blog
   draft or a sanitised sample with CLA status only when wanted.
10. Contacts: spokesperson, technical lead, marketing owner, Google contact,
    and where the pack was sent.

An interview with the customer sponsor (30 to 60 minutes, questions sent in
advance) fills the gaps the evidence leaves: why the problem mattered, what
changed for people, what they would tell a peer. Generate the questions from
the gaps, not from a generic list.
