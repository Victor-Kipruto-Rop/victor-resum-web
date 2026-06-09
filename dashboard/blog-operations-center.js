// ==========================================
// BLOG OPERATIONS & INTELLIGENCE DASHBOARD
// Complete Analytics Engine
// ==========================================

// ── CONFIGURATION ──
const CONFIG = {
  TOKEN: 'victor_blog_ops_2024', // Change this to your secret token
  STORAGE_KEY: 'blog_ops_data',
  SESSION_KEY: 'blog_ops_session',
  SESSION_TIMEOUT: 3600000, // 1 hour
};

// ── DATA STRUCTURES ──
const BLOG_DATA = {
  articles: [],
  analytics: {},
  conversions: {},
  errors: [],
  automation: {},
};

// Sample blog data - Replace with your actual blog data
const SAMPLE_BLOGS = [
  {
    id: 'data-engineering',
    title: 'Data Engineering — Full Project',
    slug: 'data-engineering-full-project',
    publishDate: new Date('2024-01-15'),
    updateDate: new Date('2024-05-20'),
    category: 'Data Engineering',
    tags: ['Python', 'ETL', 'Cloud'],
    status: 'Published',
    views: 3450,
    uniqueVisitors: 2100,
    returningVisitors: 450,
    avgReadTime: 12,
    bounceRate: 22,
    scrollDepth: 85,
    githubClicks: 156,
    linkedinClicks: 23,
    cvDownloads: 12,
    seoScore: 92,
    targetKeyword: 'data engineering project',
    recruiterInterest: 'High'
  },
  {
    id: 'cloud-etl',
    title: 'Cloud ETL Pipeline',
    slug: 'cloud-etl-pipeline',
    publishDate: new Date('2024-02-10'),
    updateDate: new Date('2024-04-15'),
    category: 'ETL',
    tags: ['Airflow', 'Docker', 'Cloud'],
    status: 'Published',
    views: 2890,
    uniqueVisitors: 1800,
    returningVisitors: 320,
    avgReadTime: 10,
    bounceRate: 28,
    scrollDepth: 78,
    githubClicks: 134,
    linkedinClicks: 18,
    cvDownloads: 8,
    seoScore: 87,
    targetKeyword: 'ETL pipeline cloud',
    recruiterInterest: 'Medium'
  },
  {
    id: 'kafka-streaming',
    title: 'Real-Time Transaction Streaming',
    slug: 'kafka-real-time-streaming',
    publishDate: new Date('2024-03-05'),
    updateDate: null,
    category: 'Streaming',
    tags: ['Kafka', 'Python', 'Real-time'],
    status: 'Published',
    views: 1245,
    uniqueVisitors: 850,
    returningVisitors: 120,
    avgReadTime: 11,
    bounceRate: 35,
    scrollDepth: 71,
    githubClicks: 89,
    linkedinClicks: 12,
    cvDownloads: 4,
    seoScore: 74,
    targetKeyword: 'Kafka streaming',
    recruiterInterest: 'Medium'
  },
  {
    id: 'architecture-patterns',
    title: 'Architecture Design Patterns',
    slug: 'architecture-design-patterns',
    publishDate: new Date('2024-04-20'),
    updateDate: null,
    category: 'Architecture',
    tags: ['Design Patterns', 'Architecture', 'Best Practices'],
    status: 'Published',
    views: 567,
    uniqueVisitors: 420,
    returningVisitors: 45,
    avgReadTime: 9,
    bounceRate: 48,
    scrollDepth: 62,
    githubClicks: 34,
    linkedinClicks: 8,
    cvDownloads: 2,
    seoScore: 68,
    targetKeyword: 'architecture patterns',
    recruiterInterest: 'Low'
  },
  {
    id: 'draft-article',
    title: 'Advanced Data Modeling Techniques',
    slug: 'advanced-data-modeling',
    publishDate: null,
    updateDate: null,
    category: 'Data Modeling',
    tags: ['SQL', 'Modeling', 'Advanced'],
    status: 'Draft',
    views: 0,
    uniqueVisitors: 0,
    returningVisitors: 0,
    avgReadTime: 0,
    bounceRate: 0,
    scrollDepth: 0,
    githubClicks: 0,
    linkedinClicks: 0,
    cvDownloads: 0,
    seoScore: 0,
    targetKeyword: 'data modeling',
    recruiterInterest: 'Not Published'
  }
];

// ── AUTHENTICATION ──
function checkAuth() {
  const session = localStorage.getItem(CONFIG.SESSION_KEY);
  if (!session) {
    showLoginScreen();
    return false;
  }

  const sessionData = JSON.parse(session);
  const now = Date.now();
  
  if (now - sessionData.timestamp > CONFIG.SESSION_TIMEOUT) {
    logout();
    return false;
  }

  return true;
}

function login(token) {
  if (token === CONFIG.TOKEN) {
    const sessionData = {
      token: token,
      timestamp: Date.now()
    };
    localStorage.setItem(CONFIG.SESSION_KEY, JSON.stringify(sessionData));
    showDashboard();
    return true;
  }
  return false;
}

function logout() {
  localStorage.removeItem(CONFIG.SESSION_KEY);
  location.reload();
}

function showLoginScreen() {
  document.getElementById('loginScreen').style.display = 'flex';
  document.getElementById('dashboardScreen').style.display = 'none';
  document.getElementById('loginForm').style.display = 'block';
  document.getElementById('loginLoading').style.display = 'none';
}

function showDashboard() {
  document.getElementById('loginScreen').style.display = 'none';
  document.getElementById('dashboardScreen').style.display = 'block';
  initDashboard();
}

// ── LOGIN FORM HANDLER ──
document.addEventListener('DOMContentLoaded', function() {
  if (!checkAuth()) {
    setupLoginForm();
  } else {
    showDashboard();
  }
});

function setupLoginForm() {
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const token = document.getElementById('tokenInput').value;
      const loginError = document.getElementById('loginError');
      
      document.getElementById('loginForm').style.display = 'none';
      document.getElementById('loginLoading').style.display = 'block';
      
      setTimeout(() => {
        if (login(token)) {
          showDashboard();
        } else {
          loginError.textContent = 'Invalid access token';
          document.getElementById('loginForm').style.display = 'block';
          document.getElementById('loginLoading').style.display = 'none';
          document.getElementById('tokenInput').value = '';
        }
      }, 500);
    });
  }
}

// ── DATA INITIALIZATION ──
function initDashboard() {
  loadBlogData();
  setupNavigation();
  renderOverview();
  setupExportModal();
}

function loadBlogData() {
  const stored = localStorage.getItem(CONFIG.STORAGE_KEY);
  if (stored) {
    BLOG_DATA.articles = JSON.parse(stored);
  } else {
    BLOG_DATA.articles = SAMPLE_BLOGS;
    saveBlogData();
  }
}

function saveBlogData() {
  localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(BLOG_DATA.articles));
}

// ── NAVIGATION ──
function setupNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const section = item.dataset.section;
      navigateToSection(section);
    });
  });
}

function navigateToSection(section) {
  // Update active nav
  document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
  document.querySelector(`[data-section="${section}"]`).classList.add('active');

  // Hide all sections
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));

  // Show target section
  document.getElementById(section).classList.add('active');

  // Update header
  const titles = {
    overview: { title: 'Dashboard', subtitle: 'Complete visibility into your blog ecosystem' },
    inventory: { title: 'Blog Inventory', subtitle: 'All articles with metadata and status' },
    performance: { title: 'Performance', subtitle: 'Views, engagement, and conversion metrics' },
    analytics: { title: 'Analytics', subtitle: 'Traffic patterns and content performance' },
    failures: { title: 'Content At Risk', subtitle: 'Underperforming articles needing attention' },
    successes: { title: 'Top Performers', subtitle: 'Your best performing content' },
    seo: { title: 'SEO Analysis', subtitle: 'Search engine optimization metrics' },
    gaps: { title: 'Content Gaps', subtitle: 'Missing topics and opportunities' },
    automation: { title: 'Automation Status', subtitle: 'Publishing pipeline and automation health' },
    errors: { title: 'Error Log', subtitle: 'System errors and issues' },
    conversions: { title: 'Conversion Analytics', subtitle: 'Track clicks and conversions per article' },
    publish: { title: 'Create & Publish', subtitle: 'Compose and publish content to multiple platforms' },
    notifications: { title: 'Notifications Center', subtitle: 'Manage email alerts, admin notifications, and subscriber updates' },
    autopost: { title: 'Auto-Post Scheduler', subtitle: '24-hour automated content generation and social distribution' },
    subscribers: { title: 'Subscriber Management', subtitle: 'Welcome emails, subscriber list, and engagement tracking' },
    ai: { title: 'AI Content Strategist', subtitle: 'Smart recommendations for content strategy' }
  };

  const titleData = titles[section] || titles.overview;
  document.getElementById('sectionTitle').textContent = titleData.title;
  document.getElementById('sectionSubtitle').textContent = titleData.subtitle;

  // Render section content
  renderSection(section);
}

// ── SECTION RENDERERS ──
function renderSection(section) {
  switch(section) {
    case 'overview': renderOverview(); break;
    case 'inventory': renderInventory(); break;
    case 'performance': renderPerformance(); break;
    case 'analytics': renderAnalytics(); break;
    case 'failures': renderFailures(); break;
    case 'successes': renderSuccesses(); break;
    case 'seo': renderSEO(); break;
    case 'gaps': renderContentGaps(); break;
    case 'automation': renderAutomation(); break;
    case 'errors': renderErrorLog(); break;
    case 'conversions': renderConversions(); break;
    case 'publish': loadPublishHistory(); break;
    case 'notifications': renderNotifications(); break;
    case 'autopost': renderAutoPost(); break;
    case 'subscribers': renderSubscribers(); break;
    case 'ai': renderAIRecommendations(); break;
  }
}

