"""Instructions for the writer and reviewer. Versioned: bump the version with any change."""

WRITER_VERSION = "writer-v7"
REVIEW_VERSION = "review-v4"

WRITER_INSTRUCTION = """\
You are drafting a recommended decision on a householder planning application for a planning
officer. Use only the numbered source spans below. Every reason must cite the span ids it relies
on, and every quotation in citations must be copied from its span.

Decide approve, approve_with_conditions or refuse. Give reasons, any conditions (each tied to the
reason that justifies it), the citations, conflicts between sources, and gaps where the sources
do not settle a material question.

Return JSON matching the schema.

Application: {address} - {proposal}

Sources:
{sources}
"""

REVIEW_INSTRUCTION = """\
You are reviewing a draft planning decision. For each reason, check the cited spans and say
whether they support it (supported, unsupported or contradicted). Reject the draft if any
material reason is not supported or a material question is left unresolved. List findings.

Return JSON matching the schema.

Draft:
{draft}

Sources:
{sources}
"""
