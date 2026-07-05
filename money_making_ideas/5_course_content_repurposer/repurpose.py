"""CourseClip - turns a raw lecture/video transcript into sellable assets:
an extractive summary and a fill-in-the-blank quiz.

Built for course creators (like the Udemy videos already recorded in this
repo) who want show notes, blog recaps, and quizzes without spending hours
writing them by hand. Uses TF-IDF sentence scoring, the same technique
covered in this repo's NLP sections.
"""
import re

from sklearn.feature_extraction.text import TfidfVectorizer


def _split_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 0]


def summarize(text: str, n_sentences: int = 4) -> list[str]:
    sentences = _split_sentences(text)
    if len(sentences) <= n_sentences:
        return sentences

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(sentences)
    scores = tfidf.sum(axis=1).A1

    ranked_idx = sorted(range(len(sentences)), key=lambda i: -scores[i])[:n_sentences]
    ranked_idx.sort()
    return [sentences[i] for i in ranked_idx]


def generate_quiz(text: str, n_questions: int = 5) -> list[dict]:
    sentences = _split_sentences(text)
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(sentences)
    vocab = vectorizer.get_feature_names_out()

    questions = []
    used_sentences = set()
    scored = []
    for i, sent in enumerate(sentences):
        row = tfidf[i].toarray()[0]
        if row.max() == 0:
            continue
        top_term_idx = row.argmax()
        scored.append((row[top_term_idx], i, vocab[top_term_idx]))

    scored.sort(key=lambda x: -x[0])
    for score, i, term in scored:
        if i in used_sentences:
            continue
        sentence = sentences[i]
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        if not pattern.search(sentence):
            continue
        blanked = pattern.sub("_____", sentence, count=1)
        questions.append({"question": blanked, "answer": term})
        used_sentences.add(i)
        if len(questions) >= n_questions:
            break
    return questions


if __name__ == "__main__":
    with open("sample_transcript.txt") as f:
        transcript = f.read()

    print("=== Auto-generated summary (show notes) ===")
    for s in summarize(transcript, n_sentences=4):
        print(f"- {s}")

    print("\n=== Auto-generated quiz ===")
    for i, q in enumerate(generate_quiz(transcript, n_questions=5), start=1):
        print(f"{i}. {q['question']}  (answer: {q['answer']})")
