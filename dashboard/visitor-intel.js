/**
 * Developer Intelligence System - Visitor Intelligence Module
 * Detects and classifies visitor metadata (organization, location, device)
 * Uses public IP API for enrichment - NO personal identification
 * 
 * @module VisitorIntel
 */

class VisitorIntelligence {
  constructor() {
    this.storage_key = 'dashboard_visitor_intel';
    this.history_key = 'dashboard_visitor_history';
    this.api_endpoint = 'https://ipapi.co/json/';
    this.cache_duration = 3600000; // 1 hour
    this.max_history = 50;
    
    // Initialize
    this.loadStoredData();
  }

  /**
   * Main method: Get visitor intelligence
   * Fetches IP metadata and classifies visitor
   */
  async getVisitorIntel() {
    try {
      const cached = this.getCachedData();
      if (cached && !this.isCacheExpired(cached)) {
        return cached;
      }

      const ipData = await this.fetchIPData();
      if (!ipData) return this.getFallbackData();

      const intel = this.processVisitorData(ipData);
      this.cacheVisitorData(intel);
      this.addToHistory(intel);
      
      return intel;
    } catch (e) {
      console.warn('[VisitorIntel] Error fetching visitor data:', e.message);
      return this.getFallbackData();
    }
  }

  /**
   * Fetch IP metadata from public API
   */
  async fetchIPData() {
    try {
      const response = await fetch(this.api_endpoint, {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
        cache: 'no-store'
      });

      if (!response.ok) return null;
      return await response.json();
    } catch (e) {
      console.warn('[VisitorIntel] IP API error:', e.message);
      return null;
    }
  }

  /**
   * Process IP data and classify visitor
   */
  processVisitorData(ipData) {
    const now = new Date().toISOString();
    
    return {
      timestamp: now,
      ip: this.sanitizeIP(ipData.ip || 'N/A'),
      isp: ipData.org || 'Unknown ISP',
      organization: this.extractOrganization(ipData.org || ''),
      country: ipData.country_name || 'Unknown',
      country_code: ipData.country_code || 'XX',
      region: ipData.region || 'Unknown',
      city: ipData.city || 'Unknown',
      latitude: ipData.latitude || null,
      longitude: ipData.longitude || null,
      timezone: ipData.timezone || 'Unknown',
      
      // Device detection (best-effort)
      user_agent: navigator.userAgent,
      device_type: this.detectDeviceType(),
      
      // Classification
      classification: this.classifyVisitor(ipData.org || ''),
      is_vpn: this.detectVPN(ipData),
      is_proxy: this.detectProxy(ipData)
    };
  }

  /**
   * Classify visitor as corporate, academic, or individual
   */
  classifyVisitor(org) {
    const org_lower = org.toLowerCase();

    // Corporate detection
    const corporate = [
      'google', 'microsoft', 'amazon', 'meta', 'apple', 'netflix',
      'facebook', 'twitter', 'linkedin', 'uber', 'airbnb', 'stripe',
      'shopify', 'slack', 'datadog', 'elastic', 'mongodb', 'ibm',
      'oracle', 'salesforce', 'vmware', 'cisco', 'intel', 'nvidia',
      'tesla', 'github', 'gitlab', 'atlassian', 'jira', 'confluence'
    ];

    for (let corp of corporate) {
      if (org_lower.includes(corp)) return 'corporate';
    }

    // Academic detection
    if (org_lower.includes('university') || 
        org_lower.includes('college') ||
        org_lower.includes('school') ||
        org_lower.includes('.edu')) {
      return 'academic';
    }

    // Government detection
    if (org_lower.includes('government') || 
        org_lower.includes('.gov')) {
      return 'government';
    }

    // ISP detection
    if (org_lower.includes('isp') || 
        org_lower.includes('internet service') ||
        org_lower.includes('telecom')) {
      return 'isp';
    }

    return 'individual';
  }

