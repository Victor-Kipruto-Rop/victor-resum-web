#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add scripts/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'python'))

from email_templates_modern import TEMPLATES

def generate_previews():
    output_dir = Path('email_previews')
    output_dir.mkdir(exist_ok=True)
    
    target_email = "kiprutovictor39@gmail.com"
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
        ('welcome', [name, target_email]),
        ('new_blog_post', [name, target_email, "Scaling Data Pipelines", "How to handle millions of events with Python and Kafka.", "scaling-pipelines", 8, "https://victor-kipruto-rop.github.io/victor-resum-web/assets/images/1.jpeg"]),
        ('weekly_digest', [name, target_email, sample_posts]),
        ('trending_content', [name, target_email, sample_posts, sample_posts[0]]),
        ('activity_recap', [name, target_email, "June 2026", sample_stats]),
        ('subscriber_milestone', [name, target_email, 100]),
        ('viral_alert', [name, target_email, "Scaling Data Pipelines", 5000, 1000, "10% per hour"]),
        ('event_announcement', [name, target_email, "Data Engineering Trends 2026", "June 15, 2026", "Join us for a deep dive into the future of data engineering.", "https://victor-kipruto-rop.github.io/victor-resum-web/"]),
        ('recruiter_alert', [name, target_email, recruiter_info]),
        ('recommended_reads', [name, target_email, sample_posts, sample_posts]),
        ('notification', [name, target_email, "Security Update", "Please review your account security settings.", "🔒", "Update Now", "https://victor-kipruto-rop.github.io/victor-resum-web/dashboard/login.html"]),
        ('dashboard_alert', [name, target_email, "High Latency Detected", sample_metrics, "Optimize database queries"]),
        ('engagement_summary', [name, target_email, "May 2026", sample_stats])
    ]
    
    print(f"📂 Generating {len(test_cases)} email previews in {output_dir}/")
    
    for template_id, args in test_cases:
        try:
            html_content = TEMPLATES[template_id](*args)
            file_path = output_dir / f"{template_id}.html"
            with open(file_path, 'w') as f:
                with open(file_path, 'w') as f:
                    f.write(html_content)
            print(f"✅ Generated: {template_id}.html")
        except Exception as e:
            print(f"💥 Error generating {template_id}: {e}")

if __name__ == "__main__":
    generate_previews()
