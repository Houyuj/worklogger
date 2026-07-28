# Work Logger - Goal-Based Task Management System

A comprehensive task management and reporting system focused on goal-based organization, visual timeline tracking, and automatic report generation with Excel/PDF export capabilities.

## Version 2.5.0 - Production Ready

**Status**: ✅ All Core Features Implemented and Fully Functional
**Last Updated**: December 17, 2025

---

## 🎯 Key Features

### ✅ Fully Implemented

- **Simple To-Do Interface**: Quick add or detailed task creation with goal linking
- **Three-Tier Goal System**: Projects → Annual Goals → Monthly Goals → Weekly Tags
- **Project Year Ranges**: Projects can span multiple years with automatic filtering
- **Advanced Gantt Chart**: Split-pane visualization with fixed left panel and scrollable timeline
- **Full-Text Display**: All names displayed in full with automatic line wrapping
- **Flexible Experiment Tracking**: Research tracking with multiple tables, rich text editor, and custom tags
- **Auto-Generated Reports**: Weekly, monthly, and annual reports with grouped goal organization
- **Excel Export**: Grouped by goals with merged cells and color coding
- **PDF Export**: Professional reports with styled tables and statistics
- **Task Edit/Delete**: Full CRUD operations with modal forms
- **Real-time Stats**: Completion rates and progress tracking
- **Year Navigation**: Jump to January 1st when changing years
- **Height Synchronization**: Gantt chart rows auto-align between panels

---

## 🚀 Quick Start

### Windows Users:
```bash
setup.bat   # First time only; requires Python 3.10, 3.11, or 3.12
run.bat     # Start application
```

### Linux/Mac Users:
```bash
conda env create -f environment.yml  # First time only
./run.sh    # Start application
```

The application opens automatically at: `http://127.0.0.1:8000`

For a research-focused Chinese onboarding guide, see [USER_GUIDE_ZH.md](USER_GUIDE_ZH.md).

---

## 📁 Project Structure

```
programNote/
├── backend/              # Backend API (FastAPI)
│   ├── main.py          # FastAPI server with 40+ endpoints
│   ├── models.py        # SQLAlchemy ORM models (8 tables)
│   ├── schemas.py       # Pydantic validation schemas
│   ├── crud.py          # Database CRUD operations
│   ├── database.py      # SQLite database configuration
│   └── logger.py        # Logging system
├── frontend/            # Frontend HTML pages
│   ├── index.html       # Navigation hub
│   ├── dashboard.html   # Daily task management (1900+ lines)
│   ├── reports.html     # Reports and analytics (990+ lines)
│   ├── gantt.html       # Split-pane Gantt chart (1160+ lines)
│   ├── experiments.html # Experiment list (640+ lines)
│   ├── experiment-detail.html # Experiment editor (1015+ lines)
│   ├── api.js           # JavaScript API client (280+ lines)
│   └── logger.js        # Frontend logging utility
├── data/                # Database storage (auto-created)
│   └── worklogger.db    # SQLite database
├── logs/                # Application logs (auto-rotated)
├── requirements.txt     # Python dependencies
├── environment.yml      # Conda environment specification
├── launcher.py          # Application launcher
├── init_sample_data.py  # Sample data generator
└── *.md                # Comprehensive documentation

Total: ~8,000 lines of code
```

---

## 💡 Usage Guide

### 1. Dashboard (Daily Task Management)

**Quick Add**:
- Type task in input box and press Enter
- Automatically tagged with current active goals
- Date picker for scheduling

**Detailed Task**:
- Click "Create Detailed Task / Link to Experiment"
- Fill in title, description, date
- Select from dropdowns:
  - Project (with year range filtering)
  - Annual Goal
  - Monthly Goal (with date range validation)
  - Weekly Goal
  - Link to Experiments
- Create new projects/goals on-the-fly with "+" options

**Edit Task**:
- Click ✏️ icon to open edit modal
- Modify any field including date and goal assignments
- Changes persist immediately

**Year Selector**:
- Filter tasks by year using dropdown
- Automatically jumps to January 1st when changing years
- Only shows projects with year ranges matching selected year

### 2. Experiments

**Create Experiment**:
- Click "+ New Experiment"
- Fill in overview (name, status, tags)
- Use rich text editors for:
  - Hypothesis
  - Methodology
  - Results
  - Conclusion
  - Progress Notes

