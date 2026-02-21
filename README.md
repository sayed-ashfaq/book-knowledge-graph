# 📚 Book Knowledge Graph
<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/OpenAI-000000?style=for-the-badge&logo=openai&logoColor=white"/>
<img src="https://img.shields.io/badge/SentenceTransformers-FFCC00?style=for-the-badge"/>
<img src="https://img.shields.io/badge/UMAP-8A2BE2?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

</p>
## The Problem Statement

Most books contain hundreds of interconnected ideas, concepts, and relationships — but when you read linearly, your brain processes them as a *sequence*, not as a *network*. You finish a book and have a vague sense of the ideas but no clear map of how they connect.


Transform any book PDF into a beautiful, interactive 3D knowledge graph using AI.

**Our system solves this.** You give it any book as a PDF. It reads the entire book, figures out the key concepts and how they relate to each other, and then builds and *visually grows* a knowledge graph — a living map of the book's ideas.

## Example Scenario

Say you feed it **"Atomic Habits" by James Clear.**

The system will:

1. **Extract text** from the PDF, chapter by chapter
2. **Identify key concepts** — things like `Habit Loop`, `Cue`, `Routine`, `Reward`, `Identity`, `1% Improvement`, `Environment Design`
3. **Identify relationships** — `Cue` *triggers* `Routine`, `Routine` *produces* `Reward`, `Identity` *drives* `Habit Loop`, and so on
4. **Build a graph** where each concept is a node and each relationship is an edge connecting them
5. **Animate it growing** — you watch the graph build itself chapter by chapter, new nodes appearing, edges forming in real time
6. **Let you interact** with the final map — hover over `Identity` and see the exact quote from the book that produced that node, click a node to see what it connects to

The final output looks like a **living mind map of the entire book**, built automatically by AI.

## Assets

<p align="center">
  <a href="./output/knowledge_graph_3d.html">
    <img src="https://img.shields.io/badge/Open-3D%20Knowledge%20Graph-blue?style=for-the-badge"/>
  </a>
</p>


## Why Is This Hard and Interesting?

Because none of those steps are trivial. The LLM has to *understand* the text well enough to extract meaningful concepts. The graph has to be structured so relationships have *weight and direction*. The layout algorithm has to place nodes so that *visually similar concepts cluster together*. And the whole thing has to work on *any* book, not just one.


## Tech Stack

| Layer | Tool |
|---|---|
| PDF Extraction | PyMuPDF |
| Text Chunking | LangChain |
| Concept Extraction | OpenAI GPT-4o-mini |
| Embeddings | sentence-transformers |
| Graph Construction | NetworkX |
| Layout | UMAP |
| Visualization | Plotly |
| Web App | Streamlit |



## Project Structure


```
book-knowledge-graph/
│
├── data/                  # Input PDFs
├── output/                # Generated graphs and cache
├── src/
│   ├── extractor.py       # PDF reading and chunking
│   ├── concepts.py        # LLM concept extraction
│   ├── embeddings.py      # Semantic embeddings
│   ├── graph.py           # Graph construction
│   ├── layout.py          # UMAP 3D layout
│   ├── animate.py         # Cluster detection and animation
│   ├── visualize.py       # Plotly 2D and 3D output
│   └── app.py             # Streamlit web app
│
├── .env                   # API keys (never commit this)
├── .gitignore
├── pyproject.toml
└── main.py
```

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/yourname/book-knowledge-graph
cd book-knowledge-graph
```

**2. Create virtual environment**
```bash
uv venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

**3. Install dependencies**
```bash
uv sync
```

**4. Add your API key**

Create a `.env` file in the project root —
```
OPENAI_API_KEY=your_key_here
```

## Run

**Web app (recommended)**
```bash
uv run streamlit run src/app.py
```

**Pipeline directly**
```bash
uv run python main.py
```


## App Controls

| Setting | What It Does |
|---|---|
| Max chunks | How much of the book to process. More = richer graph, higher cost |
| Similarity threshold | How similar two concepts must be to get connected. Higher = stricter |
| Chunk size | How much text per LLM call. Larger = more context |
| View mode | Switch between 2D interactive and 3D rotating graph |


## How It Works

1. **Extract** — PyMuPDF pulls clean text from the PDF, removing headers, footers, and page numbers
2. **Chunk** — LangChain splits text into overlapping chunks so no concept falls through a boundary
3. **Extract concepts** — GPT-4o-mini reads each chunk and returns structured JSON of nodes and edges
4. **Embed** — sentence-transformers converts every concept into a vector so hidden semantic relationships can be found
5. **Build graph** — NetworkX combines LLM edges and embedding similarity edges into a weighted graph
6. **Layout** — UMAP reduces 384-dimensional embeddings into 3D coordinates where similar concepts cluster together
7. **Visualize** — Plotly renders the final interactive graph


## Output Files

| File | Description |
|---|---|
| `output/concepts.json` | Cached LLM extractions — delete to re-extract |
| `output/nodes_with_embeddings.json` | Concepts with embedding vectors |
| `output/graph.json` | Full NetworkX graph |
| `output/layout.json` | 3D node positions — delete when switching 2D/3D |
| `output/knowledge_graph.html` | Standalone interactive 2D graph |
| `output/knowledge_graph_3d.html` | Standalone interactive 3D graph |


## Tips

- Works best on non-fiction books with clear concepts and relationships
- Delete `output/layout.json` any time you change UMAP parameters
- Keep `output/concepts.json` to avoid re-running expensive API calls during development
- Start with `max_chunks=50` for development, increase for production runs


## Built With

This project was built as a learning exercise covering PDF processing, prompt engineering, embeddings, graph theory, dimensionality reduction, and interactive visualization — end to end in Python.
