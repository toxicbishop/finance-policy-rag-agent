import httpx
import os
from backend.embedder import embed

PINECONE_HOST = os.environ.get("PINECONE_HOST")
PINECONE_KEY = os.environ.get("PINECONE_API_KEY")

async def retrieve(question: str, top_k: int = 5) -> list[dict]:
    """Retrieves relevant policy chunks from Pinecone based on the question."""
    if not PINECONE_HOST or not PINECONE_KEY:
        raise ValueError("PINECONE_HOST or PINECONE_API_KEY environment variables not set")
        
    # Generate embedding for the question
    vec = await embed(question)
    
    url = f"{PINECONE_HOST}/query"
    headers = {
        "Api-Key": PINECONE_KEY, 
        "Content-Type": "application/json"
    }
    payload = {
        "vector": vec, 
        "topK": top_k, 
        "includeMetadata": True
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
    return response.json().get("matches", [])
