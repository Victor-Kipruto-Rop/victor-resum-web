# Developer Intelligence Dashboard System

**Complete Analytics, Lead Scoring & Recruiter Detection for GitHub Pages Portfolios**

## 🎯 Overview

A 100% browser-based Developer Intelligence System that runs on GitHub Pages with **zero backend requirements**. Automatically tracks visitor analytics, detects recruiters, scores leads, and sends notifications via Telegram.

**Key Features:**
- 📊 Real-time analytics dashboard with Chart.js visualizations
- 🎯 Lead scoring system (0-100 scale)
- 🔴 Recruiter detection via organization keywords
- 🗺️ Geographic distribution tracking
- ⏱️ Page engagement metrics (time spent, scroll depth)
- 🔔 Telegram notifications for high-value visitors
- 🔐 Password-protected SaaS dashboard
- 🌓 Dark/light theme support
- 📱 Fully responsive (mobile, tablet, desktop)
- ✅ No backend server required - 100% GitHub Pages compatible

## 🏗️ System Architecture

### File Structure
```
resume/
├── dashboard/
│   ├── index-saas.html         # Main SaaS dashboard (password-protected)
│   ├── tracker.js              # Page view tracking & engagement metrics
│   ├── analytics.js            # Basic analytics aggregation
│   ├── analytics-advanced.js   # Advanced analytics & reporting
│   ├── visitor-intel.js        # Visitor classification & lead scoring
│   ├── blog-tracker.js         # Auto-track blog post reads
│   └── graphs.js               # Vanilla Canvas graph rendering (fallback)
├── .github/
│   └── workflows/
│       └── notify.yml          # GitHub Actions automation
└── automation/
    ├── notifier.py            # Telegram notification script
    └── config.json            # Configuration (Telegram secrets)
```

### Data Flow

```
Visitor Lands
    ↓
tracker.js logs page view
    ↓
visitor-intel.js fetches IP metadata
    ↓
Calculate lead score & recruiter probability
    ↓
Store in localStorage
    ↓
Dashboard displays data (index-saas.html)
    ↓
GitHub Actions → notify.py → Telegram notification
```

## 📊 Dashboard Features

### 1. Authentication
- Session-based password protection
- Prevents unauthorized access
- Login state persists during session
- **⚠️ IMPORTANT:** Change password `kipruto2024` before deployment

### 2. Analytics Tab
- **Stats Grid:** Total Views, GitHub Clicks, Unique Visitors, Recruiter Leads
- **Charts:**
  - Views Timeline (line chart)
  - Traffic Sources (doughnut chart)
  - Visitor Classification (pie chart)
  - Lead Scoring (bar chart)
  - 24-Hour Heatmap (bar chart)
  - Global Dashboard (radar chart)

### 3. Leads Tab
- High-value visitor tracking (score ≥50)
- CRM-style lead list with scores
- Organization, location, and device info
- Sort by lead score (hot/warm/cold)

### 4. Activity Tab
- Real-time event feed
- Page views, clicks, interactions
- Engagement milestones
- Time-stamped log

## 🔧 Core Modules

### tracker.js
**Purpose:** Comprehensive event tracking and analytics

**Key Methods:**
```javascript
// Page tracking
window.Tracker.trackPageView(slug)
window.Tracker.trackGitHubClick(slug)

// Engagement metrics
window.Tracker.trackTimeSpent(slug, seconds)
window.Tracker.trackScrollDepth(slug, percentage)

// Aggregation
window.Tracker.getDailyStats()      // Daily views by date
window.Tracker.getHourlyStats()     // Hourly breakdown
window.Tracker.getTopPages(limit)   // Top pages by views

// Data management
window.Tracker.getSummary()         // Complete summary
window.Tracker.exportData()         // Export all tracking data
window.Tracker.clearAllData()       // Clear localStorage
```

**Storage:**
- All data in `localStorage` under `TRACKING_DATA`, `DAILY_STATS`, `HOURLY_STATS` keys
- JSON serialization with automatic deserialization
- Persistent across page reloads

### visitor-intel.js
**Purpose:** Visitor classification and lead scoring

