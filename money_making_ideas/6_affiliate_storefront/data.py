"""Product catalog loading + click tracking for the affiliate storefront.

Click tracking exists because Amazon/ShareASale/ClickBank dashboards only
tell you what sold - they don't tell you which placement on YOUR site got
the click. Owning that data lets you A/B test which products, wording, and
positions actually drive traffic to the merchant, independent of whatever
the affiliate network reports back.
"""
import json
import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_PATH = os.path.join(BASE_DIR, "products.json")
DB_PATH = os.path.join(BASE_DIR, "clicks.db")


def load_products() -> list[dict]:
    with open(PRODUCTS_PATH) as f:
        return json.load(f)


def get_product(product_id: str) -> dict | None:
    for p in load_products():
        if p["id"] == product_id:
            return p
    return None


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            product_name TEXT NOT NULL,
            clicked_at TEXT NOT NULL,
            referrer TEXT,
            user_agent TEXT
        )"""
    )
    conn.commit()
    conn.close()


def log_click(product_id: str, product_name: str, referrer: str, user_agent: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO clicks (product_id, product_name, clicked_at, referrer, user_agent) "
        "VALUES (?, ?, ?, ?, ?)",
        (product_id, product_name, datetime.utcnow().isoformat(), referrer, user_agent),
    )
    conn.commit()
    conn.close()


def click_counts() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT product_id, product_name, COUNT(*) as clicks "
        "FROM clicks GROUP BY product_id, product_name ORDER BY clicks DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def total_clicks() -> int:
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute("SELECT COUNT(*) FROM clicks").fetchone()[0]
    conn.close()
    return count
