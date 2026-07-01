from pypdf import PdfReader


def extract_text(file_path: str):
    """
    Mengambil teks dari setiap halaman PDF.
    """

    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    return pages

def split_text(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for page in pages:

        texts = splitter.split_text(page["text"])

        for chunk in texts:

            chunks.append({
                "page": page["page"],
                "content": chunk
            })

    return chunks