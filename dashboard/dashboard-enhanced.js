/**
 * Enhanced Dashboard Controller
 * Integrates analytics + visitor intelligence + real-time metrics
 */

const DashboardEnhanced = {
  // Configuration
  refreshInterval: 5000, // 5 seconds
  refreshTimer: null,
  lastRefresh: Date.now(),

  /**
   * Initialize dashboard
   */
  init() {
    console.log('[Dashboard] Initializing enhanced dashboard...');
    
    // Set up event listeners
    document.getElementById('refreshBtn').addEventListener('click', () => this.refresh());
    document.getElementById('clearDataBtn').addEventListener('click', () => this.clearData());
    
    // Initial render
    this.refresh();
    
    // Start auto-refresh
    this.startAutoRefresh();
    
    console.log('[Dashboard] Enhanced dashboard initialized');
  },

  /**
   * Refresh all dashboard sections
   */
  refresh() {
    this.lastRefresh = Date.now();
    
    // Update analytics
    this.updateQuickStats();
    this.updateTopPosts();
    this.updateTrafficSources();
    this.updateGithubClicks();
    this.updateEngagementMetrics();
    
    // Update visitor intelligence
    this.updateVisitorIntel();
    this.updateVisitorClassification();
    
    // Update activity feed
    this.updateRealTimeData();
    
    // Update sync time
    this.updateSyncTime();
  },

  /**
   * Update quick stats
   */
  updateQuickStats() {
    const totalViews = Analytics.getTotalViews();
    const totalClicks = Analytics.getTotalGithubClicks();
    const posts = Analytics.getAllPosts();
    
    document.getElementById('totalViews').textContent = this.formatNumber(totalViews);
    document.getElementById('totalGithubClicks').textContent = this.formatNumber(totalClicks);
    document.getElementById('totalPosts').textContent = posts.length;
    
    // Unique visitors
    const stats = VisitorIntel.getStatistics();
    document.getElementById('uniqueVisitors').textContent = stats.total_visitors;
    
    // Last updated
    document.getElementById('lastUpdated').textContent = Analytics.formatTime(new Date());
  },

  /**
   * Update top posts section
   */
  updateTopPosts() {
    const topPosts = Analytics.getTopPosts(5);
    const container = document.getElementById('topPosts');
    
    if (topPosts.length === 0) {
      container.innerHTML = '<div class="empty-state">No data yet. Posts will appear here as they\'re viewed.</div>';
      return;
    }
    
    let html = '';
    topPosts.forEach((post, index) => {
      const clicks = Tracker.getPostGithubClicks(post.slug) || 0;
      html += `
        <div class="post-item">
          <div class="post-rank">#${index + 1}</div>
          <div class="post-details">
            <div class="post-title">${this.escapeHtml(post.title)}</div>
            <div class="post-meta">${post.views} views • ${clicks} GitHub clicks</div>
          </div>
          <div class="post-views">${post.views} 👁️</div>
        </div>
      `;
    });
    
    container.innerHTML = html;
  },

  /**
   * Update traffic sources
   */
  updateTrafficSources() {
    const sources = Analytics.getTrafficSources();
    const total = Object.values(sources).reduce((a, b) => a + b, 0) || 1;
    
    const percentages = {
      google: Math.round((sources.google || 0) / total * 100),
      linkedin: Math.round((sources.linkedin || 0) / total * 100),
      github: Math.round((sources.github || 0) / total * 100),
      direct: Math.round((sources.direct || 0) / total * 100)
    };
    
    document.getElementById('google-percent').textContent = percentages.google + '%';
    document.getElementById('linkedin-percent').textContent = percentages.linkedin + '%';
    document.getElementById('github-percent').textContent = percentages.github + '%';
    document.getElementById('direct-percent').textContent = percentages.direct + '%';
    
    document.getElementById('google-bar').style.width = percentages.google + '%';
    document.getElementById('linkedin-bar').style.width = percentages.linkedin + '%';
    document.getElementById('github-bar').style.width = percentages.github + '%';
    document.getElementById('direct-bar').style.width = percentages.direct + '%';
  },

  /**
   * Update GitHub clicks
   */
  updateGithubClicks() {
    const posts = Analytics.getAllPosts();
    const container = document.getElementById('githubClicks');
    
    let clickedPosts = [];
    posts.forEach(post => {
      const clicks = Tracker.getPostGithubClicks(post.slug);
      if (clicks > 0) {
        clickedPosts.push({ ...post, clicks });
      }
    });
    
    if (clickedPosts.length === 0) {
      container.innerHTML = '<div class="empty-state">No GitHub clicks tracked yet.</div>';
      return;
    }
    
    // Sort by clicks
    clickedPosts.sort((a, b) => b.clicks - a.clicks);
    
    let html = '';
    clickedPosts.forEach(post => {
      html += `
        <div class="github-click-item">
          <div class="post-title">${this.escapeHtml(post.title)}</div>
          <div class="click-count">
            <span class="badge">${post.clicks} clicks</span>
          </div>
        </div>
      `;
    });
    
    container.innerHTML = html;
  },

  /**
   * Update engagement metrics
   */
  updateEngagementMetrics() {
    const metrics = Analytics.getEngagementMetrics();
    
    document.getElementById('avgViews').textContent = Math.round(metrics.avg_views_per_post || 0);
    document.getElementById('githubCTR').textContent = metrics.github_ctr + '%';
    document.getElementById('mostViewed').textContent = metrics.most_viewed || '—';
    document.getElementById('mostClicked').textContent = metrics.most_clicked || '—';
  },

  /**
   * Update visitor intelligence panel (NEW)
   */
  async updateVisitorIntel() {
    const intel = VisitorIntel.getCachedData();
    if (!intel) {
      // Wait for API
      setTimeout(() => this.updateVisitorIntel(), 1000);
      return;
    }
    
    const container = document.getElementById('visitorIntelPanel');
    const display = VisitorIntel.formatForDisplay(intel);
    const emoji = VisitorIntel.getClassificationEmoji(intel.classification);
    const deviceEmoji = VisitorIntel.getDeviceEmoji(intel.device_type);
    
    let securityHtml = '';
    if (intel.is_vpn) securityHtml += '<span class="security-badge vpn">🔒 VPN</span>';
    if (intel.is_proxy) securityHtml += '<span class="security-badge proxy">⚡ Proxy</span>';
    
    const html = `
      <div class="visitor-details">
        <div class="visitor-row">
          <span class="label">🌐 IP Address</span>
          <span class="value">${display.ip}</span>
        </div>
        <div class="visitor-row">
          <span class="label">📍 Location</span>
          <span class="value">${display.location}</span>
        </div>
        <div class="visitor-row">
          <span class="label">🏢 Organization</span>
          <span class="value">${display.organization}</span>
        </div>
        <div class="visitor-row">
          <span class="label">🏛️ Classification</span>
          <span class="value">${emoji} ${this.capitalize(display.classification)}</span>
        </div>
        <div class="visitor-row">
          <span class="label">💻 Device</span>
          <span class="value">${deviceEmoji} ${this.capitalize(display.device)}</span>
        </div>
        <div class="visitor-row">
          <span class="label">🕐 Timezone</span>
          <span class="value">${display.timezone}</span>
        </div>
        ${securityHtml ? `<div class="visitor-row security">${securityHtml}</div>` : ''}
      </div>
    `;
    
    container.innerHTML = html;
  },

  /**
   * Update visitor classification stats (NEW)
   */
  updateVisitorClassification() {
    const stats = VisitorIntel.getStatistics();
    const container = document.getElementById('visitorClassification');
    
    if (stats.total_visitors === 0) {
      container.innerHTML = '<div class="empty-state">Visitor data will appear here as visitors arrive.</div>';
      return;
    }
    
    const classifications = stats.classifications;
    let html = '';
    
    // Sort by count
    const sorted = Object.entries(classifications)
      .sort((a, b) => b[1] - a[1]);
    
    sorted.forEach(([classification, count]) => {
      const percentage = Math.round(count / stats.total_visitors * 100);
      const emoji = VisitorIntel.getClassificationEmoji(classification);
      
      html += `
        <div class="classification-item">
          <div class="classification-label">
            <span class="label-text">${emoji} ${this.capitalize(classification)}</span>
            <span class="label-count">${count} visitors</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" style="width: ${percentage}%"></div>
          </div>
          <div class="label-percent">${percentage}%</div>
        </div>
      `;
    });
    
    html += `
      <div class="stats-summary">
        <div class="summary-stat">
          <span class="label">Total Visitors</span>
          <span class="value">${stats.total_visitors}</span>
        </div>
        <div class="summary-stat">
          <span class="label">Unique Countries</span>
          <span class="value">${stats.unique_countries}</span>
        </div>
        <div class="summary-stat">
          <span class="label">Device Types</span>
          <span class="value">${stats.unique_devices}</span>
        </div>
      </div>
    `;
    
    container.innerHTML = html;
  },

  /**
   * Update real-time activity
   */
  updateRealTimeData() {
    const activity = Analytics.getActivityFeed(10);
    const container = document.getElementById('activityFeed');
    
    if (activity.length === 0) {
      container.innerHTML = '<div class="empty-state">Activity will appear here in real-time.</div>';
      return;
    }
    
    let html = '';
    activity.forEach(item => {
      html += `
        <div class="activity-item">
          <div class="activity-icon">${item.icon}</div>
          <div class="activity-details">
            <div class="activity-text">${this.escapeHtml(item.text)}</div>
            <div class="activity-time">${Analytics.formatTime(new Date(item.timestamp))}</div>
          </div>
        </div>
      `;
    });
    
    container.innerHTML = html;
  },

  /**
   * Start auto-refresh timer
   */
  startAutoRefresh() {
    this.refreshTimer = setInterval(() => {
      this.refresh();
    }, this.refreshInterval);
  },

  /**
   * Stop auto-refresh timer
   */
  stopAutoRefresh() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
  },

  /**
   * Update sync time
   */
  updateSyncTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    document.getElementById('syncTime').textContent = `${hours}:${minutes}`;
  },

  /**
   * Clear all data
   */
  clearData() {
    if (confirm('Are you sure you want to clear all analytics data?')) {
      Tracker.clearAllData();
      VisitorIntel.clearData();
      this.refresh();
      console.log('[Dashboard] All data cleared');
    }
  },

  /**
   * Utility: Format large numbers
   */
  formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  },

  /**
   * Utility: Capitalize string
   */
  capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  },

  /**
   * Utility: Escape HTML
   */
  escapeHtml(text) {
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
  }
};

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    DashboardEnhanced.init();
  });
} else {
  DashboardEnhanced.init();
}
