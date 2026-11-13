import requests
import os
import chromadb
from fastapi import HTTPException
import config
import prompts

CLIENT = chromadb.PersistentClient(path=config.CHROMA_PATH)
COLLECTION = CLIENT.get_collection(name="przepisy")

EMBEDDING_THRESHOLD = 0.35

def embed(texts: list[str]) -> list[list[float]]:
    response = requests.post(
        f"{config.OLLAMA_URL}/api/embed",
        json={"model": "bge-m3", "input": texts},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["embeddings"]

def retrieve(question: str, k: int = 3) -> list[dict]:
    qestion_embeded = embed([question])
    response = COLLECTION.query(query_embeddings=qestion_embeded, n_results=k)
    results = []
    for doc, meta, dist in zip(response["documents"][0], response["metadatas"][0], response["distances"][0]):
        results.append({
            "text": doc,
            "act": meta["act"],
            "article": meta["article"],
            "distance": dist,
        })
    return results

def prepare_prompt(text: str) -> str:
    text = text.replace(prompts.DELIMITER, "")
    embeddings = retrieve(text, 3)
    formatted_embeddings = ""
    for act in embeddings:
        if act["distance"] <= EMBEDDING_THRESHOLD:
            formatted_embeddings += f"{act['act']},{act['article']}\n{act['text']}\n"

    if formatted_embeddings == "":
        raise HTTPException(status_code=200, detail="Złe dane wejściowe")

    prompt = prompts.PROMPT_RAG.replace("{QUESTION}", text)
    prompt = prompt.replace("{RAG_EMBEDDINGS}", formatted_embeddings)
    return prompt

def generate_rag(text: str) -> str:
    prompt = prepare_prompt(text)
    try:
        response = requests.post(f"{config.OLLAMA_URL}/api/chat", json={
            "model": config.RAG_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }, timeout=120)
        response.raise_for_status()
    except requests.RequestException as e:
        print("PRAWDZIWY BŁĄD:", e)
        raise HTTPException(status_code=503, detail="Błąd ollama")

    return response.json()["message"]["content"]