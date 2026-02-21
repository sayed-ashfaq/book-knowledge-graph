import plotly.graph_objects as go
import networkx as nx
import json
import os
from src.graph import load_graph
from src.layout import load_layout
from src.animate import assign_clusters, CLUSTER_COLORS

def build_plotly_graph(G: nx.Graph, pos: dict, output_path: str = "output/knowledge_graph.html"):
    print("Building interactive Plotly graph...")
    
    node_clusters = assign_clusters(G)
    max_degree = max(dict(G.degree()).values())
    
    # ── Edge traces ──────────────────────────────────────────────
    # Separate LLM edges and embedding edges for different styling
    llm_edge_x, llm_edge_y = [], []
    emb_edge_x, emb_edge_y = [], []
    
    for u, v, data in G.edges(data=True):
        if u not in pos or v not in pos:
            continue
        
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        
        if data.get("edge_type") == "llm":
            llm_edge_x += [x0, x1, None]
            llm_edge_y += [y0, y1, None]
        else:
            emb_edge_x += [x0, x1, None]
            emb_edge_y += [y0, y1, None]
    
    llm_edge_trace = go.Scatter(
        x=llm_edge_x, y=llm_edge_y,
        mode='lines',
        line=dict(width=1.0, color='rgba(255,255,255,0.4)'),
        hoverinfo='Explisit',
        name='Explicit Relationship'
    )
    
    emb_edge_trace = go.Scatter(
        x=emb_edge_x, y=emb_edge_y,
        mode='lines',
        line=dict(width=0.5, color='rgba(0,102,255,0.2)'),
        hoverinfo='similarity',
        name='Semantic Similarity'
    )
    
    # ── Node trace ───────────────────────────────────────────────
    node_x, node_y = [], []
    node_colors, node_sizes = [], []
    node_text, node_hover = [], []
    
    for node in G.nodes():
        if node not in pos:
            continue
        
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Color by cluster
        color = node_clusters.get(node, {}).get("color", "#FFFFFF")
        node_colors.append(color)
        
        # Size by degree
        degree = G.degree(node)
        size = 8 + (degree / max_degree) * 40
        node_sizes.append(size)
        
        # Label — show on graph
        node_text.append(node if degree >= 4 else "")
        
        # Hover text — rich information
        description = G.nodes[node].get("description", "No description")
        cluster_id = node_clusters.get(node, {}).get("cluster_id", "?")
        node_hover.append(
            f"<b>{node}</b><br>"
            f"Connections: {degree}<br>"
            f"Cluster: {cluster_id}<br>"
            f"<i>{description}</i>"
        )
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        hovertext=node_hover,
        textposition='top center',
        textfont=dict(size=8, color='white'),
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=1, color='rgba(255,255,255,0.3)')
        ),
        name='Concepts'
    )
    
    # ── Layout ───────────────────────────────────────────────────
    layout = go.Layout(
        title=dict(
            text='📚 Book Knowledge Graph',
            font=dict(size=20, color='white'),
            x=0.5
        ),
        paper_bgcolor='#0D1117',
        plot_bgcolor='#0D1117',
        showlegend=True,
        legend=dict(
            font=dict(color='white'),
            bgcolor='rgba(0,0,0,0.5)'
        ),
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    fig = go.Figure(
        data=[llm_edge_trace, emb_edge_trace, node_trace],
        layout=layout
    )
    
    # Save as interactive HTML
    fig.write_html(output_path)
    print(f"Interactive graph saved to {output_path}")
    
    return fig

def build_plotly_3d_graph(G: nx.Graph, pos: dict, output_path: str = "output/knowledge_graph_3d.html"):
    print("Building 3D interactive Plotly graph...")
    
    node_clusters = assign_clusters(G)
    max_degree = max(dict(G.degree()).values())
    
    # ── Edge traces ───────────────────────────────────────────────
    llm_edge_x, llm_edge_y, llm_edge_z = [], [], []
    emb_edge_x, emb_edge_y, emb_edge_z = [], [], []
    
    for u, v, data in G.edges(data=True):
        if u not in pos or v not in pos:
            continue
        
        x0, y0, z0 = pos[u]
        x1, y1, z1 = pos[v]
        
        if data.get("edge_type") == "llm":
            llm_edge_x += [x0, x1, None]
            llm_edge_y += [y0, y1, None]
            llm_edge_z += [z0, z1, None]
        else:
            emb_edge_x += [x0, x1, None]
            emb_edge_y += [y0, y1, None]
            emb_edge_z += [z0, z1, None]
    
    llm_edge_trace = go.Scatter3d(
        x=llm_edge_x, y=llm_edge_y, z=llm_edge_z,
        mode='lines',
        line=dict(width=1.5, color='rgba(255,255,255,0.4)'),
        hoverinfo='name',
        name='Explicit Relationship'
    )
    
    emb_edge_trace = go.Scatter3d(
        x=emb_edge_x, y=emb_edge_y, z=emb_edge_z,
        mode='lines',
        line=dict(width=0.8, color='rgba(100,100,255,0.2)'),
        hoverinfo='name',
        name='Semantic Similarity'
    )
    
    # ── Node trace ────────────────────────────────────────────────
    node_x, node_y, node_z = [], [], []
    node_colors, node_sizes = [], []
    node_text, node_hover = [], []
    
    for node in G.nodes():
        if node not in pos:
            continue
        
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        
        color = node_clusters.get(node, {}).get("color", "#FFFFFF")
        node_colors.append(color)
        
        degree = G.degree(node)
        size = 4 + (degree / max_degree) * 20
        node_sizes.append(size)
        
        node_text.append(node if degree >= 4 else "")
        
        description = G.nodes[node].get("description", "No description")
        cluster_id = node_clusters.get(node, {}).get("cluster_id", "?")
        node_hover.append(
            f"<b>{node}</b><br>"
            f"Connections: {degree}<br>"
            f"Cluster: {cluster_id}<br>"
            f"<i>{description}</i>"
        )
    
    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        hovertext=node_hover,
        textposition='top center',
        textfont=dict(size=7, color='white'),
        marker=dict(
            size=node_sizes,
            color=node_colors,
            opacity=0.9,
            line=dict(width=0.5, color='rgba(255,255,255,0.3)')
        ),
        name='Concepts'
    )
    
    # ── 3D Layout ─────────────────────────────────────────────────
    layout = go.Layout(
        title=dict(
            text='📚 Book Knowledge Graph — 3D',
            font=dict(size=20, color='white'),
            x=0.5
        ),
        paper_bgcolor='#0D1117',
        scene=dict(
            bgcolor='#0D1117',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showbackground=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showbackground=False),
            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, showbackground=False),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        showlegend=True,
        legend=dict(font=dict(color='white'), bgcolor='rgba(0,0,0,0.5)'),
        hovermode='closest',
        margin=dict(l=0, r=0, t=60, b=0)
    )
    
    fig = go.Figure(
        data=[llm_edge_trace, emb_edge_trace, node_trace],
        layout=layout
    )
    
    fig.write_html(output_path)
    print(f"3D graph saved to {output_path}")
    
    return fig