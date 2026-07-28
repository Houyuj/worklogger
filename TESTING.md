# Work Logger - Comprehensive Test Plan

**Version**: 2.5.0
**Last Updated**: December 17, 2025
**Status**: Production Ready - All Features Implemented

---

## Pre-Testing Setup

1. **Start the Application**
   ```bash
   ./run.sh  # Linux/Mac
   # or
   run.bat  # Windows
   ```

2. **Expected Result**: Browser opens automatically to `http://127.0.0.1:8000`

3. **Open Browser Console**: Press F12 to monitor for errors

---

## Test Suite 1: Dashboard - Basic Operations

### Test 1.1: Quick Add Task
**Steps:**
1. Navigate to Dashboard (Today) page
2. In "Quick add" input box, type: `Test task 1`
3. Press Enter (or click Add button)

**Expected Results:**
- ✅ Green success message: "Task added successfully!"
- ✅ Task appears in "Today's Tasks" section
- ✅ Task shows as "In Progress" (unchecked checkbox)
- ✅ Stats update: Total count increases by 1
- ✅ Input box clears after adding

---

### Test 1.2: Delete Task
**Steps:**
1. Find any task in "Today's Tasks"
2. Click the 🗑️ (trash) button
3. Confirm deletion in dialog

**Expected Results:**
- ✅ Confirmation dialog appears
- ✅ After confirming: Green success message "Task deleted successfully!"
- ✅ Task disappears from list
- ✅ Stats update (Total -1)

---

### Test 1.3: Complete/Uncomplete Task
**Steps:**
1. Find an uncompleted task (empty checkbox)
2. Click the checkbox
3. Click the checkbox again

**Expected Results:**
- ✅ First click: Checkbox fills with ✓, title gets strike-through, green left border
- ✅ Stats update: Completed +1, In Progress -1
- ✅ Second click: Checkbox empties, strike-through removed
- ✅ Stats revert to original

---

### Test 1.4: Edit Task
**Steps:**
1. Find any task
2. Click the ✏️ (edit) icon
3. Modify:
   - Title: "Updated test task"
   - Description: "New description"
   - Change date to tomorrow
4. Click "Save Changes"

**Expected Results:**
- ✅ Edit modal opens with task data pre-filled
- ✅ All fields are editable
- ✅ After save: Green success message
- ✅ Modal closes
- ✅ Task updates in list with new title
- ✅ Refresh page - changes persist

---

### Test 1.5: Detailed Task Creation
**Steps:**
1. Click "🧪 Create Detailed Task / Link to Experiment"
2. Fill in:
   - Task Title: `Detailed test task`
   - Description: `This is a test description`
   - Select project, annual goal, monthly goal, weekly goal
3. Click "Add Task"

**Expected Results:**
- ✅ Form expands/collapses correctly
- ✅ All dropdowns populated with database data
- ✅ Task created with all selected tags
- ✅ Form closes after adding
- ✅ Task appears in list

---

## Test Suite 2: Year-Based Filtering

### Test 2.1: Year Selector - Task Filtering
**Steps:**
1. Dashboard → Year selector dropdown
2. Note current date displayed
3. Select different year (e.g., 2024)
4. Observe changes

**Expected Results:**
- ✅ Date automatically jumps to January 1, 2024
- ✅ Date picker updates to show Jan 1, 2024
- ✅ Only tasks from 2024 appear in list
- ✅ If no tasks for that year, shows empty message

---

### Test 2.2: Project Year Range Creation
**Steps:**
1. Dashboard → "Create Detailed Task"
2. Project dropdown → "+ Add New Project"
3. Enter name: "Multi-Year Project"
4. Enter start year: 2025
5. Enter end year: 2026
6. Create the project

**Expected Results:**
- ✅ Prompts appear for name, start_year, end_year
- ✅ Project created successfully
- ✅ Project appears in dropdown for 2025 and 2026
- ✅ Switch year to 2024 - project should NOT appear
- ✅ Switch year to 2025 - project appears
- ✅ Switch year to 2026 - project appears

---

### Test 2.3: Year Range Filtering in Gantt
**Steps:**
1. Create project "Split Ribozyme" with start_year=2025, end_year=2026
2. Add annual goal for year 2025
3. Add monthly goal spanning Nov 2025 - Feb 2026
4. Gantt → Select year 2025
5. Gantt → Select year 2026

