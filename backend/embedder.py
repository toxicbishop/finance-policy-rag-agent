import httpx
import os

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

async def embed(text: str) -> list[float]:
    """Generates embeddings using Gemini's embedding model."""
    if not GEMINI_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set")
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:embedContent?key={GEMINI_KEY}"
    payload = {
        "model": "models/gemini-embedding-2", 
        "content": {"parts": [{"text": text}]}
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        
    return response.json()["embedding"]["values"]
