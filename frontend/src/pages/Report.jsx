import { useEffect, useState } from "react";
import api from "../lib/api";

export default function Report() {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const loadReport = async () => {
        try {
            setLoading(true);
            setError("");

            const data = await api.getHistory();

            const items = Array.isArray(data)
                ? data
                : data?.history || [];

            setHistory([...items].reverse());
        } catch (err) {
            console.error(err);
            setError(err?.message || "Unable to load reports.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadReport();
        const timer = setInterval(loadReport, 5000);
        return () => clearInterval(timer);
    }, []);

    const formatDate = (value) => {
        if (!value) return "—";
        const d = new Date(value);
        return isNaN(d.getTime())
            ? value
            : d.toLocaleString("en-IN", {
                dateStyle: "medium",
                timeStyle: "medium"
            });
    };

    const formatDuration = (seconds) => {
        if (seconds === undefined || seconds === null) return "—";
        if (seconds < 60) return `${seconds.toFixed(1)} seconds`;
        const m = Math.floor(seconds / 60);
        const s = Math.round(seconds % 60);
        return `${m}m ${s}s`;
    };

    return (
        <div className="report-page">
            <header className="report-hero">
                <div>
                    <div className="report-eyebrow">ENTERPRISE INTELLIGENCE</div>
                    <h1>Executive Reports</h1>
                    <p>Real-time investigation activity, evidence and AI-generated intelligence.</p>
                </div>

                <button className="report-export" onClick={() => window.print()}>
                    Export / Print Report
                </button>
            </header>

            {loading && history.length === 0 && (
                <section className="report-panel">
                    <h2>Loading intelligence...</h2>
                </section>
            )}

            {error && (
                <section className="report-panel report-error">
                    <h2>Unable to load reports</h2>
                    <p>{error}</p>
                    <button className="report-retry" onClick={loadReport}>
                        Retry
                    </button>
                </section>
            )}

            {!error && history.length > 0 && (
                <section className="report-panel">
                    <div className="report-section-header">
                        <div>
                            <div className="report-eyebrow">INVESTIGATION ACTIVITY</div>
                            <h2>Employee Intelligence</h2>
                        </div>

                        <div className="report-count">
                            <strong>{history.length}</strong>
                            <span>investigations</span>
                        </div>
                    </div>

                    <div className="report-grid">
                        {history.map((item, index) => {
                            const question =
                                item.objective ||
                                item.question ||
                                item.query ||
                                "Investigation";

                            const result =
                                item.report ||
                                item.answer ||
                                item.summary ||
                                item.result ||
                                "";

                            const work =
                                Array.isArray(item.work_completed)
                                    ? item.work_completed
                                    : [];

                            const employee =
                                item.employee ||
                                "Current Employee";

                            return (
                                <article
                                    className="report-card"
                                    key={item.id || item.investigation_id || index}
                                >
                                    <div className="report-card-top">
                                        <span className="report-number">
                                            REPORT #{item.id || history.length - index}
                                        </span>

                                        <span className="report-date">
                                            {formatDate(item.completed_at || item.timestamp)}
                                        </span>
                                    </div>

                                    <div className="report-status">
                                        <span className="status-dot" />
                                        {item.status === "completed"
                                            ? "Investigation completed"
                                            : item.status || "Investigation"}
                                    </div>

                                    <h3>{question}</h3>

                                    <div className="report-meta">
                                        <div><strong>Employee:</strong> {employee}</div>
                                        <div><strong>Started:</strong> {formatDate(item.started_at)}</div>
                                        <div><strong>Completed:</strong> {formatDate(item.completed_at)}</div>
                                        <div><strong>Duration:</strong> {formatDuration(item.duration_seconds)}</div>
                                        <div><strong>Evidence:</strong> {item.evidence_count ?? "—"}</div>
                                        <div><strong>Sources:</strong> {item.source_count ?? "—"}</div>
                                    </div>

                                    {work.length > 0 && (
                                        <div className="report-work">
                                            <div className="report-eyebrow">WORK COMPLETED</div>
                                            {work.map((step, i) => (
                                                <div key={i} className="work-step">
                                                    <span>✓</span>
                                                    {step}
                                                </div>
                                            ))}
                                        </div>
                                    )}

                                    <div className="report-result">
                                        <div className="report-eyebrow">EXECUTIVE RESULT</div>
                                        <p>{result || "No executive result available."}</p>
                                    </div>
                                </article>
                            );
                        })}
                    </div>
                </section>
            )}
        </div>
    );
}
