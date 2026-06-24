import json
import os, re, hashlib
from collections import Counter
from news_agent.utils.logger import logger
from news_agent.utils.cleaner import normalize_title

MEMORY_FILE = "data/memory/history.json"
TREND_FILE = "data/memory/trends.json"

STOPWORDS = {
    "the", "is", "and", "to", "of", "in", "on", "for",
    "a", "an", "with", "by", "at", "from", "as", "it"
}

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        logger.info("No memory file found, starting fresh")
        return []
    
    try:
        with open(MEMORY_FILE, "r") as f:
            content = f.read().strip()

            if not content:
                logger.warning("Memory file empty, returning []")
                return []

            data = json.loads(content)
            
            # Validate that data is a list
            if not isinstance(data, list):
                logger.error(f"Memory file corrupted: expected list, got {type(data).__name__}")
                return []
            
            # Normalize all stored titles on load (for backward compat)
            for item in data:
                if not isinstance(item, dict):
                    logger.warning(f"Skipping non-dict entry in memory: {item}")
                    continue
                if "normalized" not in item:
                    item["normalized"] = normalize_title(item.get("title", "")).lower()
                # Ensure content_hash field exists
                if "content_hash" not in item:
                    # Compute hash from title for backward compat
                    raw = normalize_title(item.get("title", "")).lower()
                    item["content_hash"] = hashlib.md5(raw.encode('utf-8')).hexdigest()
            
            logger.info(f"Loaded {len(data)} entries from memory")
            return data

    except json.JSONDecodeError as e:
        # CRITICAL: Log the error clearly instead of silently returning []
        logger.error(f"CRITICAL: Memory file corrupted (JSON parse error): {e}")
        logger.error(f"Attempting to repair memory file...")
        
        # Try to repair: read raw, remove non-JSON garbage, re-parse
        try:
            with open(MEMORY_FILE, "r") as f:
                raw = f.read()
            
            # Remove git merge conflict markers
            raw = re.sub(r'<<<<<<<.*?\n', '', raw)
            raw = re.sub(r'=======\n', '', raw)
            raw = re.sub(r'>>>>>>>.*?\n', '', raw)
            
            data = json.loads(raw)
            if isinstance(data, list):
                logger.info(f"Memory file repaired successfully, loaded {len(data)} entries")
                # Save repaired version
                with open(MEMORY_FILE + ".repaired", "w") as f:
                    json.dump(data, f, indent=2)
                return data
        except Exception as repair_err:
            logger.error(f"Memory file repair failed: {repair_err}")
        
        return []

    except Exception as e:
        logger.error(f"Memory load failed: {e}")
        return []

def save_memory(data):
    os.makedirs("data/memory", exist_ok=True)

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def filter_new_articles(articles):
    """Filter articles by checking if they already exist in memory.
    Uses BOTH normalized title AND content_hash for cross-feed dedup."""
    history = load_memory()
    
    if not history:
        logger.info("No history to filter against, all articles are new")
        return articles

    seen_titles = set()
    seen_hashes = set()
    
    for h in history:
        if not isinstance(h, dict):
            continue
        n = h.get("normalized") or normalize_title(h.get("title", "")).lower()
        seen_titles.add(n)
        ch = h.get("content_hash", "")
        if ch:
            seen_hashes.add(ch)

    new_articles = []
    skipped_count = 0

    for a in articles:
        # Use the article's pre-computed fields (set in rss_service)
        normalized = a.normalized_title if a.normalized_title else normalize_title(a.title).lower()
        content_hash = a.content_hash if a.content_hash else ""
        
        # Check both title and content hash
        title_seen = normalized in seen_titles
        hash_seen = content_hash and content_hash in seen_hashes
        
        if not title_seen and not hash_seen:
            new_articles.append(a)
        else:
            skipped_count += 1
            if skipped_count <= 3:
                reason = "title" if title_seen else "content_hash"
                logger.info(f"Filtered out (by {reason}): {a.title[:70]}")

    logger.info(f"filter_new_articles: {len(new_articles)} new out of {len(articles)} total ({skipped_count} filtered)")
    return new_articles

def update_memory(news):
    history = load_memory()
    
    existing_titles = {h.get("normalized", "") for h in history if isinstance(h, dict)}
    existing_hashes = {h.get("content_hash", "") for h in history if isinstance(h, dict) and h.get("content_hash")}

    new_count = 0
    for n in news:
        normalized = normalize_title(n["title"]).lower()
        
        # Compute title-based hash for backward compat
        raw = normalize_title(n["title"]).lower()
        content_hash = hashlib.md5(raw.encode('utf-8')).hexdigest()
        
        if normalized not in existing_titles and content_hash not in existing_hashes:
            existing_titles.add(normalized)
            existing_hashes.add(content_hash)
            history.append({
                "title": n["title"],
                "normalized": normalized,
                "content_hash": content_hash
            })
            new_count += 1

    logger.info(f"update_memory: added {new_count} new entries (total: {len(history)})")
    
    # Keep only last 500 items
    if len(history) > 500:
        history = history[-500:]

    save_memory(history)

def update_memory_attempts(articles):
    """Store articles that were sent for LLM summarization (regardless of success/failure).
    This prevents re-fetching the same articles when the LLM is temporarily down."""
    history = load_memory()

    existing_titles = {h.get("normalized", "") for h in history if isinstance(h, dict)}
    existing_hashes = {h.get("content_hash", "") for h in history if isinstance(h, dict) and h.get("content_hash")}

    new_count = 0
    for a in articles:
        normalized = a.normalized_title if hasattr(a, 'normalized_title') and a.normalized_title else normalize_title(a.title).lower()
        content_hash = a.content_hash if hasattr(a, 'content_hash') and a.content_hash else ""
        
        if not content_hash:
            raw = normalize_title(a.title).lower()
            content_hash = hashlib.md5(raw.encode('utf-8')).hexdigest()
        
        if normalized not in existing_titles and content_hash not in existing_hashes:
            existing_titles.add(normalized)
            existing_hashes.add(content_hash)
            history.append({
                "title": a.title,
                "normalized": normalized,
                "content_hash": content_hash
            })
            new_count += 1

    logger.info(f"update_memory_attempts: added {new_count} new entries")
    
    # Keep only last 500 items
    if len(history) > 500:
        history = history[-500:]

    save_memory(history)
    logger.info(f"Stored {len(articles)} attempted articles in memory")

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