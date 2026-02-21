from openai import OpenAI
import json
import re
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are a knowledge graph extractor. Given a passage of text, extract the key concepts and relationships.

Rules:
- Extract 3 to 7 most important concepts per passage. No more, no less.
- Concepts must be meaningful ideas, theories, or principles — NOT people, chapter titles, or book names
- Relationships must be concise verb phrases: "enables", "causes", "depends on", "contradicts"
- Every edge source and target must exactly match a node id
- Return ONLY raw JSON. No markdown. No explanation. No code blocks.

Output format:
{
  "nodes": [
    {"id": "concept name", "description": "one sentence explanation"}
  ],
  "edges": [
    {"source": "concept name", "target": "concept name", "relationship": "verb phrase"}
  ]
}
"""

def extract_concepts(chunk: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cost efficient for development
        max_tokens=1024,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Extract concepts from this text:\n\n{chunk}"}
        ]
    )
    
    raw = response.choices[0].message.content
    return parse_response(raw)

def parse_response(raw: str) -> dict:
    # Strip markdown code blocks if LLM adds them anyway
    raw = re.sub(r'```json|```', '', raw).strip()
    
    try:
        data = json.loads(raw)
        # Validate structure exists
        if "nodes" not in data or "edges" not in data:
            return {"nodes": [], "edges": []}
        return data
    except json.JSONDecodeError:
        return {"nodes": [], "edges": []}

def deduplicate_nodes(nodes: list[dict]) -> list[dict]:
    seen = {}
    for node in nodes:
        # Normalize to lowercase for comparison
        key = node["id"].lower().strip()
        if key not in seen:
            seen[key] = node
    return list(seen.values())

def extract_all_concepts(chunks: list[dict], max_chunks: int = 50) -> dict:
    all_nodes = []
    all_edges = []
    
    selected = chunks[:max_chunks]
    
    for i, chunk in enumerate(selected):
        print(f"Processing chunk {i+1}/{len(selected)}...")
        result = extract_concepts(chunk["text"])
        all_nodes.extend(result["nodes"])
        all_edges.extend(result["edges"])
    
    # Deduplicate before returning
    unique_nodes = deduplicate_nodes(all_nodes)
    
    print(f"\nRaw nodes: {len(all_nodes)} → After dedup: {len(unique_nodes)}")
    
    return {
        "nodes": unique_nodes,
        "edges": all_edges
    }

# we shouldn't re-run 50 API calls every time we restart the script during development. We need to cache the results to a JSON file.

import os

def save_concepts(data: dict, path: str = "output/concepts.json"):
    os.makedirs("output", exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Concepts saved to {path}")

def load_concepts(path: str = "output/concepts.json") -> dict:
    with open(path, "r") as f:
        return json.load(f)