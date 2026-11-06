import requests
import yaml
import os

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

def generate(messages: list[dict]) -> str:
    print("Start prompt ollama")
    response = requests.post(f"{OLLAMA_URL}/api/chat", json={
        "model": "paragrafLLM",
        "messages": messages,
        "stream": False,
            # "options": {
            #     "temperature": 0,
            #     "num_predict": 10000,
            #     "num_ctx": 4096,
            # }
    })
    response = response.json()["message"]["content"]
    response = response.strip().removeprefix("```yaml").removesuffix("```")
    response = yaml.safe_load(response)
    return response
