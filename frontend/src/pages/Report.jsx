import { useEffect, useMemo, useState } from "react";
import api from "../lib/api";

function Section({ title, children }) {
    return (
        <section style={{
            background: "#111827",
            border: "1px solid #263244",
            borderRadius: 16,
            padding: 22,
            marginBottom: 18
        }}>
            <h2 style={{
                margin: "0 0 16px",
                fontSize: 17,
                color: "#f8fafc"
            }}>
                {title}
            </h2>
            {children}
        </section>
    );
}

function Item({ item }) {
    if (item === null || item === undefined) return null;

    if (typeof item !== "object") {
        return (
            <div style={{
                padding: "10px 12px",
                borderRadius: 8,
                background: "#0b1220",
                color: "#cbd5e1",
                marginBottom: 8,
                lineHeight: 1.5
            }}>
                {String(item)}
            </div>
        );
    }

    return (
        <div style={{
            padding: 14,
            borderRadius: 10,
            background: "#0b1220",
            border: "1px solid #1e293b",
            marginBottom: 10
        }}>
            {Object.entries(item).map(([key, value]) => (
                <div key={key} style={{ marginBottom: 9 }}>
                    <div style={{
                        fontSize: 11,
                        textTransform: "uppercase",
                        letterSpacing: ".08em",
                        color: "#64748b",
                        marginBottom: 3
                    }}>
                        {key.replaceAll("_", " ")}
                    </div>

                    {typeof value === "object"
                        ? <Item item={value} />
                        : <div style={{
                            color: "#e2e8f0",
                            lineHeight: 1.5
                        }}>
                            {String(value)}
                        </div>
                    }
                </div>
            ))}
        </div>
    );
}

function DataSection({ title, data }) {
    if (!data) return null;

    const values = Array.isArray(data) ? data : [data];

    return (
        <Section title={title}>
            {values.length === 0
                ? <div style={{ color: "#64748b" }}>No data available.</div>
                : values.map((item, index) => (
                    <Item key={index} item={item} />
                ))
            }
        </Section>
    );
}

