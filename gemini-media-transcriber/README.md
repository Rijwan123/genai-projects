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
