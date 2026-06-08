"""
Modern, Enhanced Email Templates for Blog Notifications
Generate beautiful, responsive HTML emails with working unsubscribe functionality
"""

import hashlib
import urllib.parse

def generate_unsubscribe_token(email: str) -> str:
    """Generate a unique unsubscribe token for the subscriber"""
    return hashlib.sha256(email.encode()).hexdigest()[:16]

def get_base_styles():
    """Get enhanced CSS styles used in all email templates - matching blog.html design"""
    return """
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      font-family: 'DM Mono', 'Courier New', monospace;
      line-height: 1.8;
      color: #0a0e14;
      background: #f5f0e8;
      min-height: 100%;
    }
    .email-wrapper {
      padding: 20px;
      background: #f5f0e8;
    }
    .email-container {
      max-width: 600px;
      margin: 0 auto;
      background: #ffffff;
      border-radius: 4px;
      box-shadow: 0 4px 12px rgba(10, 14, 20, 0.08);
      overflow: hidden;
      border: 1px solid #d4cec2;
    }
    .email-header {
      background: linear-gradient(135deg, #c8401a 0%, #9a2f12 100%);
      color: white;
      padding: 50px 30px;
      text-align: center;
      position: relative;
      overflow: hidden;
    }
    .email-header::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.08) 0%, transparent 50%),
                  radial-gradient(circle at 80% 80%, rgba(255,255,255,0.04) 0%, transparent 50%);
      pointer-events: none;
    }
    .email-header h1 {
      margin: 0;
      font-size: 32px;
      font-weight: 700;
      position: relative;
      z-index: 1;
      letter-spacing: -0.3px;
      font-family: 'DM Serif Display', serif;
    }
    .email-header .subtitle {
      font-size: 14px;
      opacity: 0.95;
      margin-top: 8px;
      position: relative;
      z-index: 1;
      font-weight: 300;
      font-family: 'Syne', sans-serif;
    }
    .email-content {
      padding: 40px 30px;
    }
    .email-section {
      margin-bottom: 30px;
    }
    .email-section h2 {
      color: #0a0e14;
      font-size: 22px;
      margin-top: 0;
      margin-bottom: 16px;
      font-weight: 700;
      position: relative;
      padding-bottom: 10px;
      font-family: 'Syne', sans-serif;
    }
    .email-section h2::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 40px;
      height: 2px;
      background: #c8401a;
      border-radius: 1px;
    }
    .email-section p {
      color: #0a0e14;
      margin: 14px 0;
      font-size: 15px;
      line-height: 1.8;
      opacity: 0.9;
    }
    .email-section ul, .email-section ol {
      margin: 16px 0 16px 20px;
      color: #0a0e14;
    }
    .email-section li {
      margin: 10px 0;
      font-size: 15px;
      line-height: 1.6;
    }
    .email-icon {
      display: inline-block;
      width: 32px;
      height: 32px;
      background: #c8401a;
      color: white;
      border-radius: 4px;
      text-align: center;
      line-height: 32px;
      margin-right: 10px;
      font-size: 14px;
      vertical-align: middle;
    }
    .email-section a {
      color: #c8401a;
      text-decoration: none;
      font-weight: 600;
      border-bottom: 2px solid #c8401a;
      transition: all 0.3s ease;
    }
    .email-section a:hover {
      color: #9a2f12;
      border-bottom-color: #9a2f12;
    }
    .cta-button {
      display: inline-block;
      padding: 14px 32px;
      background: #c8401a;
      color: white !important;
      text-decoration: none !important;
      border-radius: 4px;
      font-weight: 700;
      margin: 16px 0;
      transition: all 0.3s ease;
      box-shadow: 0 4px 12px rgba(200, 64, 26, 0.2);
      border: none;
      cursor: pointer;
      font-size: 15px;
      letter-spacing: 0.3px;
      border-bottom: none !important;
      text-transform: uppercase;
    }
    .cta-button:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(200, 64, 26, 0.35);
      background: #9a2f12;
    }
    .secondary-button {
      display: inline-block;
      padding: 12px 28px;
      background: transparent;
      color: #c8401a !important;
      text-decoration: none !important;
      border-radius: 4px;
      font-weight: 600;
      margin: 12px 8px 12px 0;
      transition: all 0.3s ease;
      font-size: 14px;
      border: 2px solid #c8401a;
      border-bottom: 2px solid #c8401a;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .secondary-button:hover {
      background: #c8401a;
      color: white !important;
    }
    .highlight-box {
      background: #f5f0e8;
      border-left: 4px solid #c8401a;
      padding: 20px 20px;
      margin: 24px 0;
      border-radius: 4px;
    }
    .highlight-box strong {
      color: #0a0e14;
      font-weight: 700;
    }
    .info-box {
      background: #fef3c7;
      border-left: 4px solid #f59e0b;
      padding: 20px;
      margin: 24px 0;
      border-radius: 4px;
      border: 1px solid #d4cec2;
    }
    .success-box {
      background: #dcfce7;
      border-left: 4px solid #10b981;
      padding: 20px;
      margin: 24px 0;
      border-radius: 4px;
      border: 1px solid #d4cec2;
    }
    .stat-box {
      background: #f5f0e8;
      border: 1px solid #d4cec2;
      padding: 24px;
      border-radius: 4px;
      text-align: center;
      margin: 16px 0;
      transition: all 0.3s ease;
    }
    .stat-box:hover {
      border-color: #c8401a;
      box-shadow: 0 4px 12px rgba(200, 64, 26, 0.1);
      transform: translateY(-2px);
    }
    .stat-number {
      font-size: 36px;
      font-weight: 800;
      color: #c8401a;
      margin: 8px 0;
      font-family: 'DM Serif Display', serif;
    }
    .stat-label {
      color: #7a7060;
      font-size: 14px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .divider {
      height: 1px;
      background: #d4cec2;
      margin: 32px 0;
    }
    .content-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin: 24px 0;
    }
    .grid-item {
      background: #f5f0e8;
      padding: 16px;
      border-radius: 4px;
      border: 1px solid #d4cec2;
    }
    .grid-item h3 {
      color: #0a0e14;
      font-size: 14px;
      font-weight: 700;
      margin-bottom: 8px;
      text-transform: uppercase;
      font-family: 'Syne', sans-serif;
    }
    .grid-item p {
      color: #0a0e14;
      font-size: 13px;
      margin: 0;
    }
    .email-footer {
      background: #0a0e14;
      padding: 40px 30px;
      text-align: center;
      color: #a1a1aa;
      font-size: 12px;
    }
    .footer-links {
      margin: 20px 0;
    }
    .footer-links a {
      color: #a1a1aa;
      text-decoration: none;
      margin: 0 12px;
      font-weight: 500;
      transition: color 0.3s ease;
      border-bottom: none !important;
    }
    .footer-links a:hover {
      color: #c8401a;
    }
    .unsubscribe-notice {
      color: #a1a1aa;
      font-size: 11px;
      margin-top: 24px;
      padding-top: 20px;
      border-top: 1px solid #27272a;
    }
    .unsubscribe-notice a {
      color: #c8401a;
      text-decoration: none;
      border-bottom: none !important;
    }
    .unsubscribe-notice a:hover {
      text-decoration: underline;
    }
    .tag {
      display: inline-block;
      background: rgba(200, 64, 26, 0.1);
      color: #c8401a;
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 700;
      margin: 6px 6px 6px 0;
      border: 1px solid #d4cec2;
    }
    .tag.hot {
      background: #fee2e2;
      color: #7f1d1d;
      border-color: #fca5a5;
    }
    .tag.featured {
      background: #fef3c7;
      color: #78350f;
      border-color: #fcd34d;
    }
    .badge {
      display: inline-block;
      background: #c8401a;
      color: white;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }
    .social-links {
      margin: 20px 0;
      text-align: center;
    }
    .social-icon {
      display: inline-block;
      width: 36px;
      height: 36px;
      margin: 0 8px;
      background: #c8401a;
      border-radius: 4px;
      text-align: center;
      line-height: 36px;
      color: white;
      font-size: 16px;
      text-decoration: none;
      transition: all 0.3s ease;
      border-bottom: none !important;
    }
    .social-icon:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(200, 64, 26, 0.3);
      background: #9a2f12;
    }
    .feature-list {
      list-style: none;
      margin: 20px 0;
    }
    .feature-list li {
      padding: 12px 0;
      padding-left: 28px;
      position: relative;
      color: #0a0e14;
    }
    .feature-list li::before {
      content: '✓';
      position: absolute;
      left: 0;
      color: #10b981;
      font-weight: 700;
      font-size: 18px;
    }
    .image-card {
      margin: 24px 0;
      border-radius: 4px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(200, 64, 26, 0.1);
    }
    .image-card img {
      width: 100%;
      display: block;
      max-height: 350px;
      object-fit: cover;
    }
    @media (max-width: 600px) {
      .email-container {
        border-radius: 4px;
      }
      .content-grid {
        grid-template-columns: 1fr;
      }
      .email-header h1 {
        font-size: 24px;
      }
      .email-content {
        padding: 24px 16px;
      }
    }
    """

