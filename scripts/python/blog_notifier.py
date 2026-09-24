#!/usr/bin/env python3
"""
Blog Event Notifier
Send emails to subscribers when blog posts are published or events occur
Supports event types: new_post, announcement, alert, milestone
Also automatically posts to social media platforms (Twitter, LinkedIn, Dev.to, Medium, Telegram)
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from email_template_manager import EmailTemplateManager

# Try to import social poster for automatic posting
try:
    from auto_social_poster import AutoSocialPoster
    SOCIAL_POSTING_AVAILABLE = True
except ImportError:
    SOCIAL_POSTING_AVAILABLE = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BlogEventNotifier:
    """Handle blog events and send notifications to subscribers"""
    
    def __init__(self):
        self.email_manager = EmailTemplateManager()
        self.posts_file = Path(__file__).parent.parent.parent / "blog" / "posts.json"
        self.subscribers_file = Path(__file__).parent.parent.parent / "subscribers.json"
        self.events_file = Path(__file__).parent.parent.parent / ".blog_events.json"
        
        # Initialize social poster if available
        self.social_poster = None
        if SOCIAL_POSTING_AVAILABLE:
            try:
                self.social_poster = AutoSocialPoster()
                logger.info("✅ Social media posting enabled")
            except Exception as e:
                logger.warning(f"⚠️  Social media posting not available: {e}")
        else:
            logger.info("ℹ️  Social media posting module not available")
        
        self.ensure_events_file()
    
    def ensure_events_file(self):
        """Create events tracking file if it doesn't exist"""
        if not self.events_file.exists():
            self.events_file.write_text(json.dumps({"notified": []}, indent=2))
    
    def load_posts(self) -> List[Dict]:
        """Load blog posts from JSON"""
        if not self.posts_file.exists():
            logger.warning(f"Posts file not found: {self.posts_file}")
            return []
        
        try:
            data = json.loads(self.posts_file.read_text())
            return data if isinstance(data, list) else []
        except Exception as e:
            logger.error(f"Error loading posts: {e}")
            return []
    
    def load_subscribers(self) -> List[Dict]:
        """Load subscribers from JSON"""
        if not self.subscribers_file.exists():
            return []
        
        try:
            data = json.loads(self.subscribers_file.read_text())
            return data.get("subscribers", [])
        except Exception as e:
            logger.error(f"Error loading subscribers: {e}")
            return []
    
    def load_notified_posts(self) -> List[str]:
        """Load list of posts already notified"""
        try:
            data = json.loads(self.events_file.read_text())
            return data.get("notified", [])
        except Exception as e:
            logger.warning(f"Error loading notified posts: {e}")
            return []
    
    def mark_post_notified(self, post_id: str, event_type: str = "new_post"):
        """Mark a post as having been notified"""
        try:
            data = json.loads(self.events_file.read_text())
            notified = data.get("notified", [])
            
            event_entry = {
                "post_id": post_id,
                "type": event_type,
                "notified_at": datetime.now().isoformat()
            }
            notified.append(event_entry)
            
            data["notified"] = notified
            self.events_file.write_text(json.dumps(data, indent=2))
            logger.info(f"Marked post {post_id} as notified")
        except Exception as e:
            logger.error(f"Error marking post as notified: {e}")
    
    def notify_new_post(self, post: Dict):
        """Send new post notification to all subscribers"""
        subscribers = self.load_subscribers()
        
        if not subscribers:
            logger.warning("No subscribers found")
            return {"success": False, "message": "No subscribers"}
        
        post_id = post.get("id", post.get("slug", "unknown"))
        post_title = post.get("title", "Untitled")
        post_slug = post.get("slug", "")
        post_excerpt = post.get("description", "Check out this new article")
        read_time = post.get("readTime", 5)
        image_url = post.get("image", None)  # Use absolute URL from posts.json
        
        logger.info(f"Sending notifications for: {post_title}")
        logger.info(f"  - Subscribers: {len(subscribers)}")
        logger.info(f"  - Image URL: {image_url}")
        
        success_count = 0
        failed_count = 0
        
        for subscriber in subscribers:
            email = subscriber.get("email")
            name = subscriber.get("name", "Subscriber")
            channels = subscriber.get("channels", [])
            
            # Only send if email channel is enabled
            if "email" not in channels:
                logger.debug(f"Skipping {email} - email channel not enabled")
                continue
            
            try:
                result = self.email_manager.send_blog_post_email(
                    name=name,
                    email=email,
                    post_title=post_title,
                    post_excerpt=post_excerpt,
                    post_slug=post_slug,
                    read_time=read_time,
                    image_url=image_url
                )
                
                if result:
                    success_count += 1
                    logger.info(f"✅ Email sent to {email}")
                else:
                    failed_count += 1
                    logger.warning(f"❌ Failed to send email to {email}")
            
            except Exception as e:
                failed_count += 1
                logger.error(f"Error sending email to {email}: {e}")
        
        # Post to social media platforms
        if self.social_poster:
            try:
                logger.info("📱 Publishing to social media platforms...")
                social_result = self.social_poster.post_to_all_platforms(post)
                logger.info(f"✨ Social media publishing complete")
                logger.info(f"   Platforms reached: {len([p for p, r in social_result.get('platforms', {}).items() if r.get('success')])}")
            except Exception as e:
                logger.warning(f"⚠️  Social media posting failed: {e}")
        
        # Mark as notified
        self.mark_post_notified(post_id, "new_post")
        
        result = {
            "success": success_count > 0,
            "sent": success_count,
            "failed": failed_count,
            "post": post_title,
            "social_posted": bool(self.social_poster)
        }
        
        logger.info(f"Notification complete: {result}")
        return result
    
    def notify_event(
        self,
        event_type: str,
        title: str,
        message: str,
        icon: str = "📢",
        action_url: str = None
    ):
        """Send generic event notification to all subscribers"""
        subscribers = self.load_subscribers()
        
        if not subscribers:
            logger.warning("No subscribers found")
            return {"success": False, "message": "No subscribers"}
        
        logger.info(f"Sending event notification: {title} ({event_type})")
        
        success_count = 0
        failed_count = 0
        
        for subscriber in subscribers:
            email = subscriber.get("email")
            name = subscriber.get("name", "Subscriber")
            channels = subscriber.get("channels", [])
            
            # Only send if email channel is enabled
            if "email" not in channels:
                continue
            
            try:
                result = self.email_manager.send_notification(
                    name=name,
                    email=email,
                    title=title,
                    message=message,
                    icon=icon,
                    action_text="Learn More" if action_url else None,
                    action_url=action_url
                )
                
                if result:
                    success_count += 1
                    logger.info(f"✅ Event email sent to {email}")
                else:
                    failed_count += 1
                    logger.warning(f"❌ Failed to send event email to {email}")
            
            except Exception as e:
                failed_count += 1
                logger.error(f"Error sending event email to {email}: {e}")
        
        return {
            "success": success_count > 0,
            "sent": success_count,
            "failed": failed_count,
            "event": title
        }
    
    def notify_milestone(self, title: str, description: str, metrics: Dict):
        """Send milestone announcement"""
        subscribers = self.load_subscribers()
        
        if not subscribers:
            return {"success": False, "message": "No subscribers"}
        
        logger.info(f"Sending milestone notification: {title}")
        
        success_count = 0
        
        for subscriber in subscribers:
            email = subscriber.get("email")
            name = subscriber.get("name", "Subscriber")
            channels = subscriber.get("channels", [])
            
            if "email" not in channels:
                continue
            
            try:
                result = self.email_manager.send_dashboard_alert(
                    name=name,
                    email=email,
                    alert_title=title,
                    metrics=metrics,
                    recommendation=description
                )
                
                if result:
                    success_count += 1
            
            except Exception as e:
                logger.error(f"Error sending milestone email to {email}: {e}")
        
        return {
            "success": success_count > 0,
            "sent": success_count,
            "milestone": title
        }
    
    def notify_new_posts_batch(self):
        """Check for new published posts and notify subscribers"""
        posts = self.load_posts()
        notified_posts = self.load_notified_posts()
        notified_ids = [entry.get("post_id") for entry in notified_posts]
        
        new_posts = [
            post for post in posts
            if post.get("id") not in notified_ids and post.get("status") == "published"
        ]
        
        if not new_posts:
            logger.info("No new posts to notify")
            return {"success": False, "message": "No new posts"}
        
        results = []
        for post in new_posts:
            result = self.notify_new_post(post)
            results.append(result)
        
        return {
            "success": True,
            "total_posts": len(new_posts),
            "results": results
        }


