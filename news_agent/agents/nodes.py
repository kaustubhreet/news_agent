from news_agent.utils.cleaner import deduplicate
from news_agent.services.memory_service import filter_new_articles
from news_agent.services.ranking_service import rank_articles
from news_agent.services.llm_service import summarize, summarize_batch
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
    logger.info("summarize node (batched mode)")
    summaries = []

    # Take top 25 articles
    articles = state["ranked_articles"][:25]
    total = len(articles)

    # Convert Article objects to dicts for batch processing
    batch_input = []
    for art in articles:
        batch_input.append({
            "title": art.title,
            "summary": art.summary
        })

    # Process in batches of 5
    batch_size = 5
    for batch_start in range(0, total, batch_size):
        batch_end = min(batch_start + batch_size, total)
        batch = batch_input[batch_start:batch_end]
        batch_nums = f"{batch_start+1}-{batch_end}"

        logger.info(f"Summarizing batch {batch_nums} ({len(batch)} articles)")

        try:
            batch_results = summarize_batch(batch)

            for idx, short in enumerate(batch_results):
                article_idx = batch_start + idx
                if not short or len(short.strip()) < 10:
                    logger.warning(f"Skipping article {article_idx+1}: empty or invalid summary")
                    continue

                summaries.append({
                    "title": articles[article_idx].title,
                    "summary": short.strip()
                })

        except Exception as e:
            logger.error(f"Error summarizing batch {batch_nums}: {e}")
            # Mark all articles in this batch as skipped
            for idx in range(len(batch)):
                article_idx = batch_start + idx
                logger.warning(f"Skipping article {article_idx+1} due to batch failure")
            continue

    logger.info(f"Valid summaries: {len(summaries)} out of {total} articles")
    return {"summaries": summaries}

def critic_node(state):
    summaries = state["summaries"]

    # Filter out summaries that are empty, too short, or contain error/invalid indicators
    clean = []
    for s in summaries:
        summary_text = s["summary"]
        if not summary_text or len(summary_text.strip()) < 10:
            logger.warning(f"critic_node filtering out short/empty summary for: {s.get('title', 'unknown')[:50]}")
            continue
        clean.append(s)

    logger.info(f"critic_node: {len(clean)} valid summaries out of {len(summaries)}")
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