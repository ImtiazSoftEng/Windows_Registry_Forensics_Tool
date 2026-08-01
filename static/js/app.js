/**
 * app.js
 * ---------------------------------------------------------------------
 * Front end logic for the Windows Registry Forensic Analyzer dashboard.
 *
 * DATA LAYER
 * Every view loads its data through fetchArtifact(endpoint). It tries
 * a real backend first (GET /api/<endpoint>), and only falls back to
 * MOCK_DATA if that request fails — meaning this file does not need to
 * change when Flask is wired in. Just implement the matching route and
 * return a dict shaped like the ones in mock-data.js / the Python
 * reader classes.
 *
 * API endpoints this UI expects once Flask exists:
 *   GET /api/system-info
 *   GET /api/installed-software
 *   GET /api/startup-programs
 *   GET /api/usb-devices
 *   GET /api/user-activity
 *   POST /api/scan/full        -> triggers generate_full_report(), returns combined dict
 * ---------------------------------------------------------------------
 */

const state = {
  currentView: "overview",
  cache: {},          // per-endpoint fetched/mocked data
  consoleLines: [],
  activityFilter: "runmru",
  lastScan: null
};

/* ============================= BOOT SEQUENCE ============================= */

function bootSplash(){
  const bar = document.getElementById("splashProgress");
  const status = document.getElementById("splashStatus");
  const splash = document.getElementById("splash");
  const app = document.getElementById("app");

  let step = 0;
  const total = MOCK_BOOT_LINES.length;

  const tick = () => {
    step++;
    const pct = Math.min(100, Math.round((step / total) * 100));
    bar.style.width = pct + "%";
    if (MOCK_BOOT_LINES[step - 1]) status.textContent = MOCK_BOOT_LINES[step - 1];

    if (step < total) {
      setTimeout(tick, 380);
    } else {
      setTimeout(() => {
        splash.classList.add("hidden");
        app.classList.remove("hidden");
        initApp();
      }, 300);
    }
  };
  setTimeout(tick, 300);
}

/* ============================= DATA LAYER ============================= */

async function fetchArtifact(endpoint){
  if (state.cache[endpoint]) return state.cache[endpoint];

  try {
    const res = await fetch(`/api/${endpoint}`);
    if (!res.ok) throw new Error("bad status " + res.status);
    const data = await res.json();
    state.cache[endpoint] = data;
    logConsole(`GET /api/${endpoint}`, "ok");
    return data;
  } catch (err) {
    // No backend attached yet (or it errored) — use bundled sample data
    // so the UI is fully explorable on its own.
    const data = MOCK_DATA[endpoint];
    state.cache[endpoint] = data;
    logConsole(`/api/${endpoint} unavailable — using sample data`, "warn");
    return data;
  }
}

function invalidateCache(){
  state.cache = {};
}

/* ============================= CONSOLE LOG ============================= */

function logConsole(message, level = "info"){
  const time = new Date().toLocaleTimeString([], { hour12:false });
  state.consoleLines.unshift({ time, message, level });
  renderConsole();
}

function renderConsole(){
  const body = document.getElementById("consoleBody");
  const count = document.getElementById("consoleCount");
  count.textContent = state.consoleLines.length;
  body.innerHTML = state.consoleLines.slice(0, 60).map(l => `
    <div class="console-line ${l.level}">
      <span class="t">${l.time}</span>
      <span class="msg">${escapeHtml(l.message)}</span>
    </div>
  `).join("");
}

/* ============================= NAV / VIEW ROUTING ============================= */

const VIEW_META = {
  "overview":            { title: "Case Overview",       crumb: "Computer\\Overview" },
  "system-info":         { title: "System Information",  crumb: "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" },
  "installed-software":  { title: "Installed Software",  crumb: "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall" },
  "startup-programs":    { title: "Startup Programs",    crumb: "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" },
  "usb-devices":         { title: "USB Devices",         crumb: "HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR" },
  "user-activity":       { title: "User Activity",       crumb: "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer" },
  "full-report":         { title: "Full Report & Export", crumb: "Computer\\Case File" }
};

