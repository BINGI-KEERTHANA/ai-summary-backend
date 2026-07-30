🤖 AI Summary Feature

An intelligent, multilingual summarization module built for Corpus Insight Hub. This feature enables users to automatically generate concise summaries of database records in both Telugu (తెలుగు) and English.
🌟 Key Features

    Multilingual Generation: Instant switching and processing for Telugu and English outputs.

    Text Normalization: Automatically strips invalid characters, HTML tags, and cleans unicode sequences before processing.

    Non-Blocking Fetching: Integrated React AbortController support to prevent memory leaks and handle Strict Mode re-renders smoothly.

    Dynamic Styling & Copy: Provides custom text rendering adjusted for Telugu typography alongside one-click copy functionality.

🏗️ Architecture Overview
Plaintext

┌─────────────────────────┐         HTTP Request         ┌─────────────────────────┐
│     React Frontend      │ ───────────────────────────> │     FastAPI Backend     │
│  (Tailwind + TS + Vite) │ <─────────────────────────── │  (Python + Uvicorn + AI) │
└─────────────────────────┘         JSON Summary         └─────────────────────────┘

🛠️ Tech Stack & Requirements
Frontend

    Framework: React 18+ (with TypeScript)

    Build Tool: Vite

    Styling: Tailwind CSS

    HTTP Client: Axios

    Key Components: AISummary.tsx

Backend

    Framework: FastAPI

    ASGI Server: Uvicorn

    Data Validation: Pydantic (SummaryRequest)

    AI / Pipeline: Deep-Translator / Hugging Face pipeline

    Dependencies: Defined in backend/requirements.txt

🚀 Getting Started
1. Backend Setup

Navigate to the project root and start the Python server:
Bash

# Activate virtual environment
source backend/.venv/bin/activate

# Install dependencies (if not already installed)
pip install -r backend/requirements.txt

# Start FastAPI server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).
2. Frontend Setup

In a separate terminal window, start the Vite development server:
Bash

# Install packages
npm install

# Run Vite dev server
npm run dev

Open your browser and navigate to http://localhost:5173/ai-summary.
📡 API Reference
POST /summarize

Generates an AI summary for a given text payload.

Request Body (application/json):
JSON

{
  "title": "Sample Topic",
  "text": "Full body text content to be summarized...",
  "language": "te"
}

    language options: "te" (Telugu) | "en" (English)

Response (200 OK):
JSON

{
  "summary": "This is the generated summary text..."
}

🧪 How to Test

    Launch both the backend and frontend servers as described above.

    Navigate to the AI Summary page in your browser.

    Select a record/topic from the dropdown menu.

    Toggle your desired language (Telugu or English).

    Click Get Summary and verify that the output appears correctly in the text field.