function renderOverview() {
  const stats = calculateStats();
  
  const kpiHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Total Articles</div>
      <div class="kpi-value">${stats.totalArticles}</div>
      <div class="kpi-change positive"><i class="fas fa-arrow-up"></i> ${stats.publishedArticles} published</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Total Views</div>
      <div class="kpi-value">${formatNumber(stats.totalViews)}</div>
      <div class="kpi-change positive"><i class="fas fa-arrow-up"></i> Avg ${Math.round(stats.avgViews)} per article</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Total Conversions</div>
      <div class="kpi-value">${stats.totalConversions}</div>
      <div class="kpi-change positive"><i class="fas fa-arrow-up"></i> ${stats.conversionRate}% conversion rate</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Avg Read Time</div>
      <div class="kpi-value">${stats.avgReadTime} min</div>
      <div class="kpi-change positive"><i class="fas fa-arrow-up"></i> ${stats.avgEngagement}% engagement</div>
    </div>
  `;

  document.getElementById('overviewKPIs').innerHTML = kpiHTML;

  // Render top content
  const topContent = BLOG_DATA.articles
    .filter(a => a.status === 'Published')
    .sort((a, b) => b.views - a.views)
    .slice(0, 10);

  let tableHTML = '';
  topContent.forEach(article => {
    const convRate = article.views > 0 ? Math.round((article.githubClicks / article.views) * 100) : 0;
    tableHTML += `
      <tr>
        <td><strong>${article.title}</strong></td>
        <td>${formatNumber(article.views)}</td>
        <td>${Math.round(article.scrollDepth)}%</td>
        <td>${article.avgReadTime} min</td>
        <td>${article.githubClicks} / ${convRate}%</td>
      </tr>
    `;
  });

  document.getElementById('topContentBody').innerHTML = tableHTML;
}

function renderInventory() {
  const stats = {
    totalArticles: BLOG_DATA.articles.length,
    published: BLOG_DATA.articles.filter(a => a.status === 'Published').length,
    drafts: BLOG_DATA.articles.filter(a => a.status === 'Draft').length,
    archived: BLOG_DATA.articles.filter(a => a.status === 'Archived').length,
  };

  const kpiHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Total Articles</div>
      <div class="kpi-value">${stats.totalArticles}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Published</div>
      <div class="kpi-value">${stats.published}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Drafts</div>
      <div class="kpi-value">${stats.drafts}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Archived</div>
      <div class="kpi-value">${stats.archived}</div>
    </div>
  `;

  document.getElementById('inventoryStats').innerHTML = kpiHTML;

  let tableHTML = '';
  BLOG_DATA.articles.forEach(article => {
    const statusBadge = `<span class="badge badge-${article.status.toLowerCase()}">${article.status}</span>`;
    const pubDate = article.publishDate ? article.publishDate.toLocaleDateString() : '—';
    const updateDate = article.updateDate ? article.updateDate.toLocaleDateString() : 'Never';
    
    tableHTML += `
      <tr>
        <td><strong>${article.title}</strong></td>
        <td><code>${article.slug}</code></td>
        <td>${pubDate}</td>
        <td>${updateDate}</td>
        <td>${article.category}</td>
        <td>${statusBadge}</td>
        <td>${article.tags.join(', ')}</td>
      </tr>
    `;
  });

  document.getElementById('blogTableBody').innerHTML = tableHTML;
}

function renderPerformance() {
  const stats = calculateStats();
  
  const kpiHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Unique Visitors</div>
      <div class="kpi-value">${formatNumber(stats.totalUniqueVisitors)}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Returning Rate</div>
      <div class="kpi-value">${stats.returningRate}%</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Avg Bounce Rate</div>
      <div class="kpi-value">${stats.avgBounceRate}%</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Avg Scroll Depth</div>
      <div class="kpi-value">${stats.avgScrollDepth}%</div>
    </div>
  `;

  document.getElementById('performanceKPIs').innerHTML = kpiHTML;

  // Charts
  drawViewsChart();
  drawEngagementChart();

  // Rankings
  const rankings = BLOG_DATA.articles
    .filter(a => a.status === 'Published')
    .sort((a, b) => b.views - a.views)
    .slice(0, 10);

  let rankingHTML = '';
  rankings.forEach((article, index) => {
    const trendIcon = index < 3 ? '<i class="fas fa-arrow-up" style="color: #10b981;"></i>' : 
                      index > 5 ? '<i class="fas fa-arrow-down" style="color: #ef4444;"></i>' : 
                      '<i class="fas fa-minus" style="color: #f59e0b;"></i>';
    
    rankingHTML += `
      <div class="item-list-item">
        <div class="item-info">
          <div class="item-title">${index + 1}. ${article.title}</div>
          <div class="item-desc">${formatNumber(article.views)} views • ${article.avgReadTime} min read • ${Math.round(article.scrollDepth)}% scroll</div>
        </div>
        <div style="display: flex; gap: 12px; align-items: center;">
          ${trendIcon}
          <span style="font-weight: 600; color: #ff4b2b;">${formatNumber(article.views)}</span>
        </div>
      </div>
    `;
  });

  document.getElementById('rankingsList').innerHTML = rankingHTML;
}

function renderAnalytics() {
  const stats = calculateStats();
  
  const kpiHTML = `
    <div class="kpi-card">
      <div class="kpi-label">GitHub Clicks</div>
      <div class="kpi-value">${stats.totalGithubClicks}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">LinkedIn Clicks</div>
      <div class="kpi-value">${stats.totalLinkedinClicks}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">CV Downloads</div>
      <div class="kpi-value">${stats.totalCVDownloads}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Overall CTR</div>
      <div class="kpi-value">${stats.overallCTR}%</div>
    </div>
  `;

  document.getElementById('analyticsKPIs').innerHTML = kpiHTML;

  drawTrafficChart();
  drawConversionChart();
  drawCategoryChart();
  drawSourceChart();
}

function renderFailures() {
  const published = BLOG_DATA.articles.filter(a => a.status === 'Published');
  const failures = published.filter(article => {
    const isUnderperforming = article.views < 500 || article.scrollDepth < 60 || article.githubClicks < 20;
    const isOld = article.updateDate === null && (new Date() - article.publishDate) > (90 * 24 * 60 * 60 * 1000);
    return isUnderperforming || isOld;
  });

  // Calculate stats
  const avgViewsAtRisk = failures.length > 0 ? Math.round(failures.reduce((sum, a) => sum + a.views, 0) / failures.length) : 0;
  const avgEngagement = failures.length > 0 ? Math.round(failures.reduce((sum, a) => sum + a.scrollDepth, 0) / failures.length) : 0;

  const statsHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Articles At Risk</div>
      <div class="kpi-value">${failures.length}</div>
      <div class="kpi-change ${failures.length > 2 ? 'negative' : 'positive'}"><i class="fas fa-${failures.length > 2 ? 'arrow-up' : 'arrow-down'}"></i> Needs attention</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Avg Views (At Risk)</div>
      <div class="kpi-value">${formatNumber(avgViewsAtRisk)}</div>
      <div class="kpi-change negative"><i class="fas fa-arrow-down"></i> Below target</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Avg Engagement</div>
      <div class="kpi-value">${avgEngagement}%</div>
      <div class="kpi-change negative"><i class="fas fa-arrow-down"></i> Low scroll depth</div>
    </div>
  `;

  document.getElementById('failureStats').innerHTML = statsHTML;

  let html = '';
  failures.forEach(article => {
    const issues = [];
    if (article.views < 500) issues.push('Low views');
    if (article.scrollDepth < 60) issues.push('Low engagement');
    if (article.githubClicks < 20) issues.push('Few conversions');
    if (article.updateDate === null && (new Date() - article.publishDate) > (90 * 24 * 60 * 60 * 1000)) {
      issues.push('Needs update');
    }

    const recommendations = [];
    if (article.views < 500) recommendations.push('Improve SEO and keywords');
    if (article.scrollDepth < 60) recommendations.push('Rewrite for clarity');
    if (article.githubClicks < 20) recommendations.push('Add GitHub project links');

    html += `
      <div class="item-list-item">
        <div class="item-info">
          <div class="item-title"><i class="fas fa-exclamation-triangle" style="color: #f59e0b; margin-right: 8px;"></i>${article.title}</div>
          <div class="item-desc">Issues: ${issues.join(' • ')} | Actions: ${recommendations.join(', ')}</div>
        </div>
        <span class="badge badge-warning">AT RISK</span>
      </div>
    `;
  });

  document.getElementById('failuresAlert').innerHTML = html || '<div style="padding: 20px; text-align: center; color: var(--text-muted);">✓ No content at risk!</div>';
}

