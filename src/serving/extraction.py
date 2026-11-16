import requests
import yaml
from fastapi import HTTPException
import config

def extract_from_judgment(messages: list[dict]) -> str:
    print("Start prompt ollama")
    try:
        response = requests.post(f"{config.OLLAMA_URL}/api/chat", json={
            "model": config.EXTRACT_MODEL,
            "messages": messages,
            "stream": False
        }, timeout=120)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail="Błąd ollama")
    print("End prompt ollama")
    try:
        response = response.json()["message"]["content"]
        response = response.strip().removeprefix("```yaml").removesuffix("```")
        response = yaml.safe_load(response)
    except KeyError as e:
        raise HTTPException(status_code=502, detail="Yaml był niepoprawny")
    print("Ollama response parsed")
    return response
