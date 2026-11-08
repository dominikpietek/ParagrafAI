import requests
import yaml
import os
from fastapi import HTTPException

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

def generate(messages: list[dict]) -> str:
    print("Start prompt ollama")
    try:
        response = requests.post(f"{OLLAMA_URL}/api/chat", json={
            "model": "paragrafLLM",
            "messages": messages,
            "stream": False
        }, timeout=120)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail="Błąd ollama")

    try:
        response = response.json()["message"]["content"]
        response = response.strip().removeprefix("```yaml").removesuffix("```")
        response = yaml.safe_load(response)
    except KeyError as e:
        raise HTTPException(status_code=502, detail="Yaml był niepoprawny")
    
    return response
