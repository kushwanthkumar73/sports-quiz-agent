# 🏆 AI-Powered Sports Quiz Generation Agent

A Retrieval-Augmented Generation (RAG) web app that generates **factually grounded**
sports quizzes by combining a local vector knowledge base with live web search,
then handing verified context to an LLM to eliminate hallucinated facts.

🔗 **Live Demo:** [sports-quiz-agent.onrender.com](https://sports-quiz-agent.onrender.com)

---

## Overview

Standard LLMs can confidently make up sports stats and records. This project solves
that with a RAG pipeline: instead of asking the model to "remember" facts, it's
handed real, retrieved facts and instructed to build the quiz *only* from them.

**Two sources of grounding context:**
- 📚 **ChromaDB** — a local vector database of historic sports facts (World Cups, Grand Slams, records)
- 🌐 **DuckDuckGo Search** — live web results for recent tournament news and results

The LLM (Google Gemini) merges both into a structured, multiple-choice quiz with
answers and explanations sourced directly from the retrieved context.

## Architecture

```
User selects Sport + Difficulty
            │
            ▼
   ┌─────────────────────┐
   │   Streamlit UI       │  app.py
   └─────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │  RAG Orchestration (src/generator.py)     │
   │                                            │
   │  ChromaDB query ──► historic facts         │
   │  DuckDuckGo query ──► live news snippets   │
   │                                            │
   │  Merged context ──► Gemini prompt          │
   └─────────────────────────────────────────┘
            │
            ▼
   4 MCQs + answers + explanations, rendered in UI
```

## Tech Stack

| Layer            | Technology                          |
|-------------------|--------------------------------------|
| UI                | Streamlit                            |
| Vector store      | ChromaDB (persistent, local)         |
| Embeddings        | sentence-transformers (default)      |
| Live search       | duckduckgo-search                    |
| LLM               | Google Gemini (`gemini-2.5-flash`)   |
| Deployment        | Render                               |

## Project Structure

```
sports-quiz-agent/
├── app.py                # Streamlit UI — entry point
├── requirements.txt
├── data/
│   └── sports_facts.json # Offline knowledge base (raw facts)
├── chroma_db/             # Auto-created persistent vector store
└── src/
    ├── config.py          # Environment variable loading
    ├── database.py        # ChromaDB setup, ingestion, and querying
    ├── search.py           # Live web search via DuckDuckGo
    └── generator.py        # RAG orchestration + Gemini call
```

## Running Locally

```bash
git clone https://github.com/kushwanthkumar73/sports-quiz-agent.git
cd sports-quiz-agent
python -m venv venv
venv\Scripts\activate        # source venv/bin/activate on Mac/Linux
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_key_here
```

Run:

```bash
streamlit run app.py
```

## Key Design Decisions

- **Grounded generation over free generation** — the system prompt explicitly
  restricts the LLM to facts present in the retrieved context, reducing hallucination
  risk for niche sports statistics.
- **Metadata-filtered vector search** — ChromaDB queries are filtered by `sport`,
  so retrieval stays relevant even as the knowledge base grows.
- **Zero-cost embeddings** — uses ChromaDB's built-in sentence-transformers
  embedding function locally, avoiding a paid embeddings API.
- **Graceful degradation** — if live web search fails (rate limits, connectivity),
  the app falls back to offline facts only rather than crashing.

## Future Improvements

- Score tracking and a leaderboard across quiz attempts
- Expand the offline knowledge base to more sports
- Cache live search results to reduce redundant API calls
