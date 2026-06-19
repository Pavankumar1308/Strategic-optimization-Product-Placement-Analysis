const API_BASE = "http://127.0.0.1:5000/api";

function getToken() {
  return localStorage.getItem("token");
}

async function apiRequest(path, method = "GET", body = null, auth = true) {
  const headers = { "Content-Type": "application/json" };
  if (auth && getToken()) headers["Authorization"] = `Bearer ${getToken()}`;

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}
