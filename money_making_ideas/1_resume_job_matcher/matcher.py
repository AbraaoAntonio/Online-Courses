"""Core matching logic for ResumeFit.

Scores how well a resume matches a job description using TF-IDF + cosine
similarity (the same NLP techniques covered in this repo's
Machine_Learning_A-Z / Python_for_Data_Science courses), and surfaces the
job-posting keywords the resume is missing so the candidate can add them.
"""
import re
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "is", "are", "was", "were",
    "be", "been", "being", "to", "of", "in", "on", "for", "with", "as",
    "by", "at", "from", "this", "that", "these", "those", "it", "its",
    "your", "you", "we", "our", "their", "will", "should", "would", "can",
}


def _keywords(text, top_n=25):
    words = re.findall(r"[a-zA-Z][a-zA-Z+\-#.]{1,}", text.lower())
    words = [w.strip(".") for w in words if w not in STOPWORDS and len(w) > 2]
    return [w for w, _ in Counter(words).most_common(top_n)]


def match_score(resume_text: str, job_text: str) -> dict:
    """Return match percentage plus missing/matched keyword lists."""
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([resume_text, job_text])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    job_keywords = _keywords(job_text, top_n=30)
    resume_words = set(re.findall(r"[a-zA-Z][a-zA-Z+\-#.]{1,}", resume_text.lower()))

    missing = [kw for kw in job_keywords if kw not in resume_words][:15]
    matched = [kw for kw in job_keywords if kw in resume_words][:15]

    return {
        "score_pct": round(float(score) * 100, 1),
        "matched_keywords": matched,
        "missing_keywords": missing,
    }


if __name__ == "__main__":
    with open("sample_resume.txt") as f:
        resume = f.read()
    with open("sample_job.txt") as f:
        job = f.read()
    result = match_score(resume, job)
    print(f"Match score: {result['score_pct']}%")
    print(f"Matched keywords ({len(result['matched_keywords'])}): {result['matched_keywords']}")
    print(f"Missing keywords ({len(result['missing_keywords'])}): {result['missing_keywords']}")
