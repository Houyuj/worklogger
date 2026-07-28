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
- [ ] Export a report as Excel and confirm the file opens in Excel and belongs to the selected user.
- [ ] Export a report as PDF and confirm the file renders.

## Gantt

- [ ] Year view renders January–December and one continuous 52- or 53-week header row.
- [ ] A 53-week year places `53` at the end of the week row, never underneath Week 1.
- [ ] Project and Annual Goal rows on the left match the corresponding timeline heights on the right.
- [ ] Month view renders dated Weekly Goals and handles overlap lanes.
- [ ] Year view Export PNG offers All projects and individual Project choices; both downloads include complete, unscrolled content.
- [ ] Smart range crops empty leading and trailing months; disabling it restores the full January–December range.
- [ ] Year export contains visible ISO-week ticks and the five-item status legend.
- [ ] Exported PNG is a readable 16:9 image at 3840 × 2160 output resolution.
- [ ] Month view Export PNG is locked to Full month (all projects) and downloads a complete current-month image.

## Local users and databases

- [ ] Create an empty user and confirm Today, Projects, Goals, Tasks, Protocols, Reports, and Gantt contain no records from the source user.
- [ ] Switch back to the original user and confirm its records are unchanged.
- [ ] Create a user by merging another active user's database; confirm hierarchy, tasks, Protocols, tags, and task–Protocol links are present.
- [ ] Create a Protocol with the same title in the destination before merging; confirm the imported title becomes `Title (Source user)`.
- [ ] Import a compatible external WorkLogger `.db` file and verify the source user name is used for Protocol collision handling.
- [ ] Delete a user and confirm **Remove user, keep database** is the focused default action.
- [ ] Export a retained database and merge it into an active user.
- [ ] Confirm permanent deletion requires the separate **Delete user and database** action.
- [ ] Confirm the last active user cannot be deleted.

## Technical smoke checks

- [ ] Browser console has no uncaught errors while loading Today, Protocols, Reports, and Gantt.
- [ ] `python verify_setup.py` passes inside `.venv`.
- [ ] `data/worklogger.db`, `data/users/`, `data/retained/`, and `data/users.json` are not staged by `git status`.
- [ ] `git diff --check` reports no whitespace errors before commit.
