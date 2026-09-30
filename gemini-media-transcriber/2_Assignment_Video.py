# pip install -U google-genai python-dotenv moviepy
#Most of the initial errors came from mixing old and new Gemini SDK syntax. After migrating fully to google-genai, 
#fixing the API key, validating the video/audio, and adding retry logic for 503 errors, the pipeline became stable.

from google import genai
from google.genai import types
from dotenv import load_dotenv
from moviepy import VideoFileClip

import os
import json
import time
import random


# --------------------------------------------------
# 1. Load API key
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# 2. Gemini request with retry
# --------------------------------------------------

def generate_with_retry(uploaded_file, prompt, max_retries=5):

    for attempt in range(max_retries):

        try:

            print(
                f"Gemini request attempt "
                f"{attempt + 1}/{max_retries}..."
            )

            response = client.models.generate_content(

                model="gemini-3.5-flash",

                contents=[
                    prompt,
                    uploaded_file
                ],

                config=types.GenerateContentConfig(

                    response_mime_type="application/json",

                    response_schema={

                        "type": "array",

                        "items": {

                            "type": "object",

                            "properties": {

                                "speaker": {
                                    "type": "string"
                                },

                                "start_time": {
                                    "type": "number"
                                },

                                "end_time": {
                                    "type": "number"
                                },

                                "text": {
                                    "type": "string"
                                }
                            },

                            "required": [
                                "speaker",
                                "start_time",
                                "end_time",
                                "text"
                            ]
                        }
                    }
                )
            )

            print("Gemini response received successfully.")

            return response


        except Exception as e:

            error_message = str(e)

            # --------------------------------------
            # Retry temporary errors
            # --------------------------------------

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "high demand" in error_message.lower()
                or "429" in error_message
            ):

                if attempt < max_retries - 1:

                    # Exponential backoff:
                    # ~5, 10, 20, 40 sec...
                    wait_time = (
                        5 * (2 ** attempt)
                        + random.uniform(0, 2)
                    )

                    print(
                        "\nGemini is temporarily busy."
                    )

                    print(
                        f"Retrying in "
                        f"{wait_time:.1f} seconds...\n"
                    )

                    time.sleep(wait_time)

                else:

                    print(
                        "\nGemini is still unavailable "
                        "after all retry attempts."
                    )

                    return None

            else:

                # Permanent errors such as
                # invalid model, invalid API key, etc.
                print(
                    f"\nGemini API error:\n{e}"
                )

                return None


# --------------------------------------------------
# 3. Video transcription function
# --------------------------------------------------

def transcribe_audio_with_timestamps(video_file_path):

    audio_file_path = "temp_audio.wav"

    video = None

    try:

        # --------------------------------------------------
        # Check video exists
        # --------------------------------------------------

        if not os.path.exists(video_file_path):

            raise FileNotFoundError(
                f"Video file not found:\n"
                f"{video_file_path}"
            )


        # --------------------------------------------------
        # 4. Open video
        # --------------------------------------------------

        print("Opening video...")

        video = VideoFileClip(
            video_file_path
        )


        # --------------------------------------------------
        # Check audio track
        # --------------------------------------------------

        if video.audio is None:

            raise ValueError(
                "The video does not contain "
                "an audio track."
            )


        # --------------------------------------------------
        # 5. Extract audio
        # --------------------------------------------------

        print("Extracting audio...")

        video.audio.write_audiofile(
            audio_file_path,
            logger=None
        )

        print(
            "Audio extracted successfully."
        )


        # Close video after extraction
        video.close()
        video = None


        # --------------------------------------------------
        # 6. Upload audio to Gemini
        # --------------------------------------------------

        print("Uploading audio...")

        uploaded_file = client.files.upload(
            file=audio_file_path
        )

        print(
            "Audio uploaded successfully."
        )


        # --------------------------------------------------
        # 7. Prompt
        # --------------------------------------------------

        prompt = """
        Transcribe this audio accurately.

        Requirements:

        1. Include timestamps for each meaningful segment.

        2. Perform speaker diarization where possible.

        3. Label speakers as:
           Speaker 1,
           Speaker 2,
           Speaker 3, etc.

        4. Split the transcription based on:
           - speaker changes
           - utterances
           - meaningful pauses

        5. start_time and end_time must be in seconds.

        6. Do not summarize the conversation.

        7. Preserve the spoken words as accurately
           as possible.

        Return JSON only.

        Each segment must contain:

        - speaker
        - start_time
        - end_time
        - text
        """


        # --------------------------------------------------
        # 8. Send to Gemini
        # --------------------------------------------------

        print("Transcribing...")

        response = generate_with_retry(
            uploaded_file,
            prompt
        )


        if response is None:

            return None


        # --------------------------------------------------
        # 9. Parse JSON
        # --------------------------------------------------

        try:

            transcription = json.loads(
                response.text
            )

            return transcription


        except json.JSONDecodeError:

            print(
                "\nGemini returned invalid JSON."
            )

            print(
                "\nRaw response:\n"
            )

            print(response.text)

            return None


    except Exception as e:

        print(
            f"\nAn error occurred: {e}"
        )

        return None


    finally:

        # --------------------------------------------------
        # Close video if still open
        # --------------------------------------------------

        if video is not None:

            try:
                video.close()
            except Exception:
                pass


        # --------------------------------------------------
        # Delete temporary WAV
        # --------------------------------------------------

        if os.path.exists(
            audio_file_path
        ):

            try:

                os.remove(
                    audio_file_path
                )

                print(
                    "Temporary audio file deleted."
                )

            except Exception:

                pass


# --------------------------------------------------
# 10. Video file
# --------------------------------------------------

video_file = (
    r"D:\GEN AI Batch 38\6_PromptEngineering\b.mp4"
)


# --------------------------------------------------
# 11. Run transcription
# --------------------------------------------------

transcription_data = (
    transcribe_audio_with_timestamps(
        video_file
    )
)


# --------------------------------------------------
# 12. Print result
# --------------------------------------------------

if transcription_data:

    print(
        "\n"
        "=========================================="
    )

    print(
        "TRANSCRIPTION"
    )

    print(
        "==========================================\n"
    )


    for segment in transcription_data:

        print(
            f"{segment['speaker']} "
            f"[{segment['start_time']} - "
            f"{segment['end_time']} sec]"
        )

        print(
            segment["text"]
        )

        print()


    # --------------------------------------------------
    # 13. Save output to JSON file
    # --------------------------------------------------

    output_file = "transcription.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            transcription_data,
            file,
            indent=4,
            ensure_ascii=False
        )


    print(
        f"Transcription saved to "
        f"{output_file}"
    )