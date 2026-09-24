#!/usr/bin/env python3
"""
Send newsletter email
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def send_newsletter():
    """Prepare and send newsletter"""
    try:
        if not Path('distribution-content.json').exists():
            print("❌ No distribution content found")
            return False
        
        with open('distribution-content.json', 'r') as f:
            content = json.load(f)
        
        email_content = f"""
<h2>{content['title']}</h2>
<p>{content['description']}</p>
<p><a href="{content['url']}">Read the full article</a></p>
<p><em>Category: {content['category']}</em></p>
"""
        
        print("Email template prepared")
        print(email_content)
        
        # TODO: Integrate with Mailchimp or SendGrid
        # client = MailchimpTransactional.Client()
        # client.messages.send({'html': email_content, ...})
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    send_newsletter()
