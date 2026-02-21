# Book Knowledge Graph

## The Problem Statement

Most books contain hundreds of interconnected ideas, concepts, and relationships — but when you read linearly, your brain processes them as a *sequence*, not as a *network*. You finish a book and have a vague sense of the ideas but no clear map of how they connect.

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

## Why Is This Hard and Interesting?

Because none of those steps are trivial. The LLM has to *understand* the text well enough to extract meaningful concepts. The graph has to be structured so relationships have *weight and direction*. The layout algorithm has to place nodes so that *visually similar concepts cluster together*. And the whole thing has to work on *any* book, not just one.

