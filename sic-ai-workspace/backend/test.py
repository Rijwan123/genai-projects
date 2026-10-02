from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 2. Load environment variables
# ---------------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to your .env file."
    )
# ---------------------------------------------------------
# 3. Gemini configuration
# ---------------------------------------------------------

MODEL_NAME = "gemini-3.5-flash-lite"

GEMINI_API_URL = (
    f"https://generativelanguage.googleapis.com/"
    f"v1beta/models/{MODEL_NAME}:generateContent"
)

HEADERS = {
    "x-goog-api-key": GEMINI_API_KEY,
    "Content-Type": "application/json"
}

def summarize(text: str = Form(...)):
    prompt = f"Summarize the following paragraph:\n{text}"
    response = requests.post(GEMINI_API_URL, json={"contents": [{"parts": [{"text": prompt}]}]})
    data = response.json()
    return data

respoonse = summarize("""Update on September 29, 2026: Learn about OpenAI's latest model: GPT‑6 .1 Sol⁠⁠.

Earlier this month, we introduced GPT‑6 Astra, the most intelligent and aligned model in the world. While the most demanding and important projects still call for Astra’s full depth, work happens at different scales, rhythms, and budgets.

That’s why we’re expanding the GPT‑6 universe with GPT‑6 Sol and GPT‑6 Luna. GPT‑6 Astra introduced a new generation of intelligence—these models help distribute the benefits of that intelligence by advancing the frontier on cost efficiency. We trained GPT‑6 Sol and Luna with similar methods as GPT‑6 Astra, bringing the advances behind Astra’s state-of-the-art performance in professional work, factuality, coding, computer use, and alignment to faster, more affordable models.""")
#print(respoonse[0])
print(respoonse.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Error")    )