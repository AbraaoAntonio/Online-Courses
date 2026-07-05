"""Plug in realistic traffic/conversion assumptions to see what an
affiliate storefront could actually earn - so goals are based on math,
not hope. Adjust the numbers to match your own niche and traffic source.
"""


def estimate_monthly_revenue(
    monthly_visitors: int,
    click_through_rate: float,
    conversion_rate: float,
    avg_order_value: float,
    commission_pct: float,
) -> dict:
    clicks = monthly_visitors * click_through_rate
    sales = clicks * conversion_rate
    revenue = sales * avg_order_value * commission_pct
    return {
        "monthly_visitors": monthly_visitors,
        "outbound_clicks": round(clicks),
        "estimated_sales": round(sales, 1),
        "estimated_monthly_revenue": round(revenue, 2),
    }


SCENARIOS = {
    "Just started (month 1-2, no SEO traffic yet)": dict(
        monthly_visitors=200, click_through_rate=0.10,
        conversion_rate=0.02, avg_order_value=50, commission_pct=0.05,
    ),
    "Some traction (social posting weekly, month 3-6)": dict(
        monthly_visitors=2000, click_through_rate=0.12,
        conversion_rate=0.02, avg_order_value=50, commission_pct=0.05,
    ),
    "SEO started ranking (month 6-12)": dict(
        monthly_visitors=8000, click_through_rate=0.12,
        conversion_rate=0.025, avg_order_value=55, commission_pct=0.06,
    ),
    "Established niche authority (year 2+)": dict(
        monthly_visitors=30000, click_through_rate=0.13,
        conversion_rate=0.025, avg_order_value=55, commission_pct=0.08,
    ),
}


if __name__ == "__main__":
    print("Realistic revenue by growth stage (adjust SCENARIOS for your own niche):\n")
    for label, params in SCENARIOS.items():
        result = estimate_monthly_revenue(**params)
        print(f"{label}")
        print(f"  Visitors/mo: {result['monthly_visitors']:,} -> "
              f"clicks: {result['outbound_clicks']:,} -> "
              f"sales: {result['estimated_sales']} -> "
              f"revenue: ${result['estimated_monthly_revenue']:,.2f}/mo\n")
