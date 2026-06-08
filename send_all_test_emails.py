#!/usr/bin/env python3
"""
Send all 13 test emails to the specified recipient
Uses Resend API if configured, otherwise saves to test files
"""

import os
import json
import sys
import requests
from datetime import datetime
from pathlib import Path

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'python'))

from email_templates_modern import TEMPLATES

# Configuration
RECIPIENT_EMAIL = "kiprutovictor39@gmail.com"
RECIPIENT_NAME = "Victor Kipruto"
TWITTER_HANDLE = "VictorKipr10418"
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'onboarding@resend.dev')
RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')

# Test data for each template
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
        'celebration_message': '1,000 incredible subscribers strong!',
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

def send_via_resend(subject: str, html: str, to_email: str) -> dict:
    """Send email via Resend API"""
    if not RESEND_API_KEY:
        return {'success': False, 'error': 'Resend API key not configured'}
    
    try:
        response = requests.post(
            'https://api.resend.com/emails',
            headers={'Authorization': f'Bearer {RESEND_API_KEY}'},
            json={
                'from': SENDER_EMAIL,
                'to': to_email,
                'subject': subject,
                'html': html,
                'reply_to': 'kiprutovictor39@gmail.com'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return {'success': True, 'message_id': data.get('id')}
        else:
            return {'success': False, 'error': f'API Error: {response.status_code}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def save_test_email(template_name: str, subject: str, html: str) -> str:
    """Save email to test file"""
    os.makedirs('data/test_emails_sent', exist_ok=True)
    filename = f'data/test_emails_sent/{template_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    
    # Prepend subject to HTML for reference
    full_html = f"""<!--
    SUBJECT: {subject}
    TO: {RECIPIENT_EMAIL}
    SENT: {datetime.now().isoformat()}
    -->
    {html}"""
    
    with open(filename, 'w') as f:
        f.write(full_html)
    return filename

def send_all_emails():
    """Send all 13 test emails"""
    print("=" * 80)
    print("  SEND ALL TEST EMAILS")
    print("=" * 80)
    print(f"\nRecipient: {RECIPIENT_NAME} <{RECIPIENT_EMAIL}>")
    print(f"Twitter/X: @{TWITTER_HANDLE}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Status: {'✓ Configured' if RESEND_API_KEY else '⚠ Not configured (will save to files)'}")
    print("\n" + "=" * 80)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'recipient': RECIPIENT_EMAIL,
        'api_available': bool(RESEND_API_KEY),
        'emails_sent': [],
        'emails_failed': [],
        'summary': {}
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
            # Get template function
            template_func = TEMPLATES.get(template_name)
            if not template_func:
                raise ValueError(f"Template not found")
            
            # Get test data
            test_kwargs = TEST_DATA.get(template_name, {})
            subject = test_kwargs.pop('subject', f'Test: {template_name}')
            
            # Generate HTML
            html = template_func(**test_kwargs)
            
            if not html or len(html) < 500:
                raise ValueError("Invalid HTML generated")
            
            # Try to send via Resend
            if RESEND_API_KEY:
                result = send_via_resend(subject, html, RECIPIENT_EMAIL)
                if result['success']:
                    print(f"✅ SENT via Resend API")
                    print(f"   Message ID: {result.get('message_id')}")
                    results['emails_sent'].append({
                        'template': template_name,
                        'subject': subject,
                        'method': 'resend_api',
                        'status': 'sent',
                        'message_id': result.get('message_id')
                    })
                else:
                    # Fallback to saving file
                    saved_file = save_test_email(template_name, subject, html)
                    print(f"⚠ Resend API failed, saved to file")
                    print(f"   File: {saved_file}")
                    results['emails_failed'].append({
                        'template': template_name,
                        'subject': subject,
                        'method': 'file_save',
                        'reason': result.get('error'),
                        'file': saved_file
                    })
            else:
                # Save to file
                saved_file = save_test_email(template_name, subject, html)
                print(f"📄 Saved to file (API not configured)")
                print(f"   File: {saved_file}")
                results['emails_sent'].append({
                    'template': template_name,
                    'subject': subject,
                    'method': 'file_save',
                    'status': 'saved',
                    'file': saved_file
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
    
    print(f"\n✅ Successful: {sent}/{total}")
    print(f"❌ Failed: {failed}/{total}")
    
    if RESEND_API_KEY:
        resend_sent = sum(1 for e in results['emails_sent'] if e.get('method') == 'resend_api')
        file_saved = sum(1 for e in results['emails_sent'] if e.get('method') == 'file_save')
        print(f"   - Via Resend API: {resend_sent}")
        print(f"   - Saved to Files: {file_saved}")
    
    # Save results
    results['summary'] = {
        'total_sent': sent,
        'total_failed': failed,
        'recipient_email': RECIPIENT_EMAIL,
        'recipient_name': RECIPIENT_NAME,
        'twitter_handle': TWITTER_HANDLE
    }
    
    results_file = f'data/test_emails_sent/send_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    os.makedirs('data/test_emails_sent', exist_ok=True)
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Results saved to: {results_file}")
    print(f"\n📧 Test emails location: data/test_emails_sent/")
    
    print("\n" + "=" * 80)
    print("  NEXT STEPS")
    print("=" * 80)
    print(f"\n1. Check your email: {RECIPIENT_EMAIL}")
    if not RESEND_API_KEY:
        print(f"2. View saved emails: data/test_emails_sent/")
        print(f"3. Set RESEND_API_KEY env var to send actual emails")
    else:
        print(f"2. Verify all emails were received")
    print(f"3. Check design consistency and social links (@{TWITTER_HANDLE})")
    print(f"4. Test on mobile devices")
    
    return failed == 0

if __name__ == "__main__":
    success = send_all_emails()
    exit(0 if success else 1)
