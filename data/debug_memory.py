import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test 1: raw JSON parsing
print("=== Test 1: Raw JSON ===")
with open('data/memory/history.json') as f:
    data = json.load(f)
print(f"Total entries: {len(data)}")
print(f"First entry keys: {list(data[0].keys())}")

# Test 2: load_memory function
print("\n=== Test 2: load_memory() ===")
from news_agent.services.memory_service import load_memory
h = load_memory()
print(f"Loaded {len(h)} entries")

# Test 3: filter_new_articles
print("\n=== Test 3: filter_new_articles ===")
from news_agent.models.article import Article
from news_agent.services.memory_service import filter_new_articles

known_article = Article(
    title="Aura's impressive e-ink photo frame doesn't even look digital",
    summary="test",
    source="https://techcrunch.com/feed/",
    normalized_title="aura's impressive e-ink photo frame doesn't even look digital",
    content_hash=""
)
result = filter_new_articles([known_article])
print(f"Known article filtered: {len(result)} new (should be 0)")

new_article = Article(
    title="Totally brand new unique article 123456789",
    summary="brand new content",
    source="https://techcrunch.com/feed/",
    normalized_title="totally brand new unique article 123456789",
    content_hash=""
)
result2 = filter_new_articles([new_article])
print(f"New article filtered: {len(result2)} new (should be 1)")