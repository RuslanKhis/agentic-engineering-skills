"""Chooses the query path for a question: a reviewed template, a generated query, or clarify."""
from __future__ import annotations

import re
from dataclasses import dataclass

from analytics.domains import DOMAINS


@dataclass
class Route:
    path: str  # "template" | "generated" | "clarify"
    template: str | None = None
    domain: str | None = None
    reason: str = ""


TEMPLATE_PATTERNS = [
    (re.compile(r"\btop\b.*\bcustomers?\b.*\brevenue\b|\bbiggest customers\b", re.I), "top_customers_by_revenue"),
    (re.compile(r"\bmonthly revenue\b.*\b(north|midlands|south|scotland|wales)\b", re.I), "monthly_revenue_for_region"),
]

DOMAIN_WORDS = {
    "revenue": ("revenue", "invoice", "sales", "customer", "account"),
    "products": ("product", "sku", "catalogue", "discontinued", "price"),
}


def route(question: str) -> Route:
    for pattern, name in TEMPLATE_PATTERNS:
        if pattern.search(question):
            return Route("template", template=name, reason="matches a reviewed template")
    words = question.lower()
    hits = [d for d, keys in DOMAIN_WORDS.items() if any(k in words for k in keys)]
    if len(hits) == 1 and hits[0] in DOMAINS:
        return Route("generated", domain=hits[0], reason="single supported domain")
    if not hits:
        return Route("clarify", reason="no supported domain")
    return Route("clarify", reason="question spans several domains")
