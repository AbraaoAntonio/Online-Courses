# 3. StayWise — Churn Prediction for Subscription Businesses

**The problem:** Subscription businesses (gyms, SaaS tools, box
subscriptions, telecom resellers) lose customers every month and usually
find out only after they've already cancelled.

**The product:** The business exports a customer CSV (tenure, spend,
support tickets, contract type, etc.). A Random Forest model scores every
customer's churn risk and ranks them, so the business can proactively call
or discount the ones about to leave — before they leave.

**Why this can make money fast**
- B2B recurring revenue: sell a $99–$299/mo subscription, not a one-time
  purchase — this is the fastest way to build a stack of predictable
  income to pay down debt.
- The pitch is a hard ROI number: "keeping just 3 extra customers/month at
  $50 each pays for this tool 10x over."
- Businesses already have this data sitting in Stripe/CRM exports — no new
  data collection needed from them.

**Run the POC**
```bash
cd 3_churn_predictor
pip install -r requirements.txt
python train_and_predict.py   # trains on sample_customers.csv, prints at-risk list
```

**Path to first $ (this week)**
1. Package this as a script that accepts any CSV export (Stripe, gym
   management software, etc.) — the column-mapping is the only thing that
   changes per client.
2. Find 5 local subscription businesses (gyms, salons, SaaS on
   Indie Hackers) and offer a **free churn audit**: "send me your customer
   export, I'll tell you your 10 highest-risk customers this week."
3. Convert the audit into a $99/mo standing service: re-run monthly,
   deliver a ranked list + suggested retention offer per segment.
4. Once you have 3-5 paying clients, wrap it in a simple scheduled script
   / Flask dashboard so it runs without your manual involvement.

**Pricing:** $99/mo per business (up to 5,000 customers), $299/mo for
larger accounts, or a hybrid: flat fee + $2 per prevented churn (tracked
against a control group) for businesses that want performance-based pricing.
