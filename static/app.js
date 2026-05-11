/* ── Utility ── */
async function api(path, options = {}) {
  /* Fix #10: Only set Content-Type on requests with a body */
  const headers = options.body ? { "Content-Type": "application/json" } : {};
  const res = await fetch(path, { headers, ...options });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || "Request failed");
  return data;
}

/* ── Status badge ── */
function setStatus(running) {
  const badge = document.getElementById("statusBadge");
  if (running) {
    badge.textContent = "● main.py is running";
    badge.className = "badge badge-running";
  } else {
    badge.textContent = "● main.py is stopped";
    badge.className = "badge badge-stopped";
  }
}

/* ── Fix #8: Button loading state helpers ── */
function setBtnLoading(btn, loading) {
  if (loading) {
    btn.dataset.origText = btn.textContent;
    btn.textContent = "⏳ กำลังดำเนินการ…";
    btn.disabled = true;
    btn.style.opacity = "0.6";
  } else {
    btn.textContent = btn.dataset.origText || btn.textContent;
    btn.disabled = false;
    btn.style.opacity = "";
  }
}

/* ── Whitelist list ── */
function renderList(items) {
  const ul = document.getElementById("whitelist");
  ul.innerHTML = "";
  if (!items.length) {
    const li = document.createElement("li");
    li.textContent = "ยังไม่มีป้ายทะเบียนใน whitelist";
    li.style.color = "var(--muted)";
    ul.appendChild(li);
    return;
  }
  for (const plate of items) {
    const li = document.createElement("li");
    const span = document.createElement("span");
    span.textContent = plate;
    const btn = document.createElement("button");
    btn.className = "btn danger";
    btn.textContent = "Remove";
    btn.style.padding = "7px 12px";
    btn.onclick = async () => {
      setBtnLoading(btn, true);
      try {
        const data = await api("/api/whitelist", {
          method: "DELETE",
          body: JSON.stringify({ plate }),
        });
        renderList(data.items);
      } catch (err) { alert(err.message); }
      setBtnLoading(btn, false);
    };
    li.appendChild(span);
    li.appendChild(btn);
    ul.appendChild(li);
  }
}

/* ── LINE credentials helpers ── */
function showLineMsg(text, isOk) {
  const p = document.getElementById("lineMsg");
  p.textContent = text;
  p.className = "line-msg " + (isOk ? "ok" : "err");
  clearTimeout(p._timer);
  p._timer = setTimeout(() => { p.textContent = ""; p.className = "line-msg"; }, 5000);
}

function toggleVisibility(inputId, btn) {
  const input = document.getElementById(inputId);
  if (input.type === "password") {
    input.type = "text";
    btn.textContent = "🙈";
  } else {
    input.type = "password";
    btn.textContent = "👁";
  }
}

async function loadLineKeys() {
  try {
    const data = await api("/api/line-keys");
    document.getElementById("tokenInput").value  = data.token;
    document.getElementById("pushToInput").value = data.push_to;
  } catch (err) {
    showLineMsg("Failed to load credentials: " + err.message, false);
  }
}

/* ── Refresh all on load ── */
async function refreshAll() {
  const [status, wl] = await Promise.all([
    api("/api/status"),
    api("/api/whitelist"),
  ]);
  setStatus(status.running);
  renderList(wl.items);
  await loadLineKeys();
}

/* ── Fix #9: Auto-refresh status every 5 seconds ── */
setInterval(async () => {
  try {
    const data = await api("/api/status");
    setStatus(data.running);
  } catch (_) { /* silent — network might be down momentarily */ }
}, 5000);

/* ── Button wiring ── */
document.getElementById("runBtn").onclick = async () => {
  const btn = document.getElementById("runBtn");
  setBtnLoading(btn, true);
  try {
    await api("/api/run-main", { method: "POST" });
    setStatus(true);
  } catch (err) { alert(err.message); }
  setBtnLoading(btn, false);
};

document.getElementById("stopBtn").onclick = async () => {
  const btn = document.getElementById("stopBtn");
  setBtnLoading(btn, true);
  try {
    await api("/api/stop-main", { method: "POST" });
    setStatus(false);
  } catch (err) { alert(err.message); }
  setBtnLoading(btn, false);
};

document.getElementById("testLineBtn").onclick = async () => {
  const btn = document.getElementById("testLineBtn");
  setBtnLoading(btn, true);
  try {
    const data = await api("/api/test-line", { method: "POST" });
    showLineMsg("✓ " + data.message, true);
  } catch (err) {
    showLineMsg("✗ " + err.message, false);
  }
  setBtnLoading(btn, false);
};

document.getElementById("saveLineBtn").onclick = async () => {
  const btn = document.getElementById("saveLineBtn");
  const token  = document.getElementById("tokenInput").value.trim();
  const pushTo = document.getElementById("pushToInput").value.trim();
  if (!token || !pushTo) {
    showLineMsg("กรุณากรอกทั้ง Token และ Push-To ID", false);
    return;
  }
  setBtnLoading(btn, true);
  try {
    const data = await api("/api/line-keys", {
      method: "POST",
      body: JSON.stringify({ token, push_to: pushTo }),
    });
    showLineMsg("✓ " + data.message, true);
  } catch (err) {
    showLineMsg("✗ " + err.message, false);
  }
  setBtnLoading(btn, false);
};

document.getElementById("reloadLineBtn").onclick = () => loadLineKeys();

document.getElementById("addBtn").onclick = async () => {
  const input = document.getElementById("plateInput");
  const plate = input.value.trim();
  if (!plate) return;
  const btn = document.getElementById("addBtn");
  setBtnLoading(btn, true);
  try {
    const data = await api("/api/whitelist", {
      method: "POST",
      body: JSON.stringify({ plate }),
    });
    input.value = "";
    renderList(data.items);
  } catch (err) { alert(err.message); }
  setBtnLoading(btn, false);
};

// Also submit on Enter
document.getElementById("plateInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter") document.getElementById("addBtn").click();
});

refreshAll().catch((err) => {
  document.getElementById("statusBadge").textContent = "Error: " + err.message;
});
