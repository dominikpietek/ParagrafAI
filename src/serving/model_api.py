from fastapi import FastAPI
from dataclasses import dataclass, field
from pydantic import BaseModel
from llm import generate
from contextlib import asynccontextmanager
import requests
import os

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

PROMPT = r"""You are extracting information from the Polish court judgments.
Extract specified values strictly from the provided judgement. If information is not provided in the judgement, leave the field with null value.
Please return the response in the identical YAML format:
```yaml
court_name: "<nazwa sądu, string containing the full name of the court>"
date: <data, date in format YYYY-MM-DD>
department_name: "<nazwa wydziału, string containing the full name of the court's\
\ department>"
judges: "<sędziowie, list of judge full names>"
legal_bases: <podstawy prawne, list of strings containing legal bases (legal regulations)>
recorder: <protokolant, string containing the name of the recorder>
signature: <sygnatura, string contraining the signature of the judgment>
```
=====
{context}
======"""

@dataclass
class Result:
    court_name: str | None = field(default=None)
    date: str | None = field(default=None)
    department_name: str | None = field(default=None)
    recorder: str | None = field(default=None)
    signature: str | None = field(default=None)
    judges: list[str] = field(default=None)
    legal_bases: list[str] = field(default=None)

class InputData(BaseModel):
    judgment: str = field(min_length=1000, max_length=14000)

def is_ollama_available() -> bool:
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=20)
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

@api.post("/extract")
def extract(judgment: InputData,) -> Result:
    inputContext = judgment.judgment
    return ask_model(inputContext)

def ask_model(message_input: str) -> Result:
    messages = {"role": "user", "content": PROMPT.replace("{context}", message_input)},
    output = generate(messages)
    return output