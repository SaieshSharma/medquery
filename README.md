# MedQuery

### Retrieval-Augmented Generation for Grounded Medical Question Answering

MedQuery is a Retrieval-Augmented Generation (RAG) system designed to answer medical questions using retrieved evidence from trusted medical sources.

Instead of relying solely on the knowledge stored inside a Large Language Model (LLM), MedQuery first retrieves relevant medical information from a vector database and provides that evidence to the LLM during answer generation.

The system also includes:

- Semantic vector retrieval using Sentence Transformers
- Qdrant vector database
- Cross-encoder reranking
- Retrieval relevance guardrails
- Groq LLM generation
- Citation/provenance tracking
- Citation ID validation
- Abstention when sufficient medical evidence is not available
- FastAPI backend
- React frontend

---

## Architecture

```text
                         User
                          │
                          ▼
                  React Frontend
                  localhost:5173
                          │
                     POST /query
                          │
                          ▼
                     FastAPI
                  localhost:8001
                          │
                          ▼
                    RAG Pipeline
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
        Dense Retrieval          Guardrail
              │
              ▼
           Qdrant
              │
              ▼
       Top-K Candidates
              │
              ▼
     Cross-Encoder Reranker
              │
              ▼
        Top Relevant
         Passages
              │
              ▼
          Groq LLM
              │
              ▼
      Citation Validation
              │
        ┌─────┴─────┐
        │           │
        ▼           ▼
     Answer      Abstain
        │
        ▼
   Answer + Sources