**Multiple Tables**:
- Add multiple titled tables in Methodology and Results tabs
- Editable table cells with add/remove row/column controls
- Tables save with custom titles for organization

**Image Gallery**:
- Upload images (PNG, JPG, GIF, max 5MB)
- Stored as base64 in database
- Delete images with confirmation

**Link to Tasks**:
- Link experiments to daily tasks
- View all linked tasks in reports

### 3. Gantt Chart (Split-Pane Timeline)

**Layout**:
- **Left Panel (Fixed)**: Projects & Annual Goals with full name display
- **Right Panel (Scrollable)**: 52-week timeline with monthly goal bars
- **Header Alignment**: "Projects & Goals" header matches month/week rows height
- **Synchronized Scrolling**: Vertical scroll syncs between panels
- **Vertical Resize**: Drag handle below chart to adjust height (300px-1200px)

**Visual Elements**:
- Projects with year ranges (start_year, end_year)
- Annual goals grouped under projects
- Monthly goal bars color-coded:
  - **Gray**: Completed
  - **Light Green**: In Progress
  - **Light Blue**: Planned
  - **Light Red**: Terminated
  - **Dotted Red**: No Activity (current month)

**Full Name Display**:
- Long names automatically wrap with line breaks
- Font size adjusts (0.70em-0.95em) for better fit
- All text fully visible (no truncation)
- Row heights auto-synchronize after rendering

**Interactions**:
- Click project title: Opens project edit modal
- Click annual goal name: Jump to annual goal report
- Click monthly goal bar: Opens monthly goal modal with options:
  - Change Status (Planned/In Progress/Completed/Terminated)
  - Edit Time Range (with conflict validation)
  - View Report for Period

**Controls**:
- Zoom: +/−/100% buttons (50%-200%)
- Year Navigation: < > arrows
- Zoom operations trigger height re-synchronization

**Year Range Filtering**:
- Viewing 2026 shows:
  - Projects with year range including 2026
  - Annual goals with year=2026
  - Annual goals from other years with monthly goals overlapping 2026
- Example: "Split Ribozyme" project (2025-2026) appears in both 2025 and 2026

### 4. Reports

**Weekly Reports**:
- Task completion statistics
- Tasks grouped by monthly goal, then weekly goal
- Overlapping monthly goals (≥1 workday overlap) included
- Excel export with merged cells and color highlighting
- PDF export with styled tables

**Monthly Reports**:
- Goal progress tracking
- Monthly goals grouped by annual goal
- Completion rates with progress bars
- Excel/PDF export with grouped layout

**Annual Reports**:
- Year-long goal summary
- Project overview with statistics
- Progress percentage calculations
- Multi-year project support

**Export Features**:
- **Excel**:
  - Grouped by goals with merged cells
  - Blue background for group headers
  - Cell borders and auto-adjusted widths
  - Status icons (✓ Done, Pending)
- **PDF**:
  - Professional layout with headers
  - Colored backgrounds (#667eea theme)
  - Summary tables with metrics
  - Page formatting with margins

---

## 🏗️ Architecture & Database

### Tech Stack
- **Backend**: FastAPI 0.104.1 + Uvicorn 0.24.0
- **Database**: SQLite with SQLAlchemy 2.0.23
- **Validation**: Pydantic 2.5.0
- **Excel**: openpyxl 3.1.5
- **PDF**: reportlab 3.6.13
- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks)
- **Environment**: Conda (Python 3.10+)

### Database Schema

**Tables** (8 total):
1. **projects**
   - Columns: id, name, description, start_year, end_year, created_at
   - Relationships: 1:N with annual_goals
   - Year Range: Filters by start_year ≤ year ≤ end_year

2. **annual_goals**
   - Columns: id, project_id, name, year, total_tasks, completed_tasks, created_at
   - Relationships: N:1 with projects, 1:N with monthly_goals

3. **monthly_goals**
   - Columns: id, annual_goal_id, name, start_date, end_date, status, total_tasks, completed_tasks
   - Relationships: N:1 with annual_goals, 1:N with tasks
   - Status: planned, in-progress, completed, terminated

