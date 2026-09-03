import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../lib/api";


export default function Dashboard() {

  const employee =
    localStorage.getItem("eakos_name") ||
    localStorage.getItem("eakos_user") ||
    "Employee";


  const [workspace, setWorkspace] = useState(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");


  async function loadWorkspace() {

    try {

      setLoading(true);

      setError("");

      const data =
        await api.getWorkspace();

      setWorkspace(data);

    }
    catch (err) {

      console.error(err);

      setError(
        err?.message ||
        "Unable to load employee workspace."
      );

    }
    finally {

      setLoading(false);

    }

  }


  useEffect(() => {

    loadWorkspace();

    const interval =
      setInterval(loadWorkspace, 15000);

    return () =>
      clearInterval(interval);

  }, []);


  const attention =
    workspace?.attention || [];


  const companyActivity =
    workspace?.company_activity || [];


  const myActivity =
    workspace?.my_activity || [];


  const myWork =
    workspace?.my_work || {};


  return (

    <div
      style={{
        maxWidth: "1250px",
        margin: "0 auto",
        padding: "44px",
        boxSizing: "border-box"
      }}
    >


      {/* HEADER */}

      <div
        style={{
          marginBottom: "30px"
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
          EMPLOYEE INTELLIGENCE
        </div>


        <h1
          style={{
            margin: "8px 0",
            color: "#edf5ff",
            fontSize: "34px"
          }}
        >
          Welcome, {employee}
        </h1>


        <p
          style={{
            margin: 0,
            color: "#8fa4bd"
          }}
        >
          Here's what is happening across your workspace
          and what needs your attention.
        </p>

      </div>


      {/* ERROR */}

      {error && (

        <div
          style={{
            padding: "14px",
            marginBottom: "20px",
            borderRadius: "10px",
            background: "#35161b",
            border: "1px solid #713b48",
            color: "#f0a4b0"
          }}
        >
          {error}
        </div>

      )}


      {/* MY WORK */}

      <section
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(210px,1fr))",
          gap: "14px",
          marginBottom: "20px"
        }}
      >

        <MetricCard
          label="MY INVESTIGATIONS"
          value={myWork.investigations || 0}
          description="AI investigations completed"
        />

        <MetricCard
          label="DOCUMENTS"
          value={myWork.documents_uploaded || 0}
          description="Documents uploaded"
        />

        <MetricCard
          label="MY ACTIVITY"
          value={myWork.activities || 0}
          description="Recorded workspace actions"
        />

        <MetricCard
          label="SYSTEM"
          value="ONLINE"
          description="AI services available"
        />

      </section>


      {/* NEEDS ATTENTION */}

      <section className="panel">

        <div className="panel-header">

          <div>

            <div className="eyebrow">
              PRIORITY
            </div>

            <h2>
              Needs My Attention
            </h2>

            <p>
              Actions and items that may require your attention.
            </p>

          </div>

        </div>


        {loading && (

          <div className="answer-text">
            Loading your workspace...
          </div>

        )}


        {!loading && attention.length === 0 && (

          <div
            className="answer-text"
            style={{
              color: "#72ded8"
            }}
          >
            ✓ No immediate actions detected.
          </div>

        )}


        {!loading && attention.length > 0 && (

          <div
            style={{
              display: "grid",
              gap: "10px"
            }}
          >

            {attention.map((item) => (

              <div
                key={item.id}
                style={{
                  padding: "17px",
                  borderRadius: "10px",
                  background: "#091321",
                  border: "1px solid #30445d"
                }}
              >

                <div
                  style={{
                    color:
                      item.priority === "high"
                        ? "#f28b9c"
                        : "#e3bd73",
                    fontSize: "11px",
                    fontWeight: "800",
                    letterSpacing: "1px",
                    marginBottom: "6px"
                  }}
                >
                  {item.priority?.toUpperCase() || "ACTION"}
                </div>


                <strong
                  style={{
                    color: "#e3edf8"
                  }}
                >
                  {item.title}
                </strong>


                <p
                  style={{
                    color: "#8197af",
                    margin: "7px 0"
                  }}
                >
                  {item.description}
                </p>


                {item.action && (

                  <Link
                    to={
                      item.action.includes("Investigation")
                        ? "/investigation"
                        : "/knowledge-base"
                    }
                    style={{
                      color: "#69d9d5",
                      fontSize: "13px",
                      fontWeight: "700",
                      textDecoration: "none"
                    }}
                  >
                    {item.action} →
                  </Link>

                )}

              </div>

            ))}

          </div>

        )}

      </section>


      {/* COMPANY ACTIVITY */}

      <section className="panel">

        <div className="panel-header">

          <div>

            <div className="eyebrow">
              LIVE WORKSPACE
            </div>

            <h2>
              What's Happening
            </h2>

            <p>
              Recent activity across the enterprise.
            </p>

          </div>

          <span className="status-badge">
            LIVE
          </span>

        </div>


        {companyActivity.length === 0 ? (

          <div className="answer-text">
            No company activity recorded yet.
          </div>

        ) : (

          <div
            style={{
              display: "grid",
              gap: "9px"
            }}
          >

            {companyActivity.slice(0, 10).map((item) => (

              <ActivityRow
                key={item.id}
                item={item}
              />

            ))}

          </div>

        )}

      </section>


      {/* MY RECENT ACTIVITY */}

      <section className="panel">

        <div className="panel-header">

          <div>

            <div className="eyebrow">
              MY WORKSPACE
            </div>

            <h2>
              My Recent Activity
            </h2>

            <p>
              Your latest actions in the Knowledge OS.
            </p>

          </div>

        </div>


        {myActivity.length === 0 ? (

          <div className="answer-text">
            Your activity will appear here as you work.
          </div>

        ) : (

          <div
            style={{
              display: "grid",
              gap: "9px"
            }}
          >

            {myActivity.slice(0, 10).map((item) => (

              <ActivityRow
                key={item.id}
                item={item}
              />

            ))}

          </div>

        )}

      </section>


      {/* QUICK ACTIONS */}

      <section
        className="panel"
      >

        <div className="panel-header">

          <div>

            <div className="eyebrow">
              WORKSPACE ACTIONS
            </div>

            <h2>
              Continue Working
            </h2>

          </div>

        </div>


        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit,minmax(220px,1fr))",
            gap: "12px"
          }}
        >

          <QuickAction
            title="Upload Document"
            description="Add a document and make it searchable."
            to="/knowledge-base"
          />

          <QuickAction
            title="Summarize Document"
            description="Generate an AI summary from an uploaded document."
            to="/knowledge-base"
          />

          <QuickAction
            title="Start Investigation"
            description="Ask AI a complex enterprise question."
            to="/investigation"
          />

          <QuickAction
            title="View Reports"
            description="Review your investigation and activity history."
            to="/report"
          />

        </div>

      </section>


    </div>

  );

}


