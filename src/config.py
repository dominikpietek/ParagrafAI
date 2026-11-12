from pathlib import Path
import os

ROOT = Path(__file__).parent.resolve() 
DATA = ROOT / "data"
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
CHROMA_PATH = str(ROOT / "data" / "rag" / "chroma")
EXTRACT_MODEL = "paragrafLLM"
RAG_MODEL = "hf.co/speakleash/Bielik-4.5B-v3.0-Instruct-GGUF:Q8_0"
EMBED_MODEL = "bge-m3"