function setView(view){
  state.currentView = view;
  document.querySelectorAll(".nav-item").forEach(el =>
    el.classList.toggle("active", el.dataset.view === view)
  );
  document.getElementById("viewTitle").textContent = VIEW_META[view].title;
  document.getElementById("pathCrumb").textContent = VIEW_META[view].crumb;
  renderView(view);
}

async function renderView(view){
  const content = document.getElementById("content");
  content.innerHTML = `<div class="panel" style="text-align:center;color:var(--text-faint);font-family:var(--mono);font-size:12px;padding:40px;">Reading registry data…</div>`;

  const renderers = {
    "overview": renderOverview,
    "system-info": renderSystemInfo,
    "installed-software": () => renderTableView({
      endpoint: "installed-software",
      listKey: "software_list",
      countLabel: "programs found",
      searchKeys: ["name", "publisher", "install_location"],
      filters: [
        { label: "All", test: () => true },
        { label: "HKLM", test: r => r.registry_root === "HKLM" },
        { label: "HKCU", test: r => r.registry_root === "HKCU" }
      ],
      columns: [
        { key: "name", label: "Name", class: "cell-strong" },
        { key: "version", label: "Version", class: "cell-mono" },
        { key: "publisher", label: "Publisher" },
        { key: "install_date", label: "Installed", class: "cell-mono" },
        { key: "registry_root", label: "Hive", render: r => tag(r.registry_root, "teal") },
        { key: "registry_view", label: "View", class: "cell-mono" }
      ]
    }),
    "startup-programs": () => renderTableView({
      endpoint: "startup-programs",
      listKey: "startup_programs",
      countLabel: "auto-run entries found",
      searchKeys: ["program_name", "command"],
      filters: [
        { label: "All", test: () => true },
        { label: "All Users", test: r => r.scope === "All Users" },
        { label: "Current User", test: r => r.scope === "Current User" }
      ],
      columns: [
        { key: "program_name", label: "Program", class: "cell-strong" },
        { key: "command", label: "Command", class: "cell-mono" },
        { key: "scope", label: "Scope", render: r => tag(r.scope, r.scope === "All Users" ? "amber" : "teal") },
        { key: "registry_root", label: "Hive", class: "cell-mono" },
        { key: "value_type", label: "Type", class: "cell-mono" }
      ]
    }),
    "usb-devices": () => renderTableView({
      endpoint: "usb-devices",
      listKey: "usb_devices",
      countLabel: "device records found",
      searchKeys: ["device_name", "vendor", "product", "serial_number", "friendly_name"],
      filters: [
        { label: "All", test: () => true },
        { label: "USBSTOR", test: r => r.source === "USBSTOR" },
        { label: "Mounted", test: r => r.source === "MountedDevices" }
      ],
      columns: [
        { key: "friendly_name", label: "Device", class: "cell-strong", render: r => r.friendly_name || r.device_name },
        { key: "vendor", label: "Vendor", render: r => r.vendor || "—" },
        { key: "product", label: "Product", render: r => r.product || "—" },
        { key: "serial_number", label: "Serial", class: "cell-mono", render: r => r.serial_number || "—" },
        { key: "last_write_time", label: "Last Write", class: "cell-mono" },
        { key: "source", label: "Source", render: r => tag(r.source, r.source === "USBSTOR" ? "teal" : "neutral") }
      ]
    }),
    "user-activity": renderUserActivity,
    "full-report": renderFullReport
  };

  const fn = renderers[view];
  await fn();
}

/* ============================= OVERVIEW ============================= */

