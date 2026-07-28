# WorkLogger Implementation Status

Updated: 2026-07-29

## Current product scope

WorkLogger is a local, desktop-first personal research manager. The product supports password-free local user profiles with fully isolated databases. It does not implement authentication, permissions, team workflows, or collaboration screens.

## Implemented

### Today and task flow

- Quick task creation with date, `Normal` priority, and `Unclassified` default status.
- Styled Protocol picker with title search, direct linking, copying, and `+ Create new Protocol`.
- Save-first Protocol-copy flow: task is saved before the copy opens for editing.
- Task editing, completion, deletion, filtering, and all-time search.
- Batch task selection: click a row to select; assign selected tasks to a current Week or a Week in Manage.
- Batch deletion with explicit confirmation.
- A task assigned to Annual, Monthly, or Weekly Goal becomes `Planned`; unassigned tasks remain `Unclassified`.

### Planning hierarchy and safety

- Project → Annual Goal → Monthly Goal → Weekly Goal hierarchy.
- Compact contextual tree creation from Manage Projects & Goals.
- Archive / restore for projects and goals, with `Include archived` discovery.
- Delete protection for populated nodes; only unused empty nodes can be deleted.
- Parent relationships resolved automatically when a specific goal is assigned.

### Protocols

- User-facing terminology is **Protocol** throughout the interface.
- Protocol list, title search, duplication, task association, and rich-text editor.
- Quick Edit has exactly Title, Status, and Progress note.
- Procedure, images, notes, results, and conclusion live in the Protocol body.
- Current task UI supports one main Protocol to reduce incorrect associations.
- Legacy internal endpoints and table names retain `experiment` for existing-data compatibility; this is not exposed as the product term.

### Reports and exports

- Weekly, monthly, and annual reports.
- Inline report task editing without navigating to Today.
- Direct Protocol links open in a new tab.
- Excel and PDF exports; Word export remains available for daily reports.

### Gantt

- Year and month views.
- Overlapping bars receive separate lanes.
- Dynamic 52/53-week ISO year header.
- Timeline header, left labels, and paired goal rows are height-synchronized.
- Presentation-ready 16:9 high-resolution PNG export with visible ISO-week ticks and a status legend.
- Smart Year range crops empty leading/trailing months and can be disabled for January–December; Year supports all Projects or one Project, while Month exports the full current month.

### Runtime and data

- FastAPI API serving static frontend files.
- One isolated SQLite database per local user, selected on every API request.
- User creation, switching, database export, retained-database deletion flow, and database merging/import.
- Protocol title conflict handling during import: append the source user name and, if necessary, a number.
- Startup schema additions are applied to every active user database.
- Windows setup and launcher scripts using a local `.venv`.
- Local data, backups, logs, and virtual environments are ignored by Git.

## Deliberately deferred

- Password authentication, permissions, and collaboration UI.
- Mobile layout.
- Automatic task outcome extraction from Protocol body.
- Global keyboard shortcuts while planning semantics are still evolving.
- Forced hard deadlines or automatic overdue status.

## Verification completed in this local build

- Dashboard Protocol picker and task-selection interactions.
- Quick Edit field set: Title, Status, Progress note only.
- Gantt 53-week header and left/right row alignment.
- User switching and empty-database isolation through the live interface.
- Full hierarchy/database merge with Protocol collision renaming and retained database handling.
- Frontend JavaScript syntax checks for all HTML pages.

See [TESTING.md](TESTING.md) for the current manual regression checklist.
