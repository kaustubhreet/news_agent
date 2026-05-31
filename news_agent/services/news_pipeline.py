from news_agent.services.rss_service import fetch_articles
from news_agent.services.llm_service import summarize
from news_agent.utils.cleaner import deduplicate
from news_agent.core.config import RSS_FEEDS
from news_agent.services.ranking_service import rank_articles
from news_agent.utils.logger import logger
from news_agent.services.memory_service import filter_new_articles, update_memory

def run_pipeline():
    logger.info("🚀 Pipeline started")
    print("🔍 Fetching articles...")

    articles = fetch_articles(RSS_FEEDS)
    print(f"✅ Articles fetched: {len(articles)}")

    articles = deduplicate(articles)
    print(f"🧹 After dedup: {len(articles)}")

    # filter using memory
    articles = filter_new_articles(articles)
    logger.info(f"After memory filter: {len(articles)}")

    articles = rank_articles(articles)
    logger.info("Ranking completed")

    summarized_news = []

    # only top 25 → reduces LLM calls 🔥
    for i,article in enumerate(articles[:25]):
        logger.info(f"🤖 Summarizing {i+1}: {article.title[:120]}")
        print(f"🤖 Summarizing: {article.title[:120]}")

        short = summarize(article.summary)

        summarized_news.append({
            "title": article.title,
            "summary": short
        })

    # update memory
    update_memory(summarized_news)
    
    print("✅ Pipeline completed")
    logger.info("✅ Pipeline completed")

    return summarized_news