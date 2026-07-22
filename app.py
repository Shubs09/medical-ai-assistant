import gradio as gr

from pipeline.final_medical_pipeline import (
    run_medical_pipeline
)


def predict(audio, image):
 
    # Check audio
    if audio is None:
        return "", "❌ Please upload or record an audio file."

  

    try:

        response = run_medical_pipeline(
            audio_path=audio,
            image_path=image
        )

        # Empty response check
        if not response:
            return "", "❌ No response generated."

        return response["question"], response["response"]

    except Exception as e:

        print("\nERROR:", e)

        return "", f"""
❌ Medical AI service error.

Possible reasons:
- Gemini API unavailable
- Invalid image/audio
- Retrieval failure
- Network issue

Technical Error:
{str(e)}
"""


with gr.Blocks(title="🏥 Medical AI Assistant") as app:

    gr.Markdown("""
# 🏥 Medical AI Assistant

Ask medical questions using your voice.

### Features
- 🎤 Whisper Speech-to-Text
- 📚 Medical RAG Knowledge Base
- 🧠 Google Gemini
- 🖼️ Optional Medical Image Analysis
""")

    audio = gr.Audio(
        sources=["upload", "microphone"],
        type="filepath",
    label="🎤 Voice Query"
    )

    image = gr.Image(
        type="filepath",
        label="🖼️ Medical Image (Optional)"
    )

    question = gr.Textbox(
    label="🎤 Recognized Question",
    interactive=False
    )

    response = gr.Textbox(
    label="🤖 Medical Response",
    lines=10,
    interactive=False
    )

    submit = gr.Button("🚀 Submit")
    
    submit.click(
        fn=predict,
        inputs=[audio, image],
        outputs=[question, response]
    )


app.launch()