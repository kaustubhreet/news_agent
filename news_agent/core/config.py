import os
from dotenv import load_dotenv

load_dotenv()

RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://www.wired.com/feed/rss",
    "https://www.engadget.com/rss.xml",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.reddit.com/r/technology/.rss",
    "https://www.producthunt.com/feed",
    "https://news.ycombinator.com/rss"
    "https://hnrss.org/frontpage",
    "https://www.theverge.com/rss/index.xml"
]

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PHONE_NO = os.getenv("PHONE_NO")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")
HF_API_KEY = os.getenv("HF_API_KEY")