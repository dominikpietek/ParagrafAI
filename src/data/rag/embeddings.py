import os
import requests

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

def embed(texts: list[str]) -> list[list[float]]:
    response = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={"model": "bge-m3", "input": texts},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["embeddings"]