# Template 1: Welcome Email
def template_welcome(name: str, email: str) -> str:
    """Enhanced welcome email for new subscribers - Blog design with modern icons"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Welcome to Victor Kipruto's Blog</title>
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>Welcome Aboard!</h1>
            <p class="subtitle">You're about to discover world-class technical insights</p>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>Thank you for subscribing to my blog! You've just joined a vibrant community of <strong>data engineers, cloud architects, and full-stack developers</strong> who are passionate about building scalable, modern systems.</p>
            </div>
            
            <div class="email-section">
              <h2>What to Expect</h2>
              <ul class="feature-list">
                <li><span class="email-icon">◆</span> <strong>Deep Technical Dives:</strong> In-depth tutorials on data engineering, ETL pipelines, and real-time systems</li>
                <li><span class="email-icon">☁</span> <strong>Cloud Infrastructure:</strong> AWS, GCP, and Kubernetes best practices with real-world examples</li>
                <li><span class="email-icon">⚡</span> <strong>Code Optimization:</strong> Python and SQL performance tuning techniques</li>
                <li><span class="email-icon">★</span> <strong>Lessons Learned:</strong> Hard-won insights from building production systems</li>
                <li><span class="email-icon">📬</span> <strong>Weekly Digests:</strong> Curated content delivered straight to your inbox</li>
              </ul>
            </div>
            
            <div class="highlight-box">
              <strong>Pro Tip:</strong> Check out my <a href="https://github.com/kipruto45">GitHub repositories</a> to see code samples and projects that complement the blog posts!
            </div>
            
            <div class="email-section">
              <h2>Get Started Now</h2>
              <p>Explore my latest articles and get caught up on everything you've missed:</p>
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html" class="cta-button">Start Reading Blog</a>
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/" class="secondary-button">View Portfolio</a>
            </div>
            
            <div class="content-grid">
              <div class="grid-item">
                <h3>Latest Articles</h3>
                <p>Deep dives into data engineering, cloud infrastructure, and modern DevOps practices</p>
              </div>
              <div class="grid-item">
                <h3>Code Examples</h3>
                <p>Production-ready code samples and best practices from real-world projects</p>
              </div>
            </div>
            
            <div class="email-section">
              <h2>Connect With Me</h2>
              <div class="social-links">
                <a href="https://twitter.com/Victor_Kipruto" class="social-icon" title="Twitter">f</a>
                <a href="https://github.com/kipruto45" class="social-icon" title="GitHub">g</a>
                <a href="https://linkedin.com/in/victor-kipruto-rop" class="social-icon" title="LinkedIn">in</a>
                <a href="mailto:kiprutovictor39@gmail.com" class="social-icon" title="Email">@</a>
              </div>
            </div>
            
            <div class="highlight-box">
              <strong>Questions?</strong> Feel free to reply to this email or reach out on any of my social channels. I love hearing from readers!
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer • Full Stack Developer • Tech Content Creator</p>
            <div class="footer-links">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
              <a href="https://github.com/kipruto45">GitHub</a>
              <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
              <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              You received this because you subscribed. <a href="{unsubscribe_url}">Unsubscribe</a> • <a href="#">Update Preferences</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 2: New Blog Post
def template_new_blog_post(name: str, email: str, post_title: str, post_excerpt: str, post_slug: str, read_time: int, image_url: str = None) -> str:
    """Enhanced new blog post notification"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    post_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/post.html?id={post_slug}"
    
    image_html = ""
    if image_url:
        image_html = f'<div class="image-card"><img src="{image_url}" alt="{post_title}" style="width:100%; height:auto;"></div>'
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>New Blog Post: {post_title}</title>
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>New Article Published</h1>
            <p class="subtitle">Fresh insights from the tech trenches</p>
          </div>
          
          {image_html}
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>I just published a brand new article on my blog that I think you'll find incredibly valuable!</p>
            </div>
            
            <div class="email-section">
              <h2>{post_title}</h2>
              <p>{post_excerpt}</p>
              
              <div class="stat-box">
                <div class="stat-label">⏱ Reading Time</div>
                <span class="stat-number">{read_time} min read</span>
                <p style="margin: 8px 0 0 0; font-size: 14px; color: #7a7060;">Perfect for your coffee break</p>
              </div>
              
              <a href="{post_url}" class="cta-button">Read Full Article</a>
            </div>
            
            <div class="email-section">
              <h2>In This Article</h2>
              <ul>
                <li>Comprehensive technical overview and fundamentals</li>
                <li>Real-world examples and use cases</li>
                <li>Best practices and performance optimization tips</li>
                <li>Code samples and implementation patterns</li>
                <li>Common pitfalls and how to avoid them</li>
              </ul>
            </div>
            
            <div class="success-box">
              <strong>Share This Article</strong><br>
              Found this valuable? Help spread the word by sharing with your network!
            </div>
            
            <div class="content-grid">
              <div class="grid-item">
                <h3>More Articles</h3>
                <p><a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html">Browse All</a></p>
              </div>
              <div class="grid-item">
                <h3>Code Examples</h3>
                <p><a href="https://github.com/kipruto45">GitHub</a></p>
              </div>
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer & Full Stack Developer</p>
            <div class="footer-links">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
              <a href="https://github.com/kipruto45">GitHub</a>
              <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
              <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="{unsubscribe_url}">Unsubscribe</a> • <a href="#">Update Preferences</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 3: Weekly Digest
