# Work Logger - Quick Start Guide

**Version 2.5.0** - Production Ready
**Last Updated**: December 17, 2025

---

## First Time Setup (5 minutes)

### Windows Users:
1. **Double-click `setup.bat`**
   - Installs all required dependencies (FastAPI, SQLAlchemy, openpyxl, reportlab)
   - Creates conda environment named `worklogger`
   - Wait for "Setup completed successfully!" message

2. **Double-click `run.bat`**
   - Activates conda environment
   - Starts FastAPI server
   - Browser opens automatically to dashboard

### Linux/Mac Users:
1. **Open terminal in this folder**

2. **Create conda environment:**
   ```bash
   conda env create -f environment.yml
   ```

3. **Run the application:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

   Or manually:
   ```bash
   conda activate worklogger
   python launcher.py
   ```

The application opens automatically at: `http://127.0.0.1:8000`

---

## Loading Sample Data (Optional)

To see the application with example data:

```bash
conda activate worklogger
python init_sample_data.py
```

This creates:
- 3 sample projects (spanning 2024-2026)
- 9 annual goals
- 15 monthly goals with date ranges
- 5 weekly goals
- Sample tasks for today
- 3 experiments with rich text content and multiple tables

---

## Overview of Features

### ✅ Dashboard (Daily Task Management)
- **Quick Add**: Type task and press Enter
- **Detailed Task Creation**: Link to projects, goals, and experiments
- **Edit Tasks**: Click ✏️ icon to modify any task
- **Delete Tasks**: Click 🗑️ icon to remove
- **Date Picker**: Schedule tasks for any date
- **Year Selector**: Filter tasks by year with automatic date jump to January 1st
- **Project Year Ranges**: Projects can span multiple years (e.g., 2025-2026)

### ✅ Gantt Chart (Visual Timeline)
- **Split-Pane Layout**:
  - Fixed left panel with project/goal names (full text display)
  - Scrollable right panel with 52-week timeline
  - Synchronized vertical scrolling
- **Full Name Display**: All names wrap to multiple lines if needed
- **Color-Coded Status**: Gray (completed), Green (in progress), Red (terminated)
- **Interactive Elements**:
  - Click project title to edit year range
  - Click annual goal to jump to report
  - Click monthly goal bar to change status or edit time range
- **Zoom Controls**: 50%-200% with +/−/100% buttons
- **Year Navigation**: < > arrows to change year
- **Vertical Resize**: Drag handle to adjust chart height (300px-1200px)
- **Height Synchronization**: Rows auto-align between left and right panels

### ✅ Reports (Analytics & Export)
- **Weekly Reports**: Tasks grouped by monthly goal → weekly goal
- **Monthly Reports**: Monthly goals grouped by annual goal
- **Annual Reports**: Year-long summary with progress percentages
- **Excel Export**: Grouped layout with merged cells and color coding
- **PDF Export**: Professional styled reports with statistics

### ✅ Experiments (Research Tracking)
- **Rich Text Editors**: Hypothesis, Methodology, Results, Conclusion, Progress Notes
- **Multiple Tables**: Add unlimited titled tables to Methodology and Results sections
- **Image Gallery**: Upload images (PNG, JPG, GIF, max 5MB)
- **Custom Tags**: Organize experiments with tags
- **Task Linking**: Link experiments to daily tasks

---

## Daily Usage

1. **Open the application**
   - Windows: Double-click `run.bat`
   - Linux/Mac: Run `./run.sh`

2. **Dashboard** - Manage your daily tasks
   - **Quick add**: Type in input box and press Enter
   - **Detailed**: Click "Create Detailed Task" to link goals/experiments
   - **Edit**: Click ✏️ icon to modify title, description, date, or goal assignments
   - **Complete**: Check/uncheck boxes to mark completion
   - **Year filter**: Select year to view only that year's tasks

3. **Gantt Chart** - View project timeline
   - See all projects, annual goals, and monthly goals
   - Click elements to navigate to reports or edit
   - Zoom and adjust height as needed
   - Full name display with automatic line wrapping

4. **Reports** - Analyze progress and export
   - Weekly reports with task completion stats
   - Monthly reports with goal progress
   - Annual overview with achievement metrics
   - Export to Excel or PDF with grouped layout

5. **Experiments** - Track research
   - Create experiments with rich text content
   - Add multiple titled tables to Methodology/Results
   - Upload images to gallery
   - Link to related daily tasks

---

## Key Workflows

### Creating a New Project with Year Range
1. Dashboard → "Create Detailed Task"
2. Project dropdown → "+ Add New Project"
3. Enter name (e.g., "Split Ribozyme")
4. Enter start year: 2025
5. Enter end year: 2026 (or leave empty for ongoing)
6. Project now appears in both 2025 and 2026 Gantt views

### Viewing Year-Specific Data
1. Dashboard → Year selector dropdown
2. Select year (e.g., 2026)
3. Date automatically jumps to January 1, 2026
4. Only projects with year range including 2026 appear
5. Tasks filter to show only 2026 dates

