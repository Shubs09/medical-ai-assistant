from rag.retriever import retrieve_context
from llm.gemini import ask_gemini


def rag_answer(question):

    docs = retrieve_context(question)

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

    return response


if __name__ == "__main__":

    question = input("Ask Question: ")

    answer = rag_answer(question)

    print("\nAnswer:\n")
    print(answer)