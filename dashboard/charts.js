/**
 * Developer Analytics Dashboard
 * charts.js - Chart and visualization utilities
 */

const Charts = {
    /**
     * Generate simple ASCII chart
     * @param {Array} data - Array of numbers
     * @param {number} maxHeight - Maximum height in lines
     * @returns {string} ASCII chart
     */
    generateAsciiChart: function(data, maxHeight = 10) {
        if (!data || data.length === 0) return '';
        
        const max = Math.max(...data);
        if (max === 0) return '';
        
        let chart = '';
        for (let i = maxHeight; i > 0; i--) {
            for (let j = 0; j < data.length; j++) {
                const height = Math.round((data[j] / max) * maxHeight);
                chart += height >= i ? '█' : ' ';
                chart += ' ';
            }
            chart += '\n';
        }
        return chart;
    },

    /**
     * Create a simple pie chart visualization
     * @param {Object} data - Object with labels and values
     * @returns {string} Visual representation
     */
    generatePieChart: function(data) {
        const entries = Object.entries(data);
        const total = entries.reduce((sum, [, val]) => sum + val, 0);
        
        if (total === 0) return 'No data';
        
        return entries.map(([label, value]) => {
            const percentage = Math.round((value / total) * 100);
            const fill = Math.round(percentage / 5);
            const empty = 20 - fill;
            const bar = '█'.repeat(fill) + '░'.repeat(empty);
            return `${label.padEnd(10)} [${bar}] ${percentage}%`;
        }).join('\n');
    },

    /**
     * Create trend analysis
     * @param {Array} values - Array of values over time
     * @returns {Object} Trend information
     */
    analyzeTrend: function(values) {
        if (values.length < 2) {
            return { trend: 'stable', percentage: 0, direction: '→' };
        }
        
        const firstHalf = values.slice(0, Math.floor(values.length / 2));
        const secondHalf = values.slice(Math.floor(values.length / 2));
        
        const avgFirst = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length;
        const avgSecond = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length;
        
        const change = ((avgSecond - avgFirst) / avgFirst) * 100;
        
        if (Math.abs(change) < 5) {
            return { trend: 'stable', percentage: 0, direction: '→' };
        } else if (change > 0) {
            return { trend: 'up', percentage: Math.abs(change), direction: '↑' };
        } else {
            return { trend: 'down', percentage: Math.abs(change), direction: '↓' };
        }
    },

    /**
     * Create a sparkline
     * @param {Array} values - Array of numbers
     * @param {number} width - Width in characters
     * @returns {string} Sparkline visualization
     */
    generateSparkline: function(values, width = 20) {
        const chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'];
        
        if (values.length === 0) return '';
        
        const max = Math.max(...values);
        if (max === 0) return chars[0].repeat(width);
        
        const step = Math.ceil(values.length / width);
        let sparkline = '';
        
        for (let i = 0; i < width; i++) {
            const index = i * step;
            if (index < values.length) {
                const value = values[index];
                const level = Math.round((value / max) * (chars.length - 1));
                sparkline += chars[level];
            }
        }
        
        return sparkline;
    },

    /**
     * Compare two metrics
     * @param {number} current - Current value
     * @param {number} previous - Previous value
     * @returns {Object} Comparison object
     */
    compareMetrics: function(current, previous) {
        const change = current - previous;
        const percentage = previous > 0 ? ((change / previous) * 100).toFixed(1) : 0;
        const direction = change > 0 ? '📈' : change < 0 ? '📉' : '→';
        
        return {
            change: change,
            percentage: percentage,
            direction: direction,
            isPositive: change > 0,
            isNegative: change < 0,
            isStable: change === 0
        };
    },

    /**
     * Format large numbers
     * @param {number} num - Number to format
     * @returns {string} Formatted number
     */
    formatNumber: function(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    },

    /**
     * Generate color based on value
     * @param {number} value - Value to color
     * @param {number} threshold - Threshold for color change
     * @returns {string} CSS color
     */
    getColor: function(value, threshold = 50) {
        if (value > threshold * 2) return '#00ff00'; // Green
        if (value > threshold) return '#ffff00'; // Yellow
        return '#ff0000'; // Red
    },

    /**
     * Create heatmap visualization
     * @param {Array} days - Array of day labels
     * @param {Array} values - Array of values for each day
     * @returns {string} HTML heatmap
     */
    generateHeatmap: function(days, values) {
        const max = Math.max(...values);
        
        return days.map((day, i) => {
            const value = values[i] || 0;
            const intensity = Math.round((value / max) * 100);
            const hslColor = `hsl(120, 100%, ${100 - intensity}%)`;
            
            return `<div style="width: 20px; height: 20px; background: ${hslColor}; display: inline-block; margin: 2px; border-radius: 3px;" title="${day}: ${value}"></div>`;
        }).join('');
    },

    /**
     * Generate gauge visualization
     * @param {number} value - Current value
     * @param {number} max - Maximum value
     * @param {string} label - Gauge label
     * @returns {string} Gauge visualization
     */
    generateGauge: function(value, max = 100, label = '') {
        const percentage = Math.min((value / max) * 100, 100);
        const filled = Math.round(percentage / 5);
        const empty = 20 - filled;
        
        const gauge = `[${'█'.repeat(filled)}${'░'.repeat(empty)}]`;
        return `${label} ${gauge} ${Math.round(percentage)}%`;
    }
};

