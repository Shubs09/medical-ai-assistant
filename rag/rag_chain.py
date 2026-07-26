from rag.retriever import retrieve_context
from llm.gemini import ask_gemini


def rag_answer(question):

    result = retrieve_context(question)

    docs = result["documents"]

    sources = result["sources"]

    context = "\n\n".join(docs)

    prompt = f"""
You are a helpful medical AI assistant.

Use ONLY the provided medical context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ask_gemini(prompt)

    return {
        "answer": response,
        "sources": sources
    }


if __name__ == "__main__":

    question = input("Ask Question: ")

    result = rag_answer(question)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nSources:\n")

    for source in result["sources"]:
        print(source)