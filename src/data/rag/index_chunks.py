import chromadb
import json
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

def index_chunked_pdfs():
    client = chromadb.PersistentClient(path="chroma")
    collection = client.get_or_create_collection(
        name="przepisy",
        metadata={"hnsw:space": "cosine"},
    )

    print("READ JSONL")
    with open("articles.jsonl", "r", encoding="utf-8") as f:
        articles = [json.loads(l) for l in f]

    print("EMBEDING")
    texts = [art["text"] for art in articles] 
    BATCH = 50
    vectors = []
    for i in range(0, len(texts), BATCH):
        print(f"EMBEDING {((i+1)/len(texts)*100):.3f}%")
        text_slice = texts[i:i + BATCH]
        vectors.extend(embed(text_slice))

    print("SAVING TO VECTOR DATABASE")
    collection.upsert(
        ids=[art["id"] for art in articles],
        documents=texts,
        embeddings=vectors,
        metadatas=[{"act": a["act"], "article": a["article"]} for a in articles],
    )
    print("W bazie:", collection.count())

if __name__ == "__main__":
    index_chunked_pdfs()