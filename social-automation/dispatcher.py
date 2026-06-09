#!/usr/bin/env python3
"""
Social Media Dispatcher - Orchestrates cross-platform content distribution
Coordinates posting to LinkedIn, Twitter, Dev.to, Medium, and Telegram
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import platform-specific handlers
from linkedin import LinkedInPoster
from twitter import TwitterPoster
from devto import DevtoPoster
from medium import MediumPoster
from telegram import TelegramPoster
from formatter import ContentFormatter


class SocialDispatcher:
    """Orchestrate multi-platform content distribution"""

    def __init__(self, config_path: str = "social-automation/config.json"):
        """Initialize dispatcher with configuration"""
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        self.formatter = ContentFormatter(self.config)
        self.platforms = self._initialize_platforms()
        self.dispatch_log = []

    def _load_config(self, config_path: str) -> dict:
        """Load configuration file and resolve environment variables"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Resolve environment variables in config
            config = self._resolve_env_vars(config)
            return config
        except FileNotFoundError:
            self.logger.error(f"Config file not found: {config_path}")
            return {}

    def _resolve_env_vars(self, obj):
        """Recursively resolve environment variables in config"""
        if isinstance(obj, dict):
            return {key: self._resolve_env_vars(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._resolve_env_vars(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            var_name = obj[2:-1]
            return os.getenv(var_name, obj)
        return obj

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for dispatch operations"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler("social_dispatch.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def _initialize_platforms(self) -> Dict:
        """Initialize all platform handlers"""
        platforms = {}

        # LinkedIn
        if self.config.get("platforms", {}).get("linkedin", {}).get("enabled"):
            platforms["linkedin"] = LinkedInPoster(self.config)

        # Twitter/X
        if self.config.get("platforms", {}).get("twitter", {}).get("enabled"):
            platforms["twitter"] = TwitterPoster(self.config)

        # Dev.to
        if self.config.get("platforms", {}).get("devto", {}).get("enabled"):
            platforms["devto"] = DevtoPoster(self.config)

        # Medium
        if self.config.get("platforms", {}).get("medium", {}).get("enabled"):
            platforms["medium"] = MediumPoster(self.config)

        # Telegram
        if self.config.get("platforms", {}).get("telegram", {}).get("enabled"):
            platforms["telegram"] = TelegramPoster(self.config)

        return platforms

    def dispatch_post(self, post_data: Dict) -> Dict:
        """
        Dispatch blog post to all configured platforms

        Args:
            post_data: Blog post data with title, content, metadata

        Returns:
            Dispatch results for each platform
        """
        self.logger.info(f"Starting dispatch for post: {post_data.get('title', 'Unknown')}")

        results = {
            "post_title": post_data.get("title"),
            "dispatch_time": datetime.now().isoformat(),
            "platforms": {},
            "summary": {
                "total_platforms": len(self.platforms),
                "successful": 0,
                "failed": 0,
                "skipped": 0
            }
        }

        # Format content for each platform
        formatted_content = self.formatter.format_for_all_platforms(post_data)

        # Dispatch to each platform
        for platform_name, platform_handler in self.platforms.items():
            try:
                self.logger.info(f"Posting to {platform_name}...")

                platform_content = formatted_content.get(platform_name)
                if not platform_content:
                    self.logger.warning(f"No formatted content for {platform_name}")
                    results["platforms"][platform_name] = {
                        "status": "skipped",
                        "reason": "No formatted content"
                    }
                    results["summary"]["skipped"] += 1
                    continue

                # Post to platform
                post_result = platform_handler.post(platform_content, post_data)

                if post_result.get("success"):
                    self.logger.info(f"✓ Successfully posted to {platform_name}")
                    results["platforms"][platform_name] = {
                        "status": "success",
                        "post_id": post_result.get("post_id"),
                        "url": post_result.get("url"),
                        "timestamp": datetime.now().isoformat()
                    }
                    results["summary"]["successful"] += 1
                else:
                    self.logger.warning(f"✗ Failed to post to {platform_name}: {post_result.get('error')}")
                    results["platforms"][platform_name] = {
                        "status": "failed",
                        "error": post_result.get("error")
                    }
                    results["summary"]["failed"] += 1

            except Exception as e:
                self.logger.error(f"Error posting to {platform_name}: {str(e)}")
                results["platforms"][platform_name] = {
                    "status": "error",
                    "error": str(e)
                }
                results["summary"]["failed"] += 1

        # Notify subscribers
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from subscription_service import SubscriptionService
            sub_service = SubscriptionService()
            sub_results = sub_service.send_new_post_notification(post_data)
            results["subscribers"] = {
                "total_notified": sub_results["total_sent"],
                "email_sent": len(sub_results.get("email", [])),
                "telegram_sent": len(sub_results.get("telegram", []))
            }
            self.logger.info(f"Notified {sub_results['total_sent']} subscribers")
        except Exception as e:
            self.logger.warning(f"Subscriber notification failed: {e}")
            results["subscribers"] = {"error": str(e)}

        self._save_dispatch_result(results)
        return results

    def dispatch_from_file(self, markdown_path: str) -> Dict:
        """
        Dispatch blog post from markdown file

        Args:
            markdown_path: Path to markdown blog post

        Returns:
            Dispatch results
        """
        try:
            post_data = self._parse_markdown_post(markdown_path)
            return self.dispatch_post(post_data)
        except Exception as e:
            self.logger.error(f"Error reading post file: {str(e)}")
            return {"status": "error", "error": str(e)}

    def dispatch_from_metadata(self, metadata_path: str) -> Dict:
        """
        Dispatch blog post using metadata JSON

        Args:
            metadata_path: Path to metadata JSON file

        Returns:
            Dispatch results
        """
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            # Load markdown content
            post_id = metadata.get("id")
            markdown_path = f"blog-ai-posts/{post_id}.md"

            with open(markdown_path, 'r') as f:
                content = f.read()

            post_data = {
                **metadata,
                "content": content
            }

            return self.dispatch_post(post_data)
        except Exception as e:
            self.logger.error(f"Error reading metadata: {str(e)}")
            return {"status": "error", "error": str(e)}

    def _parse_markdown_post(self, markdown_path: str) -> Dict:
        """Parse markdown post into structured data"""
        with open(markdown_path, 'r') as f:
            content = f.read()

        # Extract frontmatter (if present)
        lines = content.split('\n')
        metadata = {}

        # Simple metadata extraction
        return {
            "title": "Blog Post",  # Extract from frontmatter or content
            "content": content,
            "url": f"https://victorkirpruto.dev/posts/{Path(markdown_path).stem}.html",
            "date": datetime.now().isoformat()
        }

    def _save_dispatch_result(self, results: Dict):
        """Save dispatch results to log file"""
        log_path = Path("dispatch_logs")
        log_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_path / f"dispatch_{timestamp}.json"

        with open(log_file, 'w') as f:
            json.dump(results, f, indent=2)

        self.logger.info(f"Dispatch results saved to {log_file}")

    def get_dispatch_status(self) -> Dict:
        """Get status of all configured platforms"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "platforms": {}
        }

        for platform_name, handler in self.platforms.items():
            try:
                platform_status = handler.get_status()
                status["platforms"][platform_name] = platform_status
            except Exception as e:
                status["platforms"][platform_name] = {
                    "status": "error",
                    "error": str(e)
                }

        return status

    def retry_failed_platforms(self, post_data: Dict, failed_platforms: List[str]) -> Dict:
        """
        Retry posting to specific platforms

        Args:
            post_data: Blog post data
            failed_platforms: List of platform names to retry

        Returns:
            Results of retry attempt
        """
        self.logger.info(f"Retrying failed platforms: {failed_platforms}")

        results = {
            "post_title": post_data.get("title"),
            "retry_time": datetime.now().isoformat(),
            "platforms": {},
            "summary": {"successful": 0, "failed": 0}
        }

        formatted_content = self.formatter.format_for_all_platforms(post_data)

        for platform_name in failed_platforms:
            if platform_name not in self.platforms:
                self.logger.warning(f"Platform not configured: {platform_name}")
                continue

            try:
                handler = self.platforms[platform_name]
                platform_content = formatted_content.get(platform_name)

                post_result = handler.post(platform_content, post_data)

                if post_result.get("success"):
                    results["platforms"][platform_name] = {
                        "status": "success",
                        "post_id": post_result.get("post_id")
                    }
                    results["summary"]["successful"] += 1
                else:
                    results["platforms"][platform_name] = {
                        "status": "failed",
                        "error": post_result.get("error")
                    }
                    results["summary"]["failed"] += 1

            except Exception as e:
                results["platforms"][platform_name] = {
                    "status": "error",
                    "error": str(e)
                }
                results["summary"]["failed"] += 1

        return results


def main():
    """CLI interface for social dispatcher"""
    import sys

    dispatcher = SocialDispatcher()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--dispatch-file":
            filepath = sys.argv[2] if len(sys.argv) > 2 else "blog-ai-posts/latest.md"
            results = dispatcher.dispatch_from_file(filepath)
            print(json.dumps(results, indent=2))

        elif sys.argv[1] == "--dispatch-metadata":
            metadata_path = sys.argv[2] if len(sys.argv) > 2 else "blog-ai-posts/latest.meta.json"
            results = dispatcher.dispatch_from_metadata(metadata_path)
            print(json.dumps(results, indent=2))

        elif sys.argv[1] == "--status":
            status = dispatcher.get_dispatch_status()
            print(json.dumps(status, indent=2))

        elif sys.argv[1] == "--retry":
            failed = sys.argv[2:] if len(sys.argv) > 2 else []
            print(f"Would retry: {failed}")

        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Usage: python3 dispatcher.py [--dispatch-file|--dispatch-metadata|--status|--retry]")

    else:
        print("Social Media Dispatcher Ready")
        status = dispatcher.get_dispatch_status()
        print(f"Configured platforms: {list(status['platforms'].keys())}")


if __name__ == "__main__":
    main()
