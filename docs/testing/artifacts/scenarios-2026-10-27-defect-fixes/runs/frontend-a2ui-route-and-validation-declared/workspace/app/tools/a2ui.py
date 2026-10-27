"""A2UI v0.9 messages for product cards and the comparison table.

Converters turn validated tool results into messages; the model never writes
component JSON. `check_messages` refuses any component outside ALLOWED_COMPONENTS,
so an unknown element fails loudly instead of rendering nothing.
No google.adk imports here (unit tests run without the SDK).
"""
from __future__ import annotations

VERSION = "v0.9"
# Assumption: the standard basic catalogue. Replace with our own catalogue id if one is published.
CATALOG_ID = "https://a2ui.org/specification/v0_9/basic_catalog.json"
ALLOWED_COMPONENTS = frozenset({"Column", "Row", "Card", "Text", "Image"})
PRODUCTS_SURFACE = "products"
COMPARE_SURFACE = "compare"

_HEADERS = {"name": "Product", "price_cents": "Price", "weight_g": "Weight", "waterproof_mm": "Waterproof",
            "rating": "Rating"}


class A2uiValidationError(ValueError):
    pass


def _money(cents: int) -> str:
    # Assumption: prices are USD. Integer arithmetic only.
    return f"${cents // 100}.{cents % 100:02d}"


def _cell(column: str, value) -> str:
    if value is None:
        return "-"
    if column == "price_cents":
        return _money(int(value))
    if column == "weight_g":
        return f"{value} g"
    if column == "waterproof_mm":
        return f"{value} mm"
    return str(value)


def _surface(surface_id: str, components: list[dict]) -> list[dict]:
    return [
        {"version": VERSION, "createSurface": {"surfaceId": surface_id, "catalogId": CATALOG_ID}},
        {"version": VERSION, "updateComponents": {"surfaceId": surface_id, "components": components}},
    ]


def product_cards(result: dict) -> list[dict]:
    components: list[dict] = []
    card_ids: list[str] = []
    for p in result["products"]:
        key = p["sku"]
        card_ids.append(f"card-{key}")
        components += [
            {"id": f"card-{key}", "component": "Card", "child": f"body-{key}"},
            {"id": f"body-{key}", "component": "Column",
             "children": [f"img-{key}", f"name-{key}", f"price-{key}", f"rating-{key}"]},
            {"id": f"img-{key}", "component": "Image", "url": p["image_url"]},
            {"id": f"name-{key}", "component": "Text", "text": p["name"]},
            {"id": f"price-{key}", "component": "Text", "text": _money(int(p["price_cents"]))},
            {"id": f"rating-{key}", "component": "Text", "text": f"Rated {p['rating']}"},
        ]
    components.append({"id": "root", "component": "Row", "children": card_ids})
    return _surface(PRODUCTS_SURFACE, components)


def comparison_table(result: dict) -> list[dict]:
    columns = result["columns"]
    components: list[dict] = []
    row_ids = ["row-head"]
    components.append({"id": "row-head", "component": "Row",
                       "children": [f"head-{c}" for c in columns]})
    components += [{"id": f"head-{c}", "component": "Text", "text": _HEADERS.get(c, c)} for c in columns]
    for r in result["rows"]:
        rid = f"row-{r['sku']}"
        row_ids.append(rid)
        components.append({"id": rid, "component": "Row", "children": [f"{rid}-{c}" for c in columns]})
        components += [{"id": f"{rid}-{c}", "component": "Text", "text": _cell(c, r.get(c))} for c in columns]
    components.append({"id": "root", "component": "Column", "children": row_ids})
    return _surface(COMPARE_SURFACE, components)


def for_tool_result(tool_name: str, result: dict) -> list[dict]:
    """Messages for one successful tool result; [] for tools without a widget or errors."""
    if not isinstance(result, dict) or result.get("status") != "ok":
        return []
    if tool_name == "search_products" and result.get("products"):
        return check_messages(product_cards(result))
    if tool_name == "compare_products":
        return check_messages(comparison_table(result))
    return []


def check_messages(messages: list[dict]) -> list[dict]:
    """Reject unknown components, a missing root and dangling child references."""
    for m in messages:
        update = m.get("updateComponents")
        if not update:
            continue
        components = update["components"]
        ids = {c["id"] for c in components}
        if "root" not in ids:
            raise A2uiValidationError(f"surface {update['surfaceId']}: missing root")
        for c in components:
            kind = c.get("component")
            if kind not in ALLOWED_COMPONENTS:
                raise A2uiValidationError(f"component {kind!r} ({c['id']}) is not in the catalogue")
            refs = list(c.get("children", [])) + ([c["child"]] if "child" in c else [])
            dangling = [r for r in refs if r not in ids]
            if dangling:
                raise A2uiValidationError(f"{c['id']}: dangling references {dangling}")
    return messages
