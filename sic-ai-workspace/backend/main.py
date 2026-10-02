# ---------------------------------------------------------
# INSTALL
# ---------------------------------------------------------
# pip install fastapi uvicorn requests python-multipart python-dotenv
#
# RUN:
# uvicorn sample:app --reload
#
# Open Swagger:
# http://127.0.0.1:8000/docs
# ---------------------------------------------------------


from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import requests
import os
import logging
import base64


# ---------------------------------------------------------
# 1. Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Starting Gemini API Backend...")


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


# ---------------------------------------------------------
# 4. Create FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="SIC AI Backend",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)


# ---------------------------------------------------------
# 5. CORS configuration
# ---------------------------------------------------------
# For development we are allowing all origins.
#
# In production replace "*" with your frontend URL.
#
# Example:
# allow_origins=["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.info("Gemini API Backend initialized successfully.")


# ---------------------------------------------------------
# 6. Common Gemini API function
# ---------------------------------------------------------

def call_gemini(parts):

    payload = {
        "contents": [
            {
                "parts": parts
            }
        ]
    }

    try:

        logging.info("Sending request to Gemini API...")

        response = requests.post(
            GEMINI_API_URL,
            headers=HEADERS,
            json=payload,
            timeout=60
        )

    except requests.RequestException as error:

        logging.exception(
            "Network error while calling Gemini API"
        )

        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to Gemini API: {str(error)}"
        )


    # Try to convert response into JSON
    try:

        data = response.json()

    except ValueError:

        logging.error(
            "Gemini returned non-JSON response: %s",
            response.text
        )

        raise HTTPException(
            status_code=502,
            detail="Invalid response received from Gemini API."
        )


    # Handle Gemini HTTP errors
    if not response.ok:

        error_message = (
            data.get("error", {})
            .get("message", "Unknown Gemini API error")
        )

        logging.error(
            "Gemini API Error: %s",
            error_message
        )

        raise HTTPException(
            status_code=response.status_code,
            detail=error_message
        )


    # Extract candidates
    candidates = data.get("candidates")

    if not candidates:

        logging.error(
            "No candidates returned from Gemini: %s",
            data
        )

        raise HTTPException(
            status_code=502,
            detail="Gemini returned no response."
        )


    # Extract generated content
    response_parts = (
        candidates[0]
        .get("content", {})
        .get("parts", [])
    )


    generated_text = "".join(
        part.get("text", "")
        for part in response_parts
    ).strip()


    if not generated_text:

        raise HTTPException(
            status_code=502,
            detail="Gemini returned an empty response."
        )


    logging.info("Gemini request completed successfully.")

    return generated_text


# ---------------------------------------------------------
# 7. Root endpoint
# ---------------------------------------------------------

@app.get("/api")
def read_root():

    return {
        "message": "Welcome to the Gemini API Backend!"
    }


# ---------------------------------------------------------
# 8. Text Summarization Endpoint
# ---------------------------------------------------------
@app.post("/api/summarize")
def summarize(text: str = Form(...)):

    if not text.strip():

        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty."
        )


    logging.info(
        "Received summarization request. Characters: %d",
        len(text)
    )


    prompt = f"""
Summarize the following paragraph clearly and concisely:

{text}
"""


    summary = call_gemini(
        [
            {
                "text": prompt
            }
        ]
    )


    logging.info("Summarization successful.")


    return {
        "summary": summary
    }


# ---------------------------------------------------------
# 9. Image Explanation Endpoint
# ---------------------------------------------------------

@app.post("/api/explain-image")
def explain_image(
    file: UploadFile = File(...)
):


    # Validate file type
    if (
        not file.content_type
        or not file.content_type.startswith("image/")
    ):

        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image file."
        )


    image_bytes = file.file.read()


    if not image_bytes:

        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty."
        )


    logging.info(
        "Received image: %s",
        file.filename
    )


    # Convert image to Base64
    image_b64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")


    prompt = """
Explain the content of this image.

Describe:
- important objects
- people if present
- visible text
- environment
- important details
"""


    explanation = call_gemini(
        [
            {
                "text": prompt
            },
            {
                "inline_data": {
                    "mime_type": file.content_type,
                    "data": image_b64
                }
            }
        ]
    )


    logging.info(
        "Image explanation completed successfully."
    )


    return {
        "filename": file.filename,
        "explanation": explanation
    }


# ---------------------------------------------------------
# 10. Chatbot Endpoint
# ---------------------------------------------------------

@app.post("/api/chat")
def chat(
    message: str = Form(...)
):


    if not message.strip():

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )


    if message.lower().strip() in [
        "quit",
        "exit"
    ]:

        return {
            "response": "Session ended."
        }


    logging.info(
        "Received chat message."
    )


    clean_message = message.strip().lower()

    if clean_message in ["hi", "hello", "hey", "hii", "hola"]:
        return {
            "response": "Hi! How can I assist you today?"
        }

    prompt = f"""
You are a helpful general-purpose AI assistant.

Answer the user's question clearly, naturally, and accurately.

{message}
"""


    answer = call_gemini(
        [
            {
                "text": prompt
            }
        ]
    )


    logging.info(
        "Chat response generated successfully."
    )


    return {
        "response": answer
    }