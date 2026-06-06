#!/usr/bin/env python3
"""
Automatic Social Media Poster - Auto-post blog content to all platforms
Integrates with blog_notifier.py to post when new blogs are published

Platforms: Twitter, LinkedIn, Dev.to, Medium, Telegram
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add social-automation to path
current_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(current_dir / "social-automation"))

from blog_notifier import BlogEventNotifier
from formatter import ContentFormatter

try:
    from twitter import TwitterPoster
    from linkedin import LinkedInPoster
    from devto import DevtoPoster
    from medium import MediumPoster
    from telegram import TelegramPoster
except ImportError as e:
    print(f"Warning: Some social modules not available: {e}")


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AutoSocialPoster:
    """Automatically post blog content to all social platforms"""

    def __init__(self, config_path: str = "social-automation/config.json"):
        """Initialize social poster with configuration"""
        self.config = self._load_config(config_path)
        self.formatter = ContentFormatter(self.config)
        self.posters = self._initialize_posters()
        self.notifier = BlogEventNotifier()
        self.social_log = self._load_social_log()

    def _load_config(self, config_path: str) -> dict:
        """Load configuration file and resolve environment variables"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Resolve environment variables
            config = self._resolve_env_vars(config)
            logger.info(f"✅ Loaded config from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            return {}

    def _resolve_env_vars(self, config: dict) -> dict:
        """Recursively resolve environment variables in config"""
        if isinstance(config, dict):
            return {k: self._resolve_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._resolve_env_vars(item) for item in config]
        elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
            env_var = config[2:-1]
            return os.getenv(env_var, config)
        return config

    def _initialize_posters(self) -> Dict:
        """Initialize all platform posters"""
        posters = {}
        
        try:
            if self.config.get("platforms", {}).get("twitter", {}).get("enabled"):
                posters["twitter"] = TwitterPoster(self.config)
                logger.info("✅ Twitter poster initialized")
        except Exception as e:
            logger.warning(f"⚠️  Twitter poster failed: {e}")

        try:
            if self.config.get("platforms", {}).get("linkedin", {}).get("enabled"):
                posters["linkedin"] = LinkedInPoster(self.config)
                logger.info("✅ LinkedIn poster initialized")
        except Exception as e:
            logger.warning(f"⚠️  LinkedIn poster failed: {e}")

        try:
            if self.config.get("platforms", {}).get("devto", {}).get("enabled"):
                posters["devto"] = DevtoPoster(self.config)
                logger.info("✅ Dev.to poster initialized")
        except Exception as e:
            logger.warning(f"⚠️  Dev.to poster failed: {e}")

        try:
            if self.config.get("platforms", {}).get("medium", {}).get("enabled"):
                posters["medium"] = MediumPoster(self.config)
                logger.info("✅ Medium poster initialized")
        except Exception as e:
            logger.warning(f"⚠️  Medium poster failed: {e}")

        try:
            if self.config.get("platforms", {}).get("telegram", {}).get("enabled"):
                posters["telegram"] = TelegramPoster(self.config)
                logger.info("✅ Telegram poster initialized")
        except Exception as e:
            logger.warning(f"⚠️  Telegram poster failed: {e}")

        return posters

    def _load_social_log(self) -> dict:
        """Load log of posts already shared on social media"""
        log_file = Path("scripts/python/.social_posts.json")
        if log_file.exists():
            with open(log_file, 'r') as f:
                return json.load(f)
        return {"posted": []}

    def _save_social_log(self):
        """Save social posting log"""
        log_file = Path("scripts/python/.social_posts.json")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'w') as f:
            json.dump(self.social_log, f, indent=2)

    def _is_already_posted(self, post_id: str, platform: str) -> bool:
        """Check if post was already shared on this platform"""
        for entry in self.social_log.get("posted", []):
            if entry.get("post_id") == post_id and entry.get("platform") == platform:
                return True
        return False

    def _mark_post_shared(self, post_id: str, platform: str, result: Dict):
        """Record that post was shared on platform"""
        self.social_log["posted"].append({
            "post_id": post_id,
            "platform": platform,
            "posted_at": datetime.now().isoformat(),
            "url": result.get("url", ""),
            "status": "success" if result.get("success") else "failed"
        })
        self._save_social_log()

    def post_to_all_platforms(self, post: Dict) -> Dict:
        """Post a blog to all configured platforms"""
        post_id = post.get("id", post.get("slug", "unknown"))
        title = post.get("title", "Untitled")
        
        logger.info(f"🚀 Starting social media distribution for: {title}")
        
        results = {
            "post_id": post_id,
            "title": title,
            "platforms": {},
            "timestamp": datetime.now().isoformat()
        }

        # Format content for all platforms
        formatted = self.formatter.format_for_all_platforms(post)

        # Post to each platform
        for platform, poster in self.posters.items():
            if self._is_already_posted(post_id, platform):
                logger.info(f"ℹ️  Post already shared on {platform}, skipping")
                results["platforms"][platform] = {"status": "skipped", "reason": "already_posted"}
                continue

            try:
                logger.info(f"📤 Posting to {platform}...")
                platform_content = formatted.get(platform, {})
                
                result = poster.post(platform_content, post)
                results["platforms"][platform] = result
                
                if result.get("success"):
                    logger.info(f"✅ Successfully posted to {platform}")
                    logger.info(f"   URL: {result.get('url', 'N/A')}")
                    self._mark_post_shared(post_id, platform, result)
                else:
                    logger.error(f"❌ Failed to post to {platform}: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                logger.error(f"❌ Error posting to {platform}: {str(e)}")
                results["platforms"][platform] = {"success": False, "error": str(e)}

        logger.info(f"✨ Social media distribution complete for: {title}")
        return results

    def post_new_blogs(self):
        """Post all new blogs that haven't been shared yet"""
        logger.info("🔍 Scanning for new blog posts...")
        
        # Load posts from blog/posts.json
        posts_file = Path("blog/posts.json")
        if not posts_file.exists():
            logger.warning("blog/posts.json not found")
            return

        with open(posts_file, 'r') as f:
            data = json.load(f)

        posts = data.get("posts", []) if isinstance(data, dict) else data
        
        if not posts:
            logger.warning("No posts found in blog/posts.json")
            return

        logger.info(f"📚 Found {len(posts)} posts")
        
        shared_count = 0
        for post in posts:
            # Check if any platform posting is pending
            post_id = post.get("id", post.get("slug"))
            platform_status = [
                not self._is_already_posted(post_id, p) 
                for p in self.posters.keys()
            ]
            
            if any(platform_status):
                self.post_to_all_platforms(post)
                shared_count += 1

        if shared_count == 0:
            logger.info("ℹ️  All posts have been shared on all platforms")
        else:
            logger.info(f"✅ Shared {shared_count} posts across all platforms")

    def post_specific_blog(self, slug: str):
        """Post a specific blog by slug"""
        posts_file = Path("blog/posts.json")
        if not posts_file.exists():
            logger.error("blog/posts.json not found")
            return

        with open(posts_file, 'r') as f:
            data = json.load(f)

        posts = data.get("posts", []) if isinstance(data, dict) else data
        
        post = next((p for p in posts if p.get("slug") == slug), None)
        if not post:
            logger.error(f"Post not found: {slug}")
            return

        self.post_to_all_platforms(post)

    def get_status(self) -> Dict:
        """Get status of all social platforms"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "platforms": {}
        }

        for platform, poster in self.posters.items():
            try:
                status["platforms"][platform] = poster.get_status()
            except Exception as e:
                status["platforms"][platform] = {"status": "error", "error": str(e)}

        return status

    def print_status(self):
        """Print formatted status"""
        status = self.get_status()
        print("\n" + "="*60)
        print("🌐 SOCIAL MEDIA PLATFORM STATUS")
        print("="*60)
        
        for platform, info in status.get("platforms", {}).items():
            status_text = info.get("status", "unknown").upper()
            emoji = "✅" if status_text == "CONNECTED" else "❌" if status_text == "ERROR" else "⚠️ "
            print(f"{emoji} {platform.upper():12} - {status_text}")
            
            if "error" in info:
                print(f"   Error: {info['error']}")

        print("="*60 + "\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Automatically post blogs to social media")
    parser.add_argument(
        "command",
        nargs="?",
        default="post-new",
        choices=["post-new", "post-all", "post", "status"],
        help="Command to execute"
    )
    parser.add_argument(
        "slug",
        nargs="?",
        help="Blog post slug (required for 'post' command)"
    )

    args = parser.parse_args()

    poster = AutoSocialPoster()

    if args.command == "status":
        poster.print_status()
    elif args.command == "post-new":
        logger.info("📢 Posting new blogs to social media...")
        poster.post_new_blogs()
    elif args.command == "post-all":
        logger.info("📢 Posting ALL blogs to social media (will retry failed posts)...")
        poster.post_new_blogs()
    elif args.command == "post":
        if not args.slug:
            logger.error("Slug required for 'post' command")
            sys.exit(1)
        logger.info(f"📢 Posting specific blog: {args.slug}")
        poster.post_specific_blog(args.slug)


if __name__ == "__main__":
    main()
