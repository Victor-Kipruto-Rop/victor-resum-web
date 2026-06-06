#!/usr/bin/env python3
"""
Distribute content to Telegram
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def distribute_to_telegram():
    """Send Telegram notification"""
    try:
        if not Path('distribution-content.json').exists():
            print("❌ No distribution content found")
            return False
        
        with open('distribution-content.json', 'r') as f:
            content = json.load(f)
        
        message = f"📝 New Blog Post!\n\n<b>{content['title']}</b>\n\n{content['description']}\n\n<a href=\"{content['url']}\">Read More →</a>"
        
        print("Telegram message preview:")
        print(message)
        
        # TODO: Integrate with Telegram API
        # bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        # chat_id = os.getenv('TELEGRAM_CHAT_ID')
        # url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        # requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    distribute_to_telegram()
