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
    message = client.messages.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Extract concepts from this text:\n\n{chunk}"}
        ]
    )
    
    raw = message.content[0].text
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

def extract_all_concepts(chunks: list[dict], max_chunks: int = 50) -> dict:
    all_nodes = []
    all_edges = []
    
    # Limit chunks for cost control during development
    selected = chunks[:max_chunks]
    
    for i, chunk in enumerate(selected):
        print(f"Processing chunk {i+1}/{len(selected)}...")
        result = extract_concepts(chunk["text"])
        all_nodes.extend(result["nodes"])
        all_edges.extend(result["edges"])
    
    return {
        "nodes": all_nodes,
        "edges": all_edges
    }