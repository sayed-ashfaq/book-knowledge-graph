# Interview Questions

### Questions before you build anything

1. You're about to start a real Python project that has maybe 15-20 different libraries — things like PDF readers, LLM clients, graph libraries, visualization tools.
If you just did pip install everything directly on your machine — what problem do you think could happen? --- Take a guess. There's no wrong answer here. Think about what happens if you have two different projects on the same machine that need different versions of the same library.--- What do you think? 

2. If you were organizing this project into folders, what folders would you create and why?
Don't worry about being perfect. Just think like someone who wants to find any file in this project 6 months later without confusion.

### Module 0 — Exit Quiz
You must answer these before we move to Module 1. Take your time, think it through.

Q1. What is the purpose of a virtual environment and what specific problem does it solve?

Q2. You're working on this project 3 months from now on a brand new laptop. You have your code but nothing else. What single file tells you exactly which libraries to install and at what versions — and what command would you run to restore everything instantly using UV?

Q3. Your friend clones your GitHub repo but your project crashes immediately because the LLM can't authenticate. You checked — all your code is correct. What's the most likely reason and what did you probably forget to tell your friend?


### Module 1
1. Why do you think we use Path from pathlib instead of just writing file paths as plain strings like "data/mybook.pdf"?

so that it can work in any environment or laptop or cloud and we can add extra features to it such as assign a root path and then add them to the folder path. hardcoding string is slow and manual which might cause issues.
* Exactly right. The technical term for what you described is cross-platform compatibility. On Windows paths look like data\mybook.pdf and on Mac/Linux they look like data/mybook.pdf. Path handles that difference automatically so your code works everywhere without you thinking about it.
* And your second point about building paths dynamically — spot on. Path("data") / "mybook.pdf" is cleaner and safer than string concatenation.

Q1. Our clean_text() function removes standalone numbers to eliminate page numbers. Can you think of a case where this regex might accidentally remove something important?

Q1 is exactly right — this is a real limitation we're accepting for now. In a production system you'd write smarter regex or use a proper NLP tokenizer to distinguish "page 47" from "revenue grew 47%". Good catch.

Q2. 3 pages were skipped because they had less than 50 characters after cleaning. What kind of pages were those likely to be in a real book?

Q2 — chapter titles and acknowledgements yes, also likely blank pages and full-image pages like diagrams or covers with no extractable text.

### Module 3 - Exit quiz
Module 3 Exit Quiz

Q1. Why did we use gpt-4o-mini instead of gpt-4o for this task?
* we are in developing and debugging phase, so in order to keep the costs low we are using mini, when in production we can use gpt-4o it gives better results and revenue will cover the costs.

Q2. Our parse_response function returns {"nodes": [], "edges": []} when JSON parsing fails instead of crashing. Why is this the right decision for a pipeline that processes 50+ chunks?
* You answered a different question. I asked why returning empty dict is the right decision instead of crashing. Think about it this way — if chunk 23 out of 50 returns malformed JSON and your code crashes, you lose all 22 chunks already processed. But if you return empty and continue, the pipeline finishes all 50 chunks and you only lose chunk 23's data.

The principle here is called **graceful degradation** — a system that partially succeeds is better than one that fully crashes. Your retry idea is also valid and is the next level improvement, but the foundation is don't crash the whole pipeline for one bad chunk.

Q3. Why is caching the concepts to a JSON file important during development?
* All these steps takes time and api calls which reduces the productivity, so we cache it and make the process faster.

### Module 4 — Embeddings 🔢
1. Which model did you use for embeddings?
> I have used open source embedding model from huggingface which is `all-MiniLM-L6-v2`.


#### Exit Questions
Q1. We encoded nodes as "concept name: description" instead of just the concept name. Why does including the description produce better embeddings?

Q2. We used threshold=0.75. If you lowered it to 0.50 what problem would appear in your graph?

Q3. In one sentence — what is the fundamental difference between what LLM edges and embedding edges represent?

Answers: 
1. Adding description to the helps the llm to understand what's inside the content and for that it can create better embeddings here. 
2. Threshold is the semantic similarity. adding greater threshold will make the content more meaningful, if you lowered the threshold then few nodes might have mixed content that is irrelevant.
3. This part i don't understand much, if i have to guess - llm edges are more keywords based where it have many values across the system which makes it harder and slower to access. Where as embedding are more meaning full edges which can be retrived faster and more accurate.

Q1 — Correct. More context gives the model more signal to place the vector accurately in semantic space.

Q2 — Correct direction, but sharpen the answer. At 0.50 threshold, concepts that are only vaguely related start connecting — imagine AI Engineering and Software Testing getting linked just because they're both tech topics. Your graph becomes a densely connected mess where everything relates to everything, which makes the visualization meaningless.

Q3 — Good intuition but let me give you the precise answer because this is important.<br>
LLM edges = explicit relationships. The model read the text and said "these two concepts are connected because the author connected them." There's a reason — causes, enables, contradicts.<br>
Embedding edges = implicit relationships. We mathematically measured that two concepts live close together in meaning-space, even if the author never explicitly connected them in the same sentence.<br>
One is semantic reasoning, the other is geometric similarity. Both are valuable for different reasons.

### Module 5 - Graph Construction 🕸️

Q1. Node size is currently set to G.degree(node) — the number of connections. Why is degree a good proxy for concept importance in a knowledge graph?
> If a concept connects to many other concepts, it means many different ideas in the book reference it or relate to it. That makes it central to the book's thesis. AI Engineering having 11 connections means 11 other concepts depend on or relate to it — it's a hub concept, not a peripheral one. High degree = high importance.

Q2. We check if G.has_node(source) and G.has_node(target) before adding edges. What problem are we preventing here?
> LLM sometimes hallucinates edge targets. It might create an edge from Habit Loop to Neural Rewiring but if Neural Rewiring never appeared as a node in any chunk, adding that edge would reference a non-existent node and corrupt the graph structure.

Q3. We have 252 nodes but started with 51 deduplicated nodes from 5 chunks. We then ran 50 chunks for embeddings. Does 252 nodes seem reasonable to you and why? 🤔
- If 51 nodes from 5 chunk then for 50 it should 250 which is completly resonable, -> Perfect math instinct. 51 nodes from 5 chunks × 10 = ~250 nodes from 50 chunks. 252 is exactly in that range. Your estimation thinking is solid.



#### Notes Universal: 
1. Don't just go forward without completing something fully, Runs the Code - OK. Is output got what you desired do not move forward. Work more on output understand is that the output you are going to present, No right then keep iterating.

