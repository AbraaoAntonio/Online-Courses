"""InstantInsights - Flask upload endpoint that returns the HTML report.

Run: python app.py, open http://localhost:5001, upload a CSV.
Monetization surface: gate the /report route behind a Stripe Checkout
success redirect, or offer 1 free report then require payment.
"""
import os
import tempfile

from flask import Flask, render_template_string, request

from report import generate_report

app = Flask(__name__)

UPLOAD_PAGE = """
<!doctype html>
<title>InstantInsights - Automated Data Report</title>
<style>body{font-family:sans-serif;max-width:600px;margin:60px auto;}</style>
<h1>InstantInsights</h1>
<p>Upload a CSV, get a full exploratory-data-analysis report in seconds.</p>
<form method="post" enctype="multipart/form-data" action="/report">
  <input type="file" name="csv_file" accept=".csv" required>
  <button type="submit">Generate report ($19 value - free preview)</button>
</form>
"""


@app.route("/")
def index():
    return render_template_string(UPLOAD_PAGE)


@app.route("/report", methods=["POST"])
def report():
    file = request.files["csv_file"]
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        file.save(tmp.name)
        path = tmp.name
    try:
        html = generate_report(path)
    finally:
        os.unlink(path)
    return html


if __name__ == "__main__":
    app.run(debug=True, port=5001)
