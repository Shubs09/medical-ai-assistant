from google import genai
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_image(image_path, question, context):

    try:

        image = Image.open(image_path)

        prompt = f"""
You are an AI Medical Assistant.

Question:
{question}

Medical Knowledge:
{context}

Instructions:
- Analyze the image carefully.
- Use the medical knowledge provided.
- Give a clear medical explanation.
- Mention uncertainty if needed.
- Do not provide a final diagnosis.
- Recommend consulting a doctor.

Answer:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                image
            ]
        )

        return response.text

    except Exception as e:

        print("Gemini Error:", e)

        return """
❌ Medical AI service is temporarily unavailable.

Possible reasons:
- Gemini API quota exceeded
- Gemini service overloaded
- Network issue

Please try again later.
"""