/**
 * Developer Intelligence Tracking System
 * tracker.js - Comprehensive event tracking and analytics for GitHub Pages
 * No backend required - uses localStorage only
 */

window.Tracker = {
    // Storage keys
    STORAGE_KEYS: {
        TRACKING_DATA: 'dev_intel_tracking',
        VIEWS: 'dashboard_views',
        GITHUB_CLICKS: 'dashboard_github_clicks',
        TRAFFIC_SOURCES: 'dashboard_traffic_sources',
        ACTIVITY_FEED: 'dashboard_activity_feed',
        DAILY_STATS: 'dashboard_daily_stats',
        HOURLY_STATS: 'dashboard_hourly_stats',
        SESSION_ID: 'dashboard_session_id'
    },

    /**
     * Track a page view
     * @param {string} slug - Post slug/identifier
     * @param {string} title - Post title (optional)
     */
    trackPageView: function(slug, title = null) {
        const views = this.getViews();
        views[slug] = (views[slug] || 0) + 1;
        localStorage.setItem(this.STORAGE_KEYS.VIEWS, JSON.stringify(views));

        // Add activity
        this.addActivity({
            text: `👁️ ${this.slugToTitle(slug)} viewed`,
            icon: '👁️',
            timestamp: new Date().toISOString()
        });

        console.log(`[Analytics] Tracked view: ${slug}`);
    },

    /**
     * Track a GitHub link click
     * @param {string} slug - Post slug/identifier
     * @param {string} repoUrl - GitHub repository URL (optional)
     */
    trackGithubClick: function(slug, repoUrl = null) {
        const clicks = this.getGithubClicks();
        clicks[slug] = (clicks[slug] || 0) + 1;
        localStorage.setItem(this.STORAGE_KEYS.GITHUB_CLICKS, JSON.stringify(clicks));

        // Add activity
        this.addActivity({
            text: `🔗 GitHub link clicked on ${this.slugToTitle(slug)}`,
            icon: '🔗',
            timestamp: new Date().toISOString()
        });

        console.log(`[Analytics] Tracked GitHub click: ${slug}`);
    },

    /**
     * Track traffic source
     * @param {string} source - Source type (google, linkedin, github, direct)
     */
    trackTrafficSource: function(source = 'direct') {
        const sources = this.getTrafficSources();
        const validSources = ['google', 'linkedin', 'github', 'direct'];
        
        if (!validSources.includes(source)) {
            source = 'direct';
        }
        
        sources[source] = (sources[source] || 0) + 1;
        localStorage.setItem(this.STORAGE_KEYS.TRAFFIC_SOURCES, JSON.stringify(sources));

        console.log(`[Analytics] Tracked traffic source: ${source}`);
    },

    /**
     * Get all page views
     * @returns {Object} Object with slug as key and view count as value
     */
    getViews: function() {
        try {
            const data = localStorage.getItem(this.STORAGE_KEYS.VIEWS);
            return data ? JSON.parse(data) : {};
        } catch (e) {
            console.error('[Analytics] Error retrieving views:', e);
            return {};
        }
    },

    /**
     * Get all GitHub clicks
     * @returns {Object} Object with slug as key and click count as value
     */
    getGithubClicks: function() {
        try {
            const data = localStorage.getItem(this.STORAGE_KEYS.GITHUB_CLICKS);
            return data ? JSON.parse(data) : {};
        } catch (e) {
            console.error('[Analytics] Error retrieving GitHub clicks:', e);
            return {};
        }
    },

    /**
     * Get traffic sources
     * @returns {Object} Object with source type and count
     */
    getTrafficSources: function() {
        try {
            const data = localStorage.getItem(this.STORAGE_KEYS.TRAFFIC_SOURCES);
            return data ? JSON.parse(data) : {
                google: 0,
                linkedin: 0,
                github: 0,
                direct: 0
            };
        } catch (e) {
            console.error('[Analytics] Error retrieving traffic sources:', e);
            return { google: 0, linkedin: 0, github: 0, direct: 0 };
        }
    },

    /**
     * Get activity feed
     * @returns {Array} Array of activity objects
     */
    getActivityFeed: function() {
        try {
            const data = localStorage.getItem(this.STORAGE_KEYS.ACTIVITY_FEED);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            console.error('[Analytics] Error retrieving activity feed:', e);
            return [];
        }
    },

    /**
     * Add activity to feed
     * @param {Object} activity - Activity object with text, icon, timestamp
     */
    addActivity: function(activity) {
        const feed = this.getActivityFeed();
        
        // Limit feed to 100 items
        if (feed.length >= 100) {
            feed.shift();
        }
        
        feed.push({
            text: activity.text,
            icon: activity.icon || '•',
            timestamp: activity.timestamp || new Date().toISOString()
        });
        
        localStorage.setItem(this.STORAGE_KEYS.ACTIVITY_FEED, JSON.stringify(feed));
    },

    /**
     * Get view count for specific post
     * @param {string} slug - Post slug
     * @returns {number} View count
     */
    getPostViews: function(slug) {
        const views = this.getViews();
        return views[slug] || 0;
    },

    /**
     * Get GitHub click count for specific post
     * @param {string} slug - Post slug
     * @returns {number} Click count
     */
    getPostGithubClicks: function(slug) {
        const clicks = this.getGithubClicks();
        return clicks[slug] || 0;
    },

    /**
     * Clear all tracking data
     */
    clearAllData: function() {
        Object.values(this.STORAGE_KEYS).forEach(key => {
            localStorage.removeItem(key);
        });
        console.log('[Analytics] All tracking data cleared');
    },

    /**
     * Clear specific data type
     * @param {string} dataType - Type of data to clear (views, clicks, activity, sources)
     */
    clearData: function(dataType) {
        const key = this.STORAGE_KEYS[dataType.toUpperCase()];
        if (key) {
            localStorage.removeItem(key);
            console.log(`[Analytics] Cleared ${dataType}`);
        }
    },

    /**
     * Export all data as JSON
     * @returns {string} JSON string of all tracking data
     */
    exportData: function() {
        return JSON.stringify({
            views: this.getViews(),
            github_clicks: this.getGithubClicks(),
            traffic_sources: this.getTrafficSources(),
            activity_feed: this.getActivityFeed(),
            exported_at: new Date().toISOString()
        }, null, 2);
    },

    /**
     * Import data from JSON
     * @param {string} jsonData - JSON string of tracking data
     */
    importData: function(jsonData) {
        try {
            const data = JSON.parse(jsonData);
            
            if (data.views) {
                localStorage.setItem(this.STORAGE_KEYS.VIEWS, JSON.stringify(data.views));
            }
            if (data.github_clicks) {
                localStorage.setItem(this.STORAGE_KEYS.GITHUB_CLICKS, JSON.stringify(data.github_clicks));
            }
            if (data.traffic_sources) {
                localStorage.setItem(this.STORAGE_KEYS.TRAFFIC_SOURCES, JSON.stringify(data.traffic_sources));
            }
            if (data.activity_feed) {
                localStorage.setItem(this.STORAGE_KEYS.ACTIVITY_FEED, JSON.stringify(data.activity_feed));
            }
            
            console.log('[Analytics] Data imported successfully');
            return true;
        } catch (e) {
            console.error('[Analytics] Error importing data:', e);
            return false;
        }
    },

    /**
     * Convert slug to readable title
     * @param {string} slug - Post slug
     * @returns {string} Readable title
     */
    slugToTitle: function(slug) {
        return slug
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    },

    /**
     * Simulate traffic for demo purposes
     */
    simulateTraffic: function() {
        const posts = ['data-pipeline-python', 'kubernetes-deployment', 'react-hooks-guide', 'terraform-aws', 'docker-best-practices'];
        const sources = ['google', 'linkedin', 'github', 'direct'];
        
        // Simulate views
        posts.forEach(post => {
            const viewCount = Math.floor(Math.random() * 100) + 10;
            for (let i = 0; i < viewCount; i++) {
                this.trackPageView(post);
            }
        });
        
        // Simulate GitHub clicks
        posts.forEach(post => {
            if (Math.random() > 0.3) {
                const clickCount = Math.floor(Math.random() * 20) + 1;
                for (let i = 0; i < clickCount; i++) {
                    this.trackGithubClick(post);
                }
            }
        });
        
        // Simulate traffic sources
        for (let i = 0; i < 200; i++) {
            const randomSource = sources[Math.floor(Math.random() * sources.length)];
            this.trackTrafficSource(randomSource);
        }
        
        console.log('[Analytics] Demo traffic simulated');
    },

    /**
     * Get analytics summary
     * @returns {Object} Summary of all tracking data
     */
    getSummary: function() {
        const views = this.getViews();
        const clicks = this.getGithubClicks();
        const sources = this.getTrafficSources();
        
        return {
            total_views: Object.values(views).reduce((a, b) => a + b, 0),
            total_clicks: Object.values(clicks).reduce((a, b) => a + b, 0),
            total_github_clicks: Object.values(clicks).reduce((a, b) => a + b, 0),
            posts_tracked: Object.keys(views).length,
            unique_ips: this.getUniqueIPs(),
            traffic_sources: sources,
            daily_stats: this.getDailyStats(),
            hourly_stats: this.getHourlyStats(),
            last_updated: new Date().toISOString()
        };
    },

    /**
     * Track time spent on page
     * @param {string} slug - Post slug
     * @param {number} seconds - Time spent in seconds
     */
    trackTimeSpent: function(slug, seconds) {
        const data = this.initializeData();
        
        if (!data.pages) data.pages = {};
        if (!data.pages[slug]) {
            data.pages[slug] = { slug, views: 0, time_spent: [] };
        }
        
        data.pages[slug].time_spent = data.pages[slug].time_spent || [];
        data.pages[slug].time_spent.push(seconds);
        
        // Calculate average time spent
        const times = data.pages[slug].time_spent;
        data.pages[slug].avg_time_spent = Math.round(times.reduce((a, b) => a + b, 0) / times.length);
        
        localStorage.setItem(this.STORAGE_KEYS.TRACKING_DATA, JSON.stringify(data));
        
        // Engagement bonus for > 60 seconds
        if (seconds > 60) {
            this.addActivity({
                text: `⏱️ High engagement on ${this.slugToTitle(slug)} (${seconds}s)`,
                icon: '⏱️',
                timestamp: new Date().toISOString()
            });
        }
    },

    /**
     * Track scroll depth
     * @param {string} slug - Post slug
     * @param {number} depth - Scroll depth percentage (0-100)
     */
    trackScrollDepth: function(slug, depth) {
        const data = this.initializeData();
        
        if (!data.pages) data.pages = {};
        if (!data.pages[slug]) {
            data.pages[slug] = { slug, views: 0 };
        }
        
        data.pages[slug].scroll_depth = data.pages[slug].scroll_depth || [];
        data.pages[slug].scroll_depth.push(depth);
        
        localStorage.setItem(this.STORAGE_KEYS.TRACKING_DATA, JSON.stringify(data));
    },

    /**
     * Get daily statistics
     * @returns {Array} Daily stats sorted by date
     */
    getDailyStats: function() {
        try {
            const data = localStorage.getItem(this.STORAGE_KEYS.DAILY_STATS);
            const stats = data ? JSON.parse(data) : {};
            return Object.values(stats).sort((a, b) => new Date(a.date) - new Date(b.date));
        } catch (e) {
            return [];
        }
    },

    /**
     * Update daily stats
     */
    updateDailyStats: function() {
        const dateKey = new Date().toISOString().split('T')[0];
        let stats = {};
        
        try {
            const data = localStorage.getItem(this.STORAGE_KEYS.DAILY_STATS);
            stats = data ? JSON.parse(data) : {};
        } catch (e) {}
        
        if (!stats[dateKey]) {
            stats[dateKey] = { date: dateKey, views: 0, clicks: 0, visitors: 0 };
        }
        
        stats[dateKey].views++;
        localStorage.setItem(this.STORAGE_KEYS.DAILY_STATS, JSON.stringify(stats));
    },

    /**
     * Get hourly statistics
     * @returns {Array} Hourly stats sorted by hour
     */
    getHourlyStats: function() {
        try {
            const data = localStorage.getItem(this.STORAGE_KEYS.HOURLY_STATS);
            const stats = data ? JSON.parse(data) : {};
            return Object.values(stats).sort((a, b) => a.hour - b.hour);
        } catch (e) {
            return [];
        }
    },

    /**
     * Update hourly stats
     */
    updateHourlyStats: function() {
        const hourKey = new Date().getHours();
        let stats = {};
        
        try {
            const data = localStorage.getItem(this.STORAGE_KEYS.HOURLY_STATS);
            stats = data ? JSON.parse(data) : {};
        } catch (e) {}
        
        const key = 'hour_' + hourKey;
        if (!stats[key]) {
            stats[key] = { hour: hourKey, views: 0, clicks: 0 };
        }
        
        stats[key].views++;
        localStorage.setItem(this.STORAGE_KEYS.HOURLY_STATS, JSON.stringify(stats));
    },

    /**
     * Get unique IPs (from visitor intel if available)
     * @returns {Array} Array of unique IP addresses
     */
    getUniqueIPs: function() {
        try {
            const data = localStorage.getItem(this.STORAGE_KEYS.TRACKING_DATA);
            const trackingData = data ? JSON.parse(data) : {};
            return trackingData.unique_ips || [];
        } catch (e) {
            return [];
        }
    },

    /**
     * Initialize comprehensive tracking data structure
     */
    initializeData: function() {
        try {
            const data = localStorage.getItem(this.STORAGE_KEYS.TRACKING_DATA);
            return data ? JSON.parse(data) : {
                pages: {},
                events: [],
                created_at: new Date().toISOString(),
                last_updated: new Date().toISOString()
            };
        } catch (e) {
            return {
                pages: {},
                events: [],
                created_at: new Date().toISOString(),
                last_updated: new Date().toISOString()
            };
        }
    },

    /**
     * Track CV download
     */
    trackCVDownload: function() {
        const data = this.initializeData();
        data.cv_downloads = (data.cv_downloads || 0) + 1;
        localStorage.setItem(this.STORAGE_KEYS.TRACKING_DATA, JSON.stringify(data));
        
        this.addActivity({
            text: '📄 CV downloaded',
            icon: '📄',
            timestamp: new Date().toISOString()
        });
    },

    /**
     * Track contact form interaction
     */
    trackContactInteraction: function() {
        const data = this.initializeData();
        data.contact_interactions = (data.contact_interactions || 0) + 1;
        localStorage.setItem(this.STORAGE_KEYS.TRACKING_DATA, JSON.stringify(data));
        
        this.addActivity({
            text: '✉️ Contact form interaction',
            icon: '✉️',
            timestamp: new Date().toISOString()
        });
    },

    /**
     * Get top pages by view count
     * @param {number} limit - Number of top pages to return
     * @returns {Array} Array of top pages with metrics
     */
    getTopPages: function(limit = 10) {
        const data = this.initializeData();
        const pages = data.pages || {};
        
        return Object.values(pages)
            .map(page => ({
                slug: page.slug,
                views: page.views || 0,
                avg_time_spent: page.avg_time_spent || 0,
                scroll_depth: page.scroll_depth || [],
                clicks: page.clicks || 0
            }))
            .sort((a, b) => b.views - a.views)
            .slice(0, limit);
    }
};

