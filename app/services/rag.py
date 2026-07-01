from app.services.chroma_service import search
from app.services.gemini import ask_gemini


def ask(question: str):

    result = search(question)

    documents = result["documents"][0]

    metadatas = result["metadatas"][0]

    context = ""

    for i, doc in enumerate(documents):

        page = metadatas[i]["page"]

        context += f"""
Page {page}

{doc}

-------------------

"""

    prompt = f"""
Kamu adalah AI yang hanya boleh menjawab berdasarkan context.

Jika jawaban tidak ada pada context,
jawab:

"Jawaban tidak ditemukan pada dokumen."

Context:

{context}

Question:

{question}

Jawaban:
"""

    answer = ask_gemini(prompt)

    return answer, metadatas