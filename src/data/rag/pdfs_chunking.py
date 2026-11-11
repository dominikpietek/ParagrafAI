import pymupdf
from pathlib import Path
import re
import json

def text_retriving_from_pdf(pdf: Path) -> str:
    doc = pymupdf.open(str(pdf))

    full_text = ""
    for page in doc:
        full_text += page.get_text()

    return full_text

def clear_pdf_text(text: str) -> str:
    text = re.sub(r"^\s*Dziennik Ustaw\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-–]\s*\d+\s*[-–]\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*Poz\.\s*\d+\s*$", "", text, flags=re.MULTILINE)
    return text

def chunking(text: str, act_name: str) -> list[dict]:
    parts = re.split(r"(^Art\.\s*\d+[a-z]?(?:\[\d+\])?\.)", text, flags=re.MULTILINE)

    articles = []
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""

        numer = re.search(r"\d+[a-z]?(?:\[\d+\])?", header).group()
        articles.append({
            "id": f"{act_name}_{numer}_{i}",
            "act": act_name,
            "article": numer,
            "text": f"{header} {body}",
        })
    return articles

if __name__ == "__main__":
    raw_dir = Path("raw")
    pdf_files = list(raw_dir.glob("*.pdf"))
    chunks = []
    for pdf in pdf_files:
        text = clear_pdf_text(text_retriving_from_pdf(pdf))
        act_name = pdf.stem 
        chunks.extend(chunking(text, act_name))

    with open("articles.jsonl", "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")