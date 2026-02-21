import networkx as nx
import numpy as np
from src.graph import load_graph
import json
import os

def compute_spring_layout(G: nx.Graph, seed: int = 42) -> dict:
    print("Computing spring layout...")
    
    # k controls spacing between nodes — higher k = more spread out
    # iterations controls how long physics simulation runs
    pos = nx.spring_layout(
        G,
        k=2.0,
        iterations=100,
        seed=seed
    )
    
    # Convert numpy arrays to plain lists for JSON serialization
    pos_serializable = {node: pos[node].tolist() for node in pos}
    return pos_serializable

def compute_umap_layout(G: nx.Graph, nodes_with_embeddings: list[dict]) -> dict:
    print("Computing UMAP layout...")
    
    try:
        import umap
        
        # Build a lookup for embeddings by node id
        embedding_lookup = {
            n["id"]: n["embedding"] 
            for n in nodes_with_embeddings 
            if "embedding" in n
        }
        
        # Only use nodes that exist in both graph and embeddings
        valid_nodes = [n for n in G.nodes() if n in embedding_lookup]
        vectors = np.array([embedding_lookup[n] for n in valid_nodes])
        
        reducer = umap.UMAP(
            n_components=3,
            random_state=42,
            min_dist=0.3,
            n_neighbors=15
        )
        
        embedding_2d = reducer.fit_transform(vectors)
        
        pos = {}
        for i, node in enumerate(valid_nodes):
            pos[node] = [
                float(embedding_3d[i][0]),
                float(embedding_3d[i][1]),
                float(embedding_3d[i][2])  # z coordinate
            ]
            
        # Handle any nodes without embeddings using spring layout fallback
        missing = [n for n in G.nodes() if n not in pos]
        if missing:
            print(f"  {len(missing)} nodes missing embeddings, using spring fallback")
            spring_pos = nx.spring_layout(G, seed=42, dim=3)
            for node in missing:
                p = spring_pos[node].tolist()
                pos[node] = p if len(p) == 3 else p + [0.0]
        
        return pos
        
    except Exception as e:
        print(f"UMAP failed: {e}, falling back to spring layout")
        return compute_spring_layout(G)

def save_layout(pos: dict, path: str = "output/layout.json"):
    os.makedirs("output", exist_ok=True)
    with open(path, "w") as f:
        json.dump(pos, f, indent=2)
    print(f"Layout saved to {path}")

def load_layout(path: str = "output/layout.json") -> dict:
    with open(path, "r") as f:
        return json.load(f)