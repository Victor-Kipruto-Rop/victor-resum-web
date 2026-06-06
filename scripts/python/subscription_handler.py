#!/usr/bin/env python3
"""
Subscription Handler - Manages email subscriptions and multi-channel notifications
Handles: Email subscriptions, Telegram notifications, Twitter notifications
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Setup path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config import config
    from notify_email import send_email_notification
    from notify_telegram import send_telegram_notification
    from distribute_twitter import post_tweet
    from email_template_manager import EmailTemplateManager
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure config.py and notification modules are in the same directory")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SubscriptionHandler:
    """Handle email subscriptions and send multi-channel notifications"""
    
    def __init__(self):
        self.config = config
        self.subscribers_file = Path(__file__).parent.parent.parent / "subscribers.json"
        self.email_manager = EmailTemplateManager()
        self.ensure_subscribers_file()
    
    def ensure_subscribers_file(self):
        """Create subscribers file if it doesn't exist"""
        if not self.subscribers_file.exists():
            self.subscribers_file.write_text(json.dumps({"subscribers": []}, indent=2))
            logger.info(f"Created subscribers file at {self.subscribers_file}")
    
    def add_subscriber(self, email: str, name: str, channels: List[str] = None) -> Dict:
        """
        Add a new subscriber
        
        Args:
            email: Email address
            name: Subscriber name
            channels: Notification channels (email, telegram, twitter)
        
        Returns:
            Dict with subscription result
        """
        if not channels:
            channels = ["email"]
        
        try:
            # Load existing subscribers
            data = json.loads(self.subscribers_file.read_text())
            subscribers = data.get("subscribers", [])
            
            # Check if already exists
            for sub in subscribers:
                if sub["email"].lower() == email.lower():
                    logger.info(f"Subscriber {email} already exists")
                    return {
                        "success": False,
                        "message": "Email already subscribed",
                        "code": "ALREADY_EXISTS"
                    }
            
            # Add new subscriber
            subscriber = {
                "email": email,
                "name": name,
                "channels": channels,
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            subscribers.append(subscriber)
            data["subscribers"] = subscribers
            
            # Save to file
            self.subscribers_file.write_text(json.dumps(data, indent=2))
            logger.info(f"Added subscriber: {email}")
            
            # Send confirmation email
            self.send_confirmation_email(email, name)
            
            return {
                "success": True,
                "message": "Successfully subscribed",
                "email": email,
                "channels": channels
            }
        
        except Exception as e:
            logger.error(f"Error adding subscriber: {e}")
            return {
                "success": False,
                "message": str(e),
                "code": "ERROR"
            }
    
    def send_confirmation_email(self, email: str, name: str):
        """Send confirmation email to new subscriber using modern template"""
        try:
            self.email_manager.send_welcome_email(name, email)
            logger.info(f"Welcome email sent to {email}")
        except Exception as e:
            logger.warning(f"Could not send welcome email: {e}")
    
    def notify_subscribers(self, title: str, message: str, url: str = None, channels: List[str] = None):
        """
        Send notification to all subscribers via selected channels
        
        Args:
            title: Notification title
            message: Notification message
            url: URL to include in notification
            channels: Channels to notify via (email, telegram, twitter)
        """
        if not channels:
            channels = ["email"]
        
        try:
            data = json.loads(self.subscribers_file.read_text())
            subscribers = data.get("subscribers", [])
            
            results = {
                "email": {"sent": 0, "failed": 0},
                "telegram": {"sent": 0, "failed": 0},
                "twitter": {"sent": 0, "failed": 0}
            }
            
            for subscriber in subscribers:
                if subscriber["status"] != "active":
                    continue
                
                sub_channels = subscriber.get("channels", ["email"])
                
                # Email notification
                if "email" in channels and "email" in sub_channels:
                    try:
                        self._send_email_notification_to_subscriber(
                            subscriber["email"],
                            subscriber["name"],
                            title,
                            message,
                            url
                        )
                        results["email"]["sent"] += 1
                    except Exception as e:
                        logger.error(f"Email notification failed for {subscriber['email']}: {e}")
                        results["email"]["failed"] += 1
                
                # Telegram notification
                if "telegram" in channels and "telegram" in sub_channels:
                    try:
                        self._send_telegram_notification(title, message, url)
                        results["telegram"]["sent"] += 1
                    except Exception as e:
                        logger.error(f"Telegram notification failed: {e}")
                        results["telegram"]["failed"] += 1
                
                # Twitter notification
                if "twitter" in channels and "twitter" in sub_channels:
                    try:
                        self._send_twitter_notification(title, message, url)
                        results["twitter"]["sent"] += 1
                    except Exception as e:
                        logger.error(f"Twitter notification failed: {e}")
                        results["twitter"]["failed"] += 1
            
            logger.info(f"Notification results: {results}")
            return results
        
        except Exception as e:
            logger.error(f"Error sending notifications: {e}")
            return {"error": str(e)}
    
    def _send_email_notification_to_subscriber(self, email: str, name: str, title: str, message: str, url: str = None):
        """Send email notification to subscriber using modern template"""
        try:
            self.email_manager.send_notification(
                name=name,
                email=email,
                title=title,
                message=message,
                action_text="Read More" if url else None,
                action_url=url
            )
        except Exception as e:
            logger.error(f"Error sending notification to {email}: {e}")
    
    def _send_telegram_notification(self, title: str, message: str, url: str = None):
        """Send Telegram notification"""
        text = f"📢 {title}\n\n{message}"
        if url:
            text += f"\n\n{url}"
        
        send_telegram_notification(text)
    
    def _send_twitter_notification(self, title: str, message: str, url: str = None):
        """Send Twitter notification"""
        tweet_text = f"{title}\n\n{message}"
        if url:
            tweet_text += f"\n\n{url}"
        
        # Truncate to Twitter's limit
        if len(tweet_text) > 280:
            tweet_text = tweet_text[:277] + "..."
        
        post_tweet(tweet_text)
    
    def get_subscribers_count(self) -> int:
        """Get total active subscribers"""
        try:
            data = json.loads(self.subscribers_file.read_text())
            subscribers = data.get("subscribers", [])
            return len([s for s in subscribers if s["status"] == "active"])
        except Exception as e:
            logger.error(f"Error getting subscriber count: {e}")
            return 0
    
    def get_subscribers(self) -> List[Dict]:
        """Get all active subscribers"""
        try:
            data = json.loads(self.subscribers_file.read_text())
            subscribers = data.get("subscribers", [])
            return [s for s in subscribers if s["status"] == "active"]
        except Exception as e:
            logger.error(f"Error getting subscribers: {e}")
            return []
    
    def unsubscribe(self, email: str) -> Dict:
        """Unsubscribe an email"""
        try:
            data = json.loads(self.subscribers_file.read_text())
            subscribers = data.get("subscribers", [])
            
            for sub in subscribers:
                if sub["email"].lower() == email.lower():
                    sub["status"] = "unsubscribed"
                    self.subscribers_file.write_text(json.dumps(data, indent=2))
                    logger.info(f"Unsubscribed: {email}")
                    return {"success": True, "message": "Unsubscribed successfully"}
            
            return {"success": False, "message": "Email not found"}
        except Exception as e:
            logger.error(f"Error unsubscribing: {e}")
            return {"success": False, "message": str(e)}


def main():
    """CLI interface for subscription handler"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Subscription Handler")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Subscribe command
    sub_subscribe = subparsers.add_parser("subscribe", help="Add subscriber")
    sub_subscribe.add_argument("email", help="Email address")
    sub_subscribe.add_argument("name", help="Subscriber name")
    sub_subscribe.add_argument("--channels", nargs="+", default=["email"], help="Notification channels")
    
    # Notify command
    sub_notify = subparsers.add_parser("notify", help="Send notifications")
    sub_notify.add_argument("title", help="Notification title")
    sub_notify.add_argument("message", help="Notification message")
    sub_notify.add_argument("--url", help="URL to include")
    sub_notify.add_argument("--channels", nargs="+", default=["email"], help="Channels to notify via")
    
    # List command
    subparsers.add_parser("list", help="List all subscribers")
    
    # Count command
    subparsers.add_parser("count", help="Get subscriber count")
    
    # Unsubscribe command
    sub_unsub = subparsers.add_parser("unsubscribe", help="Unsubscribe email")
    sub_unsub.add_argument("email", help="Email address")
    
    args = parser.parse_args()
    handler = SubscriptionHandler()
    
    if args.command == "subscribe":
        result = handler.add_subscriber(args.email, args.name, args.channels)
        print(json.dumps(result, indent=2))
    
    elif args.command == "notify":
        result = handler.notify_subscribers(args.title, args.message, args.url, args.channels)
        print(json.dumps(result, indent=2))
    
    elif args.command == "list":
        subscribers = handler.get_subscribers()
        print(json.dumps(subscribers, indent=2))
    
    elif args.command == "count":
        count = handler.get_subscribers_count()
        print(f"Active subscribers: {count}")
    
    elif args.command == "unsubscribe":
        result = handler.unsubscribe(args.email)
        print(json.dumps(result, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
