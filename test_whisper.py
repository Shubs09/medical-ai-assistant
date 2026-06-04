from speech.speech_to_text import transcribe_audio

print("Import Successful")

audio_path = "uploads/test.wav"

text = transcribe_audio(audio_path)

print("\nTranscribed Text:\n")
print(text)