4. **weekly_goals**
   - Columns: id, name, created_at
   - Relationships: 1:N with tasks
   - Manual tags (not date-bound)

5. **tasks**
   - Columns: id, title, description, date, completed, completed_at, monthly_goal_id, weekly_goal_id, created_at, updated_at
   - Relationships: N:1 with monthly_goals, N:1 with weekly_goals, M:N with experiments

6. **experiments**
   - Columns: id, name, status, hypothesis, methodology, results, conclusion, progress_notes, images_json, created_at, updated_at
   - Relationships: M:N with tasks, M:N with custom_tags
   - Images: Stored as JSON array of base64-encoded strings

7. **custom_tags**
   - Columns: id, name, created_at
   - Relationships: M:N with experiments

8. **task_experiment** (junction table)
   - Many-to-many relationship between tasks and experiments

### API Endpoints (40+)

**Projects**: GET, POST, PATCH, DELETE `/api/projects/`
**Annual Goals**: GET, POST, DELETE `/api/annual-goals/`
**Monthly Goals**: GET, POST, PATCH, DELETE `/api/monthly-goals/`, PATCH status
**Weekly Goals**: GET, POST, DELETE `/api/weekly-goals/`
**Tasks**: GET, POST, PATCH, DELETE `/api/tasks/`, GET `/api/tasks/today`
**Experiments**: GET, POST, PATCH, DELETE `/api/experiments/`, GET tasks, POST/DELETE images
**Reports**: GET daily, weekly, gantt `/api/reports/`
**Export**: GET Excel/PDF for weekly/monthly/annual `/api/export/`
**Logs**: GET, POST, DELETE `/api/logs/`
**Health**: GET `/api/health`

Full API documentation available at: `http://127.0.0.1:8000/docs`

---

## 🎨 Key Design Decisions

1. **No Time Tracking**: Focus on completion, not time spent
2. **Goal Hierarchy**: Projects → Annual → Monthly → Weekly for clarity
3. **Year Ranges**: Projects can span multiple years naturally
4. **Split-Pane Gantt**: Fixed names, scrollable timeline for better UX
5. **Full Text Display**: No truncation, automatic wrapping
6. **Height Sync**: JavaScript ensures row alignment after rendering
7. **Grouped Exports**: Excel/PDF exports group by goals for readability
8. **Self-Contained**: Single SQLite database, no cloud dependencies
9. **Conda Environment**: Isolated, reproducible setup
10. **Static Frontend**: No build process, instant startup
11. **Base64 Images**: Embedded in database for portability
12. **Multiple Tables**: Experiments can have unlimited titled tables

---

## 🔧 Advanced Configuration

### Change Server Port
Edit `launcher.py`:
```python
port = 8000  # Change to desired port
```

### Database Location
Edit `backend/database.py`:
```python
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'worklogger.db')
```

### Gantt Chart Dimensions
Edit `frontend/gantt.html` CSS:
```css
.gantt-split-container {
    height: 600px;  /* Default height */
    min-height: 300px;  /* Minimum after resize */
}

.gantt-left-panel {
    width: 350px;  /* Fixed left panel width */
}
```

### Export Styling
Edit `backend/main.py`:
```python
# Excel colors
header_fill = PatternFill(start_color="667EEA", ...)
monthly_goal_fill = PatternFill(start_color="BEE3F8", ...)

# PDF colors
header_color = colors.HexColor('#667eea')
```

---

## 📦 Data Management

### Backup
```bash
# Stop application first
cp -r data/ backup-$(date +%Y%m%d)/
```

### Restore
```bash
# Stop application
rm -rf data/
cp -r backup-20251217/ data/
# Restart application
```

### Reset Database
```bash
# Stop application
rm data/worklogger.db
# Restart application (auto-creates tables)
python init_sample_data.py  # Optional: load sample data
```

### Export Database
```bash
sqlite3 data/worklogger.db .dump > backup.sql
```

### Import Database
```bash
sqlite3 data/worklogger.db < backup.sql
```

---

## 🐛 Troubleshooting

### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
conda activate worklogger
conda install -y fastapi uvicorn sqlalchemy pydantic openpyxl reportlab

