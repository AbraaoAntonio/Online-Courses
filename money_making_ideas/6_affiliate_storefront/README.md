# 6. Affiliate Storefront — Sell Other People's Products, Zero Inventory, Zero Capital

**The model:** You don't buy, hold, ship, or touch any product. You publish
a curated storefront recommending other companies' products. Every "View
Deal" link is a tracked affiliate link. When a visitor clicks through and
buys, the *merchant* handles payment/fulfillment/support, and pays you a
commission. This is different from dropshipping — you never take on
inventory risk, chargebacks, or fulfillment obligations.

**What's in this folder:** a real, running storefront (Flask), a sample
niche catalog (`products.json`), click-through tracking (`data.py` — logs
every outbound click to a local SQLite DB so you can see what's actually
getting clicked, independent of what each affiliate network reports back),
and a revenue calculator that models honest revenue at different traffic
levels so your expectations are based on math, not hope.

## Run the POC

```bash
cd 6_affiliate_storefront
pip install -r requirements.txt
python app.py                    # storefront at http://localhost:5002
python revenue_calculator.py      # realistic revenue by growth stage
```

Visit `/`, click a "View Deal" button (redirects to the placeholder
affiliate link and logs the click), then visit `/analytics` to see the
click counts.

## The real work: 5 steps to actually launch this

### 1. Pick one tight niche — don't build a general store
"Everything store" affiliate sites don't rank on Google and don't get
followed on social media — nobody trusts a generalist for buying advice.
The sample catalog here is deliberately narrow ("home coffee gear") to
demonstrate this. Pick a niche where:
- You have genuine interest/knowledge (you'll need to produce content
  about it constantly)
- There are affiliate programs for it (almost everything does)
- You can name 20+ specific products people search for advice on

### 2. Join the affiliate programs and get real links
Replace every `affiliate_url` placeholder in `products.json` with your
real tracked link:
- **Amazon Associates** — easiest to get approved, huge catalog, but low
  commission (1-10% depending on category) and only a 24-hour cookie
  window. You must generate 3 qualifying sales within 180 days of
  approval or the account gets closed — plan your first content push
  around that.
- **ShareASale / CJ Affiliate / Awin / Impact.com** — aggregator networks
  with thousands of individual brands, commissions often 10-50%, and some
  offer recurring commissions for subscription products (see `p5` in the
  sample catalog) — recurring commission products should be prioritized
  since one referral pays you every month the customer stays subscribed.
- **ClickBank** — digital products/courses, commissions often 30-75%,
  higher payout per sale but vet quality carefully — some listings are
  low-quality; your reputation is what you're actually selling.

### 3. Legal requirement: disclosure
The FTC requires clear, unavoidable disclosure that you earn commissions
on any page with affiliate links (`base.html` already includes a
disclosure banner on every page — keep it, don't hide it in fine print).
Each network also has its own terms (e.g., Amazon prohibits link cloaking
tricks, cash-back offers for using your link, and using their links in
certain ad placements) — read the terms of whichever programs you join.

### 4. Traffic — this is the actual business, not the code
The storefront is done. Nobody will find it without traffic. In order of
cost (all free except the last):
1. **SEO content** — write genuinely useful "best X for Y" and individual
   product comparison articles targeting search terms your niche audience
   uses. Slow (3-12 months to rank) but compounds and runs itself once
   ranked.
2. **Short-form social** (TikTok/Reels/Pinterest) — much faster feedback
   loop than SEO for physical products; Pinterest in particular sends
   long-tail traffic to product-style content for years after posting.
3. **A community/niche forum presence** — genuinely helpful answers in
   niche subreddits/forums/Facebook groups, linking to your
   comparison content (not raw affiliate links) when relevant — don't spam.
4. **Paid ads** — fastest, but costs money, which you said you want to
   avoid; revisit this only once organic channels prove the niche converts.

### 5. Track and double down on what actually converts
Use `/analytics` (and each network's own dashboard) to see which specific
products and content pieces drive clicks and sales, then produce more
content like the winners — most of the revenue in affiliate sites comes
from a small number of "money pages," not from spreading effort evenly.

## Honest expectations (see `revenue_calculator.py`)

| Stage | Monthly visitors | Est. monthly revenue |
|---|---|---|
| Just started, no SEO yet | 200 | ~$1 |
| Some social traction (3-6 mo) | 2,000 | ~$12 |
| SEO started ranking (6-12 mo) | 8,000 | ~$79 |
| Established niche authority (yr 2+) | 30,000 | ~$429 |

This is a **compounding, months-to-years business**, not a fast cash
lever like the one-off products in folders 1-5 of this repo. Its appeal
for your situation is that it requires **$0 of capital** and can run
alongside a day job — but don't expect it to move your debt in month one.
Treat it as a long-term asset you build in parallel while the faster
one-time-sale ideas (`1_resume_job_matcher`, `2_instant_csv_insights`)
generate nearer-term cash.
