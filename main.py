# from src.extractor import load_pdf, chunk_pages
# from src.concepts import extract_all_concepts, save_concepts, load_concepts
# import os

# pages = load_pdf("data/AIEngg_book.pdf")
# chunks = chunk_pages(pages)

# if os.path.exists("output/concepts.json"):
#     print("Loading cached concepts...")
#     results = load_concepts()
# else:
#     results = extract_all_concepts(chunks, max_chunks=50)
#     save_concepts(results)

# print(f"Nodes: {len(results['nodes'])}, Edges: {len(results['edges'])}")

# ## MODULE 4 - EMBEDDINGS
# from src.extractor import load_pdf, chunk_pages
# from src.concepts import extract_all_concepts, save_concepts, load_concepts
# from src.embeddings import generate_embeddings, find_similar_pairs, save_embeddings, load_embeddings
# import os

# pages = load_pdf("data/AIEngg_book.pdf")
# chunks = chunk_pages(pages)

# if os.path.exists("output/concepts.json"):
#     print("Loading cached concepts...")
#     results = load_concepts()
# else:
#     results = extract_all_concepts(chunks, max_chunks=50)
#     save_concepts(results)

# if os.path.exists("output/nodes_with_embeddings.json"):
#     print("Loading cached embeddings...")
#     nodes_with_embeddings = load_embeddings()
# else:
#     nodes_with_embeddings = generate_embeddings(results["nodes"])
#     save_embeddings(nodes_with_embeddings)

# similar_edges = find_similar_pairs(nodes_with_embeddings, threshold=0.75)
# print(f"Similar pairs found: {len(similar_edges)}")
# print(f"Sample similar pair: {similar_edges[0] if similar_edges else 'None'}")


# ## ------ Module 5 -Graph Construction 🕸️ ----------------##
# from src.extractor import load_pdf, chunk_pages
# from src.concepts import extract_all_concepts, save_concepts, load_concepts
# from src.embeddings import generate_embeddings, find_similar_pairs, save_embeddings, load_embeddings
# from src.graph import build_graph, graph_stats, save_graph, load_graph
# import os

# # pages = load_pdf("data/yourbook.pdf")
# # chunks = chunk_pages(pages)

# if os.path.exists("output/concepts.json"):
#     results = load_concepts()
# else:
#     results = extract_all_concepts(chunks, max_chunks=50)
#     save_concepts(results)

# if os.path.exists("output/nodes_with_embeddings.json"):
#     nodes_with_embeddings = load_embeddings()
# else:
#     nodes_with_embeddings = generate_embeddings(results["nodes"])
#     save_embeddings(nodes_with_embeddings)

# similar_edges = find_similar_pairs(nodes_with_embeddings, threshold=0.75)

# if os.path.exists("output/graph.json"):
#     G = load_graph()
# else:
#     G = build_graph(nodes_with_embeddings, results["edges"], similar_edges)
#     save_graph(G)

# graph_stats(G)

# ========================X Module 6 — Layout & Positioning 📐 X========================#

from src.extractor import load_pdf, chunk_pages
from src.concepts import extract_all_concepts, save_concepts, load_concepts
from src.embeddings import generate_embeddings, find_similar_pairs, save_embeddings, load_embeddings
from src.graph import build_graph, graph_stats, save_graph, load_graph
from src.layout import compute_umap_layout, save_layout, load_layout
from src.animate import build_animation
from src.visualize import build_plotly_graph

import os

# pages = load_pdf("data/yourbook.pdf")
# chunks = chunk_pages(pages)

if os.path.exists("output/concepts.json"):
    results = load_concepts()
else:
    results = extract_all_concepts(chunks, max_chunks=50)
    save_concepts(results)

if os.path.exists("output/nodes_with_embeddings.json"):
    nodes_with_embeddings = load_embeddings()
else:
    nodes_with_embeddings = generate_embeddings(results["nodes"])
    save_embeddings(nodes_with_embeddings)

similar_edges = find_similar_pairs(nodes_with_embeddings, threshold=0.75)

if os.path.exists("output/graph.json"):
    G = load_graph()
else:
    G = build_graph(nodes_with_embeddings, results["edges"], similar_edges)
    save_graph(G)

if os.path.exists("output/layout.json"):
    pos = load_layout()
else:
    pos = compute_umap_layout(G, nodes_with_embeddings)
    save_layout(pos)

graph_stats(G)
print(f"Layout computed for {len(pos)} nodes")


# build_animation(G, pos)

build_plotly_graph(G, pos)