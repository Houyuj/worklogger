// API client for Work Logger application
const API_BASE_URL = window.location.origin;

class WorkLoggerAPI {
    // ========== Helper Methods ==========
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const config = { ...defaultOptions, ...options };

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

    // ========== Project APIs ==========
    async createProject(data) {
        return this.request('/api/projects/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async getProjects(year = null) {
        let endpoint = '/api/projects/';
        if (year) endpoint += `?year=${year}`;
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

    async getAnnualGoals(projectId = null, year = null) {
        let endpoint = '/api/annual-goals/';
        const params = new URLSearchParams();
        if (projectId) params.append('project_id', projectId);
        if (year) params.append('year', year);
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

    async getMonthlyGoals(annualGoalId = null) {
        let endpoint = '/api/monthly-goals/';
        if (annualGoalId) endpoint += `?annual_goal_id=${annualGoalId}`;
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

    async getWeeklyGoals() {
        return this.request('/api/weekly-goals/');
    }

    async deleteWeeklyGoal(id) {
        return this.request(`/api/weekly-goals/${id}`, {
            method: 'DELETE',
        });
    }

    // ========== Task APIs ==========
    async createTask(data) {
        return this.request('/api/tasks/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async getTasks(date = null, completed = null) {
        let endpoint = '/api/tasks/';
        const params = new URLSearchParams();
        if (date) params.append('date', date);
        if (completed !== null) params.append('completed', completed);
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
