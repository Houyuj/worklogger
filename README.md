# WorkLogger

WorkLogger is a desktop-first personal research workbench for managing several research projects, their goals, day-to-day tasks, and reusable Protocols. It runs locally in a browser and stores data in a local SQLite database.

The interface is English-first. This repository's Chinese user guide is available in [USER_GUIDE_ZH.md](USER_GUIDE_ZH.md).

## What it does today

- Organizes work as **Project → Annual Goal → Monthly Goal → Weekly Goal**.
- Captures a simple task quickly, with `Normal` priority and `Unclassified` status by default.
- Lets you select several tasks and assign them to a Weekly Goal in one action.
- Uses **Protocols** for experiments, repeated procedures, and research records.
- Creates a Protocol copy from an existing title, then opens the copy for editing after the task is saved.
- Keeps Protocol content, images, results, and conclusions in one rich-text body.
- Provides a compact **Manage Projects & Goals** tree with contextual creation, archive, restore, and safe deletion rules.
- Provides weekly, monthly, and annual reports with Excel and PDF export; linked Protocols open in a new tab from Reports.
- Provides a year/month Gantt view with 52- or 53-week ISO headers and synchronized goal/timeline row heights.

## What it deliberately does not do

- No accounts, roles, shared workspaces, or collaboration screens.
- No mobile-first layout.
- No separate inbox: tasks without a goal use the `Unclassified` work status instead.
- No separate task-result field: results belong in the linked Protocol body.

## Run on Windows

### Prerequisites

- Python 3.10, 3.11, or 3.12
- Windows PowerShell or Command Prompt

### First-time setup

```powershell
cd E:\path\to\worklogger
.\setup.bat
```

`setup.bat` creates `.venv`, installs the pinned dependencies from `requirements.txt`, and runs `verify_setup.py`.

### Start the app

```powershell
.\run.bat
```

The launcher starts the local server at `http://127.0.0.1:8000` and opens the app. Press `Ctrl+C` in the launcher window to stop it.

For development, the equivalent command is:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

## Main workflows

### Capture and classify work

1. In **Today**, enter a task title and date.
2. Optionally link a Protocol:
   - search by Protocol title;
   - choose an existing Protocol;
   - choose `Create a copy`; or
   - choose `+ Create new Protocol`.
3. Add the task. A task without a goal remains `Unclassified`.
4. Use **Select tasks** to select one or more rows, then click a current-week goal chip or a Week in **Manage Projects & Goals**. Assigned tasks become `Planned` automatically.

### Manage the research hierarchy

Open **Manage Projects & Goals** in Today. Create each child where it belongs:

- `+ New Project`
- `+ Annual`
- `+ Month`
- `+ Week`

Archive preserves history and can be restored through **Include archived**. Delete is only available for empty nodes, protecting project history.

### Work with Protocols

Open **Protocols** from the top navigation.

- **Quick Edit** contains exactly: `Protocol Title`, `Status`, and `Progress note`.
- The Protocol editor is the single place for the procedure, research log, images, results, and conclusions.
- `Duplicate` creates a copy for a new run while retaining the source Protocol.

### Review and export

- **Reports** supports weekly, monthly, and annual review, inline task editing, Protocol links, Excel export, and PDF export.
- **Gantt** supports year and month views. Its bars represent dated monthly goals or weekly goals, not a hard deadline system.

## Data and backups

Local data lives in `data/worklogger.db`. It is intentionally ignored by Git, as are backups and virtual environments.

Before a manual database operation, stop the application and copy the database:

```powershell
Copy-Item .\data\worklogger.db .\data\worklogger.db.backup
```

To restore, stop WorkLogger and replace `data/worklogger.db` with a known-good copy.

## Repository hygiene

The repository tracks application code and documentation. It ignores:

- `.venv/`
- `data/*.db`, journals, and database backups
- `backups/`
- logs and local test artifacts

Use small commits after a verified feature or fix. Do not commit personal research data.

## Technical stack

- FastAPI + Uvicorn
- SQLAlchemy + SQLite
- Vanilla HTML, CSS, and JavaScript
- openpyxl for Excel exports
- ReportLab for PDF exports
- python-docx for Word exports

See [QUICKSTART.md](QUICKSTART.md), [USER_GUIDE_ZH.md](USER_GUIDE_ZH.md), [TESTING.md](TESTING.md), and [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for operational detail.