// Auto-detect traffic source from referrer and initialize tracking
(function() {
    // Update daily and hourly stats
    window.Tracker.updateDailyStats();
    window.Tracker.updateHourlyStats();
    
    // Auto-track page view
    const pageSlug = document.body.getAttribute('data-blog-post') || 
                     window.location.pathname.split('/').pop().replace('.html', '') || 
                     'home';
    window.Tracker.trackPageView(pageSlug);
    
    const referrer = document.referrer.toLowerCase();
    
    if (referrer.includes('google')) {
        window.Tracker.trackTrafficSource('google');
    } else if (referrer.includes('linkedin')) {
        window.Tracker.trackTrafficSource('linkedin');
    } else if (referrer.includes('github')) {
        window.Tracker.trackTrafficSource('github');
    } else {
        window.Tracker.trackTrafficSource('direct');
    }
    
    // Track scroll depth every 25%
    let lastScrollPercent = 0;
    window.addEventListener('scroll', function() {
        const scrollPercent = Math.round((window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100);
        
        if (scrollPercent - lastScrollPercent >= 25 && scrollPercent <= 100) {
            window.Tracker.trackScrollDepth(pageSlug, scrollPercent);
            lastScrollPercent = scrollPercent;
        }
    });
    
    // Track time spent on page
    let timeOnPage = 0;
    const timeInterval = setInterval(() => {
        timeOnPage++;
    }, 1000);
    
    window.addEventListener('beforeunload', function() {
        clearInterval(timeInterval);
        window.Tracker.trackTimeSpent(pageSlug, timeOnPage);
    });
})();
