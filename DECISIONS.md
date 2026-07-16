# Architecture Decision Log

This document records the major architectural and design decisions made for the Finance Policy RAG Agent.

## Why Pinecone over ChromaDB / FAISS?
- **Serverless free tier:** No infrastructure to manage for a solo project.
- **Native Support:** Cosine similarity is natively supported, and dimension 768 matches `gemini-embedding-2`.
- **Tradeoff:** Vendor lock-in. For a larger production deployment, I would evaluate Weaviate or self-hosted Qdrant.

## Why word-based chunking (200 words / 30 overlap) vs sentence or paragraph?
- **Predictability:** Policy text often has irregular sentence lengths; word chunks are more predictable and ensure consistent vector sizes.
- **Context Preservation:** A 30-word overlap preserves context across chunk boundaries, preventing semantic loss at the edges.
- **Tradeoff:** It occasionally splits mid-sentence. Semantic chunking (e.g., via Langchain or custom regex by policy header) is an identified improvement (now implemented in the Python shadow layer).

## Why keyword-based uncertainty detection vs confidence score?
- **API Constraints:** The Gemini `generateContent` API does not expose logprobs or token probabilities in the free tier.
- **Speed to Market:** Keyword matching ("i don't know", "not covered") is fragile but ships fast. 
- **Evolution:** The next step (implemented in the Python shadow layer) is prompting Gemini to return a structured JSON object containing a `confidence` field (`high`, `medium`, `low`) for deterministic routing.

## Why Telegram vs a web UI?
- **Zero Frontend Infra:** Telegram is webhook-native, requiring no hosting of a frontend application.
- **User Adoption:** Finance team employees are already active on Telegram, ensuring immediate adoption without friction or a learning curve.
