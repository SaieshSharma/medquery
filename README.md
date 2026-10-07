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
```

---

## Tech Stack

### Backend
- Python 3.12+
- `uv` for Python project and dependency management
- FastAPI
- Uvicorn
- Sentence Transformers
- Qdrant
- Cross-Encoder
- Groq API
- Pydantic / Pydantic Settings

### Frontend
- React
- Vite
- Axios
- React Markdown

### Infrastructure
- Docker
- Docker Compose
- Qdrant

### Dataset
- MedQuAD (The current MVP uses usable question-answer pairs from MedQuAD)

---

## Project Structure

```text
medquery/
│
├── data/
│   ├── raw/
│   │   └── MedQuAD/
│   ├── processed/
│   └── evaluation/
│
├── docker/
│   └── qdrant/
│       └── docker-compose.yml
│
├── experiments/
├── notebooks/
│
├── scripts/
│   ├── healthcheck.py
│   ├── test_medquad.py
│   ├── embedding_demo.py
│   ├── similarity_demo.py
│   ├── qdrant_demo.py
│   ├── batch_qdrant_demo.py
│   ├── retrieval_demo.py
│   ├── reranker_demo.py
│   ├── ingest_medquad.py
│   ├── groq_demo.py
│   ├── rag_demo.py
│   ├── guardrail_demo.py
│   └── evaluate_guardrail.py
│
├── src/
│   └── medquery/
│       ├── api/
│       ├── config/
│       ├── embeddings/
│       ├── generation/
│       ├── guardrails/
│       ├── ingestion/
│       ├── pipeline/
│       ├── retrieval/
│       └── schemas/
│
├── tests/
│   ├── integration/
│   └── unit/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Prerequisites

Install the following on your machine:

- Git
- Python 3.12+
- uv
- Docker Desktop
- Node.js 18+
- npm
- A Groq API key

*Note: Make sure Docker Desktop is running before starting Qdrant.*

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY>
cd medquery
```

### 2. Set Up the Python Environment

This project uses `uv`. From the project root:

```bash
uv sync
```

This creates the project environment and installs the dependencies defined in `pyproject.toml`. You can verify your Python version:

```bash
uv run python --version
```

### 3. Configure Environment Variables

Copy the example environment file:

**Git Bash / Linux / macOS:**
```bash
cp .env.example .env
```

**Windows PowerShell:**
```powershell
Copy-Item .env.example .env
```

Open `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

> **Important:** Do not commit `.env`. The `.env` file contains secrets and is intentionally ignored by Git.

### 4. Add the MedQuAD Dataset

The dataset is not included in this repository because the raw dataset is excluded from Git. Download the MedQuAD dataset from the official MedQuAD repository and place it in:

```text
data/raw/MedQuAD/
```

The expected structure is approximately:

```text
data/
└── raw/
    └── MedQuAD/
        ├── 1_CancerGov_QA/
        ├── 2_GARD_QA/
        ├── 3_GHR_QA/
        ├── ...
        └── 12_MPlusHerbsSupplements_QA/
```

Verify that the dataset is readable:

```bash
uv run python scripts/test_medquad.py
```

*The ingestion pipeline filters out QA pairs that do not contain answers.*

### 5. Start Qdrant

Qdrant runs locally using Docker Compose. From the project root:

```bash
docker compose -f docker/qdrant/docker-compose.yml up -d
```

Check that the container is running:

```bash
docker ps
```

You can also check the health endpoint:

```bash
curl http://localhost:6333/healthz
```

Expected response:
```text
healthz check passed
```

### 6. Ingest MedQuAD into Qdrant

Before using the RAG pipeline on a fresh machine, the MedQuAD documents must be embedded and stored in Qdrant:

```bash
uv run python scripts/ingest_medquad.py
```

**Ingestion flow:**
```text
MedQuAD XML
     │
     ▼
Document loading
     │
     ▼
Usable QA filtering
     │
     ▼
Chunking
     │
     ▼
Sentence Transformer embeddings
     │
     ▼
Qdrant
```

Configuration details:
- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Embedding dimension:** `384`
- **Distance:** Cosine similarity

*The ingestion process may take some time because the embedding model needs to process the dataset. After ingestion, Qdrant contains the MedQuAD vectors and source metadata.*

### 7. Start the Backend

Open a terminal in the project root and run:

```bash
uv run uvicorn medquery.api.app:app --reload --port 8001
```

The API will be available at `http://127.0.0.1:8001`.

Check the health status at `http://127.0.0.1:8001/health`:
```json
{
  "status": "ok"
}
```

### 8. Test the API

FastAPI provides interactive API documentation at:
```text
http://127.0.0.1:8001/docs
```

Find the `POST /query` endpoint.

**Example request:**
```json
{
  "question": "What are the symptoms of diabetes?"
}
```

**Example response:**
```json
{
  "answer": "...",
  "status": "answered",
  "sources": [
    {
      "citation_id": 1,
      "document_id": "0000015-15",
      "source": "medquad",
      "source_name": "NIHSeniorHealth",
      "focus": "Diabetes",
      "url": "..."
    }
  ]
}
```

### 9. Start the Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally be available at `http://localhost:5173`. Open that address in your browser.