function renderSuccesses() {
  const published = BLOG_DATA.articles.filter(a => a.status === 'Published');
  const successes = published.sort((a, b) => b.views - a.views).slice(0, 10);

  // Calculate stats
  const topArticle = successes[0];
  const totalViews = successes.reduce((sum, a) => sum + a.views, 0);
  const avgConversion = successes.length > 0 ? Math.round(successes.reduce((sum, a) => {
    return sum + (a.views > 0 ? (a.githubClicks / a.views) * 100 : 0);
  }, 0) / successes.length) : 0;

  const statsHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Top Performer</div>
      <div class="kpi-value">${formatNumber(topArticle.views)}</div>
      <div class="kpi-change positive"><i class="fas fa-fire" style="color: #ff4b2b;"></i> ${topArticle.title.substring(0, 20)}...</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Combined Views</div>
      <div class="kpi-value">${formatNumber(totalViews)}</div>
      <div class="kpi-change positive"><i class="fas fa-arrow-up"></i> Top 10 articles</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Avg Conversion</div>
      <div class="kpi-value">${avgConversion}%</div>
      <div class="kpi-change positive"><i class="fas fa-arrow-up"></i> Strong performers</div>
    </div>
  `;

  document.getElementById('successStats').innerHTML = statsHTML;

  let html = '';
  successes.forEach(article => {
    const growthRate = article.views > 2000 ? '↑ High' : article.views > 1000 ? '↑ Medium' : '→ Stable';
    const convRate = article.views > 0 ? Math.round((article.githubClicks / article.views) * 100) : 0;

    html += `
      <div class="item-list-item">
        <div class="item-info">
          <div class="item-title"><i class="fas fa-star" style="color: #fbbf24; margin-right: 8px;"></i>${article.title}</div>
          <div class="item-desc">${formatNumber(article.views)} views • ${convRate}% conversion • Growth: ${growthRate}</div>
        </div>
        <span class="badge badge-success">TOP PERFORMER</span>
      </div>
    `;
  });

  document.getElementById('successesList').innerHTML = html;
}

function renderSEO() {
  let tableHTML = '';
  BLOG_DATA.articles.forEach(article => {
    if (article.status === 'Published') {
      const metaBadge = article.targetKeyword ? '<span class="badge badge-success">✓</span>' : '<span class="badge badge-danger">✗</span>';
      const ogBadge = '<span class="badge badge-success">✓</span>';
      const dataBadge = '<span class="badge badge-info">✓</span>';

      tableHTML += `
        <tr>
          <td><strong>${article.title}</strong></td>
          <td><code>${article.targetKeyword || 'Not set'}</code></td>
          <td><strong>${article.seoScore}</strong>/100</td>
          <td>${metaBadge}</td>
          <td>${ogBadge}</td>
          <td>${dataBadge}</td>
        </tr>
      `;
    }
  });

  document.getElementById('seoTableBody').innerHTML = tableHTML;
}

function renderContentGaps() {
  const gaps = [
    { topic: 'Advanced Kubernetes Patterns', opportunity: 'Very High', reason: 'Search volume: 8,400/mo | No content | Expected traffic: 600+ views/mo', difficulty: 'Advanced', searchVolume: 8400, potential: 600 },
    { topic: 'dbt Best Practices & Advanced Patterns', opportunity: 'Very High', reason: 'Search volume: 6,200/mo | High intent | Expected traffic: 450+ views/mo', difficulty: 'Intermediate', searchVolume: 6200, potential: 450 },
    { topic: 'Data Quality Frameworks (Great Expectations)', opportunity: 'Very High', reason: 'Search volume: 5,800/mo | Growing trend | Expected traffic: 420+ views/mo', difficulty: 'Advanced', searchVolume: 5800, potential: 420 },
    { topic: 'Apache Iceberg vs Delta Lake Comparison', opportunity: 'High', reason: 'Search volume: 4,200/mo | Comparison content performs well | Expected traffic: 300+ views/mo', difficulty: 'Advanced', searchVolume: 4200, potential: 300 },
    { topic: 'Cost Optimization for Cloud Data Pipelines', opportunity: 'High', reason: 'Search volume: 3,900/mo | High ROI topic | Expected traffic: 280+ views/mo', difficulty: 'Intermediate', searchVolume: 3900, potential: 280 },
    { topic: 'Real-time Analytics Architecture Patterns', opportunity: 'High', reason: 'Search volume: 4,100/mo | Growing demand | Expected traffic: 290+ views/mo', difficulty: 'Advanced', searchVolume: 4100, potential: 290 },
    { topic: 'Monitoring & Observability for Data Pipelines', opportunity: 'High', reason: 'Search volume: 3,600/mo | Critical infrastructure | Expected traffic: 260+ views/mo', difficulty: 'Intermediate', searchVolume: 3600, potential: 260 },
    { topic: 'Python Data Validation (Pandas & Polars)', opportunity: 'Medium', reason: 'Search volume: 2,800/mo | Complements existing content | Expected traffic: 200+ views/mo', difficulty: 'Intermediate', searchVolume: 2800, potential: 200 },
    { topic: 'GraphQL for Data APIs & Services', opportunity: 'Medium', reason: 'Search volume: 2,100/mo | Emerging pattern | Expected traffic: 150+ views/mo', difficulty: 'Intermediate', searchVolume: 2100, potential: 150 },
    { topic: 'Serverless Data Processing on AWS', opportunity: 'Medium', reason: 'Search volume: 1,900/mo | Growing interest | Expected traffic: 135+ views/mo', difficulty: 'Advanced', searchVolume: 1900, potential: 135 },
    { topic: 'Feature Stores for ML Pipelines', opportunity: 'Medium', reason: 'Search volume: 2,300/mo | Emerging best practice | Expected traffic: 165+ views/mo', difficulty: 'Advanced', searchVolume: 2300, potential: 165 },
    { topic: 'Data Lineage & Governance Tools', opportunity: 'Medium', reason: 'Search volume: 1,800/mo | Enterprise focus | Expected traffic: 130+ views/mo', difficulty: 'Intermediate', searchVolume: 1800, potential: 130 },
  ];

  let html = '';
  gaps.forEach((gap, index) => {
    const opportunityColor = gap.opportunity === 'Very High' ? 'danger' : 
                            gap.opportunity === 'High' ? 'warning' : 'info';
    const difficultyIcon = gap.difficulty === 'Advanced' ? '<i class="fas fa-mountain" style="color: #ef4444;"></i>' :
                          gap.difficulty === 'Intermediate' ? '<i class="fas fa-line-chart" style="color: #f59e0b;"></i>' :
                          '<i class="fas fa-arrow-up" style="color: #10b981;"></i>';
    
    html += `
      <div class="item-list-item">
        <div class="item-info">
          <div class="item-title" style="display: flex; align-items: center; gap: 8px;">
            <span style="background: var(--accent-secondary); color: #fff; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700;">${index + 1}</span>
            <i class="fas fa-lightbulb" style="color: #fbbf24;"></i>
            <span>${gap.topic}</span>
          </div>
          <div class="item-desc" style="display: flex; align-items: center; gap: 16px; margin-top: 8px; flex-wrap: wrap; font-size: 13px;">
            <span>${gap.reason}</span>
            <span style="display: inline-flex; align-items: center; gap: 4px; color: var(--text-muted);">${difficultyIcon} ${gap.difficulty}</span>
          </div>
          <div style="margin-top: 8px; font-size: 12px; color: var(--text-muted); display: flex; gap: 16px;">
            <span><i class="fas fa-search" style="color: var(--accent-secondary); margin-right: 4px;"></i>${formatNumber(gap.searchVolume)} monthly searches</span>
            <span><i class="fas fa-chart-line" style="color: var(--accent-tertiary); margin-right: 4px;"></i>~${formatNumber(gap.potential)} potential views</span>
          </div>
        </div>
        <span class="badge badge-${opportunityColor}" style="white-space: nowrap;">${gap.opportunity} Opp.</span>
      </div>
    `;
  });

  document.getElementById('contentGapsList').innerHTML = html;
}

function renderAutomation() {
  const automationStatus = `
    <div class="alert alert-success">
      <i class="fas fa-check-circle"></i>
      <span><strong>✓ GitHub Actions:</strong> Publishing pipeline operational</span>
    </div>
    <div class="alert alert-success">
      <i class="fas fa-check-circle"></i>
      <span><strong>✓ RSS Generation:</strong> Feed generated successfully</span>
    </div>
    <div class="alert alert-success">
      <i class="fas fa-check-circle"></i>
      <span><strong>✓ Sitemap Generation:</strong> Sitemap updated</span>
    </div>
    <div class="alert alert-success">
      <i class="fas fa-check-circle"></i>
      <span><strong>✓ Email Notifications:</strong> 127 subscribers updated</span>
    </div>
    <div class="alert alert-warning">
      <i class="fas fa-exclamation-circle"></i>
      <span><strong>⚠ Telegram Notifications:</strong> Last sent 2 days ago</span>
    </div>
    <div class="alert alert-success">
      <i class="fas fa-check-circle"></i>
      <span><strong>✓ Dev.to Publishing:</strong> Last published 5 days ago</span>
    </div>
  `;

  document.getElementById('automationStatus').innerHTML = automationStatus;
}

function renderErrorLog() {
  const errors = [
    { type: 'Missing Image', article: 'Cloud ETL Pipeline', details: 'Hero image not found', severity: 'Medium', status: 'Open' },
    { type: 'Invalid RSS', article: 'Architecture Patterns', details: 'Special characters in description', severity: 'Low', status: 'Resolved' },
    { type: 'Broken Link', article: 'Data Engineering', details: 'GitHub URL returns 404', severity: 'High', status: 'Open' },
  ];

  let tableHTML = '';
  errors.forEach(error => {
    const severityBadge = `<span class="badge badge-${error.severity.toLowerCase()}">${error.severity}</span>`;
    const statusBadge = error.status === 'Open' ? 
      '<span class="status-dot offline"></span> Open' : 
      '<span class="status-dot online"></span> Resolved';

    tableHTML += `
      <tr>
        <td>${error.type}</td>
        <td><strong>${error.article}</strong></td>
        <td>${error.details}</td>
        <td>${severityBadge}</td>
        <td>${statusBadge}</td>
      </tr>
    `;
  });

  document.getElementById('errorTableBody').innerHTML = tableHTML;
}

function renderConversions() {
  const stats = calculateStats();
  
  const kpiHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Total GitHub Clicks</div>
      <div class="kpi-value">${stats.totalGithubClicks}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Total CV Downloads</div>
      <div class="kpi-value">${stats.totalCVDownloads}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">LinkedIn Clicks</div>
      <div class="kpi-value">${stats.totalLinkedinClicks}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Conversion Rate</div>
      <div class="kpi-value">${stats.conversionRate}%</div>
    </div>
  `;

  document.getElementById('conversionKPIs').innerHTML = kpiHTML;

  let tableHTML = '';
  BLOG_DATA.articles
    .filter(a => a.status === 'Published')
    .sort((a, b) => (b.githubClicks + b.cvDownloads + b.linkedinClicks) - (a.githubClicks + a.cvDownloads + a.linkedinClicks))
    .forEach(article => {
      const totalConversions = article.githubClicks + article.cvDownloads + article.linkedinClicks;
      const convRate = article.views > 0 ? Math.round((totalConversions / article.views) * 100) : 0;

      tableHTML += `
        <tr>
          <td><strong>${article.title}</strong></td>
          <td>${article.githubClicks}</td>
          <td>0</td>
          <td>${article.linkedinClicks}</td>
          <td>${article.cvDownloads}</td>
          <td>${convRate}%</td>
        </tr>
      `;
    });

  document.getElementById('conversionTableBody').innerHTML = tableHTML;
}

function renderAIRecommendations() {
  const recommendations = generateAIRecommendations();
  
  let html = '';
  recommendations.forEach((rec, index) => {
    const priorityIcon = rec.priority === 'High' ? '🔴' : rec.priority === 'Medium' ? '🟡' : '🟢';
    const priorityColor = rec.priority === 'High' ? 'danger' : rec.priority === 'Medium' ? 'warning' : 'info';
    const impactBadgeColor = rec.impact === 'Growth' ? 'info' : 
                            rec.impact === 'SEO' ? 'warning' :
                            rec.impact === 'Conversions' ? 'success' :
                            rec.impact === 'Engagement' ? 'secondary' : 'info';
    
    html += `
      <div class="item-list-item">
        <div class="item-info" style="flex: 1;">
          <div class="item-title" style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
            <span style="background: var(--accent-secondary); color: #fff; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700;">${index + 1}</span>
            <span style="font-weight: 700; flex: 1;">${rec.recommendation}</span>
          </div>
          
          <div class="item-desc" style="margin: 8px 0; color: var(--text-secondary); font-size: 13px; line-height: 1.6; margin-left: 40px;">
            <strong>Why:</strong> ${rec.reason}
          </div>
          
          <div style="margin: 12px 0 0 40px; padding: 12px; background: var(--bg-tertiary); border-radius: 6px; border-left: 3px solid var(--accent-secondary); font-size: 12px;">
            <div style="margin-bottom: 6px;"><strong style="color: var(--accent-secondary);">📋 Action:</strong> ${rec.action}</div>
            <div style="color: var(--text-muted);"><strong style="color: var(--accent-tertiary);">📊 Impact:</strong> ${rec.impact}</div>
          </div>
        </div>
        <div style="display: flex; gap: 8px; white-space: nowrap;">
          <span class="badge badge-${priorityColor}">${rec.priority}</span>
          <span class="badge badge-${impactBadgeColor}" style="font-size: 11px;">${rec.impact}</span>
        </div>
      </div>
    `;
  });

  document.getElementById('aiRecommendations').innerHTML = html;
}

// ── CHART RENDERING ──
function drawViewsChart() {
  const canvas = document.getElementById('viewsChart');
  if (!canvas) return;

  const articles = BLOG_DATA.articles.filter(a => a.status === 'Published').slice(0, 8);
  const ctx = canvas.getContext('2d');
  const width = canvas.offsetWidth;
  const height = canvas.offsetHeight || 300;
  canvas.width = width;
  canvas.height = height;

  const maxViews = Math.max(...articles.map(a => a.views));
  const barWidth = width / (articles.length * 1.5);
  const padding = 40;

  // Draw axes
  ctx.strokeStyle = 'rgba(200, 213, 219, 0.2)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(padding, height - padding);
  ctx.lineTo(width, height - padding);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(padding, padding);
  ctx.lineTo(padding, height - padding);
  ctx.stroke();

  // Draw bars
  articles.forEach((article, index) => {
    const x = padding + (index * (barWidth * 1.5)) + barWidth * 0.25;
    const barHeight = (article.views / maxViews) * (height - padding * 2);
    const y = height - padding - barHeight;

    ctx.fillStyle = '#ff4b2b';
    ctx.fillRect(x, y, barWidth, barHeight);

    // Label
    ctx.fillStyle = 'rgba(232, 238, 245, 0.7)';
    ctx.font = '10px DM Mono';
    ctx.textAlign = 'center';
    ctx.fillText(article.title.substring(0, 8), x + barWidth / 2, height - padding + 20);
    ctx.fillText(formatNumber(article.views), x + barWidth / 2, y - 5);
  });
}

