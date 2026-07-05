"""ResumeFit - minimal Flask front-end for the matcher.

Run: python app.py, then open http://localhost:5000
This is the sellable surface: a free score + a paywalled "detailed report"
button (Stripe Checkout link goes where STRIPE_PAYMENT_LINK is marked).
"""
from flask import Flask, render_template_string, request

from matcher import match_score

app = Flask(__name__)

STRIPE_PAYMENT_LINK = "https://buy.stripe.com/REPLACE_ME"

PAGE = """
<!doctype html>
<title>ResumeFit - Instant ATS Match Score</title>
<style>
 body { font-family: sans-serif; max-width: 720px; margin: 40px auto; }
 textarea { width: 100%; height: 160px; }
 .score { font-size: 48px; font-weight: bold; color: {{ '#2e7d32' if score and score >= 70 else '#c62828' }}; }
 .kw { display:inline-block; background:#eee; padding:2px 8px; margin:2px; border-radius:4px; }
 .missing { background:#ffe0e0; }
 .cta { background:#5b21b6; color:white; padding:12px 20px; border:none; border-radius:6px; font-size:16px; }
</style>
<h1>ResumeFit</h1>
<p>Paste your resume and a job description. Get an instant ATS match score.</p>
<form method="post">
  <label>Resume text</label>
  <textarea name="resume">{{ resume or '' }}</textarea>
  <label>Job description</label>
  <textarea name="job">{{ job or '' }}</textarea>
  <br><br>
  <button type="submit">Check my match score</button>
</form>
{% if score is not none %}
  <h2>Your match score</h2>
  <div class="score">{{ score }}%</div>
  <p><b>Matched keywords:</b><br>
  {% for k in matched %}<span class="kw">{{ k }}</span>{% endfor %}</p>
  <p><b>Missing keywords (add these to your resume):</b><br>
  {% for k in missing %}<span class="kw missing">{{ k }}</span>{% endfor %}</p>
  <hr>
  <p>Want a full rewrite of your bullet points to close every gap?</p>
  <a class="cta" href="{{ stripe_link }}">Get the $9 detailed report &rarr;</a>
{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def index():
    score = matched = missing = None
    resume = job = ""
    if request.method == "POST":
        resume = request.form.get("resume", "")
        job = request.form.get("job", "")
        if resume.strip() and job.strip():
            result = match_score(resume, job)
            score = result["score_pct"]
            matched = result["matched_keywords"]
            missing = result["missing_keywords"]
    return render_template_string(
        PAGE, score=score, matched=matched, missing=missing,
        resume=resume, job=job, stripe_link=STRIPE_PAYMENT_LINK,
    )


if __name__ == "__main__":
    app.run(debug=True)
