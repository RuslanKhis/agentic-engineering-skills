#!/usr/bin/env python3
"""Check governance drafts for citations, jurisdictions, counsel flags and dated legal claims. Standard library only.

A draft is a Markdown file written from one of this skill's templates. It
opens with front matter naming its ``document`` type, ``counsel_required``
(``yes``, ``no`` or ``pending``) and ``jurisdictions``: the regimes the
jurisdiction screen found in scope, as codes in the fixed order ``au``,
``us``, ``eu``, ``uk``, ``nz``, ``sg``, ``ca``. The checker never judges the
law. It reports what a reviewer would otherwise find by hand:

- ``jurisdictions`` missing, empty, out of order or holding an unknown code;
  a regime section (``## Australia: ...``, ``## United States: ...``,
  ``## EU: ...``, ``## United Kingdom: ...``, ``## New Zealand: ...``,
  ``## Singapore: ...``, ``## Canada: ...``) whose code is not listed; records
  of processing without ``eu`` or ``uk``; a transfer assessment without a
  regime that has a transfer rule (``eu``, ``uk``, ``nz``, ``sg``, ``ca``);
  government form answers without ``au``;
- a required section (``##`` heading) that is missing or empty; the required
  set follows ``jurisdictions``;
- a regulatory memo whose jurisdiction screen (or a proof-of-concept note
  whose Classification section) does not name all seven regimes, so a regime
  left out has no recorded reason; a screen written before New Zealand,
  Singapore and Canada were added fails until it gains their rows (Canada is
  named "Canada", "Canadian" or "Quebec", never "CA", which means California);
- a statement (a bullet, a table data row or a prose paragraph) that cites
  nothing: no design, plan or evidence ID (``R``, ``C``, ``D``, ``SB``, ``G``
  with ``/A``, ``M``, ``I``, ``W``, ``O``), no project file path, no dated
  source (``source: <who or what>, <YYYY-MM-DD>`` or ``checked <YYYY-MM-DD>``)
  and no ``assumption:``, ``counsel:``, ``agency:``, ``gap:``, ``deferred:``,
  ``hypothesis:`` or ``n/a:`` marker (``agency:`` marks what only a
  government client's officers can answer);
- a counsel trigger phrase in the draft or in a ``--source`` file while
  ``counsel_required`` is not ``yes``: the EU AI Act's Annex III areas and the
  high-stakes cases of the other regimes (consequential decisions in
  employment, credit, housing, insurance, health or education; children;
  biometrics, including emotion inference; Commonwealth, NSW and other state
  agencies, the AIAF and AI Review Committees, State contracts, UK central
  government, New Zealand and Singapore public bodies, Canadian federal
  departments and AIA levels; solely or exclusively automated decisions).
  Sections headed as
  out-of-scope or excluded uses, the screening and jurisdiction-screen
  checklists, and the memo's prohibited-practices, high-risk and transparency
  checklists are not scanned, and in a draft a phrase is skipped when the
  drafter's own clause before it says "n/a:", "no" or "not" (source files
  are always scanned in full);
- a line that states when a law or one of its provisions applies (a legal
  reference from any of the four regimes, an applicability word and a date
  written in words, such as "2 August 2026" or "January 1, 2027") without
  ``checked <date>``; ISO dates are treated as project or provenance dates,
  and "read", "updated" or "published" dates are ignored; a checked date in
  the future is an error, one older than ``--max-age-days`` a warning; a
  wrapped statement may carry its checked date on another of its lines, and a
  project-file citation such as ``docs/x.md §4`` is not a statute section;
- with ``--source``, a cited R, C, D, SB, M, I, W or O ID that no source
  file contains (an invented reference); an SB rule named on a ``gap:``,
  ``n/a:`` or ``deferred:`` line is exempt, because the baseline lists rules
  a design may omit; a cited ``docs/`` file that does not exist from the
  current directory is a warning;
- an unfilled template placeholder (``<...>``);
- government form answers without ``form``, ``form_version``, ``form_url``
  or a real ``form_checked`` date, or without saying in the preamble that the
  draft is not the official form; a ``form_checked`` date older than
  ``--form-max-age-days`` (90 by default, because official forms change
  faster than laws) is a warning;
- a draft without the drafting-aid banner under its title (it says the draft
  is not legal advice and is not reviewed until the reviewer signs), without
  a ``## Review and sign-off`` table holding at least one reviewer row, with a
  decision outside ``pending``, ``approved``, ``approved with changes``,
  ``changes requested`` or ``rejected``, or with a recorded decision that has
  no sign-off date; ``status`` must be ``draft`` or ``reviewed``, a draft may
  not carry a recorded decision (only the reviewer signs, and sets
  ``status: reviewed`` when they do), and a reviewed document needs one. The
  sign-off rows are not held to the cite-or-flag rule.

Exit status: 0 clean (warnings allowed), 1 when any error is found, 2 when a
file cannot be read, has no front matter or names an unknown document type.
"""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

REGIMES = ("au", "us", "eu", "uk", "nz", "sg", "ca")
REGIME_NAMES = {"au": "Australia", "us": "United States", "eu": "EU", "uk": "United Kingdom",
                "nz": "New Zealand", "sg": "Singapore", "ca": "Canada"}