async function renderOverview(){
  const [sys, sw, startup, usb, activity] = await Promise.all([
    fetchArtifact("system-info"),
    fetchArtifact("installed-software"),
    fetchArtifact("startup-programs"),
    fetchArtifact("usb-devices"),
    fetchArtifact("user-activity")
  ]);

  const cards = [
    { view:"system-info",        icon:iconSystem(),   num: sys.computer_name || "—",           label:"Computer Name" },
    { view:"installed-software", icon:iconSoftware(), num: sw.total_programs,                   label:"Installed Programs" },
    { view:"startup-programs",   icon:iconStartup(),  num: startup.total_startup_programs,      label:"Startup Entries" },
    { view:"usb-devices",        icon:iconUsb(),       num: usb.total_usb_devices,               label:"USB Device Records" },
    { view:"user-activity",      icon:iconActivity(), num:
        activity.runmru_count + activity.typed_paths_count + activity.recent_docs_count + activity.userassist_count,
      label:"Activity Traces" }
  ];

  const content = document.getElementById("content");
  content.innerHTML = `
    <div class="section-fade">
      <div class="stat-grid">
        ${cards.map(c => `
          <div class="stat-card" data-jump="${c.view}">
            <div class="icon">${c.icon}</div>
            <div class="num">${c.num}</div>
            <div class="label">${c.label}</div>
          </div>
        `).join("")}
      </div>

      <div class="panel">
        <div class="panel-head">
          <h3>About this tool</h3>
          <span class="hint">main.py → backend/live_registry/*</span>
        </div>
        <div class="about-grid">
          <p>
            This dashboard reads the Windows Registry the same way the original
            command-line tool does — via <code>winreg</code> — and groups the
            evidence into five artifact categories: system identity, installed
            software, startup persistence, USB device history, and user
            activity traces (Run box, typed paths, recent documents, UserAssist).
          </p>
          <p>
            Every value shown carries the exact registry hive and key path it was
            read from, so nothing here is presented without its source. Click
            <strong>Run Full Scan</strong> to refresh all five artifacts at once,
            or <strong>Export</strong> to save the current case data as JSON/CSV —
            mirroring <code>generate_full_report()</code> in <code>main.py</code>.
          </p>
        </div>
      </div>

      <div class="panel" style="margin-bottom:0;">
        <div class="panel-head">
          <h3>Current session</h3>
        </div>
        <div class="kv-grid">
          <div class="kv-cell"><div class="k">Tool Mode</div><div class="v">${sys.tool_mode}</div></div>
          <div class="kv-cell"><div class="k">Admin Status</div><div class="v">${sys.admin_status ? "Elevated" : "Standard User"}</div></div>
          <div class="kv-cell"><div class="k">Windows Edition</div><div class="v">${sys.windows_info.product_name} (${sys.windows_info.display_version})</div></div>
          <div class="kv-cell"><div class="k">Current User</div><div class="v">${sys.user_info.username}</div></div>
        </div>
      </div>
    </div>
  `;

  content.querySelectorAll("[data-jump]").forEach(el => {
    el.addEventListener("click", () => setView(el.dataset.jump));
  });
}

/* ============================= SYSTEM INFO ============================= */

async function renderSystemInfo(){
  const data = await fetchArtifact("system-info");
  const content = document.getElementById("content");

  const rows = [
    ["Admin Status", data.admin_status ? "Elevated (Administrator)" : "Standard User"],
    ["Computer Name", data.computer_name],
    ["Architecture", data.architecture],
    ["Machine", data.machine],
    ["Processor", data.processor]
  ];
  const win = data.windows_info;
  const winRows = [
    ["Product Name", win.product_name], ["Display Version", win.display_version],
    ["Build Number", win.current_build], ["UBR", win.ubr],
    ["Edition ID", win.edition_id], ["Install Date", win.install_date],
    ["System Root", win.system_root]
  ];
  const userRows = [
    ["Username", data.user_info.username], ["User Domain", data.user_info.user_domain],
    ["User Profile", data.user_info.user_profile]
  ];
  const tzRows = [
    ["Time Zone", data.timezone_info.time_zone], ["Standard Name", data.timezone_info.standard_name]
  ];

  const section = (title, hint, rows) => `
    <div class="panel">
      <div class="panel-head"><h3>${title}</h3><span class="hint">${hint}</span></div>
      <div class="kv-grid">
        ${rows.map(([k,v]) => `<div class="kv-cell"><div class="k">${k}</div><div class="v">${v ?? "—"}</div></div>`).join("")}
      </div>
    </div>
  `;

  content.innerHTML = `
    <div class="section-fade">
      ${section("Host", "HKLM\\SYSTEM\\CurrentControlSet\\Control\\ComputerName", rows)}
      ${section("Windows Version", "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", winRows)}
      ${section("Current User", "Environment", userRows)}
      ${section("Timezone", "HKLM\\SYSTEM\\CurrentControlSet\\Control\\TimeZoneInformation", tzRows)}
    </div>
  `;
}

