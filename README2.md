# Windows Registry Forensic Analyzer — Flask Edition

This turns the original CLI tool (`main.py`) into a local web app: same
registry-reading logic, now served through Flask with the dashboard UI
you already saw, instead of a terminal menu.

## Project structure

```
wrfa-flask/
├── app.py                       Flask app — routes + server startup
├── main.py                      Original CLI menu (still works standalone, untouched)
├── requirements.txt             python-registry, flask
│
├── backend/                     Same package as the original repo
│   ├── live_registry/            Live registry readers (winreg) — Windows only
│   │   ├── common_reader.py
│   │   ├── system_info.py
│   │   ├── installed_software.py
│   │   ├── startup_programs.py
│   │   ├── usb_devices.py
│   │   └── user_activity.py
│   ├── mock/                     NEW: dev-mode readers, same method names/shapes
│   │   └── mock_readers.py        used automatically when NOT running on Windows
│   ├── registry_parser/          Offline hive parser (python-registry) — not wired to routes yet
│   └── reports/                  JSON/CSV export, unchanged
│       ├── json_export.py
│       └── csv_export.py
│
├── templates/
│   └── index.html                Dashboard page (Jinja: url_for() for static assets)
│
├── static/                       Everything the browser loads directly
│   ├── css/styles.css
│   ├── js/
│   │   ├── app.js                 View rendering, search/filter, scan, modal
│   │   └── mock-data.js           Client-side fallback sample data (used only if /api/* is unreachable)
│   └── assets/favicon.svg
│
└── output/                       Where JSON/CSV reports get saved (created automatically)
```

### Why `backend/mock/`

`winreg` (and therefore every reader in `backend/live_registry/`) only
exists on Windows. `app.py` checks the platform at startup:

```python
if IS_WINDOWS:
    from backend.live_registry.system_info import SystemInfoReader   # real data
else:
    from backend.mock.mock_readers import SystemInfoReader           # sample data
```

Both classes expose the exact same method names and return the exact same
dict shapes, so every route in `app.py` works unchanged either way. This
means you can build and test the whole app (routes, UI, exports) on
Linux/Mac, then just run it on Windows for live registry data — nothing
in the code has to change, it switches itself automatically.

The dashboard shows an amber banner when it's running in dev/mock mode, so
it's never ambiguous which mode you're looking at.

## Routes

| Method | Route                              | What it does |
|--------|-------------------------------------|--------------|
| GET    | `/`                                  | Renders the dashboard |
| GET    | `/api/system-info`                   | `SystemInfoReader().get_system_info()` |
| GET    | `/api/installed-software`            | `InstalledSoftwareReader().get_installed_software()` |
| GET    | `/api/startup-programs`              | `StartupProgramsReader().get_startup_programs()` |
| GET    | `/api/usb-devices`                   | `USBDevicesReader().read_usb_devices()` |
| GET    | `/api/user-activity`                 | `UserActivityReader().get_user_activity()` |
| POST   | `/api/scan/full`                     | Runs all 5, saves JSON+CSV to `output/` (same as `generate_full_report()`), returns everything as JSON |
| GET    | `/api/export/download/<filename>`    | Downloads a previously saved file from `output/` |

## Running it

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000**.

- On Windows: real registry data. USB devices and some startup entries
  need the terminal/IDE running **as Administrator**, same limitation
  the original CLI tool already has.
- On Linux/Mac: runs fine in mock mode for development — you'll see the
  dev-mode banner and sample data, and `/api/scan/full` still exercises
  the real JSON/CSV export code with that sample data.

## What changed vs. the original repo

- Nothing in `backend/live_registry/*` or `backend/reports/*` was modified —
  same classes, same method names, same return shapes.
- `main.py` (the CLI) is untouched and still runs standalone if you want it.
- Added: `app.py`, `backend/mock/`, `templates/`, `static/`.
- Fixed a filename typo: `backend/registry_parser/init_.py` → `__init__.py`.

## Next steps you might want

- Wire `backend/registry_parser/hive_loader.py` (offline `.dat` hive
  parsing) into its own routes, e.g. `/api/offline/load` + `/api/offline/keys`,
  for analyzing a copied `NTUSER.DAT` instead of the live registry.
- Swap Flask's built-in dev server for a production one (waitress on
  Windows works well) before packaging this into the `.exe` build.
- Add basic auth or a local-only bind if this ever needs to run somewhere
  more than your own machine, since it currently has no access control.
