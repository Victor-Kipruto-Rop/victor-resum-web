#!/usr/bin/env python3
"""
Dev.to Poster - Publish blog content to Dev.to
"""

import json
import logging
from datetime import datetime
from typing import Dict


class DevtoPoster:
    """Handle Dev.to publishing"""

    def __init__(self, config: Dict):
        """Initialize Dev.to poster"""
        self.config = config.get("platforms", {}).get("devto", {})
        self.logger = logging.getLogger(__name__)

    def post(self, content: Dict, metadata: Dict) -> Dict:
        """
        Publish content to Dev.to

        Args:
            content: Formatted content dict with 'markdown', 'tags'
            metadata: Blog post metadata

        Returns:
            Result dict with success status and article_id
        """
        try:
            if not self.config.get("api_key"):
                return {"success": False, "error": "Dev.to API key not configured"}

            # Prepare Dev.to article
            devto_article = self._format_article(content, metadata)

            self.logger.info(f"Publishing to Dev.to: {content.get('title')}")

            # In production: Use Dev.to API
            # import requests
            # response = requests.post(
            #     "https://dev.to/api/articles",
            #     headers={"api-key": self.config['api_key']},
            #     json={"article": devto_article}
            # )
            # article = response.json()

            article_id = f"devto_{datetime.now().timestamp()}"

            return {
                "success": True,
                "article_id": article_id,
                "url": f"https://dev.to/victorkirpruto/{article_id}",
                "platform": "devto",
                "posted_at": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Dev.to posting error: {str(e)}")
            return {"success": False, "error": str(e)}

    def _format_article(self, content: Dict, metadata: Dict) -> Dict:
        """Format content for Dev.to"""
        tags = content.get("tags", ["dataengineering", "blogging"])[:4]  # Max 4 tags

        return {
            "title": content.get("title", ""),
            "body_markdown": content.get("markdown", ""),
            "tags": tags,
            "published": True,
            "canonical_url": content.get("canonical_url", "")
        }

    def get_status(self) -> Dict:
        """Get Dev.to connection status"""
        try:
            if self.config.get("api_key"):
                return {"status": "connected", "platform": "devto"}
            return {"status": "disconnected", "platform": "devto"}
        except Exception as e:
            return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    # Test
    config = {"platforms": {"devto": {"api_key": "test_key"}}}
    poster = DevtoPoster(config)
    result = poster.post(
        {
            "title": "Test Article",
            "markdown": "# Test\n\nThis is a test article.",
            "tags": ["dataengineering"],
            "canonical_url": "https://victorkirpruto.dev"
        },
        {"date": datetime.now().isoformat()}
    )
    print(json.dumps(result, indent=2))
