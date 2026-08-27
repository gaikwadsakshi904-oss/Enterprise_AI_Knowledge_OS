const API_BASE = "http://127.0.0.1:8000";

async function handleResponse(response) {
    const text = await response.text();

    let data = null;

    try {
        data = text ? JSON.parse(text) : null;
    } catch {
        data = null;
    }

    if (!response.ok) {
        const message =
            data?.detail ||
            data?.message ||
            text ||
            `Request failed: ${response.status}`;

        throw new Error(
            typeof message === "string"
                ? message
                : JSON.stringify(message)
        );
    }

    return data;
}

const api = {

    async health() {
        const response = await fetch(
            `${API_BASE}/health`
        );

        return handleResponse(response);
    },

    async ask(question) {
        const response = await fetch(
            `${API_BASE}/api/ask`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    question: question.trim(),
                }),
            }
        );

        return handleResponse(response);
    },

    async investigate(objective) {
        if (!objective || !objective.trim()) {
            throw new Error("Investigation objective is required.");
        }

        const response = await fetch(
            `${API_BASE}/api/agent/research`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    objective: objective.trim(),
                }),
            }
        );

        return handleResponse(response);
    },

    async uploadDocument(file) {
        if (!file) {
            throw new Error("Please select a document.");
        }

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(
            `${API_BASE}/api/documents/upload`,
            {
                method: "POST",
                body: formData,
            }
        );

        return handleResponse(response);
    },

    async getHistory() {
        const response = await fetch(
            `${API_BASE}/api/agent/history`
        );

        return handleResponse(response);
    },

    async getInvestigation(id) {
        const response = await fetch(
            `${API_BASE}/api/agent/history/${id}`
        );

        return handleResponse(response);
    },
};

export default api;
