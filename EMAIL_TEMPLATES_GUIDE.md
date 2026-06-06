# Email Templates Guide

Complete collection of 13 email templates for blog notifications, activity tracking, and subscriber engagement.

## 📋 Available Templates

### 1. **Welcome Email** (`welcome`)
**Purpose:** Greet new subscribers and set expectations
**Parameters:**
- `name` (str): Subscriber's name
- `email` (str): Email address

**Usage:**
```python
from scripts.python.email_templates import template_welcome
html = template_welcome("John Doe", "john@example.com")
```

**Content:**
- Warm welcome message
- What to expect from the blog
- Quick start links
- Social media links

---

### 2. **New Blog Post Notification** (`new_blog_post`)
**Purpose:** Announce newly published blog articles
**Parameters:**
- `name` (str): Subscriber name
- `post_title` (str): Article title
- `post_excerpt` (str): Article summary/preview
- `post_slug` (str): URL slug for the post
- `read_time` (int): Estimated reading time in minutes
- `image_url` (str, optional): Featured image URL

**Usage:**
```python
html = template_new_blog_post(
    name="Alice",
    post_title="Building Scalable Data Pipelines",
    post_excerpt="Learn how to design ETL systems...",
    post_slug="data-pipelines",
    read_time=8,
    image_url="https://example.com/image.png"
)
```

**Content:**
- Post title with featured image (optional)
- Article excerpt
- Read time estimate
- Call-to-action button
- Social sharing options

---

### 3. **Weekly Digest** (`weekly_digest`)
**Purpose:** Send curated collection of weekly posts
**Parameters:**
- `name` (str): Subscriber name
- `posts` (list): List of post dictionaries with keys:
  - `title` or `name`
  - `excerpt` or `description`
  - `readTime` or `read_time`
  - `date` or `publishDate`
  - `tags` (optional list)
  - `id` or `slug`

**Usage:**
```python
posts = [
    {
        "title": "ETL Best Practices",
        "excerpt": "Top 10 patterns...",
        "read_time": 5,
        "publishDate": "Jun 5, 2026",
        "tags": ["ETL", "Data"],
        "id": "etl-practices"
    }
]
html = template_weekly_digest("Bob", posts)
```

**Content:**
- Weekly recap introduction
- Multiple post cards with excerpts
- Read time & publication date
- Tag display
- Individual read buttons
- Link to full blog

---

### 4. **Generic Notification** (`notification`)
**Purpose:** Send customizable alert notifications
**Parameters:**
- `name` (str): Recipient name
- `title` (str): Notification title
- `message` (str): Notification body
- `icon` (str, optional): Emoji icon (default: "🔔")
- `action_text` (str, optional): Button text
- `action_url` (str, optional): Button link

**Usage:**
```python
html = template_notification(
    name="Charlie",
    title="New Feature Available",
    message="Check out our new dashboard feature...",
    icon="✨",
    action_text="Explore",
    action_url="https://example.com/new-feature"
)
```

**Content:**
- Customizable title and icon
- Message body
- Optional action button
- Help/support section

---

### 5. **Dashboard Alert** (`dashboard_alert`)
**Purpose:** Report analytics and metrics
**Parameters:**
- `name` (str): Recipient name
- `alert_title` (str): Alert subject
- `metrics` (dict): Key-value pairs of metric names and values
- `recommendation` (str): Actionable insight

**Usage:**
```python
metrics = {
    "Page Views": "2,456",
    "Unique Visitors": "1,120",
    "Bounce Rate": "32%"
}
html = template_dashboard_alert(
    name="David",
    alert_title="Daily Analytics Report",
    metrics=metrics,
    recommendation="Focus on improving mobile experience"
)
```

**Content:**
- Alert title
- Grid of metric boxes
- Actionable recommendations
- Dashboard access link

---

### 6. **Event Announcement** (`event_announcement`)
**Purpose:** Announce new projects, courses, or events
**Parameters:**
- `name` (str): Recipient name
- `event_title` (str): Event/project name
- `event_date` (str): Event date or launch date
- `event_description` (str): Event details
- `event_url` (str, optional): Event link

**Usage:**
```python
html = template_event_announcement(
    name="Eva",
    event_title="Advanced Python Course",
    event_date="July 15, 2026",
    event_description="Master async programming...",
    event_url="https://example.com/course"
)
```

