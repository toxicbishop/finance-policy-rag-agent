from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.rag_chain import answer

app = FastAPI(title="Finance Policy RAG API")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    confidence: str
    cited_sections: list[str]

@app.post("/query", response_model=QueryResponse)
async def query_policy(request: QueryRequest):
    """Answers a finance policy question using RAG."""
    try:
        result = await answer(request.question)
        return QueryResponse(
            answer=result.get("answer", ""),
            confidence=result.get("confidence", "low"),
            cited_sections=result.get("cited_sections", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
