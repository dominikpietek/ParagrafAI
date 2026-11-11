import pymupdf
from pathlib import Path

def text_retriving_from_pdf(pdf: Path) -> str:
    doc = pymupdf.open(str(pdf))

    full_text = ""
    for page in doc:
        full_text += page.get_text()

    return full_text

if __name__ == "__main__":
    raw_dir = Path("raw")
    pdf_files = list(raw_dir.glob("*.pdf"))
    for pdf in pdf_files:
        text = text_retriving_from_pdf(pdf)
        print("============================")
        print(text)