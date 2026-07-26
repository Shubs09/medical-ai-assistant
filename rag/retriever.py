from sentence_transformers import SentenceTransformer
import chromadb

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


client = chromadb.PersistentClient(
    path="rag/chroma_db"
)

collection = client.get_collection(
    name="medical_docs"
)

SIMILARITY_THRESHOLD = 1.05
def retrieve_context(query, k=3):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas","distances"]
    )

    documents = results["documents"][0]
    distances = results["distances"][0]
    is_relevant = len(distances) > 0 and min(distances) <= SIMILARITY_THRESHOLD

    sources = []

    for metadata in results["metadatas"][0]:
        if metadata and "source" in metadata:
            sources.append(metadata["source"])

    return {
        "documents": documents,
        "sources": list(dict.fromkeys(sources)),
        "distances": distances,
        "is_relevant": is_relevant
    }


if __name__ == "__main__":

    query = input("Ask Question: ")

    result = retrieve_context(query)

    print("\nRetrieved Chunks:\n")

    for i, doc in enumerate(result["documents"], start=1):
        print(f"\nChunk {i}:\n")
        print(doc)

    print("\nSources Used:\n")

    for source in result["sources"]:
        print(source)

    print("\nDistances:\n")

    for i, distance in enumerate(result["distances"], start=1):
        print(f"Chunk {i}: {distance:.4f}")