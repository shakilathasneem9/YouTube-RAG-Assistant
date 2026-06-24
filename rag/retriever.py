from rag.embedder import create_embedding
from rag.vectorstore import search

def retrieve(query):
    embedding = create_embedding(query)

    results = search(
        embedding,
        k=5 #Find 5 most similar chunks in my stored transcript
    )

    return [
        item["text"]
        for item in results
    ]