ORDER = ", ".join(REGIMES)
# A regime section's heading starts with the regime's name and a colon.
REGIME_PREFIX = {"au": "australia:", "us": "united states:", "eu": "eu:", "uk": "united kingdom:",
                 "nz": "new zealand:", "sg": "singapore:", "ca": "canada:"}
# How a screen table names each regime. Canada is never matched by "CA", which
# US sections use for California.
SCREEN_NAME = {
    "au": re.compile(r"\bAustralia|\bAU\b"),
    "us": re.compile(r"\bUnited States|\bUS\b|\bUSA\b"),
    "eu": re.compile(r"\bEU\b|\bEuropean Union"),
    "uk": re.compile(r"\bUnited Kingdom|\bUK\b"),
    "nz": re.compile(r"\bNew Zealand|\bNZ\b"),
    "sg": re.compile(r"\bSingapore|\bSG\b"),
    "ca": re.compile(r"\bCanad(?:a|ian)\b|\bQu[eé]bec\b"),
}

# Older names still read, so a pack written before the rename keeps its type.
ALIASES = {"classification-memo": "regulatory-memo", "dpia-input-pack": "privacy-impact-input-pack"}

REQUIRED = {
    "regulatory-memo": (
        "Summary", "Jurisdiction screen", "System and intended purpose", "Roles",
        "Applicable dates", "Questions for counsel"),
    "impact-assessment": (
        "Scope and intended use", "Interested parties", "System information",
        "Impacts", "Measures", "Residual risk and decision", "NIST AI RMF mapping",
        "Monitoring and review"),
    "privacy-impact-input-pack": (
        "Screening", "Processing description", "Data flows", "People and data categories|Data subjects",
        "Automated decisions", "Necessity and proportionality", "Retention and erasure",
        "Recipients", "Model provider data use",
        "Risks and measures", "Questions for counsel"),
    "system-card": (
        "Intended use", "Out-of-scope use", "Limits", "Evaluation results",
        "Human oversight", "Automated-decision disclosure", "AI disclosure and hand-off",
        "Data", "Contact"),
    "processing-records": ("Processing activities",),
    "transfer-assessment": (
        "Transfers", "Destination and access facts", "Supplementary measures", "Questions for counsel"),
    "security-questionnaire": ("Answer bank",),
    "poc-note": ("Classification", "Data flow summary", "Questions for counsel"),
    "government-form-answers": (
        "Form and version", "Who completes and approves", "Draft answers", "Questions for the agency",
        "Questions for counsel"),
}
# Sections a regime adds when its code is in ``jurisdictions``.
REGIME_REQUIRED = {
    "regulatory-memo": {
        "au": ("Australia: Privacy Act and APPs", "Australia: Automated decisions",
               "Australia: Sector, state and government AI policy"),
        "us": ("United States: Preemption status and FTC claims",
               "United States: Automated decisions and state AI laws",
               "United States: Privacy, sector and employment laws"),
        "eu": ("EU: Prohibited practices", "EU: High-risk classification",
               "EU: Transparency obligations", "EU: General-purpose AI model"),
        "uk": ("United Kingdom: UK GDPR and automated decisions",
               "United Kingdom: Equality, consumer, online safety and sector"),
        "nz": ("New Zealand: Privacy Act and IPPs",
               "New Zealand: Sector, consumer and government AI policy"),
        "sg": ("Singapore: PDPA and roles", "Singapore: AI governance frameworks",
               "Singapore: Sector and employment"),
        "ca": ("Canada: Privacy laws and roles", "Canada: Automated decisions",
               "Canada: Employment, sector and government AI policy"),
    },
    "privacy-impact-input-pack": {
        "au": ("Australia: APP compliance check", "Australia: Inventory and notice inputs"),
        "us": ("United States: Notice, consent and opt-out", "United States: Assessment approval"),
        "eu": ("EU: Legal basis",),
        "uk": ("United Kingdom: Lawful basis and ADM safeguards",),
        "nz": ("New Zealand: IPP compliance check", "New Zealand: Collection and notice inputs"),
        "sg": ("Singapore: PDPA obligations check", "Singapore: Notification and policy inputs"),
        "ca": ("Canada: Consent and notice inputs", "Canada: Quebec PIA and s 17 facts"),
    },
    "transfer-assessment": {
        "nz": ("New Zealand: s 11 agents and IPP 12",),
        "sg": ("Singapore: Transfer Limitation Obligation",),
        "ca": ("Canada: Quebec s 17 and Alberta service providers",),
    },
}
# Documents that exist only under some regimes, with the reason the checker gives.
# Australia's APP 8 facts and NSW's s 19(2) facts live in the input pack, so an
# Australian-only pack has no transfer annex.
NEEDS_REGIME = {
    "processing-records": (("eu", "uk"), "applies under GDPR or UK GDPR only; jurisdictions lists neither eu nor uk"),
    "transfer-assessment": (("eu", "uk", "nz", "sg", "ca"),
                            "is written for a regime with a transfer rule (eu, uk, nz, sg or ca); jurisdictions "
                            "lists none of them, and Australian APP 8 facts belong in the input pack"),
    "government-form-answers": (("au",), "drafts answers to Australian government forms; jurisdictions must "
                                "list au"),
}
# The section that must name all seven regimes, with a row or line for each.
SCREEN_SECTION = {"regulatory-memo": "jurisdiction screen", "poc-note": "classification"}
COUNSEL_VALUES = {"yes", "no", "pending"}
STATUS_VALUES = {"draft", "reviewed"}
# Every draft opens with the drafting-aid banner and ends with the reviewer's
# sign-off table; only the reviewer records a decision there.
SIGNOFF = "review and sign-off"
BANNER_PHRASES = ("not legal advice", "not reviewed until")
DECISIONS = {"pending", "approved", "approved with changes", "changes requested", "rejected"}
# Government form answers name the official form they answer and when its page
# was last read; forms change faster than laws.
FORM_FIELDS = ("form", "form_version", "form_url")
FORM_MAX_AGE = 90
NOT_THE_FORM = "not the official form"

