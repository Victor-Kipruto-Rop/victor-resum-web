/**
 * Developer Analytics Dashboard
 * analytics.js - Core analytics and data processing
 */

const Analytics = {
    // Get all posts data
    getAllPosts: function() {
        const views = Tracker.getViews();
        const githubClicks = Tracker.getGithubClicks();
        const posts = [];
        
        // Get all tracked posts from views
        if (views && typeof views === 'object') {
            Object.keys(views).forEach(slug => {
                posts.push({
                    slug: slug,
                    title: this.slugToTitle(slug),
                    views: views[slug] || 0,
                    githubClicks: githubClicks[slug] || 0
                });
            });
        }
        
        return posts.sort((a, b) => b.views - a.views);
    },

    // Get top posts
    getTopPosts: function(limit = 5) {
        return this.getAllPosts().slice(0, limit);
    },

    // Get total views
    getTotalViews: function() {
        const views = Tracker.getViews();
        if (!views || typeof views !== 'object') return 0;
        return Object.values(views).reduce((sum, count) => sum + count, 0);
    },

    // Get total GitHub clicks
    getTotalGithubClicks: function() {
        const clicks = Tracker.getGithubClicks();
        if (!clicks || typeof clicks !== 'object') return 0;
        return Object.values(clicks).reduce((sum, count) => sum + count, 0);
    },

    // Get traffic sources breakdown
    getTrafficSources: function() {
        const traffic = Tracker.getTrafficSources();
        return {
            google: traffic.google || 35,
            linkedin: traffic.linkedin || 25,
            github: traffic.github || 20,
            direct: traffic.direct || 20
        };
    },

    // Get engagement metrics
    getEngagementMetrics: function() {
        const posts = this.getAllPosts();
        const totalViews = this.getTotalViews();
        const totalClicks = this.getTotalGithubClicks();
        
        const avgViews = posts.length > 0 ? Math.round(totalViews / posts.length) : 0;
        const ctr = totalViews > 0 ? Math.round((totalClicks / totalViews) * 100) : 0;
        
        const mostViewed = posts.length > 0 ? posts[0].title : '—';
        const mostClicked = posts.filter(p => p.githubClicks > 0).sort((a, b) => b.githubClicks - a.githubClicks)[0];
        
        return {
            avgViewsPerPost: avgViews,
            githubCTR: ctr,
            mostViewedPost: mostViewed,
            mostClickedPost: mostClicked ? mostClicked.title : '—'
        };
    },

    // Convert slug to readable title
    slugToTitle: function(slug) {
        return slug
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    },

    // Format timestamp
    formatTime: function(date) {
        if (!date) return 'just now';
        const now = new Date();
        const diff = now - date;
        
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        
        if (seconds < 60) return 'just now';
        if (minutes < 60) return `${minutes}m ago`;
        if (hours < 24) return `${hours}h ago`;
        return date.toLocaleDateString();
    },

    // Get activity feed
    getActivityFeed: function(limit = 10) {
        const activity = Tracker.getActivityFeed() || [];
        return activity.slice(-limit).reverse();
    },

    // Calculate percentage
    calculatePercentage: function(value, total) {
        return total === 0 ? 0 : Math.round((value / total) * 100);
    }
};

/**
 * Dashboard App Controller
 */
