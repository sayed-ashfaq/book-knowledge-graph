import fitz
import re
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

def clean_text(text: str) -> str:
    text = re.sub(r'-\n', '', text)           # Fix hyphenated line breaks
    text = re.sub(r'\n+', ' ', text)          # Replace newlines with spaces
    text = re.sub(r'\s+', ' ', text)          # Collapse multiple spaces
    text = re.sub(r'\b\d+\b', '', text)       # Remove standalone numbers (page nums)
    text = re.sub(r'(CHAPTER|Chapter)\s+\w+', '', text)  # Remove chapter headers
    return text.strip()

def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    pdf_path = Path(pdf_path)
    doc = fitz.open(pdf_path)
    pages = []

    for page_num, page in enumerate(doc, start=1):
        raw_text = page.get_text()
        cleaned = clean_text(raw_text)

        if len(cleaned.strip()) < 50:
            continue

        pages.append({
            "page": page_num,
            "text": cleaned
        })

    doc.close()
    return pages

def load_pdf(pdf_path: str) -> list[dict]:
    pages = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(pages)} pages from {Path(pdf_path).name}")
    return pages


def chunk_pages(pages: list[dict], chunk_size: int = 1000, overlap: int = 150) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " "]
    )
    
    all_chunks = []
    
    for page in pages:
        chunks = splitter.split_text(page["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "page": page["page"],
                "chunk_index": i,
                "text": chunk
            })
    
    return all_chunks