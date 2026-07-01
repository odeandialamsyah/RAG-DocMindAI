from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def create_embedding(text: str):
    """
    Menghasilkan embedding dari sebuah teks.
    """
    return model.encode(text).tolist()