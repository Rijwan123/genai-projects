Gemini Media Transcriber

Project Name:
Gemini Media Transcriber

GitHub Repository Name:
gemini-media-transcriber


PROJECT SUMMARY

Gemini Media Transcriber is a Generative AI project that transcribes both audio and video files using Google Gemini.

The project supports:
- Audio transcription
- Video-to-audio extraction using MoviePy
- Speaker diarization
- Timestamped transcription
- Structured JSON output
- Gemini API integration using the google-genai SDK
- API key loading from a .env file
- Retry handling for temporary Gemini API errors
- Cleanup of temporary audio files


AUDIO FLOW

Audio File
    |
    v
Upload to Gemini
    |
    v
Gemini Transcription
    |
    v
Speaker + Timestamp + Text
    |
    v
Structured JSON Output


VIDEO FLOW

MP4 Video
    |
    v
MoviePy
    |
    v
Extract Audio
    |
    v
temp_audio.wav
    |
    v
Upload to Gemini
    |
    v
Gemini Transcription
    |
    v
Speaker + Timestamp + Text
    |
    v
Structured JSON Output


TECHNOLOGIES USED

- Python
- Google Gemini API
- google-genai
- MoviePy
- python-dotenv
- JSON


OUTPUT FORMAT

Example:

[
  {
    "speaker": "Speaker 1",
    "start_time": 0.0,
    "end_time": 5.2,
    "text": "Hello, this is the beginning."
  },
  {
    "speaker": "Speaker 2",
    "start_time": 5.2,
    "end_time": 10.1,
    "text": "And I am responding."
  }
]


KEY LEARNING

This project demonstrates how multimodal Generative AI can be used to process audio and video content, extract speech, identify speakers, generate timestamps, and return structured output that can be used in downstream applications.

It also provides hands-on experience with:
- Gemini API integration
- Audio and video file processing
- Speaker diarization
- Timestamp generation
- Environment variable management
- Structured JSON responses
- API retry handling
- Temporary file cleanup


FINAL END-TO-END FLOW

MP4 Video / Audio File
    |
    v
Audio Preparation
    |
    v
Upload to Gemini
    |
    v
Gemini Transcription
    |
    v
Speaker + Timestamp + Text
    |
    v
Structured JSON Output

---------------------------------------------------------------------------------
How to Run Gemini Media Transcriber

1. Open the Project Folder

Open the terminal in:

genai-projects/gemini-media-transcriber

2. Create a Virtual Environment

python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1

3. Install Required Packages

pip install -U google-genai python-dotenv moviepy

4. Create a .env File

Create a file named:

.env

Add your Gemini API key:

GEMINI_API_KEY=your_gemini_api_key_here

5. Add the Video File

Place the video file on your system and update the path in the Python script.

Example:

video_file = r"C:\Users\YourName\Videos\sample.mp4"

6. Run the Script

python .\2_Assignment_Video.py

7. Check the Output

The transcription will be displayed in the terminal.

After successful execution, the output will also be saved as:

transcription.json