def template_weekly_digest(name: str, email: str, posts: list) -> str:
    """Enhanced weekly digest"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    
    posts_html = ""
    for i, post in enumerate(posts, 1):
        title = post.get('title', 'Untitled')
        excerpt = post.get('excerpt', '')
        read_time = post.get('readTime', 5)
        post_id = post.get('id', post.get('slug', 'post'))
        
        posts_html += f"""
        <div class="email-section" style="border: 2px solid #e9ecef; padding: 20px; border-radius: 10px; margin-bottom: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
              <span class="badge">{i}</span>
              <h3 style="color: #2d3748; font-size: 18px; margin: 8px 0; font-weight: 700;">{title}</h3>
              <p style="color: #718096; margin: 8px 0; font-size: 13px;">⏱️ {read_time} min read</p>
              <p style="color: #4a5568; margin: 12px 0; font-size: 14px; line-height: 1.6;">{excerpt}</p>
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/post.html?id={post_id}" class="secondary-button" style="margin-top: 12px;">Read Article →</a>
            </div>
          </div>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Weekly Digest - Victor Kipruto's Blog</title>
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>Your Weekly Digest</h1>
            <p class="subtitle">This week's best technical insights</p>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>Here's what I published this week that you don't want to miss:</p>
            </div>
            
            {posts_html}
            
            <div class="email-section">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html" class="cta-button">Browse All Articles</a>
            </div>
            
            <div class="success-box">
              <strong>Customize Your Experience</strong><br>
              You can now customize which topics you want to receive. <a href="#">Update Your Preferences</a>
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer & Full Stack Developer</p>
            <div class="footer-links">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
              <a href="https://github.com/kipruto45">GitHub</a>
              <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
              <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html?frequency=daily">Change Frequency</a> • <a href="{unsubscribe_url}">Unsubscribe</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 4: Trending Content Alert
