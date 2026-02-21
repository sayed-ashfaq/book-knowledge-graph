from src.extractor import load_pdf

pages = load_pdf("data/AIEngg_book.pdf")
# print(pages[0])  # See what page 1 looks like
# print(pages[5])  # See what page 5 looks likeS

from src.extractor import load_pdf, chunk_pages

chunks = chunk_pages(pages)

print(f"Total chunks: {len(chunks)}")
print(f"Sample chunk:\n{chunks[10]}")