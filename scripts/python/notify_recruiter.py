#!/usr/bin/env python3
"""
Recruiter Notification - Alert on recruiter visits
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def notify_recruiter_visit(recruiter_info):
    """
    Send notification when recruiter visits
    
    Args:
        recruiter_info: Dictionary with recruiter details
    """
    try:
        import requests
        
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat = os.getenv('TELEGRAM_CHAT_ID')
        
        if not telegram_token or not telegram_chat:
            print("⚠️  Telegram not configured")
            return False
        
        message = f"""
🔍 Recruiter Visit Detected!

👤 Name: {recruiter_info.get('name', 'Unknown')}
🏢 Company: {recruiter_info.get('company', 'Unknown')}
📧 Email: {recruiter_info.get('email', 'N/A')}
🔗 LinkedIn: {recruiter_info.get('linkedin', 'N/A')}
⏰ Time: {recruiter_info.get('timestamp', 'Unknown')}
        """
        
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            'chat_id': telegram_chat,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"✅ Recruiter alert sent")
            return True
        else:
            print(f"❌ Failed to send recruiter alert")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    recruiter = {
        'name': 'John Doe',
        'company': 'Tech Company',
        'email': 'john@example.com',
        'linkedin': 'https://linkedin.com/in/johndoe'
    }
    notify_recruiter_visit(recruiter)
