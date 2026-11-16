from fastapi import FastAPI, Depends
from extraction import generate
from contextlib import asynccontextmanager
import requests
from auth import verify_api_key
from rag import generate_rag
import config
import prompts
from models import Result, InputJudgement, InputAsk

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
def extract(judgment: InputJudgement) -> Result:
    inputContext = judgment.judgment
    messages = [{"role": "user", "content": prompts.PROMPT_EXTRACTION.replace("{context}", inputContext)}]
    output = generate(messages)
    return output

@api.post("/ask", dependencies=[Depends(verify_api_key)])
def ask(question: InputAsk) -> str:
    return generate_rag(question.text)