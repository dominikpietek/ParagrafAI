from fastapi import FastAPI, Depends
from dataclasses import dataclass
from pydantic import BaseModel, Field
from serving.extraction import generate
from contextlib import asynccontextmanager
import requests
from auth import verify_api_key
from serving.rag import generate_rag
import config
import prompts

@dataclass
class Result:
    court_name: str | None = Field(default=None)
    date: str | None = Field(default=None)
    department_name: str | None = Field(default=None)
    recorder: str | None = Field(default=None)
    signature: str | None = Field(default=None)
    judges: list[str] = Field(default=None)
    legal_bases: list[str] = Field(default=None)

class InputData(BaseModel):
    judgment: str = Field(min_length=1000, max_length=14000)

def is_ollama_available() -> bool:
    try:
        response = requests.get(f"{config.OLLAMA_URL}/api/tags", timeout=20)
        response.raise_for_status()
    except:
        return False

    return True

@asynccontextmanager
async def lifespan(app):
    if is_ollama_available() == False:
        print("Ollama niedostępna!")
    print("ParagrafAI gotowy")
    yield
    print("ParagrafAI zamknięty")

api = FastAPI(title="ParagrafAI", lifespan=lifespan)

@api.get("/health")
def health():
    if is_ollama_available() == False:
        return {"status": "ok", "model_status": "bad"}

    return {"status": "ok", "model_status": "ok"}

@api.post("/extract", dependencies=[Depends(verify_api_key)])
def extract(judgment: InputData,) -> Result:
    inputContext = judgment.judgment
    return ask_model(inputContext)

def ask_model(message_input: str) -> Result:
    messages = {"role": "user", "content": prompts.PROMPT_EXTRACTION.replace("{context}", message_input)},
    output = generate(messages)
    return output

@api.post("/ask", dependencies=[Depends(verify_api_key)])
def ask(question: str) -> str:
    return generate_rag(question)