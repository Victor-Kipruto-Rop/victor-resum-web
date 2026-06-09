#!/usr/bin/env python3
"""
Blog Subscription Service
Manages subscriber database and sends notifications for new blog posts.
Stores subscribers in JSON files and supports email notifications.
"""

import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Paths
BASE_DIR = Path(__file__).parent
SUBSCRIBERS_DIR = BASE_DIR / "subscribers"
EMAIL_FILE = SUBSCRIBERS_DIR / "email.json"
TELEGRAM_FILE = SUBSCRIBERS_DIR / "telegram.json"
RSS_FILE = SUBSCRIBERS_DIR / "rss.json"
STATS_FILE = SUBSCRIBERS_DIR / "stats.json"
SEGMENTS_FILE = SUBSCRIBERS_DIR / "segments.json"

# Ensure directories exist
SUBSCRIBERS_DIR.mkdir(parents=True, exist_ok=True)


class SubscriptionService:
    """Manages blog subscribers and notifications."""

    def __init__(self):
        self.email_db = self._load_db(EMAIL_FILE)
        self.telegram_db = self._load_db(TELEGRAM_FILE)
        self.rss_db = self._load_db(RSS_FILE)
        self.stats = self._load_db(STATS_FILE)
        self.segments = self._load_db(SEGMENTS_FILE)

    def _load_db(self, path: Path) -> dict:
        """Load a JSON database file."""
        if path.exists():
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"subscribers": [], "last_updated": datetime.now().isoformat()}

    def _save_db(self, path: Path, data: dict):
        """Save a JSON database file."""
        data["last_updated"] = datetime.now().isoformat()
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def _save_all(self):
        """Save all databases."""
        self._save_db(EMAIL_FILE, self.email_db)
        self._save_db(TELEGRAM_FILE, self.telegram_db)
        self._save_db(RSS_FILE, self.rss_db)
        self._save_db(STATS_FILE, self.stats)
        self._save_db(SEGMENTS_FILE, self.segments)

    # ── Email Subscriptions ──

    def subscribe_email(self, email: str, name: str = "", interests: List[str] = None) -> Dict:
        """Subscribe an email address."""
        # Check for duplicate
        for sub in self.email_db["subscribers"]:
            if sub["contact"] == email:
                if sub["status"] == "active":
                    return {"success": False, "message": "Email already subscribed", "subscriber_id": sub["id"]}
                else:
                    # Reactivate
                    sub["status"] = "active"
                    sub["subscribed_at"] = datetime.now().isoformat()
                    self._save_all()
                    return {"success": True, "message": "Subscription reactivated", "subscriber_id": sub["id"]}

        subscriber_id = f"sub_{uuid.uuid4().hex[:8]}"
        subscriber = {
            "id": subscriber_id,
            "contact": email,
            "name": name,
            "subscribed_at": datetime.now().isoformat(),
            "status": "active",
            "interests": interests or [],
            "engagement_level": "new",
            "preferences": {
                "digest_frequency": "weekly",
                "notifications": True
            },
            "metadata": {
                "source": "blog",
                "total_opens": 0,
                "total_clicks": 0
            }
        }
        self.email_db["subscribers"].append(subscriber)
        self._save_all()

        # Update stats
        self._update_stats("email_subscriptions", 1)

        return {"success": True, "message": "Successfully subscribed!", "subscriber_id": subscriber_id}

    def unsubscribe_email(self, email: str) -> Dict:
        """Unsubscribe an email address."""
        for sub in self.email_db["subscribers"]:
            if sub["contact"] == email:
                sub["status"] = "inactive"
                sub["unsubscribed_at"] = datetime.now().isoformat()
                self._save_all()
                return {"success": True, "message": "Successfully unsubscribed"}
        return {"success": False, "message": "Email not found"}

    def get_active_subscribers(self, channel: str = "email") -> List[Dict]:
        """Get all active subscribers for a channel."""
        if channel == "email":
            return [s for s in self.email_db["subscribers"] if s["status"] == "active"]
        elif channel == "telegram":
            return [s for s in self.telegram_db["subscribers"] if s["status"] == "active"]
        return []

    def get_subscriber_count(self, channel: str = "email") -> int:
        """Get count of active subscribers."""
        return len(self.get_active_subscribers(channel))

    # ── Telegram Subscriptions ──

    def subscribe_telegram(self, chat_id: str, username: str = "") -> Dict:
        """Subscribe a Telegram chat."""
        for sub in self.telegram_db["subscribers"]:
            if sub["contact"] == chat_id:
                if sub["status"] == "active":
                    return {"success": False, "message": "Already subscribed"}
                else:
                    sub["status"] = "active"
                    self._save_all()
                    return {"success": True, "message": "Reactivated"}

        subscriber = {
            "id": f"tg_{uuid.uuid4().hex[:8]}",
            "contact": chat_id,
            "name": username,
            "subscribed_at": datetime.now().isoformat(),
            "status": "active",
            "interests": [],
            "engagement_level": "new",
            "preferences": {"digest_frequency": "weekly"},
            "metadata": {"source": "telegram"}
        }
        self.telegram_db["subscribers"].append(subscriber)
        self._save_all()
        self._update_stats("telegram_subscriptions", 1)
        return {"success": True, "message": "Subscribed to Telegram updates"}

    # ── Notifications ──

    def send_new_post_notification(self, post_data: Dict) -> Dict:
        """Send notification to all active subscribers about a new post."""
        results = {"email": [], "telegram": [], "total_sent": 0}

        # Email notifications
        email_subscribers = self.get_active_subscribers("email")
        for sub in email_subscribers:
            try:
                result = self._send_email_notification(sub, post_data)
                results["email"].append({"subscriber": sub["contact"], "status": "sent"})
                results["total_sent"] += 1
            except Exception as e:
                results["email"].append({"subscriber": sub["contact"], "status": "failed", "error": str(e)})

        # Telegram notifications
        telegram_subscribers = self.get_active_subscribers("telegram")
        for sub in telegram_subscribers:
            try:
                result = self._send_telegram_notification(sub, post_data)
                results["telegram"].append({"subscriber": sub["contact"], "status": "sent"})
                results["total_sent"] += 1
            except Exception as e:
                results["telegram"].append({"subscriber": sub["contact"], "status": "failed", "error": str(e)})

        # Update stats
        self._update_stats("notifications_sent", results["total_sent"])
        self._update_stats("last_notification", datetime.now().isoformat())

        return results

    def _send_email_notification(self, subscriber: Dict, post_data: Dict) -> bool:
        """Send email notification to a subscriber."""
        # Try to use the email notifier if available
        try:
            sys.path.insert(0, str(BASE_DIR / "blog-ai"))
            from email_notifier import EmailNotifier
            notifier = EmailNotifier()
            notification_data = {
                "title": post_data.get("title", "New Blog Post"),
                "excerpt": post_data.get("excerpt", post_data.get("description", "")),
                "read_time": post_data.get("readTime", 10),
                "tags": post_data.get("tags", []),
                "url": post_data.get("url", f"https://victor-kipruto-rop.github.io/victor-resum-web/post.html?id={post_data.get('id', 'post')}"),
                "published_date": datetime.now().strftime("%B %d, %Y"),
                "author": "Victor Kipruto Rop"
            }
            notifier.send_new_post_notification(notification_data)
            return True
        except ImportError:
            # Fallback: log the notification
            print(f"  📧 Email notification to {subscriber['contact']}: {post_data.get('title', 'New Post')}")
            return True
        except Exception as e:
            print(f"  ❌ Email failed for {subscriber['contact']}: {e}")
            return False

    def _send_telegram_notification(self, subscriber: Dict, post_data: Dict) -> bool:
        """Send Telegram notification to a subscriber."""
        try:
            sys.path.insert(0, str(BASE_DIR / "scripts" / "python"))
            from notify_telegram import send_telegram_notification
            message = f"""📚 *New Blog Post*

*{post_data.get('title', 'New Post')}*

_{post_data.get('excerpt', '')}_

⏱️ {post_data.get('readTime', 10)} min read
🔗 [Read More]({post_data.get('url', '')})"""
            send_telegram_notification(message)
            return True
        except ImportError:
            print(f"  📱 Telegram notification to {subscriber['contact']}: {post_data.get('title', 'New Post')}")
            return True
        except Exception as e:
            print(f"  ❌ Telegram failed for {subscriber['contact']}: {e}")
            return False

    # ── Stats ──

    def _update_stats(self, key: str, value):
        """Update statistics. For numeric keys, accumulate. For others, overwrite."""
        if "stats" not in self.stats:
            self.stats["stats"] = {}
        # Store timestamps and string values directly
        if isinstance(value, str):
            self.stats["stats"][key] = value
        elif key not in self.stats["stats"]:
            self.stats["stats"][key] = value
        elif isinstance(self.stats["stats"][key], (int, float)):
            self.stats["stats"][key] += value
        else:
            self.stats["stats"][key] = value
        self.stats["stats"]["last_updated"] = datetime.now().isoformat()
        self._save_db(STATS_FILE, self.stats)

    def get_stats(self) -> Dict:
        """Get subscription statistics."""
        return {
            "email_subscribers": self.get_subscriber_count("email"),
            "telegram_subscribers": self.get_subscriber_count("telegram"),
            "total_subscribers": self.get_subscriber_count("email") + self.get_subscriber_count("telegram"),
            "stats": self.stats.get("stats", {})
        }

    # ── CLI ──

    def list_subscribers(self, channel: str = "email"):
        """List all subscribers for a channel."""
        subscribers = self.get_active_subscribers(channel)
        print(f"\n{'='*60}")
        print(f"  {channel.upper()} Subscribers ({len(subscribers)} active)")
        print(f"{'='*60}")
        for sub in subscribers:
            print(f"  {sub['id']} | {sub['contact']} | {sub.get('name', 'N/A')} | {sub['status']}")
        print()


