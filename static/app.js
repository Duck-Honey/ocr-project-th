async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.message || "Request failed");
  }
  return data;
}

function setStatus(text) {
  document.getElementById("statusText").textContent = text;
}

function renderList(items) {
  const ul = document.getElementById("whitelist");
  ul.innerHTML = "";
  if (!items.length) {
    const li = document.createElement("li");
    li.textContent = "No whitelist plates yet.";
    ul.appendChild(li);
    return;
  }

  for (const plate of items) {
    const li = document.createElement("li");
    li.innerHTML = `<span>${plate}</span>`;
    const btn = document.createElement("button");
    btn.className = "btn danger";
    btn.textContent = "Remove";
    btn.onclick = async () => {
      try {
        const data = await api("/api/whitelist", {
          method: "DELETE",
          body: JSON.stringify({ plate }),
        });
        renderList(data.items);
      } catch (err) {
        alert(err.message);
      }
    };
    li.appendChild(btn);
    ul.appendChild(li);
  }
}

async function refreshAll() {
  const status = await api("/api/status");
  setStatus(status.running ? "main.py is running" : "main.py is stopped");
  const wl = await api("/api/whitelist");
  renderList(wl.items);
}

document.getElementById("runBtn").onclick = async () => {
  try {
    const data = await api("/api/run-main", { method: "POST" });
    setStatus(data.message);
  } catch (err) {
    alert(err.message);
  }
};

document.getElementById("stopBtn").onclick = async () => {
  try {
    const data = await api("/api/stop-main", { method: "POST" });
    setStatus(data.message);
  } catch (err) {
    alert(err.message);
  }
};

document.getElementById("testLineBtn").onclick = async () => {
  try {
    const data = await api("/api/test-line", { method: "POST" });
    alert(data.message);
  } catch (err) {
    alert(err.message);
  }
};

document.getElementById("addBtn").onclick = async () => {
  const input = document.getElementById("plateInput");
  const plate = input.value.trim();
  if (!plate) {
    return;
  }
  try {
    const data = await api("/api/whitelist", {
      method: "POST",
      body: JSON.stringify({ plate }),
    });
    input.value = "";
    renderList(data.items);
  } catch (err) {
    alert(err.message);
  }
};

refreshAll().catch((err) => setStatus(err.message));
