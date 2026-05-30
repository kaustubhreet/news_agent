import os
from dotenv import load_dotenv

load_dotenv()

RSS_FEEDS = [
    # --- Your Existing General & Consumer Tech Feeds ---
    "https://techcrunch.com/feed/",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://www.wired.com/feed/rss",
    "https://www.engadget.com/rss.xml",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.producthunt.com/feed",
    "https://www.theverge.com/rss/index.xml",
    
    # --- Aggregators & Hacker Forums (Fixed syntax comma from original) ---
    "https://news.ycombinator.com/rss",
    "https://hnrss.org/frontpage",
    "https://hnrss.org/newest?q=LLM+OR+Agent+OR+OpenAI+OR+Anthropic+OR+HuggingFace", # Targeted HN AI filter

    # --- Reddit Developer & Open-Weights Communities ---
    "https://www.reddit.com/r/LocalLLMA/.rss",          # Crucial for open-source LLMs & fine-tunes
    "https://www.reddit.com/r/MachineLearning/.rss",     # Core ML/Agent research drops
    "https://www.reddit.com/r/ArtificialIntelligence/.rss",
    "https://www.reddit.com/r/technology/.rss",          # Your original general technology feed

    # --- Primary AI Lab & Open Source Ecosystem Feeds ---
    "https://huggingface.co/blog/feed.xml",              # Hub for open models & framework releases
    "https://openai.com/news/rss.xml",                   # Official OpenAI releases
    "https://deepmind.google/blog/rss.xml",              # Google DeepMind frontier models
    "https://aws.amazon.com/blogs/machine-learning/feed/", # Bedrock updates & agent toolchains
    
    # --- Specialized AI Engineering & Media Publications ---
    "https://www.unite.ai/feed/",                        # High-frequency focus on specialized AI tooling
    "https://www.infoq.com/feed/AI-ML-Data-Engineering/" # Architecture & production deployment of agents
]

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PHONE_NO = os.getenv("PHONE_NO")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")
HF_API_KEY = os.getenv("HF_API_KEY")
