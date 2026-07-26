from speech.speech_to_text import transcribe_audio
from rag.retriever import retrieve_context
from llm.gemini_vision import analyze_image


def run_medical_pipeline(question=None, audio_path=None, image_path=None):

    # If no typed question is provided, use Whisper
    if not question:

        question = transcribe_audio(audio_path)

        if not question or question.strip() == "":
            return {
                "question": "",
                "response": "❌ Could not detect speech in the audio. Please try again.",
                "sources": []
            }

    print("\nQuestion:")
    print(question)

    # =====================================
    # Image Query (Vision Only)
    # =====================================
    if image_path is not None:

        print("\nVision Mode")

        final_response = analyze_image(
            image_path=image_path,
            question=question,
            context=""
        )

        print("\nFinal Response Generated")

        return {
            "question": question,
            "response": final_response,
            "sources": []
        }

    # =====================================
    # Text / Voice Query (RAG)
    # =====================================
    print("\nKnowledge Mode (RAG)")

    result = retrieve_context(question)

    # Reject if no relevant medical knowledge is found
    if not result["is_relevant"]:
        return {
            "question": question,
            "response": (
                "❌ I couldn't find relevant information about this topic "
                "in the current medical knowledge base.\n\n"
                "Please ask a question related to the available medical documents."
            ),
            "sources": []
        }

    docs = result["documents"]
    sources = result["sources"]

    context = "\n\n".join(docs)

    print("\nMedical Context Retrieved")

    final_response = analyze_image(
        image_path=None,
        question=question,
        context=context
    )

    print("\nFinal Response Generated")

    return {
        "question": question,
        "response": final_response,
        "sources": sources
    }