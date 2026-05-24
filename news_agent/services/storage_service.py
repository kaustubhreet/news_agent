import os
from datetime import datetime
from news_agent.utils.logger import logger

def save_news(news):
    os.makedirs("data/processed", exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    file_path = f"data/processed/{today}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        for n in news:
            f.write(n["summary"] + "\n")

    logger.info(f"News saved to {file_path}")