def template_trending_content(name: str, email: str, trending_posts: list, top_post_stats: dict) -> str:
    """Alert for trending/viral content"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    
    trending_html = ""
    for i, post in enumerate(trending_posts[:5], 1):
        views = post.get('views', 0)
        growth = post.get('growth', '0%')
        title = post.get('title', 'Untitled')
        slug = post.get('slug', post.get('id', 'post'))
        
        trending_html += f"""
        <div class="email-section" style="border-left: 5px solid #f59e0b; padding: 16px 16px 16px 20px; background: #fffaf0; margin-bottom: 14px; border-radius: 6px;">
          <h3 style="margin: 0 0 8px 0; color: #92400e; font-size: 16px;">#{i} 🔥 {title}</h3>
          <div style="font-size: 13px; color: #a16207; margin-bottom: 10px;">
            👁️ <strong>{views:,} views</strong> • 📈 <strong>{growth} growth</strong>
          </div>
          <a href="https://victor-kipruto-rop.github.io/victor-resum-web/post.html?id={slug}" class="secondary-button" style="font-size: 13px; padding: 10px 16px;">View Article →</a>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Trending Content Alert</title>
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>Content Going Viral!</h1>
            <p class="subtitle">These articles are resonating with readers</p>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>Some of my blog posts are trending right now! Here are the hottest articles getting massive engagement:</p>
            </div>
            
            {trending_html}
            
            <div class="success-box">
              <strong>Top Performer This Week</strong><br>
              <strong>"{top_post_stats.get('title', 'N/A')}"</strong><br>
              With an impressive <strong>{top_post_stats.get('views', 0):,} views</strong> and <strong>{top_post_stats.get('share_count', 0)} social shares</strong>, this is dominating the conversation!
            </div>
            
            <div class="email-section">
              <p><strong>Why This Matters:</strong> These trending articles represent the topics readers are most interested in. If you haven't read them yet, they're definitely worth your time!</p>
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html" class="cta-button">Explore More Articles</a>
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer & Full Stack Developer</p>
            <div class="footer-links">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
              <a href="https://github.com/kipruto45">GitHub</a>
              <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="{unsubscribe_url}">Unsubscribe</a> • <a href="#">Manage Alerts</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 5: Monthly Activity Recap
