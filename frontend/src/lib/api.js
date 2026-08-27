const API_BASE =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";

async function req(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...(options.body instanceof FormData
        ? {}
        : { "Content-Type": "application/json" }),
      ...(options.headers || {})
    }
  });

  let data = null;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      data?.message ||
      `Request failed: ${response.status}`
    );
  }

  return data;
}

const api = {
  health: () =>
    req("/health"),

  ask: (question) =>
    req("/api/ask", {
      method: "POST",
      body: JSON.stringify({
        question: question
      })
    }),

  investigate: (objective, employee) =>
    req("/api/agent/research", {
      method: "POST",
      body: JSON.stringify({
        objective: objective,
        employee:
          employee ||
          localStorage.getItem("eakos_name") ||
          localStorage.getItem("eakos_user") ||
          "Current Employee"
      })
    }),

  getHistory: () =>
    req("/api/agent/history"),

  getInvestigation: (id) =>
    req(`/api/agent/history/${id}`),

  uploadDocument: (file) => {
    const form = new FormData();
    form.append("file", file);

    return req("/api/documents/upload", {
      method: "POST",
      body: form
    });
  },

  getJob: (jobId) =>
    req(`/api/jobs/${jobId}`),

  uploadSummary: (file) => {
    const form = new FormData();
    form.append("file", file);

    return req("/documents/upload-summary", {
      method: "POST",
      body: form
    });
  }
};

export default api;
