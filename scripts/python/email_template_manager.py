#!/usr/bin/env python3
"""
Email Template Manager
Send beautiful HTML emails using pre-built templates
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

from email_templates import (
    template_welcome,
    template_new_blog_post,
    template_weekly_digest,
    template_notification,
    template_dashboard_alert,
    template_event_announcement,
)

try:
    from notify_email import send_email_notification
except ImportError:
    print("⚠️  notify_email module not available")
    send_email_notification = None

class EmailTemplateManager:
    """Manager for sending templated emails"""
    
    def __init__(self):
        self.send_email = send_email_notification
    
    def send_welcome_email(self, name: str, email: str) -> bool:
        """Send welcome email to new subscriber"""
        try:
            html_content = template_welcome(name, email)
            return self.send_email(
                subject="Welcome to Victor Kipruto's Blog! 🎉",
                body=html_content,
                to_email=email
            )
        except Exception as e:
            print(f"❌ Error sending welcome email: {e}")
            return False
    
    def send_blog_post_email(
        self,
        name: str,
        email: str,
        post_title: str,
        post_excerpt: str,
        post_slug: str,
        read_time: int,
        image_url: str = None
    ) -> bool:
        """Send new blog post notification with optional featured image"""
        try:
            html_content = template_new_blog_post(
                name, post_title, post_excerpt, post_slug, read_time, image_url
            )
            return self.send_email(
                subject=f"New Post: {post_title}",
                body=html_content,
                to_email=email
            )
        except Exception as e:
            print(f"❌ Error sending blog post email: {e}")
            return False
    
    def send_weekly_digest_email(
        self,
        name: str,
        email: str,
        posts: list
    ) -> bool:
        """Send weekly digest of blog posts"""
        try:
            html_content = template_weekly_digest(name, posts)
            return self.send_email(
                subject="This Week on Victor Kipruto's Blog",
                body=html_content,
                to_email=email
            )
        except Exception as e:
            print(f"❌ Error sending weekly digest: {e}")
            return False
    
    def send_notification(
        self,
        name: str,
        email: str,
        title: str,
        message: str,
        icon: str = "🔔",
        action_text: str = "Learn More",
        action_url: str = None
    ) -> bool:
        """Send generic notification"""
        try:
            html_content = template_notification(
                name, title, message, icon, action_text, action_url
            )
            return self.send_email(
                subject=title,
                body=html_content,
                to_email=email
            )
        except Exception as e:
            print(f"❌ Error sending notification: {e}")
            return False
    
    def send_dashboard_alert(
        self,
        name: str,
        email: str,
        alert_title: str,
        metrics: Dict,
        recommendation: str
    ) -> bool:
        """Send dashboard alert"""
        try:
            html_content = template_dashboard_alert(
                name, alert_title, metrics, recommendation
            )
            return self.send_email(
                subject=f"Dashboard Alert: {alert_title}",
                body=html_content,
                to_email=email
            )
        except Exception as e:
            print(f"❌ Error sending dashboard alert: {e}")
            return False
    
    def send_event_announcement(
        self,
        name: str,
        email: str,
        event_title: str,
        event_date: str,
        event_description: str,
        event_url: str = None
    ) -> bool:
        """Send event or project announcement"""
        try:
            html_content = template_event_announcement(
                name, event_title, event_date, event_description, event_url
            )
            return self.send_email(
                subject=f"Announcement: {event_title}",
                body=html_content,
                to_email=email
            )
        except Exception as e:
            print(f"❌ Error sending event announcement: {e}")
            return False


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Email Template Manager')
    parser.add_argument('template_type', help='Template type: welcome, blog_post, digest, notification, alert, event')
    parser.add_argument('--name', default='Subscriber', help='Recipient name')
    parser.add_argument('--email', required=True, help='Recipient email')
    parser.add_argument('--title', help='Email title')
    parser.add_argument('--message', help='Email message')
    
    args = parser.parse_args()
    
    if not send_email_notification:
        print("❌ Email sending not configured")
        return 1
    
    manager = EmailTemplateManager()
    
    if args.template_type == 'welcome':
        manager.send_welcome_email(args.name, args.email)
    elif args.template_type == 'notification':
        manager.send_notification(args.name, args.email, args.title or "Notification", args.message or "Check this out!")
    else:
        print(f"Unknown template type: {args.template_type}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