export default function Report() {
    const [history, setHistory] = useState([]);
    const [selected, setSelected] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    async function loadReports() {
        try {
            setLoading(true);
            setError("");

            const result = await api.getHistory();

            const records =
                Array.isArray(result)
                    ? result
                    : result?.history ||
                      result?.investigations ||
                      result?.data ||
                      [];

            setHistory(records);

            if (records.length > 0) {
                setSelected(records[0]);
            }
        } catch (err) {
            setError(err.message || "Unable to load investigation history.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadReports();
    }, []);

    const report = selected || {};

    const counts = useMemo(() => {
        const findings =
            report.findings ||
            report.result?.findings ||
            [];

        const risks =
            report.risks ||
            report.result?.risks ||
            [];

        const conflicts =
            report.policy_conflicts ||
            report.conflicts ||
            report.result?.policy_conflicts ||
            [];

        const gaps =
            report.knowledge_gaps ||
            report.gaps ||
            report.result?.knowledge_gaps ||
            [];

        const actions =
            report.remediation_actions ||
            report.actions ||
            report.result?.remediation_actions ||
            [];

        return {
            findings: Array.isArray(findings) ? findings.length : 0,
            risks: Array.isArray(risks) ? risks.length : 0,
            conflicts: Array.isArray(conflicts) ? conflicts.length : 0,
            gaps: Array.isArray(gaps) ? gaps.length : 0,
            actions: Array.isArray(actions) ? actions.length : 0
        };
    }, [report]);

    function printReport() {
        window.print();
    }

    return (
        <div style={{
            maxWidth: 1250,
            margin: "0 auto",
            paddingBottom: 40
        }}>

            <div className="report-header" style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                gap: 20,
                marginBottom: 26
            }}>
                <div>
                    <div style={{
                        color: "#64748b",
                        fontSize: 11,
                        letterSpacing: ".14em",
                        fontWeight: 700,
                        marginBottom: 8
                    }}>
                        ENTERPRISE INTELLIGENCE
                    </div>

                    <h1 style={{
                        margin: 0,
                        color: "#f8fafc",
                        fontSize: 30
                    }}>
                        Executive Reports
                    </h1>

                    <p style={{
                        color: "#94a3b8",
                        marginTop: 8
                    }}>
                        Investigation results, evidence and remediation intelligence.
                    </p>
                </div>

                <button
                    onClick={printReport}
                    disabled={!selected}
                    style={{
                        border: "1px solid #334155",
                        background: "#2563eb",
                        color: "white",
                        borderRadius: 10,
                        padding: "11px 18px",
                        cursor: "pointer",
                        fontWeight: 700
                    }}
                >
                    Export / Print Report
                </button>
            </div>

            {loading && (
                <Section title="Loading">
                    <div style={{ color: "#94a3b8" }}>
                        Loading investigation history...
                    </div>
                </Section>
            )}

            {error && (
                <Section title="Report Error">
                    <div style={{ color: "#fca5a5" }}>
                        {error}
                    </div>
                    <button
                        onClick={loadReports}
                        style={{
                            marginTop: 12,
                            padding: "9px 14px",
                            borderRadius: 8,
                            border: "1px solid #475569",
                            background: "#1e293b",
                            color: "white",
                            cursor: "pointer"
                        }}
                    >
                        Retry
                    </button>
                </Section>
            )}

            {!loading && !error && history.length === 0 && (
                <Section title="No Investigations Yet">
                    <div style={{
                        color: "#94a3b8",
                        lineHeight: 1.7
                    }}>
                        Run an investigation first. Completed investigations
                        will automatically appear here as executive reports.
                    </div>
                </Section>
            )}

            {history.length > 0 && (
                <>
                    <Section title="Investigation History">
                        <select
                            value={history.indexOf(selected)}
                            onChange={(e) =>
                                setSelected(history[Number(e.target.value)])
                            }
                            style={{
                                width: "100%",
                                padding: 12,
                                borderRadius: 9,
                                border: "1px solid #334155",
                                background: "#0b1220",
                                color: "#e2e8f0"
                            }}
                        >
                            {history.map((item, index) => (
                                <option key={index} value={index}>
                                    Investigation #{item.id || index + 1}
                                    {" — "}
                                    {item.objective ||
                                        item.question ||
                                        item.title ||
                                        "Enterprise investigation"}
                                </option>
                            ))}
                        </select>
                    </Section>

                    <Section title="Investigation Overview">
                        <div style={{
                            color: "#e2e8f0",
                            fontSize: 16,
                            lineHeight: 1.7
                        }}>
                            {report.objective ||
                                report.question ||
                                report.title ||
                                report.result?.objective ||
                                "Enterprise AI security investigation"}
                        </div>

                        {report.created_at && (
                            <div style={{
                                marginTop: 10,
                                color: "#64748b",
                                fontSize: 13
                            }}>
                                Created: {report.created_at}
                            </div>
                        )}
                    </Section>

                    <div style={{
                        display: "grid",
                        gridTemplateColumns: "repeat(auto-fit,minmax(170px,1fr))",
                        gap: 14,
                        marginBottom: 18
                    }}>
                        {[
                            ["Findings", counts.findings],
                            ["Risks", counts.risks],
                            ["Policy Conflicts", counts.conflicts],
                            ["Knowledge Gaps", counts.gaps],
                            ["Remediation Actions", counts.actions]
                        ].map(([label, value]) => (
                            <div key={label} style={{
                                background: "#111827",
                                border: "1px solid #263244",
                                borderRadius: 14,
                                padding: 20
                            }}>
                                <div style={{
                                    color: "#64748b",
                                    fontSize: 11,
                                    textTransform: "uppercase",
                                    letterSpacing: ".07em"
                                }}>
                                    {label}
                                </div>

                                <div style={{
                                    marginTop: 8,
                                    color: "#f8fafc",
                                    fontSize: 30,
                                    fontWeight: 800
                                }}>
                                    {value}
                                </div>
                            </div>
                        ))}
                    </div>

                    <DataSection
                        title="Findings"
                        data={report.findings || report.result?.findings}
                    />

                    <DataSection
                        title="Risks"
                        data={report.risks || report.result?.risks}
                    />

                    <DataSection
                        title="Policy Conflicts"
                        data={
                            report.policy_conflicts ||
                            report.conflicts ||
                            report.result?.policy_conflicts
                        }
                    />

                    <DataSection
                        title="Knowledge Gaps"
                        data={
                            report.knowledge_gaps ||
                            report.gaps ||
                            report.result?.knowledge_gaps
                        }
                    />

                    <DataSection
                        title="Remediation Actions"
                        data={
                            report.remediation_actions ||
                            report.actions ||
                            report.result?.remediation_actions
                        }
                    />

                    <DataSection
                        title="Evidence & Sources"
                        data={
                            report.sources ||
                            report.evidence ||
                            report.result?.sources
                        }
                    />

                    <DataSection
                        title="Verification"
                        data={
                            report.verification ||
                            report.result?.verification
                        }
                    />
                </>
            )}
        </div>
    );
}
