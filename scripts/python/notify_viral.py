#!/usr/bin/env python3
"""
Viral Content Notification - Alert when content goes viral
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def notify_viral_content(post_info):
    """
    Send viral content alert notification
    
    Args:
        post_info: Dictionary with viral post details
    """
    try:
        import requests
        
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat = os.getenv('TELEGRAM_CHAT_ID')
        
        if not telegram_token or not telegram_chat:
            print("⚠️  Telegram not configured")
            return False
        
        message = f"""
🚀 VIRAL CONTENT ALERT!

📝 Title: {post_info.get('title', 'Unknown')}
📊 Views: {post_info.get('views', '0')}
👍 Likes: {post_info.get('likes', '0')}
💬 Comments: {post_info.get('comments', '0')}
🔗 Shares: {post_info.get('shares', '0')}
📈 Engagement Rate: {post_info.get('engagement_rate', 'N/A')}%
⚡ Viral Score: {post_info.get('viral_score', 'N/A')}
        """
        
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            'chat_id': telegram_chat,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"✅ Viral alert sent")
            return True
        else:
            print(f"❌ Failed to send viral alert")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    post = {
        'title': 'Amazing Data Engineering Post',
        'views': '50000',
        'likes': '2500',
        'comments': '350',
        'shares': '1200',
        'engagement_rate': '8.5',
        'viral_score': '95'
    }
    notify_viral_content(post)
