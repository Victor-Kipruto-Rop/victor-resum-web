#!/usr/bin/env python3
"""
SEO Notification - Alert on SEO improvements and ranking changes
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def notify_seo_update(seo_data):
    """
    Send SEO update notification
    
    Args:
        seo_data: Dictionary with SEO metrics
    """
    try:
        import requests
        
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat = os.getenv('TELEGRAM_CHAT_ID')
        
        if not telegram_token or not telegram_chat:
            print("⚠️  Telegram not configured")
            return False
        
        message = f"""
📊 SEO Update Detected!

🎯 Keywords Ranking: {seo_data.get('keywords_ranking', 'N/A')}
📈 Traffic Change: {seo_data.get('traffic_change', 'N/A')}
🔍 Indexing Status: {seo_data.get('indexing_status', 'Good')}
⭐ Page Authority: {seo_data.get('page_authority', 'N/A')}
🔗 Backlinks: {seo_data.get('backlinks', '0')}
        """
        
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            'chat_id': telegram_chat,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"✅ SEO notification sent")
            return True
        else:
            print(f"❌ Failed to send SEO notification")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    seo_data = {
        'keywords_ranking': '15 new keywords ranking',
        'traffic_change': '+12%',
        'page_authority': '45',
        'backlinks': '120'
    }
    notify_seo_update(seo_data)
