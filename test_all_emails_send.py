#!/usr/bin/env python3
"""
Test script to generate and send all 13 email templates
Email: kiprutovictor39@gmail.com
Twitter/X: VictorKipr10418
"""

import json
import os
from datetime import datetime
from scripts.python.email_templates_modern import TEMPLATES

# Configuration
RECIPIENT_EMAIL = "kiprutovictor39@gmail.com"
RECIPIENT_NAME = "Victor Kipruto"
TWITTER_HANDLE = "VictorKipr10418"

# Test data for each template
TEST_DATA = {
    'welcome': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
    },
    'new_blog_post': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'post_title': 'Building Scalable Data Pipelines with Apache Airflow',
        'post_excerpt': 'Learn how to design and implement production-grade data pipelines using Apache Airflow. We\'ll cover DAGs, operators, sensors, and real-world optimization techniques.',
        'post_slug': 'airflow-data-pipelines',
        'read_time': 12,
        'image_url': 'https://victor-kipruto-rop.github.io/victor-resum-web/assets/images/data-engineering.jpg'
    },
    'weekly_digest': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'posts': [
            {
                'title': 'Cloud Infrastructure Best Practices',
                'excerpt': 'Essential patterns for designing resilient cloud systems',
                'readTime': 10,
                'id': 'cloud-infrastructure',
                'slug': 'cloud-infrastructure'
            },
            {
                'title': 'Python Performance Optimization',
                'excerpt': 'Advanced techniques to optimize Python applications',
                'readTime': 15,
                'id': 'python-performance',
                'slug': 'python-performance'
            },
            {
                'title': 'Docker and Kubernetes Deep Dive',
                'excerpt': 'Containerization strategies for modern applications',
                'readTime': 18,
                'id': 'docker-kubernetes',
                'slug': 'docker-kubernetes'
            }
        ]
    },
    'trending_content': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'trending_posts': [
            {
                'title': 'Building Real-Time Analytics Platforms',
                'views': 4250,
                'growth': '+85%',
                'slug': 'realtime-analytics',
                'id': 'realtime-analytics'
            },
            {
                'title': 'Microservices Architecture Guide',
                'views': 3820,
                'growth': '+72%',
                'slug': 'microservices',
                'id': 'microservices'
            },
            {
                'title': 'Mastering SQL Query Optimization',
                'views': 3150,
                'growth': '+65%',
                'slug': 'sql-optimization',
                'id': 'sql-optimization'
            }
        ],
        'top_post_stats': {
            'title': 'Building Real-Time Analytics Platforms',
            'views': 4250,
            'share_count': 342
        }
    },
    'activity_recap': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'month': 'June 2026',
        'stats': {
            'total_views': 12450,
            'new_posts': 4,
            'new_subscribers': 87,
            'avg_read_time': 11,
            'top_post_1': 'Building Real-Time Analytics Platforms',
            'top_post_1_views': 4250,
            'top_post_2': 'Cloud Infrastructure Best Practices',
            'top_post_2_views': 3820,
            'top_post_3': 'Docker and Kubernetes Deep Dive',
            'top_post_3_views': 3150,
            'insight': 'Your readers show strongest engagement with infrastructure and performance optimization content!'
        }
    },
    'subscriber_milestone': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'milestone': 1000,
        'celebration_message': 'We\'ve reached an incredible 1,000 subscribers! This is a testament to the quality of technical content that resonates with developers worldwide. Thank you for being part of this journey!'
    },
    'viral_alert': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'post_title': 'Building Real-Time Analytics Platforms',
        'current_views': 4250,
        'viral_threshold': 1000,
        'growth_rate': '+85% in 48 hours'
    },
    'event_announcement': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'event_title': 'Advanced Data Engineering Masterclass',
        'event_date': 'July 15, 2026',
        'event_description': 'Join me for an in-depth exploration of modern data engineering practices. We\'ll cover data pipeline architecture, distributed systems, and production deployment strategies.',
        'event_url': 'https://victor-kipruto-rop.github.io/victor-resum-web/'
    },
    'recruiter_alert': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'recruiter_info': {
            'company': 'Tech Innovation Labs',
            'position': 'Senior Data Engineer'
        }
    },
    'recommended_reads': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'reading_history': ['cloud-infrastructure', 'python-performance', 'docker-kubernetes'],
        'recommended_posts': [
            {
                'title': 'Advanced Distributed Systems Design',
                'excerpt': 'Deep dive into consensus algorithms and fault tolerance',
                'slug': 'distributed-systems',
                'id': 'distributed-systems',
                'relevance': '95%'
            },
            {
                'title': 'Production Kubernetes Patterns',
                'excerpt': 'Battle-tested patterns for production Kubernetes deployments',
                'slug': 'k8s-patterns',
                'id': 'k8s-patterns',
                'relevance': '92%'
            },
            {
                'title': 'Event-Driven Architecture Guide',
                'excerpt': 'Building scalable systems with event streaming',
                'slug': 'event-driven',
                'id': 'event-driven',
                'relevance': '88%'
            }
        ]
    },
    'notification': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'title': 'New Technical Resource Available',
        'message': 'I\'ve just published a comprehensive guide on modern data engineering practices. This resource covers architecture patterns, tools, and real-world implementation strategies.',
        'action_text': 'Read the Guide',
        'action_url': 'https://victor-kipruto-rop.github.io/victor-resum-web/blog.html'
    },
    'dashboard_alert': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'alert_title': 'Weekly Performance Summary',
        'metrics': {
            'Pageviews': '2,450',
            'Unique Visitors': '890',
            'Avg Session Duration': '4m 32s',
            'Bounce Rate': '32%'
        },
        'recommendation': 'Your content on data engineering continues to drive strong engagement. Consider creating more deep-dives on distributed systems.'
    },
    'engagement_summary': {
        'name': RECIPIENT_NAME,
        'email': RECIPIENT_EMAIL,
        'period': 'June 2026',
        'engagement_stats': {
            'pageviews': 12450,
            'unique_visitors': 3420,
            'avg_session': '280',
            'return_rate': '42',
            'source_1': 'Organic Search',
            'source_1_pct': '55',
            'source_2': 'Direct',
            'source_2_pct': '28',
            'source_3': 'Social Media',
            'source_3_pct': '17',
            'top_content_type': 'infrastructure and optimization content'
        }
    }
}

