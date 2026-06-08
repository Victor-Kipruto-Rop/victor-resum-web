#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'python'))

from email_templates_modern import TEMPLATES
from notify_email import send_email_notification
from email_notifier import EmailNotifier

def test_all_emails(target_email):
    load_dotenv()
    print(f"🚀 Starting test of all email templates to: {target_email}")
    
    name = "Victor"
    
    # Sample data
    sample_posts = [
        {"title": "Scaling Data Pipelines", "excerpt": "How to handle millions of events...", "slug": "scaling-pipelines", "read_time": 8},
        {"title": "Modern ETL with Airflow", "excerpt": "Best practices for DAG design...", "slug": "airflow-etl", "read_time": 12}
    ]
    
    sample_stats = {
        "total_views": 1250,
        "unique_visitors": 450,
        "shares": 85,
        "growth": "+15%"
    }
    
    sample_metrics = {
        "Response Time": "450ms (High)",
        "Error Rate": "2.5% (Critical)",
        "CPU Usage": "88%"
    }
    
    recruiter_info = {
        "company": "Google",
        "role": "Data Engineer",
        "location": "Nairobi",
        "interest_score": "95%",
        "pages_viewed": 5
    }
    
    test_cases = [
        ('welcome', "Welcome to Victor's Blog", [name, target_email]),
        ('new_blog_post', "New Post: Scaling Data Pipelines", [name, target_email, "Scaling Data Pipelines", "How to handle millions of events with Python and Kafka.", "scaling-pipelines", 8, "https://victor-kipruto-rop.github.io/victor-resum-web/assets/images/1.jpeg"]),
        ('weekly_digest', "Your Weekly Tech Digest", [name, target_email, sample_posts]),
        ('trending_content', "Your post is trending!", [name, target_email, sample_posts, sample_posts[0]]),
        ('activity_recap', "Weekly Activity Recap", [name, target_email, "June 2026", sample_stats]),
        ('subscriber_milestone', "You've reached a milestone!", [name, target_email, 100]),
        ('viral_alert', "🔥 YOUR POST IS VIRAL", [name, target_email, "Scaling Data Pipelines", 5000, 1000, "10% per hour"]),
        ('event_announcement', "Live Webinar: Data Engineering Trends", [name, target_email, "Data Engineering Trends 2026", "June 15, 2026", "Join us for a deep dive into the future of data engineering.", "https://victor-kipruto-rop.github.io/victor-resum-web/"]),
        ('recruiter_alert', "💼 New Recruiter Activity", [name, target_email, recruiter_info]),
        ('recommended_reads', "Recommended for you", [name, target_email, sample_posts, sample_posts]),
        ('notification', "System Notification", [name, target_email, "Security Update", "Please review your account security settings.", "🔒", "Update Now", "https://victor-kipruto-rop.github.io/victor-resum-web/dashboard/login.html"]),
        ('dashboard_alert', "🚨 System Alert", [name, target_email, "High Latency Detected", sample_metrics, "Optimize database queries"]),
        ('engagement_summary', "Monthly Engagement Summary", [name, target_email, "May 2026", sample_stats])
    ]
    
    notifier = EmailNotifier()
    results = []
    
    for template_id, subject, args in test_cases:
        print(f"\n📧 Testing template: {template_id}")
        try:
            html_content = TEMPLATES[template_id](*args)
            
            # Try Resend first
            print("  Trying Resend API...")
            success = send_email_notification(subject, html_content, target_email)
            
            # Fallback to SMTP if Resend fails and SMTP is available
            if not success:
                print("  Resend failed. Trying SMTP fallback...")
                success = notifier.send_email([target_email], subject, html_content)
                
            results.append((template_id, success))
            if success:
                print(f"✅ Sent: {template_id}")
            else:
                print(f"❌ Failed all methods: {template_id}")
        except Exception as e:
            print(f"💥 Error rendering/sending {template_id}: {e}")
            results.append((template_id, False))
            
    print("\n" + "="*30)
    print("      TEST SUMMARY")
    print("="*30)
    for tid, status in results:
        mark = "✅" if status else "❌"
        print(f"{mark} {tid}")

if __name__ == "__main__":
    target = "kiprutovictor39@gmail.com"
    test_all_emails(target)
