import json
import os,re
from collections import Counter
from news_agent.utils.logger import logger

MEMORY_FILE = "data/memory/history.json"
TREND_FILE = "data/memory/trends.json"

STOPWORDS = {
    "the", "is", "and", "to", "of", "in", "on", "for",
    "a", "an", "with", "by", "at", "from", "as", "it"
}

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    
    try:
        with open(MEMORY_FILE, "r") as f:
            content = f.read().strip()

            if not content:
                logger.warning("Memory file empty, returning []")
                return []

            return json.loads(content)

    except Exception as e:
        logger.error(f"Memory load failed: {e}")
        return []

def save_memory(data):
    os.makedirs("data/memory", exist_ok=True)

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def filter_new_articles(articles):
    history = load_memory()

    seen_titles = {h["title"].lower() for h in history}

    new_articles = []

    for a in articles:
        if a.title.lower() not in seen_titles:
            new_articles.append(a)

    return new_articles

def update_memory(news):
    history = load_memory()

    for n in news:
        history.append({
            "title": n["title"]
        })

    # keep only last 200 items
    history = history[-200:]

    save_memory(history)

def update_trends(news):
    words = []

    for n in news:
        text = (n["title"] + " " + n["summary"]).lower()

        # remove punctuation
        text = re.sub(r"[^\w\s]", "", text)

        for word in text.split():
            if len(word) > 3 and word not in STOPWORDS:
                words.append(word)

    counter = Counter(words)

    trends = dict(counter.most_common(25))

    os.makedirs("data/memory", exist_ok=True)

    with open(TREND_FILE, "w") as f:
        json.dump(trends, f, indent=2)

    logger.info(f"Trends updated: {list(trends.keys())[:5]}")