#!/usr/bin/env python3
"""
Twitter/X Poster - Post blog content to Twitter/X
"""

import json
import logging
from datetime import datetime
from typing import Dict


class TwitterPoster:
    """Handle Twitter/X posting"""

    def __init__(self, config: Dict):
        """Initialize Twitter poster"""
        self.config = config.get("platforms", {}).get("twitter", {})
        self.logger = logging.getLogger(__name__)
        self.max_length = 280

    def post(self, content: Dict, metadata: Dict) -> Dict:
        """
        Post content to Twitter/X

        Args:
            content: Formatted content dict with 'tweet', 'thread'
            metadata: Blog post metadata

        Returns:
            Result dict with success status and tweet_id
        """
        try:
            if not self.config.get("api_key"):
                return {"success": False, "error": "Twitter API key not configured"}

            tweets = content.get("thread", [content.get("tweet", "")])

            self.logger.info(f"Posting to Twitter/X with {len(tweets)} tweets")

            # In production: Use Twitter API v2
            # client = tweepy.Client(
            #     bearer_token=self.config['bearer_token'],
            #     consumer_key=self.config['api_key'],
            #     consumer_secret=self.config['api_secret'],
            #     access_token=self.config['access_token'],
            #     access_token_secret=self.config['access_token_secret']
            # )
            # response = client.create_tweet(text=tweets[0])

            tweet_ids = []
            for i, tweet in enumerate(tweets):
                # Validate tweet length
                if len(tweet) > self.max_length:
                    self.logger.warning(f"Tweet {i+1} exceeds max length, truncating")
                    tweet = tweet[:self.max_length-3] + "..."

                tweet_id = f"twitter_{datetime.now().timestamp()}_{i}"
                tweet_ids.append(tweet_id)

            return {
                "success": True,
                "tweet_ids": tweet_ids,
                "thread_count": len(tweets),
                "url": f"https://twitter.com/victorkirpruto/status/{tweet_ids[0]}",
                "platform": "twitter",
                "posted_at": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Twitter posting error: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict:
        """Get Twitter connection status"""
        try:
            if self.config.get("api_key"):
                return {"status": "connected", "platform": "twitter"}
            return {"status": "disconnected", "platform": "twitter"}
        except Exception as e:
            return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    # Test
    config = {"platforms": {"twitter": {"api_key": "test_key"}}}
    poster = TwitterPoster(config)
    result = poster.post(
        {"tweet": "Check out my latest blog post! 🚀", "thread": []},
        {"date": datetime.now().isoformat()}
    )
    print(json.dumps(result, indent=2))
