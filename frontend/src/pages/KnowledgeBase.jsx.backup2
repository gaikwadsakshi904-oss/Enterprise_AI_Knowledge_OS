import { useState } from "react";
import api from "../lib/api";

export default function KnowledgeBase() {
    const [mode, setMode] = useState("summarize");
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");

    const handleFile = (e) => {
        const selected = e.target.files?.[0];

        if (!selected) return;

        setFile(selected);
        setResult(null);
        setError("");
    };

    const handleProcess = async () => {
        if (!file) {
            setError("Please select a document first.");
            return;
        }

        setLoading(true);
        setError("");
        setResult(null);

        try {
            let response;

            if (mode === "summarize") {
                response = await api.uploadSummary(file);
            } else {
                response = await api.uploadDocument(file);
            }

            setResult(response);
        } catch (err) {
            setError(err.message || "Something went wrong.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={styles.page}>

            <div style={styles.header}>
                <div>
                    <div style={styles.eyebrow}>ENTERPRISE AI KNOWLEDGE OS</div>

                    <h1 style={styles.title}>
                        Document Workspace
                    </h1>

                    <p style={styles.subtitle}>
                        Upload documents, generate AI summaries, and add
                        enterprise knowledge to your workspace.
                    </p>
                </div>

                <div style={styles.status}>
                    <span style={styles.statusDot}></span>
                    AI SYSTEM ONLINE
                </div>
            </div>

            <div style={styles.tabs}>
                <button
                    onClick={() => {
                        setMode("summarize");
                        setResult(null);
                        setError("");
                    }}
                    style={{
                        ...styles.tab,
                        ...(mode === "summarize" ? styles.activeTab : {})
                    }}
                >
                    ✨ Summarize Document
                </button>

                <button
                    onClick={() => {
                        setMode("knowledge");
                        setResult(null);
                        setError("");
                    }}
                    style={{
                        ...styles.tab,
                        ...(mode === "knowledge" ? styles.activeTab : {})
                    }}
                >
                    📚 Add to Knowledge Base
                </button>
            </div>

            <div style={styles.grid}>

                <div style={styles.card}>

                    <div style={styles.cardHeader}>
                        <div>
                            <div style={styles.cardLabel}>
                                {mode === "summarize"
                                    ? "AI DOCUMENT SUMMARY"
                                    : "KNOWLEDGE INGESTION"}
                            </div>

                            <h2 style={styles.cardTitle}>
                                {mode === "summarize"
                                    ? "Analyze a document"
                                    : "Add enterprise knowledge"}
                            </h2>
                        </div>

                        <div style={styles.iconBox}>
                            {mode === "summarize" ? "✦" : "◈"}
                        </div>
                    </div>

                    <label style={styles.dropzone}>
                        <input
                            type="file"
                            accept=".pdf,.txt,.doc,.docx"
                            onChange={handleFile}
                            style={{ display: "none" }}
                        />

                        <div style={styles.uploadIcon}>
                            ↑
                        </div>

                        <div style={styles.uploadTitle}>
                            {file
                                ? file.name
                                : "Drop your document here"}
                        </div>

                        <div style={styles.uploadText}>
                            {file
                                ? `${(file.size / 1024 / 1024).toFixed(2)} MB`
                                : "or click to browse from your computer"}
                        </div>

                        <div style={styles.formats}>
                            PDF · DOC · DOCX · TXT
                        </div>
                    </label>

                    {file && (
                        <div style={styles.fileRow}>
                            <div>
                                <div style={styles.fileName}>
                                    {file.name}
                                </div>

                                <div style={styles.fileMeta}>
                                    {(file.size / 1024 / 1024).toFixed(2)} MB
                                </div>
                            </div>

                            <button
                                onClick={() => {
                                    setFile(null);
                                    setResult(null);
                                }}
                                style={styles.remove}
                            >
                                Remove
                            </button>
                        </div>
                    )}

                    {error && (
                        <div style={styles.error}>
                            {error}
                        </div>
                    )}

                    <button
                        onClick={handleProcess}
                        disabled={loading}
                        style={{
                            ...styles.primaryButton,
                            opacity: loading ? 0.6 : 1
                        }}
                    >
                        {loading
                            ? "AI IS PROCESSING..."
                            : mode === "summarize"
                                ? "Generate AI Summary →"
                                : "Add Document to Knowledge Base →"}
                    </button>

                    <div style={styles.note}>
                        🔒 Your document is processed through the Enterprise
                        AI pipeline.
                    </div>
                </div>

                <div style={styles.card}>

                    <div style={styles.cardLabel}>
                        AI OUTPUT
                    </div>

                    <h2 style={styles.cardTitle}>
                        {result
                            ? "Document Intelligence"
                            : "Your results will appear here"}
                    </h2>

                    {!result && !loading && (
                        <div style={styles.empty}>
                            <div style={styles.emptyIcon}>✦</div>

                            <p style={styles.emptyTitle}>
                                Ready for analysis
                            </p>

                            <p style={styles.emptyText}>
                                Upload a document on the left and let the
                                AI Knowledge OS analyze it.
                            </p>

                            <div style={styles.features}>
                                <div>✓ Document understanding</div>
                                <div>✓ AI-generated summary</div>
                                <div>✓ Knowledge extraction</div>
                                <div>✓ Enterprise retrieval</div>
                            </div>
                        </div>
                    )}

                    {loading && (
                        <div style={styles.loadingBox}>
                            <div style={styles.spinner}>◌</div>

                            <div style={styles.loadingTitle}>
                                Analyzing document...
                            </div>

                            <div style={styles.loadingText}>
                                Extracting content and generating
                                enterprise intelligence.
                            </div>
                        </div>
                    )}

                    {result && (
                        <div>

                            <div style={styles.success}>
                                <span>✓</span>
                                Document processed successfully
                            </div>

                            {result.filename && (
                                <div style={styles.resultFile}>
                                    📄 {result.filename}
                                </div>
                            )}

                            {result.characters && (
                                <div style={styles.stats}>
                                    <div style={styles.stat}>
                                        <strong>
                                            {result.characters}
                                        </strong>
                                        <span>Characters</span>
                                    </div>

                                    <div style={styles.stat}>
                                        <strong>
                                            AI
                                        </strong>
                                        <span>Analysis</span>
                                    </div>

                                    <div style={styles.stat}>
                                        <strong>
                                            ✓
                                        </strong>
                                        <span>Processed</span>
                                    </div>
                                </div>
                            )}

                            {result.summary && (
                                <div style={styles.summary}>
                                    <div style={styles.summaryTitle}>
                                        AI SUMMARY
                                    </div>

                                    <div style={styles.summaryText}>
                                        {result.summary}
                                    </div>
                                </div>
                            )}

                            {result.status && (
                                <div style={styles.resultStatus}>
                                    Status: {result.status}
                                </div>
                            )}
                        </div>
                    )}

                </div>
            </div>
        </div>
    );
}

const styles = {
    page: {
        minHeight: "100%",
        padding: "42px",
        color: "#e8f1ff",
        background:
            "radial-gradient(circle at 80% 0%, rgba(53,111,170,.15), transparent 35%), #06111e"
    },

    header: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        gap: "30px",
        marginBottom: "34px"
    },

    eyebrow: {
        color: "#67a9df",
        fontSize: "11px",
        letterSpacing: "3px",
        fontWeight: 700,
        marginBottom: "12px"
    },

    title: {
        margin: 0,
        fontSize: "38px",
        fontWeight: 750,
        letterSpacing: "-1px"
    },

    subtitle: {
        marginTop: "12px",
        color: "#7694b3",
        fontSize: "15px",
        maxWidth: "720px",
        lineHeight: 1.6
    },

    status: {
        border: "1px solid rgba(91,190,174,.25)",
        background: "rgba(38,120,105,.12)",
        borderRadius: "30px",
        padding: "10px 16px",
        color: "#76d8c4",
        fontSize: "11px",
        fontWeight: 700,
        letterSpacing: "1px",
        whiteSpace: "nowrap"
    },

    statusDot: {
        display: "inline-block",
        width: "7px",
        height: "7px",
        borderRadius: "50%",
        background: "#61d6bd",
        marginRight: "8px"
    },

    tabs: {
        display: "flex",
        gap: "10px",
        marginBottom: "20px"
    },

    tab: {
        padding: "13px 20px",
        borderRadius: "10px",
        border: "1px solid #1c344c",
        background: "#0a1929",
        color: "#7593b1",
        cursor: "pointer",
        fontWeight: 700
    },

    activeTab: {
        background: "#102a42",
        color: "#9deee1",
        borderColor: "#2b596e"
    },

    grid: {
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "20px"
    },

    card: {
        background: "rgba(10,25,41,.88)",
        border: "1px solid #19334b",
        borderRadius: "18px",
        padding: "28px",
        boxShadow: "0 20px 60px rgba(0,0,0,.18)"
    },

    cardHeader: {
        display: "flex",
        justifyContent: "space-between",
        marginBottom: "25px"
    },

    cardLabel: {
        fontSize: "10px",
        letterSpacing: "2px",
        color: "#5f8bb3",
        fontWeight: 800,
        marginBottom: "9px"
    },

    cardTitle: {
        margin: 0,
        fontSize: "22px"
    },

    iconBox: {
        width: "42px",
        height: "42px",
        borderRadius: "12px",
        display: "grid",
        placeItems: "center",
        background: "rgba(102,210,193,.1)",
        color: "#8de4d5",
        fontSize: "21px"
    },

    dropzone: {
        display: "block",
        textAlign: "center",
        border: "1px dashed #31536d",
        borderRadius: "15px",
        padding: "42px 20px",
        cursor: "pointer",
        background: "rgba(5,15,27,.55)"
    },

    uploadIcon: {
        margin: "auto",
        width: "54px",
        height: "54px",
        borderRadius: "15px",
        display: "grid",
        placeItems: "center",
        background: "#102b43",
        color: "#86e4d5",
        fontSize: "27px",
        marginBottom: "15px"
    },

    uploadTitle: {
        fontSize: "16px",
        fontWeight: 700,
        wordBreak: "break-word"
    },

    uploadText: {
        marginTop: "8px",
        color: "#6f8da9",
        fontSize: "13px"
    },

    formats: {
        marginTop: "18px",
        color: "#47708f",
        fontSize: "10px",
        letterSpacing: "1px"
    },

    fileRow: {
        marginTop: "15px",
        padding: "13px 15px",
        border: "1px solid #203c55",
        borderRadius: "10px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center"
    },

    fileName: {
        fontSize: "13px",
        fontWeight: 700
    },

    fileMeta: {
        color: "#64819d",
        fontSize: "11px",
        marginTop: "3px"
    },

    remove: {
        background: "transparent",
        border: "none",
        color: "#e8879b",
        cursor: "pointer"
    },

    primaryButton: {
        width: "100%",
        marginTop: "20px",
        padding: "15px",
        borderRadius: "10px",
        border: "none",
        background: "linear-gradient(135deg,#74d8ca,#55b8ce)",
        color: "#04131e",
        fontWeight: 800,
        cursor: "pointer",
        fontSize: "13px"
    },

    note: {
        textAlign: "center",
        color: "#4f718e",
        fontSize: "10px",
        marginTop: "14px"
    },

    error: {
        marginTop: "15px",
        padding: "12px",
        borderRadius: "9px",
        background: "rgba(190,50,80,.1)",
        border: "1px solid rgba(220,80,110,.25)",
        color: "#f08ca1",
        fontSize: "13px"
    },

    empty: {
        marginTop: "50px",
        textAlign: "center"
    },

    emptyIcon: {
        fontSize: "38px",
        color: "#75d8cb"
    },

    emptyTitle: {
        fontWeight: 750,
        fontSize: "17px"
    },

    emptyText: {
        color: "#66839e",
        fontSize: "13px",
        lineHeight: 1.6,
        maxWidth: "390px",
        margin: "auto"
    },

    features: {
        textAlign: "left",
        margin: "25px auto 0",
        maxWidth: "300px",
        color: "#7896b1",
        fontSize: "12px",
        lineHeight: 2
    },

    loadingBox: {
        textAlign: "center",
        marginTop: "70px"
    },

    spinner: {
        fontSize: "45px",
        color: "#7ce1d3",
        marginBottom: "20px"
    },

    loadingTitle: {
        fontSize: "17px",
        fontWeight: 700
    },

    loadingText: {
        marginTop: "9px",
        color: "#66839e",
        fontSize: "13px"
    },

    success: {
        padding: "12px 14px",
        borderRadius: "9px",
        background: "rgba(59,174,142,.1)",
        border: "1px solid rgba(80,200,170,.22)",
        color: "#83dfcc",
        fontSize: "12px",
        fontWeight: 700
    },

    resultFile: {
        marginTop: "16px",
        color: "#9bb5cc",
        fontSize: "13px"
    },

    stats: {
        display: "grid",
        gridTemplateColumns: "repeat(3,1fr)",
        gap: "10px",
        marginTop: "18px"
    },

    stat: {
        padding: "13px",
        borderRadius: "10px",
        background: "#081725",
        border: "1px solid #19344c"
    },

    summary: {
        marginTop: "20px",
        padding: "20px",
        borderRadius: "12px",
        background: "#071521",
        border: "1px solid #1d3a53"
    },

    summaryTitle: {
        fontSize: "10px",
        letterSpacing: "2px",
        color: "#66b4d8",
        fontWeight: 800,
        marginBottom: "13px"
    },

    summaryText: {
        whiteSpace: "pre-wrap",
        color: "#c4d6e8",
        lineHeight: 1.75,
        fontSize: "14px"
    },

    resultStatus: {
        marginTop: "15px",
        color: "#6d8ba7",
        fontSize: "11px"
    }
};
