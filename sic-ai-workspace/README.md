# SIC AI Workspace

## Project Summary

SIC AI Workspace is a small multimodal Generative AI application built using **FastAPI, React, Vite, Three.js, and Google Gemini AI**.

The application provides three main AI features:

- **S — Summarize**: Summarize long text into concise information.
- **I — Image Intelligence**: Upload an image and generate an AI-powered explanation of its contents.
- **C — Chat**: Interact with a general-purpose Gemini-powered AI assistant.

---

### Technology Used

#### Backend

- Python
- FastAPI
- Uvicorn
- Google Gemini API
- Requests
- Python Dotenv
- Python Multipart

#### Frontend

- React
- Vite
- JavaScript
- Three.js
- React Three Fiber
- Lucide React
- CSS

---

### Application Flow

```text
User
  ↓
React Frontend
  ↓
FastAPI Backend
  ↓
Google Gemini API
  ↓
FastAPI Response
  ↓
React UI
```

---

# 🚀 Steps to Run the Project

## 1. Clone the Repository

Clone the main GenAI projects repository:

```bash
git clone https://github.com/YOUR_USERNAME/genai-projects.git
```

Move into the project:

```bash
cd genai-projects/sic-ai-workspace
```

---

## 2. Setup Backend

Move to the backend folder:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

For macOS/Linux:

```bash
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Gemini API Key

Create a `.env` file inside the `backend` folder.

Add:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Example:

```text
GEMINI_API_KEY=your_actual_api_key_here
```

> ⚠️ Never push the `.env` file or your Gemini API key to GitHub.

---

## 4. Start FastAPI Backend

Run:

```bash
uvicorn sample:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger API Documentation:

```text
http://127.0.0.1:8000/docs
```

Keep this terminal running.

---

## 5. Setup Frontend

Open a second terminal.

Move to the frontend folder:

```bash
cd genai-projects/sic-ai-workspace/frontend
```

If you are already inside the backend folder:

```bash
cd ../frontend
```

Install frontend dependencies:

```bash
npm install
```

---

## 6. Start React Frontend

Run:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

Open this URL in your browser.

---

# ⚡ Quick Run

## Backend Terminal

```bash
cd genai-projects/sic-ai-workspace/backend
.venv\Scripts\Activate.ps1
uvicorn sample:app --reload
```

## Frontend Terminal

```bash
cd genai-projects/sic-ai-workspace/frontend
npm install
npm run dev
```

---

# 🌐 Application URLs

**Frontend**

```text
http://localhost:5173
```

**Backend**

```text
http://127.0.0.1:8000
```

**FastAPI Swagger**

```text
http://127.0.0.1:8000/docs
```

---

# 🔐 Important

The backend and frontend must run at the same time.

Keep your Gemini API key only inside:

```text
backend/.env
```

Make sure `.env` is included in `.gitignore` and is never pushed to GitHub.