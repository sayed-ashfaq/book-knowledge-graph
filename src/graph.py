import networkx as nx
import json
import os

def build_graph(nodes: list[dict], llm_edges: list[dict], embedding_edges: list[dict]) -> nx.Graph:
    G = nx.Graph()
    
    # Add nodes with all their attributes
    for node in nodes:
        G.add_node(
            node["id"],
            description=node.get("description", ""),
            size=1  # We'll update this based on importance
        )
    
    # Add LLM edges — high confidence, full weight
    for edge in llm_edges:
        source = edge["source"]
        target = edge["target"]
        
        # Only add edge if both nodes exist in graph
        if G.has_node(source) and G.has_node(target):
            G.add_edge(
                source,
                target,
                relationship=edge["relationship"],
                weight=1.0,
                edge_type="llm"
            )
    
    # Add embedding edges — lower confidence, weighted by similarity
    for edge in embedding_edges:
        source = edge["source"]
        target = edge["target"]
        
        if G.has_node(source) and G.has_node(target):
            # Don't overwrite existing LLM edge
            if not G.has_edge(source, target):
                G.add_edge(
                    source,
                    target,
                    relationship="semantically similar",
                    weight=edge["weight"],
                    edge_type="embedding"
                )
    
    # Update node size based on degree (how many connections it has)
    for node in G.nodes():
        G.nodes[node]["size"] = G.degree(node)
    
    return G

def graph_stats(G: nx.Graph):
    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")
    print(f"Most connected nodes:")
    
    # Sort by degree and show top 5
    top_nodes = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:5]
    for node, degree in top_nodes:
        print(f"  {node} — {degree} connections")

def save_graph(G: nx.Graph, path: str = "output/graph.json"):
    os.makedirs("output", exist_ok=True)
    data = nx.node_link_data(G)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Graph saved to {path}")

def load_graph(path: str = "output/graph.json") -> nx.Graph:
    with open(path, "r") as f:
        data = json.load(f)
    return nx.node_link_graph(data)