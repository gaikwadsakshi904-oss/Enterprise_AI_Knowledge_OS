import { useState } from "react";
import api from "../lib/api";

export default function Investigation() {
  const [question, setQuestion] = useState(
    "What are the rules for responsible AI usage by employees?"
  );

  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askAI(e) {
    e.preventDefault();

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const employee =
        localStorage.getItem("eakos_name") ||
        localStorage.getItem("eakos_user") ||
        "Current Employee";

      /*
       * Investigation endpoint
       */
      const data = await api.investigate(
        question.trim(),
        employee
      );

      console.log("AI INVESTIGATION RESPONSE:", data);

      /*
       * Support the different response names used
       * by the backend.
       */
      const result = data?.result || data?.data || data;

      const finalAnswer =
        result?.answer ||
        result?.final_answer ||
        result?.finalAnswer ||
        result?.response ||
        result?.report ||
        result?.summary ||
        result?.message ||
        "";

      const finalSources =
        result?.sources ||
        result?.evidence ||
        result?.supporting_sources ||
        [];

      if (!finalAnswer) {
        setAnswer(
          "The AI completed the investigation but did not return an answer."
        );
      } else {
        setAnswer(
          typeof finalAnswer === "string"
            ? finalAnswer
            : JSON.stringify(finalAnswer, null, 2)
        );
      }

      setSources(
        Array.isArray(finalSources)
          ? finalSources
          : []
      );

    } catch (err) {
      console.error(err);
      setError(
        err?.message ||
        "Unable to get an answer from the AI."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        maxWidth: "1250px",
        margin: "0 auto",
        padding: "48px 44px 80px"
      }}
    >

      <div style={{ marginBottom: "30px" }}>

        <div
          style={{
            color: "#69d9d5",
            fontSize: "11px",
            fontWeight: "700",
            letterSpacing: "2px"
          }}
        >
          AI KNOWLEDGE ASSISTANT
        </div>

        <h1
          style={{
            color: "#edf5ff",
            fontSize: "34px",
            margin: "8px 0"
          }}
        >
          Enterprise Document Investigation
        </h1>

        <p style={{ color: "#8fa4bd" }}>
          Ask questions and get grounded answers from
          company documents and policies.
        </p>

      </div>


      {/* QUESTION */}
      <section
        style={{
          background: "#111c2d",
          border: "1px solid #263b54",
          borderRadius: "16px",
          padding: "28px",
          marginBottom: "20px"
        }}
      >

        <div
          style={{
            color: "#69a9dc",
            fontSize: "11px",
            fontWeight: "700",
            letterSpacing: "2px",
            marginBottom: "10px"
          }}
        >
          ASK YOUR QUESTION
        </div>

        <h2
          style={{
            color: "#e8f2ff",
            fontSize: "19px"
          }}
        >
          What would you like to know?
        </h2>

        <form onSubmit={askAI}>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about your enterprise documents..."
            rows={6}
            style={{
              width: "100%",
              boxSizing: "border-box",
              padding: "18px",
              background: "#07111f",
              color: "#e8f2ff",
              border: "1px solid #30445d",
              borderRadius: "10px",
              fontSize: "15px",
              fontFamily: "inherit",
              resize: "vertical"
            }}
          />

          <div
            style={{
              display: "flex",
              justifyContent: "flex-end",
              marginTop: "14px"
            }}
          >

            <button
              type="submit"
              disabled={loading}
              style={{
                border: "none",
                borderRadius: "10px",
                padding: "13px 25px",
                background: "#61d8d5",
                color: "#06121e",
                fontWeight: "800",
                cursor: loading ? "wait" : "pointer"
              }}
            >
              {loading ? "Thinking..." : "Ask AI →"}
            </button>

          </div>

        </form>

        {error && (
          <div
            style={{
              marginTop: "15px",
              padding: "12px",
              borderRadius: "8px",
              background: "#35161b",
              color: "#f0a4b0"
            }}
          >
            {error}
          </div>
        )}

      </section>


      {/* ANSWER */}
      <section
        style={{
          background: "#111c2d",
          border: "1px solid #263b54",
          borderRadius: "16px",
          padding: "28px",
          marginBottom: "20px"
        }}
      >

        <div
          style={{
            color: "#69d9d5",
            fontSize: "11px",
            fontWeight: "700",
            letterSpacing: "2px"
          }}
        >
          AI ANSWER
        </div>

        <h2
          style={{
            color: "#e8f2ff",
            marginBottom: "18px"
          }}
        >
          Answer
        </h2>

        {loading ? (

          <div
            style={{
              padding: "25px",
              background: "#091321",
              borderRadius: "10px",
              color: "#69d9d5"
            }}
          >
            AI is searching the enterprise knowledge base...
          </div>

        ) : answer ? (

          <div
            style={{
              padding: "22px",
              background: "#091321",
              border: "1px solid #263b54",
              borderRadius: "10px",
              color: "#dceafa",
              fontSize: "16px",
              lineHeight: "1.8",
              whiteSpace: "pre-wrap"
            }}
          >
            {answer}
          </div>

        ) : (

          <div
            style={{
              padding: "22px",
              background: "#091321",
              borderRadius: "10px",
              color: "#71869d"
            }}
          >
            Ask a question to get an AI answer.
          </div>

        )}

      </section>


      {/* SOURCES */}
      {sources.length > 0 && (

        <section
          style={{
            background: "#111c2d",
            border: "1px solid #263b54",
            borderRadius: "16px",
            padding: "28px"
          }}
        >

          <div
            style={{
              color: "#69d9d5",
              fontSize: "11px",
              fontWeight: "700",
              letterSpacing: "2px"
            }}
          >
            EVIDENCE
          </div>

          <h2 style={{ color: "#e8f2ff" }}>
            Supporting Sources
          </h2>

          {sources.map((source, index) => {

            const text =
              typeof source === "string"
                ? source
                : source?.filename ||
                  source?.source ||
                  source?.file ||
                  JSON.stringify(source);

            return (
              <div
                key={index}
                style={{
                  padding: "14px",
                  marginTop: "10px",
                  background: "#091321",
                  border: "1px solid #263b54",
                  borderRadius: "9px",
                  color: "#cbd9e8"
                }}
              >
                {text}
              </div>
            );

          })}

        </section>

      )}

    </div>
  );
}
