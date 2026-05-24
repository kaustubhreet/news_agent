import requests
from news_agent.utils.logger import logger
from news_agent.core.config import OLLAMA_URL, MODEL_NAME

def summarize(text):
    prompt = f"""
    Summarize this tech news in 1 short line (max 20 words).
    Focus on impact.

    {text}
    """
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        # 🔥 check raw response first
        if not response.text.strip():
            logger.error("Empty response from Ollama")
            return "⚠️ No summary available"

        logger.info(f"Ollama raw response: {response.text[:200]}")
        data = response.json()

        return data.get("response", "⚠️ No summary")

    except Exception as e:
        logger.error(f"LLM error: {e}")
        return "⚠️ LLM failed"