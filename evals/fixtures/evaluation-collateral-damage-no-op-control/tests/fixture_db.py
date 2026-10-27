"""A fresh, seeded expenses database per test."""
from expense_agent import db, tools

EMPLOYEES = [("emp-101", "Ana Ruiz", "dep-1", "emp-900"), ("emp-102", "Ben Okafor", "dep-1", "emp-900"),
             ("emp-203", "Chen Li", "dep-2", "emp-901"), ("emp-900", "Dana Fox", "dep-1", None),
             ("emp-901", "Eli Ward", "dep-2", None)]


def fresh_db():
    conn = db.connect(":memory:")
    with conn:
        conn.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", EMPLOYEES)
        conn.executemany("INSERT INTO departments VALUES (?, ?, ?)", [("dep-1", "Sales", "CC-10"), ("dep-2", "Ops", "CC-20")])
        conn.executemany("INSERT INTO profiles VALUES (?, ?, ?, ?, '2026-09-01')",
                         [("emp-101", "emp-900", "4411", "EUR"), ("emp-102", "emp-900", "1290", "EUR"),
                          ("emp-203", "emp-901", "7781", "GBP")])
        conn.executemany("INSERT INTO expense_categories VALUES (?, ?, ?)",
                         [("MEAL", "Meals", "6410"), ("TRAVEL", "Travel", "6420"), ("HOTEL", "Hotels", "6430"), ("OFFICE", "Office", "6440")])
        conn.executemany("INSERT INTO policy_limits VALUES (?, ?, ?)",
                         [(c, g, l) for c, l in (("MEAL", 6000), ("TRAVEL", 50000), ("HOTEL", 18000), ("OFFICE", 15000))
                          for g in ("G1", "G2", "G3")])
        conn.executemany("INSERT INTO exchange_rates VALUES (?, ?, ?)", [("GBP", "2026-10-01", 1.16), ("USD", "2026-10-01", 0.92)])
        conn.executemany("INSERT INTO cards VALUES (?, ?, 1)", [("emp-101", "4411"), ("emp-102", "1290")])
    tools.use_connection(conn)
    return conn
