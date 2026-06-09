#!/usr/bin/env python3
"""
LinkedIn Poster - Post blog content to LinkedIn
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict


class LinkedInPoster:
    """Handle LinkedIn posting"""

    def __init__(self, config: Dict):
        """Initialize LinkedIn poster"""
        self.config = config.get("platforms", {}).get("linkedin", {})
        self._resolve_env_vars(self.config)
        self.logger = logging.getLogger(__name__)

    def _resolve_env_vars(self, obj):
        """Resolve ${ENV_VAR} references in config"""
        if isinstance(obj, dict):
            for k, v in obj.items():
                obj[k] = self._resolve_env_vars(v)
        elif isinstance(obj, list):
            return [self._resolve_env_vars(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            return os.getenv(obj[2:-1], obj)
        return obj

    def post(self, content: Dict, metadata: Dict) -> Dict:
        """
        Post content to LinkedIn
        """
        try:
            token = self.config.get("access_token")
            if not token:
                return {"success": False, "error": "LinkedIn access token not configured"}

            import requests
            
            # 1. Get Member URN (Priority: .env override -> /me -> /userinfo)
            member_urn = os.getenv("LINKEDIN_MEMBER_URN")
            
            if member_urn:
                author_urn = member_urn if member_urn.startswith("urn:li:") else f"urn:li:person:{member_urn}"
                self.logger.info(f"Using manual Member URN from .env: {author_urn}")
            else:
                self.logger.info("Fetching LinkedIn profile to get member ID...")
                me_response = requests.get(
                    "https://api.linkedin.com/v2/me",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if me_response.ok:
                    member_id = me_response.json().get("id")
                    author_urn = f"urn:li:person:{member_id}"
                else:
                    # Try userinfo fallback (OpenID Connect)
                    self.logger.info("Retrying with userinfo endpoint...")
                    ui_response = requests.get(
                        "https://api.linkedin.com/v2/userinfo",
                        headers={"Authorization": f"Bearer {token}"}
                    )
                    if not ui_response.ok:
                        error_data = ui_response.json()
                        raise Exception(f"LinkedIn Profile error: {error_data.get('message', 'Not enough permissions to get URN. Please add openid/profile scope or set LINKEDIN_MEMBER_URN in .env')}")
                    member_id = ui_response.json().get("sub")
                    author_urn = f"urn:li:person:{member_id}"

            self.logger.info(f"Using Author URN: {author_urn}")

            # 2. Prepare LinkedIn post (ugcPosts format)
            linkedin_post = {
                "author": author_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": f"{content.get('title')}\n\n{content.get('excerpt')}\n\nRead more: {content.get('url')}"
                        },
                        "shareMediaCategory": "ARTICLE",
                        "media": [
                            {
                                "status": "READY",
                                "description": {
                                    "text": content.get("excerpt", "")
                                },
                                "originalUrl": content.get("url", ""),
                                "title": {
                                    "text": content.get("title", "")
                                }
                            }
                        ]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            self.logger.info(f"Posting to LinkedIn: {content.get('title')}")

            response = requests.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers={"Authorization": f"Bearer {token}"},
                json=linkedin_post
            )
            
            if not response.ok:
                error_data = response.json()
                # If error is about unpermitted fields, it might be the wrong endpoint/schema
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