function MetricCard({
  label,
  value,
  description
}) {

  return (

    <div
      style={{
        background: "#0d1928",
        border: "1px solid #263b54",
        borderRadius: "12px",
        padding: "18px"
      }}
    >

      <div
        style={{
          color: "#607b98",
          fontSize: "10px",
          fontWeight: "700",
          letterSpacing: "1.5px"
        }}
      >
        {label}
      </div>


      <div
        style={{
          color: "#e3edf8",
          fontSize: "25px",
          fontWeight: "800",
          margin: "8px 0 4px"
        }}
      >
        {value}
      </div>


      <div
        style={{
          color: "#71869d",
          fontSize: "12px"
        }}
      >
        {description}
      </div>

    </div>

  );

}


function ActivityRow({ item }) {

  const date =
    item.timestamp
      ? new Date(item.timestamp)
          .toLocaleString()
      : "";


  return (

    <div
      style={{
        display: "flex",
        alignItems: "flex-start",
        gap: "12px",
        padding: "13px 14px",
        background: "#091321",
        border: "1px solid #253950",
        borderRadius: "9px"
      }}
    >

      <span
        style={{
          width: "8px",
          height: "8px",
          marginTop: "6px",
          flexShrink: 0,
          borderRadius: "50%",
          background: "#69d9d5",
          boxShadow:
            "0 0 10px rgba(105,217,213,.5)"
        }}
      />


      <div style={{ minWidth: 0 }}>

        <strong
          style={{
            color: "#dceafa",
            fontSize: "14px"
          }}
        >
          {item.title}
        </strong>


        <div
          style={{
            color: "#8197af",
            fontSize: "12px",
            marginTop: "4px"
          }}
        >
          {item.employee || "Employee"}
          {item.description
            ? ` · ${item.description}`
            : ""}
        </div>


        {date && (

          <div
            style={{
              color: "#566e88",
              fontSize: "11px",
              marginTop: "5px"
            }}
          >
            {date}
          </div>

        )}

      </div>

    </div>

  );

}


function QuickAction({
  title,
  description,
  to
}) {

  return (

    <Link
      to={to}
      style={{
        textDecoration: "none",
        padding: "18px",
        borderRadius: "11px",
        border: "1px solid #263b54",
        background: "#091321"
      }}
    >

      <strong
        style={{
          color: "#e3edf8",
          fontSize: "15px"
        }}
      >
        {title}
      </strong>


      <p
        style={{
          color: "#8197af",
          fontSize: "12px",
          lineHeight: "1.6",
          marginBottom: 0
        }}
      >
        {description}
      </p>

    </Link>

  );

}
