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
    { topic: 'Advanced Kubernetes Patterns', opportunity: 'High', reason: 'No K8s content yet' },
    { topic: 'dbt Best Practices', opportunity: 'High', reason: 'Popular in data community' },
    { topic: 'Data Quality Frameworks', opportunity: 'Very High', reason: 'Growing trend' },
    { topic: 'Cost Optimization for Data Pipelines', opportunity: 'Medium', reason: 'Common question' },
    { topic: 'Monitoring & Observability', opportunity: 'High', reason: 'Critical topic' },
  ];

  let html = '';
  gaps.forEach(gap => {
    const opportunityColor = gap.opportunity === 'Very High' ? 'danger' : 
                            gap.opportunity === 'High' ? 'warning' : 'info';
    
    html += `
      <div class="item-list-item">
        <div class="item-info">
          <div class="item-title"><i class="fas fa-lightbulb" style="color: #fbbf24; margin-right: 8px;"></i>${gap.topic}</div>
          <div class="item-desc">${gap.reason}</div>
        </div>
        <span class="badge badge-${opportunityColor}">${gap.opportunity} Opportunity</span>
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
  recommendations.forEach(rec => {
    const priorityColor = rec.priority === 'High' ? 'danger' : rec.priority === 'Medium' ? 'warning' : 'info';
    
    html += `
      <div class="item-list-item">
        <div class="item-info">
          <div class="item-title"><i class="fas fa-brain" style="color: #3b82f6; margin-right: 8px;"></i>${rec.recommendation}</div>
          <div class="item-desc">${rec.reason}</div>
        </div>
        <span class="badge badge-${priorityColor}">${rec.priority} Priority</span>
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

  // Low views
  const lowViews = published.filter(a => a.views < 500);
  if (lowViews.length > 0) {
    recommendations.push({
      recommendation: `Update ${lowViews.length} article(s) with low views`,
      reason: `Articles with less than 500 views need better SEO and title optimization`,
      priority: 'High'
    });
  }

  // No recent updates
  const needsUpdate = published.filter(a => a.updateDate === null);
  if (needsUpdate.length > 0) {
    recommendations.push({
      recommendation: `Refresh ${needsUpdate.length} article(s) lacking recent updates`,
      reason: `Evergreen content benefits from periodic refreshes to maintain relevance`,
      priority: 'Medium'
    });
  }

  // High performers
  const highPerformers = published.filter(a => a.views > 2000);
  if (highPerformers.length > 0) {
    recommendations.push({
      recommendation: `Create follow-up articles on ${highPerformers[0].category}`,
      reason: `Your "${highPerformers[0].title}" is a top performer. Related content would perform well`,
      priority: 'Medium'
    });
  }

  // Content gaps
  recommendations.push({
    recommendation: 'Write article on "Kubernetes for Data Engineers"',
    reason: 'High search volume + missing from your content library',
    priority: 'High'
  });

  recommendations.push({
    recommendation: 'Create tutorial on "dbt Best Practices"',
    reason: 'Trending topic in data community with high engagement potential',
    priority: 'Medium'
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
  const data = {
    inventory: document.getElementById('export-inventory').checked ? BLOG_DATA.articles : null,
    conversions: document.getElementById('export-conversions').checked ? calculateStats() : null,
  };

  let content = '';
  let filename = `blog-analytics-${new Date().toISOString().split('T')[0]}`;

  if (format === 'json') {
    content = JSON.stringify(data, null, 2);
    filename += '.json';
  } else if (format === 'csv') {
    content = 'Title,Views,Conversions,Read Time\n';
    BLOG_DATA.articles.forEach(a => {
      content += `"${a.title}",${a.views},${a.githubClicks + a.linkedinClicks + a.cvDownloads},${a.avgReadTime}\n`;
    });
    filename += '.csv';
  }

  const blob = new Blob([content], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  closeExportModal();
}

// ── REFRESH & LOGOUT ──
function refreshDashboard() {
  location.reload();
}

window.logout = logout;
