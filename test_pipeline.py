from pipeline.multimodal_pipeline import run_pipeline

response = run_pipeline(
    audio_path="uploads/test.wav",
    image_path="uploads/test.png"
)

print("\nFinal Response:\n")
print(response)