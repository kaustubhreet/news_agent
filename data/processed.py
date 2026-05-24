from datetime import datetime

def save_news(news):
    today = datetime.now().strftime("%Y-%m-%d")

    with open(f"data/processed/{today}.txt", "w") as f:
        for n in news:
            f.write(n['summary'] + "\n")