import { useRef, useState } from "react";
import api from "../lib/api";

export default function KnowledgeBase() {
  const fileRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [summarizing, setSummarizing] = useState(false);

  const [uploadMessage, setUploadMessage] = useState("");
  const [summary, setSummary] = useState("");
  const [jobId, setJobId] = useState("");
  const [error, setError] = useState("");

  function chooseFile(file) {
    if (!file) return;

    setSelectedFile(file);
    setUploadMessage("");
    setSummary("");
    setJobId("");
    setError("");
  }

  async function uploadDocument() {
    if (!selectedFile) {
      setError("Please select a document first.");
      return;
    }

    setUploading(true);
    setError("");
    setUploadMessage("");
    setJobId("");

    try {
      const result = await api.uploadDocument(selectedFile);

      setJobId(result?.job_id || "");

      setUploadMessage(
        `${selectedFile.name} uploaded successfully. Document processing has started.`
      );
    } catch (err) {
      console.error(err);
      setError(
        `Upload failed: ${err?.message || "Unknown error"}`
      );
    } finally {
      setUploading(false);
    }
  }

  async function summarizeDocument() {
    if (!selectedFile) {
      setError("Please select a document first.");
      return;
    }

    setSummarizing(true);
    setError("");
    setSummary("");

    try {
      const result = await api.uploadSummary(selectedFile);

      console.log("Summary response:", result);

      const finalSummary =
        result?.summary ||
        result?.answer ||
        result?.text ||
        result?.result?.summary ||
        result?.data?.summary ||
        "";

      if (!finalSummary) {
        throw new Error(
          "The summarizer did not return a summary."
        );
      }

      setSummary(finalSummary);
    } catch (err) {
      console.error(err);

      setError(
        `Summary failed: ${err?.message || "Unknown error"}`
      );
    } finally {
      setSummarizing(false);
    }
  }

  return (
    <div className="page-shell">

      {/* HEADER */}
      <div className="page-heading">

        <div className="eyebrow">
          ENTERPRISE DOCUMENT INTELLIGENCE
        </div>

        <h1>Knowledge Base</h1>

        <p>
          Upload, index and summarize enterprise documents
          using AI-powered document intelligence.
        </p>

      </div>


      {/* UPLOAD SECTION */}
      <section className="panel upload-panel">

        <div className="panel-header">

          <div>
            <div className="eyebrow">
              DOCUMENT MANAGEMENT
            </div>

            <h2>
              Upload Documents
            </h2>

            <p>
              Add company documents to the enterprise
              knowledge repository.
            </p>
          </div>

          <div className="upload-icon">
            ↑
          </div>

        </div>


        {/* DROP ZONE */}
        <div
          className="upload-zone"
          onClick={() => fileRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            chooseFile(e.dataTransfer.files?.[0]);
          }}
        >

          <div className="upload-cloud">
            ↑
          </div>

          <h3>
            Drop your document here
          </h3>

          <p>
            or click to browse from your computer
          </p>

          <span className="upload-types">
            PDF · DOCX · TXT · MD · CSV
          </span>

          <input
            ref={fileRef}
            type="file"
            hidden
            accept=".pdf,.docx,.txt,.md,.csv"
            onChange={(e) =>
              chooseFile(e.target.files?.[0])
            }
          />

        </div>


        {/* SELECTED FILE */}
        {selectedFile && (

          <div className="selected-file">

            <div>

              <strong>
                {selectedFile.name}
              </strong>

              <span>
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </span>

            </div>

            <button
              type="button"
              className="secondary-btn"
              onClick={() => {
                setSelectedFile(null);
                setSummary("");
                setUploadMessage("");
                setJobId("");
                setError("");
              }}
            >
              Remove
            </button>

          </div>

        )}


        {/* ACTIONS */}
        {selectedFile && (

          <div
            style={{
              display: "flex",
              gap: "12px",
              marginTop: "18px",
              flexWrap: "wrap"
            }}
          >

            <button
              type="button"
              className="primary-btn"
              onClick={uploadDocument}
              disabled={uploading}
            >
              {uploading
                ? "Uploading..."
                : "Upload & Index"}
            </button>


            <button
              type="button"
              className="secondary-btn"
              onClick={summarizeDocument}
              disabled={summarizing}
            >
              {summarizing
                ? "Generating Summary..."
                : "✨ Summarize Document"}
            </button>

          </div>

        )}


        {/* SUCCESS */}
        {uploadMessage && (

          <div className="status-success">
            ✓ {uploadMessage}
          </div>

        )}


        {/* JOB */}
        {jobId && (

          <div className="job-info">

            <strong>
              PROCESSING JOB
            </strong>

            <span>
              {jobId}
            </span>

          </div>

        )}


        {/* ERROR */}
        {error && (

          <div
            className="status-error"
            style={{ marginTop: "15px" }}
          >
            {error}
          </div>

        )}

      </section>


      {/* SUMMARY SECTION */}
      <section className="panel">

        <div className="panel-header">

          <div>

            <div className="eyebrow">
              AI DOCUMENT ANALYSIS
            </div>

            <h2>
              Document Summarizer
            </h2>

            <p>
              Generate a concise AI summary of the selected
              enterprise document.
            </p>

          </div>

          <div className="upload-icon">
            ✦
          </div>

        </div>


        {!summary && !summarizing && (

          <div
            style={{
              padding: "35px 20px",
              textAlign: "center",
              border: "1px dashed #30445d",
              borderRadius: "12px",
              background: "#091321"
            }}
          >

            <div
              style={{
                fontSize: "30px",
                marginBottom: "10px"
              }}
            >
              ✦
            </div>

            <h3 style={{ margin: "0 0 8px" }}>
              No summary generated
            </h3>

            <p
              style={{
                margin: 0,
                color: "#8197af"
              }}
            >
              Select a document above and click
              "Summarize Document".
            </p>

          </div>

        )}


        {summarizing && (

          <div
            style={{
              padding: "35px",
              textAlign: "center",
              border: "1px solid #263b54",
              borderRadius: "12px",
              background: "#091321"
            }}
          >

            <div
              style={{
                fontSize: "15px",
                color: "#69d9d5"
              }}
            >
              AI is analyzing the document...
            </div>

            <p
              style={{
                color: "#8197af",
                marginBottom: 0
              }}
            >
              Extracting key information and generating
              an enterprise summary.
            </p>

          </div>

        )}


        {summary && (

          <div>

            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                marginBottom: "14px"
              }}
            >

              <span className="status-badge">
                AI SUMMARY READY
              </span>

              {selectedFile && (
                <span
                  style={{
                    color: "#71869d",
                    fontSize: "13px"
                  }}
                >
                  {selectedFile.name}
                </span>
              )}

            </div>


            <div className="answer-text">
              {summary}
            </div>

          </div>

        )}

      </section>


      {/* WORKFLOW INFO */}
      <section className="panel">

        <div className="panel-header">

          <div>

            <div className="eyebrow">
              KNOWLEDGE WORKFLOW
            </div>

            <h2>
              Document Processing
            </h2>

          </div>

        </div>


        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "12px"
          }}
        >

          <div className="source-card">
            <strong>01 · Upload</strong>
            <p>
              Employee uploads an enterprise document.
            </p>
          </div>

          <div className="source-card">
            <strong>02 · Index</strong>
            <p>
              Document is processed and added to the
              searchable knowledge base.
            </p>
          </div>

          <div className="source-card">
            <strong>03 · Summarize</strong>
            <p>
              AI extracts the important information and
              creates a concise summary.
            </p>
          </div>

          <div className="source-card">
            <strong>04 · Investigate</strong>
            <p>
              Use the Investigation module to perform
              deeper AI research.
            </p>
          </div>

        </div>

      </section>

    </div>
  );
}
