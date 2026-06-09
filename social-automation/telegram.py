#!/usr/bin/env python3
"""
Telegram Poster - Send blog content to Telegram channel/group
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict


class TelegramPoster:
    """Handle Telegram messaging"""

    def __init__(self, config: Dict):
        """Initialize Telegram poster"""
        self.config = config.get("platforms", {}).get("telegram", {})
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
        Send content to Telegram

        Args:
            content: Formatted content dict with 'message', 'link_preview'
            metadata: Blog post metadata

        Returns:
            Result dict with success status and message_id
        """
        try:
            if not self.config.get("bot_token"):
                return {"success": False, "error": "Telegram bot token not configured"}

            chat_id = self.config.get("channel_id") or self.config.get("chat_id")
            if not chat_id:
                return {"success": False, "error": "Telegram chat_id not configured"}

            # Prepare Telegram message
            telegram_message = self._format_message(content, metadata)

            self.logger.info(f"Sending to Telegram: {content.get('title')}")

            import requests
            response = requests.post(
                f"https://api.telegram.org/bot{self.config['bot_token']}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": telegram_message,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False
                }
            )
            
            if not response.ok:
                error_data = response.json()
                raise Exception(f"Telegram API error: {error_data.get('description', 'Unknown error')}")

            result = response.json()
            message_id = result.get("result", {}).get("message_id", f"telegram_{datetime.now().timestamp()}")

            return {
                "success": True,
                "message_id": message_id,
                "channel": self.config.get("channel_id"),
                "platform": "telegram",
                "posted_at": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Telegram posting error: {str(e)}")
            return {"success": False, "error": str(e)}

    def _format_message(self, content: Dict, metadata: Dict) -> str:
        """Format content for Telegram"""
        title = content.get("title", "")
        excerpt = content.get("excerpt", "")
        url = content.get("url", "")

        message = f"""
<b>{title}</b>

{excerpt}

<a href="{url}">Read full article →</a>

#DataEngineering #Blog
"""
        return message.strip()

    def send_direct_message(self, chat_id: str, message: str) -> Dict:
        """Send direct message to user"""
        try:
            self.logger.info(f"Sending direct message to {chat_id}")

            # In production: Use Telegram Bot API
            # response = requests.post(
            #     f"https://api.telegram.org/bot{self.config['bot_token']}/sendMessage",
            #     json={"chat_id": chat_id, "text": message}
            # )

            return {
                "success": True,
                "message_id": f"telegram_dm_{datetime.now().timestamp()}",
                "platform": "telegram"
            }

        except Exception as e:
            self.logger.error(f"Telegram DM error: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict:
        """Get Telegram connection status"""
        try:
            if self.config.get("bot_token"):
                return {"status": "connected", "platform": "telegram"}
            return {"status": "disconnected", "platform": "telegram"}
        except Exception as e:
            return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    # Test
    config = {"platforms": {"telegram": {"bot_token": "test_token", "channel_id": "@test_channel"}}}
    poster = TelegramPoster(config)
    result = poster.post(
        {
            "title": "New Blog Post",
            "excerpt": "Check out my latest article on data engineering!",
            "url": "https://victorkirpruto.dev/posts/example"
        },
        {"date": datetime.now().isoformat()}
    )
    print(json.dumps(result, indent=2))
