import requests
import yaml

def generate(messages: list[dict]) -> str:
    print("Start prompt ollama")
    response = requests.post("http://localhost:11434/api/chat", json={
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
