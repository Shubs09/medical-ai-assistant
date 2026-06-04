import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(prompt):

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            print(f"\nAttempt {attempt + 1} Failed:")
            print(e)

            if attempt < 2:
                print("Waiting 60 seconds before retrying...")
                time.sleep(60)

    return "Gemini API unavailable. Please try again later."