from src.extractor import load_pdf, chunk_pages
from src.concepts import extract_all_concepts

pages = load_pdf("data/AIEngg_book.pdf")
chunks = chunk_pages(pages)

results = extract_all_concepts(chunks, max_chunks=5)

print(f"Nodes extracted: {len(results['nodes'])}")
print(f"Edges extracted: {len(results['edges'])}")
print("\nSample nodes:")
for node in results['nodes'][:5]:
    print(node)
print("\nSample edges:")
for edge in results['edges'][:5]:
    print(edge)