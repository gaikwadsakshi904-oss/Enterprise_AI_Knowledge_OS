const API_BASE =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";


async function req(path, options = {}) {

  const response = await fetch(
    `${API_BASE}${path}`,
    {
      ...options,

      headers: {
        ...(options.body instanceof FormData
          ? {}
          : { "Content-Type": "application/json" }),

        ...(options.headers || {})
      }
    }
  );


  const text = await response.text();

  let data = {};

  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = {
      raw: text
    };
  }


  if (!response.ok) {

    throw new Error(
      data?.detail ||
      data?.message ||
      data?.error ||
      `Request failed: ${response.status}`
    );

  }


  return data;
}


/* ============================================================
   CURRENT EMPLOYEE
   ============================================================ */

function getEmployee() {

  return (
    localStorage.getItem("eakos_name") ||
    localStorage.getItem("eakos_user") ||
    "Current Employee"
  );

}


/* ============================================================
   EMPLOYEE ACTIVITY
   ============================================================ */

async function recordActivity(
  activity_type,
  title,
  description = "",
  metadata = {}
) {

  try {

    return await req(
      "/api/employee/activity",
      {
        method: "POST",

        body: JSON.stringify({

          employee: getEmployee(),

          activity_type,

          title,

          description,

          metadata

        })

      }
    );

  } catch (error) {

    /*
     * Activity tracking must never break the main
     * application workflow.
     */

    console.warn(
      "Activity tracking failed:",
      error
    );

    return null;

  }

}


/* ============================================================
   API
   ============================================================ */

const api = {


  health: () =>
    req("/health"),


  /* ----------------------------------------------------------
     KNOWLEDGE BASE
     ---------------------------------------------------------- */

  ask: (question) =>
    req("/api/ask", {

      method: "POST",

      body: JSON.stringify({
        question: question.trim()
      })

    }),


  /* ----------------------------------------------------------
     INVESTIGATION
     ---------------------------------------------------------- */

  investigate: async (
    objective,
    employee
  ) => {

    const currentEmployee =
      employee ||
      getEmployee();


    const result = await req(
      "/api/agent/research",
      {

        method: "POST",

        body: JSON.stringify({

          objective,

          employee: currentEmployee

        })

      }
    );


    /*
     * Record completed investigation.
     */

    await recordActivity(

      "investigation_completed",

      "AI investigation completed",

      objective,

      {
        investigation_id:
          result?.id ||
          result?.investigation_id ||
          null,

        evidence_count:
          result?.evidence_count ||
          0,

        source_count:
          result?.source_count ||
          0
      }

    );


    return result;

  },


  getHistory: () =>
    req("/api/agent/history"),


  getInvestigation: (id) =>
    req(`/api/agent/history/${id}`),


  /* ----------------------------------------------------------
     DOCUMENT UPLOAD
     ---------------------------------------------------------- */

  uploadDocument: async (file) => {

    const form =
      new FormData();

    form.append(
      "file",
      file
    );


    const result = await req(
      "/api/documents/upload",
      {

        method: "POST",

        body: form

      }
    );


    /*
     * Record document upload.
     */

    await recordActivity(

      "document_uploaded",

      `Document uploaded: ${file.name}`,

      "Employee uploaded a document to the enterprise knowledge base.",

      {
        filename: file.name,

        size_bytes: file.size,

        job_id:
          result?.job_id ||
          null
      }

    );


    return result;

  },


  getJob: (jobId) =>
    req(`/api/jobs/${jobId}`),


  /* ----------------------------------------------------------
     DOCUMENT SUMMARY
     ---------------------------------------------------------- */

  uploadSummary: async (file) => {

    const form =
      new FormData();

    form.append(
      "file",
      file
    );


    const result = await req(
      "/documents/upload-summary",
      {

        method: "POST",

        body: form

      }
    );


    /*
     * Record summary generation.
     */

    await recordActivity(

      "document_summarized",

      `Document summarized: ${file.name}`,

      "AI generated a summary of the uploaded document.",

      {
        filename: file.name
      }

    );


    return result;

  },


  /* ----------------------------------------------------------
     EMPLOYEE WORKSPACE
     ---------------------------------------------------------- */

  getWorkspace: () => {

    const employee =
      getEmployee();


    return req(
      `/api/employee/workspace?employee=${encodeURIComponent(employee)}`
    );

  },


  recordActivity

};


export default api;
