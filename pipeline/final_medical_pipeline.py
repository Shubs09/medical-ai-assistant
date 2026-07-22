from speech.speech_to_text import transcribe_audio
from rag.retriever import retrieve_context
from llm.gemini_vision import analyze_image


def run_medical_pipeline(audio_path, image_path):

    question = transcribe_audio(audio_path)

    if not question or question.strip() == "":
        return "❌ Could not detect speech in the audio. Please try again."

    print("\nQuestion:")
    print(question)

    docs = retrieve_context(question)

    context = "\n\n".join(docs)

    print("\nMedical Context Retrieved")

    final_response = analyze_image(
        image_path=image_path,
        question=question,
        context=context
    )

    print("\nFinal Response Generated")

    return {
    "question": question,
    "response": final_response
}