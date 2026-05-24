import requests
import os
import json

# res = requests.post(
#     "http://localhost:11434/api/generate",
#     json={
#         "model": "qwen2.5:1.5b",
#         "prompt": "Hello",
#         "stream": False
#     }
# )

#test HF model
# HF_API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-0.5B-Instruct"
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {"Authorization": "Bearer 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"}
response = requests.post(
                HF_API_URL,
                headers=headers,
                json={"inputs": "Hi"},
                timeout=30,
                model= "deepseek-ai/DeepSeek-V4-Flash:novita",
                stream= True,
            )

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload, stream=True)
#     for line in response.iter_lines():
#         if not line.startswith(b"data:"):
#             continue
#         if line.strip() == b"data: [DONE]":
#             return
#         yield json.loads(line.decode("utf-8").lstrip("data:").rstrip("/n"))

# chunks = query({
#     "messages": [
#         {
#             "role": "user",
#             "content": "What is the capital of France?"
#         }
#     ],
#     "model": "deepseek-ai/DeepSeek-V4-Flash:novita",
#     "stream": True,
# })

# for chunk in chunks:
#     print(chunk["choices"], end="")
print(response.text)