### 10. Run the Complete Application

To run the whole system locally, keep these three processes running:

- **Terminal 1 — Qdrant:**
  ```bash
  docker compose -f docker/qdrant/docker-compose.yml up -d
  ```
- **Terminal 2 — FastAPI:**
  ```bash
  uv run uvicorn medquery.api.app:app --reload --port 8001
  ```
- **Terminal 3 — React:**
  ```bash
  cd frontend
  npm run dev
  ```

Open `http://localhost:5173` in your browser.

---

## Demo Questions

### Medical question
> *"What are the symptoms of diabetes?"*

**Expected:** `status: answered`  
The response should contain an answer along with retrieved sources.

### Another medical question
> *"What are the symptoms of high blood pressure?"*

**Expected:** `status: answered`

### Out-of-domain question
> *"What is the capital of France?"*

**Expected:** `status: abstained`  
The system responds that it does not have enough relevant medical information rather than hallucinating an answer. This demonstrates the retrieval relevance guardrail.

---

## How the RAG Pipeline Works

When a user submits a question:

1. **Query embedding:** The question is converted into a vector using `all-MiniLM-L6-v2`.
2. **Dense retrieval:** The query vector is sent to Qdrant, retrieving the top $K = 10$ most semantically similar medical passages.
3. **Relevance guardrail:** The retrieved scores are checked. If the evidence is insufficient:
   ```text
   Retrieve ──► Insufficient evidence ──► Abstain
   ```
   The LLM is not called.
4. **Cross-encoder reranking:** If sufficient evidence is found, retrieved candidates are reranked using `cross-encoder/ms-marco-MiniLM-L-6-v2` for more precise ordering.
5. **Generation:** Top retrieved passages are provided as context to the Groq LLM with instructions to answer strictly using the retrieved evidence.
6. **Citation validation:** The generated answer is checked for citation IDs (e.g., `Frequent urination can be a symptom of diabetes. [1]`). The system verifies that citation `[1]` corresponds to an actual retrieved source.

---

## Testing & Quality

Run all Python tests:
```bash
uv run pytest
```

Run linting:
```bash
uv run ruff check .
```

Both should pass before committing changes.

---

## Useful Development Commands

```bash
# Run Python scripts in project environment
uv run python scripts/retrieval_demo.py

# Add a Python dependency
uv add <package>

# Synchronize dependencies
uv sync

# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Fix Ruff issues automatically
uv run ruff check . --fix
```

---

## Troubleshooting

- **Qdrant is not running:**  
  Check `docker ps`. If the container is absent, run:
  ```bash
  docker compose -f docker/qdrant/docker-compose.yml up -d
  ```
- **Port 8000 is unavailable:**  
  The project is preconfigured to use port `8001`. Start FastAPI with:
  ```bash
  uv run uvicorn medquery.api.app:app --reload --port 8001
  ```
  Ensure the frontend is targeting `http://127.0.0.1:8001`.
- **Groq API errors:**  
  Confirm `.env` exists and contains your valid key:
  ```bash
  ls -la .env
  ```
- **Dataset not found:**  
  Confirm `data/raw/MedQuAD` exists and contains the unzipped MedQuAD XML files.
- **Frontend cannot connect to backend:**  
  Ensure both servers are running. Check `http://127.0.0.1:8001/health` and review browser console logs for CORS or network issues.

---

## Current Limitations

The current version is an MVP focused on demonstrating the end-to-end RAG pipeline:
- MedQuAD is currently the primary indexed corpus.
- Retrieval is dense-only; hybrid BM25 + dense retrieval is not yet implemented.
- Claim-level citation entailment is not fully verified.
- PubMed ingestion is planned but not part of the current MVP.
- Relevance thresholds were tuned experimentally.
- The API uses a local development configuration.
- Groq is currently the sole generation provider.

---

## Planned Improvements

```text
MedQuAD + PubMed abstracts
           │
           ▼
Hybrid Dense + BM25 Retrieval
           │
           ▼
Cross-Encoder Reranking
           │
           ▼
Grounded Generation
           │
           ▼
Claim-level Citation Verification
           │
           ▼
RAGAS Evaluation
           │
           ▼
Observability / Tracing
```

- PubMed ingestion through NCBI E-utilities
- Hybrid retrieval
- Better semantic chunking
- RAGAS evaluation
- Claim-level citation verification
- More robust medical-domain guardrails
- Local Ollama fallback
- Production deployment configuration
- Observability and request tracing

---

## Important Note

**MedQuery is a research and academic project demonstrating retrieval-grounded medical question answering.**

It is not a replacement for a qualified medical professional and should not be used for diagnosis or treatment decisions. The system is designed to demonstrate how retrieval, reranking, source provenance, and guarded generation can be combined to reduce unsupported LLM responses.

---

## Development Workflow

Before committing changes:
```bash
uv run pytest
uv run ruff check .
git status
git diff
```

Commit format conventions:
```bash
git add <files>
git commit -m "type: description"
git push
```

Common commit types:
- `feat:` add new functionality
- `fix:` correct a bug
- `refactor:` improve code structure
- `test:` add or update tests
- `docs:` update documentation
- `chore:` maintenance