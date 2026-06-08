#!/usr/bin/env python3
"""
Send all test emails via SMTP (Gmail or another provider)
"""

import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'python'))

from email_templates_modern import TEMPLATES

# Configuration
RECIPIENT_EMAIL = "kiprutovictor39@gmail.com"
RECIPIENT_NAME = "Victor Kipruto"

# SMTP Configuration - Gmail or custom SMTP
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')  # Your email address
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', '')  # Your app password

# Test data
TEST_DATA = {
    'welcome': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'subject': 'Welcome to Victor Kipruto\'s Technical Blog!'
    },
    'new_blog_post': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'post_title': 'Building Scalable Data Pipelines with Apache Airflow',
        'post_excerpt': 'Learn how to design and implement production-grade data pipelines using Apache Airflow.',
        'post_slug': 'airflow-data-pipelines',
        'read_time': 12,
        'subject': 'New Article: Building Scalable Data Pipelines'
    },
    'weekly_digest': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'posts': [
            {'title': 'Cloud Infrastructure Best Practices', 'excerpt': 'Essential patterns', 'readTime': 10, 'id': 'cloud-1', 'slug': 'cloud-1'},
            {'title': 'Python Performance Optimization', 'excerpt': 'Advanced techniques', 'readTime': 15, 'id': 'python-1', 'slug': 'python-1'},
            {'title': 'Docker and Kubernetes Deep Dive', 'excerpt': 'Containerization strategies', 'readTime': 18, 'id': 'docker-1', 'slug': 'docker-1'}
        ],
        'subject': 'Your Weekly Digest'
    },
    'trending_content': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'trending_posts': [
            {'title': 'Real-Time Analytics', 'views': 4250, 'growth': '+85%', 'slug': 'analytics-1', 'id': 'analytics-1'},
            {'title': 'Microservices Guide', 'views': 3820, 'growth': '+72%', 'slug': 'micro-1', 'id': 'micro-1'},
            {'title': 'SQL Optimization', 'views': 3150, 'growth': '+65%', 'slug': 'sql-1', 'id': 'sql-1'}
        ],
        'top_post_stats': {'title': 'Real-Time Analytics', 'views': 4250, 'share_count': 342},
        'subject': 'Content Going Viral!'
    },
    'activity_recap': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'month': 'June 2026',
        'stats': {
            'total_views': 12450, 'new_posts': 4, 'new_subscribers': 87, 'avg_read_time': 11,
            'top_post_1': 'Real-Time Analytics', 'top_post_1_views': 4250,
            'top_post_2': 'Cloud Infrastructure', 'top_post_2_views': 3820,
            'top_post_3': 'Docker & K8s', 'top_post_3_views': 3150,
            'insight': 'Strong engagement with infrastructure content!'
        },
        'subject': 'June Activity Recap'
    },
    'subscriber_milestone': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'milestone': 1000,
        'celebration_message': '1,000 incredible subscribers!',
        'subject': 'We Hit 1,000 Subscribers!'
    },
    'viral_alert': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'post_title': 'Real-Time Analytics Platforms',
        'current_views': 4250,
        'viral_threshold': 1000,
        'growth_rate': '+85% in 48 hours',
        'subject': 'Your Post is Going Viral!'
    },
    'event_announcement': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'event_title': 'Advanced Data Engineering Masterclass',
        'event_date': 'July 15, 2026',
        'event_description': 'In-depth exploration of modern data engineering practices.',
        'event_url': 'https://victor-kipruto-rop.github.io/victor-resum-web/',
        'subject': 'New Masterclass: Advanced Data Engineering'
    },
    'recruiter_alert': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'recruiter_info': {'company': 'Tech Innovation Labs', 'position': 'Senior Data Engineer'},
        'subject': 'Recruiter Interest Detected'
    },
    'recommended_reads': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'reading_history': ['cloud-1', 'python-1', 'docker-1'],
        'recommended_posts': [
            {'title': 'Distributed Systems', 'excerpt': 'Deep dive into consensus', 'slug': 'dist-1', 'id': 'dist-1', 'relevance': '95%'},
            {'title': 'Kubernetes Patterns', 'excerpt': 'Battle-tested patterns', 'slug': 'k8s-1', 'id': 'k8s-1', 'relevance': '92%'},
            {'title': 'Event-Driven Architecture', 'excerpt': 'Event streaming', 'slug': 'event-1', 'id': 'event-1', 'relevance': '88%'}
        ],
        'subject': 'Recommended For You'
    },
    'notification': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'title': 'New Technical Resource',
        'message': 'Comprehensive guide on modern data engineering practices.',
        'action_text': 'Read the Guide',
        'action_url': 'https://victor-kipruto-rop.github.io/victor-resum-web/blog.html',
        'subject': 'New Technical Resource Available'
    },
    'dashboard_alert': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'alert_title': 'Weekly Performance Summary',
        'metrics': {'Pageviews': '2,450', 'Unique Visitors': '890', 'Avg Duration': '4m 32s', 'Bounce Rate': '32%'},
        'recommendation': 'Continue creating infrastructure content.',
        'subject': 'Weekly Performance Summary'
    },
    'engagement_summary': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'period': 'June 2026',
        'engagement_stats': {
            'pageviews': 12450, 'unique_visitors': 3420, 'avg_session': '280', 'return_rate': '42',
            'source_1': 'Organic Search', 'source_1_pct': '55',
            'source_2': 'Direct', 'source_2_pct': '28',
            'source_3': 'Social Media', 'source_3_pct': '17',
            'top_content_type': 'infrastructure and optimization content'
        },
        'subject': 'Engagement Summary - June 2026'
    }
}

