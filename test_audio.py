import gradio as gr

def test(audio):
    return str(audio)

with gr.Blocks() as demo:
    audio = gr.Audio(
        sources=["microphone", "upload"],
        type="filepath"
    )

    output = gr.Textbox()

    btn = gr.Button("Submit")

    btn.click(
        test,
        inputs=audio,
        outputs=output
    )

demo.launch()