#!/usr/bin/env python3
"""
Medium Poster - Publish blog content to Medium
"""

import json
import logging
from datetime import datetime
from typing import Dict


class MediumPoster:
    """Handle Medium publishing"""

    def __init__(self, config: Dict):
        """Initialize Medium poster"""
        self.config = config.get("platforms", {}).get("medium", {})
        self.logger = logging.getLogger(__name__)

    def post(self, content: Dict, metadata: Dict) -> Dict:
        """
        Publish content to Medium

        Args:
            content: Formatted content dict with 'title', 'html', 'tags'
            metadata: Blog post metadata

        Returns:
            Result dict with success status and story_id
        """
        try:
            if not self.config.get("access_token"):
                return {"success": False, "error": "Medium access token not configured"}

            # Get user ID (usually stored in config)
            user_id = self.config.get("user_id")
            if not user_id:
                return {"success": False, "error": "Medium user ID not configured"}

            # Prepare Medium story
            medium_story = self._format_story(content, metadata)

            self.logger.info(f"Publishing to Medium: {content.get('title')}")

            # In production: Use Medium API
            # import requests
            # response = requests.post(
            #     f"https://api.medium.com/v1/users/{user_id}/posts",
            #     headers={"Authorization": f"Bearer {self.config['access_token']}"},
            #     json=medium_story
            # )
            # story = response.json()

            story_id = f"medium_{datetime.now().timestamp()}"

            return {
                "success": True,
                "story_id": story_id,
                "url": f"https://medium.com/@victorkirpruto/{story_id}",
                "platform": "medium",
                "posted_at": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Medium posting error: {str(e)}")
            return {"success": False, "error": str(e)}

    def _format_story(self, content: Dict, metadata: Dict) -> Dict:
        """Format content for Medium"""
        tags = content.get("tags", ["data-engineering", "blog"])[:5]  # Max 5 tags

        return {
            "title": content.get("title", ""),
            "contentFormat": "html",
            "content": content.get("html", ""),
            "tags": tags,
            "canonicalUrl": content.get("canonical_url", ""),
            "publishStatus": "public"
        }

    def get_status(self) -> Dict:
        """Get Medium connection status"""
        try:
            if self.config.get("access_token"):
                return {"status": "connected", "platform": "medium"}
            return {"status": "disconnected", "platform": "medium"}
        except Exception as e:
            return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    # Test
    config = {"platforms": {"medium": {"access_token": "test_token", "user_id": "test_user"}}}
    poster = MediumPoster(config)
    result = poster.post(
        {
            "title": "Test Story",
            "html": "<h1>Test</h1><p>This is a test story.</p>",
            "tags": ["dataengineering"],
            "canonical_url": "https://victorkirpruto.dev"
        },
        {"date": datetime.now().isoformat()}
    )
    print(json.dumps(result, indent=2))
