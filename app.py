import gradio as gr

css = """
/* ===============================
   Main App
================================= */

.gradio-container{
    max-width:1600px !important;
    margin:auto !important;
    padding:25px !important;
}

/* ===============================
   Header
================================= */

.header{
    text-align:center;
    margin-bottom:15px;
}

/* ===============================
   Disclaimer
================================= */

.disclaimer{
    margin-bottom:20px;
}

/* ===============================
   Cards
================================= */

.input-card,
.output-card{
    border:1px solid rgba(255,255,255,0.08);
    border-radius:18px !important;
    padding:18px !important;
    box-shadow:0 6px 18px rgba(0,0,0,0.15);
}

/* ===============================
   Textbox
================================= */

.question-box textarea{
    font-size:15px !important;
}

/* ===============================
   AI Response
================================= */

.response-box{
    padding:18px !important;
    border-radius:12px !important;
    background:#20252d;
    line-height:1.8;
}

.response-box p,
.response-box li{
    font-size:16px !important;
}

.response-box ul{
    padding-left:22px !important;
}

/* ===============================
   Sources
================================= */

.sources-box{
    margin-top:12px;
    padding:15px !important;
    border-radius:12px;
    background:#20252d;
}

/* ===============================
   Audio & Image
================================= */

.audio-box,
.image-box{
    border-radius:12px !important;
}

/* ===============================
   Buttons
================================= */

.submit-btn button{
    border-radius:10px !important;
    font-weight:600 !important;
}

.clear-btn button{
    border-radius:10px !important;
    font-weight:600 !important;
}

/* ===============================
   Footer
================================= */

.footer{
    text-align:center;
    margin-top:25px;
    color:#9ca3af;
}
"""

from pipeline.final_medical_pipeline import (
    run_medical_pipeline
)


def predict(
    text_question,
    audio,
    image,
):

    # Check input
    if not text_question and audio is None:
        return (
            "",
            "❌ Please either type a question or upload/record audio.",
            ""
        )

    try:

        response = run_medical_pipeline(
            question=text_question,
            audio_path=audio,
            image_path=image,
        )

        # Empty response check
        if not response:
            return (
                "",
                "❌ No response generated.",
                ""
            )

        # Format sources
        if response["sources"]:
            source_text = (
                "### 📚 Reference Documents\n\n"
                + "\n".join(
                    f"📄 {source}"
                    for source in response["sources"]
                )
        )   
        else:
            source_text = ""

        return (
            response["question"],
            response["response"],
            source_text
        )

    except Exception as e:

        print("\nERROR:", e)

        return (
            "",
            f"""❌ Unexpected application error.

Technical Details:
{str(e)}
""",
            ""
        )


with gr.Blocks(
    css=css,
    title="🏥 Medical AI Assistant",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="zinc",
        neutral_hue="slate"
    )
) as app:

    # ==========================
    # Header
    # ==========================

    gr.Markdown("""
<div align="center">

<h1 style="font-size:60px; margin-bottom:5px;">
🩺 Medical AI Assistant
</h1>

<p style="font-size:22px; color:#9ca3af;">
AI-powered Medical Question Answering System
</p>

</div>
""",
elem_classes="header")

    gr.Markdown("---")

    # ==========================
    # Disclaimer
    # ==========================

    gr.Markdown("""
<div style="
padding:15px;
border-left:5px solid #f59e0b;
background:#1f2937;
border-radius:8px;
margin-bottom:20px;
">

<b>⚠️ Disclaimer</b><br><br>

This application is intended for educational purposes only.
It is <b>not a substitute for professional medical advice,
diagnosis, or treatment.</b>

Always consult a qualified healthcare professional.

</div>
""",
elem_classes="disclaimer")

    with gr.Row():

        # ==========================
        # Left Panel
        # ==========================

        # ==========================

        with gr.Column(scale=3):

            with gr.Group(elem_classes="input-card"):

                gr.Markdown("## 📥 Ask Your Medical Question")

                text_question = gr.Textbox(
                    label="Medical Question",
                    placeholder="""
Ask any medical question...

Examples:
• What are the symptoms of diabetes?
• What causes asthma?
• What does this skin rash look like?
""",
                    lines=2
                )

                with gr.Accordion("💡 Example Questions", open=False):

                    gr.Examples(
                        examples=[
                            ["What are the symptoms of diabetes?"],
                            ["What causes asthma?"],
                            ["What causes high blood pressure?"],
                            ["What does this skin rash look like?"]
                        ],
                        inputs=text_question
                    )

                gr.Markdown("---")

                audio = gr.Audio(
                    sources=["upload", "microphone"],
                    type="filepath",
                    label="🎤 Voice Query",
                    elem_classes="audio-box"
                )

                gr.Markdown("---")

                image = gr.Image(
                    type="filepath",
                    height=280,
                    label=" Medical Image",
                    elem_classes="image-box"
                )

                with gr.Row(equal_height=True):

                    submit = gr.Button(
                        "🩺 Get Medical Insight",
                        variant="primary",
                        elem_classes="submit-btn"
                    )

                    clear = gr.Button(
                        "🗑 Clear",
                        elem_classes="clear-btn"
                    )

        # ==========================
        # Right Panel
        # ==========================

        with gr.Column(scale=3):

            with gr.Group(elem_classes="output-card"):

                gr.Markdown("## 🤖 AI Response")

                question = gr.Textbox(
                    label="Question",
                    interactive=False,
                    elem_classes="question-box"
                )

                response = gr.Markdown(
                    label="Medical Explanation",
                    elem_classes="response-box"
                )

                sources = gr.Markdown(
                    label="📄 References",
                    elem_classes="sources-box"
                )

    submit.click(
        fn=predict,
        inputs=[
            text_question,
            audio,
            image
        ],
        outputs=[
            question,
            response,
            sources
        ],
        show_progress="full"
    )

    clear.click(
        fn=lambda: ("", None, None, "", "", ""),
        outputs=[
            text_question,
            audio,
            image,
            question,
            response,
            sources
        ]
    )

    gr.Markdown("""
---

<div align="center">

Built with **Whisper • ChromaDB • Sentence Transformers • Google Gemini • Gradio**

</div>
""",
elem_classes="footer")

import os

try:
    print("Launching Medical AI Assistant...")
    port = int(os.environ.get("PORT", 7860))

    app.launch(
        server_name="0.0.0.0",
        server_port=port
    )
except Exception as e:
    print("Launch Error:", e)