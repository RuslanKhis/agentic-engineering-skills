"""Memory Bank configuration for the delivery assistant (applied when the Agent Engine is created)."""

MEMORY_TOPICS = [
    {"managed_memory_topic": {"managed_topic_enum": "USER_PERSONAL_INFO"}},
    {"managed_memory_topic": {"managed_topic_enum": "USER_PREFERENCES"}},
    {"custom_memory_topic": {
        "label": "delivery_details",
        "description": (
            "Delivery address, building access, where to leave bags, preferred slots. There is one current "
            "delivery address: when the customer says they moved or gives a new address, UPDATE the existing "
            "address memory to the new one and do not keep the old address as a separate or additional fact."),
    }},
    # No account_benefits topic: discounts, VIP status and offers are owned by checkout/account systems and
    # a memory must never grant them (incident 2026-09-24). Removing it here only affects an engine once the
    # config is re-applied to it; that is a manual step, see README.
]

MEMORY_BANK_CONFIG = {
    "customization_configs": [{"memory_topics": MEMORY_TOPICS}],
    "similarity_search_config": {"embedding_model": "text-embedding-005"},
    "generation_config": {"model": "gemini-2.5-flash"},
}

# Revisions are on (the default); kept 90 days.
REVISION_TTL = "7776000s"
