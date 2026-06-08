"""
Modern Email Templates for DBOS Notifications
Generate beautiful, responsive HTML emails for different events and notifications
"""

def get_base_styles():
    """Get CSS styles used in all email templates"""
    return """
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      background: #f5f5f5;
    }
    .email-container {
      max-width: 600px;
      margin: 0 auto;
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      overflow: hidden;
    }
    .email-header {
      background: linear-gradient(135deg, #ff6b6b 0%, #ff4b2b 100%);
      color: white;
      padding: 40px 30px;
      text-align: center;
    }
    .email-header h1 {
      margin: 0;
      font-size: 28px;
      font-weight: 600;
    }
    .email-content {
      padding: 40px 30px;
    }
    .email-section {
      margin-bottom: 30px;
    }
    .email-section h2 {
      color: #222;
      font-size: 20px;
      margin-top: 0;
      margin-bottom: 15px;
    }
    .email-section p {
      color: #555;
      margin: 12px 0;
    }
    .cta-button {
      display: inline-block;
      padding: 12px 28px;
      background: linear-gradient(135deg, #ff6b6b 0%, #ff4b2b 100%);
      color: white;
      text-decoration: none;
      border-radius: 6px;
      font-weight: 600;
      margin: 10px 0;
      transition: transform 0.2s;
    }
    .cta-button:hover {
      transform: translateY(-2px);
    }
    .highlight-box {
      background: #f0f7ff;
      border-left: 4px solid #3b82f6;
      padding: 15px 20px;
      margin: 20px 0;
      border-radius: 4px;
    }
    .stat-box {
      background: #f9fafb;
      border: 1px solid #e5e7eb;
      padding: 20px;
      border-radius: 8px;
      text-align: center;
      margin: 15px 0;
    }
    .stat-number {
      font-size: 28px;
      font-weight: 700;
      color: #ff4b2b;
    }
    .stat-label {
      color: #666;
      font-size: 14px;
      margin-top: 5px;
    }
    .divider {
      height: 1px;
      background: #e5e7eb;
      margin: 30px 0;
    }
    .email-footer {
      background: #f9fafb;
      padding: 30px;
      text-align: center;
      border-top: 1px solid #e5e7eb;
      color: #666;
      font-size: 13px;
    }
    .footer-links {
      margin: 15px 0;
    }
    .footer-links a {
      color: #3b82f6;
      text-decoration: none;
      margin: 0 10px;
    }
    .tag {
      display: inline-block;
      background: #e3f2fd;
      color: #1976d2;
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
      margin: 5px 5px 5px 0;
    }
    """

def template_welcome(name: str, email: str) -> str:
    """Welcome email for new subscribers"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Welcome to Victor Kipruto's Blog</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>🎉 Welcome!</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>Thanks for subscribing to my blog! You're now part of a community of data engineers and tech enthusiasts passionate about building scalable systems.</p>
          </div>
          
          <div class="email-section">
            <h2>What to Expect</h2>
            <p>I share insights on:</p>
            <ul>
              <li>Data Engineering & ETL Pipelines</li>
              <li>Real-time Streaming Systems</li>
              <li>Cloud Infrastructure & DevOps</li>
              <li>Python & SQL Optimization</li>
              <li>Best Practices & Lessons Learned</li>
            </ul>
          </div>
          
          <div class="email-section">
            <h2>Start Reading</h2>
            <p>Check out my latest posts and get caught up on everything you've missed:</p>
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html" class="cta-button">Read Blog →</a>
          </div>
          
          <div class="highlight-box">
            <strong>💡 Tip:</strong> Follow me on <a href="https://twitter.com/Victor_Kipruto">Twitter</a> and <a href="https://github.com/kipruto45">GitHub</a> for real-time updates and code samples!
          </div>
          
          <div class="email-section">
            <p>Questions or suggestions? Reply to this email or reach out on <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a>.</p>
            <p><strong>Happy learning! 🚀</strong></p>
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <div class="footer-links">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
            <a href="https://github.com/kipruto45">GitHub</a>
            <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
            <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a>
          </div>
          <p><a href="mailto:kiprutovictor39@gmail.com">kiprutovictor39@gmail.com</a></p>
          <p style="margin-top: 20px; border-top: 1px solid #e5e7eb; padding-top: 20px;">
            You received this email because you subscribed to updates. 
            <a href="#">Manage preferences</a> | <a href="#">Unsubscribe</a>
          </p>
        </div>
      </div>
    </body>
    </html>
    """

