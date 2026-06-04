from pipeline.final_medical_pipeline import run_medical_pipeline

response = run_medical_pipeline(
    audio_path="uploads/test.wav",
    image_path="uploads/test.png"
)

print("\nFINAL RESPONSE:\n")
print(response)