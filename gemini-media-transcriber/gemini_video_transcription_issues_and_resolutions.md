# Gemini Video Transcription - Issues and Resolutions

## 1. Deprecated Gemini SDK

**Issue:** The code was using the old `google.generativeai` package.

**Resolution:** Migrated to the new `google-genai` SDK.

```python
from google import genai
```

---

## 2. `genai.configure()` Error

**Issue:** `genai.configure()` is part of the old Gemini SDK.

**Resolution:** Created a Gemini client using:

```python
client = genai.Client(api_key=api_key)
```

---

## 3. `GenerativeModel` Error

**Issue:** `genai.GenerativeModel()` is not available in the new SDK.

**Resolution:** Replaced it with:

```python
client.models.generate_content()
```

---

## 4. API Key Not Found

**Issue:** Python could not read `GEMINI_API_KEY`.

**Resolution:** Loaded environment variables from `.env`.

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
```

---

## 5. Invalid API Key

**Issue:** Gemini returned `API_KEY_INVALID`.

**Resolution:** Generated a valid Gemini API key and updated the `.env` file.

```env
GEMINI_API_KEY=your_api_key
```

---

## 6. Video Had No Audio

**Issue:** The downloaded YouTube video contained only the video stream.

**Resolution:** Downloaded both video and audio and verified that an audio track exists.

```python
if video.audio is None:
    raise ValueError("Video does not contain an audio track.")
```

---

## 7. Corrupted WEBM File

**Issue:** MoviePy could not read the downloaded `.webm` file.

**Resolution:** Deleted the corrupted file and downloaded a fresh MP4 file.

---

## 8. MoviePy `NoneType` Error

**Issue:** `video.audio` was `None`, causing `write_audiofile()` to fail.

**Resolution:** Added audio-track validation before extracting audio.

---

## 9. Gemini Model 404 Error

**Issue:** The selected Gemini model was unavailable or unsupported for the API method.

**Resolution:** Changed to a supported Gemini model.

---

## 10. Gemini 503 High Demand Error

**Issue:** Gemini returned:

`503 UNAVAILABLE - model is currently experiencing high demand`

**Resolution:** Added automatic retry logic with exponential backoff.

Example retry intervals:

```text
5 sec -> 10 sec -> 20 sec -> 40 sec
```

---

## 11. Invalid JSON Response

**Issue:** Gemini could potentially return text that could not be parsed as JSON.

**Resolution:** Used a structured JSON response schema and parsed the result using:

```python
json.loads(response.text)
```

---

## 12. Temporary Audio File

**Issue:** `temp_audio.wav` remained after execution.

**Resolution:** Added cleanup logic inside the `finally` block.

```python
if os.path.exists(audio_file_path):
    os.remove(audio_file_path)
```

---

# Final Flow

```text
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
Structured JSON
    |
    v
transcription.json
```

# Key Learning

Most issues were caused by mixing the old and new Gemini SDK syntax.

The final implementation uses:

```text
google-genai
    |
    v
genai.Client()
    |
    v
client.files.upload()
    |
    v
client.models.generate_content()
    |
    v
Structured JSON response
```
