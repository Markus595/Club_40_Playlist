from fastapi import FastAPI
from playlist_handler import router as playlist_router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(playlist_router, prefix="")

@app.get("/")
def root():
    return {"status": "Backend läuft ✅"}
