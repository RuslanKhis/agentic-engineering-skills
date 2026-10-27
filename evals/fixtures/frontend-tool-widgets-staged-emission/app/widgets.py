"""A2UI payloads for the product cards and the comparison table.

The React app renders widgets whose provider is "a2ui" next to the reply.
"""
from __future__ import annotations

CARDS_ID = "product-cards"
TABLE_ID = "comparison-table"


def product_cards(products: list[dict], currency: str = "GBP") -> dict:
    symbol = {"GBP": "£", "EUR": "€", "USD": "$"}.get(currency, "")
    return {
        "surfaceId": CARDS_ID,
        "components": [
            {"id": f"card-{p['sku']}", "component": "ProductCard",
             "title": p["name"], "price": f"{symbol}{p['price_cents'] / 100:.2f}",
             "image": p["image_url"], "rating": p["rating"]}
            for p in products
        ],
    }


def comparison_table(columns: list[str], rows: list[dict]) -> dict:
    return {"surfaceId": TABLE_ID,
            "components": [{"id": "table", "component": "Table", "columns": columns, "rows": rows}]}


def to_ui_widget(widget_id: str, payload: dict):
    from google.adk.events.ui_widget import UiWidget

    return UiWidget(id=widget_id, provider="a2ui", payload=payload)
