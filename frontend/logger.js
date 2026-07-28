/**
 * Work Logger - Frontend Logging Utility
 * Buffers logs and sends them to the backend in batches.
 * Replaces console.log for structured logging.
 */

class WorkLoggerLogger {
    constructor(options = {}) {
        this.buffer = [];
        this.bufferSize = options.bufferSize || 10;
        this.flushInterval = options.flushInterval || 5000; // 5 seconds
        this.apiEndpoint = options.apiEndpoint || '/api/logs/';
        this.enabled = options.enabled !== false;
        this.consoleOutput = options.consoleOutput !== false; // Also log to console

        // Start auto-flush timer
        this._startAutoFlush();

        // Flush on page unload
        window.addEventListener('beforeunload', () => this.flush());
    }

    /**
     * Start the auto-flush timer
     */
    _startAutoFlush() {
        if (this._flushTimer) {
            clearInterval(this._flushTimer);
        }
        this._flushTimer = setInterval(() => this.flush(), this.flushInterval);
    }

    /**
     * Create a log entry
     */
    _createEntry(level, message, data = null) {
        return {
            timestamp: new Date().toISOString(),
            level: level,
            source: 'frontend',
            message: message,
            data: data,
            url: window.location.href,
            userAgent: navigator.userAgent
        };
    }

    /**
     * Add a log entry to the buffer
     */
    _log(level, message, data = null) {
        if (!this.enabled) return;

        const entry = this._createEntry(level, message, data);

        // Console output for development
        if (this.consoleOutput) {
            const consoleMethod = level === 'ERROR' ? 'error' :
                                  level === 'WARN' ? 'warn' :
                                  level === 'DEBUG' ? 'debug' : 'log';
            const prefix = `[${level}]`;
            if (data) {
                console[consoleMethod](prefix, message, data);
            } else {
                console[consoleMethod](prefix, message);
            }
        }

        // Add to buffer
        this.buffer.push(entry);

        // Auto-flush if buffer is full
        if (this.buffer.length >= this.bufferSize) {
            this.flush();
        }
    }

    /**
     * Log a DEBUG message
     */
    debug(message, data = null) {
        this._log('DEBUG', message, data);
    }

    /**
     * Log an INFO message
     */
    info(message, data = null) {
        this._log('INFO', message, data);
    }

    /**
     * Log a WARN message
     */
    warn(message, data = null) {
        this._log('WARN', message, data);
    }

    /**
     * Log an ERROR message
     */
    error(message, data = null) {
        this._log('ERROR', message, data);
    }

    /**
     * Flush buffered logs to the server
     */
    async flush() {
        if (this.buffer.length === 0) return;

        const logsToSend = [...this.buffer];
        this.buffer = [];

        try {
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ logs: logsToSend }),
            });

            if (!response.ok) {
                // Re-add logs to buffer on failure (limit to prevent memory issues)
                if (this.buffer.length < 100) {
                    this.buffer = [...logsToSend, ...this.buffer];
                }
            }
        } catch (error) {
            // Network error - re-add logs to buffer
            if (this.buffer.length < 100) {
                this.buffer = [...logsToSend, ...this.buffer];
            }
            // Log to console as fallback
            if (this.consoleOutput) {
                console.warn('[Logger] Failed to flush logs:', error.message);
            }
        }
    }

    /**
     * Get logs from the server
     */
    async getLogs(options = {}) {
        const params = new URLSearchParams();
        if (options.date) params.append('date', options.date);
        if (options.level) params.append('level', options.level);
        if (options.source) params.append('source', options.source);
        if (options.limit) params.append('limit', options.limit);
        if (options.offset) params.append('offset', options.offset);

        const url = `${this.apiEndpoint}?${params.toString()}`;

        try {
            const response = await fetch(url);
            if (response.ok) {
                return await response.json();
            }
            return [];
        } catch (error) {
            console.error('[Logger] Failed to get logs:', error);
            return [];
        }
    }

    /**
     * Get list of log files
     */
    async getLogFiles() {
        try {
            const response = await fetch(`${this.apiEndpoint}files`);
            if (response.ok) {
                return await response.json();
            }
            return [];
        } catch (error) {
            console.error('[Logger] Failed to get log files:', error);
            return [];
        }
    }

    /**
     * Clear logs
     */
    async clearLogs(date = null) {
        try {
            const url = date ? `${this.apiEndpoint}?date=${date}` : this.apiEndpoint;
            const response = await fetch(url, { method: 'DELETE' });
            return response.ok;
        } catch (error) {
            console.error('[Logger] Failed to clear logs:', error);
            return false;
        }
    }

    /**
     * Enable logging
     */
    enable() {
        this.enabled = true;
    }

    /**
     * Disable logging
     */
    disable() {
        this.enabled = false;
    }

    /**
     * Destroy the logger (clean up timers)
     */
    destroy() {
        if (this._flushTimer) {
            clearInterval(this._flushTimer);
        }
        this.flush();
    }
}

// Create global logger instance
const appLogger = new WorkLoggerLogger({
    bufferSize: 10,
    flushInterval: 5000,
    consoleOutput: true  // Keep console output for development
});

// Export for module systems (if used)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { WorkLoggerLogger, appLogger };
}
