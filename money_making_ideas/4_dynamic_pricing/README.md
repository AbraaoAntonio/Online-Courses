# 4. PricePilot — Demand Forecasting & Price Optimization for Sellers

**The problem:** Etsy/Shopify/Amazon sellers set prices by gut feel. They
have the sales history to do better, but no way to turn it into a price
recommendation.

**The product:** Feed in historical price/units-sold data (with
competitor price + seasonality), a Random Forest regressor predicts demand
at different price points and recommends the price that maximizes expected
revenue.

**Why this can make money fast**
- Direct revenue impact is easy to demonstrate and easy to sell: "raise
  your average order value by even 5% and this pays for itself."
- Huge addressable market: millions of small Etsy/Shopify/Amazon sellers,
  most with zero pricing strategy today.
- Can be sold as a lightweight monthly report before building a full
  dashboard — low build cost for the first sale.

**Run the POC**
```bash
cd 4_dynamic_pricing
pip install -r requirements.txt
python forecast.py     # trains per-product models on sample_sales.csv,
                        # prints recommended price + predicted revenue
```

**Path to first $ (this week)**
1. Find 10 Etsy/Shopify sellers (Etsy seller Facebook groups, r/EtsySellers,
   r/shopify) and offer a **free pricing audit** on their best-selling
   product using their exported order history.
2. Turn the audit into a one-page PDF: "current price vs. recommended
   price vs. projected revenue lift" — this single chart sells itself.
3. Charge $29/mo per store for a monthly re-run + email report, or bundle
   with #2 (InstantInsights) as a combined "seller analytics" package.

**Pricing:** $29/mo single store, $79/mo for sellers with 10+ SKUs,
one-time $99 pricing audit for sellers who don't want a subscription yet
(great low-friction first sale to build trust before upselling).
