# WorkLogger Manual Regression Checklist

Run this checklist before committing a feature that changes the local app. Use disposable test data where a step creates or deletes records.

## Preparation

1. Run `.\setup.bat` if the environment is missing.
2. Start with `.\run.bat` or the development Uvicorn command.
3. Open `http://127.0.0.1:8000` and use `Ctrl+Shift+R` after static frontend changes.

## Today and tasks

- [ ] Create a Quick add task; it defaults to `Normal` and `Unclassified`.
- [ ] Search and link an existing Protocol by title.
- [ ] Create a task with `Create a copy`; confirm the task saves before the copied Protocol opens.
- [ ] Create a task with `+ Create new Protocol`; confirm a new Protocol opens after task save.
- [ ] Enter Select tasks mode; clicking a task row selects it and does not open edit.
- [ ] Assign selected tasks through a current-week chip and through a Week in Manage.
- [ ] Confirm assigned tasks become `Planned` and carry parent hierarchy links.
- [ ] In Select tasks mode, use one delete button and confirm it targets the selected set only after confirmation.
- [ ] Verify an unlinked task remains discoverable with All time + Unclassified.

## Manage Projects & Goals

- [ ] Create a Project, Annual Goal, Monthly Goal, and Weekly Goal from their contextual `+` actions.
- [ ] Archive each supported node type and verify it disappears from default selectors.
- [ ] Enable Include archived and verify Restore works.
- [ ] Verify Delete is unavailable or rejected for nodes with children, tasks, or history.

## Protocols

- [ ] Protocol navigation and headings use `Protocol` / `Protocols`, not user-facing `Experiment` labels.
- [ ] New Protocol opens with the Quick Edit fields: Protocol Title, Status, Progress note.
- [ ] Quick Edit contains no Hypothesis, Methodology, Results, Conclusion, or Custom Tags fields.
- [ ] Save a Progress note and Status; reopen Quick Edit to confirm persistence.
- [ ] Edit rich text and insert an image in the Protocol body; save and reload.
- [ ] Duplicate a Protocol and verify source content is retained in the copy.

## Reports and exports

- [ ] Open a Weekly Report task and edit it inline without leaving Reports.
- [ ] Click a linked Protocol and confirm it opens in a new tab.
- [ ] Export a report as Excel and confirm the file opens in Excel.
- [ ] Export a report as PDF and confirm the file renders.

## Gantt

- [ ] Year view renders January–December and one continuous 52- or 53-week header row.
- [ ] A 53-week year places `53` at the end of the week row, never underneath Week 1.
- [ ] Project and Annual Goal rows on the left match the corresponding timeline heights on the right.
- [ ] Month view renders dated Weekly Goals and handles overlap lanes.

## Technical smoke checks

- [ ] Browser console has no uncaught errors while loading Today, Protocols, Reports, and Gantt.
- [ ] `python verify_setup.py` passes inside `.venv`.
- [ ] SQLite data remains in `data/worklogger.db` and is not staged by `git status`.
- [ ] `git diff --check` reports no whitespace errors before commit.
