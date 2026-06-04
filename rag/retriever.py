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


def retrieve_context(query, k=3):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]


if __name__ == "__main__":

    query = input("Ask Question: ")

    docs = retrieve_context(query)

    print("\nRetrieved Chunks:\n")

    for i, doc in enumerate(docs, start=1):
        print(f"\nChunk {i}:\n")
        print(doc)