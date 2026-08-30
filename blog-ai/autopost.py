#!/usr/bin/env python3
"""
Unified Autopost Script
Full cycle: Generate -> SEO Optimize -> Publish -> Notify -> Social Dispatch -> GitHub Push
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# Add necessary directories to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "social-automation"))

from generate import BlogPostGenerator
from email_notifier import EmailNotifier
from dispatcher import SocialDispatcher
from trend_scraper import TrendScraper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autopost.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Autopost")

def run_autopost_cycle():
    logger.info("🚀 Starting Unified Autopost Cycle...")
    
    try:
        # 1. Initialize services
        generator = BlogPostGenerator()
        notifier = EmailNotifier()
        dispatcher = SocialDispatcher()
        scraper = TrendScraper()
        
        # 2. Get a trending topic
        logger.info("📊 Fetching latest trends...")
        report = scraper.compile_trends_report()
        title = None
        if report['data']['trending_technologies']:
            tech = report['data']['trending_technologies'][0]['name']
            title = f"Building Scalable Systems with {tech}: A Data Engineer's Guide"
            logger.info(f"💡 Selected trending topic: {title}")

        # 3. Generate Post
        logger.info("📝 Generating and SEO optimizing post...")
        title, content, metadata_str = generator.generate_post(title)
        md_file, meta_file = generator.save_post(title, content, metadata_str)
        metadata = json.loads(metadata_str)
        
        # 4. Notify Subscribers
        logger.info("📧 Sending subscriber notifications...")
        post_url = f"https://victorkipruto.com/post.html?id={metadata.get('id', 'latest')}"
        notification_data = {
            "title": title,
            "excerpt": metadata.get("excerpt", ""),
            "read_time": metadata.get("read_time", 10),
            "tags": metadata.get("tags", []),
            "url": post_url,
            "published_date": datetime.now().strftime("%B %d, %Y"),
            "author": generator.config["author"]["name"]
        }
        notifier.send_new_post_notification(notification_data)
        
        # 5. Social Dispatch
        logger.info("📱 Dispatching to social media...")
        post_data = {
            **metadata,
            "content": content,
            "url": post_url
        }
        dispatch_results = dispatcher.dispatch_post(post_data)
        logger.info(f"✅ Social dispatch complete: {dispatch_results['summary']['successful']} successful")

        # 6. GitHub Push
        logger.info("📤 Pushing to GitHub...")
        push_script = Path(__file__).parent / "push.sh"
        if push_script.exists():
            import subprocess
            subprocess.run(["bash", str(push_script), title], cwd=Path(__file__).parent.parent)
            logger.info("✅ GitHub push initiated")

        logger.info("✨ Full Autopost Cycle Completed Successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Autopost Cycle Failed: {str(e)}")
        return False

if __name__ == "__main__":
    run_autopost_cycle()
