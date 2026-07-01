from fastapi import APIRouter

from pydantic import BaseModel

from app.services.rag import ask

from app.database import history_collection

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    answer, metadata = ask(request.question)

    history_collection.insert_one(
        {
            "question": request.question,
            "answer": answer
        }
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": metadata
    }