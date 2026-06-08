#!/usr/bin/env python3
"""
LinkedIn Poster - Post blog content to LinkedIn
"""

import json
import logging
from datetime import datetime
from typing import Dict, Optional


class LinkedInPoster:
    """Handle LinkedIn posting"""

    def __init__(self, config: Dict):
        """Initialize LinkedIn poster"""
        self.config = config.get("platforms", {}).get("linkedin", {})
        self.logger = logging.getLogger(__name__)

    def post(self, content: Dict, metadata: Dict) -> Dict:
        """
        Post content to LinkedIn

        Args:
            content: Formatted content dict with 'title', 'excerpt', 'url'
            metadata: Blog post metadata

        Returns:
            Result dict with success status and post_id
        """
        try:
            if not self.config.get("access_token"):
                return {"success": False, "error": "LinkedIn access token not configured"}

            # Prepare LinkedIn post
            linkedin_post = self._format_post(content, metadata)

            self.logger.info(f"Posting to LinkedIn: {content.get('title')}")

            # In production: Use LinkedIn API
            import requests
            response = requests.post(
                f"https://api.linkedin.com/v2/ugcPosts",
                headers={"Authorization": f"Bearer {self.config['access_token']}"},
                json=linkedin_post
            )
            
            if not response.ok:
                error_data = response.json()
                raise Exception(f"LinkedIn API error: {error_data.get('message', 'Unknown error')}")

            result = response.json()
            post_id = result.get("id", f"linkedin_{datetime.now().timestamp()}")

            return {
                "success": True,
                "post_id": post_id,
                "url": f"https://www.linkedin.com/feed/update/{post_id}",
                "platform": "linkedin",
                "posted_at": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"LinkedIn posting error: {str(e)}")
            return {"success": False, "error": str(e)}

    def _format_post(self, content: Dict, metadata: Dict) -> Dict:
        """Format content for LinkedIn"""
        return {
            "content": {
                "contentTypes": ["ARTICLE"],
                "title": content.get("title", ""),
                "description": content.get("excerpt", ""),
                "landingPageUrl": content.get("url", "")
            },
            "distribution": {
                "feedDistribution": "PUBLIC",
                "targetAudiences": ["CONNECTIONS", "FOLLOWERS"]
            }
        }

    def get_status(self) -> Dict:
        """Get LinkedIn connection status"""
        try:
            if self.config.get("access_token"):
                return {"status": "connected", "platform": "linkedin"}
            return {"status": "disconnected", "platform": "linkedin"}
        except Exception as e:
            return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    # Test
    config = {"platforms": {"linkedin": {"access_token": "test_token"}}}
    poster = LinkedInPoster(config)
    result = poster.post(
        {"title": "Test", "excerpt": "Test post", "url": "https://example.com"},
        {"date": datetime.now().isoformat()}
    )
    print(json.dumps(result, indent=2))
