import whisper

print("Whisper module loaded")

model = whisper.load_model("base")

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]