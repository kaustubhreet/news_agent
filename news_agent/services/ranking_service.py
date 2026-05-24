KEYWORDS = [
    "AI", "OpenAI", "Google", "Microsoft",
    "startup", "funding", "India", "Nvidia",
    "LLM", "GPT", "chip", "acquisition", "Layoff", "engineer"
]

SOURCE_WEIGHT = {
    "techcrunch": 5,
    "theverge": 4,
    "hnrss": 2,
    "wired": 3,
    "feeds.feedburner": 3,
    "news.ycombinator": 2,
}

def score_article(article):
    score = 0

    text = (article.title + " " + article.summary).lower()

    # keyword scoring
    for kw in KEYWORDS:
        if kw.lower() in text:
            score += 2

    # source scoring
    for source, weight in SOURCE_WEIGHT.items():
        if source in article.source.lower():
            score += weight

    # length filter (avoid junk)
    if len(article.summary) < 50:
        score -= 2

    return score

from collections import Counter

def detect_trends(articles):
    words = []

    for a in articles:
        words.extend(a.title.lower().split())

    common = Counter(words).most_common(10)

    trending_words = {w for w, _ in common if len(w) > 4}

    return trending_words

def boost_with_trends(article, trending_words):
    score = 0

    for word in trending_words:
        if word in article.title.lower():
            score += 3

    return score

def rank_articles(articles):
    trending_words = detect_trends(articles)

    scored = []

    for article in articles:
        base_score = score_article(article)
        trend_score = boost_with_trends(article, trending_words)

        total_score = base_score + trend_score

        scored.append((article, total_score))

    # sort descending
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    return [a for a, _ in ranked]
