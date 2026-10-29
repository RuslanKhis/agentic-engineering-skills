"""Invoice hold agent: extraction, then the hold decision. Illustrative wiring for the evaluation fixture."""

from google.adk.agents import LlmAgent, SequentialAgent

from .tools import find_paid_invoice

extract_invoice = LlmAgent(
    name="extract_invoice",
    model="gemini-3.5-flash",
    instruction=(
        "Read the attached invoice scan. Return invoice_number, supplier_name, po_number, "
        "total and po_amount exactly as printed, or null when a field is absent."
    ),
    output_key="extracted",
)

decide_hold = LlmAgent(
    name="decide_hold",
    model="gemini-3.5-flash",
    instruction=(
        "Invoice fields: {extracted}\n"
        "Call find_paid_invoice with the invoice number. Decide pay or hold under the hold rules: "
        "hold a duplicate, a total more than 2% over the purchase order amount, or an invoice with "
        "no purchase order. Give the rule and a one-sentence reason."
    ),
    tools=[find_paid_invoice],
    output_key="decision",
)

root_agent = SequentialAgent(name="invoice_hold", sub_agents=[extract_invoice, decide_hold])
