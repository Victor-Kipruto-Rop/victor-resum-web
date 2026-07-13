#!/usr/bin/env python3
"""
Blog Post Scheduler
Automates blog post generation on a schedule
"""

import os
import sys
import json
import schedule
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List
import subprocess

from generate import BlogPostGenerator
from email_notifier import EmailNotifier

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('blog_scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent / "config.json"
SCHEDULE_STATE_FILE = Path(__file__).parent / ".schedule_state"

class BlogScheduler:
    def __init__(self):
        """Initialize the scheduler"""
        with open(CONFIG_PATH) as f:
            self.config = json.load(f)
        
        self.generator = BlogPostGenerator()
        self.email_notifier = EmailNotifier()
        self.schedule_state = self._load_schedule_state()

    def _load_schedule_state(self) -> dict:
        """Load schedule state from file"""
        if SCHEDULE_STATE_FILE.exists():
            with open(SCHEDULE_STATE_FILE) as f:
                return json.load(f)
        return {"last_generated": None, "posts_count": 0}

    def _save_schedule_state(self):
        """Save schedule state to file"""
        with open(SCHEDULE_STATE_FILE, 'w') as f:
            json.dump(self.schedule_state, f, indent=2)

    def generate_and_publish(self):
        """Generate a blog post and publish it"""
        logger.info("🚀 Starting scheduled blog post generation...")
        
        try:
            # Generate post
            title, content, metadata = self.generator.generate_post()
            md_file, meta_file = self.generator.save_post(title, content, metadata)
            
            # Format for assets/shared/posts.js
            post_entry = self.generator.format_for_posts_js(title, content, metadata)
            
            # Update schedule state
            self.schedule_state["last_generated"] = datetime.now().isoformat()
            self.schedule_state["posts_count"] += 1
            self._save_schedule_state()
            
            logger.info(f"✅ Post generated: {title}")
            
            # Notify subscribers
            try:
                self._notify_subscribers(title, post_entry, metadata)
            except Exception as e:
                logger.error(f"❌ Error sending notifications: {e}")
            
            # Auto-push to GitHub if enabled
            if self.config.get("github", {}).get("auto_push"):
                try:
                    self._push_to_github(title, md_file)
                except Exception as e:
                    logger.error(f"❌ Error pushing to GitHub: {e}")
            
            logger.info(f"✅ Scheduled generation complete. Total posts: {self.schedule_state['posts_count']}")
            
        except Exception as e:
            logger.error(f"❌ Error during scheduled generation: {e}")
            raise

    def _notify_subscribers(self, title: str, post_entry: dict, metadata: str):
        """Send notifications to email subscribers"""
        logger.info(f"📧 Sending notifications for: {title}")
        
        metadata_dict = json.loads(metadata)
        
        notification_data = {
            "title": title,
            "excerpt": metadata_dict.get("excerpt", ""),
            "read_time": metadata_dict.get("read_time", 10),
            "tags": metadata_dict.get("tags", []),
            "url": f"https://victorkirpruto.dev/post/?id={metadata_dict.get('id', title.lower().replace(' ', '-'))}",
            "published_date": datetime.now().strftime("%B %d, %Y"),
            "author": self.config["author"]["name"]
        }
        
        self.email_notifier.send_new_post_notification(notification_data)
        logger.info(f"✅ Notifications sent")

    def _push_to_github(self, title: str, md_file: str):
        """Auto-push to GitHub"""
        logger.info(f"📤 Pushing to GitHub...")
        
        try:
            # Run push script
            push_script = Path(__file__).parent / "push.sh"
            result = subprocess.run(
                ["bash", str(push_script), title, md_file],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Pushed to GitHub successfully")
            else:
                logger.error(f"❌ GitHub push failed: {result.stderr}")
        except Exception as e:
            logger.error(f"❌ Error running push script: {e}")

    def schedule_posts(self):
        """Schedule blog post generation"""
        blog_config = self.config.get("blog", {})
        publish_time = blog_config.get("publish_time", "09:00")
        publish_day = blog_config.get("publish_day", "monday")
        
        logger.info(f"📅 Scheduling posts for {publish_day} at {publish_time}")
        
        # Schedule based on day
        day_mapping = {
            'monday': schedule.every().monday,
            'tuesday': schedule.every().tuesday,
            'wednesday': schedule.every().wednesday,
            'thursday': schedule.every().thursday,
            'friday': schedule.every().friday,
            'saturday': schedule.every().saturday,
            'sunday': schedule.every().sunday
        }
        
        if publish_day.lower() in day_mapping:
            day_mapping[publish_day.lower()].at(publish_time).do(self.generate_and_publish)
            logger.info(f"✅ Scheduled! Posts will be generated every {publish_day} at {publish_time}")
        else:
            logger.error(f"❌ Invalid publish_day: {publish_day}")

    def run(self):
        """Run the scheduler"""
        logger.info("🎯 Blog Scheduler Started")
        logger.info(f"Author: {self.config['author']['name']}")
        logger.info(f"Blog: {self.config['blog']['title']}")
        
        self.schedule_posts()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("⛔ Scheduler stopped by user")
        except Exception as e:
            logger.error(f"❌ Scheduler error: {e}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Schedule blog post generation")
    parser.add_argument("--now", action="store_true", help="Generate post immediately")
    parser.add_argument("--test", action="store_true", help="Test notification system")
    
    args = parser.parse_args()
    
    scheduler = BlogScheduler()
    
    if args.test:
        logger.info("🧪 Testing notification system...")
        test_data = {
            "title": "Test Post: Advanced Data Pipeline Patterns",
            "excerpt": "Learn best practices for building scalable data pipelines.",
            "read_time": 12,
            "tags": ["Data Engineering", "Pipelines", "Best Practices"],
            "url": "https://victorkirpruto.dev/post/?id=test-post",
            "published_date": datetime.now().strftime("%B %d, %Y"),
            "author": scheduler.config["author"]["name"]
        }
        scheduler.email_notifier.send_new_post_notification(test_data)
        logger.info("✅ Test notification sent")
    elif args.now:
        logger.info("⚡ Generating post immediately...")
        scheduler.generate_and_publish()
    else:
        scheduler.run()

if __name__ == "__main__":
    main()