def send_email_smtp(subject: str, html: str, to_email: str) -> dict:
    """Send email via SMTP"""
    
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return {
            'success': False,
            'error': 'SMTP credentials not configured. Set SENDER_EMAIL and SENDER_PASSWORD env vars'
        }
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Reply-To'] = 'kiprutovictor39@gmail.com'
        
        # Attach HTML
        msg.attach(MIMEText(html, 'html'))
        
        # Connect to SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return {'success': True, 'message': f'Email sent successfully'}
    
    except smtplib.SMTPAuthenticationError:
        return {
            'success': False,
            'error': 'SMTP authentication failed. Check SENDER_EMAIL and SENDER_PASSWORD'
        }
    except smtplib.SMTPException as e:
        return {'success': False, 'error': f'SMTP error: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def send_all_emails():
    """Send all test emails"""
    
    print("=" * 80)
    print("  SENDING ALL TEST EMAILS")
    print("=" * 80)
    print(f"\nRecipient: {RECIPIENT_NAME} <{RECIPIENT_EMAIL}>")
    print(f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"From: {SENDER_EMAIL if SENDER_EMAIL else 'NOT CONFIGURED'}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("\n" + "=" * 80)
        print("  ⚠️  SMTP CREDENTIALS NOT CONFIGURED")
        print("=" * 80)
        print("""
To send emails, set these environment variables:

For Gmail:
  export SENDER_EMAIL='your-email@gmail.com'
  export SENDER_PASSWORD='your-app-password'  # Not your regular password!
  
  Get an app password: https://support.google.com/accounts/answer/185833

For other SMTP servers:
  export SENDER_EMAIL='your-email@example.com'
  export SENDER_PASSWORD='your-password'
  export SMTP_SERVER='smtp.example.com'
  export SMTP_PORT='587'

Then run:
  SENDER_EMAIL='...' SENDER_PASSWORD='...' python3 send_all_emails_smtp.py
        """)
        return False
    
    print("\n" + "=" * 80)
    print("  SENDING EMAILS...")
    print("=" * 80)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'recipient': RECIPIENT_EMAIL,
        'sender': SENDER_EMAIL,
        'emails_sent': [],
        'emails_failed': []
    }
    
    template_names = [
        'welcome', 'new_blog_post', 'weekly_digest', 'trending_content',
        'activity_recap', 'subscriber_milestone', 'viral_alert', 'event_announcement',
        'recruiter_alert', 'recommended_reads', 'notification', 'dashboard_alert',
        'engagement_summary'
    ]
    
    for i, template_name in enumerate(template_names, 1):
        print(f"\n[{i}/13] {template_name.upper()}")
        print("-" * 80)
        
        try:
            template_func = TEMPLATES.get(template_name)
            if not template_func:
                raise ValueError(f"Template not found")
            
            test_kwargs = TEST_DATA.get(template_name, {})
            subject = test_kwargs.pop('subject', f'Test: {template_name}')
            
            html = template_func(**test_kwargs)
            
            if not html or len(html) < 500:
                raise ValueError("Invalid HTML generated")
            
            # Send via SMTP
            result = send_email_smtp(subject, html, RECIPIENT_EMAIL)
            
            if result['success']:
                print(f"✅ SENT")
                print(f"   Subject: {subject}")
                print(f"   To: {RECIPIENT_EMAIL}")
                results['emails_sent'].append({
                    'template': template_name,
                    'subject': subject,
                    'status': 'sent'
                })
            else:
                print(f"❌ FAILED: {result['error']}")
                results['emails_failed'].append({
                    'template': template_name,
                    'subject': subject,
                    'error': result['error']
                })
        
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            results['emails_failed'].append({
                'template': template_name,
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    sent = len(results['emails_sent'])
    failed = len(results['emails_failed'])
    total = sent + failed
    
    print(f"\n✅ Sent: {sent}/13")
    print(f"❌ Failed: {failed}/13")
    
    if sent > 0:
        print(f"\n🎉 All emails have been sent to {RECIPIENT_EMAIL}!")
        print(f"\nCheck your inbox for:")
        for email in results['emails_sent']:
            print(f"   • {email['subject']}")
    
    if failed > 0:
        print(f"\n⚠️  Some emails failed to send:")
        for email in results['emails_failed']:
            print(f"   • {email['template']}: {email['error']}")
    
    # Save results
    results_file = f'data/test_emails_sent/smtp_send_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    os.makedirs('data/test_emails_sent', exist_ok=True)
    import json
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Results saved to: {results_file}")
    
    return failed == 0

if __name__ == "__main__":
    success = send_all_emails()
    exit(0 if success else 1)
