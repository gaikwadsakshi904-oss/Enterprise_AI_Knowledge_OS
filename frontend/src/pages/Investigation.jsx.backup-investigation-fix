import { useState } from "react";
import api from "../lib/api";

const DEFAULT_QUESTION =
  "What are the rules for responsible AI usage by employees?";

export default function Investigation() {
  const [question, setQuestion] = useState(DEFAULT_QUESTION);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function askAI() {
    if (!question.trim()) return;

    setLoading(true);
    setError("");

    try {
      const data = await api.ask(question);
      setResult(data);
      localStorage.setItem("eakos_latest_answer", JSON.stringify(data));
    } catch (e) {
      setError(e?.message || "Unable to get AI response.");
    } finally {
      setLoading(false);
    }
  }

  const sources = result?.sources || [];
  const confidence = result?.confidence || {};

  return (
    <>
      <div className="intro">
        <div>
          <small>AI KNOWLEDGE ASSISTANT</small>
          <h2>Enterprise Document Investigation</h2>
          <p>
            Ask questions and get grounded answers from company documents,
            policies and knowledge-base evidence.
          </p>
        </div>
      </div>

      <div className="panel query">
        <small>ASK YOUR QUESTION</small>

        <h3>What would you like to know?</h3>

        <textarea
          rows="5"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about a company policy..."
        />

        <div className="query-foot">
          <span>
            Answers are grounded in the enterprise knowledge base.
          </span>

          <button
            className="btn"
            onClick={askAI}
            disabled={loading}
          >
            {loading ? "Thinking..." : "Ask AI →"}
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {result && (
        <>
          <div className="panel">
            <small>AI ANSWER</small>

            <h3>Knowledge-based response</h3>

            <div
              className="ai-answer"
              style={{
                whiteSpace: "pre-wrap",
                lineHeight: 1.7,
                marginTop: "15px"
              }}
            >
              {result.answer || "No answer returned."}
            </div>
          </div>

          <div className="metrics mini">
            <div className="metric">
              <strong>{sources.length}</strong>
              <span>Sources</span>
            </div>

            <div className="metric">
              <strong>
                {confidence.percentage ?? 0}%
              </strong>
              <span>Confidence</span>
            </div>

            <div className="metric">
              <strong>
                {confidence.level || "N/A"}
              </strong>
              <span>Evidence level</span>
            </div>
          </div>

          <div className="panel">
            <small>DOCUMENT EVIDENCE</small>

            <h3>
              Retrieved sources {sources.length}
            </h3>

            {sources.length === 0 ? (
              <p>No document sources returned.</p>
            ) : (
              sources.map((source, index) => (
                <div className="finding" key={index}>
                  <small>SOURCE {index + 1}</small>

                  <b>{source.document}</b>

                  <span>
                    {source.page
                      ? `Page ${source.page} • `
                      : ""}
                    Relevance:{" "}
                    {source.score
                      ? Number(source.score).toFixed(3)
                      : "N/A"}
                  </span>
                </div>
              ))
            )}
          </div>

          <div className="panel">
            <small>EVIDENCE CONFIDENCE</small>

            <h3>
              {confidence.percentage ?? 0}% —{" "}
              {confidence.level || "UNKNOWN"}
            </h3>

            <p>
              {confidence.reason ||
                "Evidence retrieved from the enterprise knowledge base."}
            </p>

            <p>
              Grounded:{" "}
              <strong>
                {confidence.grounded ? "YES ✓" : "NO"}
              </strong>
            </p>
          </div>
        </>
      )}
    </>
  );
}