**Key Methods:**
```javascript
// Main intelligence
window.VisitorIntel.getVisitorIntel()           // Full visitor metadata

// Classification & scoring
window.VisitorIntel.calculateLeadScore(visitor) // 0-100 lead score
window.VisitorIntel.detectRecruiter(visitor)    // Boolean recruiter flag
window.VisitorIntel.categorizeLead(score)       // 'hot'|'warm'|'cold'

// Data retrieval
window.VisitorIntel.getAllVisitors()            // All visitors
window.VisitorIntel.getHighValueVisitors(50)   // Score ≥50
window.VisitorIntel.getEnrichedVisitors()       // With calculated scores
window.VisitorIntel.detectRecruiterVisits()     // All recruiter visits

// Statistics
window.VisitorIntel.getLeadStatistics()         // Lead distribution stats
window.VisitorIntel.getStatistics()             // Geographic/device stats

// Data management
window.VisitorIntel.clearData()                 // Clear localStorage
window.VisitorIntel.exportData()                // Export all visitor data
```

**Scoring Algorithm (0-100):**
- Corporate org: +40
- Academic org: +20
- Government: +25
- Desktop device: +15
- Org identified: +10
- Recruiter keywords: +25 each
- Business ISP: +10
- Targeted country (US/UK/DE/CA/AU/NL/SG): +5
- Engagement bonuses: +5-15

### analytics-advanced.js
**Purpose:** Data aggregation and advanced analytics

**Key Methods:**
```javascript
// Comprehensive reports
window.Analytics.getComprehensiveSummary()      // All metrics
window.Analytics.getTopPosts(limit)             // Top pages with engagement
window.Analytics.getConversionMetrics()         // Conversion rates
window.Analytics.getTrafficSourceBreakdown()    // Source distribution

// Classifications
window.Analytics.getClassificationBreakdown()   // Corporate/Academic/ISP breakdown
window.Analytics.getLeadScoreDistribution()     // Score distribution
window.Analytics.getTopCountries(limit)         // Geographic distribution
window.Analytics.getDeviceBreakdown()           // Desktop/Mobile/Tablet split

// Trends
window.Analytics.getTrafficTrend(days)          // Daily trend
window.Analytics.getHourlyTrend()               // 24-hour trend
window.Analytics.getPageEngagementMetrics()     // Page-level metrics

// Alerts
window.Analytics.getRecentHighValueAlerts(limit) // Recent hot leads

// Export
window.Analytics.exportAnalytics()              // Full analytics export
```

### visitor-intel.js & blog-tracker.js
**Purpose:** Auto-track blog post engagement

**Setup:**
```html
<!-- Add to blog posts -->
<script src="dashboard/blog-tracker.js"></script>

<!-- Optional: specify slug explicitly -->
<body data-blog-post="how-to-use-javascript">
```

**Automatically tracks:**
- Page views
- Time spent reading
- Scroll depth milestones
- Link clicks (especially GitHub links)
- Reading completion

## 🚀 Usage

### 1. Add Analytics to Your Pages
```html
<!-- Add to your portfolio/blog pages -->
<script src="dashboard/tracker.js"></script>
<script src="dashboard/visitor-intel.js"></script>

<!-- Optional: advanced analytics -->
<script src="dashboard/analytics-advanced.js"></script>

<!-- Optional: auto-track blog posts -->
<script src="dashboard/blog-tracker.js"></script>
```

### 2. Access the Dashboard
```
https://yourdomain.com/dashboard/index-saas.html
```
Password: `kipruto2024` (change this!)

### 3. Configure Notifications (Optional)

Add Telegram secrets to GitHub:
```
Settings → Secrets and Variables → Actions
TELEGRAM_BOT_TOKEN: your_bot_token_here
TELEGRAM_CHAT_ID: your_chat_id_here
```

The workflow will automatically notify you of:
- New blog posts
- High-value visitor arrivals
- Recruiter activity
- Weekly analytics summaries

## 📈 Data Collection Points

### Automatically Tracked
- ✅ Page views (all pages)
- ✅ Time spent on page
- ✅ Scroll depth
- ✅ Traffic source (referrer)
- ✅ GitHub link clicks
- ✅ Visitor IP metadata
- ✅ Device type (desktop/mobile/tablet)
- ✅ Organization (IP reverse lookup)
- ✅ Geographic location
- ✅ Daily/hourly aggregation

### Lead Scoring Signals
- Organization classification (corporate, academic, ISP)
- Recruiter keywords in org name
- Device type (professional = desktop)
- Geographic location
- Engagement metrics
- Interaction history

## 🔐 Security & Privacy

### What's Stored
- Page view timestamps & duration
- Device type (not fingerprint)
- Country/region (no precision)
- Sanitized IP (last octet masked)
- Organization name (from IP)

### What's NOT Stored
- ❌ Full IP address (masked to X.X.X.XXX)
- ❌ Personal identification
- ❌ Browsing history
- ❌ Email addresses
- ❌ Form submission data

