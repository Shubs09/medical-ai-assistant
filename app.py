import gradio as gr

from pipeline.final_medical_pipeline import (
    run_medical_pipeline
)


def predict(audio, image):

    # Check audio
    if audio is None:
        return "❌ Please upload or record an audio file."

    # Check image
    if image is None:
        return "❌ Please upload an image."

    try:

        response = run_medical_pipeline(
            audio_path=audio,
            image_path=image
        )

        # Empty response check
        if not response:
            return "❌ No response generated."

        return response

    except Exception as e:

        print("\nERROR:", e)

        return f"""
❌ Medical AI service error.

Possible reasons:
- Gemini API unavailable
- Invalid image/audio
- Retrieval failure
- Network issue

Technical Error:
{str(e)}
"""


app = gr.Interface(
    fn=predict,

    inputs=[
        gr.Audio(
            sources=["upload", "microphone"],
            type="filepath",
            label="Upload Voice"
        ),

        gr.Image(
            type="filepath",
            label="Upload Image"
        )
    ],

    outputs=gr.Textbox(
        label="Medical AI Response",
        lines=20
    ),

    title="Medical AI Assistant",

    description="""
Upload a voice query and image.

Features:
• Whisper Speech-to-Text
• Medical RAG
• ChromaDB
• Gemini Vision
"""
)

app.launch()