def template_activity_recap(name: str, email: str, month: str, stats: dict) -> str:
    """Monthly activity recap"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Activity Recap - {month}</title>
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>Activity Recap</h1>
            <p class="subtitle">Here's what happened on the blog this month</p>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>It's been an amazing {month}! Here's a comprehensive breakdown of blog performance:</p>
            </div>
            
            <div class="content-grid">
              <div class="stat-box">
                <div class="stat-label">Total Views</div>
                <span class="stat-number">{stats.get('total_views', 0):,}</span>
              </div>
              <div class="stat-box">
                <div class="stat-label">New Articles</div>
                <span class="stat-number">{stats.get('new_posts', 0)}</span>
              </div>
              <div class="stat-box">
                <div class="stat-label">New Subscribers</div>
                <span class="stat-number">+{stats.get('new_subscribers', 0)}</span>
              </div>
              <div class="stat-box">
                <div class="stat-label">Avg Read Time</div>
                <span class="stat-number">{stats.get('avg_read_time', 0)}m</span>
              </div>
            </div>
            
            <div class="email-section">
              <h2>Top 3 Articles This Month</h2>
              <ol>
                <li><strong>{stats.get('top_post_1', 'Article 1')}</strong><br><span style="color: #7a7060; font-size: 14px;">{stats.get('top_post_1_views', 0):,} views</span></li>
                <li><strong>{stats.get('top_post_2', 'Article 2')}</strong><br><span style="color: #7a7060; font-size: 14px;">{stats.get('top_post_2_views', 0):,} views</span></li>
                <li><strong>{stats.get('top_post_3', 'Article 3')}</strong><br><span style="color: #7a7060; font-size: 14px;">{stats.get('top_post_3_views', 0):,} views</span></li>
              </ol>
            </div>
            
            <div class="success-box">
              <strong>Key Insight:</strong> {stats.get('insight', 'Your readers are most engaged with technical deep-dives and real-world case studies!')}
            </div>
            
            <div class="email-section">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/dashboard/hub.html" class="cta-button">View Full Dashboard</a>
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer & Full Stack Developer</p>
            <div class="footer-links">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
              <a href="https://github.com/kipruto45">GitHub</a>
              <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="{unsubscribe_url}">Unsubscribe</a> • <a href="#">Preferences</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 6: Milestone Celebration
def template_subscriber_milestone(name: str, email: str, milestone: int, celebration_message: str = "") -> str:
    """Celebrate subscriber milestones"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>We Hit {milestone} Subscribers!</title>
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>We Did It!</h1>
            <p class="subtitle">You're part of something special</p>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>I'm thrilled to share that we've just hit <strong>{milestone:,} subscribers</strong>!</p>
            </div>
            
            <div class="stat-box">
              <span class="stat-number">{milestone:,}</span>
              <div class="stat-label">Incredible Readers</div>
              <p style="margin: 12px 0 0 0; font-size: 14px; color: #7a7060;">And growing every day!</p>
            </div>
            
            <div class="email-section">
              <h2>Thank You</h2>
              <p>{celebration_message or "This milestone wouldn't be possible without your support and engagement. Your comments, shares, and questions inspire me to keep creating high-quality content that matters."}</p>
              <p><strong>What I'm committed to:</strong></p>
              <ul class="feature-list">
                <li>Deep technical content that goes beyond surface-level tutorials</li>
                <li>Real-world project walkthroughs and case studies</li>
                <li>Best practices learned from production environments</li>
                <li>Honest lessons from failures and mistakes</li>
                <li>Early access to experimental ideas and concepts</li>
              </ul>
            </div>
            
            <div class="success-box">
              <strong>Next Goal:</strong> {milestone + 500:,} subscribers!<br><br>
              Help me get there by sharing your favorite articles with colleagues and friends.
            </div>
            
            <div class="email-section">
              <div class="social-links">
                <a href="https://twitter.com/Victor_Kipruto" class="social-icon" title="Twitter">𝕏</a>
                <a href="https://github.com/kipruto45" class="social-icon" title="GitHub">◆</a>
                <a href="https://linkedin.com/in/victor-kipruto-rop" class="social-icon" title="LinkedIn">in</a>
              </div>
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer & Full Stack Developer</p>
            <div class="footer-links">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
              <a href="https://github.com/kipruto45">GitHub</a>
              <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="{unsubscribe_url}">Unsubscribe</a> • <a href="#">Preferences</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 7: Viral Alert
