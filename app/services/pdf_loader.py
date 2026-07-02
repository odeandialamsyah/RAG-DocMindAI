from pypdf import PdfReader

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        RecursiveCharacterTextSplitter = None


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
    if RecursiveCharacterTextSplitter is None:
        splitter = None
    else:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    chunks = []

    for page in pages:
        text = page["text"]

        if splitter is not None:
            texts = splitter.split_text(text)
        else:
            texts = []
            start = 0
            chunk_size = 500
            chunk_overlap = 100
            while start < len(text):
                end = min(start + chunk_size, len(text))
                texts.append(text[start:end])
                start += chunk_size - chunk_overlap
                if start < 0:
                    start = 0

        for chunk in texts:
            chunks.append({
                "page": page["page"],
                "content": chunk
            })

    return chunks