from fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent.parent / "local.env")

HEADERS={"X-API-Key": os.environ["PARAGRAF_API_KEY"]}

mcp = FastMCP("ParagrafAI")

@mcp.tool()
def wyciagnij_dane_z_wyroku(tekst: str) -> str:
    """Na podstawie wyroku przygotowywuje yaml"""
    try:
        response = requests.post("http://localhost:8000/extract", json={"judgement": tekst}, timeout=120, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Error: {e}")

    return response.content

@mcp.tool()
def zapytaj_o_przepisy(pytanie: str) -> str:
    """Odpowiada na pytania z polskiego prawa pracy i konsumenckiego
    na podstawie przepisów, z podaniem artykułów."""
    try:
        response = requests.post("http://localhost:8000/ask", json={"question": pytanie}, timeout=120, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Error: {e}")

    return response.content

mcp.run()