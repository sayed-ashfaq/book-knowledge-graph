import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np
from src.graph import load_graph
from src.layout import load_layout
import json
import os

# Dark theme colors for clusters
CLUSTER_COLORS = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
    '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F',
    '#BB8FCE', '#85C1E9'
]

def assign_clusters(G: nx.Graph) -> dict:
    # Use community detection to find clusters
    from networkx.algorithms import community
    
    communities = community.greedy_modularity_communities(G)
    
    node_cluster = {}
    for i, comm in enumerate(communities):
        color = CLUSTER_COLORS[i % len(CLUSTER_COLORS)]
        for node in comm:
            node_cluster[node] = {
                "cluster_id": i,
                "color": color
            }
    
    return node_cluster

def get_node_order(G: nx.Graph) -> list:
    # Sort nodes by degree descending — most connected appear first
    return [node for node, degree in sorted(
        G.degree(), key=lambda x: x[1], reverse=True
    )]

def build_animation(G: nx.Graph, pos: dict, output_path: str = "output/knowledge_graph.gif"):
    print("Building animation...")
    
    node_clusters = assign_clusters(G)
    node_order = get_node_order(G)
    
    # Setup figure with dark theme
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    fig.patch.set_facecolor('#0D1117')
    ax.set_facecolor('#0D1117')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Convert pos keys to match graph nodes
    valid_pos = {n: pos[n] for n in G.nodes() if n in pos}
    
    # Precompute node sizes based on degree
    max_degree = max(dict(G.degree()).values())
    
    def get_node_size(node):
        degree = G.degree(node)
        # Scale between 100 and 800
        return 100 + (degree / max_degree) * 700
    
    # Animation step — show first N nodes and their edges
    def animate(frame):
        ax.clear()
        ax.set_facecolor('#0D1117')
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Nodes visible in this frame
        visible_nodes = node_order[:frame+1]
        visible_set = set(visible_nodes)
        
        # Only draw edges where both nodes are visible
        visible_edges = [
            (u, v) for u, v in G.edges()
            if u in visible_set and v in visible_set
        ]
        
        # Draw edges
        for u, v in visible_edges:
            x = [valid_pos[u][0], valid_pos[v][0]]
            y = [valid_pos[u][1], valid_pos[v][1]]
            weight = G[u][v].get("weight", 0.5)
            edge_type = G[u][v].get("edge_type", "llm")
            
            color = '#FFFFFF' if edge_type == "llm" else '#444444'
            ax.plot(x, y, color=color, alpha=weight * 0.6, linewidth=0.8)
        
        # Draw nodes
        for node in visible_nodes:
            if node not in valid_pos:
                continue
            x, y = valid_pos[node]
            color = node_clusters.get(node, {}).get("color", "#FFFFFF")
            size = get_node_size(node)
            
            ax.scatter(x, y, c=color, s=size, alpha=0.9, zorder=5)
            
            # Only label high degree nodes to avoid clutter
            if G.degree(node) >= 4:
                ax.annotate(
                    node,
                    (x, y),
                    fontsize=6,
                    color='white',
                    ha='center',
                    va='bottom',
                    xytext=(0, 8),
                    textcoords='offset points'
                )
        
        # Title
        ax.set_title(
            f'Knowledge Graph — {frame+1}/{len(node_order)} concepts',
            color='white',
            fontsize=12,
            pad=10
        )
    
    # Only animate every 3rd node for speed
    frames = range(0, len(node_order), 3)
    
    anim = animation.FuncAnimation(
        fig,
        animate,
        frames=frames,
        interval=100,
        repeat=False
    )
    
    print(f"Saving animation to {output_path}...")
    anim.save(output_path, writer='pillow', fps=10, dpi=80)
    plt.close()
    print("Animation complete!")
    
    return output_path