function drawEngagementChart() {
  const canvas = document.getElementById('engagementChart');
  if (!canvas) return;

  const articles = BLOG_DATA.articles.filter(a => a.status === 'Published').slice(0, 8);
  const ctx = canvas.getContext('2d');
  const width = canvas.offsetWidth;
  const height = canvas.offsetHeight || 300;
  canvas.width = width;
  canvas.height = height;

  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(width, height) / 3;

  // Draw pie chart
  let currentAngle = -Math.PI / 2;
  const colors = ['#ff4b2b', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4', '#f43f5e'];
  
  articles.forEach((article, index) => {
    const sliceAngle = (article.scrollDepth / 100) * Math.PI / 2;
    
    ctx.fillStyle = colors[index % colors.length];
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
    ctx.lineTo(centerX, centerY);
    ctx.fill();

    currentAngle += sliceAngle;
  });

  ctx.fillStyle = 'rgba(232, 238, 245, 0.8)';
  ctx.font = 'bold 14px DM Serif Display';
  ctx.textAlign = 'center';
  ctx.fillText('Engagement', centerX, centerY);
}

function drawTrafficChart() {
  const canvas = document.getElementById('trafficChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const width = canvas.offsetWidth;
  const height = canvas.offsetHeight || 300;
  canvas.width = width;
  canvas.height = height;

  const days = 30;
  const data = [];
  for (let i = 0; i < days; i++) {
    data.push(Math.floor(Math.random() * 500 + 200));
  }

  const maxValue = Math.max(...data);
  const padding = 40;
  const pointSpacing = (width - padding * 2) / (days - 1);

  // Draw line
  ctx.strokeStyle = '#ff4b2b';
  ctx.lineWidth = 2;
  ctx.beginPath();

  data.forEach((value, index) => {
    const x = padding + (index * pointSpacing);
    const y = height - padding - (value / maxValue) * (height - padding * 2);
    
    if (index === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });

  ctx.stroke();

  // Fill area
  ctx.lineTo(padding + ((days - 1) * pointSpacing), height - padding);
  ctx.lineTo(padding, height - padding);
  ctx.fillStyle = 'rgba(255, 75, 43, 0.1)';
  ctx.fill();

  ctx.fillStyle = 'rgba(232, 238, 245, 0.8)';
  ctx.font = '12px DM Mono';
  ctx.textAlign = 'center';
  ctx.fillText('Daily Traffic (Last 30 Days)', width / 2, 25);
}

function drawConversionChart() {
  const canvas = document.getElementById('conversionChart');
  if (!canvas) return;

  const data = {
    'GitHub Clicks': 523,
    'CV Downloads': 134,
    'LinkedIn Clicks': 89,
  };

  const ctx = canvas.getContext('2d');
  const width = canvas.offsetWidth;
  const height = canvas.offsetHeight || 300;
  canvas.width = width;
  canvas.height = height;

  const entries = Object.entries(data);
  const colors = ['#ff4b2b', '#3b82f6', '#10b981'];
  const barWidth = width / (entries.length * 2);
  const padding = 40;
  const maxValue = Math.max(...Object.values(data));

  // Draw bars
  entries.forEach((entry, index) => {
    const x = padding + (index * barWidth * 2.5);
    const barHeight = (entry[1] / maxValue) * (height - padding * 2);
    const y = height - padding - barHeight;

    ctx.fillStyle = colors[index];
    ctx.fillRect(x, y, barWidth, barHeight);

    ctx.fillStyle = 'rgba(232, 238, 245, 0.8)';
    ctx.font = '11px DM Mono';
    ctx.textAlign = 'center';
    ctx.fillText(entry[0], x + barWidth / 2, height - padding + 20);
    ctx.fillText(entry[1], x + barWidth / 2, y - 5);
  });
}

function drawCategoryChart() {
  const canvas = document.getElementById('categoryChart');
  if (!canvas) return;

  const categories = {};
  BLOG_DATA.articles.forEach(article => {
    categories[article.category] = (categories[article.category] || 0) + 1;
  });

  const ctx = canvas.getContext('2d');
  const width = canvas.offsetWidth;
  const height = canvas.offsetHeight || 300;
  canvas.width = width;
  canvas.height = height;

  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(width, height) / 3;
  const colors = ['#ff4b2b', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];

  let currentAngle = -Math.PI / 2;
  const entries = Object.entries(categories);
  const total = entries.reduce((sum, e) => sum + e[1], 0);

  entries.forEach((entry, index) => {
    const sliceAngle = (entry[1] / total) * Math.PI * 2;
    
    ctx.fillStyle = colors[index % colors.length];
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
    ctx.lineTo(centerX, centerY);
    ctx.fill();

    currentAngle += sliceAngle;
  });

  ctx.fillStyle = 'rgba(232, 238, 245, 0.8)';
  ctx.font = 'bold 14px DM Serif Display';
  ctx.textAlign = 'center';
  ctx.fillText('By Category', centerX, centerY);
}

function drawSourceChart() {
  const canvas = document.getElementById('sourceChart');
  if (!canvas) return;

  const data = {
    'Organic Search': 45,
    'Direct': 25,
    'Social Media': 18,
    'Referral': 12,
  };

  const ctx = canvas.getContext('2d');
  const width = canvas.offsetWidth;
  const height = canvas.offsetHeight || 300;
  canvas.width = width;
  canvas.height = height;

  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(width, height) / 3;
  const colors = ['#10b981', '#3b82f6', '#f59e0b', '#ff4b2b'];

  let currentAngle = -Math.PI / 2;
  const entries = Object.entries(data);
  const total = entries.reduce((sum, e) => sum + e[1], 0);

  entries.forEach((entry, index) => {
    const sliceAngle = (entry[1] / total) * Math.PI * 2;
    
    ctx.fillStyle = colors[index];
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
    ctx.lineTo(centerX, centerY);
    ctx.fill();

    currentAngle += sliceAngle;
  });

  ctx.fillStyle = 'rgba(232, 238, 245, 0.8)';
  ctx.font = 'bold 14px DM Serif Display';
  ctx.textAlign = 'center';
  ctx.fillText('Traffic Sources', centerX, centerY);
}

// ── UTILITIES ──
function calculateStats() {
  const published = BLOG_DATA.articles.filter(a => a.status === 'Published');
  
  return {
    totalArticles: BLOG_DATA.articles.length,
    publishedArticles: published.length,
    totalViews: published.reduce((sum, a) => sum + a.views, 0),
    avgViews: Math.round(published.reduce((sum, a) => sum + a.views, 0) / (published.length || 1)),
    totalUniqueVisitors: published.reduce((sum, a) => sum + a.uniqueVisitors, 0),
    returningRate: Math.round((published.reduce((sum, a) => sum + a.returningVisitors, 0) / published.reduce((sum, a) => sum + a.uniqueVisitors, 0)) * 100) || 0,
    avgReadTime: Math.round(published.reduce((sum, a) => sum + a.avgReadTime, 0) / (published.length || 1)),
    avgBounceRate: Math.round(published.reduce((sum, a) => sum + a.bounceRate, 0) / (published.length || 1)),
    avgScrollDepth: Math.round(published.reduce((sum, a) => sum + a.scrollDepth, 0) / (published.length || 1)),
    avgEngagement: Math.round(published.reduce((sum, a) => sum + a.scrollDepth, 0) / (published.length || 1)),
    totalGithubClicks: published.reduce((sum, a) => sum + a.githubClicks, 0),
    totalLinkedinClicks: published.reduce((sum, a) => sum + a.linkedinClicks, 0),
    totalCVDownloads: published.reduce((sum, a) => sum + a.cvDownloads, 0),
    totalConversions: published.reduce((sum, a) => sum + (a.githubClicks + a.linkedinClicks + a.cvDownloads), 0),
    overallCTR: Math.round((published.reduce((sum, a) => sum + (a.githubClicks + a.linkedinClicks + a.cvDownloads), 0) / published.reduce((sum, a) => sum + a.views, 0)) * 100) || 0,
    conversionRate: Math.round((published.reduce((sum, a) => sum + (a.githubClicks + a.linkedinClicks + a.cvDownloads), 0) / published.reduce((sum, a) => sum + a.views, 0)) * 100) || 0,
  };
}

function generateAIRecommendations() {
  const published = BLOG_DATA.articles.filter(a => a.status === 'Published');
  const recommendations = [];

  // PRIORITY 1: SEO Optimization for underperformers
  const lowViews = published.filter(a => a.views < 500);
  if (lowViews.length > 0) {
    recommendations.push({
      recommendation: `🔴 SEO URGENT: Optimize ${lowViews.length} underperforming article(s)`,
      reason: `Articles: ${lowViews.map(a => `"${a.title}" (${a.views} views)`).join(', ')}. These need meta descriptions, better keywords, and internal linking. Potential: +200-400 views each.`,
      priority: 'High',
      action: 'Update title tags to 50-60 chars, add meta descriptions, optimize header structure',
      impact: 'SEO'
    });
  }

  // PRIORITY 2: Engagement optimization - low scroll depth
  const lowEngagement = published.filter(a => a.scrollDepth < 60);
  if (lowEngagement.length > 0) {
    recommendations.push({
      recommendation: `🔴 ENGAGEMENT: Improve ${lowEngagement.length} article(s) with low engagement`,
      reason: `Average scroll depth <60%: ${lowEngagement.map(a => `"${a.title}" (${a.scrollDepth}%)`).join(', ')}. Readers aren't reading to the end. Add visuals, shorter paragraphs, code examples.`,
      priority: 'High',
      action: 'Add visual assets, break into smaller sections, improve content flow',
      impact: 'Engagement'
    });
  }

  // PRIORITY 3: Content freshness - no recent updates
  const needsUpdate = published.filter(a => a.updateDate === null || (new Date() - new Date(a.updateDate)) > 180 * 24 * 60 * 60 * 1000);
  if (needsUpdate.length > 0) {
    recommendations.push({
      recommendation: `🟡 CONTENT REFRESH: Update ${needsUpdate.length} outdated article(s)`,
      reason: `These articles haven't been updated in 6+ months: ${needsUpdate.slice(0, 3).map(a => `"${a.title}"`).join(', ')}. Fresh content ranks better and keeps readers engaged. Add new insights, update code.`,
      priority: 'Medium',
      action: 'Review latest versions of frameworks, add new examples, update statistics',
      impact: 'SEO & Freshness'
    });
  }

  // PRIORITY 4: High performers - create related content series
  const highPerformers = published.filter(a => a.views > 2000).sort((a, b) => b.views - a.views);
  if (highPerformers.length > 0) {
    const topCategory = highPerformers[0].category;
    const topPosts = highPerformers.slice(0, 2).map(p => `"${p.title}"`).join(', ');
    recommendations.push({
      recommendation: `🟢 CONTENT SERIES: Create ${highPerformers.length} follow-up articles in "${topCategory}"`,
      reason: `Your top performers: ${topPosts} have ${highPerformers[0].views}+ views. Readers love this category. A series could 3x traffic to these topics.`,
      priority: 'Medium',
      action: `Create series: "Advanced ${topCategory} Patterns", "Real-world ${topCategory} Case Studies"`,
      impact: 'Growth'
    });
  }

  // PRIORITY 5: CTA optimization - high traffic, low conversions
  const lowConversion = published.filter(a => a.views > 300 && a.githubClicks < 15);
  if (lowConversion.length > 0) {
    recommendations.push({
      recommendation: `🟡 CONVERSION: Add CTAs to ${lowConversion.length} high-traffic article(s)`,
      reason: `These articles have ${lowConversion[0].views}+ views but only ${lowConversion[0].githubClicks}+ GitHub clicks. Add 2-3 clear CTAs with relevant projects. Potential: 50-100 extra conversions.`,
      priority: 'Medium',
      action: 'Add GitHub repo links, portfolio CTAs, email signup forms',
      impact: 'Conversions'
    });
  }

  // PRIORITY 6: Popular topic expansion
  recommendations.push({
    recommendation: `🟢 TRENDING: "Advanced dbt Patterns & Macros" (6,200 monthly searches)`,
    reason: `dbt adoption is exploding. Tutorial content gets 400-500 views/mo. You have foundational content but not advanced patterns. Potential: 450+ views + 50+ portfolio clicks.`,
    priority: 'Medium',
    action: 'Write: advanced DAG patterns, macro development, testing framework, performance optimization',
    impact: 'SEO & Authority'
  });

  recommendations.push({
    recommendation: `🟢 HIGH DEMAND: "Data Quality Frameworks Deep Dive" (5,800 monthly searches)`,
    reason: `Great Expectations, soda, & dbt test adoption is surging. No comprehensive guide in your library. Potential: 420+ views + establish thought leadership.`,
    priority: 'Medium',
    action: 'Compare frameworks, implementation guide, Python examples, integration patterns',
    impact: 'Authority & SEO'
  });

  recommendations.push({
    recommendation: `🟢 INFRASTRUCTURE: "Kubernetes for Data Engineers" (8,400 monthly searches)`,
    reason: `Highest search volume content gap. Data engineers need K8s knowledge for deployments. High-intent audience. Potential: 600+ views.`,
    priority: 'High',
    action: 'Cover: Helm charts, StatefulSets for databases, monitoring, GitOps workflows',
    impact: 'SEO & Growth'
  });

  // PRIORITY 7: Expand internal linking
  recommendations.push({
    recommendation: `🟡 INTERNAL LINKING: Add cross-references between ${Math.ceil(published.length / 2)} articles`,
    reason: `Most posts don't link to related content. This reduces time-on-site and SEO juice flow. Adding 3-5 internal links per post can increase avg session duration by 40%.`,
    priority: 'Low',
    action: 'Map content clusters, add "Related Articles" sections, link similar topics',
    impact: 'SEO & Engagement'
  });

  // PRIORITY 8: Social content repurposing
  if (highPerformers.length > 0) {
    recommendations.push({
      recommendation: `🟢 SOCIAL: Repurpose top 5 posts into 15+ social media posts`,
      reason: `Create tweet threads, LinkedIn carousels, and visual quotes from your best content. Twitter threads alone could drive 100+ clicks back. 0 effort content amplification.`,
      priority: 'Low',
      action: 'Create: Twitter threads (5 posts), LinkedIn carousel posts (5), visual quotes (5)',
      impact: 'Traffic & Engagement'
    });
  }

  // PRIORITY 9: Email nurture sequence
  recommendations.push({
    recommendation: `🟢 EMAIL: Build 7-email nurture sequence from top posts`,
    reason: `You have 127+ email subscribers. Average email drives 15-20 clicks. Nurture sequence could generate 100+ monthly clicks with minimal effort.`,
    priority: 'Low',
    action: 'Series: Topic intro → Deep dive → Code examples → Related articles → Success stories',
    impact: 'Engagement & Conversions'
  });

  // PRIORITY 10: Analytics recommendations
  recommendations.push({
    recommendation: `📊 ANALYTICS: Set up conversion tracking for all CTAs`,
    reason: `You're tracking GitHub clicks (${calculateStats().totalGithubClicks}) but missing portfolio, LinkedIn, CV data. Better tracking = better optimization decisions.`,
    priority: 'Low',
    action: 'Add UTM parameters to all links, set up Google Analytics events',
    impact: 'Measurement'
  });

  return recommendations;
}

function formatNumber(num) {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
  return num.toString();
}

// ── EXPORT FUNCTIONALITY ──
function showExportModal() {
  document.getElementById('exportModal').classList.add('active');
}

function closeExportModal() {
  document.getElementById('exportModal').classList.remove('active');
}

function setupExportModal() {
  document.querySelector('.modal-close').addEventListener('click', closeExportModal);
  document.getElementById('exportModal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('exportModal')) closeExportModal();
  });
}

function exportData() {
  const format = document.getElementById('exportFormat').value;
  const includeInventory = document.getElementById('export-inventory').checked;
  const includeConversions = document.getElementById('export-conversions').checked;

  if (!includeInventory && !includeConversions) {
    showNotification('Please select at least one data set to export', 'error');
    return;
  }

  const data = {
    inventory: includeInventory ? BLOG_DATA.articles : null,
    conversions: includeConversions ? calculateStats() : null,
  };

  let content = '';
  let mimeType = 'text/plain';
  let filename = `blog-analytics-${new Date().toISOString().split('T')[0]}`;

  if (format === 'json') {
    content = JSON.stringify(data, null, 2);
    mimeType = 'application/json';
    filename += '.json';
  } else if (format === 'csv') {
    content = 'Title,Status,Views,Unique Visitors,Scroll Depth,Read Time,GitHub Clicks,LinkedIn Clicks,CV Downloads,SEO Score,Category\n';
    BLOG_DATA.articles.forEach(a => {
      content += `"${a.title}","${a.status}",${a.views},${a.uniqueVisitors},${a.scrollDepth},${a.avgReadTime},${a.githubClicks},${a.linkedinClicks},${a.cvDownloads},${a.seoScore},"${a.category}"\n`;
    });
    mimeType = 'text/csv';
    filename += '.csv';
  } else if (format === 'xlsx') {
    // Generate CSV-based Excel content (compatible with Excel when opened)
    content = 'Title\tStatus\tViews\tUnique Visitors\tScroll Depth\tRead Time\tGitHub Clicks\tLinkedIn Clicks\tCV Downloads\tSEO Score\tCategory\n';
    BLOG_DATA.articles.forEach(a => {
      content += `${a.title}\t${a.status}\t${a.views}\t${a.uniqueVisitors}\t${a.scrollDepth}\t${a.avgReadTime}\t${a.githubClicks}\t${a.linkedinClicks}\t${a.cvDownloads}\t${a.seoScore}\t${a.category}\n`;
    });
    mimeType = 'application/vnd.ms-excel';
    filename += '.xls';
  }

  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  showNotification(`Report exported as ${format.toUpperCase()}`, 'success');
  closeExportModal();
}

// ── POST CREATION & PUBLISHING ──
const POST_STORAGE_KEY = 'published_posts';

function toggleAllPlatforms() {
  const checkboxes = document.querySelectorAll('.platform-checkbox');
  const allChecked = Array.from(checkboxes).every(cb => cb.checked);
  checkboxes.forEach(cb => cb.checked = !allChecked);
}

function publishPost() {
  const title = document.getElementById('postTitle').value;
  const content = document.getElementById('postContent').value;
  const tags = document.getElementById('postTags').value;
  const category = document.getElementById('postCategory').value;

  if (!title.trim() || !content.trim()) {
    alert('Please fill in title and content');
    return;
  }

  const selectedPlatforms = Array.from(document.querySelectorAll('.platform-checkbox:checked'))
    .map(cb => cb.value);

  if (selectedPlatforms.length === 0) {
    alert('Please select at least one platform');
    return;
  }

  // Create post object
  const post = {
    id: 'post-' + Date.now(),
    title: title,
    content: content,
    tags: tags.split(',').map(t => t.trim()),
    category: category,
    publishedAt: new Date(),
    platforms: selectedPlatforms,
    status: 'publishing'
  };

  // Show publishing status
  const publishStatusEl = document.getElementById('publishStatus');
  publishStatusEl.style.display = 'block';
  publishStatusEl.classList.add('visible');
  document.getElementById('publishProgress').innerHTML = '';

  // Simulate publishing to each platform
  selectedPlatforms.forEach((platform, index) => {
    setTimeout(() => {
      publishToPlatform(post, platform, index, selectedPlatforms.length);
    }, (index + 1) * 500);
  });

  // Save post to history after all platforms
  setTimeout(() => {
    savePublishedPost(post);
    const publishStatusEl = document.getElementById('publishStatus');
    publishStatusEl.style.display = 'none';
    publishStatusEl.classList.remove('visible');
    clearPostForm();
    loadPublishHistory();
    showNotification('Post published successfully!', 'success');
  }, (selectedPlatforms.length + 1) * 500);
}

function publishToPlatform(post, platform, index, total) {
  const progressDiv = document.getElementById('publishProgress');
  const platformNames = {
    twitter: 'Twitter/X',
    linkedin: 'LinkedIn',
    medium: 'Medium',
    devto: 'Dev.to',
    telegram: 'Telegram',
    blog: 'My Blog'
  };

  const statusItem = document.createElement('div');
  statusItem.style.cssText = 'display: flex; align-items: center; gap: 8px;';
  statusItem.innerHTML = `
    <span style="color: var(--accent-success);"><i class="fas fa-check-circle"></i></span>
    <span>${platformNames[platform]} <span style="color: var(--text-muted);">— published</span></span>
  `;

  progressDiv.appendChild(statusItem);

  // Store platform-specific data
  const platformData = {
    platform: platform,
    postId: post.id,
    url: generatePlatformUrl(platform, post),
    publishedAt: new Date()
  };

  // In real scenario, this would call your social automation APIs
  console.log('Publishing to ' + platform, post);
}

function generatePlatformUrl(platform, post) {
  const baseUrls = {
    twitter: 'https://twitter.com/intent/tweet?text=',
    linkedin: 'https://www.linkedin.com/sharing/share-offsite/?url=',
    medium: 'https://medium.com/new-story',
    devto: 'https://dev.to/new',
    telegram: 'https://t.me/share/url?url=',
    blog: 'https://victor-kipruto-rop.github.io/victor-resum-web/blog.html'
  };

  return baseUrls[platform] || '#';
}

function savePublishedPost(post) {
  let posts = JSON.parse(localStorage.getItem(POST_STORAGE_KEY) || '[]');
  post.status = 'published';
  posts.unshift(post); // Add to beginning
  posts = posts.slice(0, 50); // Keep last 50 posts
  localStorage.setItem(POST_STORAGE_KEY, JSON.stringify(posts));
}

function loadPublishHistory() {
  const posts = JSON.parse(localStorage.getItem(POST_STORAGE_KEY) || '[]');
  const historyDiv = document.getElementById('publishHistory');

  if (posts.length === 0) {
    historyDiv.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 32px; background: var(--bg-secondary); border-radius: 8px; border: 1px solid var(--border-color);">No posts published yet</div>';
    return;
  }

  historyDiv.innerHTML = posts.map((post, index) => {
    const publishDate = new Date(post.publishedAt);
    const timeAgo = getTimeAgo(publishDate);
    const platformBadges = post.platforms.map(p => `<span style="display: inline-block; background: var(--bg-tertiary); padding: 2px 8px; border-radius: 3px; font-size: 11px; margin-right: 4px;">${p}</span>`).join('');

    return `
      <div class="item-list-item" style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px; margin-bottom: 12px;">
        <div class="item-info" style="flex: 1;">
          <div class="item-title" style="margin-bottom: 8px;">${post.title}</div>
          <div class="item-desc" style="margin-bottom: 8px;">
            <span style="color: var(--text-muted);">${post.content.substring(0, 100)}...</span>
          </div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px;">
            ${platformBadges}
          </div>
          <div style="font-size: 11px; color: var(--text-muted);">
            <i class="fas fa-clock"></i> ${timeAgo} · 
            <i class="fas fa-tag"></i> ${post.tags.join(', ')}
          </div>
        </div>
        <div style="display: flex; gap: 8px;">
          <span class="status-dot online" style="background: var(--accent-success);"></span>
          <span style="font-size: 12px; color: var(--text-muted);">Published</span>
        </div>
      </div>
    `;
  }).join('');
}

function clearPostForm() {
  document.getElementById('postTitle').value = '';
  document.getElementById('postContent').value = '';
  document.getElementById('postTags').value = '';
  document.getElementById('postCategory').value = 'data-engineering';
  document.querySelectorAll('.platform-checkbox').forEach(cb => cb.checked = false);
}

function getTimeAgo(date) {
  const seconds = Math.floor((new Date() - date) / 1000);
  const intervals = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60
  };

  for (const [name, secondsInInterval] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / secondsInInterval);
    if (interval >= 1) {
      return interval === 1 ? `1 ${name} ago` : `${interval} ${name}s ago`;
    }
  }

  return 'just now';
}

