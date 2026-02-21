from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(nodes: list[dict]) -> list[dict]:
    texts = [f"{n['id']}: {n['description']}" for n in nodes]
    
    print("Generating embeddings...")
    vectors = model.encode(texts, show_progress_bar=True)
    
    for i, node in enumerate(nodes):
        node["embedding"] = vectors[i].tolist()
    
    return nodes

def find_similar_pairs(nodes: list[dict], threshold: float = 0.75) -> list[dict]:
    vectors = np.array([n["embedding"] for n in nodes])
    
    # Normalize vectors for cosine similarity
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    normalized = vectors / norms
    
    # Dot product of normalized vectors = cosine similarity
    similarity_matrix = np.dot(normalized, normalized.T)
    
    similar_edges = []
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if similarity_matrix[i][j] > threshold:
                similar_edges.append({
                    "source": nodes[i]["id"],
                    "target": nodes[j]["id"],
                    "relationship": "semantically similar",
                    "weight": float(similarity_matrix[i][j])
                })
    
    return similar_edges

def save_embeddings(nodes: list[dict], path: str = "output/nodes_with_embeddings.json"):
    os.makedirs("output", exist_ok=True)
    with open(path, "w") as f:
        json.dump(nodes, f, indent=2)
    print(f"Embeddings saved to {path}")

def load_embeddings(path: str = "output/nodes_with_embeddings.json") -> list[dict]:
    with open(path, "r") as f:
        return json.load(f)