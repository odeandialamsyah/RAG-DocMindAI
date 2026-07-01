from fastapi import APIRouter, UploadFile, File

from app.services.file_service import save_uploaded_file
from app.services.pdf_loader import extract_text, split_text
from app.database import documents_collection

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Simpan file
    filename, path = await save_uploaded_file(file)

    # Ekstrak isi PDF
    pages = extract_text(path)

    # Split menjadi beberapa chunk
    chunks = split_text(pages)

    pages = extract_text(path)

    add_chunks(
        chunks,
        filename
    )

    # Simpan metadata ke MongoDB
    document = {
        "original_name": file.filename,
        "stored_name": filename,
        "path": path,
        "status": "processed",
        "total_pages": len(pages),
        "total_chunks": len(chunks),
        "uploaded_at": datetime.utcnow()
    }

    result = documents_collection.insert_one(document)

    return {
        "message": "Upload success",
        "document_id": str(result.inserted_id),
        "filename": filename,
        "total_pages": len(pages),
        "total_chunks": len(chunks),
        "preview": chunks[:3]
    }