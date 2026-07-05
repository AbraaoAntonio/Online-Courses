# 5. CourseClip — Auto Show Notes & Quizzes for Course Creators

**The problem:** Course creators and YouTubers (this repo's owner already
has an entire course-video back catalog!) spend hours writing show notes,
blog recaps, and quiz questions for content they've already recorded.

**The product:** Paste a transcript, get back an extractive summary
(show notes / blog recap) and an auto-generated fill-in-the-blank quiz —
built on the same TF-IDF techniques already used elsewhere in this repo's
NLP sections.

**Why this can make money fast**
- You are the first customer: run it on your own existing YouTube/Udemy
  video transcripts to instantly generate blog posts + quizzes, which
  themselves drive more traffic/signups to your other paid products above.
- Sell to other course creators and corporate L&D teams who record
  training videos and need quizzes for compliance/completion tracking.
- Transcripts are usually already available for free (YouTube auto-captions,
  Udemy transcripts) — no expensive data collection.

**Run the POC**
```bash
cd 5_course_content_repurposer
pip install -r requirements.txt
python repurpose.py     # prints a summary + quiz from sample_transcript.txt
```

**Path to first $ (this week)**
1. Run it against transcripts of your own existing YouTube playlist videos,
   publish the generated show notes/blog recaps to drive SEO traffic back
   to your other tools (ResumeFit, InstantInsights, etc.) — free
   distribution flywheel.
2. Offer it as a $15/video service on Fiverr/Upwork to other course
   creators and YouTubers ("show notes + quiz from your video, 24h
   turnaround").
3. Pitch corporate training / L&D teams a $199/mo plan: batch-process
   their training video library into quizzes for compliance tracking.

**Pricing:** $15/video one-off, $49/mo for creators publishing weekly
(≈4 videos), $199/mo for teams processing a whole training library.
