import streamlit as st
import os
import json
import tempfile
from pathlib import Path
import sys

# Add project root to path so src modules are always findable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.extractor import load_pdf, chunk_pages
from src.concepts import extract_all_concepts
from src.embeddings import generate_embeddings, find_similar_pairs
from src.graph import build_graph
from src.layout import compute_umap_layout
from src.visualize import build_plotly_graph
from src.animate import assign_clusters

# Page config must be first Streamlit command
st.set_page_config(
    page_title="Book Knowledge Graph",
    page_icon="📚",
    layout="wide"
)

def run_app():
    # ── Header ───────────────────────────────────────────────────
    st.title("📚 Book Knowledge Graph")
    st.markdown(
        "Transform any book PDF into an interactive knowledge graph. "
        "Upload a book and watch AI extract concepts, relationships, "
        "and build a visual map of the entire book's knowledge structure."
    )
    
    st.divider()
    
    # ── Sidebar Controls ─────────────────────────────────────────
    with st.sidebar:
        st.header("⚙️ Settings")
        
        max_chunks = st.slider(
            "Max chunks to process",
            min_value=10,
            max_value=200,
            value=50,
            help="More chunks = richer graph but higher cost and time"
        )
        
        similarity_threshold = st.slider(
            "Semantic similarity threshold",
            min_value=0.5,
            max_value=0.95,
            value=0.75,
            step=0.05,
            help="Higher = only very similar concepts get connected"
        )
        
        chunk_size = st.slider(
            "Chunk size (tokens)",
            min_value=500,
            max_value=2000,
            value=1000,
            step=100,
            help="Larger chunks = more context per LLM call"
        )
        
        st.divider()
        st.markdown("**How it works:**")
        st.markdown("1. Extract text from PDF")
        st.markdown("2. Split into smart chunks")
        st.markdown("3. LLM extracts concepts")
        st.markdown("4. Build knowledge graph")
        st.markdown("5. Visualize interactively")
    
    # ── File Upload ───────────────────────────────────────────────
    uploaded_file = st.file_uploader(
        "Upload your book PDF",
        type=["pdf"],
        help="Any non-fiction book works best"
    )
    
    if uploaded_file is None:
        st.info("👆 Upload a PDF to get started")
        
        # Show sample stats to build excitement
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg concepts extracted", "250+")
        with col2:
            st.metric("Avg relationships found", "200+")
        with col3:
            st.metric("Processing time", "~2 mins")
        return
    
    # ── Pipeline Execution ────────────────────────────────────────
    if st.button("🚀 Generate Knowledge Graph", type="primary"):
        
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        try:
            # Stage 1
            with st.status("📄 Extracting text from PDF...") as status:
                pages = load_pdf(tmp_path)
                st.write(f"✅ Extracted {len(pages)} pages")
                status.update(label="📄 Text extracted", state="complete")
            
            # Stage 2
            with st.status("✂️ Chunking text...") as status:
                chunks = chunk_pages(pages, chunk_size=chunk_size)
                st.write(f"✅ Created {len(chunks)} chunks")
                status.update(label="✂️ Chunking complete", state="complete")
            
            # Stage 3
            with st.status("🧠 Extracting concepts with AI...") as status:
                st.write(f"Processing {max_chunks} chunks...")
                results = extract_all_concepts(chunks, max_chunks=max_chunks)
                st.write(f"✅ Found {len(results['nodes'])} concepts")
                st.write(f"✅ Found {len(results['edges'])} relationships")
                status.update(label="🧠 Concepts extracted", state="complete")
            
            # Stage 4
            with st.status("🔢 Generating embeddings...") as status:
                nodes_with_embeddings = generate_embeddings(results["nodes"])
                similar_edges = find_similar_pairs(
                    nodes_with_embeddings, 
                    threshold=similarity_threshold
                )
                st.write(f"✅ Found {len(similar_edges)} semantic connections")
                status.update(label="🔢 Embeddings complete", state="complete")
            
            # Stage 5
            with st.status("🕸️ Building graph...") as status:
                G = build_graph(
                    nodes_with_embeddings,
                    results["edges"],
                    similar_edges
                )
                status.update(label="🕸️ Graph built", state="complete")
            
            # Stage 6
            with st.status("📐 Computing layout...") as status:
                pos = compute_umap_layout(G, nodes_with_embeddings)
                status.update(label="📐 Layout complete", state="complete")
            
            # Stage 7 — Render
            with st.status("🎨 Rendering visualization...") as status:
                fig = build_plotly_graph(G, pos)
                status.update(label="🎨 Visualization ready", state="complete")
            
            # ── Display Results ───────────────────────────────────
            st.success("✅ Knowledge graph generated successfully!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Concepts", G.number_of_nodes())
            with col2:
                st.metric("Relationships", G.number_of_edges())
            with col3:
                # Count clusters
                from src.animate import assign_clusters
                clusters = assign_clusters(G)
                unique_clusters = len(set(v["cluster_id"] for v in clusters.values()))
                st.metric("Clusters", unique_clusters)
            
            # Display interactive graph
            st.plotly_chart(fig, use_container_width=True)
            
            # Download button
            html_path = "output/knowledge_graph.html"
            build_plotly_graph(G, pos, html_path)
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            st.download_button(
                label="⬇️ Download Interactive Graph",
                data=html_content,
                file_name=f"{uploaded_file.name}_knowledge_graph.html",
                mime="text/html"
            )
            
        finally:
            os.unlink(tmp_path)

if __name__ == "__main__":
    run_app()