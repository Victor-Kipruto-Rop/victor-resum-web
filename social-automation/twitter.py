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
            import tweepy
            client = tweepy.Client(
                bearer_token=self.config.get('bearer_token'),
                consumer_key=self.config.get('api_key'),
                consumer_secret=self.config.get('api_secret'),
                access_token=self.config.get('access_token'),
                access_token_secret=self.config.get('access_token_secret')
            )
            
            tweet_ids = []
            previous_tweet_id = None
            
            for i, tweet_text in enumerate(tweets):
                # Validate tweet length
                if len(tweet_text) > self.max_length:
                    self.logger.warning(f"Tweet {i+1} exceeds max length, truncating")
                    tweet_text = tweet_text[:self.max_length-3] + "..."

                if i == 0:
                    response = client.create_tweet(text=tweet_text)
                else:
                    response = client.create_tweet(text=tweet_text, in_reply_to_tweet_id=previous_tweet_id)
                
                tweet_id = response.data.get("id")
                tweet_ids.append(tweet_id)
                previous_tweet_id = tweet_id

            return {
                "success": True,
                "tweet_ids": tweet_ids,
                "thread_count": len(tweets),
                "url": f"https://twitter.com/{self.config.get('handle', 'user').replace('@', '')}/status/{tweet_ids[0]}",
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
