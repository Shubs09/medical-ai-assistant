from google import genai
from PIL import Image
from dotenv import load_dotenv
import os

# =====================================
# Load Environment Variables
# =====================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to your .env file (local) or Hugging Face Secrets."
    )

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.6-flash"


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

        if image_path is not None:

            with Image.open(image_path) as image:

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=[
                        prompt,
                        image
                    ]
                )

        else:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

        return response.text

    except Exception as e:

        print("Gemini Error:", e)

        error_message = str(e)

        # -------------------------------
        # Quota Exceeded
        # -------------------------------
        if "RESOURCE_EXHAUSTED" in error_message or "429" in error_message:

            return """
⚠️ Gemini API Daily Quota Exceeded

The Medical AI Assistant is working correctly,
but the free Gemini API request limit has been reached.

Please try one of the following:

• Wait for the daily quota to reset.
• Use another Gemini API key.
"""

        # -------------------------------
        # Invalid API Key
        # -------------------------------
        elif "API_KEY_INVALID" in error_message or "401" in error_message:

            return """
❌ Invalid Gemini API Key

Please check your GEMINI_API_KEY.
"""

        # -------------------------------
        # Permission Error
        # -------------------------------
        elif "PERMISSION_DENIED" in error_message or "403" in error_message:

            return """
❌ Permission Denied

Your Gemini API key does not have permission
to access the requested model.
"""

        # -------------------------------
        # Network Error
        # -------------------------------
        elif (
            "Connection" in error_message
            or "Timeout" in error_message
            or "Network" in error_message
        ):

            return """
🌐 Unable to connect to Gemini.

Please check your internet connection
and try again.
"""

        # -------------------------------
        # Unknown Error
        # -------------------------------
        else:

            return f"""
❌ Unexpected Error

Technical Details:

{error_message}
"""