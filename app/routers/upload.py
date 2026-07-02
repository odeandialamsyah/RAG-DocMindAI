from datetime import datetime

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.database import documents_collection
from app.services.chroma_service import add_chunks
from app.services.file_service import save_uploaded_file
from app.services.pdf_loader import extract_text, split_text

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Simpan file
    filename, path = await save_uploaded_file(file)

    try:
        # Ekstrak isi PDF
        pages = extract_text(path)

        # Split menjadi beberapa chunk
        chunks = split_text(pages)

        add_chunks(chunks, filename)

        # Simpan metadata ke MongoDB
        document = {
            "original_name": file.filename,
            "stored_name": filename,
            "path": path,
            "status": "processed",
            "total_pages": len(pages),
            "total_chunks": len(chunks),
            "uploaded_at": datetime.utcnow(),
        }

        result = documents_collection.insert_one(document)

        return {
            "message": "Upload success",
            "document_id": str(result.inserted_id),
            "filename": filename,
            "total_pages": len(pages),
            "total_chunks": len(chunks),
            "preview": chunks[:3],
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(exc)}") from exc