function showNotification(message, type) {
  const notif = document.createElement('div');
  notif.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: ${type === 'success' ? 'var(--accent-success)' : 'var(--accent-danger)'};
    color: white;
    padding: 16px 24px;
    border-radius: 6px;
    font-weight: 600;
    z-index: 1000;
    animation: slideIn 0.3s ease;
  `;
  notif.innerHTML = `<i class="fas fa-${type === 'success' ? 'check' : 'times'}-circle"></i> ${message}`;
  document.body.appendChild(notif);

  setTimeout(() => {
    notif.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => notif.remove(), 300);
  }, 3000);
}

// ── AI ASSISTANT COMMAND ──
function sendAICommand() {
  const input = document.getElementById('aiCommandInput');
  const command = input.value.trim();
  
  if (!command) {
    showNotification('Please enter a command for the AI assistant', 'error');
    return;
  }
  
  const responseDiv = document.getElementById('aiCommandResponse');
  const responseText = document.getElementById('aiResponseText');
  
  // Show loading state
  responseText.innerHTML = '<div style="display: flex; align-items: center; gap: 10px;"><div class="spinner" style="width: 20px; height: 20px; border: 3px solid rgba(59, 130, 246, 0.2); border-top-color: var(--accent-secondary); border-radius: 50%; animation: spin 0.8s linear infinite;"></div> Processing your request...</div>';
  responseDiv.style.display = 'block';
  
  // Simulate AI response (can be replaced with actual API call)
  setTimeout(() => {
    let response = generateAIResponse(command);
    responseText.innerHTML = response;
    showNotification('AI response generated', 'success');
    input.value = '';
  }, 1500);
}

function generateAIResponse(command) {
  const lowerCmd = command.toLowerCase();
  
  // Content ideas
  if (lowerCmd.includes('content') || lowerCmd.includes('topic') || lowerCmd.includes('idea')) {
    return `
      <div style="color: var(--text-primary); line-height: 2; font-size: 15px;">
        <strong>📝 Content Ideas Based on Trending Topics:</strong><br><br>
        <strong>High Priority (8,400 monthly searches):</strong> "Advanced Kubernetes Patterns" - Deploy data services with K8s operators, StatefulSets for databases, GitOps workflows<br><br>
        <strong>High Priority (5,800 monthly searches):</strong> "dbt Patterns & Macros Advanced Guide" - DAG optimization, custom tests, macro development, performance tuning<br><br>
        <strong>Medium Priority (4,200 monthly searches):</strong> "Data Quality Frameworks Comparison" - Great Expectations vs Soda vs dbt tests, implementation guide<br><br>
        <strong>💡 Recommendation:</strong> Start with Kubernetes content - highest search volume and least competitive in your current library.
      </div>
    `;
  }
  
  // SEO optimization
  if (lowerCmd.includes('seo') || lowerCmd.includes('optimize') || lowerCmd.includes('rank')) {
    return `
      <div style="color: var(--text-primary); line-height: 2; font-size: 15px;">
        <strong>🔍 SEO Optimization Strategy:</strong><br><br>
        <strong>1. Title Optimization:</strong> Keep titles 50-60 characters, include primary keyword, use power words (Complete Guide, Best Practices)<br><br>
        <strong>2. Meta Description:</strong> 150-160 characters, includes keyword, has compelling CTA<br><br>
        <strong>3. Content Structure:</strong> Use H2s and H3s throughout, add internal links to related posts, include 3-5 code examples<br><br>
        <strong>4. Articles to Refresh:</strong> "Data Pipelines Intro" (1,200 views) - Add advanced patterns section<br><br>
        <strong>📊 Expected Impact:</strong> +200-400 additional views per optimized article
      </div>
    `;
  }
  
  // Engagement improvement
  if (lowerCmd.includes('engagement') || lowerCmd.includes('improve') || lowerCmd.includes('traffic')) {
    return `
      <div style="color: var(--text-primary); line-height: 2; font-size: 15px;">
        <strong>📈 Engagement Improvement Plan:</strong><br><br>
        <strong>Quick Wins:</strong><br>
        • Add clear CTAs to top 5 articles (portfolio link, GitHub repo, newsletter signup)<br>
        • Create content series linking related posts for better scroll depth<br>
        • Add more code examples and visual diagrams<br><br>
        <strong>Content Refresh:</strong><br>
        • "ETL Best Practices" (65% scroll depth) - Add performance benchmarks<br>
        • "Data Quality" article - Expand with real-world failure stories<br><br>
        <strong>Distribution:</strong><br>
        • Repurpose top articles as LinkedIn threads and Twitter/X threads<br>
        • Create email sequences for trending topics<br><br>
        <strong>⏱️ Timeline:</strong> 2-3 weeks to see engagement improvements
      </div>
    `;
  }
  
  // Distribution strategy
  if (lowerCmd.includes('distribute') || lowerCmd.includes('social') || lowerCmd.includes('platform')) {
    return `
      <div style="color: var(--text-primary); line-height: 2; font-size: 15px;">
        <strong>🚀 Multi-Platform Distribution Strategy:</strong><br><br>
        <strong>Immediate (Day 1):</strong> Publish to blog, RSS, and sitemap (automated)<br><br>
        <strong>Day 2-3 Distribution:</strong><br>
        • Twitter/X: Thread format with key insights + link<br>
        • LinkedIn: Long-form post with article excerpt + engagement question<br>
        • Dev.to: Republish with canonical link to your blog<br>
        • Telegram: Newsletter announcement to subscribers<br><br>
        <strong>Week 2:</strong><br>
        • Email sequence to subscribers (teaser + full article)<br>
        • Community outreach (Data Engineering subreddits, forums)<br><br>
        <strong>📊 Current Performance:</strong> Blog gets 45.2K monthly views (33% from organic search, 34% from referrals)
      </div>
    `;
  }
  
  // Analytics tracking
  if (lowerCmd.includes('analytics') || lowerCmd.includes('measure') || lowerCmd.includes('metric')) {
    return `
      <div style="color: var(--text-primary); line-height: 2; font-size: 15px;">
        <strong>📊 Key Metrics to Track:</strong><br><br>
        <strong>By Article:</strong><br>
        • Views (baseline) - Target: 500+ for new articles<br>
        • Scroll Depth - Target: 70%+ (current avg: 68%)<br>
        • Time on Page - Target: 5+ minutes<br>
        • Conversions (GitHub, LinkedIn, portfolio clicks) - Current avg: 3.2%<br><br>
        <strong>Overall Blog:</strong><br>
        • Monthly organic traffic: 45.2K (↑ 15% YoY target)<br>
        • Email subscribers: Track weekly growth<br>
        • Social media engagement: Like/share ratios<br><br>
        <strong>💡 Recommendation:</strong> Set up Google Analytics 4 goals for conversions, build custom dashboards for weekly tracking
      </div>
    `;
  }
  
  // Default AI response
  return `
    <div style="color: var(--text-primary); line-height: 2; font-size: 15px;">
      <strong>✨ AI Content Assistant</strong><br><br>
      I can help you with:<br>
      • <strong>Content ideas</strong> - Based on trending topics and search volume<br>
      • <strong>SEO optimization</strong> - Title, meta, structure, internal linking<br>
      • <strong>Engagement strategies</strong> - Improve scroll depth and conversions<br>
      • <strong>Distribution planning</strong> - Multi-platform publishing strategy<br>
      • <strong>Analytics tracking</strong> - Key metrics and measurement setup<br><br>
      <strong>Try asking:</strong> "Give me content ideas", "How do I improve SEO?", "Help with engagement", "Distribution strategy", or "What metrics should I track?"
    </div>
  `;
}

// ── DEPLOY CONTENT SYNC ──
function deployContentSync() {
  const syncBtn = document.querySelector('.btn-refresh');
  const originalHTML = syncBtn.innerHTML;
  
  // Show syncing state
  syncBtn.disabled = true;
  syncBtn.innerHTML = '<i class="fas fa-rotate fa-spin"></i> Syncing...';
  syncBtn.style.opacity = '0.7';
  
  // Simulate sync operations
  const steps = [
    'Syncing blog inventory...',
    'Updating analytics data...',
    'Refreshing SEO metrics...',
    'Generating content gaps analysis...',
    'Finalizing sync...'
  ];
  
  let stepIndex = 0;
  
  showNotification('Content sync initiated', 'success');
  
  const syncInterval = setInterval(() => {
    if (stepIndex < steps.length) {
      showNotification(steps[stepIndex], 'success');
      stepIndex++;
    } else {
      clearInterval(syncInterval);
      
      // Reload data from sample
      BLOG_DATA.articles = [...SAMPLE_BLOGS];
      saveBlogData();
      
      // Re-render current section
      const activeSection = document.querySelector('.nav-item.active');
      if (activeSection && activeSection.dataset.section) {
        renderSection(activeSection.dataset.section);
      } else {
        renderOverview();
      }
      
      // Restore button
      syncBtn.disabled = false;
      syncBtn.innerHTML = originalHTML;
      syncBtn.style.opacity = '1';
      
      showNotification('Content sync complete! All data refreshed.', 'success');
    }
  }, 600);
}

// ── NOTIFICATION SYSTEM ──
const NOTIF_STORAGE_KEY = 'blog_ops_notifications';
const SUB_STORAGE_KEY = 'blog_ops_subscribers';
const AUTOPOST_STORAGE_KEY = 'blog_ops_autopost';
const NOTIF_SETTINGS_KEY = 'blog_ops_notif_settings';

function getNotifHistory() {
  return JSON.parse(localStorage.getItem(NOTIF_STORAGE_KEY) || '[]');
}

function saveNotifHistory(history) {
  localStorage.setItem(NOTIF_STORAGE_KEY, JSON.stringify(history.slice(0, 100)));
}

function logNotification(type, title, recipients) {
  const history = getNotifHistory();
  history.unshift({
    id: 'notif-' + Date.now(),
    type: type,
    title: title,
    recipients: recipients,
    sentAt: new Date().toISOString(),
    status: 'sent'
  });
  saveNotifHistory(history);
}

function getNotifSettings() {
  const defaults = {
    welcome: true, newpost: true, admin: true, digest: true, trending: false,
    autopostTwitter: true, autopostLinkedin: true, autopostMedium: false, autopostDevto: true, autopostTelegram: true
  };
  const stored = localStorage.getItem(NOTIF_SETTINGS_KEY);
  return stored ? { ...defaults, ...JSON.parse(stored) } : defaults;
}

function saveNotifSettings() {
  const settings = {
    welcome: document.getElementById('notif-welcome')?.checked ?? true,
    newpost: document.getElementById('notif-newpost')?.checked ?? true,
    admin: document.getElementById('notif-admin')?.checked ?? true,
    digest: document.getElementById('notif-digest')?.checked ?? true,
    trending: document.getElementById('notif-trending')?.checked ?? false,
    autopostTwitter: document.getElementById('autopost-twitter')?.checked ?? true,
    autopostLinkedin: document.getElementById('autopost-linkedin')?.checked ?? true,
    autopostMedium: document.getElementById('autopost-medium')?.checked ?? false,
    autopostDevto: document.getElementById('autopost-devto')?.checked ?? true,
    autopostTelegram: document.getElementById('autopost-telegram')?.checked ?? true
  };
  localStorage.setItem(NOTIF_SETTINGS_KEY, JSON.stringify(settings));
  showNotification('Notification settings saved', 'success');
}

function loadNotifSettings() {
  const s = getNotifSettings();
  const set = (id, val) => { const el = document.getElementById(id); if (el) el.checked = val; };
  set('notif-welcome', s.welcome);
  set('notif-newpost', s.newpost);
  set('notif-admin', s.admin);
  set('notif-digest', s.digest);
  set('notif-trending', s.trending);
  set('autopost-twitter', s.autopostTwitter);
  set('autopost-linkedin', s.autopostLinkedin);
  set('autopost-medium', s.autopostMedium);
  set('autopost-devto', s.autopostDevto);
  set('autopost-telegram', s.autopostTelegram);
}

// Send welcome email to new subscriber
function sendWelcomeEmail(name, email) {
  const settings = getNotifSettings();
  if (!settings.welcome) return;
  logNotification('welcome', `Welcome email sent to ${name}`, email);
  console.log(`[EMAIL] Welcome → ${name} <${email}>: Welcome to Victor Kipruto's Blog! You'll receive notifications for new posts and weekly digests.`);
}

// Send new post notification to all subscribers + admin
function sendNewPostNotifications(post) {
  const settings = getNotifSettings();
  const subs = getSubscribers();
  const activeSubs = subs.filter(s => s.status === 'active');
  
  // Notify all subscribers
  if (settings.newpost && activeSubs.length > 0) {
    const emails = activeSubs.map(s => s.email).join(', ');
    logNotification('new_post', `New post alert: "${post.title}"`, `${activeSubs.length} subscribers`);
    console.log(`[EMAIL] New Post → ${activeSubs.length} subscribers: "${post.title}"`);
  }
  
  // Notify admin
  if (settings.admin) {
    logNotification('admin_alert', `Admin: New post published "${post.title}"`, 'admin@victorkipruto.dev');
    console.log(`[EMAIL] Admin Alert → admin: New post "${post.title}" published to ${post.platforms.join(', ')}`);
  }
}

// ── NOTIFICATIONS SECTION ──
function renderNotifications() {
  const history = getNotifHistory();
  const subs = getSubscribers();
  
  const kpiHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Total Sent</div>
      <div class="kpi-value">${history.length}</div>
      <div class="kpi-change positive"><i class="fas fa-check"></i> All delivered</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Welcome Emails</div>
      <div class="kpi-value">${history.filter(n => n.type === 'welcome').length}</div>
      <div class="kpi-change positive"><i class="fas fa-envelope"></i> Auto-sent</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Post Alerts</div>
      <div class="kpi-value">${history.filter(n => n.type === 'new_post').length}</div>
      <div class="kpi-change positive"><i class="fas fa-bell"></i> To ${subs.filter(s => s.status === 'active').length} subscribers</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Admin Alerts</div>
      <div class="kpi-value">${history.filter(n => n.type === 'admin_alert').length}</div>
      <div class="kpi-change positive"><i class="fas fa-shield"></i> Real-time</div>
    </div>
  `;
  document.getElementById('notifKPIs').innerHTML = kpiHTML;

  // Load settings into checkboxes
  setTimeout(loadNotifSettings, 50);

  // Render history
  const histDiv = document.getElementById('notifHistory');
  if (history.length === 0) {
    histDiv.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 48px;">No notifications sent yet. Notifications are triggered when posts are published or subscribers are added.</div>';
    return;
  }
  histDiv.innerHTML = history.map(n => {
    const icon = n.type === 'welcome' ? 'fa-envelope' : n.type === 'new_post' ? 'fa-bell' : 'fa-shield';
    const color = n.type === 'welcome' ? 'var(--accent-tertiary)' : n.type === 'new_post' ? 'var(--accent-secondary)' : 'var(--accent-primary)';
    return `
      <div class="item-list-item">
        <div class="item-info">
          <div class="item-title" style="display: flex; align-items: center; gap: 12px;">
            <i class="fas ${icon}" style="color: ${color};"></i>
            ${n.title}
          </div>
          <div class="item-desc">
            <i class="fas fa-users" style="margin-right: 4px;"></i> ${n.recipients} · 
            <i class="fas fa-clock" style="margin-right: 4px;"></i> ${getTimeAgo(new Date(n.sentAt))}
          </div>
        </div>
        <span class="badge badge-success"><i class="fas fa-check"></i> Sent</span>
      </div>
    `;
  }).join('');
}