/* ============================= GENERIC TABLE VIEW ============================= */
/* Used for Installed Software, Startup Programs, USB Devices */

async function renderTableView(cfg){
  const data = await fetchArtifact(cfg.endpoint);
  const rows = data[cfg.listKey] || [];
  let filterIndex = 0;
  let query = "";

  const content = document.getElementById("content");

  const draw = () => {
    const filtered = rows
      .filter(cfg.filters[filterIndex].test)
      .filter(r => {
        if (!query) return true;
        const q = query.toLowerCase();
        return cfg.searchKeys.some(k => String(r[k] ?? "").toLowerCase().includes(q));
      });

    content.innerHTML = `
      <div class="section-fade">
        <div class="view-toolbar">
          <div class="search-box">
            <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
            <input type="text" id="tableSearch" placeholder="Search ${cfg.countLabel}…" value="${escapeHtml(query)}">
          </div>
          <div class="filter-pills">
            ${cfg.filters.map((f,i) => `<button class="filter-pill ${i===filterIndex?"active":""}" data-i="${i}">${f.label}</button>`).join("")}
          </div>
          <div class="result-count">${filtered.length} / ${rows.length} ${cfg.countLabel}</div>
        </div>

        <div class="table-wrap">
          <table>
            <thead><tr>${cfg.columns.map(c => `<th>${c.label}</th>`).join("")}</tr></thead>
            <tbody>
              ${filtered.length ? filtered.map((r, idx) => `
                <tr data-idx="${idx}">
                  ${cfg.columns.map(c => `<td class="${c.class||""}">${c.render ? c.render(r) : escapeHtml(r[c.key] ?? "—")}</td>`).join("")}
                </tr>
              `).join("") : `<tr class="empty-row"><td colspan="${cfg.columns.length}">No matching evidence for this filter.</td></tr>`}
            </tbody>
          </table>
        </div>
      </div>
    `;

    content.querySelector("#tableSearch").addEventListener("input", e => {
      query = e.target.value;
      draw();
      content.querySelector("#tableSearch").focus();
      const val = content.querySelector("#tableSearch").value;
      content.querySelector("#tableSearch").setSelectionRange(val.length, val.length);
    });
    content.querySelectorAll(".filter-pill").forEach(btn => {
      btn.addEventListener("click", () => { filterIndex = Number(btn.dataset.i); draw(); });
    });
    content.querySelectorAll("tbody tr[data-idx]").forEach(tr => {
      tr.addEventListener("click", () => openModal(filtered[Number(tr.dataset.idx)]));
    });
  };

  draw();
}

/* ============================= USER ACTIVITY (sub-tabbed) ============================= */

