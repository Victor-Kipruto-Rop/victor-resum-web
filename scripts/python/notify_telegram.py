#!/usr/bin/env python3
"""
Helper script to send Telegram notifications from GitHub Actions
"""

import sys
import os
import json
from pathlib import Path
from telegram_notifier import TelegramNotifier

def main():
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: notify_telegram.py <event_type> [options]")
        sys.exit(1)
    
    event_type = sys.argv[1]
    
    notifier = TelegramNotifier()
    
    if not notifier.validate_credentials():
        print("⚠️  Telegram credentials not configured")
        return False
    
    # Handle different event types
    if event_type == "blog_published":
        # Load latest post from posts.json
        posts_file = Path('blog/posts.json')
        if posts_file.exists():
            with open(posts_file) as f:
                posts = json.load(f)
                if posts:
                    latest = posts[0]
                    seo_score = latest.get('seoScore', 70)
                    return notifier.send_blog_published(
                        latest['title'],
                        latest['slug'],
                        seo_score,
                        latest.get('category', 'General')
                    )
    
    elif event_type == "viral_detected":
        # Load viral analysis
        viral_file = Path('analytics/viral-analysis.json')
        if viral_file.exists():
            with open(viral_file) as f:
                data = json.load(f)
                viral_posts = data.get('viral_posts', [])
                if viral_posts:
                    post = viral_posts[0]
                    return notifier.send_viral_detected(
                        post['title'],
                        post['views'],
                        post.get('growth_indicators', {}).get('estimated_24h_rate', 2.0),
                        post.get('viral_score', 85)
                    )
    
    elif event_type == "recruiter_detected":
        # Load recruiter analysis
        recruiter_file = Path('analytics/recruiter-analysis.json')
        if recruiter_file.exists():
            with open(recruiter_file) as f:
                data = json.load(f)
                recruiters = data.get('recruiters_detected', [])
                if recruiters:
                    recruiter = recruiters[0]
                    return notifier.send_recruiter_detected(
                        recruiter['company'],
                        len(recruiter.get('indicators', [])),
                        recruiter['recruiter_score'],
                        600,  # example time spent
                        recruiter.get('returning', False)
                    )
    
    elif event_type == "github_actions_success":
        workflow = sys.argv[2] if len(sys.argv) > 2 else "Workflow"
        return notifier.send_github_actions_status(workflow, "success")
    
    elif event_type == "github_actions_failed":
        workflow = sys.argv[2] if len(sys.argv) > 2 else "Workflow"
        error = sys.argv[3] if len(sys.argv) > 3 else "Unknown error"
        return notifier.send_github_actions_status(workflow, "failure", error)
    
    return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