# Check port availability
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows
```

### Gantt Chart Alignment Issues
- Rows should auto-sync after 100ms delay
- If misaligned, refresh page (F5)
- Check browser console for JavaScript errors
- Height sync runs after: render, zoom, year change, window resize

### Excel Export Internal Server Error
- Ensure openpyxl is installed: `conda list openpyxl`
- Check: `conda install -n worklogger openpyxl -y`
- Verify environment: `conda activate worklogger`

### Long Names Not Wrapping
- Check CSS: `white-space: normal` and `word-wrap: break-word`
- Clear browser cache (Ctrl+F5)
- Inspect element in DevTools to verify CSS applied

### Year Range Filtering Not Working
- Projects require start_year and/or end_year fields
- Run migration: `python -m backend.migrations.add_project_year_range`
- Check API response: `http://127.0.0.1:8000/api/projects/?year=2026`

### Database Errors
```bash
# Backup first!
cp data/worklogger.db data/worklogger.db.backup

# Reset database
rm data/worklogger.db
python launcher.py  # Auto-creates tables

# Restore from SQL dump if available
sqlite3 data/worklogger.db < backup.sql
```

---

## 🚀 Optimization Opportunities for Future Developers

### Performance Optimizations

1. **Database Indexing**
   - Add indexes to frequently queried columns
   - File: `backend/models.py`
   ```python
   # Add to models
   __table_args__ = (
       Index('idx_tasks_date', 'date'),
       Index('idx_tasks_monthly_goal', 'monthly_goal_id'),
       Index('idx_monthly_goals_dates', 'start_date', 'end_date'),
   )
   ```

2. **Gantt Chart Rendering**
   - Current: Synchronizes heights after full render
   - Optimization: Use CSS Grid for automatic alignment
   - File: `frontend/gantt.html`
   - Consider: CSS `display: grid` with `grid-template-columns` instead of split panels

3. **API Response Caching**
   - Cache Gantt data for 1 minute (rarely changes)
   - Use `@lru_cache` decorator in `backend/crud.py`
   - Invalidate cache on data updates

4. **Lazy Loading**
   - Load Gantt chart projects on-demand (scroll-triggered)
   - Currently loads all projects at once
   - Beneficial for 50+ projects

5. **Image Optimization**
   - Current: Base64 in database (increases size ~33%)
   - Alternative: Store in `data/images/` folder, reference by path
   - Pros: Smaller database, faster queries
   - Cons: Loses portability

### UI/UX Enhancements

1. **Drag-and-Drop Task Scheduling**
   - Drag monthly goal bars to change dates
   - Drag tasks between weekly goals
   - Libraries: interact.js, sortable.js

2. **Keyboard Shortcuts**
   - `Ctrl+N`: New task
   - `Ctrl+E`: New experiment
   - `Ctrl+S`: Save/submit forms
   - Implementation: `document.addEventListener('keydown', ...)`

3. **Dark Mode**
   - Add theme toggle in header
   - Store preference in localStorage
   - CSS variables for colors

4. **Mobile Responsive Design**
   - Current: Optimized for desktop
   - Add media queries for < 768px
   - Stack Gantt panels vertically on mobile

5. **Bulk Operations**
   - Select multiple tasks with checkboxes
   - Bulk complete/delete/move to goal
   - Add "Select All" checkbox

### Architecture Improvements

1. **Pagination**
   - Current: Loads all tasks/experiments
   - Add: `?page=1&limit=50` parameters
   - Update: `backend/crud.py`, `frontend/api.js`

2. **WebSocket Real-Time Updates**
   - Auto-refresh when data changes in another tab
   - Use FastAPI WebSocket support
   - Notify: "New task added by another session"

3. **Authentication & Multi-User**
   - Add user accounts with login
   - Row-level security in database
   - JWT token-based auth

4. **Database Migration System**
   - Current: Manual SQL alters
   - Use: Alembic for version-controlled migrations
   - Command: `alembic upgrade head`

5. **Frontend State Management**
   - Current: Reload data after each operation
   - Add: Simple store pattern (like Redux)
   - Benefits: Reduced API calls, optimistic updates

### Code Quality

1. **Unit Tests**
   - Add `tests/` folder
   - Use pytest for backend
   - Jest for frontend JavaScript
   - Target: 80% coverage

2. **TypeScript Conversion**
   - Convert `api.js` to TypeScript
   - Add type safety for API responses
   - Use interfaces for schemas

