# Concepts

## Module 1 — PDF Reading & Text Extraction 📄

Before we touch any code, intuition first.

---

### Think About This

A PDF is not a text file. When you save a Word document as PDF, the PDF format doesn't actually store "paragraphs" and "sentences" the way you'd think. It stores **drawing instructions** — "place this character at x=102, y=340, font=Arial, size=12."

So when we want to *read* a PDF programmatically, we're essentially reconstructing text from a set of visual positioning instructions.

**This means extraction can get messy.** Headers, footers, page numbers, footnotes, weird spacing — all of that comes along for the ride.

---

### Before I Show You Anything —

Think about a real book PDF. Imagine you're extracting text from it to later send to an LLM for concept extraction.

**What kinds of "noise" or unwanted content do you think would appear in the raw extracted text that you'd want to clean up before sending it to an LLM?**
> The noise could be headers, footer and pagenumbers, index pages, broken lines as well need to be considered - they either repeat in each page or unnecessary which pollutes context windows, and llm might think they are important. 
> one more thing is that hypheneted line breaks - When extracted naively, this becomes environ- and mental as separate pieces. The LLM might not reconnect them properly. So we need to handle that too.

## Module 2 -- Text Chunking

Q1. Why did chunk count drop from 1632 to 1273 when we switched from page-by-page to full-text chunking?
* Page by page created many small underfilled chunks at page boundaries. Full text lets the splitter pack chunks properly to their capacity.

Q2. We set overlap=150. If you increased this to overlap=400 what are the two tradeoffs — one benefit, one problem?
* The real problem with large overlap is redundancy - if chunks overlap too much, the same text gets sent to the LLM multiple times, which means duplicate concept extractions, higher cost, and a noisier graph. The LLM might extract the same concept 5 times from 5 overlapping chunks

## Module 3 -- Concept Extraction with LLM 🧠

#### Prompt Formatting
1. You need to write a system prompt that instructs the LLM to extract concepts and relationships. What instructions would you give the LLM to make sure it returns consistent, clean, structured JSON every single time?
* You are an intelligent content formatter who is great building knowledge graphs. You will be given content and you have format it into JSON format that is specified below. You have to strictly adhere to the format, should not give anything other than this. 
The content: {content} 
The jSON format: format
> correction by llm 
```
Good start. You got the core ideas right — role assignment, content injection, format specification, and strict adherence instruction. That's solid prompt engineering instinct.

But there are gaps that will cause real problems at scale. Let me point them out 

Problem 1 — You didn't tell it what a concept is. The LLM will guess. On one chunk it might extract James Clear as a node, on another it extracts Page Layout as a node. Without a definition, consistency breaks.

Problem 2 — You didn't limit the number of nodes per chunk. Without a limit, some chunks return 3 nodes, others return 25. Your graph becomes unbalanced.

Problem 3 — You didn't handle the relationship label. Without guidance, one chunk returns "reinforces", another returns "is related to", another returns "has a connection with". Inconsistent edge labels make graph analysis meaningless.

Problem 4 — You didn't explicitly say "no markdown, no explanation, raw JSON only." LLMs love to wrap JSON in ```json blocks or add "Here is your JSON:" before it. That breaks your parser instantly.
```

2. Notice `max_chunks=50` in `extract_all_concepts`.<br>
Why do you think I added that limit for development? What would happen if you ran all 1273 chunks right now? 🤔

* That's one reason yes. But there's a more important reason — cost.
* 1273 chunks × 1 API call each = 1273 API calls to Claude. Each call sends ~1000 tokens and receives ~500 tokens. That's roughly 1.9 million tokens in one run. Depending on the model that could cost you real money during a debugging session where you're just testing if the output format is correct.
* Always develop and debug on a small sample. Only run the full dataset when you're confident the code is correct. That's standard practice in ML engineering.

> Module 3 output
```bash
Extracted 988 pages from AIEngg_book.pdf
Processing chunk 1/10...
Processing chunk 2/10...
Processing chunk 3/10...
Processing chunk 4/10...
Processing chunk 5/10...
Processing chunk 6/10...
Processing chunk 7/10...
Processing chunk 8/10...
Processing chunk 9/10...
Processing chunk 10/10...

Raw nodes: 57 → After dedup: 51
Nodes extracted: 51
Edges extracted: 49

Sample nodes:
{'id': 'generative AI systems', 'description': 'AI systems that can generate content or data based on input and learned patterns.'}
{'id': 'AI engineering', 'description': 'The application of engineering principles to design and build effective AI systems.'}
{'id': 'production deployment', 'description': 'The process of implementing AI systems in a real-world environment for practical use.'}
{'id': 'model development', 'description': 'The creation and training of algorithms that enable AI systems to learn from data.'}
{'id': 'end-to-end AI system design', 'description': 'A comprehensive approach to designing AI systems from conception to operational use.'}

Sample edges:
{'source': 'AI engineering', 'target': 'generative AI systems', 'relationship': 'enables'}
{'source': 'AI engineering', 'target': 'production deployment', 'relationship': 'depends on'}
{'source': 'model development', 'target': 'end-to-end AI system design', 'relationship': 'is part of'}
{'source': 'production deployment', 'target': 'end-to-end AI system design', 'relationship': 'is part of'}
{'source': 'generative AI systems', 'target': 'AI engineering', 'relationship': 'requires'}
```