def template_viral_alert(name: str, email: str, post_title: str, current_views: int, viral_threshold: int, growth_rate: str) -> str:
    """Alert when content becomes viral"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Viral Alert: {post_title}</title>
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>Content Going Viral!</h1>
            <p class="subtitle">An article is experiencing explosive growth</p>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>Exciting news! One of my articles is trending and getting tons of attention right now!</p>
            </div>
            
            <div class="email-section" style="border: 3px solid #c8401a; padding: 24px; border-radius: 4px; background: #f5f0e8;">
              <h2 style="margin-top: 0; color: #0a0e14;">"<strong>{post_title}</strong>"</h2>
              
              <div class="content-grid" style="margin: 24px 0;">
                <div class="stat-box">
                  <div class="stat-label">Current Views</div>
                  <span class="stat-number">{current_views:,}</span>
                </div>
                <div class="stat-box">
                  <div class="stat-label">Growth Rate</div>
                  <span class="stat-number">{growth_rate}</span>
                </div>
              </div>
              
              <p style="font-size: 14px; color: #0a0e14; margin: 0;">
                <strong>Viral Status Activated!</strong><br>
                This post has exceeded the {viral_threshold:,} view threshold and is spreading rapidly across social media!
              </p>
            </div>
            
            <div class="success-box">
              <strong>Action Items:</strong>
              <ul style="margin: 12px 0 0 0; list-style: none; padding: 0;">
                <li>✓ Share on all your social channels to capitalize on momentum</li>
                <li>✓ Update your social profiles to highlight this achievement</li>
                <li>✓ Engage with comments and discussions in real-time</li>
                <li>✓ Consider creating follow-up content based on reader engagement</li>
              </ul>
            </div>
            
            <div class="email-section">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html" class="cta-button">View All Articles</a>
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer & Full Stack Developer</p>
            <div class="footer-links">
              <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
              <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a>
              <a href="https://github.com/kipruto45">GitHub</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="{unsubscribe_url}">Unsubscribe</a> • <a href="#">Preferences</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 8: Event Announcement
def template_event_announcement(name: str, email: str, event_title: str, event_date: str, event_description: str, event_url: str = None) -> str:
    """Project or event announcement"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    button_html = f'<a href="{event_url}" class="cta-button">🎯 Learn More →</a>' if event_url else ""
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{event_title}</title>
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>{event_title}</h1>
            <p class="subtitle">Something exciting is happening</p>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>I'm thrilled to announce something new and exciting!</p>
            </div>
            
            <div class="stat-box">
              <div class="stat-label">Date</div>
              <div style="font-size: 20px; color: #c8401a; font-weight: 700; margin-top: 12px;">{event_date}</div>
            </div>
            
            <div class="email-section">
              <h2>{event_title}</h2>
              <p>{event_description}</p>
              {button_html}
            </div>
            
            <div class="success-box">
              <strong>Why You Should Care:</strong> This represents a significant milestone and evolution in my work. It's designed specifically for people like you who are passionate about technical excellence and continuous learning.
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer & Full Stack Developer</p>
            <div class="footer-links">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
              <a href="https://github.com/kipruto45">GitHub</a>
              <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="{unsubscribe_url}">Unsubscribe</a> • <a href="#">Preferences</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 9: Recruiter Alert