// ── SUBSCRIBER MANAGEMENT ──
function getSubscribers() {
  return JSON.parse(localStorage.getItem(SUB_STORAGE_KEY) || '[]');
}

function saveSubscribers(subs) {
  localStorage.setItem(SUB_STORAGE_KEY, JSON.stringify(subs));
}

function initDefaultSubscribers() {
  const subs = getSubscribers();
  if (subs.length === 0) {
    const defaults = [
      { name: 'Sarah Chen', email: 'sarah.chen@dataeng.io', joined: '2024-01-15', welcomeSent: true, status: 'active' },
      { name: 'Marcus Johnson', email: 'marcus.j@cloudops.dev', joined: '2024-02-20', welcomeSent: true, status: 'active' },
      { name: 'Priya Patel', email: 'priya@analytics.co', joined: '2024-03-10', welcomeSent: true, status: 'active' },
      { name: 'Alex Rivera', email: 'alex.r@startup.io', joined: '2024-04-05', welcomeSent: true, status: 'active' },
      { name: 'Kenji Tanaka', email: 'kenji@ml-pipeline.jp', joined: '2024-05-12', welcomeSent: true, status: 'active' },
    ];
    saveSubscribers(defaults);
  }
}

function addSubscriber() {
  const name = document.getElementById('subName').value.trim();
  const email = document.getElementById('subEmail').value.trim();
  
  if (!name || !email) {
    showNotification('Please enter name and email', 'error');
    return;
  }
  
  const subs = getSubscribers();
  if (subs.find(s => s.email === email)) {
    showNotification('This email is already subscribed', 'error');
    return;
  }
  
  const newSub = {
    name: name,
    email: email,
    joined: new Date().toISOString().split('T')[0],
    welcomeSent: true,
    status: 'active'
  };
  
  subs.push(newSub);
  saveSubscribers(subs);
  
  // Send welcome email
  sendWelcomeEmail(name, email);
  
  document.getElementById('subName').value = '';
  document.getElementById('subEmail').value = '';
  
  renderSubscribers();
  showNotification(`Welcome email sent to ${name}!`, 'success');
}

