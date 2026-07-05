# 1. ResumeFit — Instant ATS Match Score

**The problem:** Every job seeker gets filtered by ATS keyword-matching software
before a human ever sees their resume. Most have no idea why they're getting
rejected.

**The product:** Paste a resume + a job description, get an instant match
score (TF-IDF cosine similarity) and the exact keywords missing from the
resume. Free score, $9 upsell for a "detailed report" (rewritten bullet
points closing every gap).

**Why this can make money fast**
- Massive, constantly-renewing market: everyone job-hunting, all the time.
- Zero marginal cost per use — pure margin after the first sale.
- Distribution is free: post before/after screenshots on r/resumes,
  r/jobs, TikTok, LinkedIn. The product IS the marketing content.
- No inventory, no shipping, no support burden.

**Run the POC**
```bash
cd 1_resume_job_matcher
pip install -r requirements.txt
python matcher.py          # CLI demo on the sample resume/job
python app.py               # web version at http://localhost:5000
```

**Path to first $ (this week)**
1. Deploy `app.py` to Render/Fly.io free tier (or just Replit).
2. Create a Stripe Payment Link for "$9 detailed report", drop the URL into
   `STRIPE_PAYMENT_LINK` in `app.py`.
3. Post 3 "I checked my resume against a real job posting and scored 25%,
   here's what was missing" screenshots on relevant subreddits/LinkedIn,
   linking to the free tool.
4. Manually deliver the "detailed" report (rewrite the top 5 bullets using
   the missing keywords) for the first ~20 orders — automate only once
   demand is proven.

**Pricing:** $9 one-time report, or $19/mo unlimited checks + rewrites for
active job seekers (bundle of ~10 resumes to $99/mo for career coaches /
bootcamps who want to offer this to every student).
