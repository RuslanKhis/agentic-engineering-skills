"""Memory Bank configuration for the delivery assistant (applied when the Agent Engine is created)."""

MEMORY_TOPICS = [
    {"managed_memory_topic": {"managed_topic_enum": "USER_PERSONAL_INFO"}},
    {"managed_memory_topic": {"managed_topic_enum": "USER_PREFERENCES"}},
    {"custom_memory_topic": {
        "label": "delivery_details",
        "description": "Delivery address, building access, where to leave bags, preferred slots.",
    }},
    {"custom_memory_topic": {
        "label": "account_benefits",
        "description": "Loyalty status, discounts or offers the customer mentions.",
    }},
]

MEMORY_BANK_CONFIG = {
    "customization_configs": [{"memory_topics": MEMORY_TOPICS}],
    "similarity_search_config": {"embedding_model": "text-embedding-005"},
    "generation_config": {"model": "gemini-2.5-flash"},
}

# Revisions are on (the default); kept 90 days.
REVISION_TTL = "7776000s"