3. **API Versioning**
   - Add `/api/v1/` prefix
   - Allows breaking changes in v2
   - Backwards compatibility

4. **Error Logging**
   - Enhanced error tracking
   - Stack traces in logs
   - Error reporting dashboard

5. **Code Documentation**
   - Add JSDoc comments
   - Docstrings for Python functions
   - API endpoint descriptions

### Deployment

1. **Docker Containerization**
   ```dockerfile
   FROM python:3.10
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]
   ```

2. **Nginx Reverse Proxy**
   - Serve static files directly
   - Proxy `/api/` to FastAPI
   - SSL/TLS certificates

3. **Cloud Deployment**
   - Deploy to: AWS EC2, DigitalOcean, Heroku
   - Use managed databases: AWS RDS
   - CDN for static assets

4. **Backup Automation**
   - Cron job: Daily database backups
   - Upload to S3/Google Drive
   - Retention policy: 30 days

### Feature Extensions

1. **Recurring Tasks**
   - Add: `recurrence_pattern` field
   - Options: daily, weekly, monthly
   - Auto-create tasks based on pattern

2. **Task Dependencies**
   - "Task B blocked by Task A"
   - Gantt chart shows dependencies with arrows
   - Validation: Can't complete B before A

3. **Notifications**
   - Email reminders for due tasks
   - Desktop notifications (Web Notifications API)
   - Weekly summary emails

4. **Analytics Dashboard**
   - Productivity trends over time
   - Completion rate graphs (Chart.js)
   - Goal achievement metrics

5. **Import/Export**
   - Import from CSV, JSON
   - Export entire database to JSON
   - Integrate with Google Calendar, Todoist

6. **Templates**
   - Save project structures as templates
   - Quick-start with predefined goals
   - Share templates between users

7. **Comments & Attachments**
   - Add comments to tasks
   - File attachments (PDFs, docs)
   - Activity timeline

---

## 📚 Documentation Files

- **README.md**: This file - comprehensive overview
- **QUICKSTART.md**: 5-minute quick start guide
- **PROJECT_SUMMARY.md**: Technical architecture summary
- **IMPLEMENTATION_STATUS.md**: Feature completion status
- **TESTING.md**: Manual testing procedures
- **API Docs**: `http://127.0.0.1:8000/docs` (auto-generated)

---

## 🤝 Contributing

### Code Style
- Python: PEP 8
- JavaScript: ESLint standard
- CSS: BEM naming convention

### Git Workflow
```bash
# Feature branch
git checkout -b feature/new-feature

# Commit with descriptive messages
git commit -m "feat: add drag-drop task scheduling"

# Push and create PR
git push origin feature/new-feature
```

### Testing Before Commit
```bash
# Run backend tests (when implemented)
pytest tests/

# Check for Python errors
python -m py_compile backend/*.py

# Manual testing
./run.sh
# Verify all features work
```

---

## 📄 License

This is a self-contained application for personal and organizational use.
No external dependencies on cloud services.
All data stored locally.

---

## 📞 Support & Resources

- **Documentation**: Check all .md files in project root
- **API Reference**: `http://127.0.0.1:8000/docs`
- **Database Schema**: See `backend/models.py`
- **Sample Data**: Run `python init_sample_data.py`
- **Logs**: Check `logs/` folder for debug info

---

## 🎉 Version History

### v2.5.0 (2025-12-17) - Current
- ✅ Split-pane Gantt chart with height synchronization
- ✅ Full-text display with line wrapping
- ✅ Excel export with grouped goals and merged cells
- ✅ PDF export with professional styling
- ✅ Year range filtering for projects
- ✅ Monthly goal time range editing with validation
- ✅ Experiment detail page with multiple tables
- ✅ Image upload and gallery in experiments

### v2.0.0 (2025-12-16)
- ✅ All CRUD operations functional
- ✅ Edit task modal
- ✅ Search and filter
- ✅ Dynamic reports from database
- ✅ Experiment tracking with API integration
- ✅ Logging system

### v1.2.0 (Initial Release)
- ✅ Basic dashboard and Gantt chart
- ✅ Static frontend pages
- ✅ SQLite database with FastAPI backend

---

**Application is production-ready for personal and team use.**
**All core features tested and functional.**
**Ready for deployment and customization.**