def template_new_blog_post(name: str, post_title: str, post_excerpt: str, post_slug: str, read_time: int, image_url: str = None) -> str:
    """New blog post notification with optional featured image"""
    post_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/post.html?id={post_slug}"
    
    # Optional featured image
    image_html = ""
    if image_url:
        image_html = f"""
        <div class="email-section" style="margin-bottom: 0;">
          <img src="{image_url}" alt="{post_title}" style="width: 100%; max-height: 300px; object-fit: cover; border-radius: 8px; display: block;">
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>New Blog Post: {post_title}</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>📝 New Blog Post</h1>
        </div>
        {image_html}
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>I just published a new article on my blog!</p>
          </div>
          
          <div class="email-section">
            <h2>{post_title}</h2>
            <p>{post_excerpt}</p>
            
            <div class="stat-box">
              <span class="stat-number">⏱️ {read_time}</span>
              <div class="stat-label">minutes to read</div>
            </div>
            
            <a href="{post_url}" class="cta-button">Read Full Article →</a>
          </div>
          
          <div class="email-section">
            <h2>Quick Links</h2>
            <ul>
              <li><a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html">All Articles</a></li>
              <li><a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a></li>
              <li><a href="https://github.com/kipruto45">View Projects</a></li>
            </ul>
          </div>
          
          <div class="highlight-box">
            <strong>Share this article:</strong> Help spread the word by sharing with your network on <a href="https://twitter.com/intent/tweet?url={post_url}&text={post_title}">Twitter</a>, <a href="https://www.linkedin.com/sharing/share-offsite/?url={post_url}">LinkedIn</a>, or <a href="https://wa.me/?text={post_title}%20{post_url}">WhatsApp</a>
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <div class="footer-links">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
            <a href="https://github.com/kipruto45">GitHub</a>
            <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
            <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a>
          </div>
          <p style="margin-top: 20px; border-top: 1px solid #e5e7eb; padding-top: 20px;">
            You received this email because you subscribed to blog updates. 
            <a href="#">Manage preferences</a> | <a href="#">Unsubscribe</a>
          </p>
        </div>
      </div>
    </body>
    </html>
    """

def template_weekly_digest(name: str, posts: list) -> str:
    """Weekly digest of blog posts"""
    posts_html = ""
    for post in posts:
        # Handle various field names for compatibility
        title = post.get('title', post.get('name', 'Untitled'))
        excerpt = post.get('excerpt', post.get('description', post.get('summary', '')))
        read_time = post.get('readTime', post.get('read_time', 5))
        date = post.get('date', post.get('publishDate', 'Recent'))
        tags = post.get('tags', [])
        post_id = post.get('id', post.get('slug', 'post'))
        
        posts_html += f"""
        <div class="email-section" style="border: 1px solid #e5e7eb; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
          <h3 style="margin-top: 0; color: #222;">{title}</h3>
          <p>{excerpt}</p>
          <div style="font-size: 13px; color: #666;">
            <span>⏱️ {read_time} min read</span>
            <span> • {date}</span>
            {' • '.join([f'<span class="tag">{tag}</span>' for tag in tags[:3]]) if tags else ''}
          </div>
          <a href="https://victor-kipruto-rop.github.io/victor-resum-web/post.html?id={post_id}" class="cta-button" style="font-size: 14px; padding: 10px 20px; margin-top: 10px;">Read →</a>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Weekly Digest - Victor Kipruto's Blog</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>📬 Weekly Digest</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>Here's what I published this week:</p>
          </div>
          
          {posts_html}
          
          <div class="email-section">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html" class="cta-button">View All Articles →</a>
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <div class="footer-links">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
            <a href="https://github.com/kipruto45">GitHub</a>
            <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
            <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a>
          </div>
          <p style="margin-top: 20px; border-top: 1px solid #e5e7eb; padding-top: 20px;">
            <a href="#">Change frequency</a> • <a href="#">Manage preferences</a> • <a href="#">Unsubscribe</a>
          </p>
        </div>
      </div>
    </body>
    </html>
    """

