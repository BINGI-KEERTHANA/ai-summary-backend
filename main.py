from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .ai import generate_summary

# THIS LINE MUST BE EXACTLY "app"
app = FastAPI(title="LexiHub AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummaryRequest(BaseModel):
    text: str = ""
    language: str = "english"
    title: str = ""

@app.get("/")
def home():
    return {"message": "LexiHub AI Backend Running"}

@app.post("/summarize")
def summarize(request: SummaryRequest):
    summary = generate_summary(
        text=request.text, 
        language=request.language, 
        title=request.title
    )
    return {"summary": summary}