# Phrases that put a system near a high-stakes area in at least one regime: the
# EU AI Act's Annex III areas, Australian APP 1.7 significant decisions, US
# consequential decisions, UK Article 22A significant decisions and the public
# bodies that carry extra duties. A match forces counsel review; it decides
# nothing about the law.
COUNSEL_TRIGGERS = {
    "biometrics": (r"biometric(?! Processing Privacy Code)", r"facial recognition", r"face recognition", r"emotion recognition",
                   r"voiceprint", r"face geometry", r"speaker verification",
                   r"fingerprint (?:matching|scan|recognition)",
                   r"emotion (?:inference|detection|analysis)", r"infer(?:s|ring)? (?:the )?emotions?",
                   r"(?:mood|attention|fatigue|alertness) (?:detection|monitoring|inference)",
                   r"voice (?:verification|identification)"),
    "critical infrastructure": (r"critical infrastructure", r"critical information infrastructure", r"\bCII owner",
                                r"road traffic", r"water supply",
                                r"gas supply", r"electricity supply", r"heating supply"),
    "education": (r"(?:student|school|university|college) admissions?", r"student assessment",
                  r"grading students", r"proctoring", r"learning outcomes?", r"educational institution",
                  r"vocational training"),
    "employment": (r"recruit(?:ment|ing)", r"\bhiring\b", r"\bCVs?\b", r"r[eé]sum[eé]s?\b",
                   r"candidate screening", r"job applicants?", r"job applications?",
                   r"shortlist(?:ing)? candidates", r"rank(?:s|ing)? candidates", r"promotion decisions?",
                   r"terminat(?:e|ion) of employment", r"dismissal", r"(?:employee|worker|staff) performance",
                   r"allocat(?:e|ing|ion of) (?:tasks|work|shifts) to (?:employees|workers|staff)",
                   r"monitor(?:ing)? (?:employees|workers|staff)", r"remuneration (?:decisions?|outcomes?)",
                   r"bonus (?:decisions?|outcomes?)", r"automated employment decision",
                   r"performance (?:management|conversations?|reviews?|ratings?|improvement plans?)",
                   r"attendance (?:records?|summar(?:y|ies))", r"screen, assess or select applicants",
                   r"publicly advertised job postings?", r"electronic monitoring", r"evaluative purpose"),
    "essential services": (r"creditworth", r"credit scor", r"credit decision", r"loan (?:approval|decision|application)",
                           r"public (?:assistance|benefits?)", r"social (?:security|benefits?)",
                           r"eligibility for (?:benefits|services)", r"life insurance", r"health insurance",
                           r"insurance pricing", r"emergency (?:calls?|dispatch)", r"patient triage",
                           r"adverse action", r"credit report(?:s|ing)", r"MAS-regulated"),
    "housing": (r"tenant screening", r"rental applications?", r"housing (?:eligibility|decisions?|applications?)"),
    "insurance": (r"insurance (?:eligibility|underwriting|claims? decisions?)",),
    "health care": (r"health ?care decisions?", r"clinical decision support", r"treatment decisions?",
                    r"diagnos(?:is|tic) decisions?", r"medical device", r"in vitro diagnostic", r"\bMDR\b",
                    r"protected health information", r"\bPHI\b", r"My Health Record",
                    r"Health Information Privacy Code", r"\bHIPC\b", r"\bNHI\b", r"\bHRIP Act\b",
                    r"health information custodian", r"personal health information", r"\bAI scribes?\b",
                    r"\bNEHR\b", r"HCSA licensee"),
    "children": (r"(?:directed|aimed|targeted) (?:at|to) children", r"(?<!not )likely to be accessed by children",
                 r"\bunder[- ]13s?\b", r"(?<!no )children(?:'s)? (?:data|users|accounts|personal information)",
                 r"users? (?:are|may be|include) (?:children|minors)"),
    "public-body clients": (r"Commonwealth (?:agenc(?:y|ies)|entit(?:y|ies)|departments?)",
                            r"Australian Government agenc", r"central government department",
                            r"public sector equality duty", r"\bPSED\b",
                            # NSW and other Australian state government clients
                            r"\bNSW (?:Government )?(?:agenc(?:y|ies)|departments?|public sector agenc(?:y|ies))",
                            r"\bstate (?:government )?agenc(?:y|ies)", r"\bAIAF\b", r"AI Assessment Framework",
                            r"AI Review Committee", r"DCS-2026-02", r"NSW AI Operational Policy",
                            r"\bState contracts?\b(?! exemptions?)", r"administrative decisions? under an Act",
                            # New Zealand
                            r"Public Service (?:departments?|agenc(?:y|ies))", r"departmental agenc(?:y|ies)",
                            r"Crown entit(?:y|ies)", r"public functions? conferred", r"Algorithm Charter signator",
                            # Singapore
                            r"statutory boards?", r"organs? of state", r"Singapore (?:government )?ministr(?:y|ies)",
                            # Canada
                            r"federal (?:departments?|institutions?)", r"Government of Canada (?:department|institution)",
                            r"Directive on Automated Decision-Making", r"Algorithmic Impact Assessment",
                            r"\bAIA (?:impact )?level", r"impact level (?:I{1,3}V?|IV|[1-4])\b",
                            r"Ontario ministr(?:y|ies)", r"provincial agenc(?:y|ies)"),
    "automated decisions": (r"(?<!no )(?<!not )solely automated (?:significant )?decisions?",
                            r"(?<!no )(?<!not )exclusively automated", r"based exclusively on automated processing",
                            r"fond[ée]e exclusivement sur un traitement automatis"),
    "law enforcement": (r"law enforcement", r"\bpolice\b", r"criminal (?:offence|risk)", r"recidivism",
                        r"evidence reliability"),
    "migration and border control": (r"\basylum\b", r"\bvisa applications?\b", r"border control", r"immigration"),
    "justice and democratic processes": (r"judicial", r"\bcourt\b", r"dispute resolution", r"\belections?\b",
                                         r"voting behaviour", r"\breferendum\b"),
}
# Acronyms matched with their case, so "cv" in a word or "phi" in a name does not fire.
CASE_SENSITIVE = (r"\bCV", r"\bMDR", r"\bPHI", r"\bNHI", r"\bHIPC", r"\bNEHR", r"\bAIAF", r"\bAIA ", r"\bCII",
                  r"MAS-")
