# ParagrafAI

Asystent do polskiego prawa pracy i konsumenckiego. Projekt edukacyjny
łączący dwa podejścia:

- **fine-tuning** — model dostrojony do wyciągania ustrukturyzowanych danych
  z wyroków sądowych,
- **RAG** — odpowiadanie na pytania prawne w oparciu o treść ustaw,
  z cytowaniem artykułów.

Celem było przejście całej ścieżki: od przygotowania danych, przez trening
i serwowanie modelu, po RAG i integrację z MCP.

## Funkcje

- **`/extract`** — zamienia tekst wyroku na ustrukturyzowane dane (sąd, data,
  sygnatura, wydział, sędziowie, podstawy prawne).
- **`/ask`** — odpowiada na pytania zadane potocznie, w oparciu o przepisy,
  z numerami artykułów. Gdy przepisy nie zawierają odpowiedzi, sygnalizuje to
  zamiast zgadywać.

## Architektura

- **API (FastAPI)** — punkt wejścia z endpointami `/extract`, `/ask`,
  `/health` oraz warstwą zabezpieczeń.
- **Ollama** — serwuje modele: dostrojony do ekstrakcji, bazowy Bielik do
  generowania odpowiedzi i bge-m3 do embeddingów.
- **ChromaDB** — baza wektorowa z artykułami ustaw.
- **Serwer MCP** — wystawia funkcje API jako narzędzia dla asystenta AI.

Przepływ RAG: pytanie → embedding → wyszukanie artykułów w ChromaDB →
prompt z artykułami → odpowiedź modelu z cytatami.

## Jak to działa: fine-tuning vs RAG

- **fine-tuning uczy formatu**, nie wiedzy — model i tak wie, gdzie w wyroku
  jest data czy sąd, trening uczy go tylko konwencji odpowiedzi.
- **RAG dostarcza wiedzę** — zamiast polegać na pamięci modelu, podaje mu
  właściwe przepisy w prompcie, dzięki czemu nie zmyśla i cytuje źródła.

## Stack

Bielik-4.5B-v3.0-Instruct (fine-tuning QLoRA przez Unsloth), bge-m3,
ChromaDB, FastAPI, Ollama, Docker Compose, MCP. Dane: JuDDGES/pl-court-instruct
(trening), Kodeks pracy i ustawa o prawach konsumenta z ELI API (RAG).

## Uruchomienie

Wymagania: Docker Desktop z obsługą GPU (NVIDIA, WSL2).
Po uzupełnieniu `local.env` całość startuje przez `docker compose up`.
Modele rejestruje się w Ollama jednorazowo (szczegóły w kodzie pipeline'u).

## Kluczowe decyzje i problemy

- **Eksport do GGUF** dostrojonego modelu powodował zapętlanie przez błędne
  tokeny specjalne; rozwiązaniem było scalenie adaptera z modelem bazowym
  i kwantyzacja po stronie Ollamy.
- **Źródło przepisów:** ISAP blokuje automaty (robots.txt), więc dane pochodzą
  z oficjalnego ELI API. Pobierany jest najnowszy tekst jednolity, nie ustawy
  zmieniające.
- **Jakość danych treningowych:** etykiety są generowane automatycznie
  i bywają niepełne — w części przypadków model bywał dokładniejszy od wzorca.
- **Zabezpieczenia:** klucz API, walidacja wejścia (długość, heurystyka
  „czy to wyrok”), walidacja odpowiedzi modelu oraz próg odległości w RAG
  odrzucający pytania spoza zakresu przed wywołaniem modelu.

## Ograniczenia

Baza RAG odzwierciedla stan prawny na datę tekstu jednolitego, zakres
ograniczony do dwóch ustaw, projekt nie stanowi porady prawnej.