### Storage Location
- 100% client-side localStorage
- No backend database
- No third-party tracking
- No cookies (session storage only)

## 🔧 Customization

### Change Password
**File:** `dashboard/index-saas.html` (line ~850)
```javascript
const DASHBOARD_PASSWORD = 'kipruto2024'; // ← Change this
```

### Customize Colors
**File:** `dashboard/index-saas.html` (CSS variables at top)
```css
:root {
  --ink:    #0a0e14;      /* Text color */
  --paper:  #f5f0e8;      /* Background */
  --accent: #c8401a;      /* Brand color */
  --blue:   #1a4fd6;      /* Chart colors */
  --green:  #16a34a;
  --red:    #dc2626;
}
```

### Adjust Lead Scoring
**File:** `dashboard/visitor-intel.js` (line ~550)
```javascript
calculateLeadScore(visitor, engagementData = {}) {
  let score = 0;
  // Adjust weights here
  score += classificationScores[visitor.classification] || 0;
  // ...
}
```

## 📊 Chart Types

- **Line Chart:** Views timeline trend
- **Doughnut Chart:** Traffic source breakdown
- **Pie Chart:** Visitor classification distribution
- **Bar Chart:** Lead score distribution, hourly heatmap
- **Radar Chart:** Multi-dimensional dashboard metrics

All charts update dynamically with theme toggle (dark/light mode).

## 🤖 GitHub Actions Automation

**File:** `.github/workflows/notify.yml`

Triggers on:
- Push to main branch with blog changes
- Manual workflow dispatch
- Scheduled daily/weekly checks

Actions:
- Detects blog post changes
- Runs Python notifier script
- Sends Telegram alerts
- Logs analytics updates
- Validates dashboard security

## 📱 Responsive Design

- **Desktop (≥1024px):** Full layout with sidebar
- **Tablet (768-1023px):** Stacked layout, optimized spacing
- **Mobile (<480px):** Single column, touch-friendly buttons

## ⚙️ Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

**Requires:**
- localStorage API
- sessionStorage API
- ES6 JavaScript
- Fetch API

## 🐛 Troubleshooting

### Dashboard shows "Visitor intelligence unavailable"
- IP API may have rate limits
- CORS blocked on file:// protocol (normal in development)
- API will work fine on https:// (production)

### Charts not displaying
- Ensure Chart.js CDN is accessible
- Check browser console for errors
- Verify theme toggle works

### Data not persisting
- Check localStorage isn't cleared
- Verify browser allows localStorage
- Check for private/incognito mode

### No Telegram notifications
- Verify `TELEGRAM_BOT_TOKEN` secret is set
- Check bot token is valid
- Ensure `TELEGRAM_CHAT_ID` is correct
- Check GitHub Actions logs for errors

## 📚 API Reference

### window.Tracker
- `trackPageView(slug)`
- `trackGitHubClick(slug)`
- `trackScrollDepth(slug, depth)`
- `trackTimeSpent(slug, seconds)`
- `trackCVDownload()`
- `trackContactInteraction()`
- `getDailyStats()`
- `getHourlyStats()`
- `getTopPages(limit)`
- `getSummary()`
- `exportData()`
- `clearAllData()`

### window.VisitorIntel
- `getVisitorIntel()`
- `getAllVisitors()`
- `getHighValueVisitors(threshold)`
- `calculateLeadScore(visitor)`
- `detectRecruiter(visitor)`
- `getLeadStatistics()`
- `getEnrichedVisitors()`
- `exportData()`
- `clearData()`

### window.Analytics
- `getComprehensiveSummary()`
- `getTopPosts(limit)`
- `getConversionMetrics()`
- `getTrafficSourceBreakdown()`
- `getLeadScoreDistribution()`
- `getTopCountries(limit)`
- `getClassificationBreakdown()`
- `exportAnalytics()`

## 🎓 Learning Resources

- [GitHub Pages Documentation](https://pages.github.com/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [localStorage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

## 📄 License

Built for personal portfolio analytics. Customize and deploy freely.

## 🤝 Contributing

To improve this system:
1. Test locally first
2. Verify localStorage data integrity
3. Test on mobile/tablet
4. Check theme toggle works
5. Validate analytics calculations

## 📧 Support

For issues or questions:
1. Check browser console for errors
2. Verify all script files are loaded
3. Check GitHub Pages is enabled
4. Review this documentation

---

**Built with ❤️ for developers who want analytics without the backend.**
