import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def build_prompt(query, contexts):

    context_block = "\n\n".join(
        [f"[{c['doc']} - page {c['page']}] {c['text']}" for c in contexts]
    )

    return f"""
You are an RAG assistant. Use ONLY the context to answer.
If not found in context, say “Not found in the provided documents.”

Context:
{context_block}

User question:
{query}

Include citations like (doc/page).
"""

async def generate_answer(query, contexts, model):

    prompt = build_prompt(query, contexts)

    llm = genai.GenerativeModel(model)

    try:
        response = llm.generate_content(prompt)
        answer_text = response.text or "No answer generated."
    except Exception as e:
        answer_text = f"LLM Error: {str(e)}"

    return {
        "answer": answer_text,
        "sources": contexts
    }