def template_recruiter_alert(name: str, email: str, recruiter_info: dict) -> str:
    """Recruiter interest detected"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    company = recruiter_info.get('company', 'Top Company')
    position = recruiter_info.get('position', 'Senior Engineer')
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Recruiter Interest Detected</title>
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>Recruiter Interest</h1>
            <p class="subtitle">Your work is getting noticed</p>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>Great news! A recruiter from a top-tier company has been actively engaging with your content.</p>
            </div>
            
            <div class="success-box">
              <strong>Company:</strong> {company}<br>
              <strong>Position:</strong> {position}<br>
              <strong>Status:</strong> Active Interest
            </div>
            
            <div class="email-section">
              <h2>What This Means</h2>
              <ul class="feature-list">
                <li>Your technical content is impressing industry professionals</li>
                <li>Companies are actively viewing your portfolio and GitHub</li>
                <li>This is a perfect opportunity to expand your network</li>
              </ul>
            </div>
            
            <div class="success-box">
              <strong>Recommended Next Steps:</strong><br>
              <ul style="margin: 12px 0 0 0;">
                <li>Update your LinkedIn profile with recent accomplishments</li>
                <li>Refresh your portfolio with latest projects</li>
                <li>Ensure your GitHub is up-to-date and well-documented</li>
                <li>Consider reaching out to expand your network</li>
              </ul>
            </div>
            
            <div class="email-section">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/resume.html" class="cta-button">View Your Resume</a>
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer & Full Stack Developer</p>
            <div class="footer-links">
              <a href="https://linkedin.com/in/victor-kipruto-rop">LinkedIn</a>
              <a href="https://github.com/kipruto45">GitHub</a>
              <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="{unsubscribe_url}">Unsubscribe</a> • <a href="#">Manage Alerts</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 10: Personalized Recommendations
def template_recommended_reads(name: str, email: str, reading_history: list, recommended_posts: list) -> str:
    """Personalized recommendations"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    
    recommendations_html = ""
    for i, post in enumerate(recommended_posts[:5], 1):
        title = post.get('title', 'Untitled')
        excerpt = post.get('excerpt', '')
        slug = post.get('slug', post.get('id', 'post'))
        relevance = post.get('relevance', '85%')
        
        recommendations_html += f"""
        <div class="email-section" style="border: 2px solid #e9ecef; padding: 18px; border-radius: 10px; margin-bottom: 14px; background: #f8f9fa;">
          <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
              <h3 style="margin: 0 0 8px 0; color: #2d3748; font-size: 16px; font-weight: 700;">{i}. {title}</h3>
              <p style="color: #718096; font-size: 13px; margin: 8px 0; line-height: 1.6;">{excerpt}</p>
              <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                <span style="color: #667eea; font-weight: 700; font-size: 12px;">Match: {relevance}</span>
                <a href="https://victor-kipruto-rop.github.io/victor-resum-web/post.html?id={slug}" class="secondary-button" style="font-size: 12px; padding: 8px 14px;">Read →</a>
              </div>
            </div>
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
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>Recommended For You</h1>
            <p class="subtitle">Personalized based on your reading habits</p>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>Based on the articles you've been reading, I've curated a list of posts I think you'll absolutely love:</p>
            </div>
            
            {recommendations_html}
            
            <div class="success-box">
              <strong>How It Works:</strong> I analyze your reading history to recommend articles that match your interests and expertise level. The higher the match percentage, the more likely you'll find it valuable!
            </div>
            
            <div class="email-section">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html" class="cta-button">Explore All Articles</a>
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer & Full Stack Developer</p>
            <div class="footer-links">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
              <a href="https://github.com/kipruto45">GitHub</a>
              <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="{unsubscribe_url}">Unsubscribe</a> • <a href="#">Preferences</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 11: Generic Notification
def template_notification(name: str, email: str, title: str, message: str, icon: str = "🔔", action_text: str = "Learn More", action_url: str = None) -> str:
    """Generic notification template"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    button_html = f'<a href="{action_url}" class="cta-button">{action_text} →</a>' if action_url else ""
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{title}</title>
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>{title}</h1>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>{message}</p>
              {button_html}
            </div>
            
            <div class="success-box">
              <strong>Need help?</strong> Reply to this email or visit my <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">portfolio</a>.
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer & Full Stack Developer</p>
            <div class="footer-links">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
              <a href="https://github.com/kipruto45">GitHub</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="{unsubscribe_url}">Unsubscribe</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 12: Dashboard Alert
