
import { useState } from "react";
import "./App.css";

function App() {
  const [page, setPage] = useState("Dashboard");

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <div className="logo-box">AI</div>
          <div>
            <h2>Knowledge OS</h2>
            <p>Enterprise AI</p>
          </div>
        </div>

        <p className="menu-title">MAIN</p>

        <button
          className={page === "Dashboard" ? "menu active" : "menu"}
          onClick={() => setPage("Dashboard")}
        >
          <span>⌂</span>
          Dashboard
        </button>

        <button
          className={page === "AI Assistant" ? "menu active" : "menu"}
          onClick={() => setPage("AI Assistant")}
        >
          <span>✦</span>
          AI Assistant
        </button>

        <button
          className={page === "Knowledge Base" ? "menu active" : "menu"}
          onClick={() => setPage("Knowledge Base")}
        >
          <span>▤</span>
          Knowledge Base
        </button>

        <button
          className={page === "Search" ? "menu active" : "menu"}
          onClick={() => setPage("Search")}
        >
          <span>⌕</span>
          Semantic Search
        </button>

        <p className="menu-title">SYSTEM</p>

        <button
          className={page === "Analytics" ? "menu active" : "menu"}
          onClick={() => setPage("Analytics")}
        >
          <span>◒</span>
          Analytics
        </button>

        <button
          className={page === "Settings" ? "menu active" : "menu"}
          onClick={() => setPage("Settings")}
        >
          <span>⚙</span>
          Settings
        </button>

        <div className="system">
          <span className="online"></span>
          <div>
            <strong>System Online</strong>
            <small>All services operational</small>
          </div>
        </div>
      </aside>

      <main className="main">
        <header className="header">
          <div>
            <p className="small-title">ENTERPRISE AI KNOWLEDGE OS</p>
            <h1>{page}</h1>
            <p className="subtitle">
              Intelligent knowledge management for your organization.
            </p>
          </div>

          <button
            className="upload"
            onClick={() => setPage("Knowledge Base")}
          >
            + Upload Document
          </button>
        </header>

        {page === "Dashboard" && <Dashboard />}
        {page === "AI Assistant" && <Assistant />}
        {page === "Knowledge Base" && <Knowledge />}
        {page === "Search" && <Search />}
        {page === "Analytics" && <Analytics />}
        {page === "Settings" && <Settings />}
      </main>
    </div>
  );
}

function Dashboard() {
  return (
    <>
      <div className="stats">
        <Card icon="▤" title="Total Documents" value="1,248" />
        <Card icon="✦" title="AI Queries" value="8,426" />
        <Card icon="◈" title="Knowledge Nodes" value="42.8K" />
        <Card icon="✓" title="AI Accuracy" value="96.8%" />
      </div>

      <section className="ai-card">
        <div className="ai-header">
          <div className="ai-icon">✦</div>
          <div>
            <h2>Enterprise AI Assistant</h2>
            <p>Ask anything about your organization's knowledge.</p>
          </div>
          <span className="ai-status">● AI Online</span>
        </div>

        <div className="search-box">
          <span>⌕</span>
          <input placeholder="Ask your knowledge base anything..." />
          <button>Ask AI →</button>
        </div>

        <div className="suggestions">
          <span>Try asking:</span>
          <button>Summarize recent reports</button>
          <button>Find HR policies</button>
          <button>Explain company strategy</button>
        </div>
      </section>

      <div className="bottom">
        <section className="panel">
          <div className="panel-heading">
            <div>
              <h2>Recent Documents</h2>
              <p>Latest knowledge added to your system</p>
            </div>
            <button>View all</button>
          </div>

          <Document
            title="Enterprise Strategy 2026"
            info="PDF • 2.4 MB • 5 minutes ago"
          />

          <Document
            title="Employee Handbook"
            info="PDF • 4.8 MB • 1 hour ago"
          />

          <Document
            title="Q2 Financial Report"
            info="PDF • 1.8 MB • 3 hours ago"
          />
        </section>

        <section className="panel">
          <div className="panel-heading">
            <div>
              <h2>AI Activity</h2>
              <p>Recent system activity</p>
            </div>
          </div>

          <div className="big-number">842</div>
          <p className="muted">Queries today</p>

          <div className="progress">
            <div></div>
          </div>

          <div className="activity">
            <div>
              <strong>96.8%</strong>
              <small>Accuracy</small>
            </div>

            <div>
              <strong>1.2s</strong>
              <small>Response</small>
            </div>

            <div>
              <strong>98%</strong>
              <small>Success</small>
            </div>
          </div>
        </section>
      </div>
    </>
  );
}

