// API client for Work Logger application
const API_BASE_URL = window.location.origin;
const ACTIVE_USER_STORAGE_KEY = 'worklogger.activeUserId';
const WORKLOGGER_NATIVE_FETCH = window.fetch.bind(window);

window.fetch = function workloggerUserAwareFetch(input, options = {}) {
    const requestUrl = new URL(
        typeof input === 'string' ? input : input.url,
        window.location.origin
    );
    const activeUserId = localStorage.getItem(ACTIVE_USER_STORAGE_KEY);
    if (requestUrl.origin !== window.location.origin ||
        !requestUrl.pathname.startsWith('/api/') ||
        !activeUserId) {
        return WORKLOGGER_NATIVE_FETCH(input, options);
    }

    const headers = new Headers(options.headers || (input instanceof Request ? input.headers : undefined));
    if (!headers.has('X-WorkLogger-User')) {
        headers.set('X-WorkLogger-User', activeUserId);
    }
    return WORKLOGGER_NATIVE_FETCH(input, { ...options, headers });
};

class WorkLoggerAPI {
    // ========== Helper Methods ==========
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const activeUserId = localStorage.getItem(ACTIVE_USER_STORAGE_KEY);
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...(activeUserId ? { 'X-WorkLogger-User': activeUserId } : {}),
            },
        };

        const config = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...(options.headers || {}),
            },
        };
        if (options.body instanceof FormData) {
            delete config.headers['Content-Type'];
        }

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'An error occurred');
            }
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // ========== Local User APIs ==========
    async getUsers() {
        return this.request('/api/users/');
    }

    async createUser(name) {
        return this.request('/api/users/', {
            method: 'POST',
            body: JSON.stringify({ name }),
        });
    }

    async deleteUser(userId, keepDatabase = true) {
        return this.request(`/api/users/${userId}?keep_database=${keepDatabase}`, {
            method: 'DELETE',
        });
    }

    async mergeUserDatabase(targetUserId, sourceUserId) {
        return this.request(`/api/users/${targetUserId}/merge-user/${sourceUserId}`, {
            method: 'POST',
        });
    }

    async mergeRetainedDatabase(targetUserId, retainedId) {
        return this.request(`/api/users/${targetUserId}/merge-retained/${retainedId}`, {
            method: 'POST',
        });
    }

    async importUserDatabase(targetUserId, file, sourceUsername) {
        const formData = new FormData();
        formData.append('source_username', sourceUsername);
        formData.append('database_file', file);
        return this.request(`/api/users/${targetUserId}/import-database`, {
            method: 'POST',
            body: formData,
        });
    }

    userDatabaseUrl(userId) {
        return `${API_BASE_URL}/api/users/${userId}/database`;
    }

    retainedDatabaseUrl(retainedId) {
        return `${API_BASE_URL}/api/users/retained/${retainedId}/database`;
    }

    withActiveUser(url) {
        const userAwareUrl = new URL(url, API_BASE_URL);
        const activeUserId = localStorage.getItem(ACTIVE_USER_STORAGE_KEY);
        if (activeUserId) userAwareUrl.searchParams.set('user_id', activeUserId);
        return `${userAwareUrl.pathname}${userAwareUrl.search}`;
    }

    // ========== Project APIs ==========
    async createProject(data) {
        return this.request('/api/projects/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async getProjects(year = null, includeArchived = false) {
        let endpoint = '/api/projects/';
        const params = new URLSearchParams();
        if (year) params.append('year', year);
        if (includeArchived) params.append('include_archived', 'true');
        if (params.toString()) endpoint += `?${params.toString()}`;
        return this.request(endpoint);
    }

    async getProject(id) {
        return this.request(`/api/projects/${id}`);
    }

    async deleteProject(id) {
        return this.request(`/api/projects/${id}`, {
            method: 'DELETE',
        });
    }

    async updateProject(id, data) {
        return this.request(`/api/projects/${id}`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    // ========== Annual Goal APIs ==========
    async createAnnualGoal(data) {
        return this.request('/api/annual-goals/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async getAnnualGoals(projectId = null, year = null, includeArchived = false) {
        let endpoint = '/api/annual-goals/';
        const params = new URLSearchParams();
        if (projectId) params.append('project_id', projectId);
        if (year) params.append('year', year);
        if (includeArchived) params.append('include_archived', 'true');
        if (params.toString()) endpoint += '?' + params.toString();
        return this.request(endpoint);
    }

    async getAnnualGoal(id) {
        return this.request(`/api/annual-goals/${id}`);
    }

    async deleteAnnualGoal(id) {
        return this.request(`/api/annual-goals/${id}`, {
            method: 'DELETE',
        });
    }

    async updateAnnualGoal(id, data) {
        return this.request(`/api/annual-goals/${id}`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    // ========== Monthly Goal APIs ==========
    async createMonthlyGoal(data) {
        return this.request('/api/monthly-goals/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async getMonthlyGoals(annualGoalId = null, includeArchived = false) {
        let endpoint = '/api/monthly-goals/';
        const params = new URLSearchParams();
        if (annualGoalId) params.append('annual_goal_id', annualGoalId);
        if (includeArchived) params.append('include_archived', 'true');
        if (params.toString()) endpoint += `?${params.toString()}`;
        return this.request(endpoint);
    }

    async getMonthlyGoal(id) {
        return this.request(`/api/monthly-goals/${id}`);
    }

    async updateMonthlyGoalStatus(id, status) {
        return this.request(`/api/monthly-goals/${id}/status?status=${status}`, {
            method: 'PATCH',
        });
    }

    async updateMonthlyGoal(id, data) {
        return this.request(`/api/monthly-goals/${id}`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    async deleteMonthlyGoal(id) {
        return this.request(`/api/monthly-goals/${id}`, {
            method: 'DELETE',
        });
    }

    // ========== Weekly Goal APIs ==========
    async createWeeklyGoal(data) {
        return this.request('/api/weekly-goals/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async getWeeklyGoals(monthlyGoalId = null, year = null, includeArchived = false) {
        const params = new URLSearchParams();
        if (monthlyGoalId) params.append('monthly_goal_id', monthlyGoalId);
        if (year) params.append('year', year);
        if (includeArchived) params.append('include_archived', 'true');
        const query = params.toString();
        return this.request('/api/weekly-goals/' + (query ? `?${query}` : ''));
    }

    async deleteWeeklyGoal(id) {
        return this.request(`/api/weekly-goals/${id}`, {
            method: 'DELETE',
        });
    }

    async updateWeeklyGoal(id, data) {
        return this.request(`/api/weekly-goals/${id}`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    // ========== Task APIs ==========
    async createTask(data) {
        return this.request('/api/tasks/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async getTasks(date = null, completed = null, inbox = null) {
        let endpoint = '/api/tasks/';
        const params = new URLSearchParams();
        if (date) params.append('date', date);
        if (completed !== null) params.append('completed', completed);
        if (inbox !== null) params.append('inbox', inbox);
        if (params.toString()) endpoint += '?' + params.toString();
        return this.request(endpoint);
    }

    async getTodayTasks() {
        return this.request('/api/tasks/today');
    }

    async getTask(id) {
        return this.request(`/api/tasks/${id}`);
    }

    async updateTask(id, data) {
        return this.request(`/api/tasks/${id}`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    async deleteTask(id) {
        return this.request(`/api/tasks/${id}`, {
            method: 'DELETE',
        });
    }

    // ========== Experiment APIs ==========
    async createExperiment(data) {
        return this.request('/api/experiments/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async getExperiments(status = null) {
        let endpoint = '/api/experiments/';
        if (status) endpoint += `?status=${status}`;
        return this.request(endpoint);
    }

    async getExperiment(id) {
        return this.request(`/api/experiments/${id}`);
    }

    async updateExperiment(id, data) {
        return this.request(`/api/experiments/${id}`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    async getExperimentTasks(id) {
        return this.request(`/api/experiments/${id}/tasks`);
    }

    async deleteExperiment(id) {
        return this.request(`/api/experiments/${id}`, {
            method: 'DELETE',
        });
    }

    async duplicateExperiment(id) {
        return this.request(`/api/experiments/${id}/duplicate`, {
            method: 'POST',
        });
    }

    // ========== Experiment Image APIs ==========
    async uploadExperimentImage(experimentId, filename, base64Data) {
        return this.request(`/api/experiments/${experimentId}/images`, {
            method: 'POST',
            body: JSON.stringify({ filename: filename, base64_data: base64Data }),
        });
    }

    async getExperimentImages(experimentId) {
        return this.request(`/api/experiments/${experimentId}/images`);
    }

    async deleteExperimentImage(experimentId, imageId) {
        return this.request(`/api/experiments/${experimentId}/images/${imageId}`, {
            method: 'DELETE',
        });
    }

    // ========== Custom Tag APIs ==========
    async getCustomTags() {
        return this.request('/api/tags/');
    }

    // ========== Report APIs ==========
    async getDailyReport(date) {
        return this.request(`/api/reports/daily?date=${date}`);
    }

    async getWeeklyReport(weekStart) {
        return this.request(`/api/reports/weekly?week_start=${weekStart}`);
    }

    async getGanttData(year) {
        const currentYear = year || new Date().getFullYear();
        return this.request(`/api/reports/gantt?year=${currentYear}`);
    }

    // ========== Utility Methods ==========
    formatDate(date) {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    getTodayDate() {
        return this.formatDate(new Date());
    }

    getWeekNumber(date) {
        const d = new Date(date);
        d.setHours(0, 0, 0, 0);
        d.setDate(d.getDate() + 4 - (d.getDay() || 7));
        const yearStart = new Date(d.getFullYear(), 0, 1);
        const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
        return weekNo;
    }

    getWeekStartDate(weekNumber, year) {
        const jan1 = new Date(year, 0, 1);
        const daysToAdd = (weekNumber - 1) * 7;
        const weekStart = new Date(jan1.setDate(jan1.getDate() + daysToAdd));
        // Adjust to Sunday
        const day = weekStart.getDay();
        const diff = weekStart.getDate() - day;
        return new Date(weekStart.setDate(diff));
    }
}

// Create global API instance
const api = new WorkLoggerAPI();

function escapeUserHtml(value) {
    const element = document.createElement('div');
    element.textContent = String(value ?? '');
    return element.innerHTML;
}

function installUserInterfaceStyles() {
    if (document.getElementById('workloggerUserStyles')) return;
    const styles = document.createElement('style');
    styles.id = 'workloggerUserStyles';
    styles.textContent = `
        .wl-user-switcher {
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .wl-user-switcher select {
            min-width: 130px;
            padding: 7px 30px 7px 10px;
            border: 1px solid #cbd8d4;
            border-radius: 8px;
            background: #fff;
            color: #30434a;
            font: inherit;
            cursor: pointer;
        }
        .wl-user-manage-button {
            width: 36px;
            height: 36px;
            border: 1px solid #cbd8d4;
            border-radius: 9px;
            background: #f7faf9;
            color: #3d5b5a;
            cursor: pointer;
            font-size: 17px;
        }
        .wl-user-manage-button:hover {
            background: #edf5f2;
            border-color: #91aaa3;
        }
        .wl-user-modal {
            position: fixed;
            inset: 0;
            z-index: 12000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 30px;
            background: rgba(30, 47, 50, 0.34);
            backdrop-filter: blur(3px);
        }
        .wl-user-modal.is-open {
            display: flex;
        }
        .wl-user-dialog {
            width: min(880px, 96vw);
            max-height: 90vh;
            overflow: auto;
            border: 1px solid #d7e2de;
            border-radius: 18px;
            background: #fbfcfb;
            box-shadow: 0 24px 70px rgba(35, 55, 58, 0.24);
        }
        .wl-user-dialog-header {
            position: sticky;
            top: 0;
            z-index: 1;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 22px 26px;
            border-bottom: 1px solid #e1e9e6;
            background: rgba(251, 252, 251, 0.96);
        }
        .wl-user-dialog-header h2 {
            margin: 0;
            color: #27383d;
            font-size: 1.45rem;
        }
        .wl-user-close {
            width: 36px;
            height: 36px;
            border: 0;
            border-radius: 9px;
            background: #edf2f0;
            color: #4a5f65;
            cursor: pointer;
            font-size: 22px;
        }
        .wl-user-dialog-body {
            display: grid;
            gap: 22px;
            padding: 24px 26px 28px;
        }
        .wl-user-section {
            padding: 20px;
            border: 1px solid #dfe8e5;
            border-radius: 14px;
            background: #fff;
        }
        .wl-user-section h3 {
            margin: 0 0 6px;
            color: #30434a;
            font-size: 1.05rem;
        }
        .wl-user-section-note {
            margin: 0 0 16px;
            color: #708087;
            font-size: 0.88rem;
            line-height: 1.45;
        }
        .wl-user-list {
            display: grid;
            gap: 9px;
        }
        .wl-user-row {
            display: flex;
            align-items: center;
            gap: 10px;
            min-height: 48px;
            padding: 9px 11px 9px 14px;
            border-radius: 10px;
            background: #f4f7f6;
        }
        .wl-user-row.is-active {
            background: #e8f3ef;
            box-shadow: inset 3px 0 #3c8f7b;
        }
        .wl-user-row-name {
            min-width: 0;
            flex: 1;
            color: #31464d;
            font-weight: 700;
            overflow-wrap: anywhere;
        }
        .wl-user-badge {
            padding: 3px 8px;
            border-radius: 999px;
            background: #d8eae4;
            color: #356c5f;
            font-size: 0.74rem;
            font-weight: 700;
        }
        .wl-user-button {
            padding: 8px 12px;
            border: 1px solid #b9cbc5;
            border-radius: 8px;
            background: #fff;
            color: #38554f;
            font: inherit;
            font-size: 0.86rem;
            font-weight: 650;
            cursor: pointer;
        }
        .wl-user-button:hover {
            background: #edf5f2;
        }
        .wl-user-button.primary {
            border-color: #367e6e;
            background: #367e6e;
            color: #fff;
        }
        .wl-user-button.danger {
            border-color: #d67b7b;
            color: #a43d3d;
        }
        .wl-user-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .wl-user-create-grid {
            display: grid;
            grid-template-columns: minmax(180px, 1fr) minmax(240px, 1.25fr) auto;
            gap: 10px;
            align-items: end;
        }
        .wl-user-field {
            display: grid;
            gap: 6px;
            color: #53676c;
            font-size: 0.82rem;
            font-weight: 700;
        }
        .wl-user-field input,
        .wl-user-field select {
            min-width: 0;
            padding: 10px 11px;
            border: 1px solid #cbd8d4;
            border-radius: 8px;
            background: #fff;
            color: #2f4249;
            font: inherit;
            font-weight: 400;
        }
        .wl-user-upload-fields {
            display: none;
            grid-template-columns: 1.2fr 1fr;
            gap: 10px;
            margin-top: 10px;
        }
        .wl-user-upload-fields.is-visible {
            display: grid;
        }
        .wl-user-status {
            display: none;
            padding: 11px 13px;
            border-radius: 9px;
            background: #e8f4ef;
            color: #28604f;
            font-size: 0.88rem;
            line-height: 1.4;
        }
        .wl-user-status.is-visible {
            display: block;
        }
        .wl-user-status.is-error {
            background: #fff0f0;
            color: #a33e3e;
        }
        .wl-delete-choice {
            display: none;
            padding: 16px;
            border: 1px solid #efc6c6;
            border-radius: 12px;
            background: #fff8f8;
        }
        .wl-delete-choice.is-visible {
            display: block;
        }
        .wl-delete-choice p {
            margin: 0 0 13px;
            color: #5c4545;
            line-height: 1.45;
        }
        .wl-delete-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 9px;
        }
        @media (max-width: 760px) {
            .wl-user-create-grid,
            .wl-user-upload-fields {
                grid-template-columns: 1fr;
            }
            .wl-user-row {
                flex-wrap: wrap;
            }
        }
    `;
    document.head.appendChild(styles);
}

let workloggerUserContext = null;

function activeWorkLoggerUserId() {
    return localStorage.getItem(ACTIVE_USER_STORAGE_KEY);
}

function setActiveWorkLoggerUser(userId) {
    localStorage.setItem(ACTIVE_USER_STORAGE_KEY, userId);
}

function showUserStatus(message, isError = false) {
    const status = document.getElementById('wlUserStatus');
    if (!status) return;
    status.textContent = message;
    status.classList.toggle('is-error', isError);
    status.classList.add('is-visible');
}

function renderUserSwitcher() {
    const container = document.getElementById('wlUserSwitcher');
    if (!container || !workloggerUserContext) return;
    const currentId = activeWorkLoggerUserId();
    const select = container.querySelector('select');
    select.innerHTML = workloggerUserContext.users.map(user =>
        `<option value="${user.id}">${escapeUserHtml(user.name)}</option>`
    ).join('');
    select.value = currentId;
}

function renderUserManagement() {
    if (!workloggerUserContext) return;
    const currentId = activeWorkLoggerUserId();
    const usersList = document.getElementById('wlUserAccounts');
    usersList.innerHTML = workloggerUserContext.users.map(user => `
        <div class="wl-user-row ${user.id === currentId ? 'is-active' : ''}">
            <span class="wl-user-row-name">${escapeUserHtml(user.name)}</span>
            ${user.id === currentId ? '<span class="wl-user-badge">Current</span>' : ''}
            ${user.id === currentId ? '' : `<button class="wl-user-button" type="button" data-switch-user="${user.id}">Switch</button>`}
            <a class="wl-user-button" href="${api.userDatabaseUrl(user.id)}">Export DB</a>
            <button class="wl-user-button danger" type="button" data-delete-user="${user.id}" data-user-name="${escapeUserHtml(user.name)}" ${workloggerUserContext.users.length <= 1 ? 'disabled' : ''}>Delete</button>
        </div>
    `).join('');

    const sourceSelect = document.getElementById('wlCreateSource');
    const previousSource = sourceSelect.value;
    sourceSelect.innerHTML = [
        '<option value="empty">Start with an empty database</option>',
        ...workloggerUserContext.users.map(user =>
            `<option value="user:${user.id}">Merge from user: ${escapeUserHtml(user.name)}</option>`
        ),
        ...workloggerUserContext.retained_databases.map(record =>
            `<option value="retained:${record.id}">Merge retained DB: ${escapeUserHtml(record.name)}</option>`
        ),
        '<option value="upload">Import a WorkLogger .db file…</option>',
    ].join('');
    if ([...sourceSelect.options].some(option => option.value === previousSource)) {
        sourceSelect.value = previousSource;
    }
    updateUserUploadFields();

    const retainedList = document.getElementById('wlRetainedDatabases');
    const retainedSection = document.getElementById('wlRetainedSection');
    retainedSection.style.display = workloggerUserContext.retained_databases.length ? '' : 'none';
    retainedList.innerHTML = workloggerUserContext.retained_databases.map(record => `
        <div class="wl-user-row">
            <span class="wl-user-row-name">${escapeUserHtml(record.name)}</span>
            <span class="wl-user-badge">Database retained</span>
            <a class="wl-user-button" href="${api.retainedDatabaseUrl(record.id)}">Export DB</a>
            <button class="wl-user-button" type="button" data-merge-retained="${record.id}" data-retained-name="${escapeUserHtml(record.name)}">Merge into current</button>
        </div>
    `).join('');
}

function updateUserUploadFields() {
    const source = document.getElementById('wlCreateSource');
    const fields = document.getElementById('wlUserUploadFields');
    if (!source || !fields) return;
    fields.classList.toggle('is-visible', source.value === 'upload');
}

async function refreshUserContext() {
    workloggerUserContext = await api.getUsers();
    const currentId = activeWorkLoggerUserId();
    if (!workloggerUserContext.users.some(user => user.id === currentId)) {
        setActiveWorkLoggerUser(workloggerUserContext.default_user_id);
    }
    renderUserSwitcher();
    renderUserManagement();
}

function openUserManagement() {
    document.getElementById('wlUserModal')?.classList.add('is-open');
    document.getElementById('wlDeleteChoice')?.classList.remove('is-visible');
    const status = document.getElementById('wlUserStatus');
    if (status) status.className = 'wl-user-status';
}

function closeUserManagement() {
    document.getElementById('wlUserModal')?.classList.remove('is-open');
}

function showDeleteUserChoice(userId, userName) {
    const choice = document.getElementById('wlDeleteChoice');
    choice.dataset.userId = userId;
    choice.querySelector('strong').textContent = userName;
    choice.classList.add('is-visible');
    choice.querySelector('[data-delete-mode="keep"]').focus();
}

async function performUserDeletion(keepDatabase) {
    const choice = document.getElementById('wlDeleteChoice');
    const userId = choice.dataset.userId;
    if (!userId) return;
    try {
        showUserStatus(keepDatabase ? 'Removing user and retaining database…' : 'Deleting user and database…');
        const result = await api.deleteUser(userId, keepDatabase);
        if (activeWorkLoggerUserId() === userId) {
            setActiveWorkLoggerUser(result.fallback_user.id);
        }
        await refreshUserContext();
        choice.classList.remove('is-visible');
        showUserStatus(keepDatabase
            ? 'User removed. The database is retained and available below for export or merging.'
            : 'User and database permanently deleted.');
    } catch (error) {
        showUserStatus(error.message, true);
    }
}

async function createWorkLoggerUser() {
    const nameInput = document.getElementById('wlNewUserName');
    const sourceSelect = document.getElementById('wlCreateSource');
    const createButton = document.getElementById('wlCreateUserButton');
    const userName = nameInput.value.trim();
    if (!userName) {
        showUserStatus('Enter a user name.', true);
        nameInput.focus();
        return;
    }

    createButton.disabled = true;
    let newUser = null;
    const source = sourceSelect.value;
    try {
        showUserStatus('Creating isolated user database…');
        newUser = await api.createUser(userName);
        let importResult = null;
        if (source.startsWith('user:')) {
            importResult = await api.mergeUserDatabase(newUser.id, source.slice(5));
        } else if (source.startsWith('retained:')) {
            importResult = await api.mergeRetainedDatabase(newUser.id, source.slice(9));
        } else if (source === 'upload') {
            const file = document.getElementById('wlDatabaseFile').files[0];
            const sourceUsername = document.getElementById('wlSourceUsername').value.trim();
            if (!file) throw new Error('Select a WorkLogger database file to import.');
            if (!sourceUsername) throw new Error('Enter the source user name for Protocol title conflict handling.');
            importResult = await api.importUserDatabase(newUser.id, file, sourceUsername);
        }

        setActiveWorkLoggerUser(newUser.id);
        const renamed = importResult?.counts?.renamed_protocols || 0;
        showUserStatus(importResult
            ? `User created and database merged. ${renamed} conflicting Protocol title${renamed === 1 ? '' : 's'} renamed.`
            : 'User created with an empty isolated database.');
        setTimeout(() => window.location.reload(), 650);
    } catch (error) {
        if (newUser && source !== 'empty') {
            try {
                await api.deleteUser(newUser.id, false);
                newUser = null;
            } catch (rollbackError) {
                console.error('Failed to roll back user after import error:', rollbackError);
            }
        }
        showUserStatus(error.message, true);
        await refreshUserContext();
    } finally {
        createButton.disabled = false;
    }
}

async function mergeRetainedIntoCurrent(recordId, recordName) {
    const currentId = activeWorkLoggerUserId();
    if (!currentId) return;
    if (!window.confirm(`Merge all content from ${recordName}'s retained database into the current user?`)) return;
    try {
        showUserStatus('Merging retained database…');
        const result = await api.mergeRetainedDatabase(currentId, recordId);
        showUserStatus(`Database merged. ${result.counts.renamed_protocols} conflicting Protocol title(s) renamed.`);
    } catch (error) {
        showUserStatus(error.message, true);
    }
}

function buildUserManagementModal() {
    if (document.getElementById('wlUserModal')) return;
    const modal = document.createElement('div');
    modal.id = 'wlUserModal';
    modal.className = 'wl-user-modal';
    modal.innerHTML = `
        <div class="wl-user-dialog" role="dialog" aria-modal="true" aria-labelledby="wlUserDialogTitle">
            <div class="wl-user-dialog-header">
                <h2 id="wlUserDialogTitle">Manage Local Users</h2>
                <button class="wl-user-close" type="button" aria-label="Close">×</button>
            </div>
            <div class="wl-user-dialog-body">
                <section class="wl-user-section">
                    <h3>Users</h3>
                    <p class="wl-user-section-note">Each user has a separate local SQLite database. No password is required.</p>
                    <div id="wlUserAccounts" class="wl-user-list"></div>
                </section>
                <section class="wl-user-section">
                    <h3>Create User</h3>
                    <p class="wl-user-section-note">Start empty or merge an existing database into the new isolated account.</p>
                    <div class="wl-user-create-grid">
                        <label class="wl-user-field">User name
                            <input id="wlNewUserName" type="text" maxlength="80" autocomplete="off" placeholder="e.g. Houyuj">
                        </label>
                        <label class="wl-user-field">Initial content
                            <select id="wlCreateSource"></select>
                        </label>
                        <button id="wlCreateUserButton" class="wl-user-button primary" type="button">Create User</button>
                    </div>
                    <div id="wlUserUploadFields" class="wl-user-upload-fields">
                        <label class="wl-user-field">WorkLogger database
                            <input id="wlDatabaseFile" type="file" accept=".db,.sqlite,.sqlite3,application/vnd.sqlite3">
                        </label>
                        <label class="wl-user-field">Source user name
                            <input id="wlSourceUsername" type="text" maxlength="80" autocomplete="off" placeholder="Used when Protocol titles conflict">
                        </label>
                    </div>
                </section>
                <section id="wlRetainedSection" class="wl-user-section" style="display:none">
                    <h3>Retained Databases</h3>
                    <p class="wl-user-section-note">These users were removed, but their database files were kept for export, sharing or later merging.</p>
                    <div id="wlRetainedDatabases" class="wl-user-list"></div>
                </section>
                <div id="wlDeleteChoice" class="wl-delete-choice">
                    <p>Remove <strong></strong>? Keeping the database is the recommended default so it remains available for export or later merging.</p>
                    <div class="wl-delete-actions">
                        <button class="wl-user-button primary" type="button" data-delete-mode="keep">Remove user, keep database</button>
                        <button class="wl-user-button danger" type="button" data-delete-mode="permanent">Delete user and database</button>
                        <button class="wl-user-button" type="button" data-delete-mode="cancel">Cancel</button>
                    </div>
                </div>
                <div id="wlUserStatus" class="wl-user-status"></div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    modal.querySelector('.wl-user-close').addEventListener('click', closeUserManagement);
    modal.addEventListener('click', event => {
        if (event.target === modal) closeUserManagement();
    });
    document.getElementById('wlCreateSource').addEventListener('change', updateUserUploadFields);
    document.getElementById('wlDatabaseFile').addEventListener('change', event => {
        const file = event.target.files[0];
        const sourceName = document.getElementById('wlSourceUsername');
        if (file && !sourceName.value.trim()) {
            sourceName.value = file.name.replace(/\.(db|sqlite|sqlite3)$/i, '');
        }
    });
    document.getElementById('wlCreateUserButton').addEventListener('click', createWorkLoggerUser);
    document.getElementById('wlDeleteChoice').addEventListener('click', event => {
        const mode = event.target.dataset.deleteMode;
        if (mode === 'keep') performUserDeletion(true);
        if (mode === 'permanent') performUserDeletion(false);
        if (mode === 'cancel') event.currentTarget.classList.remove('is-visible');
    });
    modal.addEventListener('click', event => {
        const switchButton = event.target.closest('[data-switch-user]');
        if (switchButton) {
            setActiveWorkLoggerUser(switchButton.dataset.switchUser);
            window.location.reload();
            return;
        }
        const deleteButton = event.target.closest('[data-delete-user]');
        if (deleteButton) {
            showDeleteUserChoice(deleteButton.dataset.deleteUser, deleteButton.dataset.userName);
            return;
        }
        const retainedButton = event.target.closest('[data-merge-retained]');
        if (retainedButton) {
            mergeRetainedIntoCurrent(
                retainedButton.dataset.mergeRetained,
                retainedButton.dataset.retainedName
            );
        }
    });
}

async function initializeWorkLoggerUsers() {
    installUserInterfaceStyles();
    buildUserManagementModal();
    const menu = document.querySelector('.user-menu');
    if (menu) {
        [...menu.children].forEach(child => {
            if (child.tagName === 'SPAN' &&
                (child.textContent.includes('User') || child.textContent.includes('⚙'))) {
                child.remove();
            }
        });
        const switcher = document.createElement('div');
        switcher.id = 'wlUserSwitcher';
        switcher.className = 'wl-user-switcher';
        switcher.innerHTML = `
            <select aria-label="Current user"></select>
            <button class="wl-user-manage-button" type="button" title="Manage local users" aria-label="Manage local users">⚙</button>
        `;
        menu.appendChild(switcher);
        switcher.querySelector('select').addEventListener('change', event => {
            setActiveWorkLoggerUser(event.target.value);
            window.location.reload();
        });
        switcher.querySelector('button').addEventListener('click', openUserManagement);
    }

    try {
        await refreshUserContext();
    } catch (error) {
        console.error('Failed to initialize local users:', error);
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeWorkLoggerUsers, { once: true });
} else {
    initializeWorkLoggerUsers();
}