TRIGGER_PATTERNS = [(area, re.compile(p, 0 if p.startswith(CASE_SENSITIVE) else re.IGNORECASE))
                    for area, ps in COUNSEL_TRIGGERS.items() for p in ps]
# Sections that list excluded uses, or walk the screening, Article 5 and Annex III
# checklists, name the areas by design; the system's own description and the
# source records still trigger.
EXCLUDED_HEADING = re.compile(r"out[- ]of[- ]scope|excluded|prohibited|not intended|high-risk classification"
                              r"|transparency|^jurisdiction screen|^screening\b", re.IGNORECASE)

ID = re.compile(r"(?<![\w/-])(?:G\d+(?:/A\d+)?|SB\d+|[RCDMIWOHB]\d+)(?![\w-])")   # H, B: impact IDs
CHECKABLE_ID = re.compile(r"(?<![\w/-])(SB\d+|[RCDMIWO]\d+)(?![\w/-])")
PATH = re.compile(r"(?<![\w])[\w./-]+\.(?:md|json|csv|yaml|yml|txt|html|pdf)\b")
URL = re.compile(r"https?://\S+")
ISO = r"\d{4}-\d{2}-\d{2}"
DATED_SOURCE = re.compile(r"\bsource:[^\n]*?" + ISO, re.IGNORECASE)
CHECKED = re.compile(r"\bchecked\s+(" + ISO + r")", re.IGNORECASE)
MARKER = re.compile(r"(?<![\w/])(?:assumption|counsel|agency|gap|n/a|hypothesis|deferred)\s*:\s*[^\s|]",
                    re.IGNORECASE)
AGENCY = re.compile(r"(?<![\w/])agency\s*:\s*[^\s|]", re.IGNORECASE)
PLACEHOLDER = re.compile(r"<[A-Za-z][^<>\n]{0,80}>")
HTML_TAG = re.compile(r"</?(?:br|sub|sup|b|i|em|strong|code|details|summary|p|a)\b", re.IGNORECASE)