/**
 * Dashboard Chart Renderer
 */
const ChartRenderer = {
    /**
     * Render post popularity chart
     * @param {Array} posts - Array of post objects
     */
    renderPopularityChart: function(posts) {
        if (!posts || posts.length === 0) return 'No data';
        
        const maxViews = Math.max(...posts.map(p => p.views));
        
        return posts.map(post => {
            const percentage = maxViews > 0 ? Math.round((post.views / maxViews) * 100) : 0;
            const barLength = Math.round(percentage / 5);
            const bar = '█'.repeat(barLength) + '░'.repeat(20 - barLength);
            
            return `${post.title.padEnd(25)} ${bar} ${post.views} views`;
        }).join('\n');
    },

    /**
     * Render traffic source distribution
     * @param {Object} sources - Traffic sources object
     */
    renderTrafficChart: function(sources) {
        const total = Object.values(sources).reduce((a, b) => a + b, 0);
        
        if (total === 0) return 'No traffic data';
        
        return Object.entries(sources).map(([source, count]) => {
            const percentage = Math.round((count / total) * 100);
            const barLength = Math.round(percentage / 5);
            const bar = '█'.repeat(barLength) + '░'.repeat(20 - barLength);
            
            return `${source.padEnd(10)} ${bar} ${percentage}%`;
        }).join('\n');
    },

    /**
     * Render engagement metrics
     * @param {Object} metrics - Metrics object
     */
    renderMetrics: function(metrics) {
        const lines = [];
        
        Object.entries(metrics).forEach(([key, value]) => {
            const label = key.replace(/_/g, ' ').toUpperCase();
            lines.push(`${label}: ${value}`);
        });
        
        return lines.join('\n');
    }
};

// Export functions for console usage
window.chartUtils = {
    Charts: Charts,
    ChartRenderer: ChartRenderer,
    
    // Helper function to visualize data in console
    visualize: function(data, type = 'bar') {
        if (type === 'bar' && Array.isArray(data)) {
            console.log(Charts.generateAsciiChart(data));
        } else if (type === 'pie' && typeof data === 'object') {
            console.log(Charts.generatePieChart(data));
        }
    },
    
    // Helper to analyze trends
    trend: function(values) {
        const result = Charts.analyzeTrend(values);
        console.log(`Trend: ${result.direction} ${result.trend} (${result.percentage.toFixed(1)}% change)`);
        return result;
    }
};