function Card({ icon, title, value }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <div>
        <p>{title}</p>
        <h2>{value}</h2>
        <span>+12.4% this month</span>
      </div>
    </div>
  );
}

function Document({ title, info }) {
  return (
    <div className="document">
      <div className="document-icon">▤</div>
      <div className="document-info">
        <strong>{title}</strong>
        <small>{info}</small>
      </div>
      <span>Indexed</span>
    </div>
  );
}

function Assistant() {
  return (
    <section className="page">
      <h2>AI Knowledge Assistant</h2>
      <p className="muted">
        Ask questions about your organization's documents.
      </p>

      <div className="chat">
        <div className="large-icon">✦</div>
        <h2>How can I help you?</h2>
        <p>
          Ask about reports, policies, strategies and company knowledge.
        </p>
      </div>

      <div className="chat-input">
        <input placeholder="Ask your knowledge base..." />
        <button>Send →</button>
      </div>
    </section>
  );
}

function Knowledge() {
  return (
    <section className="page">
      <h2>Knowledge Base</h2>
      <p className="muted">
        Upload and manage your enterprise documents.
      </p>

      <label className="drop-zone">
        <div className="large-icon">↑</div>
        <h3>Upload Document</h3>
        <p>PDF, DOCX and TXT files supported</p>
        <input type="file" />
      </label>
    </section>
  );
}

function Search() {
  return (
    <section className="page">
      <h2>Semantic Search</h2>
      <p className="muted">
        Search your knowledge using AI-powered semantic matching.
      </p>

      <div className="search-box standalone">
        <span>⌕</span>
        <input placeholder="Search your knowledge base..." />
        <button>Search</button>
      </div>

      <div className="result">
        <div className="document-icon">▤</div>
        <div>
          <strong>Enterprise Strategy 2026</strong>
          <p>Strategic objectives and business priorities.</p>
          <span>94% relevant</span>
        </div>
      </div>
    </section>
  );
}

function Analytics() {
  return (
    <section className="page">
      <h2>Analytics</h2>
      <p className="muted">Monitor your AI system performance.</p>

      <div className="analytics">
        <Card title="Total Queries" value="8,426" icon="⌕" />
        <Card title="AI Accuracy" value="96.8%" icon="✓" />
        <Card title="Average Response" value="1.2s" icon="◷" />
        <Card title="Documents" value="1,248" icon="▤" />
      </div>
    </section>
  );
}

function Settings() {
  return (
    <section className="page">
      <h2>Settings</h2>
      <p className="muted">Configure your Knowledge OS.</p>

      <div className="setting">
        <div>
          <strong>AI System</strong>
          <p>Enable enterprise AI services.</p>
        </div>
        <div className="toggle"></div>
      </div>

      <div className="setting">
        <div>
          <strong>Semantic Search</strong>
          <p>Enable AI-powered semantic search.</p>
        </div>
        <div className="toggle"></div>
      </div>

      <div className="setting">
        <div>
          <strong>Document Indexing</strong>
          <p>Automatically index uploaded documents.</p>
        </div>
        <div className="toggle"></div>
      </div>
    </section>
  );
}

export default App;