def template_dashboard_alert(name: str, email: str, alert_title: str, metrics: dict, recommendation: str) -> str:
    """Dashboard alert for metrics"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    
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
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>{alert_title}</h1>
            <p class="subtitle">Your dashboard metrics update</p>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>Here's a snapshot of your dashboard metrics:</p>
            </div>
            
            <div class="content-grid">
              {metrics_html}
            </div>
            
            <div class="success-box">
              <strong>Recommendation:</strong> {recommendation}
            </div>
            
            <div class="email-section">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/dashboard/hub.html" class="cta-button">View Full Dashboard</a>
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Dashboard Analytics</p>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="#">Manage Alerts</a> • <a href="{unsubscribe_url}">Unsubscribe</a>
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# Template 13: Engagement Summary
def template_engagement_summary(name: str, email: str, period: str, engagement_stats: dict) -> str:
    """Reader engagement summary"""
    token = generate_unsubscribe_token(email)
    unsubscribe_url = f"https://victor-kipruto-rop.github.io/victor-resum-web/unsubscribe.html?token={token}&email={urllib.parse.quote(email)}"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Reader Engagement Summary</title>
      <style>{get_base_styles()}</style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="email-container">
          <div class="email-header">
            <h1>Engagement Summary</h1>
            <p class="subtitle">How readers engaged this {period}</p>
          </div>
          
          <div class="email-content">
            <div class="email-section">
              <p>Hi {name},</p>
              <p>Here's a detailed breakdown of how my readers engaged with content this {period}:</p>
            </div>
            
            <div class="content-grid">
              <div class="stat-box">
                <div class="stat-label">Total Pageviews</div>
                <span class="stat-number">{engagement_stats.get('pageviews', 0):,}</span>
              </div>
              <div class="stat-box">
                <div class="stat-label">Unique Visitors</div>
                <span class="stat-number">{engagement_stats.get('unique_visitors', 0):,}</span>
              </div>
              <div class="stat-box">
                <div class="stat-label">Avg Duration</div>
                <span class="stat-number">{engagement_stats.get('avg_session', '0')}s</span>
              </div>
              <div class="stat-box">
                <div class="stat-label">Return Rate</div>
                <span class="stat-number">{engagement_stats.get('return_rate', '0')}%</span>
              </div>
            </div>
            
            <div class="email-section">
              <h2>Top Traffic Sources</h2>
              <ol>
                <li><strong>{engagement_stats.get('source_1', 'Organic Search')}</strong> - {engagement_stats.get('source_1_pct', '0')}%</li>
                <li><strong>{engagement_stats.get('source_2', 'Direct')}</strong> - {engagement_stats.get('source_2_pct', '0')}%</li>
                <li><strong>{engagement_stats.get('source_3', 'Social Media')}</strong> - {engagement_stats.get('source_3_pct', '0')}%</li>
              </ol>
            </div>
            
            <div class="success-box">
              <strong>Key Insight:</strong> Your readers are most engaged with {engagement_stats.get('top_content_type', 'technical tutorials')}, indicating strong interest in deep, practical content.
            </div>
            
            <div class="email-section">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/dashboard/hub.html" class="cta-button">View Detailed Analytics</a>
            </div>
          </div>
          
          <div class="email-footer">
            <p><strong>Victor Kipruto Rop</strong><br>Data Engineer & Full Stack Developer</p>
            <div class="footer-links">
              <a href="https://victor-kipruto-rop.github.io/victor-resum-web/">Portfolio</a>
              <a href="https://github.com/kipruto45">GitHub</a>
              <a href="https://twitter.com/Victor_Kipruto">Twitter</a>
            </div>
            <p class="unsubscribe-notice">
              © 2024 Victor Kipruto. All rights reserved.<br>
              <a href="{unsubscribe_url}">Unsubscribe</a> • <a href="#">Preferences</a>
            </p>
          </div>
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
    'trending_content': template_trending_content,
    'activity_recap': template_activity_recap,
    'subscriber_milestone': template_subscriber_milestone,
    'viral_alert': template_viral_alert,
    'event_announcement': template_event_announcement,
    'recruiter_alert': template_recruiter_alert,
    'recommended_reads': template_recommended_reads,
    'notification': template_notification,
    'dashboard_alert': template_dashboard_alert,
    'engagement_summary': template_engagement_summary,
}

def get_template(template_type: str):
    """Get a template by type"""
    return TEMPLATES.get(template_type)
