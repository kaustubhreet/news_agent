import json
import requests
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

def summarize(text):
    prompt = f"""
    Summarize this tech news in 1 short line (max 50 words).
    Focus on impact.

    {text}
    """

    try:
        # =========================
        # 🔥 OLLAMA (LOCAL)
        # =========================
        if MODEL_PROVIDER == "ollama":
            logger.info("Using Ollama model")

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )

            if not response.text.strip():
                logger.error("Empty response from Ollama")
                return ""

            logger.info(f"Ollama raw: {response.text[:150]}")

            data = response.json()
            return data.get("response", "")

        # =========================
        # 🌐 HUGGING FACE (REMOTE)
        # =========================
        elif MODEL_PROVIDER == "hf":
            logger.info("Using HuggingFace model")
            return hf_summarize_with_fallback(prompt)
        # =========================
        # ❌ UNKNOWN PROVIDER
        # =========================
        else:
            logger.error(f"Invalid MODEL_PROVIDER: {MODEL_PROVIDER}")
            return ""

    except Exception as e:
        logger.error(f"LLM error: {e}")
        return ""