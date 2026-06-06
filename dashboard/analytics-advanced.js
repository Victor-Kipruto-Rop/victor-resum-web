/**
 * Advanced Analytics System
 * analytics-advanced.js - Data aggregation and trend analysis for Developer Intelligence Dashboard
 * Processes data from tracker.js and visitor-intel.js without backend
 */

window.Analytics = {
  /**
   * Get comprehensive analytics summary
   */
  getComprehensiveSummary() {
    const trackerData = window.Tracker?.getSummary?.();
    const visitorStats = window.VisitorIntel?.getLeadStatistics?.();
    
    return {
      traffic: {
        total_views: trackerData?.total_views || 0,
        github_clicks: trackerData?.total_github_clicks || 0,
        cv_clicks: trackerData?.total_cv_clicks || 0,
        contact_interactions: trackerData?.total_contact_interactions || 0,
        sources: trackerData?.traffic_sources || {}
      },
      visitors: {
        total_visitors: visitorStats?.total_visitors || 0,
        hot_leads: visitorStats?.hot_leads || 0,
        warm_leads: visitorStats?.warm_leads || 0,
        cold_leads: visitorStats?.cold_leads || 0,
        recruiters: visitorStats?.recruiters_detected || 0,
        avg_lead_score: visitorStats?.avg_score || 0
      },
      pages: {
        top_pages: window.Tracker?.getTopPages?.(10) || [],
        total_pages_tracked: trackerData?.posts_tracked || 0
      },
      daily_stats: window.Tracker?.getDailyStats?.() || [],
      hourly_stats: window.Tracker?.getHourlyStats?.() || []
    };
  },

  /**
   * Get top posts with engagement metrics
   */
  getTopPosts(limit = 5) {
    const pages = window.Tracker?.getTopPages?.(limit) || [];
    return pages.map(page => ({
      ...page,
      engagement_score: this.calculateEngagementScore(page)
    })).sort((a, b) => b.engagement_score - a.engagement_score);
  },

  /**
   * Calculate engagement score for a page
   */
  calculateEngagementScore(page) {
    let score = 0;
    if (page.views) score += page.views * 1;
    if (page.avg_time_spent) score += Math.min(page.avg_time_spent / 60, 10); // Max 10 points for time
    const avgScrollDepth = page.scroll_depth?.length ? 
      page.scroll_depth.reduce((a, b) => a + b, 0) / page.scroll_depth.length : 0;
    if (avgScrollDepth > 50) score += 5;
    return Math.round(score);
  },

  /**
   * Get traffic trend (last N days)
   */
  getTrafficTrend(days = 7) {
    const dailyStats = window.Tracker?.getDailyStats?.() || [];
    const sorted = dailyStats.sort((a, b) => new Date(a.date) - new Date(b.date));
    return sorted.slice(-days);
  },

  /**
   * Get hourly trend (24 hours)
   */
  getHourlyTrend() {
    return window.Tracker?.getHourlyStats?.() || [];
  },

  /**
   * Calculate traffic conversion rate
   */
  getConversionMetrics() {
    const summary = this.getComprehensiveSummary();
    
    return {
      github_click_rate: summary.traffic.total_views > 0 ? 
        Math.round((summary.traffic.github_clicks / summary.traffic.total_views) * 100) : 0,
      cv_download_rate: summary.traffic.total_views > 0 ? 
        Math.round((summary.traffic.cv_clicks / summary.traffic.total_views) * 100) : 0,
      contact_interaction_rate: summary.traffic.total_views > 0 ? 
        Math.round((summary.traffic.contact_interactions / summary.traffic.total_views) * 100) : 0,
      lead_conversion_rate: summary.visitors.total_visitors > 0 ? 
        Math.round(((summary.visitors.hot_leads + summary.visitors.warm_leads) / summary.visitors.total_visitors) * 100) : 0
    };
  },

  /**
   * Get traffic source breakdown
   */
  getTrafficSourceBreakdown() {
    const sources = window.Tracker?.getSummary?.()?.traffic_sources || {};
    const total = Object.values(sources).reduce((a, b) => a + b, 0);
    
    return Object.entries(sources).map(([source, count]) => ({
      source: source.charAt(0).toUpperCase() + source.slice(1),
      count,
      percentage: total > 0 ? Math.round((count / total) * 100) : 0
    })).sort((a, b) => b.count - a.count);
  },

  /**
   * Get visitor classification breakdown
   */
  getClassificationBreakdown() {
    const visitors = window.VisitorIntel?.getEnrichedVisitors?.() || [];
    const breakdown = {};
    
    visitors.forEach(visitor => {
      const classification = visitor.classification;
      breakdown[classification] = (breakdown[classification] || 0) + 1;
    });

    const total = visitors.length;
    return Object.entries(breakdown).map(([classification, count]) => ({
      classification: classification.charAt(0).toUpperCase() + classification.slice(1),
      count,
      percentage: total > 0 ? Math.round((count / total) * 100) : 0,
      emoji: window.VisitorIntel?.getClassificationEmoji?.(classification) || ''
    }));
  },

  /**
   * Get lead scoring distribution
   */
  getLeadScoreDistribution() {
    const stats = window.VisitorIntel?.getLeadStatistics?.();
    if (!stats) return [];
    
    return [
      { range: '0-25 (Cold)', count: stats.score_distribution['0-25'], color: '#999' },
      { range: '25-50 (Warm)', count: stats.score_distribution['25-50'], color: '#ff9800' },
      { range: '50-75 (Hot)', count: stats.score_distribution['50-75'], color: '#ff5722' },
      { range: '75-100 (Premium)', count: stats.score_distribution['75-100'], color: '#d32f2f' }
    ];
  },

  /**
   * Get top countries by visitor count
   */
  getTopCountries(limit = 10) {
    const visitors = window.VisitorIntel?.getAllVisitors?.() || [];
    const countries = {};
    
    visitors.forEach(visitor => {
      const country = visitor.country || 'Unknown';
      countries[country] = (countries[country] || 0) + 1;
    });

    return Object.entries(countries)
      .map(([country, count]) => ({ country, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, limit);
  },

  /**
   * Get device breakdown
   */
  getDeviceBreakdown() {
    const visitors = window.VisitorIntel?.getEnrichedVisitors?.() || [];
    const devices = {};
    
    visitors.forEach(visitor => {
      const device = visitor.device_type;
      devices[device] = (devices[device] || 0) + 1;
    });

    const total = visitors.length;
    return Object.entries(devices).map(([device, count]) => ({
      device: device.charAt(0).toUpperCase() + device.slice(1),
      count,
      percentage: total > 0 ? Math.round((count / total) * 100) : 0,
      emoji: window.VisitorIntel?.getDeviceEmoji?.(device) || ''
    }));
  },

  /**
   * Get recent high-value visitor alerts
   */
  getRecentHighValueAlerts(limit = 10) {
    const visitors = window.VisitorIntel?.getHighValueVisitors?.(50) || [];
    return visitors.slice(-limit).reverse().map(visitor => ({
      organization: visitor.organization,
      country: visitor.country,
      timestamp: visitor.timestamp,
      lead_score: window.VisitorIntel?.calculateLeadScore?.(visitor) || 0,
      is_recruiter: window.VisitorIntel?.detectRecruiter?.(visitor) || false
    }));
  },

  /**
   * Get engagement metrics per page
   */
  getPageEngagementMetrics() {
    const pages = window.Tracker?.getTopPages?.(20) || [];
    return pages.map(page => ({
      slug: page.slug,
      views: page.views,
      avg_time: Math.round(page.avg_time_spent || 0),
      avg_scroll: page.scroll_depth?.length ? 
        Math.round(page.scroll_depth.reduce((a, b) => a + b, 0) / page.scroll_depth.length) : 0,
      engagement_score: this.calculateEngagementScore(page)
    }));
  },

  /**
   * Get stats
   */
  getStats() {
    return this.getComprehensiveSummary();
  },

  /**
   * Export all analytics data
   */
  exportAnalytics() {
    return {
      summary: this.getComprehensiveSummary(),
      top_posts: this.getTopPosts(20),
      traffic_trend: this.getTrafficTrend(30),
      conversion_metrics: this.getConversionMetrics(),
      traffic_sources: this.getTrafficSourceBreakdown(),
      classifications: this.getClassificationBreakdown(),
      lead_scores: this.getLeadScoreDistribution(),
      top_countries: this.getTopCountries(20),
      devices: this.getDeviceBreakdown(),
      high_value_alerts: this.getRecentHighValueAlerts(50),
      exported_at: new Date().toISOString()
    };
  }
};

// Make sure it's globally available
window.Analytics = window.Analytics || {};
