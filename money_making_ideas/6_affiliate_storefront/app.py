"""Affiliate storefront - list other people's products, earn a commission
when a visitor clicks through and buys, hold zero inventory and spend
zero money on stock.

Run: python app.py, open http://localhost:5002

Every "View Deal" button points at /go/<product_id>, which logs the click
and 302-redirects to the real affiliate link (from products.json). Swap
the placeholder affiliate_url values for your real Amazon Associates /
ShareASale / ClickBank links before going live.
"""
from collections import defaultdict

from flask import Flask, abort, redirect, render_template, request

from data import click_counts, get_product, init_db, load_products, log_click, total_clicks

app = Flask(__name__)
init_db()


@app.route("/")
def index():
    products = load_products()
    by_category = defaultdict(list)
    for p in products:
        by_category[p["category"]].append(p)
    return render_template("index.html", by_category=dict(by_category))


@app.route("/category/<category>")
def category(category):
    products = [p for p in load_products() if p["category"] == category]
    if not products:
        abort(404)
    return render_template("category.html", category=category, products=products)


@app.route("/go/<product_id>")
def go(product_id):
    product = get_product(product_id)
    if product is None:
        abort(404)
    log_click(
        product_id=product["id"],
        product_name=product["name"],
        referrer=request.referrer or "direct",
        user_agent=request.headers.get("User-Agent", ""),
    )
    return redirect(product["affiliate_url"], code=302)


@app.route("/analytics")
def analytics():
    return render_template(
        "analytics.html", counts=click_counts(), total=total_clicks()
    )


if __name__ == "__main__":
    app.run(debug=True, port=5002)