async function renderUserActivity(){
  const data = await fetchArtifact("user-activity");
  const content = document.getElementById("content");

  const tabs = [
    { key: "runmru",      label: "Run Box (RunMRU)", count: data.runmru_count,
      columns: [
        { key: "command", label: "Command", class:"cell-strong" },
        { key: "command_name", label: "MRU Key", class:"cell-mono" },
        { key: "registry_path", label: "Registry Path", render: r => regpath("HKCU", r.registry_path) }
      ], rows: data.runmru },
    { key: "typed_paths", label: "Typed Paths", count: data.typed_paths_count,
      columns: [
        { key: "typed_path", label: "Path", class:"cell-strong" },
        { key: "value_name", label: "Value", class:"cell-mono" },
        { key: "registry_path", label: "Registry Path", render: r => regpath("HKCU", r.registry_path) }
      ], rows: data.typed_paths },
    { key: "recent_docs", label: "Recent Documents", count: data.recent_docs_count,
      columns: [
        { key: "recent_item", label: "Item", class:"cell-strong" },
        { key: "category", label: "Category", render: r => tag(r.category, "neutral") },
        { key: "registry_path", label: "Registry Path", render: r => regpath("HKCU", r.registry_path) }
      ], rows: data.recent_docs },
    { key: "userassist", label: "UserAssist", count: data.userassist_count,
      columns: [
        { key: "decoded_name", label: "Program (decoded)", class:"cell-strong" },
        { key: "encoded_name", label: "ROT13 Raw", class:"cell-mono" },
        { key: "guid", label: "GUID", class:"cell-mono" }
      ], rows: data.userassist }
  ];

  let active = state.activityFilter;
  let query = "";

  const draw = () => {
    const tab = tabs.find(t => t.key === active);
    const rows = tab.rows.filter(r => {
      if (!query) return true;
      const q = query.toLowerCase();
      return Object.values(r).some(v => String(v ?? "").toLowerCase().includes(q));
    });

    content.innerHTML = `
      <div class="section-fade">
        <div class="subtabs">
          ${tabs.map(t => `
            <button class="subtab ${t.key===active?"active":""}" data-key="${t.key}">
              ${t.label} <span class="count">${t.count}</span>
            </button>
          `).join("")}
        </div>

        <div class="view-toolbar">
          <div class="search-box">
            <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
            <input type="text" id="actSearch" placeholder="Search ${tab.label.toLowerCase()}…" value="${escapeHtml(query)}">
          </div>
          <div class="result-count">${rows.length} / ${tab.rows.length} entries</div>
        </div>

        <div class="table-wrap">
          <table>
            <thead><tr>${tab.columns.map(c => `<th>${c.label}</th>`).join("")}</tr></thead>
            <tbody>
              ${rows.length ? rows.map((r, idx) => `
                <tr data-idx="${idx}">
                  ${tab.columns.map(c => `<td class="${c.class||""}">${c.render ? c.render(r) : escapeHtml(r[c.key] ?? "—")}</td>`).join("")}
                </tr>
              `).join("") : `<tr class="empty-row"><td colspan="${tab.columns.length}">No entries found for this artifact.</td></tr>`}
            </tbody>
          </table>
        </div>
      </div>
    `;

    content.querySelectorAll(".subtab").forEach(btn => {
      btn.addEventListener("click", () => {
        active = btn.dataset.key;
        state.activityFilter = active;
        query = "";
        draw();
      });
    });
    content.querySelector("#actSearch").addEventListener("input", e => {
      query = e.target.value;
      draw();
      const el = content.querySelector("#actSearch");
      el.focus();
      el.setSelectionRange(query.length, query.length);
    });
    content.querySelectorAll("tbody tr[data-idx]").forEach(tr => {
      tr.addEventListener("click", () => openModal(rows[Number(tr.dataset.idx)]));
    });
  };

  draw();
}

/* ============================= FULL REPORT ============================= */

