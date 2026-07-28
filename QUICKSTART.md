# WorkLogger Quick Start

## 1. Install once

WorkLogger is tested as a Windows desktop-local application. Install Python 3.10–3.12, then run:

```powershell
cd E:\path\to\worklogger
.\setup.bat
```

The script creates `.venv`, installs `requirements.txt`, and verifies the installation.

## 2. Start

```powershell
.\run.bat
```

Open `http://127.0.0.1:8000` if the browser does not open automatically. Stop the app with `Ctrl+C` in the terminal window.

## 3. First structure

In **Today**, open **Manage Projects & Goals** and build only the structure you need:

1. Create a Project.
2. Add an Annual Goal beneath it.
3. Add the current Monthly Goal.
4. Add this week's Weekly Goal when needed.

You do not need to pre-create a large hierarchy. Monthly goals are usually stable; weekly goals are intended for more frequent changes.

## 4. Daily task flow

1. Enter a task title in **Quick add**.
2. Keep the default `Normal` priority.
3. Optionally search a Protocol title, create a copy, or choose `+ Create new Protocol`.
4. Add the task.

Tasks without a goal are `Unclassified`. Later, select tasks and assign them to a Weekly Goal. The application fills the parent hierarchy and changes their work status to `Planned`.

## 5. Protocol flow

Open **Protocols** when you need to create, copy, or maintain a reusable procedure.

- `Quick Edit` has only Title, Status, and Progress note.
- Use the Protocol editor body for procedure text, images, results, and conclusion.
- Duplicate a similar Protocol for a new experimental run; the copy opens after the task is saved.

## 6. Review

- Use **Reports** for weekly/monthly review and Excel/PDF export.
- Use **Gantt** for a visual check of dated goals. It supports year and month views, plus high-resolution PNG export. In Year view choose all projects or a single Project; Month view always exports the full current month.
- Archive finished projects or goals in **Manage Projects & Goals** instead of deleting their history.

## Troubleshooting

### `run.bat` says the environment is missing

Run `setup.bat` again from the project folder.

### Port 8000 is already in use

Stop the other local WorkLogger server, or run the development command with a different `--port` and open that port in the browser.

### The browser shows old static UI

Use `Ctrl+Shift+R` to force-refresh the page.

### Database safety

Stop WorkLogger before copying, replacing, or restoring `data/worklogger.db`.

For fuller workflows, see [USER_GUIDE_ZH.md](USER_GUIDE_ZH.md).
