const BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

async function req(path, opt = {}) {
  const r = await fetch(BASE + path, opt);
  const t = await r.text();

  let d = {};
  try {
    d = t ? JSON.parse(t) : {};
  } catch {
    d = { message: t };
  }

  if (!r.ok) {
    throw Error(d.detail || d.message || `Request failed (${r.status})`);
  }

  return d;
}

const api = {
  health: () => req("/health"),

  ask: (question) =>
    req("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    }),

  investigate: (question) =>
    req("/api/agent/research", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    }),

  uploadDocument: (file) => {
    const form = new FormData();
    form.append("file", file);

    return req("/api/documents/upload", {
      method: "POST",
      body: form
    });
  },

  uploadSummary: (file) => {
    const form = new FormData();
    form.append("file", file);

    return req("/documents/upload-summary", {
      method: "POST",
      body: form
    });
  },

  history: () => req("/api/agent/history")
};

export default api;

