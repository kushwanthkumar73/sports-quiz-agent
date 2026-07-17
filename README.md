# 🏆 AI-Powered Sports Quiz Generation Agent

A Retrieval-Augmented Generation (RAG) web app that generates factually grounded
sports quizzes by combining:

- **ChromaDB** (local vector store of historic sports facts)
- **DuckDuckGo Search** (live web context for recent events)
- **Google Gemini** (LLM that writes the quiz using only retrieved context)

Built with Streamlit.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file:

```
GEMINI_API_KEY=your_key_here
```

Run:

```bash
streamlit run app.py
```

## How it works

1. **Offline knowledge base** — `data/sports_facts.json` is embedded and stored in
   `ChromaDB` (`src/database.py`) on first run.
2. **Live web search** — `src/search.py` queries DuckDuckGo for recent news on the
   selected sport.
3. **RAG orchestration** — `src/generator.py` merges both context sources into a
   single grounded prompt and calls Gemini to produce the quiz, instructed to avoid
   hallucinating facts outside the given context.
4. **UI** — `app.py` renders sport/difficulty selectors, the generated quiz, and an
   expandable "ground truth" panel showing exactly what context was used.

## Project structure

```
sports-quiz-agent/
├── app.py
├── requirements.txt
├── data/sports_facts.json
├── chroma_db/        (auto-created)
└── src/
    ├── config.py
    ├── database.py
    ├── search.py
    └── generator.py
```

## Notes

- Uses Gemini (`gemini-2.5-flash`) via the `google-genai` SDK — swap in another
  provider by editing `src/generator.py`.
- ChromaDB's default embedding function (sentence-transformers) runs locally, so no
  extra API key is needed for embeddings.
