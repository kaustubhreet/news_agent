from news_agent.utils.cleaner import deduplicate
from news_agent.services.memory_service import filter_new_articles
from news_agent.services.ranking_service import rank_articles
from news_agent.services.llm_service import summarize
from news_agent.services.notification_service import send_all
from news_agent.utils.formatter import format_news
from news_agent.services.rss_service import fetch_articles
from news_agent.core.config import RSS_FEEDS
from news_agent.utils.logger import logger
from news_agent.services.memory_service import update_memory, update_trends

def fetch_node(state):
    logger.info(f"Fetching articles... {state}")
    articles = fetch_articles(RSS_FEEDS)
    logger.info(f"Fetched {len(articles)} articles")
    return {"articles": articles}

def filter_node(state):
    logger.info("Filter node...")
    articles = state["articles"]

    articles = deduplicate(articles)
    logger.info("Filter node filter_new_articles start")
    articles = filter_new_articles(articles)

    return {"filtered_articles": articles}

def rank_node(state):
    logger.info("rank node...")
    ranked = rank_articles(state["filtered_articles"])
    return {"ranked_articles": ranked}

def summarize_node(state):
    logger.info("summarize node")
    summaries = []

    for i, article in enumerate(state["ranked_articles"][:25]):
        logger.info(f"Summarizing {i+1}")

        try:
            short = summarize(article.summary)

            summaries.append({
                "title": article.title,
                "summary": short
            })

        except Exception as e:
            logger.error(f"Error in summarize_node: {e}")
            logger.error(f"Article summary: {article.summary[:200]}")
            continue

    return {"summaries": summaries}

def critic_node(state):
    summaries = state["summaries"]

    # simple filter (can upgrade later)
    clean = [s for s in summaries if len(s["summary"]) > 10]

    return {"summaries": clean}

def notify_node(state):
    message = format_news(state["summaries"])
    send_all(message)

    return state

def memory_node(state):
    logger.info("Updating memory...")

    summaries = state["summaries"]

    update_memory(summaries)
    update_trends(summaries)

    logger.info("Memory updated successfully")

    return state