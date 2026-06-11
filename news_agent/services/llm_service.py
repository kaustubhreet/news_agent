import json
import requests
import re
from news_agent.utils.logger import logger
from news_agent.core.config import (
    OLLAMA_URL,
    MODEL_NAME,
    HF_API_KEY,
    MODEL_PROVIDER
)

HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
MODELS = [
    "deepseek-ai/DeepSeek-V4-Flash:novita",
    "Qwen/Qwen2.5-7B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3"
]

def hf_summarize_with_fallback(prompt):
    for model in MODELS:
        try:
            logger.info(f"Trying model: {model}")

            response = requests.post(
                "https://router.huggingface.co/v1/chat/completions",
                headers={"Authorization": f"Bearer {HF_API_KEY}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=30
            )

            data = response.json()

            if "error" in data:
                continue

            choices = data.get("choices", [])
            if choices:
                return choices[0]["message"]["content"]

        except:
            continue

    return ""


def _call_llm(prompt):
    """Internal helper: send a prompt to the configured LLM and return the raw response text."""
    try:
        if MODEL_PROVIDER == "ollama":
            logger.info("Using Ollama model")
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            if not response.text.strip():
                logger.error("Empty response from Ollama")
                return ""
            data = response.json()
            return data.get("response", "")

        elif MODEL_PROVIDER == "hf":
            logger.info("Using HuggingFace model")
            return hf_summarize_with_fallback(prompt)

        else:
            logger.error(f"Invalid MODEL_PROVIDER: {MODEL_PROVIDER}")
            return ""

    except Exception as e:
        logger.error(f"LLM call error: {e}")
        return ""


def summarize(text):
    """Summarize a single article (legacy, kept for compatibility)."""
    prompt = f"""
    Summarize this tech news in 1 short line (max 50 words).
    Focus on impact.

    {text}
    """
    return _call_llm(prompt)


def summarize_batch(articles):
    """
    Summarize a batch of articles (up to 5) in a single LLM call.
    
    Args:
        articles: list of dicts with 'title' and 'summary' keys
        
    Returns:
        list of summary strings, same length as input (empty string for failures)
    """
    if not articles:
        return []

    # Build a single prompt with all articles numbered
    parts = []
    for i, art in enumerate(articles, 1):
        parts.append(f"Article {i}:\nTitle: {art['title']}\nContent: {art['summary'][:500]}")
    
    batch_text = "\n\n".join(parts)
    
    prompt = f"""You are a tech news summarizer. Below are {len(articles)} tech articles.

For EACH article, write ONE short summary line (max 50 words each). Focus on impact.
Number your responses exactly as shown.

{batch_text}

Now write your summaries (one per line, numbered 1 to {len(articles)}):"""

    response = _call_llm(prompt)
    
    if not response:
        logger.warning(f"Empty response for batch of {len(articles)} articles")
        return [""] * len(articles)

    logger.info(f"Batch response received ({len(response)} chars)")

    # Parse numbered summaries from the response
    # Look for patterns like "1. summary" or "1: summary" or "1) summary"
    results = []
    for i in range(1, len(articles) + 1):
        # Try multiple patterns for flexibility
        patterns = [
            rf"(?:^|\n)\s*{i}[.)]\s*(.+?)(?=\n\s*{i+1}[.)]\s*|\n?\s*$)",
            rf"(?:^|\n)\s*{i}[:)\-]\s*(.+?)(?=\n\s*{i+1}[:)\-]\s*|\n?\s*$)",
        ]
        
        summary = ""
        for pattern in patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                summary = match.group(1).strip()
                break
        
        # Fallback: split by newlines and find the line starting with the number
        if not summary:
            for line in response.split("\n"):
                line = line.strip()
                if re.match(rf"^{i}[.)]\s*", line):
                    summary = re.sub(rf"^{i}[.)]\s*", "", line).strip()
                    break
        
        if summary:
            results.append(summary)
        else:
            logger.warning(f"Could not parse summary #{i} from batch response")
            results.append("")

    return results