**Expected Results:**
- ✅ Year 2025: "Split Ribozyme" project appears
- ✅ Year 2025: Annual goal 2025 appears
- ✅ Year 2025: Monthly goal appears (Nov-Dec portion)
- ✅ Year 2026: "Split Ribozyme" project appears
- ✅ Year 2026: Annual goal 2025 appears (because monthly goal overlaps 2026)
- ✅ Year 2026: Monthly goal appears (Jan-Feb portion)

---

## Test Suite 3: Gantt Chart - Split-Pane Layout

### Test 3.1: Split-Pane Structure
**Steps:**
1. Navigate to Gantt page
2. Observe layout

**Expected Results:**
- ✅ Left panel (350px wide) shows "Projects & Goals" header
- ✅ Right panel shows month labels and week numbers
- ✅ Left panel header has two rows matching right panel header height
- ✅ Left panel does not scroll horizontally
- ✅ Right panel scrolls horizontally to view all 52 weeks

---

### Test 3.2: Vertical Scroll Synchronization
**Steps:**
1. Gantt page with multiple projects
2. Scroll left panel vertically
3. Observe right panel
4. Scroll right panel vertically
5. Observe left panel

**Expected Results:**
- ✅ Scrolling left panel → right panel scrolls to same position
- ✅ Scrolling right panel → left panel scrolls to same position
- ✅ Smooth synchronized scrolling
- ✅ Rows stay aligned

---

### Test 3.3: Full-Text Display with Line Wrapping
**Steps:**
1. Create project with long name: "Very Long Project Name That Should Wrap to Multiple Lines for Display Purposes"
2. Create annual goal with long name: "Extremely Long Annual Goal Name That Needs Multiple Lines to Display Completely Without Truncation"
3. Create monthly goal with long name: "Super Long Monthly Goal Name That Should Wrap Within the Bar and Expand Height"
4. View in Gantt chart

**Expected Results:**
- ✅ Project title wraps to multiple lines, all text visible
- ✅ Annual goal name wraps to multiple lines, all text visible
- ✅ Monthly goal bar text wraps, bar expands vertically, all text visible
- ✅ No ellipsis (...) truncation anywhere
- ✅ Text is readable with appropriate font sizes (0.70em-1.0em)

---

### Test 3.4: Row Height Synchronization
**Steps:**
1. Gantt with long monthly goal name (from Test 3.3)
2. Observe row heights after page load (wait 100ms)
3. Zoom in (+)
4. Zoom out (-)
5. Change year
6. Resize window

**Expected Results:**
- ✅ After initial load: Left annual goal row height matches right timeline row height
- ✅ After zoom in: Heights re-synchronize automatically
- ✅ After zoom out: Heights re-synchronize automatically
- ✅ After year change: Heights re-synchronize for new data
- ✅ After window resize: Heights re-synchronize (200ms debounce)
- ✅ Rows always perfectly aligned horizontally

---

### Test 3.5: Vertical Resize Handle
**Steps:**
1. Gantt page → Locate horizontal resize handle below chart (gray bar with ⋯)
2. Hover over handle
3. Drag down to increase height
4. Drag up to decrease height
5. Try to drag beyond limits

**Expected Results:**
- ✅ Hover changes cursor to `ns-resize`
- ✅ Hover changes background color
- ✅ Dragging down increases chart height smoothly
- ✅ Dragging up decreases chart height smoothly
- ✅ Minimum height enforced: 300px
- ✅ Maximum height enforced: 1200px
- ✅ Cannot drag beyond limits

---

## Test Suite 4: Gantt Chart - Interactive Elements

### Test 4.1: Edit Project Year Range
**Steps:**
1. Gantt → Click on a project title (left panel)
2. Modal opens
3. Change name to "Updated Project"
4. Change start_year to 2024
5. Change end_year to 2027
6. Click "Save Changes"

**Expected Results:**
- ✅ Edit modal opens with current values pre-filled
- ✅ All fields editable
- ✅ After save: Green success message
- ✅ Modal closes
- ✅ Gantt reloads with updated data
- ✅ Project now appears in Gantt for years 2024-2027
- ✅ Project does NOT appear for year 2023