**Content:**
- Eye-catching announcement header
- Event date highlight
- Detailed description
- Call-to-action button

---

### 7. **Trending Content Alert** (`trending_content`)
**Purpose:** Highlight viral/trending articles
**Parameters:**
- `name` (str): Recipient name
- `trending_posts` (list): List of trending post objects with:
  - `title`: Post title
  - `views`: View count
  - `growth`: Growth percentage (e.g., "50%")
  - `slug` or `id`: Post identifier
- `top_post_stats` (dict): Top post with:
  - `title`: Title of top post
  - `views`: View count

**Usage:**
```python
trending = [
    {"title": "ML Ops Guide", "views": 1240, "growth": "120%", "slug": "ml-ops"},
    {"title": "Docker Tips", "views": 890, "growth": "95%", "slug": "docker-tips"}
]
html = template_trending_content(
    name="Frank",
    trending_posts=trending,
    top_post_stats={"title": "ML Ops Guide", "views": 1240}
)
```

**Content:**
- "Trending" header
- Top 5 trending posts with view counts
- Growth percentages
- Top performer highlight
- Blog link

---

### 8. **Monthly Activity Recap** (`activity_recap`)
**Purpose:** Monthly summary of blog performance
**Parameters:**
- `name` (str): Recipient name
- `month` (str): Month name (e.g., "June")
- `stats` (dict): Statistics dictionary with keys:
  - `total_views`: Total pageviews
  - `new_posts`: Number of new articles
  - `subscribers`: Subscriber count
  - `avg_read_time`: Average reading time
  - `top_post_1/2/3`: Top article titles
  - `top_post_1/2/3_views`: Views for top posts
  - `insight`: Key insight or finding

**Usage:**
```python
stats = {
    "total_views": 15420,
    "new_posts": 4,
    "subscribers": 850,
    "avg_read_time": 7,
    "top_post_1": "Kubernetes Guide",
    "top_post_1_views": 2150,
    "top_post_2": "Python Patterns",
    "top_post_2_views": 1890,
    "top_post_3": "SQL Optimization",
    "top_post_3_views": 1620,
    "insight": "Technical deep-dives are resonating!"
}
html = template_activity_recap("Grace", "June", stats)
```

**Content:**
- Month title
- 4-metric grid (views, posts, subscribers, read time)
- Top 3 articles with view counts
- Key insights
- Dashboard link

---

### 9. **Subscriber Milestone** (`subscriber_milestone`)
**Purpose:** Celebrate reaching subscriber milestones
**Parameters:**
- `name` (str): Recipient name
- `milestone` (int): Milestone number (e.g., 1000)
- `celebration_message` (str, optional): Custom message

**Usage:**
```python
html = template_subscriber_milestone(
    name="Henry",
    milestone=1000,
    celebration_message="Your support drives my content!"
)
```

**Content:**
- Celebration announcement
- Milestone number display
- Thank you message
- Benefits summary
- Next milestone target
- Twitter share button

---

### 10. **Viral Content Alert** (`viral_alert`)
**Purpose:** Alert when content goes viral
**Parameters:**
- `name` (str): Recipient name
- `post_title` (str): Article title
- `current_views` (int): Current view count
- `viral_threshold` (int): Threshold for viral (e.g., 500)
- `growth_rate` (str): Growth rate (e.g., "250%/day")

**Usage:**
```python
html = template_viral_alert(
    name="Iris",
    post_title="Kubernetes Patterns",
    current_views=2350,
    viral_threshold=500,
    growth_rate="180%/day"
)
```

**Content:**
- "Going Viral" announcement
- Post title with emphasis
- View count display
- Growth rate metrics
- Viral status explanation
- Action recommendations

---

### 11. **Recruiter Interest Alert** (`recruiter_alert`)
**Purpose:** Notify when recruiters engage with content
**Parameters:**
- `name` (str): Recipient name
- `recruiter_info` (dict): Recruiter data with:
  - `company`: Company name
  - `position`: Job position
  - `seniority`: Seniority level

**Usage:**
```python
recruiter = {
    "company": "Google",
    "position": "Senior Data Engineer",
    "seniority": "Staff Level"
}
html = template_recruiter_alert("Jack", recruiter)
```

