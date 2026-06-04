from llm.gemini_vision import analyze_image

question = input("Ask a question about the image:")

response = analyze_image(
    "uploads/test.png",
    question
)

print("\nAI Response:\n")
print(response)