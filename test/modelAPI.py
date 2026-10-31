import fastapi from FastAPI

api = FastAPI("paragrafAI")

@api.get
def health():
    return 