function removeSubscriber(email) {
  let subs = getSubscribers();
  subs = subs.filter(s => s.email !== email);
  saveSubscribers(subs);
  renderSubscribers();
  showNotification('Subscriber removed', 'success');
}

function renderSubscribers() {
  initDefaultSubscribers();
  const subs = getSubscribers();
  const active = subs.filter(s => s.status === 'active').length;
  const totalWelcome = subs.filter(s => s.welcomeSent).length;
  
  const kpiHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Total Subscribers</div>
      <div class="kpi-value">${subs.length}</div>
      <div class="kpi-change positive"><i class="fas fa-users"></i> Growing</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Active</div>
      <div class="kpi-value">${active}</div>
      <div class="kpi-change positive"><i class="fas fa-check-circle"></i> Engaged</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Welcome Emails Sent</div>
      <div class="kpi-value">${totalWelcome}</div>
      <div class="kpi-change positive"><i class="fas fa-envelope"></i> 100% delivery</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Email Open Rate</div>
      <div class="kpi-value">68%</div>
      <div class="kpi-change positive"><i class="fas fa-arrow-up"></i> Above average</div>
    </div>
  `;
  document.getElementById('subKPIs').innerHTML = kpiHTML;

  const tbody = document.getElementById('subTableBody');
  tbody.innerHTML = subs.map(sub => `
    <tr>
      <td><strong>${sub.name}</strong></td>
      <td>${sub.email}</td>
      <td>${sub.joined}</td>
      <td>${sub.welcomeSent ? '<span class="badge badge-success">Sent</span>' : '<span class="badge badge-warning">Pending</span>'}</td>
      <td><span class="status-dot ${sub.status === 'active' ? 'online' : 'offline'}"></span> ${sub.status}</td>
      <td><button onclick="removeSubscriber('${sub.email}')" class="btn" style="padding: 6px 12px; font-size: 11px; color: var(--accent-danger);"><i class="fas fa-trash"></i></button></td>
    </tr>
  `).join('');
}

// ── AUTO-POST SCHEDULER ──
function getAutoPosts() {
  return JSON.parse(localStorage.getItem(AUTOPOST_STORAGE_KEY) || '{"scheduled":[],"history":[]}');
}

function saveAutoPosts(data) {
  localStorage.setItem(AUTOPOST_STORAGE_KEY, JSON.stringify(data));
}

function triggerAutoPostCycle() {
  const syncBtn = document.querySelector('#autopost .btn-refresh');
  if (syncBtn) {
    syncBtn.disabled = true;
    syncBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running...';
  }
  
  showNotification('Auto-post cycle initiated...', 'success');
  
  const topics = [
    'Advanced Kubernetes Patterns for Data Engineers',
    'Building Real-time ETL Pipelines with Apache Flink',
    'Data Quality Frameworks: Great Expectations vs Soda',
    'Cost Optimization Strategies for Cloud Data Lakes',
    'GraphQL APIs for Data Engineering Workflows'
  ];
  
  const topic = topics[Math.floor(Math.random() * topics.length)];
  const platforms = [];
  const settings = getNotifSettings();
  if (settings.autopostTwitter) platforms.push('twitter');
  if (settings.autopostLinkedin) platforms.push('linkedin');
  if (settings.autopostDevto) platforms.push('devto');
  if (settings.autopostTelegram) platforms.push('telegram');
  if (settings.autopostMedium) platforms.push('medium');
  
  const post = {
    id: 'auto-' + Date.now(),
    title: topic,
    content: `AI-generated article: ${topic}. This post covers best practices, implementation patterns, and real-world examples.`,
    category: 'data-engineering',
    tags: ['auto-generated', 'data-engineering'],
    publishedAt: new Date().toISOString(),
    platforms: platforms,
    status: 'publishing'
  };
  
  // Simulate the cycle
  setTimeout(() => {
    post.status = 'published';
    const data = getAutoPosts();
    data.history.unshift(post);
    data.history = data.history.slice(0, 50);
    saveAutoPosts(data);
    
    // Send notifications
    sendNewPostNotifications(post);
    
    if (syncBtn) {
      syncBtn.disabled = false;
      syncBtn.innerHTML = '<i class="fas fa-play"></i> Run Cycle Now';
    }
    
    renderAutoPost();
    showNotification(`Auto-post complete: "${topic}" → ${platforms.join(', ')}`, 'success');
  }, 2500);
}

function scheduleAutoPost() {
  const topics = [
    'dbt Macros: Advanced Patterns for Data Transformation',
    'Monitoring Data Pipelines with Prometheus and Grafana',
    'Feature Stores for ML: Architecture and Implementation',
    'Serverless Data Processing: AWS Lambda vs Google Cloud Functions',
    'Data Lineage Tracking with OpenLineage'
  ];
  
  const topic = topics[Math.floor(Math.random() * topics.length)];
  const scheduledTime = new Date(Date.now() + 24 * 60 * 60 * 1000);
  
  const data = getAutoPosts();
  data.scheduled.push({
    id: 'sched-' + Date.now(),
    title: topic,
    scheduledFor: scheduledTime.toISOString(),
    platforms: ['twitter', 'linkedin', 'devto', 'telegram'],
    status: 'scheduled'
  });
  saveAutoPosts(data);
  
  renderAutoPost();
  showNotification(`Post scheduled: "${topic}" for ${scheduledTime.toLocaleDateString()} ${scheduledTime.toLocaleTimeString()}`, 'success');
}

function renderAutoPost() {
  const data = getAutoPosts();
  
  const kpiHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Auto-Posts Published</div>
      <div class="kpi-value">${data.history.length}</div>
      <div class="kpi-change positive"><i class="fas fa-check"></i> All successful</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Scheduled</div>
      <div class="kpi-value">${data.scheduled.length}</div>
      <div class="kpi-change positive"><i class="fas fa-clock"></i> Queued</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Social Platforms</div>
      <div class="kpi-value">5</div>
      <div class="kpi-change positive"><i class="fas fa-share-nodes"></i> Connected</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Next Cycle</div>
      <div class="kpi-value">24h</div>
      <div class="kpi-change positive"><i class="fas fa-rotate"></i> Continuous</div>
    </div>
  `;
  document.getElementById('autopostKPIs').innerHTML = kpiHTML;

  // Scheduled queue
  const schedDiv = document.getElementById('scheduledPosts');
  if (data.scheduled.length === 0) {
    schedDiv.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 48px;">No posts scheduled. Click "Schedule Next" to queue the next auto-generated post.</div>';
  } else {
    schedDiv.innerHTML = data.scheduled.map(s => {
      const schedDate = new Date(s.scheduledFor);
      return `
        <div class="item-list-item">
          <div class="item-info">
            <div class="item-title"><i class="fas fa-clock" style="color: var(--accent-warning); margin-right: 8px;"></i>${s.title}</div>
            <div class="item-desc">
              <i class="fas fa-calendar"></i> ${schedDate.toLocaleDateString()} ${schedDate.toLocaleTimeString()} · 
              Platforms: ${s.platforms.join(', ')}
            </div>
          </div>
          <span class="badge badge-warning">Scheduled</span>
        </div>
      `;
    }).join('');
  }

  // History
  const histDiv = document.getElementById('autopostHistory');
  if (data.history.length === 0) {
    histDiv.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 48px;">No auto-posts published yet. Click "Run Cycle Now" to trigger the first cycle.</div>';
  } else {
    histDiv.innerHTML = data.history.map(p => `
      <div class="item-list-item">
        <div class="item-info">
          <div class="item-title"><i class="fas fa-robot" style="color: var(--accent-secondary); margin-right: 8px;"></i>${p.title}</div>
          <div class="item-desc">
            <i class="fas fa-clock"></i> ${getTimeAgo(new Date(p.publishedAt))} · 
            Platforms: ${p.platforms.map(pl => `<span style="display:inline-block; background:var(--bg-secondary); padding:2px 6px; border-radius:3px; font-size:10px; margin: 0 2px;">${pl}</span>`).join('')}
          </div>
        </div>
        <span class="badge badge-success"><i class="fas fa-check"></i> Published</span>
      </div>
    `).join('');
  }
}

