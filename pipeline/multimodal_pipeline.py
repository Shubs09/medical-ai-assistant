from speech.speech_to_text import transcribe_audio
from llm.gemini_vision import analyze_image


def run_pipeline(audio_path, image_path):

    question = transcribe_audio(audio_path)

    print("\nQuestion from Audio:")
    print(question)

    response = analyze_image(image_path, question)

    return response