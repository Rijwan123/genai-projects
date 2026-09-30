# pip install -U google-genai python-dotenv

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os


# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)


def transcribe_audio_with_diarization(audio_file_path):

    try:
        # Read audio file
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()

        prompt = """
        Please transcribe the following audio accurately.

        Also perform speaker diarization.

        Requirements:
        - Identify different speakers.
        - Label them as Speaker 1, Speaker 2, Speaker 3, etc.
        - Put the speaker label before each spoken segment.
        - Do not summarize the conversation.
        - Preserve the spoken content as accurately as possible.
        """

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=audio_data,
                    mime_type="audio/wav"
                )
            ]
        )

        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Correct Windows path
audio_file = r"D:\GEN AI Batch 38\6_PromptEngineering\a.wav"

result = transcribe_audio_with_diarization(audio_file)

if result:
    print("\n----- TRANSCRIPTION -----\n")
    print(result)