const DashboardApp = {
    refreshInterval: null,

    // Initialize dashboard
    init: function() {
        this.refresh();
        this.updateLastSyncTime();
    },

    // Refresh all dashboard data
    refresh: function() {
        this.updateQuickStats();
        this.updateTopPosts();
        this.updateTrafficSources();
        this.updateGithubClicks();
        this.updateEngagementMetrics();
        this.updateActivityFeed();
    },

    // Update quick stats
    updateQuickStats: function() {
        document.getElementById('totalViews').textContent = Analytics.getTotalViews().toLocaleString();
        document.getElementById('totalGithubClicks').textContent = Analytics.getTotalGithubClicks().toLocaleString();
        document.getElementById('totalPosts').textContent = Analytics.getAllPosts().length;
        
        const lastUpdated = new Date();
        document.getElementById('lastUpdated').textContent = Analytics.formatTime(lastUpdated);
    },

    // Update top posts section
    updateTopPosts: function() {
        const topPosts = Analytics.getTopPosts(5);
        const container = document.getElementById('topPosts');
        
        if (topPosts.length === 0) {
            container.innerHTML = '<div class="empty-state">No data yet. Posts will appear here as they\'re viewed.</div>';
            return;
        }
        
        container.innerHTML = topPosts.map((post, index) => `
            <div class="post-item">
                <div class="post-rank">#${index + 1}</div>
                <div class="post-details">
                    <div class="post-title">${this.escapeHtml(post.title)}</div>
                    <div class="post-meta">${post.views} views • ${post.githubClicks} GitHub clicks</div>
                </div>
                <div class="post-badge">${post.views} 👁️</div>
            </div>
        `).join('');
    },

    // Update traffic sources
    updateTrafficSources: function() {
        const traffic = Analytics.getTrafficSources();
        const total = traffic.google + traffic.linkedin + traffic.github + traffic.direct;
        
        const sources = [
            { id: 'google', label: 'Google', value: traffic.google },
            { id: 'linkedin', label: 'LinkedIn', value: traffic.linkedin },
            { id: 'github', label: 'GitHub', value: traffic.github },
            { id: 'direct', label: 'Direct', value: traffic.direct }
        ];
        
        sources.forEach(source => {
            const percentage = Analytics.calculatePercentage(source.value, total);
            document.getElementById(`${source.id}-percent`).textContent = `${percentage}%`;
            document.getElementById(`${source.id}-bar`).style.width = `${percentage}%`;
        });
    },

    // Update GitHub clicks
    updateGithubClicks: function() {
        const posts = Analytics.getAllPosts().filter(p => p.githubClicks > 0);
        const container = document.getElementById('githubClicks');
        
        if (posts.length === 0) {
            container.innerHTML = '<div class="empty-state">No GitHub clicks tracked yet.</div>';
            return;
        }
        
        container.innerHTML = posts
            .sort((a, b) => b.githubClicks - a.githubClicks)
            .map(post => `
                <div class="click-item">
                    <div class="click-post">${this.escapeHtml(post.title)}</div>
                    <div class="click-count">${post.githubClicks} clicks</div>
                </div>
            `).join('');
    },

    // Update engagement metrics
    updateEngagementMetrics: function() {
        const metrics = Analytics.getEngagementMetrics();
        
        document.getElementById('avgViewsPerPost').textContent = metrics.avgViewsPerPost.toLocaleString();
        document.getElementById('githubCTR').textContent = `${metrics.githubCTR}%`;
        document.getElementById('mostViewedPost').textContent = this.escapeHtml(metrics.mostViewedPost);
        document.getElementById('mostClickedRepo').textContent = this.escapeHtml(metrics.mostClickedPost);
    },

    // Update activity feed
    updateActivityFeed: function() {
        const activity = Analytics.getActivityFeed(8);
        const container = document.getElementById('activityFeed');
        
        if (activity.length === 0) {
            container.innerHTML = '<div class="empty-state">Activity will appear here in real-time.</div>';
            return;
        }
        
        container.innerHTML = activity.map(item => `
            <div class="activity-item">
                <div class="activity-icon">${item.icon}</div>
                <div class="activity-details">
                    <div class="activity-text">${this.escapeHtml(item.text)}</div>
                    <div class="activity-time">${Analytics.formatTime(new Date(item.timestamp))}</div>
                </div>
            </div>
        `).join('');
    },

    // Update real-time data
    updateRealTimeData: function() {
        this.updateQuickStats();
        this.updateActivityFeed();
    },

    // Update last sync time
    updateLastSyncTime: function() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        document.getElementById('syncTime').textContent = timeStr;
    },

    // Escape HTML
    escapeHtml: function(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};