def template_notification(name: str, title: str, message: str, icon: str = "🔔", action_text: str = "Learn More", action_url: str = None) -> str:
    """Generic notification template"""
    button_html = f'<a href="{action_url}" class="cta-button">{action_text} →</a>' if action_url else ""
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{title}</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>{icon} {title}</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>{message}</p>
            {button_html}
          </div>
          
          <div class="highlight-box">
            <strong>Need help?</strong> Reply to this email or visit my <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">portfolio</a>.
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <p><a href="mailto:kiprutovictor39@gmail.com">kiprutovictor39@gmail.com</a></p>
        </div>
      </div>
    </body>
    </html>
    """

def template_dashboard_alert(name: str, alert_title: str, metrics: dict, recommendation: str) -> str:
    """Dashboard alert for metrics and analytics"""
    metrics_html = ""
    for metric, value in metrics.items():
        metrics_html += f"""
        <div class="stat-box">
          <div class="stat-label">{metric}</div>
          <span class="stat-number">{value}</span>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Dashboard Alert: {alert_title}</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>📊 {alert_title}</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>Here's a snapshot of your dashboard metrics:</p>
          </div>
          
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            {metrics_html}
          </div>
          
          <div class="highlight-box">
            <strong>💡 Recommendation:</strong> {recommendation}
          </div>
          
          <div class="email-section">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/dashboard/hub.html" class="cta-button">View Full Dashboard →</a>
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Dashboard Analytics</p>
          <p style="margin-top: 20px; border-top: 1px solid #e5e7eb; padding-top: 20px;">
            <a href="#">Manage alerts</a> • <a href="#">Unsubscribe</a>
          </p>
        </div>
      </div>
    </body>
    </html>
    """

def template_event_announcement(name: str, event_title: str, event_date: str, event_description: str, event_url: str = None) -> str:
    """Event or project announcement"""
    button_html = f'<a href="{event_url}" class="cta-button">Learn More →</a>' if event_url else ""
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{event_title}</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>🚀 {event_title}</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>I'm excited to announce something new!</p>
          </div>
          
          <div class="stat-box">
            <div class="stat-label">Date</div>
            <div style="font-size: 18px; color: #ff4b2b; font-weight: 600; margin-top: 10px;">{event_date}</div>
          </div>
          
          <div class="email-section">
            <h2>{event_title}</h2>
            <p>{event_description}</p>
            {button_html}
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <div class="footer-links">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
            <a href="https://github.com/kipruto45">GitHub</a>
            <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

def template_trending_content(name: str, trending_posts: list, top_post_stats: dict) -> str:
    """Alert for trending/viral blog content"""
    trending_html = ""
    for i, post in enumerate(trending_posts[:5], 1):
        views = post.get('views', 0)
        growth = post.get('growth', '0%')
        title = post.get('title', 'Untitled')
        slug = post.get('slug', post.get('id', 'post'))
        
        trending_html += f"""
        <div class="email-section" style="border-left: 4px solid #ff4b2b; padding-left: 15px; margin-bottom: 20px;">
          <h3 style="margin: 0 0 8px 0; color: #222;">#{i} 📈 {title}</h3>
          <div style="font-size: 13px; color: #666;">
            <span>👁️ {views:,} views</span>
            <span> • 📊 {growth} growth</span>
          </div>
          <a href="https://victor-kipruto-rop.github.io/victor-resum-web/post.html?id={slug}" class="cta-button" style="font-size: 13px; padding: 8px 16px; margin-top: 8px;">View →</a>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Trending Content Alert</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>🔥 Trending Content!</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>Some of my blog posts are trending right now! Check out what's resonating with readers:</p>
          </div>
          
          {trending_html}
          
          <div class="highlight-box">
            <strong>🏆 Top Performer:</strong> "{top_post_stats.get('title', 'N/A')}" is dominating with {top_post_stats.get('views', 0):,} views!
          </div>
          
          <div class="email-section">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html" class="cta-button">Read More Articles →</a>
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <div class="footer-links">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
            <a href="https://github.com/kipruto45">GitHub</a>
            <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

