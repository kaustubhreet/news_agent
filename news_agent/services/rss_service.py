import feedparser
import hashlib
from news_agent.models.article import Article
from news_agent.utils.logger import logger
from news_agent.utils.cleaner import normalize_title

def get_entry_summary(entry):
    """Extract summary from feed entry, handling different field names."""
    # Try 'summary' first (most common)
    if hasattr(entry, 'summary'):
        return entry.summary
    
    # Try 'description' as fallback
    if hasattr(entry, 'description'):
        return entry.description
    
    # Try 'content' (some feeds use this)
    if hasattr(entry, 'content') and entry.content and len(entry.content) > 0:
        return entry.content[0].value
    
    # Try 'summary_detail' (Atom feeds)
    if hasattr(entry, 'summary_detail') and entry.summary_detail:
        return entry.summary_detail.get('value', '')
    
    # Last resort: try to get from 'title' if nothing else works
    logger.warning(f"Could not find summary for entry: {entry.get('title', 'Unknown')}")
    return entry.get('title', '')

def get_entry_link(entry):
    """Extract link from feed entry."""
    if hasattr(entry, 'link') and entry.link:
        return entry.link
    if hasattr(entry, 'links') and entry.links:
        for link in entry.links:
            if link.get('rel') == 'alternate' or link.get('type') == 'text/html':
                return link.get('href', '')
        return entry.links[0].get('href', '')
    return ''

def compute_content_hash(title, summary):
    """Compute a hash of title+summary for dedup across feeds."""
    raw = (title + summary).strip().lower()
    raw = normalize_title(raw)
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

def fetch_articles(feeds):
    articles = []

    for url in feeds:
        feed = feedparser.parse(url)

        for entry in feed.entries[:25]:
            try:
                summary = get_entry_summary(entry)
                link = get_entry_link(entry)
                normalized = normalize_title(entry.title).lower()
                content_hash = compute_content_hash(entry.title, summary)
                
                articles.append(
                    Article(
                        title=entry.title,
                        summary=summary,
                        source=url,
                        link=link,
                        normalized_title=normalized,
                        content_hash=content_hash
                    )
                )
            except Exception as e:
                logger.error(f"Error processing entry: {e}")
                continue

    return articles
