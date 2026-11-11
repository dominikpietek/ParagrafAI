import time
from pathlib import Path
import requests

HEADERS = {"User-Agent": "ParagrafAI/0.1 (projekt edukacyjny)"}

DELAY_TIME = 0.1

ACTS = {
    "kodeks_pracy": "https://api.sejm.gov.pl/eli/acts/search?title=Kodeks%20pracy&publisher=DU",
    "prawa_konsumenta": "https://api.sejm.gov.pl/eli/acts/search?title=Praw%20Konsumenta&publisher=DU",
}

def download_pdf(url: str, out_dir: Path) -> None:
    response = requests.get(url, headers=HEADERS, timeout=120, stream=True)
    response.raise_for_status()

    response = response.json()
    id_list = [x["ELI"] for x in response["items"] 
               if "jednolitego tekstu" in x["title"].lower() and "kodeks pracy" in x["title"].lower()]

    for id in id_list:
        pdf_response = requests.get("https://api.sejm.gov.pl/eli/acts/" + id + "/text.pdf", headers=HEADERS, timeout=120)
        pdf_response.raise_for_status()

        out_path = out_dir / f"{id.replace('/', '_')}.pdf"
        with open(out_path, "wb") as f:
            f.write(pdf_response.content)
        print(f"Pobrano: {out_path.name}")

def main():
    out_dir = Path("raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, url in ACTS.items():
        download_pdf(url, out_dir)
        time.sleep(DELAY_TIME)

if __name__ == "__main__":
    main()