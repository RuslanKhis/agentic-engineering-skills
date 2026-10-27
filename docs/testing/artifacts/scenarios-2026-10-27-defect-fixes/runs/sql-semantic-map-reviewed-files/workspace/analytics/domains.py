"""Semantic domains for the generated-query route.

The map lives in reviewed YAML under `semantic/` (see `analytics/semantic.py`); this module loads it
into the shape the metadata collector and generated route use. Each domain lists the tables the
author may see, the columns exposed to it, the joins it may use and any derived tables (defined by
SQL that the metadata collector expands into the candidate).
"""
from analytics.semantic import build_domains

PROJECT = "fernhill-analytics"
DATASET = "sales"

DOMAINS = build_domains()
