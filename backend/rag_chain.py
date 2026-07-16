import httpx
import os
import json
from backend.retriever import retrieve

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

async def answer(question: str) -> dict:
    """Retrieves context and generates an answer using Gemini with structured JSON output."""
    if not GEMINI_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set")
        
    matches = await retrieve(question)
    
    # Build context with sections and chunk IDs if available
    context_chunks = []
    for m in matches:
        meta = m.get("metadata", {})
        section = meta.get("section", "Policy")
        chunk_id = meta.get("chunkId", "N/A")
        text = meta.get("text", "")
        context_chunks.append(f"[{section}, chunk {chunk_id}]\n{text}")
        
    context = "\n\n".join(context_chunks)
    
    prompt = f"""You are a Finance Policy Assistant. Answer using ONLY the context below.
Respond in exact JSON format:
{{
    "answer": "your answer here",
    "confidence": "high" | "medium" | "low",
    "cited_sections": ["section name 1", "section name 2"]
}}

CONTEXT:
{context}

QUESTION: {question}"""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        
    raw_response = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    
    # Clean and parse JSON response
    cleaned = raw_response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
        
    return json.loads(cleaned.strip())
