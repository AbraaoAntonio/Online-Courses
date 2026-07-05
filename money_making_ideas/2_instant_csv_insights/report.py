"""InstantInsights - turns any CSV into an automated EDA report.

Reuses the exploratory-data-analysis workflow from this repo's ML courses
(missing-value checks, correlation heatmaps, distributions) and packages it
as a one-click HTML report anyone can hand to a client or boss.
"""
import base64
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def _fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def generate_report(csv_path: str) -> str:
    df = pd.read_csv(csv_path)
    numeric_df = df.select_dtypes(include="number")

    n_rows, n_cols = df.shape
    missing = df.isna().sum()
    missing_pct = (missing / n_rows * 100).round(1)

    sections = []
    sections.append(f"<h1>InstantInsights Report</h1>")
    sections.append(f"<p><b>{n_rows}</b> rows &times; <b>{n_cols}</b> columns</p>")

    sections.append("<h2>Missing data</h2><table border='1' cellpadding='4'>"
                     "<tr><th>Column</th><th>Missing</th><th>%</th></tr>")
    for col in df.columns:
        sections.append(f"<tr><td>{col}</td><td>{missing[col]}</td>"
                         f"<td>{missing_pct[col]}%</td></tr>")
    sections.append("</table>")

    sections.append("<h2>Summary statistics</h2>")
    sections.append(df.describe(include="all").to_html())

    if numeric_df.shape[1] >= 2:
        sections.append("<h2>Correlation heatmap</h2>")
        corr = numeric_df.corr()
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right")
        ax.set_yticklabels(corr.columns)
        fig.colorbar(im)
        sections.append(f'<img src="data:image/png;base64,{_fig_to_base64(fig)}"/>')

    for col in numeric_df.columns[:6]:
        fig, ax = plt.subplots(figsize=(5, 3))
        df[col].dropna().hist(ax=ax, bins=20)
        ax.set_title(f"Distribution of {col}")
        sections.append(f'<h3>{col}</h3><img src="data:image/png;base64,{_fig_to_base64(fig)}"/>')

    html = "<html><body style='font-family:sans-serif;max-width:900px;margin:auto;'>" \
           + "".join(sections) + "</body></html>"
    return html


if __name__ == "__main__":
    html = generate_report("sample_data.csv")
    with open("report_output.html", "w") as f:
        f.write(html)
    print("Wrote report_output.html")
