import re
import html

def normalize_title(title):
    """Normalize title by unescaping HTML entities, normalizing unicode, and stripping whitespace."""
    # Unescape HTML entities (e.g. &#8217; -> ', & -> &)
    title = html.unescape(title)
    # Normalize unicode characters (e.g. smart quotes to ASCII)
    title = title.replace('\u2018', "'").replace('\u2019', "'")  # smart single quotes
    title = title.replace('\u201c', '"').replace('\u201d', '"')  # smart double quotes
    title = title.replace('\u2013', '-').replace('\u2014', '--')  # en/em dashes
    title = title.replace('\u2026', '...')  # ellipsis
    # Collapse multiple spaces
    title = re.sub(r'\s+', ' ', title)
    return title.strip()

def deduplicate(articles):
    """Deduplicate articles using both normalized title AND content hash.
    This catches same articles from different feeds (different URLs, same content)."""
    seen_titles = set()
    seen_hashes = set()
    unique = []

    for a in articles:
        # Normalize title before dedup check
        normalized = normalize_title(a.title).lower()
        
        # Use both title and content hash for dedup
        title_key = normalized
        hash_key = a.content_hash if a.content_hash else ""
        
        if title_key not in seen_titles and hash_key not in seen_hashes:
            seen_titles.add(title_key)
            if hash_key:
                seen_hashes.add(hash_key)
            # Store the normalized title back on the article for downstream use
            a.normalized_title = normalized
            unique.append(a)
        else:
            # Log when we skip a duplicate
            reason = "title" if title_key in seen_titles else "content_hash"
            import logging
            logging.getLogger("news_agent").debug(f"Dedup skipped (by {reason}): {a.title[:60]}")

    return unique