def template_activity_recap(name: str, month: str, stats: dict) -> str:
    """Monthly activity recap with blog statistics"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Activity Recap - {month}</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>📊 {month} Activity Recap</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>Here's what happened on my blog this month:</p>
          </div>
          
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div class="stat-box">
              <div class="stat-label">Total Views</div>
              <span class="stat-number">{stats.get('total_views', 0):,}</span>
            </div>
            <div class="stat-box">
              <div class="stat-label">New Articles</div>
              <span class="stat-number">{stats.get('new_posts', 0)}</span>
            </div>
            <div class="stat-box">
              <div class="stat-label">Subscribers</div>
              <span class="stat-number">{stats.get('subscribers', 0):,}</span>
            </div>
            <div class="stat-box">
              <div class="stat-label">Avg Read Time</div>
              <span class="stat-number">{stats.get('avg_read_time', 0)} min</span>
            </div>
          </div>
          
          <div class="email-section" style="margin-top: 30px;">
            <h2>Top Articles This Month</h2>
            <ul style="list-style: none; padding: 0;">
              <li style="margin-bottom: 10px;">
                <strong>1. {stats.get('top_post_1', 'Article 1')}</strong><br>
                <span style="font-size: 13px; color: #666;">👁️ {stats.get('top_post_1_views', 0):,} views</span>
              </li>
              <li style="margin-bottom: 10px;">
                <strong>2. {stats.get('top_post_2', 'Article 2')}</strong><br>
                <span style="font-size: 13px; color: #666;">👁️ {stats.get('top_post_2_views', 0):,} views</span>
              </li>
              <li>
                <strong>3. {stats.get('top_post_3', 'Article 3')}</strong><br>
                <span style="font-size: 13px; color: #666;">👁️ {stats.get('top_post_3_views', 0):,} views</span>
              </li>
            </ul>
          </div>
          
          <div class="highlight-box">
            <strong>💡 Insight:</strong> {stats.get('insight', 'Your readers are engaging with technical deep-dives the most!')}
          </div>
          
          <div class="email-section">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/dashboard/hub.html" class="cta-button">View Full Dashboard →</a>
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <div class="footer-links">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
            <a href="https://github.com/kipruto45">GitHub</a>
            <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

def template_subscriber_milestone(name: str, milestone: int, celebration_message: str = "") -> str:
    """Celebrate subscriber milestones"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>🎉 We Hit {milestone} Subscribers!</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>🎉 We Did It!</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>Thanks to amazing subscribers like you, we just hit <strong>{milestone:,} subscribers!</strong></p>
          </div>
          
          <div class="stat-box">
            <span class="stat-number">{milestone:,}</span>
            <div class="stat-label">Amazing Readers</div>
          </div>
          
          <div class="email-section">
            <h2>Thank You! 🙏</h2>
            <p>{celebration_message or "Your support means everything. I'm committed to delivering high-quality technical content that helps you grow as a developer."}</p>
            <ul>
              <li>Exclusive technical deep-dives</li>
              <li>Real-world project walkthroughs</li>
              <li>Best practices & lessons learned</li>
              <li>Early access to new content</li>
            </ul>
          </div>
          
          <div class="highlight-box">
            <strong>Next milestone:</strong> {milestone + 500:,} subscribers! Help me get there by sharing your favorite articles with friends and colleagues.
          </div>
          
          <div class="email-section">
            <a href="https://twitter.com/intent/tweet?text=Just%20subscribed%20to%20Victor%20Kipruto%27s%20blog%21%20Great%20technical%20content%20on%20data%20engineering%20and%20cloud%20infrastructure%21%20https%3A%2F%2Fvictor-kipruto-rop.github.io%2Fvictor-resum-web%2Fblog.html" class="cta-button">Share on Twitter →</a>
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <div class="footer-links">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
            <a href="https://github.com/kipruto45">GitHub</a>
            <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

