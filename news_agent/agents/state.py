from typing import TypedDict, List

class NewsState(TypedDict):
    articles: list
    filtered_articles: list
    ranked_articles: list
    summaries: list