MONTHS = (r"(?:January|February|March|April|May|June|July|August|September|October|November|December"
          r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?")
# Applicability dates are written in words ("2 August 2026", "January 1, 2027"), as
# the law and the references write them; ISO dates are project and provenance dates.
LEGAL_DATE = re.compile(rf"\b\d{{1,2}}\s+{MONTHS}\s+\d{{4}}\b|\b{MONTHS}\s+\d{{1,2}},?\s+\d{{4}}\b", re.IGNORECASE)
# A date that records when a source was read or updated is not an applicability date.
PROVENANCE = re.compile(rf"\b(?:checked|read|updated|modified|dated|published)\s+(?:on\s+)?(?:{ISO}|"
                        rf"\d{{1,2}}\s+{MONTHS}\s+\d{{4}})", re.IGNORECASE)
GAP_LINE = re.compile(r"(?<![\w/])(?:gap|n/a|deferred)\s*:", re.IGNORECASE)
# Legal references of the seven regimes: EU instruments; Australian APPs,
# sections and codes, NSW Acts, circulars, policies and contracts, and DTA
# policy; US statutes, bills and rules; UK statutes; New Zealand IPPs and codes;
# Singapore's PDPA and frameworks; Canadian federal, Quebec and provincial law.
# Canadian titles put a comma before the year ("Working for Workers Four Act, 2024").
LEGAL_REF = re.compile(
    r"\b(?:Art\.|Articles?|Annex|Regulation|Directive|AI Act|GDPR|Omnibus|Chapter"
    r"|APPs?\s?\d|Privacy Act|Schedule|Code|Standard|CPS\s?\d+|Act,?\s(?:19|20)\d\d"
    r"|CCPA|CPRA|CPPA|CalPrivacy|ADMT|Colorado|Texas|TRAIGA|Utah|Illinois|Local Law|FEHA|COPPA|HIPAA"
    r"|GLBA|FCRA|ECOA|TCPA|CFR|Civ\. Code|DUAA|Data \(Use and Access\) Act|DPA 2018|PECR"
    r"|Equality Act|Online Safety Act|(?:SB|HB|AB|LD)\s?\d+|PA\s\d\d-\d+"
    r"|PPIP Act|PPIPA|HRIP Act|HRIPA|HPPs?\s?\d+|Part 6A|MNDB|GIPA|State Records Act|DCS-20\d\d-\d\d"
    r"|PBD-20\d\d-\d\d|ICTA|AIAF|Operational Policy|Cyber Security Policy|Essential Eight|AGT\.\d|DTA"
    r"|IPPs?\s?\d+[A-Z]?|Biometric Processing Privacy Code|HIPC|UEMA|NZBORA|Algorithm Charter"
    r"|PDPA|PDPC|Do Not Call|FSM-N\d+|AIHGle|Workplace Fairness|TGFEP|OSRAA|Model AI Governance Framework|MGF"
    r"|PIPEDA|PPCDA|Bill C-\d+|AIDA|Law 25|Loi 25|P-39\.1|CQLR|EFVP|PIPA|PHIPA|FIPPA|EDSTA|CASL|DADM|AIA"
    r"|Directive on Automated Decision-Making|O\. Reg\. \d+/\d+|SOR/\d{4}-\d+)\b"
    r"|(?<!\.md )§\s?\d+|(?<![\w'’])ss?\.?\s\d+[A-Z]*\b",
    re.IGNORECASE)
# Words in the drafter's own clause that say a trigger phrase does not apply.
NEGATION = re.compile(r"(?<![\w/])n/a\s*:|\b(?:no|not|none|never|without|neither|nor)\b", re.IGNORECASE)
APPLICABILITY = re.compile(r"\b(?:appl(?:y|ies|ied|ying|ication|icable)|in force|enters?|entry into force"
                           r"|from|until|since|due|deadline|delay(?:ed|s)?|postpone(?:d|s)?|effective"
                           r"|commenc(?:e|es|ed|ement|ing)|operative|takes? effect|obligations? start)\b",
                           re.IGNORECASE)


def split_front_matter(text: str) -> tuple[dict, list[str], int] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            meta = {}
            for raw in lines[1:end]:
                if ":" in raw and not raw.lstrip().startswith("#"):
                    key, value = raw.split(":", 1)
                    meta[key.strip().lower()] = value.strip().strip("\"'")
            return meta, lines[end + 1:], end + 2
    return None


def parse_jurisdictions(value: str | None) -> tuple[list[str], list[str]]:
    """Return (codes, errors) for the ``jurisdictions`` front-matter value."""
    if value is None or not value.strip("[] \t"):
        return [], ["front matter: jurisdictions is missing or empty; list the regimes the jurisdiction "
                    "screen found in scope, for example jurisdictions: [au, eu]"]
    codes = [c.strip().lower() for c in re.split(r"[,\s]+", value.strip().strip("[]")) if c.strip()]
    errors = []
    unknown = [c for c in codes if c not in REGIMES]
    if unknown:
        errors.append(f"front matter: unknown jurisdiction {', '.join(unknown)}; use {ORDER}")
    known = [c for c in codes if c in REGIMES]
    if len(set(known)) != len(known):
        errors.append("front matter: jurisdictions lists a regime twice")
    elif known != sorted(known, key=REGIMES.index):
        errors.append(f"front matter: list jurisdictions in the order {ORDER}")
    return known, errors


def regime_of(heading: str) -> str | None:
    lowered = heading.lower()
    return next((code for code, prefix in REGIME_PREFIX.items() if lowered.startswith(prefix)), None)


def sections(body: list[str], offset: int):
    """Yield (heading, [(line_number, text)]) per ``##`` section, code fences removed."""
    heading, current, fenced = "(preamble)", [], False
    for index, line in enumerate(body):
        number = index + offset
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if re.match(r"^##\s+", line):
            yield heading, current
            heading, current = re.sub(r"^##\s+", "", line).strip(), []
            continue
        current.append((number, line))
    yield heading, current


def cites(text: str) -> bool:
    return bool(ID.search(text) or PATH.search(text) or URL.search(text) or DATED_SOURCE.search(text)
                or CHECKED.search(text) or MARKER.search(text))


def statements(lines: list[tuple[int, str]], spans: list | None = None):
    """Yield (line_number, text) for bullets, table data rows and prose paragraphs.

    A bullet absorbs the indented lines that continue it. When ``spans`` is a
    list, (first_line, last_line, text) is appended for every statement.
    """
    buffer: list[tuple[int, str]] = []
    in_bullet = False
    table_row = 0

    def flush():
        if buffer:
            joined = " ".join(t.strip() for _, t in buffer)
            first, last = buffer[0][0], buffer[-1][0]
            buffer.clear()
            if spans is not None:
                spans.append((first, last, joined))
            return (first, joined)
        return None

    for number, raw in lines:
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("<!--") or line == "---":
            item = flush()
            if item:
                yield item
            table_row, in_bullet = 0, False
            continue
        if line.startswith("|"):
            item = flush()
            if item:
                yield item
            in_bullet = False
            table_row += 1
            if table_row == 1 or re.fullmatch(r"\|?[\s:|-]+\|?", line):
                continue
            if spans is not None:
                spans.append((number, number, line))
            cells = [c.strip() for c in line.strip("|").split("|")]
            if any(c and c not in {"-", "—"} for c in cells[1:]) or len(cells) == 1:
                yield number, line
            continue
        table_row = 0
        if re.match(r"^(?:[-*+]|\d+[.)])\s+", line):
            item = flush()
            if item:
                yield item
            buffer.append((number, raw))
            in_bullet = True
            continue
        if in_bullet and not raw[:1].isspace():
            item = flush()
            if item:
                yield item
            in_bullet = False
        buffer.append((number, raw))
    item = flush()
    if item:
        yield item


def negated(line: str, start: int) -> bool:
    """True when the drafter's own clause says the phrase does not apply ("n/a:", "no", "not").

    Only drafts are read this way; the source records always trigger, so a real
    high-stakes fact still forces counsel through the brief, design or plan.
    """
    clause = re.split(r"[;|]|\.\s", line[:start])[-1]
    return bool(NEGATION.search(clause))


def lead_in(text: str) -> bool:
    """A short label line such as ``Data flows:`` introduces the statements under it."""
    stripped = re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", text).strip().strip("*_")
    return stripped.endswith(":") and len(stripped.split()) <= 8


def check_structure(doc: str, codes: list[str], found: dict[str, list]) -> list[str]:
    """Required sections, regime sections and the screen, following ``jurisdictions``."""
    errors: list[str] = []
    required = list(REQUIRED[doc])
    for code in codes:
        required.extend(REGIME_REQUIRED.get(doc, {}).get(code, ()))
    for entry in required:
        # "New name|older name": a pack written before a heading was renamed still passes.
        names = entry.split("|")
        name = names[0]
        match = next((h for h in found if any(h.startswith(n.lower()) for n in names)), None)
        if match is None:
            errors.append(f"missing section: ## {name}")
        elif not any(t.strip() for _, t in found[match]):
            errors.append(f"empty section: ## {name}")
    for heading in found:
        code = regime_of(heading)
        if code and code not in codes:
            errors.append(f"section ## {heading} belongs to {REGIME_NAMES[code]}, which jurisdictions does not "
                          f"list; add {code} to jurisdictions or remove the section")
    needs = NEEDS_REGIME.get(doc)
    if needs and codes and not set(needs[0]) & set(codes):
        errors.append(f"{doc} {needs[1]}")
    screen = SCREEN_SECTION.get(doc)
    match = next((h for h in found if h.startswith(screen)), None) if screen else None
    if match is not None:
        text = "\n".join(t for _, t in found[match])
        missing = [code for code in REGIMES if not SCREEN_NAME[code].search(text)]
        for code in missing:
            errors.append(f"## {match}: names no row for {REGIME_NAMES[code]}; record every regime, "
                          "with the reason for any not in scope")
        if missing and set(missing) <= {"nz", "sg", "ca"}:
            errors.append(f"## {match}: the screen now covers seven regimes ({ORDER}); add rows for "
                          + ", ".join(REGIME_NAMES[c] for c in missing)
                          + " with the reason each is or is not in scope (name Canada as Canada or Quebec, "
                          "never CA)")
    return errors


def check_review(meta: dict, found: dict[str, list], today: date) -> list[str]:
    """The drafting-aid banner, the sign-off table and a status that matches it."""
    errors: list[str] = []
    preamble = " ".join(t.strip().lstrip(">").strip() for _, t in found.get("(preamble)", [])).lower()
    preamble = re.sub(r"[*_`]", "", re.sub(r"\s+", " ", preamble))
    if not all(phrase in preamble for phrase in BANNER_PHRASES):
        errors.append("missing the drafting-aid banner under the title (it says the draft is not legal advice "
                      "and not reviewed until the reviewer signs); copy it from the template")
    status = (meta.get("status") or "").lower()
    if status not in STATUS_VALUES:
        errors.append(f"front matter: status must be draft or reviewed (found {status or 'nothing'!r})")
    match = next((h for h in found if h.startswith(SIGNOFF)), None)
    if match is None:
        errors.append("missing section: ## Review and sign-off")
        return errors
    rows = []
    for number, raw in found[match]:
        line = raw.strip()
        if not line.startswith("|") or re.fullmatch(r"\|?[\s:|-]+\|?", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0].lower().startswith("reviewer"):
            continue
        rows.append((number, cells))
    if not rows:
        errors.append("## Review and sign-off: no reviewer row; add one for the reviewer named in for:")
    decided = 0
    for number, cells in rows:
        if len(cells) < 4 or not cells[0]:
            errors.append(f"line {number}: a sign-off row needs reviewer, scope, decision and date")
            continue
        decision, when = cells[2].lower(), cells[3].lower()
        if decision not in DECISIONS:
            errors.append(f"line {number}: decision must be one of {', '.join(sorted(DECISIONS))} "
                          f"(found {cells[2]!r})")
            continue
        if decision == "pending":
            continue
        decided += 1
        try:
            signed = date.fromisoformat(when)
        except ValueError:
            errors.append(f"line {number}: a recorded decision needs the date the reviewer signed (YYYY-MM-DD)")
            continue
        if signed > today:
            errors.append(f"line {number}: sign-off date {when} is in the future")
    if status == "draft" and decided:
        errors.append("status is draft but a reviewer decision is recorded; only the reviewer signs, and sets "
                      "status: reviewed when they do")
    if status == "reviewed" and rows and not decided:
        errors.append("status is reviewed but every sign-off decision is pending")
    return errors


def check_form(meta: dict, found: dict[str, list], today: date, form_max_age: int) -> tuple[list[str], list[str]]:
    """Government form answers name the official form and its checked date, and never claim to be the form."""
    errors: list[str] = []
    warnings: list[str] = []
    for field in FORM_FIELDS:
        if not meta.get(field):
            errors.append(f"front matter: {field} is missing; name the official form, its version as the official "
                          "page shows it, and its URL")
    url = meta.get("form_url", "")
    if url and not url.startswith(("https://", "http://")):
        errors.append(f"front matter: form_url must be the official page's URL (found {url!r})")
    checked = meta.get("form_checked", "")
    try:
        when = date.fromisoformat(checked)
    except ValueError:
        errors.append("front matter: form_checked must be the ISO date (YYYY-MM-DD) the official form's page was "
                      f"last read (found {checked or 'nothing'!r})")
    else:
        if when > today:
            errors.append(f"front matter: form_checked {checked} is in the future")
        elif (today - when).days > form_max_age:
            warnings.append(f"form_checked {checked} is over {form_max_age} days old; re-read the official form's "
                            "page, compare its version and update the answers before the agency relies on them")
    preamble = " ".join(t.strip().lstrip(">").strip() for _, t in found.get("(preamble)", [])).lower()
    if NOT_THE_FORM not in re.sub(r"[*_`]", "", re.sub(r"\s+", " ", preamble)):
        errors.append("the preamble must say this is not the official form (keep the template's sentence): the "
                      "agency's officers complete and approve the form in the official tool")
    return errors, warnings


def check(path: Path, sources: list[Path], today: date, max_age: int,
          form_max_age: int = FORM_MAX_AGE) -> tuple[list[str], list[str], dict]:
    text = path.read_text(encoding="utf-8")
    parsed = split_front_matter(text)
    if parsed is None:
        raise ValueError(f"{path}: no front matter (expected a leading --- block)")
    meta, body, offset = parsed
    doc = ALIASES.get(meta.get("document", ""), meta.get("document", ""))
    if doc not in REQUIRED:
        raise ValueError(f"{path}: unknown document type {meta.get('document', '')!r}; "
                         f"expected one of {sorted(REQUIRED)}")
    errors: list[str] = []
    warnings: list[str] = []
    counsel = meta.get("counsel_required", "").lower().split()[0] if meta.get("counsel_required") else ""
    if counsel not in COUNSEL_VALUES:
        errors.append(f"front matter: counsel_required must be yes, no or pending (found {counsel or 'nothing'!r})")
    codes, jurisdiction_errors = parse_jurisdictions(meta.get("jurisdictions"))
    errors.extend(jurisdiction_errors)

    found = {}
    for heading, lines in sections(body, offset):
        found[heading.lower()] = lines
    errors.extend(check_structure(doc, codes, found))
    errors.extend(check_review(meta, found, today))
    if doc == "government-form-answers":
        form_errors, form_warnings = check_form(meta, found, today, form_max_age)
        errors.extend(form_errors)
        warnings.extend(form_warnings)

    triggers: dict[str, set[str]] = {}
    cited_ids: dict[str, int] = {}
    agency_items = 0
    for heading, lines in sections(body, offset):
        excluded = bool(EXCLUDED_HEADING.search(heading))
        spans: list[tuple[int, int, str]] = []
        section_statements = list(statements(lines, spans))
        for number, raw in lines:
            for placeholder in PLACEHOLDER.findall(raw):
                if not HTML_TAG.match(placeholder) and not placeholder.startswith(("<http:", "<https:")):
                    errors.append(f"line {number}: unfilled placeholder {placeholder}")
            if not excluded:
                for area, pattern in TRIGGER_PATTERNS:
                    hit = next((h for h in pattern.finditer(raw) if not negated(raw, h.start())), None)
                    if hit:
                        triggers.setdefault(area, set()).add(f"{path.name}:{number} '{hit.group(0)}'")
            for ident in CHECKABLE_ID.findall(raw):
                # A baseline rule the design does not list may be named as a gap or n/a.
                if not (ident.startswith("SB") and GAP_LINE.search(raw)):
                    cited_ids.setdefault(ident, number)
            for cited in PATH.findall(raw):
                if cited.startswith("docs/") and not Path(cited).exists():
                    warnings.append(f"line {number}: cited file {cited} not found from the current directory")
            undated = PROVENANCE.sub("", raw)
            if LEGAL_REF.search(undated) and APPLICABILITY.search(undated) and LEGAL_DATE.search(undated):
                # A wrapped statement may carry its checked date on a neighbouring line.
                statement = next((text for first, last, text in spans if first <= number <= last), raw)
                if not CHECKED.search(raw) and not CHECKED.search(statement):
                    errors.append(f"line {number}: legal applicability date without 'checked <YYYY-MM-DD>'")
            for value in CHECKED.findall(raw):
                try:
                    when = date.fromisoformat(value)
                except ValueError:
                    errors.append(f"line {number}: checked date {value} is not a real date")
                    continue
                if when > today:
                    errors.append(f"line {number}: checked date {value} is in the future")
                elif (today - when).days > max_age:
                    warnings.append(f"line {number}: checked {value} is over {max_age} days old; re-check the source")
        if heading == "(preamble)" or heading.lower().startswith(SIGNOFF):
            continue
        for number, statement in section_statements:
            agency_items += len(AGENCY.findall(statement))
            if lead_in(statement) or cites(statement):
                continue
            snippet = statement if len(statement) <= 70 else statement[:67] + "..."
            errors.append(f"line {number}: statement cites no ID, path, dated source or marker: {snippet}")

    source_ids: set[str] = set()
    for source in sources:
        source_text = source.read_text(encoding="utf-8")
        source_ids.update(CHECKABLE_ID.findall(source_text))
        for number, raw in enumerate(source_text.splitlines(), 1):
            for area, pattern in TRIGGER_PATTERNS:
                hit = pattern.search(raw)
                if hit:
                    triggers.setdefault(area, set()).add(f"{source.name}:{number} '{hit.group(0)}'")
    if sources:
        for ident, number in sorted(cited_ids.items(), key=lambda item: item[1]):
            if ident not in source_ids:
                errors.append(f"line {number}: cites {ident}, which no source file contains")
    if triggers and counsel != "yes":
        areas = ", ".join(sorted(triggers))
        example = sorted(next(iter(triggers.values())))[0]
        errors.append(f"counsel trigger ({areas}; e.g. {example}): set counsel_required: yes; counsel confirms "
                      "or rejects the high-risk classification and the automated-decision questions")
    summary = {"file": str(path), "document": doc, "jurisdictions": codes, "counsel_required": counsel,
               "counsel_triggers": sorted(triggers), "annex_iii_areas": sorted(triggers),
               "agency_items": agency_items, "errors": errors, "warnings": warnings}
    return errors, warnings, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("drafts", nargs="+", type=Path, help="draft files or a directory of drafts")
    parser.add_argument("--source", action="append", type=Path, default=[],
                        help="discovery brief, design, plan or ticket the drafts cite (repeatable)")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(), help=argparse.SUPPRESS)
    parser.add_argument("--max-age-days", type=int, default=180)
    parser.add_argument("--form-max-age-days", type=int, default=FORM_MAX_AGE,
                        help="warn when a government form's form_checked date is older than this")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    files: list[Path] = []
    for item in args.drafts:
        files.extend(sorted(item.glob("*.md")) if item.is_dir() else [item])
    if not files:
        print("ERROR: no draft files found", file=sys.stderr)
        return 2
    results, status = [], 0
    for path in files:
        try:
            errors, warnings, summary = check(path, args.source, args.today, args.max_age_days,
                                              args.form_max_age_days)
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        results.append(summary)
        status = max(status, 1 if errors else 0)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for summary in results:
            state = "FAIL" if summary["errors"] else "ok"
            areas = ", ".join(summary["counsel_triggers"]) or "none"
            regimes = ", ".join(summary["jurisdictions"]) or "?"
            agency = f"; agency questions: {summary['agency_items']}" if summary["agency_items"] else ""
            print(f"{state}  {summary['file']} ({summary['document']}; jurisdictions: {regimes}; "
                  f"counsel_required: {summary['counsel_required'] or '?'}; counsel triggers: {areas}{agency})")
            for message in summary["errors"]:
                print(f"  error: {message}")
            for message in summary["warnings"]:
                print(f"  warning: {message}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
