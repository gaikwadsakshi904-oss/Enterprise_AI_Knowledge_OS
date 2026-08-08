import {
  FileText,
  MessageSquare,
  Database,
  BarChart3
} from "lucide-react";

function Dashboard() {
  return (
    <div>

      <h1>Dashboard</h1>

      <p className="page-description">
        Overview of your Enterprise AI Knowledge System.
      </p>

      <div className="stats-grid">

        <div className="stat-card">
          <div className="stat-icon">
            <FileText size={20} />
          </div>

          <div>
            <p>Total Documents</p>
            <h2>1,248</h2>
            <span className="positive">
              +12% this month
            </span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <MessageSquare size={20} />
          </div>

          <div>
            <p>AI Queries</p>
            <h2>8,426</h2>
            <span className="positive">
              +18% this month
            </span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Database size={20} />
          </div>

          <div>
            <p>Knowledge Nodes</p>
            <h2>42.8K</h2>
            <span className="positive">
              +8.4% this month
            </span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <BarChart3 size={20} />
          </div>

          <div>
            <p>AI Accuracy</p>
            <h2>96.8%</h2>
            <span className="positive">
              +2.1% this month
            </span>
          </div>
        </div>

      </div>

    </div>
  );
}

export default Dashboard;