def main():
    """CLI interface for blog notifications"""
    import sys
    
    notifier = BlogEventNotifier()
    
    if len(sys.argv) < 2:
        print("Usage: python blog_notifier.py <command> [args]")
        print("Commands:")
        print("  notify-posts     Send notifications for all new posts")
        print("  notify-event     Send a custom event notification")
        print("  notify-milestone Send a milestone announcement")
        print("  list-posts       List all blog posts")
        print("  list-subs        List all subscribers")
        return
    
    command = sys.argv[1]
    
    if command == "notify-posts":
        result = notifier.notify_new_posts_batch()
        print(json.dumps(result, indent=2))
    
    elif command == "notify-event":
        if len(sys.argv) < 4:
            print("Usage: python blog_notifier.py notify-event <title> <message> [url]")
            return
        
        title = sys.argv[2]
        message = sys.argv[3]
        url = sys.argv[4] if len(sys.argv) > 4 else None
        
        result = notifier.notify_event(
            event_type="custom",
            title=title,
            message=message,
            action_url=url
        )
        print(json.dumps(result, indent=2))
    
    elif command == "notify-milestone":
        if len(sys.argv) < 4:
            print("Usage: python blog_notifier.py notify-milestone <title> <description>")
            return
        
        title = sys.argv[2]
        description = sys.argv[3]
        
        result = notifier.notify_milestone(
            title=title,
            description=description,
            metrics={"status": "achieved", "date": datetime.now().isoformat()}
        )
        print(json.dumps(result, indent=2))
    
    elif command == "list-posts":
        posts = notifier.load_posts()
        for post in posts:
            print(f"  📝 {post.get('title')} ({post.get('id')})")
    
    elif command == "list-subs":
        subs = notifier.load_subscribers()
        print(f"Total subscribers: {len(subs)}")
        for sub in subs:
            print(f"  📧 {sub.get('email')} - {sub.get('name')} ({', '.join(sub.get('channels', []))})")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
