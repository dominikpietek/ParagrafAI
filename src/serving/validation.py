import re

JUDGEMENT_PATTERNS = [
    "Sąd", "RZECZYPOSPOLITEJ POLSKIEJ", "Wyrok", "Uchwała", "Sygn", "Przewodnicząc", "Protokolant", "Postanowienie"
]

MIN_MATCHES = 3

def count_matches(text: str) -> int:
    counter = 0
    for pattern in JUDGEMENT_PATTERNS:
        counter += re.search(pattern, text, re.IGNORECASE) is not None
    return counter

def looks_like_judgement(text: str) -> bool:
    if (count_matches(text) >= MIN_MATCHES):
        return True
    else:
        return False