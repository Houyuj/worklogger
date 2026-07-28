# WorkLogger Project Summary

Updated: 2026-07-28

## Purpose

WorkLogger gives an individual research lead one local workspace for three connected concerns:

1. planning research work across Project, Annual, Monthly, and Weekly goals;
2. capturing and progressing daily tasks without friction; and
3. maintaining reusable Protocols and research records close to the tasks that use them.

## Product model

| Term | Meaning |
| --- | --- |
| Project | A durable research programme or workstream. |
| Annual Goal | A yearly research direction inside a Project. |
| Monthly Goal | A time-bounded monthly deliverable inside an Annual Goal. |
| Weekly Goal | A high-frequency work commitment inside a Monthly Goal. |
| Task | A dated action item. It is `Unclassified` until assigned to a goal. |
| Protocol | A reusable experimental procedure, recurring process, or research record. |

## Architecture

```text
frontend/              Vanilla HTML, CSS, JavaScript
  dashboard.html       Today, task capture, selection, and Manage tree
  experiments.html     User-facing Protocol list and Quick Edit
  experiment-detail.html  Rich-text Protocol editor
  reports.html         Review and exports
  gantt.html           Year/month timeline
backend/               FastAPI + SQLAlchemy
data/worklogger.db     Local SQLite data (ignored by Git)
launcher.py            Local server/browser launcher
setup.bat / run.bat    Windows setup and run entry points
```

The HTTP API and SQLite schema retain legacy `experiment` names for backwards compatibility. The product and user documentation call the record a **Protocol**.

## Key design choices

- Personal-first and desktop-first; no account or team UI.
- English product UI; Chinese product discussion and user guide are supported.
- Fast capture first, classification later.
- A Protocol is linked by title search instead of a mandatory category taxonomy.
- Protocol content is a single rich-text body rather than fragmented result fields.
- Archive preserves research history; delete protects populated planning nodes.
- Excel is the primary editable report handoff; PDF remains for read-only sharing.
- Gantt can export a standalone high-resolution PNG for a full year, one Project, or the full current month.

## Current version-control practice

- `main` is the local working branch.
- Code and documentation are tracked.
- SQLite databases, backups, `.venv`, logs, and local test artifacts are ignored.
- Use a commit after each verified change set; do not put research data in Git.

## Runtime dependencies

Pinned runtime dependencies are listed in `requirements.txt`:

- FastAPI / Uvicorn
- SQLAlchemy / Pydantic
- openpyxl, ReportLab, and python-docx for exports

## Start locally

```powershell
.\setup.bat
.\run.bat
```

See [README.md](README.md) for an overview, [QUICKSTART.md](QUICKSTART.md) for setup, and [USER_GUIDE_ZH.md](USER_GUIDE_ZH.md) for the research workflow.
