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