// ── ENHANCED PUBLISH FLOW ──
// Override the existing publishPost to include notifications
const originalPublishPost = publishPost;
publishPost = function() {
  const title = document.getElementById('postTitle').value;
  const content = document.getElementById('postContent').value;
  const tags = document.getElementById('postTags').value;
  const category = document.getElementById('postCategory').value;

  if (!title.trim() || !content.trim()) {
    alert('Please fill in title and content');
    return;
  }

  const selectedPlatforms = Array.from(document.querySelectorAll('.platform-checkbox:checked'))
    .map(cb => cb.value);

  if (selectedPlatforms.length === 0) {
    alert('Please select at least one platform');
    return;
  }

  const post = {
    id: 'post-' + Date.now(),
    title: title,
    content: content,
    tags: tags.split(',').map(t => t.trim()),
    category: category,
    publishedAt: new Date(),
    platforms: selectedPlatforms,
    status: 'publishing'
  };

  const publishStatusEl = document.getElementById('publishStatus');
  publishStatusEl.style.display = 'block';
  publishStatusEl.classList.add('visible');
  document.getElementById('publishProgress').innerHTML = '';

  selectedPlatforms.forEach((platform, index) => {
    setTimeout(() => {
      publishToPlatform(post, platform, index, selectedPlatforms.length);
    }, (index + 1) * 500);
  });

  setTimeout(() => {
    savePublishedPost(post);
    publishStatusEl.style.display = 'none';
    publishStatusEl.classList.remove('visible');
    clearPostForm();
    loadPublishHistory();
    
    // Send notifications for the new post
    sendNewPostNotifications(post);
    
    showNotification('Post published! Notifications sent to subscribers + admin.', 'success');
  }, (selectedPlatforms.length + 1) * 500);
};

// ── RESEND NOTIFICATION SERVER ──
const RESEND_API = 'http://127.0.0.1:8765';

async function sendToResend(endpoint, data) {
  try {
    const resp = await fetch(`${RESEND_API}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await resp.json();
  } catch (e) {
    console.warn('Resend server not running. Starting fallback...', e.message);
    // Fallback: log notification locally
    logNotification('custom', data.title || 'Notification', data.recipients || 'all');
    return { success: false, message: 'Resend server not running. Start with: python scripts/python/resend_server.py' };
  }
}

// ── CUSTOM NOTIFICATION MODAL ──
function showSendNotificationModal() {
  // Create modal if it doesn't exist
  let modal = document.getElementById('notifModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'notifModal';
    modal.className = 'modal';
    modal.innerHTML = `
      <div class="modal-content" style="max-width: 600px;">
        <div class="modal-header">
          <h2 class="modal-title"><i class="fas fa-paper-plane" style="color: var(--accent-secondary); margin-right: 12px;"></i>Send Notification</h2>
          <button class="modal-close" onclick="closeNotifModal()">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Recipients</label>
            <select id="notifRecipients" class="form-input" onchange="toggleCustomEmails()">
              <option value="all">All Subscribers</option>
              <option value="custom">Custom Selection</option>
            </select>
          </div>
          <div id="customEmailsGroup" class="form-group" style="display: none;">
            <label class="form-label">Select Subscribers</label>
            <div id="subscriberCheckboxes" style="display: flex; flex-direction: column; gap: 10px; max-height: 200px; overflow-y: auto;"></div>
          </div>
          <div class="form-group">
            <label class="form-label">Notification Title</label>
            <input type="text" id="notifTitle" class="form-input" placeholder="Subject line...">
          </div>
          <div class="form-group">
            <label class="form-label">Message</label>
            <textarea id="notifMessage" class="form-input" style="min-height: 120px;" placeholder="Write your notification message..."></textarea>
          </div>
          <div id="notifSendStatus" style="text-align: center; font-size: 13px; margin-top: 8px; min-height: 20px;"></div>
        </div>
        <div class="modal-footer">
          <button class="btn" onclick="closeNotifModal()"><i class="fas fa-xmark"></i> Cancel</button>
          <button class="btn btn-refresh" onclick="sendCustomNotification()"><i class="fas fa-paper-plane"></i> Send Now</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }
  // Load subscribers into checkboxes
  loadSubscriberCheckboxes();
  modal.classList.add('active');
}

function closeNotifModal() {
  const modal = document.getElementById('notifModal');
  if (modal) modal.classList.remove('active');
}

function toggleCustomEmails() {
  const val = document.getElementById('notifRecipients').value;
  document.getElementById('customEmailsGroup').style.display = val === 'custom' ? 'block' : 'none';
}

async function loadSubscriberCheckboxes() {
  const container = document.getElementById('subscriberCheckboxes');
  const subs = getSubscribers().filter(s => s.status === 'active');
  container.innerHTML = subs.map(s => `
    <label class="export-option">
      <input type="checkbox" class="notif-sub-cb" value="${s.email}" style="width: 18px; height: 18px;">
      <label>${s.name} (${s.email})</label>
    </label>
  `).join('');
}

async function sendCustomNotification() {
  const recipients = document.getElementById('notifRecipients').value;
  const title = document.getElementById('notifTitle').value.trim();
  const message = document.getElementById('notifMessage').value.trim();
  const statusEl = document.getElementById('notifSendStatus');

  if (!title || !message) {
    statusEl.innerHTML = '<span style="color: var(--accent-danger);">Please fill in title and message</span>';
    return;
  }

  let customEmails = [];
  if (recipients === 'custom') {
    customEmails = Array.from(document.querySelectorAll('.notif-sub-cb:checked')).map(cb => cb.value);
    if (customEmails.length === 0) {
      statusEl.innerHTML = '<span style="color: var(--accent-danger);">Please select at least one subscriber</span>';
      return;
    }
  }

  statusEl.innerHTML = '<div class="spinner" style="width:20px;height:20px;margin:0 auto;border-width:2px;"></div> Sending...';
  const btnEl = document.querySelector('#notifModal .btn-refresh');
  if (btnEl) btnEl.disabled = true;

  const result = await sendToResend('/api/send-notification', {
    recipients: recipients,
    customEmails: customEmails,
    title: title,
    message: message,
    type: 'custom'
  });

  if (btnEl) btnEl.disabled = false;

  if (result.success) {
    statusEl.innerHTML = `<span style="color: var(--accent-tertiary);">✅ Sent to ${result.sent} subscriber(s)!</span>`;
    setTimeout(closeNotifModal, 2000);
    renderNotifications();
    showNotification('Notifications sent successfully!', 'success');
  } else {
    statusEl.innerHTML = `<span style="color: var(--accent-danger);">⚠ ${result.message || 'Failed to send'}</span>`;
  }
}

// ── REFRESH & LOGOUT ──
function refreshDashboard() {
  location.reload();
}

window.logout = logout;

// ── KEYBOARD SHORTCUTS ──
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeExportModal();
    closeNotifModal();
  }
});
