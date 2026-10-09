from support_agent import tools


def test_orders_api_constant():
    assert tools.ORDERS_API.startswith("https://")
