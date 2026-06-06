/**
 * Blog Page Tracker Integration
 * blog-tracker.js - Auto-track blog post views and interactions
 * 
 * Usage: Add to blog pages, automatically detects and tracks:
 * - data-blog-post="slug" attribute on body
 * - Page view events
 * - Time spent reading
 * - Scroll depth
 * - Link clicks
 */

window.BlogTracker = {
  /**
   * Initialize blog tracking
   */
  init: function() {
    // Detect blog post slug from body attribute
    const blogSlug = document.body.getAttribute('data-blog-post') || 
                     document.querySelector('h1')?.textContent?.toLowerCase().replace(/\s+/g, '-') ||
                     'blog-post';
    
    // Track page view
    if (window.Tracker) {
      window.Tracker.trackPageView(blogSlug);
      window.Tracker.addActivity({
        text: `📖 Blog post read: ${this.formatTitle(blogSlug)}`,
        icon: '📖',
        timestamp: new Date().toISOString()
      });
    }

    // Setup event listeners
    this.setupScrollTracking(blogSlug);
    this.setupTimeTracking(blogSlug);
    this.setupLinkTracking(blogSlug);
  },

  /**
   * Track scroll depth on blog post
   */
  setupScrollTracking: function(slug) {
    let lastScrollPercent = 0;
    const maxScrollPercent = 0;

    window.addEventListener('scroll', () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercent = scrollHeight > 0 ? 
        Math.round((window.scrollY / scrollHeight) * 100) : 0;

      // Track every 25% scroll
      if (scrollPercent - lastScrollPercent >= 25 && scrollPercent <= 100) {
        window.Tracker?.trackScrollDepth?.(slug, scrollPercent);
        
        // Activity milestone
        if (scrollPercent === 100) {
          window.Tracker?.addActivity?.({
            text: `✅ Blog post completed: ${this.formatTitle(slug)}`,
            icon: '✅',
            timestamp: new Date().toISOString()
          });
        }

        lastScrollPercent = scrollPercent;
      }
    });
  },

  /**
   * Track time spent reading blog
   */
  setupTimeTracking: function(slug) {
    let timeOnPage = 0;
    const timeInterval = setInterval(() => {
      timeOnPage++;
    }, 1000);

    // Auto-save every 30 seconds
    const saveInterval = setInterval(() => {
      if (timeOnPage > 0) {
        window.Tracker?.trackTimeSpent?.(slug, timeOnPage);
      }
    }, 30000);

    // Save on page unload
    window.addEventListener('beforeunload', () => {
      clearInterval(timeInterval);
      clearInterval(saveInterval);
      if (timeOnPage > 0) {
        window.Tracker?.trackTimeSpent?.(slug, timeOnPage);
      }
    });
  },

  /**
   * Track external link clicks on blog post
   */
  setupLinkTracking: function(slug) {
    const links = document.querySelectorAll('a[href]');
    
    links.forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        
        // Track GitHub links
        if (href?.includes('github.com')) {
          window.Tracker?.trackGitHubClick?.(slug);
          window.Tracker?.addActivity?.({
            text: `🔗 GitHub link clicked from: ${this.formatTitle(slug)}`,
            icon: '🔗',
            timestamp: new Date().toISOString()
          });
        }
        
        // Track external links
        if (href?.startsWith('http') && !href?.includes(window.location.hostname)) {
          window.Tracker?.trackTrafficSource?.('referral');
        }
      });
    });
  },

  /**
   * Format slug to readable title
   */
  formatTitle: function(slug) {
    return slug.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()).substring(0, 40);
  }
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => window.BlogTracker?.init?.());
} else {
  window.BlogTracker?.init?.();
}

// Make it globally available
window.BlogTracker = window.BlogTracker || {};
