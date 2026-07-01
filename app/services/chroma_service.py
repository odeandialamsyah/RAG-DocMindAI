import chromadb

from app.services.embedding import create_embedding

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)

def add_chunks(chunks, filename):

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(f"{filename}_{index}")

        documents.append(chunk["content"])

        embeddings.append(
            create_embedding(chunk["content"])
        )

        metadatas.append({
            "page": chunk["page"],
            "filename": filename
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

def search(question, top_k=3):

    embedding = create_embedding(question)

    result = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    return result