### Creating Experiment with Multiple Tables
1. Experiments → "+ New Experiment"
2. Fill in Overview (name, status, tags)
3. Methodology tab → Rich text editor + "Add New Table" button
4. Add multiple tables with custom titles (e.g., "PCR Conditions", "Primer Sequences")
5. Results tab → Rich text editor + multiple titled tables
6. Upload images in Images tab
7. Save changes

### Exporting Weekly Report with Grouped Goals
1. Reports → Weekly tab
2. Navigate to desired week
3. Click "Export to Excel"
4. Excel file downloads with:
   - Tasks grouped by monthly goal
   - Weekly goals nested under monthly goals
   - Merged cells for group headers
   - Blue background highlighting
   - Status icons (✓ Done, Pending)

### Editing Gantt Chart Elements
1. **Edit Project Year Range**:
   - Gantt → Click project title
   - Modal opens → Edit start_year/end_year
   - Save changes

2. **Change Monthly Goal Status**:
   - Gantt → Click monthly goal bar
   - Modal opens with status buttons
   - Click new status (Planned/In Progress/Completed/Terminated)
   - Bar color updates immediately

3. **Edit Monthly Goal Time Range**:
   - Gantt → Click monthly goal bar
   - Modal → "Edit Time Range" button
   - Enter new start/end dates
   - Validation prevents conflicts with existing tasks

---

## Stopping the Application

- Press `Ctrl+C` in the terminal/command window
- Or simply close the terminal window

---

## Accessing from Other Devices

The application runs on: `http://127.0.0.1:8000`

To access from other devices on your network:
1. Find your computer's IP address
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig` or `ip addr`
2. Open on other device: `http://YOUR_IP:8000`

---

## Backup Your Data

Your data is stored in the `data` folder.

**To backup:**
```bash
# Stop application first
cp -r data/ backup-$(date +%Y%m%d)/
```

**To restore:**
```bash
# Stop application
rm -rf data/
cp -r backup-20251217/ data/
# Restart application
```

**What's backed up:**
- SQLite database with all tasks, goals, experiments
- Images stored as base64 in database (portable)

---

## Configuration

### Change Server Port
Edit `launcher.py`:
```python
port = 8000  # Change to desired port
```

### Gantt Chart Height Range
Edit `frontend/gantt.html` CSS:
```css
.gantt-split-container {
    height: 600px;  /* Default height */
    min-height: 300px;  /* Min after resize */
}
```
Draggable range: 300px - 1200px

### Database Location
Edit `backend/database.py`:
```python
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'worklogger.db')
```

---

## Troubleshooting

### Application won't start?
```bash
# Check Python version (requires 3.8+)
python --version

# Reinstall dependencies
conda activate worklogger
conda install -y fastapi uvicorn sqlalchemy pydantic openpyxl reportlab

# Check port availability
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows
```

### Port 8000 already in use?
- Edit `launcher.py` and change the port number
- Or kill process using port 8000

### Browser doesn't open automatically?
- Manually navigate to: `http://127.0.0.1:8000`

### Gantt chart rows misaligned?
- Refresh page (F5)
- Height sync runs automatically after 100ms
- Check browser console for JavaScript errors
- Clear cache (Ctrl+F5)

### Excel export shows "Internal Server Error"?
```bash
# Verify openpyxl is installed
conda activate worklogger
conda list openpyxl

# If missing, install it
conda install -n worklogger openpyxl -y

# Also install reportlab for PDF export
conda install -n worklogger reportlab -y
```

### Year range filtering not working?
- Projects need start_year and end_year fields
- Run migration (if upgrading from v2.0.0):
  ```bash
  conda activate worklogger
  python -m backend.migrations.add_project_year_range
  ```

### Long names not wrapping in Gantt?
- Check CSS in `frontend/gantt.html`:
  ```css
  .project-title, .annual-goal-name, .month-goal {
      white-space: normal;
      word-wrap: break-word;
      word-break: break-word;
  }
  ```
- Clear browser cache (Ctrl+F5)

---

## Need Help?

Check the full documentation:
- **README.md**: Comprehensive feature documentation with optimization guide
- **PROJECT_SUMMARY.md**: Technical architecture details
- **IMPLEMENTATION_STATUS.md**: Feature completion status
- **TESTING.md**: Test procedures for all features
- **API Docs**: `http://127.0.0.1:8000/docs` (auto-generated Swagger UI)

---

## Version Information

**Current Version**: 2.5.0
**Release Date**: December 17, 2025
**Status**: Production Ready

**New in v2.5.0:**
- ✅ Split-pane Gantt chart with fixed left panel
- ✅ Full-text display with automatic line wrapping
- ✅ Excel export with grouped goals and merged cells
- ✅ PDF export with professional styling
- ✅ Project year ranges (start_year, end_year)
- ✅ Year-based filtering with automatic date jump
- ✅ Experiment detail page with multiple titled tables
- ✅ Monthly goal time range editing with conflict validation
- ✅ Vertical resize handle for Gantt chart
- ✅ Height synchronization between Gantt panels

**Version History:**
- v2.5.0 (Dec 17, 2025) - Split-pane Gantt, Excel/PDF export, year ranges
- v2.0.0 (Dec 16, 2025) - Full CRUD, Edit modal, Experiments, Logging
- v1.2.0 (Initial) - Basic dashboard and Gantt chart

---

**Enjoy organizing your work!**
