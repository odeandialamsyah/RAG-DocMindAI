from fastapi import FastAPI

from app.routers.upload import router as upload_router
from app.routers.chat import router as chat_router

app = FastAPI(
    title="Simple RAG API",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {
        "message": "Simple RAG API is running"
    }