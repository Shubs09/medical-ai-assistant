import whisper

print("Whisper module imported")

model = None

def get_model():
    global model
    if model is None:
        print("Loading Whisper model...")
        model = whisper.load_model("tiny")
    return model

def transcribe_audio(audio_path):
    whisper_model = get_model()
    result = whisper_model.transcribe(audio_path)
    return result["text"]