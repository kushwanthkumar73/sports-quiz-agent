from google import genai
from src.config import GEMINI_API_KEY
from src.database import query_historic_facts
from src.search import get_live_news_context

MODEL_NAME = "gemini-2.5-flash"


def compile_quiz_data(sport, difficulty):
    """
    1. Gathers context from ChromaDB (historical facts).
    2. Gathers context from DuckDuckGo (live news).
    3. Blends them inside a grounded prompt.
    4. Sends the prompt to Gemini and returns the generated quiz text.
    """
    db_query = f"{sport} history cup championships rules records"
    db_matches = query_historic_facts(sport=sport, query_text=db_query, n_results=2)
    db_context = "\n".join(db_matches) if db_matches else "No offline historic data recorded."

    web_context = get_live_news_context(sport)

    unified_context = (
        f"=== HISTORICAL FACTS ===\n{db_context}\n\n"
        f"=== LIVE INTERNET NEWS ===\n{web_context}"
    )

    client = genai.Client(api_key=GEMINI_API_KEY)

    system_instruction = (
        "You are an expert sports quiz creator. Write multiple-choice quizzes relying "
        "strictly on the provided context. Avoid hallucinations. Do not use facts not "
        "found in the context below. If facts are scarce, make do with what you have, "
        "but keep every detail accurate to the context.\n\n"
        f"CONTEXT DETAILS:\n{unified_context}"
    )

    user_prompt = (
        f"Generate exactly 3 unique multiple-choice questions for the sport: {sport}.\n"
        f"Difficulty target: {difficulty}.\n\n"
        "Format each question exactly as follows so my program can parse it:\n"
        "Question: [Question text here]\n"
        "A) [Option A]\n"
        "B) [Option B]\n"
        "C) [Option C]\n"
        "D) [Option D]\n"
        "Correct Answer: [Single Letter, e.g., A]\n"
        "Explanation: [Detailed reasoning based on the context]\n"
        "---"
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config={
            "system_instruction": system_instruction,
            "temperature": 0.7,
        },
    )

    return response.text, unified_context