async function renderFullReport(){
  const content = document.getElementById("content");
  const items = [
    { icon: iconSystem(), title: "System Information", desc: "Windows version, computer identity, timezone, and current user context." },
    { icon: iconSoftware(), title: "Installed Software", desc: "All programs found across 64-bit, 32-bit, and per-user Uninstall keys." },
    { icon: iconStartup(), title: "Startup Programs", desc: "Auto-run entries from HKLM and HKCU Run keys, all-user and per-user scope." },
    { icon: iconUsb(), title: "USB Devices", desc: "USBSTOR device history plus MountedDevices drive-letter mappings." },
    { icon: iconActivity(), title: "User Activity", desc: "RunMRU, TypedPaths, RecentDocs, and decoded UserAssist execution traces." }
  ];

  content.innerHTML = `
    <div class="section-fade">
      <div class="panel">
        <div class="panel-head">
          <h3>Report contents</h3>
          <span class="hint">generate_full_report()</span>
        </div>
        <div class="report-grid">
          ${items.map(i => `
            <div class="report-card">
              <div class="icon">${i.icon}</div>
              <div><h4>${i.title}</h4><p>${i.desc}</p></div>
            </div>
          `).join("")}
        </div>
        <div class="report-actions">
          <button class="btn btn-primary" id="reportJson">
            <svg viewBox="0 0 24 24"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>
            Download JSON
          </button>
          <button class="btn btn-ghost" id="reportCsv">
            <svg viewBox="0 0 24 24"><path d="M4 4h16v16H4z"/><path d="M4 9h16M9 4v16"/></svg>
            Download CSV bundle notes
          </button>
        </div>
      </div>

      <div class="panel" style="margin-bottom:0;">
        <div class="panel-head"><h3>Last scan</h3></div>
        <div class="kv-grid">
          <div class="kv-cell"><div class="k">Scan Time</div><div class="v">${state.lastScan || "No scan run this session"}</div></div>
          <div class="kv-cell"><div class="k">Artifacts Collected</div><div class="v">5 / 5</div></div>
        </div>
      </div>
    </div>
  `;

  document.getElementById("reportJson").addEventListener("click", downloadFullReportJson);
  document.getElementById("reportCsv").addEventListener("click", () => {
    logConsole("CSV export happens per-artifact on the backend (csv_export.py) — wire this button to /api/scan/full then save_all_csv_reports().", "info");
  });
}

