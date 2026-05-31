import feedparser
from news_agent.models.article import Article
from news_agent.utils.logger import logger

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

def fetch_articles(feeds):
    articles = []

    for url in feeds:
        feed = feedparser.parse(url)

        for entry in feed.entries[:25]:
            try:
                summary = get_entry_summary(entry)
                articles.append(
                    Article(
                        title=entry.title,
                        summary=summary,
                        source=url
                    )
                )
            except Exception as e:
                logger.error(f"Error processing entry: {e}")
                continue

    return articles
