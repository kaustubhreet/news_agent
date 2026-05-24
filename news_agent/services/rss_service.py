import feedparser
from news_agent.models.article import Article

def fetch_articles(feeds):
    articles = []

    for url in feeds:
        feed = feedparser.parse(url)

        for entry in feed.entries[:15]:
            articles.append(
                Article(
                    title=entry.title,
                    summary=entry.summary,
                    source=url
                )
            )

    return articles