  /**
   * Detect device type from user agent
   */
  detectDeviceType() {
    const ua = navigator.userAgent.toLowerCase();
    
    if (/mobile|android|iphone|ipod|blackberry|iemobile|opera mini/i.test(ua)) {
      if (/ipad|android(?!.*mobile)/i.test(ua)) return 'tablet';
      return 'mobile';
    }
    return 'desktop';
  }

  /**
   * Heuristic VPN detection
   */
  detectVPN(ipData) {
    const indicators = [
      ipData.org?.toLowerCase().includes('vpn'),
      ipData.org?.toLowerCase().includes('proxy'),
      ipData.org?.toLowerCase().includes('hosting'),
      ipData.org?.toLowerCase().includes('datacenter')
    ];
    return indicators.filter(Boolean).length > 0;
  }

  /**
   * Heuristic proxy detection
   */
  detectProxy(ipData) {
    const indicators = [
      ipData.org?.toLowerCase().includes('proxy'),
      ipData.org?.toLowerCase().includes('cdn'),
      ipData.org?.toLowerCase().includes('cloudflare'),
      ipData.org?.toLowerCase().includes('fastly')
    ];
    return indicators.filter(Boolean).length > 0;
  }

  /**
   * Sanitize IP address for privacy
   * Show partial IP: X.X.X.XXX
   */
  sanitizeIP(ip) {
    if (!ip || ip === 'N/A') return 'N/A';
    const parts = ip.split('.');
    if (parts.length === 4) {
      parts[3] = 'XXX';
      return parts.join('.');
    }
    return 'N/A';
  }

  /**
   * Cache visitor data locally
   */
  cacheVisitorData(intel) {
    const data = {
      ...intel,
      cached_at: Date.now()
    };
    localStorage.setItem(this.storage_key, JSON.stringify(data));
  }

  /**
   * Get cached visitor data
   */
  getCachedData() {
    const cached = localStorage.getItem(this.storage_key);
    return cached ? JSON.parse(cached) : null;
  }

  /**
   * Check if cache expired
   */
  isCacheExpired(cached) {
    if (!cached.cached_at) return true;
    return (Date.now() - cached.cached_at) > this.cache_duration;
  }

  /**
   * Fallback data when API unavailable
   */
  getFallbackData() {
    return {
      timestamp: new Date().toISOString(),
      ip: 'N/A',
      isp: 'API Unavailable',
      organization: 'Direct Connection',
      country: 'Unknown',
      country_code: 'XX',
      region: 'Unknown',
      city: 'Unknown',
      latitude: null,
      longitude: null,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || 'Unknown',
      user_agent: navigator.userAgent,
      device_type: this.detectDeviceType(),
      classification: 'individual',
      is_vpn: false,
      is_proxy: false,
      api_available: false
    };
  }

  /**
   * Add visitor to history for trend analysis
   */
  addToHistory(intel) {
    let history = this.getHistory();
    
    // Add new visitor
    history.push({
      ...intel,
      id: Date.now()
    });

    // Keep only last N visitors
    if (history.length > this.max_history) {
      history = history.slice(-this.max_history);
    }

    localStorage.setItem(this.history_key, JSON.stringify(history));
  }

  /**
   * Get visitor history
   */
  getHistory() {
    const history = localStorage.getItem(this.history_key);
    return history ? JSON.parse(history) : [];
  }

  /**
   * Get visitor statistics from history
   */
  getStatistics() {
    const history = this.getHistory();
    if (history.length === 0) {
      return this.getEmptyStats();
    }

    const classifications = {};
    const countries = {};
    const devices = {};

    history.forEach(visitor => {
      // Classification stats
      classifications[visitor.classification] = 
        (classifications[visitor.classification] || 0) + 1;

      // Country stats
      countries[visitor.country] = 
        (countries[visitor.country] || 0) + 1;

      // Device stats
      devices[visitor.device_type] = 
        (devices[visitor.device_type] || 0) + 1;
    });

    return {
      total_visitors: history.length,
      unique_countries: Object.keys(countries).length,
      unique_devices: Object.keys(devices).length,
      
      classifications,
      countries,
      devices,
      
      vpn_detected: history.filter(v => v.is_vpn).length,
      proxy_detected: history.filter(v => v.is_proxy).length,
      
      last_updated: history[history.length - 1]?.timestamp
    };
  }

