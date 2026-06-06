#!/usr/bin/env python3
"""
Email Notification Service - Send email notifications
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def send_email_notification(subject, body, to_email=None):
    """
    Send email notification via Resend API
    
    Args:
        subject: Email subject
        body: Email body/content
        to_email: Recipient email (optional)
    """
    try:
        import requests
        
        api_key = os.getenv('RESEND_API_KEY')
        if not api_key:
            print("⚠️  RESEND_API_KEY not configured")
            return False
        
        email = to_email or os.getenv('NOTIFICATION_FROM_EMAIL')
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'from': os.getenv('RESEND_FROM_EMAIL', 'notifications@example.com'),
            'to': email,
            'subject': subject,
            'html': body
        }
        
        response = requests.post(
            'https://api.resend.com/emails',
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"✅ Email sent: {subject}")
            return True
        else:
            print(f"❌ Email failed: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

if __name__ == '__main__':
    send_email_notification(
        subject="Test Notification",
        body="<p>This is a test notification from DBOS</p>"
    )