def template_viral_alert(name: str, post_title: str, current_views: int, viral_threshold: int, growth_rate: str) -> str:
    """Alert when content becomes viral"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>🚀 Viral Alert: {post_title}</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>🚀 Content Going Viral!</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>Exciting news! One of my articles is trending and getting tons of attention:</p>
          </div>
          
          <div class="email-section" style="border: 2px solid #ff4b2b; padding: 20px; border-radius: 8px;">
            <h2 style="margin-top: 0; color: #ff4b2b;">"{post_title}"</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0;">
              <div class="stat-box">
                <div class="stat-label">Current Views</div>
                <span class="stat-number">{current_views:,}</span>
              </div>
              <div class="stat-box">
                <div class="stat-label">Growth Rate</div>
                <span class="stat-number">{growth_rate}</span>
              </div>
            </div>
            
            <p style="font-size: 13px; color: #666;">
              <strong>Viral Status:</strong> This post has exceeded the {viral_threshold:,} view threshold and is spreading rapidly across social media!
            </p>
          </div>
          
          <div class="highlight-box">
            <strong>💡 Action:</strong> Now is the perfect time to share this on your networks and capitalize on the momentum!
          </div>
          
          <div class="email-section">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html" class="cta-button">View All Articles →</a>
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <div class="footer-links">
            <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
            <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a>
            <a href="https://github.com/kipruto45">GitHub</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

def template_recruiter_alert(name: str, recruiter_info: dict) -> str:
    """Alert when a recruiter/FAANG company engages with content"""
    company = recruiter_info.get('company', 'FAANG Company')
    position = recruiter_info.get('position', 'Senior Engineer')
    seniority = recruiter_info.get('seniority', 'Unknown')
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>👔 Recruiter Interest Alert</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>👔 Recruiter Interest Detected</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>Great news! A recruiter from a top company has been engaging with your content:</p>
          </div>
          
          <div class="highlight-box">
            <strong>Company:</strong> {company}<br>
            <strong>Likely Position:</strong> {position}<br>
            <strong>Seniority:</strong> {seniority}
          </div>
          
          <div class="email-section">
            <h2>What This Means</h2>
            <ul>
              <li>Your technical content is impressing industry professionals</li>
              <li>Companies are actively viewing your portfolio and projects</li>
              <li>This is a great opportunity to strengthen your professional network</li>
            </ul>
          </div>
          
          <div class="email-section">
            <h2>Next Steps</h2>
            <ol>
              <li>Update your <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">portfolio</a> with your latest projects</li>
              <li>Ensure your <a href="https://github.com/kipruto45">GitHub</a> is up to date</li>
              <li>Connect on <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a> to be found</li>
            </ol>
          </div>
          
          <div class="email-section">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/resume.html" class="cta-button">View Your Resume →</a>
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <div class="footer-links">
            <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a>
            <a href="https://github.com/kipruto45">GitHub</a>
            <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
          </div>
          <p style="margin-top: 20px; border-top: 1px solid #e5e7eb; padding-top: 20px;">
            This is an automated alert based on visitor analytics. <a href="#">Disable these alerts</a>
          </p>
        </div>
      </div>
    </body>
    </html>
    """

