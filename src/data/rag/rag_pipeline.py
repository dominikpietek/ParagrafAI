from embeddings import embed
import chromadb

client = chromadb.PersistentClient(path="chroma")
collection = client.get_collection(name="przepisy")

q = embed(["ile dni urlopu mi przysługuje?"])
res = collection.query(query_embeddings=q, n_results=3)

for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
    print(round(dist, 3), "|", meta["act"], meta["article"], "|", doc[:80])