**Content:**
- "Recruiter Interest" notification
- Company and position details
- Implications of interest
- Portfolio update tips
- Resume/LinkedIn links

---

### 12. **Engagement Summary** (`engagement_summary`)
**Purpose:** Detailed reader engagement metrics
**Parameters:**
- `name` (str): Recipient name
- `period` (str): Time period (e.g., "week", "month")
- `engagement_stats` (dict): Engagement metrics with keys:
  - `pageviews`: Total page views
  - `unique_visitors`: Unique visitor count
  - `avg_session`: Average session duration (seconds)
  - `bounce_rate`: Bounce rate percentage
  - `return_rate`: Return visitor percentage
  - `social_shares`: Social media shares count
  - `source_1/2/3`: Traffic source names
  - `source_1/2/3_pct`: Traffic source percentages

**Usage:**
```python
stats = {
    "pageviews": 5420,
    "unique_visitors": 2100,
    "avg_session": "240",
    "bounce_rate": "28",
    "return_rate": "45",
    "social_shares": 156,
    "source_1": "Organic Search",
    "source_1_pct": "62",
    "source_2": "Direct",
    "source_2_pct": "22",
    "source_3": "Social Media",
    "source_3_pct": "16"
}
html = template_engagement_summary("Karen", "week", stats)
```

**Content:**
- Engagement header
- 6-metric grid (views, visitors, session, bounce, return, shares)
- Top 3 traffic sources with percentages
- Engagement insights
- Analytics dashboard link

---

### 13. **Personalized Recommendations** (`recommended_reads`)
**Purpose:** Send personalized content suggestions
**Parameters:**
- `name` (str): Recipient name
- `reading_history` (list): User's previously read posts
- `recommended_posts` (list): Recommended post objects with:
  - `title`: Post title
  - `excerpt`: Post excerpt
  - `slug` or `id`: Post identifier
  - `relevance` (optional): Match percentage (e.g., "85%")

**Usage:**
```python
recommendations = [
    {
        "title": "Advanced ETL Patterns",
        "excerpt": "Master complex data transformations...",
        "slug": "etl-patterns",
        "relevance": "92%"
    }
]
html = template_recommended_reads("Leo", [], recommendations)
```

**Content:**
- "Recommended For You" header
- Up to 5 personalized recommendations
- Post excerpts with match scores
- Individual read buttons
- "How personalization works" explanation

---

## 🚀 Integration Examples

### Using with Email Service (Resend)
```python
from scripts.python.email_templates import template_new_blog_post
import resend

html = template_new_blog_post(
    name="Subscriber",
    post_title="My Latest Article",
    post_excerpt="This is about...",
    post_slug="article-slug",
    read_time=5
)

resend.Emails.send({
    "from": "blog@example.com",
    "to": "subscriber@example.com",
    "subject": "New Blog Post: My Latest Article",
    "html": html
})
```

### Creating Custom Template Wrapper
```python
from scripts.python.email_templates import get_template

def send_notification(template_type, recipient, **kwargs):
    template_func = get_template(template_type)
    if template_func:
        kwargs['name'] = recipient['name']
        html = template_func(**kwargs)
        # Send email with html...
```

---

## 🎨 Customization

All templates use CSS variables:
- `--ink`: Text color (#0a0e14)
- `--paper`: Background color (#f5f0e8)
- `--accent`: Primary color (#ff4b2b / #c8401a)
- `--muted`: Secondary text (#7a7060)
- `--rule`: Border color (#d4cec2)

Modify `get_base_styles()` function to customize colors globally.

---

## 📊 Template Statistics

- **Total Templates:** 13
- **Total Lines of Code:** 1,200+
- **Responsive Design:** ✅ All templates
- **Dark Mode Support:** ✅ CSS variables
- **Personalization:** ✅ All templates support dynamic content
- **Accessibility:** ✅ Semantic HTML, proper contrast

---

## 🔄 Update History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | Jun 6, 2026 | Added 7 new templates (trending, activity, milestone, viral, recruiter, engagement, recommendations) |
| 1.0 | Earlier | Initial 6 templates (welcome, blog post, digest, notification, alert, event) |

---

## 📝 Notes

- All templates use responsive design for mobile/desktop
- Images display properly with fallback colors
- Links are all absolute URLs (no relative paths)
- Unsubscribe/preference links included in footers
- All templates tested with major email clients
