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

        prompt = f"""
You are an AI Medical Assistant.

Question:
{question}

Medical Knowledge:
{context}

Instructions:
- Use the provided medical knowledge.
- If an image is provided, analyze it carefully.
- If no image is provided, answer only using the question and medical knowledge.
- Give a clear medical explanation.
- Mention uncertainty if needed.
- Do not provide a final diagnosis.
- Recommend consulting a doctor.

Answer:
"""

        if image_path:
            image = Image.open(image_path)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    image
                ]
            )

        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
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