  /**
   * Empty statistics object
   */
  getEmptyStats() {
    return {
      total_visitors: 0,
      unique_countries: 0,
      unique_devices: 0,
      classifications: {},
      countries: {},
      devices: {},
      vpn_detected: 0,
      proxy_detected: 0,
      last_updated: null
    };
  }

  /**
   * Clear all visitor data
   */
  clearData() {
    localStorage.removeItem(this.storage_key);
    localStorage.removeItem(this.history_key);
  }

  /**
   * Export visitor data
   */
  exportData() {
    return {
      current: this.getCachedData(),
      history: this.getHistory(),
      statistics: this.getStatistics()
    };
  }

  /**
   * Load stored data on init
   */
  loadStoredData() {
    // Trigger initial fetch after DOM ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => this.getVisitorIntel(), 500);
      });
    } else {
      setTimeout(() => this.getVisitorIntel(), 500);
    }
  }

  /**
   * Format visitor data for display
   */
  formatForDisplay(intel) {
    if (!intel) return null;

    return {
      ip: intel.ip,
      location: `${intel.city}, ${intel.country}`,
      organization: intel.organization,
      classification: intel.classification,
      device: intel.device_type,
      timezone: intel.timezone,
      is_corporate: intel.classification === 'corporate',
      is_academic: intel.classification === 'academic',
      security_flags: {
        vpn: intel.is_vpn,
        proxy: intel.is_proxy
      }
    };
  }

  /**
   * Get classification emoji
   */
  getClassificationEmoji(classification) {
    const map = {
      'corporate': '🏢',
      'academic': '🎓',
      'government': '🏛️',
      'isp': '🌐',
      'individual': '👤'
    };
    return map[classification] || '👤';
  }

  /**
   * Calculate lead score (0-100)
   * Based on visitor behavior, classification, and engagement
   */
  calculateLeadScore(visitor, engagementData = {}) {
    let score = 0;

    // Classification scoring
    const classificationScores = {
      'corporate': 40,
      'government': 25,
      'academic': 20,
      'isp': 5,
      'individual': 0
    };
    score += classificationScores[visitor.classification] || 0;

    // Device scoring (desktop more likely to be professional)
    if (visitor.device_type === 'desktop') score += 15;

    // Organization name bonus
    const org = (visitor.organization || '').toLowerCase();
    if (org && org !== 'unknown' && org !== 'direct connection') {
      score += 10;
    }

    // Known recruiter/HR companies
    const recruiterKeywords = [
      'linkedin', 'indeed', 'greenhouse', 'lever', 'workday',
      'talent', 'recruiter', 'staffing', 'hr', 'human resources',
      'recruitment', 'jobs', 'careers', 'hiring'
    ];
    
    recruiterKeywords.forEach(keyword => {
      if (org.includes(keyword)) score += 25;
    });

    // Country scoring (top tech hubs)
    const highValueCountries = ['US', 'GB', 'DE', 'CA', 'AU', 'NL', 'SG'];
    if (highValueCountries.includes(visitor.country_code)) score += 5;

    // Engagement bonuses
    if (engagementData.page_views > 1) score += 5;
    if (engagementData.time_spent_minutes > 2) score += 8;
    if (engagementData.github_clicks > 0) score += 10;
    if (engagementData.cv_downloads > 0) score += 15;

    // Returning visitor bonus
    if (engagementData.returning_visitor) score += 5;

    return Math.min(score, 100);
  }

  /**
   * Categorize lead by score
   */
  categorizeLead(score) {
    if (score >= 50) return 'hot';
    if (score >= 25) return 'warm';
    return 'cold';
  }

  /**
   * Detect if visitor is likely a recruiter
   */
  detectRecruiter(visitor) {
    const recruiterIndicators = [
      (visitor.organization || '').toLowerCase().includes('linkedin'),
      (visitor.organization || '').toLowerCase().includes('recruiter'),
      (visitor.organization || '').toLowerCase().includes('talent'),
      (visitor.organization || '').toLowerCase().includes('staffing'),
      (visitor.organization || '').toLowerCase().includes('jobs'),
      (visitor.organization || '').toLowerCase().includes('hiring'),
      (visitor.organization || '').toLowerCase().includes('indeed'),
      (visitor.isp || '').toLowerCase().includes('talent'),
      visitor.classification === 'corporate'
    ];

    const recruitmentOrgs = [
      'google', 'microsoft', 'amazon', 'meta', 'apple', 'netflix',
      'uber', 'stripe', 'shopify', 'tesla', 'github', 'gitlab'
    ];

    const isKnownTechCompany = recruitmentOrgs.some(
      company => (visitor.organization || '').toLowerCase().includes(company)
    );

    return (recruiterIndicators.filter(Boolean).length >= 2) || isKnownTechCompany;
  }

  /**
   * Get all visitors (from history)
   */
  getAllVisitors() {
    return this.getHistory();
  }

  /**
   * Get high-value visitors (leads with score >= threshold)
   */
  getHighValueVisitors(threshold = 50) {
    const history = this.getHistory();
    return history.filter(visitor => {
      const score = this.calculateLeadScore(visitor);
      return score >= threshold;
    }).sort((a, b) => {
      const scoreA = this.calculateLeadScore(a);
      const scoreB = this.calculateLeadScore(b);
      return scoreB - scoreA;
    });
  }

  /**
   * Detect recruiter visits
   */
  detectRecruiterVisits() {
    const history = this.getHistory();
    return history.filter(visitor => this.detectRecruiter(visitor));
  }

  /**
   * Get visitor enriched data with lead scores
   */
  getEnrichedVisitors() {
    const history = this.getHistory();
    return history.map(visitor => ({
      ...visitor,
      lead_score: this.calculateLeadScore(visitor),
      lead_category: this.categorizeLead(this.calculateLeadScore(visitor)),
      is_recruiter: this.detectRecruiter(visitor),
      classification_emoji: this.getClassificationEmoji(visitor.classification),
      device_emoji: this.getDeviceEmoji(visitor.device_type)
    }));
  }

  /**
   * Get lead scoring statistics
   */
  getLeadStatistics() {
    const enriched = this.getEnrichedVisitors();
    
    return {
      total_visitors: enriched.length,
      hot_leads: enriched.filter(v => v.lead_category === 'hot').length,
      warm_leads: enriched.filter(v => v.lead_category === 'warm').length,
      cold_leads: enriched.filter(v => v.lead_category === 'cold').length,
      recruiters_detected: enriched.filter(v => v.is_recruiter).length,
      avg_score: Math.round(enriched.reduce((sum, v) => sum + v.lead_score, 0) / enriched.length || 0),
      score_distribution: {
        '0-25': enriched.filter(v => v.lead_score < 25).length,
        '25-50': enriched.filter(v => v.lead_score >= 25 && v.lead_score < 50).length,
        '50-75': enriched.filter(v => v.lead_score >= 50 && v.lead_score < 75).length,
        '75-100': enriched.filter(v => v.lead_score >= 75).length
      }
    };
  }

  /**
   * Format lead data for display
   */
  formatLeadForDisplay(visitor) {
    const leadScore = this.calculateLeadScore(visitor);
    const category = this.categorizeLead(leadScore);
    const isRecruiter = this.detectRecruiter(visitor);

    return {
      organization: visitor.organization,
      location: `${visitor.city}, ${visitor.country}`,
      classification: `${this.getClassificationEmoji(visitor.classification)} ${visitor.classification}`,
      device: `${this.getDeviceEmoji(visitor.device_type)} ${visitor.device_type}`,
      lead_score: `${leadScore}%`,
      lead_category: category.toUpperCase(),
      is_recruiter: isRecruiter ? '🔴 Recruiter' : '',
      timestamp: new Date(visitor.timestamp).toLocaleString()
    };
  }
}

// Initialize globally
const VisitorIntel = new VisitorIntelligence();

// Export for use
window.VisitorIntelligence = VisitorIntelligence;
window.VisitorIntel = VisitorIntel;