def save_test_email(template_name: str, html: str) -> str:
    """Save email HTML to file for testing"""
    os.makedirs('data/test_emails_all', exist_ok=True)
    filename = f'data/test_emails_all/{template_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    with open(filename, 'w') as f:
        f.write(html)
    return filename

def test_all_templates():
    """Test all 13 email templates"""
    print("=" * 80)
    print("  COMPREHENSIVE EMAIL TEMPLATE TEST")
    print("=" * 80)
    print(f"\nTest Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Recipient: {RECIPIENT_NAME} <{RECIPIENT_EMAIL}>")
    print(f"Twitter/X: @{TWITTER_HANDLE}")
    print("\n" + "=" * 80)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'recipient': RECIPIENT_EMAIL,
        'templates_tested': [],
        'success_count': 0,
        'failed_count': 0
    }
    
    template_names = [
        'welcome',
        'new_blog_post',
        'weekly_digest',
        'trending_content',
        'activity_recap',
        'subscriber_milestone',
        'viral_alert',
        'event_announcement',
        'recruiter_alert',
        'recommended_reads',
        'notification',
        'dashboard_alert',
        'engagement_summary'
    ]
    
    for i, template_name in enumerate(template_names, 1):
        print(f"\n[{i}/13] Testing {template_name.upper()}")
        print("-" * 80)
        
        try:
            # Get template function
            template_func = TEMPLATES.get(template_name)
            if not template_func:
                raise ValueError(f"Template '{template_name}' not found")
            
            # Get test data
            test_kwargs = TEST_DATA.get(template_name)
            if not test_kwargs:
                raise ValueError(f"No test data for template '{template_name}'")
            
            # Generate email HTML
            html = template_func(**test_kwargs)
            
            # Validate HTML
            if not html or len(html) < 500:
                raise ValueError("Generated HTML is too short")
            
            if '#c8401a' not in html:
                raise ValueError("Modern design color (#c8401a) not found in template")
            
            if 'DM Serif Display' not in html and 'font-family' not in html:
                raise ValueError("Google Fonts not detected")
            
            # Save to file
            saved_file = save_test_email(template_name, html)
            
            # Calculate size
            html_size = len(html.encode('utf-8')) / 1024
            
            # Store result
            results['templates_tested'].append({
                'name': template_name,
                'status': 'SUCCESS',
                'file': saved_file,
                'size_kb': round(html_size, 2),
                'has_modern_design': True
            })
            results['success_count'] += 1
            
            print(f"✅ SUCCESS")
            print(f"   File: {saved_file}")
            print(f"   Size: {html_size:.2f} KB")
            print(f"   Modern Design: ✓ Verified")
            
        except Exception as e:
            print(f"❌ FAILED - {str(e)}")
            results['templates_tested'].append({
                'name': template_name,
                'status': 'FAILED',
                'error': str(e)
            })
            results['failed_count'] += 1
    
    # Save results summary
    print("\n" + "=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    print(f"\n✅ Successful: {results['success_count']}/13")
    print(f"❌ Failed: {results['failed_count']}/13")
    
    results_file = f'data/test_emails_all/test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    os.makedirs('data/test_emails_all', exist_ok=True)
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Results saved to: {results_file}")
    print(f"\n📧 Test emails saved to: data/test_emails_all/")
    
    print("\n" + "=" * 80)
    print("  NEXT STEPS")
    print("=" * 80)
    print(f"\n1. Open emails in: data/test_emails_all/")
    print(f"2. Check design consistency across all templates")
    print(f"3. Verify social links display correctly with @{TWITTER_HANDLE}")
    print(f"4. Test responsive design on mobile devices")
    print(f"\n📧 Email address: {RECIPIENT_EMAIL}")
    print(f"🐦 Twitter/X: @{TWITTER_HANDLE}")
    
    return results['success_count'] == 13

if __name__ == "__main__":
    success = test_all_templates()
    exit(0 if success else 1)