def main():
    """CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(description="Blog Subscription Service")
    parser.add_argument("action", choices=["subscribe", "unsubscribe", "list", "stats", "notify"],
                        help="Action to perform")
    parser.add_argument("--email", type=str, help="Email address")
    parser.add_argument("--name", type=str, default="", help="Subscriber name")
    parser.add_argument("--channel", type=str, default="email", help="Channel (email/telegram)")
    parser.add_argument("--post-title", type=str, help="Post title for notification")
    parser.add_argument("--post-url", type=str, help="Post URL for notification")

    args = parser.parse_args()
    service = SubscriptionService()

    if args.action == "subscribe":
        if not args.email:
            print("Error: --email required")
            sys.exit(1)
        result = service.subscribe_email(args.email, args.name)
        print(json.dumps(result, indent=2))

    elif args.action == "unsubscribe":
        if not args.email:
            print("Error: --email required")
            sys.exit(1)
        result = service.unsubscribe_email(args.email)
        print(json.dumps(result, indent=2))

    elif args.action == "list":
        service.list_subscribers(args.channel)

    elif args.action == "stats":
        stats = service.get_stats()
        print(json.dumps(stats, indent=2))

    elif args.action == "notify":
        post_data = {
            "title": args.post_title or "New Blog Post",
            "url": args.post_url or "https://victor-kipruto-rop.github.io/victor-resum-web/blog.html",
            "excerpt": "A new article has been published.",
            "readTime": 10,
            "tags": ["data-engineering"]
        }
        result = service.send_new_post_notification(post_data)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()