async function downloadFullReportJson(){
  const [system_info, installed_software, startup_programs, usb_devices, user_activity] = await Promise.all([
    fetchArtifact("system-info"), fetchArtifact("installed-software"),
    fetchArtifact("startup-programs"), fetchArtifact("usb-devices"), fetchArtifact("user-activity")
  ]);
  const report = {
    tool_name: "Portable Windows Registry Forensic Analyzer",
    tool_mode: "Live Registry Analysis",
    scan_time: state.lastScan || new Date().toISOString(),
    system_info, installed_software, startup_programs, usb_devices, user_activity
  };
  const blob = new Blob([JSON.stringify(report, null, 4)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `registry_scan_report_${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
  logConsole("Saved registry_scan_report_*.json", "ok");
}

/* ============================= FULL SCAN ============================= */

async function runFullScan(){
  const btn = document.getElementById("scanBtn");
  btn.disabled = true;
  const original = btn.innerHTML;
  btn.innerHTML = `<svg viewBox="0 0 24 24"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 4v6h-6"/></svg> Scanning…`;

  logConsole("Full Registry Scan Started", "info");
  invalidateCache();

  const steps = [
    ["Collecting system information…", "system-info"],
    ["Collecting installed software…", "installed-software"],
    ["Collecting startup programs…", "startup-programs"],
    ["Collecting USB devices…", "usb-devices"],
    ["Collecting user activity…", "user-activity"]
  ];

  // Try the real backend's combined scan endpoint first — this is the one
  // that actually calls generate_full_report()-equivalent logic and saves
  // JSON/CSV to output/ via JSONExport / CSVExport on the server.
  let usedServerScan = false;
  try {
    for (const [label] of steps) logConsole(label, "info");
    const res = await fetch("/api/scan/full", { method: "POST" });
    if (!res.ok) throw new Error("bad status " + res.status);
    const data = await res.json();

    state.cache["system-info"] = data.report.system_info;
    state.cache["installed-software"] = data.report.installed_software;
    state.cache["startup-programs"] = data.report.startup_programs;
    state.cache["usb-devices"] = data.report.usb_devices;
    state.cache["user-activity"] = data.report.user_activity;

    logConsole(data.json_export?.message || "JSON report saved", "ok");
    (data.csv_exports || []).forEach(r => logConsole(`${r.message} -> ${r.file_path}`, "ok"));
    usedServerScan = true;
  } catch (err) {
    logConsole("/api/scan/full unavailable — falling back to per-artifact fetch", "warn");
  }

  if (!usedServerScan){
    for (const [label, endpoint] of steps){
      await fetchArtifact(endpoint);
      await new Promise(r => setTimeout(r, 180));
    }
  }

  state.lastScan = new Date().toLocaleString();
  document.getElementById("scanClock").textContent = `Last scan: ${state.lastScan}`;
  logConsole("Full report generation completed successfully.", "ok");

  btn.disabled = false;
  btn.innerHTML = original;

  renderView(state.currentView);
  document.getElementById("console").classList.add("open");
}

/* ============================= MODAL ============================= */

function openModal(record){
  const backdrop = document.getElementById("modalBackdrop");
  const body = document.getElementById("modalBody");
  body.innerHTML = Object.entries(record).map(([k,v]) => `
    <div class="modal-row">
      <div class="k">${k.replace(/_/g," ")}</div>
      <div class="v">${escapeHtml(v ?? "—")}</div>
    </div>
  `).join("");
  backdrop.classList.add("open");
}
function closeModal(){ document.getElementById("modalBackdrop").classList.remove("open"); }

/* ============================= SMALL HELPERS ============================= */

function tag(text, kind){ return `<span class="tag tag-${kind}">${escapeHtml(text)}</span>`; }
function regpath(hive, path){
  return `<span class="regpath trunc"><span class="hive">${hive}</span>\\${escapeHtml(path)}</span>`;
}
function escapeHtml(str){
  return String(str).replace(/[&<>"']/g, m => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[m]));
}

/* Inline icon set (no external assets / CDN needed) */
function iconSystem(){ return `<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/></svg>`; }
function iconSoftware(){ return `<svg viewBox="0 0 24 24"><path d="M4 4h16v16H4z"/><path d="M4 9h16M9 4v5"/></svg>`; }
function iconStartup(){ return `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>`; }
function iconUsb(){ return `<svg viewBox="0 0 24 24"><path d="M12 3v7M9 6l3-3 3 3M8 13h8l2 3-2 3H8l-2-3z"/></svg>`; }
function iconActivity(){ return `<svg viewBox="0 0 24 24"><path d="M4 19V5a2 2 0 0 1 2-2h9l5 5v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><path d="M8 11h8M8 15h5"/></svg>`; }

/* ============================= INIT ============================= */

function initApp(){
  document.querySelectorAll(".nav-item").forEach(btn => {
    btn.addEventListener("click", () => setView(btn.dataset.view));
  });

  document.getElementById("scanBtn").addEventListener("click", runFullScan);
  document.getElementById("exportBtn").addEventListener("click", downloadFullReportJson);
  document.getElementById("consoleToggle").addEventListener("click", () => {
    document.getElementById("console").classList.toggle("open");
  });
  document.getElementById("modalClose").addEventListener("click", closeModal);
  document.getElementById("modalBackdrop").addEventListener("click", e => {
    if (e.target.id === "modalBackdrop") closeModal();
  });

  // Admin privilege pill — reflects system_info.admin_status once loaded
  fetchArtifact("system-info").then(data => {
    const pill = document.getElementById("adminPill");
    const text = document.getElementById("adminPillText");
    if (data.admin_status){
      pill.classList.add("ok");
      text.textContent = "Running elevated (Administrator)";
    } else {
      pill.classList.add("warn");
      text.textContent = "Standard user — some artifacts limited";
    }
  });

  if (document.body.dataset.mode === "dev") {
    document.getElementById("devBanner").style.display = "block";
    logConsole("Backend running in dev/mock mode (non-Windows) — sample data only.", "warn");
  }

  MOCK_BOOT_LINES.forEach(l => logConsole(l, "info"));
  setView("overview");
}

document.addEventListener("DOMContentLoaded", bootSplash);