---

### Test 4.2: Change Monthly Goal Status
**Steps:**
1. Gantt → Click on a monthly goal bar
2. Modal opens showing current status
3. Click "In Progress" button
4. Wait for update

**Expected Results:**
- ✅ Modal opens with goal name and date range
- ✅ Four status buttons visible (Planned/In Progress/Completed/Terminated)
- ✅ After clicking status: Modal closes
- ✅ Green success message
- ✅ Gantt reloads
- ✅ Monthly goal bar color updates to light green (#9ae6b4)

---

### Test 4.3: Edit Monthly Goal Time Range - Valid Change
**Steps:**
1. Create monthly goal: Jan 1 - Jan 31, 2025
2. Add task on Jan 15, 2025 to this goal
3. Gantt → Click monthly goal bar
4. Click "Edit Time Range"
5. Enter new start: 2025-01-01
6. Enter new end: 2025-02-28 (extending range)
7. Confirm prompts

**Expected Results:**
- ✅ Prompts appear for start and end dates
- ✅ After entering valid dates: Green success message
- ✅ Modal closes
- ✅ Gantt reloads
- ✅ Monthly goal bar now spans Jan-Feb

---

### Test 4.4: Edit Monthly Goal Time Range - Conflict Validation
**Steps:**
1. Create monthly goal: Jan 1 - Jan 31, 2025
2. Add tasks on Jan 5, Jan 15, Jan 25, 2025 to this goal
3. Gantt → Click monthly goal bar
4. Click "Edit Time Range"
5. Enter new start: 2025-01-10 (shortening range)
6. Enter new end: 2025-01-20 (shortening range)
7. Confirm prompts

**Expected Results:**
- ✅ Prompts appear for dates
- ✅ After entering dates: Red error message appears
- ✅ Error message shows: "Cannot shorten date range. 2 task(s) fall outside the new range (dates: 2025-01-05, 2025-01-25). Please delete or reassign these tasks first."
- ✅ Change is blocked, monthly goal remains Jan 1 - Jan 31
- ✅ No data lost

---

### Test 4.5: View Monthly Goal Report
**Steps:**
1. Gantt → Click monthly goal bar
2. Modal opens
3. Click "View Report for This Period"

**Expected Results:**
- ✅ Navigates to reports.html
- ✅ URL includes date range parameters: `?start=YYYY-MM-DD&end=YYYY-MM-DD&goal=ID`
- ✅ Report page loads tasks for that date range
- ✅ Report highlights the specific monthly goal

---

## Test Suite 5: Reports - Excel/PDF Export

### Test 5.1: Weekly Report Excel Export
**Steps:**
1. Reports → Weekly tab
2. Navigate to a week with multiple tasks
3. Ensure tasks have different monthly goals and weekly goals assigned
4. Click "Export to Excel" button
5. Open downloaded file

**Expected Results:**
- ✅ File downloads: `weekly_report_YYYY-MM-DD.xlsx`
- ✅ Excel opens successfully
- ✅ Title row: "Weekly Report: [date] to [date]"
- ✅ Column headers: Monthly Goal, Weekly Goal, Task Description, Status (blue background #667EEA)
- ✅ **Tasks grouped by monthly goal first**
- ✅ **Within monthly goal, grouped by weekly goal**
- ✅ **Monthly goal column merged vertically** (single cell spanning multiple task rows)
- ✅ Monthly goal background: Light blue (#BEE3F8)
- ✅ All cells have borders
- ✅ Status shows "✓ Done" or "Pending"
- ✅ Column widths auto-adjusted

---

### Test 5.2: Weekly Report PDF Export
**Steps:**
1. Reports → Weekly tab
2. Same week as Test 5.1
3. Click "Export to PDF" button
4. Open downloaded file

**Expected Results:**
- ✅ File downloads: `weekly_report_YYYY-MM-DD.pdf`
- ✅ PDF opens successfully
- ✅ Title: "Weekly Report: [date] to [date]" (purple/blue color #667eea)
- ✅ Summary section with metrics (Total, Completed, Completion Rate)
- ✅ Tasks table with columns: Title, Date, Status
- ✅ Professional styling with grid borders
- ✅ Page margins and formatting

---

### Test 5.3: Monthly Report Excel Export
**Steps:**
1. Reports → Monthly tab
2. Select month and year with multiple monthly goals
3. Ensure monthly goals belong to different annual goals
4. Click "Export to Excel"
5. Open downloaded file

**Expected Results:**
- ✅ File downloads: `monthly_report_YYYY_MM.xlsx`
- ✅ Title: "Monthly Report: [Month] [Year]"
- ✅ Columns: Annual Goal, Monthly Goals, Status
- ✅ **Monthly goals grouped by annual goal**
- ✅ **Annual goal column merged vertically** for each group
- ✅ Annual goal background: Light blue (#BEE3F8)
- ✅ All cells have borders
- ✅ Status shows: planned/in-progress/completed/terminated

---

### Test 5.4: Annual Report Excel Export
**Steps:**
1. Reports → Annual tab
2. Select a year with multiple projects and goals
3. Click "Export to Excel"
4. Open downloaded file

**Expected Results:**
- ✅ File downloads: `annual_report_YYYY.xlsx`
- ✅ Title: "Annual Report: [Year]"
- ✅ Columns: Project, Annual Goal, Monthly Goals, Total Tasks, Completed, Progress
- ✅ Data for all projects and goals
- ✅ Progress column shows percentages (e.g., "75.0%")
- ✅ Statistics calculated correctly

---

### Test 5.5: PDF Export - All Types
**Steps:**
1. Export Monthly PDF
2. Export Annual PDF
3. Open both files

**Expected Results:**
- ✅ Both files download successfully
- ✅ Professional styling with #667eea color theme
- ✅ Styled tables with headers
- ✅ Summary statistics
- ✅ Readable fonts and spacing

---

## Test Suite 6: Experiments - Multiple Tables

### Test 6.1: Create Experiment with Multiple Methodology Tables
**Steps:**
1. Experiments → "+ New Experiment"
2. Name: "PCR Optimization Study"
3. Navigate to Methodology tab
4. Type text in rich text editor: "We performed PCR with varying conditions."
5. Click "+ Add New Table" button
6. Enter title: "PCR Conditions"
7. Enter rows: 3, columns: 3
8. Fill table with data (Temperature, Time, Result)
9. Click "+ Add New Table" again
10. Enter title: "Primer Sequences"
11. Enter rows: 2, columns: 2
12. Fill table with primer data
13. Click "Save Changes"

**Expected Results:**
- ✅ Rich text editor saves HTML content
- ✅ First table created with title "PCR Conditions"
- ✅ Table has 3 rows, 3 columns, all cells editable
- ✅ Second table created with title "Primer Sequences"
- ✅ Both tables visible in Methodology tab
- ✅ Each table has controls: + Row, + Column, - Row, - Column, Delete Table
- ✅ After save: Green success message
- ✅ Refresh page - both tables persist with data

---

### Test 6.2: Manipulate Table Structure
**Steps:**
1. Open experiment from Test 6.1
2. Methodology tab → "PCR Conditions" table
3. Click "+ Row" button
4. Click "+ Column" button
5. Fill new cells with data
6. Click "− Row" button
7. Click "− Column" button
8. Save changes

**Expected Results:**
- ✅ + Row adds new row at bottom with "Data" placeholders
- ✅ + Column adds new column to right
- ✅ New cells are editable
- ✅ − Row removes last row (if > 1 row)
- ✅ − Column removes last column (if > 1 column)
- ✅ Changes persist after save
- ✅ Cannot reduce to 0 rows or 0 columns

---

### Test 6.3: Edit and Delete Tables
**Steps:**
1. Open experiment from Test 6.1
2. Methodology tab → Click "PCR Conditions" title
3. Enter new title: "Updated PCR Conditions"
4. Click "Delete Table" button on "Primer Sequences" table
5. Confirm deletion
6. Save changes

**Expected Results:**
- ✅ Clicking table title prompts for new title
- ✅ Title updates immediately after entering
- ✅ Delete button shows confirmation dialog
- ✅ After confirm: Table disappears
- ✅ After save: Changes persist
- ✅ Refresh page: "PCR Conditions" table with new title remains, "Primer Sequences" gone

---

### Test 6.4: Multiple Tables in Results Section
**Steps:**
1. Open experiment
2. Results tab → Type results text
3. Click "+ Add New Table"
4. Create "Gel Electrophoresis Results" table
5. Click "+ Add New Table"
6. Create "Quantification Data" table
7. Fill both tables
8. Save

**Expected Results:**
- ✅ Results editor saves HTML
- ✅ Both tables created separately from Methodology tables
- ✅ Both tables visible in Results tab
- ✅ Tables stored in separate JSON arrays (methodology vs results)
- ✅ After save and refresh: All data persists correctly

---

### Test 6.5: Image Upload and Gallery
**Steps:**
1. Open experiment
2. Navigate to Images tab
3. Click upload area (or select file)
4. Choose PNG image < 5MB
5. Wait for upload
6. Upload another image (JPG)
7. Click × button on first image
8. Confirm deletion
9. Save changes

**Expected Results:**
- ✅ File picker opens on click
- ✅ After selecting file: Image converts to base64 and uploads
- ✅ Green success message: "Image uploaded successfully"
- ✅ Image appears in grid gallery (200px thumbnail)
- ✅ Second image uploads successfully
- ✅ Delete button (×) shows confirmation dialog
- ✅ After deletion: Image disappears from gallery
- ✅ Refresh page: Remaining image still present

---

## Test Suite 7: Data Persistence and Edge Cases

### Test 7.1: Data Persistence After Refresh
**Steps:**
1. Create 5 tasks, complete 3
2. Edit 1 task
3. Create 1 experiment with tables and images
4. Refresh page (F5)

**Expected Results:**
- ✅ All 5 tasks remain
- ✅ 3 tasks show as completed
- ✅ Edited task shows updated data
- ✅ Experiment exists with all tables and images intact
- ✅ Stats are correct

---

### Test 7.2: Data Persistence After Restart
**Steps:**
1. Create data (tasks, goals, experiments)
2. Stop application (Ctrl+C)
3. Restart application
4. Navigate to pages

**Expected Results:**
- ✅ All data intact after restart
- ✅ Database file `data/worklogger.db` preserved
- ✅ No data loss

---

### Test 7.3: Very Long Text Inputs
**Steps:**
1. Create task with title: 500 characters
2. Create task with description: 5000 characters
3. Create experiment with hypothesis: 10,000 characters

**Expected Results:**
- ✅ All data saves successfully
- ✅ Layout doesn't break
- ✅ Text displays correctly (may scroll)
- ✅ No truncation in database

---

### Test 7.4: Special Characters and XSS Prevention
**Steps:**
1. Create task with title: `Test <script>alert('XSS')</script>`
2. Create table cell with: `<img src=x onerror=alert('XSS')>`
3. View task and table

**Expected Results:**
- ✅ Text is HTML-escaped
- ✅ No script execution
- ✅ Raw text displayed as: `Test <script>alert('XSS')</script>`
- ✅ No security vulnerabilities

---

### Test 7.5: Empty States
**Steps:**
1. Delete all tasks
2. Gantt → Switch to year with no projects
3. Reports → View week with no tasks

**Expected Results:**
- ✅ Dashboard shows: "No tasks for today..."
- ✅ Gantt shows: "No projects found for [year]"
- ✅ Reports show: "No tasks for this week"
- ✅ No errors, graceful handling

---

## Test Suite 8: Browser Console and Errors

### Test 8.1: Console Error Check
**Steps:**
1. Open browser console (F12)
2. Perform all major operations:
   - Add task
   - Edit task
   - Delete task
   - Navigate to Gantt
   - Zoom Gantt
   - Export Excel/PDF
   - Create experiment with tables
3. Check console

**Expected Results:**
- ✅ No red error messages
- ✅ API calls return 200 status codes (check Network tab)
- ✅ No JavaScript exceptions
- ✅ Only INFO/LOG messages present

---

### Test 8.2: Network API Check
**Steps:**
1. Open Network tab in DevTools
2. Refresh dashboard
3. Add a task
4. Edit a task
5. Check network requests

**Expected Results:**
- ✅ GET /api/tasks/today returns 200
- ✅ POST /api/tasks/ returns 200
- ✅ PATCH /api/tasks/{id} returns 200
- ✅ All requests have correct JSON payloads
- ✅ Responses match expected schema

---

## Test Suite 9: Concurrent Access

### Test 9.1: Multi-Tab Consistency
**Steps:**
1. Open app in Tab 1
2. Open app in Tab 2 (same browser)
3. Tab 1: Create task "Task from Tab 1"
4. Tab 2: Refresh page
5. Tab 2: Delete the task
6. Tab 1: Refresh page

**Expected Results:**
- ✅ Tab 2 sees task after refresh
- ✅ Task deleted successfully in Tab 2
- ✅ Tab 1 refresh shows task is gone
- ✅ Database operations are consistent
- ✅ No conflicts

---

## Testing Checklist Summary

Mark each test suite as completed:

- [ ] Test Suite 1: Dashboard - Basic Operations (5 tests)
- [ ] Test Suite 2: Year-Based Filtering (3 tests)
- [ ] Test Suite 3: Gantt Chart - Split-Pane Layout (5 tests)
- [ ] Test Suite 4: Gantt Chart - Interactive Elements (5 tests)
- [ ] Test Suite 5: Reports - Excel/PDF Export (5 tests)
- [ ] Test Suite 6: Experiments - Multiple Tables (5 tests)
- [ ] Test Suite 7: Data Persistence and Edge Cases (5 tests)
- [ ] Test Suite 8: Browser Console and Errors (2 tests)
- [ ] Test Suite 9: Concurrent Access (1 test)

**Total Tests**: 36

---

## Automated Testing (Future Enhancement)

For future developers, consider implementing:

### Backend Tests (pytest)
```python
# tests/test_api.py
def test_create_task():
    response = client.post("/api/tasks/", json={...})
    assert response.status_code == 200

def test_year_filtering():
    # Test get_projects(year=2025)
    # Test get_gantt_data(year=2025)

def test_conflict_validation():
    # Test update_monthly_goal with outside tasks
    # Expect 400 error with detailed message
```

### Frontend Tests (Jest)
```javascript
// tests/dashboard.test.js
test('Quick add task', async () => {
    await userEvent.type(input, 'Test task');
    await userEvent.click(addButton);
    expect(await screen.findByText('Test task')).toBeInTheDocument();
});
```

### End-to-End Tests (Playwright/Cypress)
```javascript
// e2e/gantt.spec.js
test('Gantt row alignment', async ({ page }) => {
    await page.goto('/gantt.html');
    const leftRow = await page.locator('.annual-goal-name').first();
    const rightRow = await page.locator('.timeline').first();
    expect(await leftRow.boundingBox().height)
        .toBe(await rightRow.boundingBox().height);
});
```

---

## Troubleshooting Failed Tests

### Gantt Rows Not Aligning
- **Cause**: Height synchronization timing issue
- **Solution**: Refresh page, check console for errors, verify `synchronizeRowHeights()` runs after 100ms

### Excel Export Returns 500 Error
- **Cause**: openpyxl not installed
- **Solution**: `conda install -n worklogger openpyxl -y`

### Year Filtering Not Working
- **Cause**: Database missing start_year/end_year columns
- **Solution**: Run migration `python -m backend.migrations.add_project_year_range`

### Long Names Still Truncated
- **Cause**: CSS not applied
- **Solution**: Clear browser cache (Ctrl+F5), verify CSS properties in DevTools

### Images Not Uploading
- **Cause**: File size > 5MB or unsupported format
- **Solution**: Compress image or convert to PNG/JPG

---

## Reporting Issues

When reporting a failed test, include:

1. **Test number** (e.g., Test 5.1)
2. **Steps performed**
3. **Expected result**
4. **Actual result**
5. **Browser and version** (e.g., Chrome 120)
6. **Console errors** (screenshot or copy-paste)
7. **Network errors** (if API-related)
8. **Screenshots** (if visual issue)

Example:
```
Test 4.4 Failed: Edit Monthly Goal Time Range - Conflict Validation

Steps: Attempted to shorten monthly goal date range with tasks outside new range
Expected: Error message with affected task dates
Actual: Change went through, tasks became unlinked
Console Error: None
Browser: Firefox 121
Screenshot: [attached]
```

---

**Status**: All 36 tests should pass on v2.5.0
**Version**: 2.5.0
**Last Updated**: December 17, 2025
**Ready for**: Production deployment
