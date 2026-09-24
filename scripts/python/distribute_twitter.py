#!/usr/bin/env python3
"""
Distribute content to Twitter/X
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def distribute_to_twitter():
    """Prepare and distribute content to Twitter"""
    try:
        with open('distribution-content.json', 'r') as f:
            content = json.load(f)
        
        # Prepare Twitter content
        title = content['title'][:100]
        url = content['url']
        tags = ' '.join([f"#{tag.replace('-', '')}" for tag in content['tags'][:3]])
        
        tweet = f"""📝 New article: {title}

{content['description'][:140]}

Read more: {url}

{tags}"""
        
        print("Tweet preview:")
        print(tweet)
        print(f"\nLength: {len(tweet)} chars")
        
        # TODO: Integrate with Twitter API
        # import tweepy
        # client = tweepy.Client(...)
        # client.create_tweet(text=tweet)
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    distribute_to_twitter()
