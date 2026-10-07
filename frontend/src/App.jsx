import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askQuestion = async () => {
    if (!question.trim() || loading) {
      return;
    }

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const result = await axios.post(
        "http://127.0.0.1:8001/query",
        {
          question: question.trim(),
        },
      );

      setResponse(result.data);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to connect to MedQuery. Make sure the backend is running.",
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && event.ctrlKey) {
      askQuestion();
    }
  };

  return (
    <main className="app">
      <div className="container">
        <header className="header">
          <div className="brand">
            <div className="logo">M</div>
            <div>
              <h1>MedQuery</h1>
              <p>Grounded medical question answering</p>
            </div>
          </div>

          <div className="badge">
            <span className="badge-dot" />
            RAG-powered
          </div>
        </header>

        <section className="hero">
          <p className="eyebrow">MEDICAL KNOWLEDGE ASSISTANT</p>

          <h2>
            Ask a medical question.
            <br />
            Get an answer grounded in sources.
          </h2>

          <p className="hero-description">
            MedQuery retrieves relevant medical information, reranks the
            evidence, and generates an answer using the retrieved sources.
          </p>
        </section>

        <section className="query-card">
          <label htmlFor="question">Your question</label>

          <textarea
            id="question"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="e.g. What are the symptoms of diabetes?"
            rows={4}
            disabled={loading}
          />

          <div className="query-footer">
            <span>Ctrl + Enter to submit</span>

            <button
              onClick={askQuestion}
              disabled={loading || !question.trim()}
            >
              {loading ? "Analyzing..." : "Ask MedQuery →"}
            </button>
          </div>
        </section>

        {error && (
          <section className="error-card">
            <strong>Something went wrong</strong>
            <p>{error}</p>
          </section>
        )}

        {response && (
          <section className="results">
            <div className="results-header">
              <h2>Answer</h2>

              <span
                className={
                  response.status === "answered"
                    ? "status answered"
                    : "status abstained"
                }
              >
                {response.status === "answered"
                  ? "Evidence found"
                  : "Insufficient evidence"}
              </span>
            </div>

            <article className="answer-card">
              <ReactMarkdown>{response.answer}</ReactMarkdown>
            </article>

            {response.sources.length > 0 && (
              <section className="sources-section">
                <div className="sources-header">
                  <h2>Sources</h2>
                  <span>{response.sources.length} retrieved sources</span>
                </div>

                <div className="sources-grid">
                  {response.sources.map((source) => (
                    <article
                      className="source-card"
                      key={source.citation_id}
                    >
                      <div className="source-number">
                        [{source.citation_id}]
                      </div>

                      <div className="source-content">
                        <h3>{source.source_name || source.source}</h3>

                        {source.focus && <p>{source.focus}</p>}

                        {source.url && (
                          <a
                            href={source.url}
                            target="_blank"
                            rel="noreferrer"
                          >
                            View original source ↗
                          </a>
                        )}
                      </div>
                    </article>
                  ))}
                </div>
              </section>
            )}
          </section>
        )}

        {!response && !loading && !error && (
          <section className="examples">
            <p>Try asking:</p>

            <div className="example-list">
              <button
                onClick={() =>
                  setQuestion("What are the symptoms of diabetes?")
                }
              >
                What are the symptoms of diabetes?
              </button>

              <button
                onClick={() =>
                  setQuestion("What are the symptoms of high blood pressure?")
                }
              >
                What are the symptoms of high blood pressure?
              </button>

              <button
                onClick={() => setQuestion("What is the capital of France?")}
              >
                What is the capital of France?
              </button>
            </div>
          </section>
        )}

        <footer>
          <span>MedQuery</span>
          <span>•</span>
          <span>Grounded answers from medical sources</span>
        </footer>
      </div>
    </main>
  );
}

export default App;