def template_engagement_summary(name: str, period: str, engagement_stats: dict) -> str:
    """Summary of reader engagement metrics"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Reader Engagement Summary</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>📈 Engagement Summary</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>Here's how my readers engaged with my content this {period}:</p>
          </div>
          
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div class="stat-box">
              <div class="stat-label">Total Pageviews</div>
              <span class="stat-number">{engagement_stats.get('pageviews', 0):,}</span>
            </div>
            <div class="stat-box">
              <div class="stat-label">Unique Visitors</div>
              <span class="stat-number">{engagement_stats.get('unique_visitors', 0):,}</span>
            </div>
            <div class="stat-box">
              <div class="stat-label">Avg Session Duration</div>
              <span class="stat-number">{engagement_stats.get('avg_session', '0')}s</span>
            </div>
            <div class="stat-box">
              <div class="stat-label">Bounce Rate</div>
              <span class="stat-number">{engagement_stats.get('bounce_rate', '0')}%</span>
            </div>
            <div class="stat-box">
              <div class="stat-label">Return Visitors</div>
              <span class="stat-number">{engagement_stats.get('return_rate', '0')}%</span>
            </div>
            <div class="stat-box">
              <div class="stat-label">Social Shares</div>
              <span class="stat-number">{engagement_stats.get('social_shares', 0):,}</span>
            </div>
          </div>
          
          <div class="email-section" style="margin-top: 30px;">
            <h2>Top Traffic Sources</h2>
            <ul style="list-style: none; padding: 0;">
              <li style="padding: 10px 0; border-bottom: 1px solid #e5e7eb;">
                <strong>{engagement_stats.get('source_1', 'Organic Search')}</strong>
                <span style="float: right; color: #ff4b2b; font-weight: 600;">{engagement_stats.get('source_1_pct', '0')}%</span>
              </li>
              <li style="padding: 10px 0; border-bottom: 1px solid #e5e7eb;">
                <strong>{engagement_stats.get('source_2', 'Direct')}</strong>
                <span style="float: right; color: #ff4b2b; font-weight: 600;">{engagement_stats.get('source_2_pct', '0')}%</span>
              </li>
              <li style="padding: 10px 0;">
                <strong>{engagement_stats.get('source_3', 'Social Media')}</strong>
                <span style="float: right; color: #ff4b2b; font-weight: 600;">{engagement_stats.get('source_3_pct', '0')}%</span>
              </li>
            </ul>
          </div>
          
          <div class="email-section">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/dashboard/hub.html" class="cta-button">View Detailed Analytics →</a>
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <div class="footer-links">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
            <a href="https://github.com/kipruto45">GitHub</a>
            <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

def template_recommended_reads(name: str, reading_history: list, recommended_posts: list) -> str:
    """Personalized recommendations based on reading history"""
    recommendations_html = ""
    for i, post in enumerate(recommended_posts[:5], 1):
        title = post.get('title', 'Untitled')
        excerpt = post.get('excerpt', '')
        slug = post.get('slug', post.get('id', 'post'))
        relevance = post.get('relevance', '85%')
        
        recommendations_html += f"""
        <div class="email-section" style="border: 1px solid #e5e7eb; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
          <h3 style="margin: 0 0 8px 0; color: #222;">{i}. {title}</h3>
          <p style="font-size: 13px; color: #666; margin: 8px 0; line-height: 1.5;">{excerpt}</p>
          <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
            <span style="color: #666;">Match: <strong>{relevance}</strong></span>
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/post.html?id={slug}" style="color: #ff4b2b; text-decoration: none; font-weight: 600;">Read →</a>
          </div>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Personalized Recommendations</title>
      <style>
        {get_base_styles()}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="email-header">
          <h1>📚 Recommended For You</h1>
        </div>
        
        <div class="email-content">
          <div class="email-section">
            <p>Hi {name},</p>
            <p>Based on the articles you've been reading, here are some posts I think you'll love:</p>
          </div>
          
          {recommendations_html}
          
          <div class="email-section">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html" class="cta-button">Explore All Articles →</a>
          </div>
          
          <div class="highlight-box">
            <strong>💡 Did you know?</strong> I personalize these recommendations based on your reading habits to help you discover content that's most relevant to your interests.
          </div>
        </div>
        
        <div class="email-footer">
          <p><strong>Victor Kipruto Rop</strong> | Data Engineer & Full Stack Developer</p>
          <div class="footer-links">
            <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
            <a href="https://github.com/kipruto45">GitHub</a>
            <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
          </div>
          <p style="margin-top: 20px; border-top: 1px solid #e5e7eb; padding-top: 20px;">
            <a href="#">Manage preferences</a> • <a href="#">Unsubscribe</a>
          </p>
        </div>
      </div>
    </body>
    </html>
    """

# Export all templates
TEMPLATES = {
    'welcome': template_welcome,
    'new_blog_post': template_new_blog_post,
    'weekly_digest': template_weekly_digest,
    'notification': template_notification,
    'dashboard_alert': template_dashboard_alert,
    'event_announcement': template_event_announcement,
    'trending_content': template_trending_content,
    'activity_recap': template_activity_recap,
    'subscriber_milestone': template_subscriber_milestone,
    'viral_alert': template_viral_alert,
    'recruiter_alert': template_recruiter_alert,
    'engagement_summary': template_engagement_summary,
    'recommended_reads': template_recommended_reads,
}

def get_template(template_type: str):
    """Get a template by type"""
    return TEMPLATES.get(template_type)
