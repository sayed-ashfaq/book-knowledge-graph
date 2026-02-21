from src.extractor import load_pdf, chunk_pages
from src.concepts import extract_all_concepts, save_concepts, load_concepts
import os

pages = load_pdf("data/AIEngg_book.pdf")
chunks = chunk_pages(pages)

if os.path.exists("output/concepts.json"):
    print("Loading cached concepts...")
    results = load_concepts()
else:
    results = extract_all_concepts(chunks, max_chunks=50)
    save_concepts(results)

print(f"Nodes: {len(results['nodes'])}, Edges: {len(results['edges'])}")