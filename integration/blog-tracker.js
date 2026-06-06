/**
 * Developer Analytics Dashboard
 * blog-tracker.js - Blog post integration for tracking
 * 
 * Add this script to the end of your blog post HTML file:
 * <script src="/dashboard/blog-tracker.js"></script>
 * 
 * Then add data attributes to your blog:
 * <body data-blog-post="post-slug">
 * <a href="..." class="tracked-github-link">link</a>
 */

(function() {
    'use strict';

    const BlogTracker = {
        // Configuration
        config: {
            dashboardPath: '/dashboard/', // Path to dashboard
            storageKeys: {
                views: 'dashboard_views',
                github_clicks: 'dashboard_github_clicks',
                traffic_sources: 'dashboard_traffic_sources',
                activity_feed: 'dashboard_activity_feed'
            }
        },

        // Get current post slug from data attribute
        getPostSlug: function() {
            const bodyElement = document.querySelector('body');
            return bodyElement ? bodyElement.getAttribute('data-blog-post') : null;
        },

        // Track page view
        trackPageView: function() {
            const slug = this.getPostSlug();
            if (!slug) {
                console.warn('[BlogTracker] No post slug found. Add data-blog-post attribute to <body>');
                return;
            }

            this.updateStorage(this.config.storageKeys.views, slug, 1);
            this.addActivity('👁️', `${this.slugToTitle(slug)} viewed`);
            
            console.log(`[BlogTracker] Tracked page view for: ${slug}`);
        },

        // Track GitHub link click
        trackGithubClick: function(url) {
            const slug = this.getPostSlug();
            if (!slug) {
                console.warn('[BlogTracker] No post slug found.');
                return;
            }

            this.updateStorage(this.config.storageKeys.github_clicks, slug, 1);
            this.addActivity('🔗', `GitHub link clicked from ${this.slugToTitle(slug)}`);
            
            console.log(`[BlogTracker] Tracked GitHub click: ${url}`);
        },

        // Track traffic source
        trackTrafficSource: function(source = 'direct') {
            const validSources = ['google', 'linkedin', 'github', 'direct'];
            if (!validSources.includes(source)) {
                source = 'direct';
            }

            this.updateStorage(this.config.storageKeys.traffic_sources, source, 1);
            console.log(`[BlogTracker] Tracked traffic source: ${source}`);
        },

        // Update storage
        updateStorage: function(storageKey, itemKey, increment = 1) {
            try {
                let data = {};
                const stored = localStorage.getItem(storageKey);
                
                if (stored) {
                    data = JSON.parse(stored);
                }
                
                data[itemKey] = (data[itemKey] || 0) + increment;
                localStorage.setItem(storageKey, JSON.stringify(data));
            } catch (e) {
                console.error('[BlogTracker] Storage error:', e);
            }
        },

        // Add activity
        addActivity: function(icon, text) {
            try {
                let feed = [];
                const stored = localStorage.getItem(this.config.storageKeys.activity_feed);
                
                if (stored) {
                    feed = JSON.parse(stored);
                }
                
                // Limit to 100 items
                if (feed.length >= 100) {
                    feed.shift();
                }
                
                feed.push({
                    icon: icon,
                    text: text,
                    timestamp: new Date().toISOString()
                });
                
                localStorage.setItem(this.config.storageKeys.activity_feed, JSON.stringify(feed));
            } catch (e) {
                console.error('[BlogTracker] Activity feed error:', e);
            }
        },

        // Convert slug to title
        slugToTitle: function(slug) {
            return slug
                .split('-')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
        },

        // Initialize tracker
        init: function() {
            // Track page view
            this.trackPageView();

            // Auto-detect traffic source from referrer
            this.autoDetectTrafficSource();

            // Setup GitHub link tracking
            this.setupGithubLinkTracking();

            // Expose API to window
            window.BlogTracker = this;
        },

        // Auto-detect traffic source from referrer
        autoDetectTrafficSource: function() {
            const referrer = document.referrer.toLowerCase();
            
            if (referrer.includes('google')) {
                this.trackTrafficSource('google');
            } else if (referrer.includes('linkedin')) {
                this.trackTrafficSource('linkedin');
            } else if (referrer.includes('github')) {
                this.trackTrafficSource('github');
            } else if (referrer === '') {
                this.trackTrafficSource('direct');
            }
        },

        // Setup GitHub link tracking
        setupGithubLinkTracking: function() {
            const self = this;

            // Method 1: Track links with class 'tracked-github-link'
            document.addEventListener('click', function(e) {
                const link = e.target.closest('.tracked-github-link, a[href*="github.com"]');
                
                if (link && link.href.includes('github.com')) {
                    self.trackGithubClick(link.href);
                }
            });

            // Method 2: Track programmatic clicks
            window.trackGithubClick = function(url) {
                self.trackGithubClick(url);
            };
        },

        // Manual tracking methods (for custom scenarios)
        manualTrackView: function(slug) {
            this.updateStorage(this.config.storageKeys.views, slug, 1);
            this.addActivity('👁️', `${this.slugToTitle(slug)} viewed`);
        },

        manualTrackClick: function(slug, url) {
            this.updateStorage(this.config.storageKeys.github_clicks, slug, 1);
            this.addActivity('🔗', `GitHub link clicked from ${this.slugToTitle(slug)}`);
        },

        // Get current stats
        getStats: function() {
            try {
                const views = JSON.parse(localStorage.getItem(this.config.storageKeys.views) || '{}');
                const clicks = JSON.parse(localStorage.getItem(this.config.storageKeys.github_clicks) || '{}');
                const sources = JSON.parse(localStorage.getItem(this.config.storageKeys.traffic_sources) || '{}');

                return {
                    views: views,
                    github_clicks: clicks,
                    traffic_sources: sources,
                    total_views: Object.values(views).reduce((a, b) => a + b, 0),
                    total_clicks: Object.values(clicks).reduce((a, b) => a + b, 0)
                };
            } catch (e) {
                console.error('[BlogTracker] Error getting stats:', e);
                return null;
            }
        },

        // Export data
        exportData: function() {
            const stats = this.getStats();
            return JSON.stringify(stats, null, 2);
        }
    };

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            BlogTracker.init();
        });
    } else {
        BlogTracker.init();
    }

    // Expose to window for manual tracking
    window.BlogTracker = BlogTracker;
})();
