#!/usr/bin/env python3
"""
Test Email Sending - Send welcome email to test subscriber
Tests direct email delivery without subscription form
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'python'))

from email_templates_modern import TEMPLATES, generate_unsubscribe_token

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_section(title):
    print(f"\n📌 {title}")
    print("-" * 70)

def print_success(msg):
    print(f"✅ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_warning(msg):
    print(f"⚠️  {msg}")

def print_info(msg):
    print(f"ℹ️  {msg}")

def send_welcome_email(name, email):
    """Send welcome email directly"""
    print_section(f"SENDING WELCOME EMAIL TO {email}")
    
    print(f"\n📧 Email Details:")
    print_info(f"   Recipient: {name} <{email}>")
    print_info(f"   Template: Welcome Email")
    print_info(f"   Subject: Welcome to Victor Kipruto's Blog! 🚀")
    
    try:
        # Generate welcome email
        token = generate_unsubscribe_token(email)
        html_content = TEMPLATES['welcome'](name, email)
        
        print_info(f"   HTML Size: {len(html_content):,} bytes")
        print_info(f"   Unsubscribe Token: {token}")
        
        # Check for Resend API key
        resend_api_key = os.getenv('RESEND_API_KEY', '')
        sender_email = os.getenv('SENDER_EMAIL', 'onboarding@resend.dev')
        
        if resend_api_key:
            print(f"\n🌐 Using Resend API...")
            print_info(f"   API Key: {resend_api_key[:20]}...")
            print_info(f"   From: {sender_email}")
            
            # Send via Resend API
            try:
                response = requests.post(
                    'https://api.resend.com/emails',
                    headers={
                        'Authorization': f'Bearer {resend_api_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'from': sender_email,
                        'to': email,
                        'subject': 'Welcome to Victor Kipruto\'s Blog! 🚀',
                        'html': html_content,
                        'tags': [
                            {'name': 'type', 'value': 'welcome'},
                            {'name': 'test', 'value': 'true'}
                        ]
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    message_id = data.get('id')
                    print_success(f"Email sent successfully!")
                    print_info(f"   Message ID: {message_id}")
                    
                    # Save record
                    save_email_record(name, email, message_id, token, 'sent')
                    return {'success': True, 'message_id': message_id}
                else:
                    error_msg = response.text
                    print_error(f"Resend API error: {response.status_code}")
                    print_error(f"   Response: {error_msg[:200]}")
                    save_email_record(name, email, None, token, 'failed', error_msg)
                    return {'success': False, 'error': error_msg}
            
            except requests.exceptions.RequestException as e:
                print_error(f"Request failed: {str(e)}")
                save_email_record(name, email, None, token, 'failed', str(e))
                return {'success': False, 'error': str(e)}
        else:
            print_warning(f"Resend API key not configured")
            print(f"\n💾 Saving email to test file...")
            
            # Save to test file
            test_email_data = {
                'to': email,
                'from': sender_email,
                'subject': 'Welcome to Victor Kipruto\'s Blog! 🚀',
                'name': name,
                'html': html_content[:200] + '...' if len(html_content) > 200 else html_content,
                'token': token,
                'timestamp': datetime.now().isoformat(),
                'status': 'test_mode'
            }
            
            test_file = 'data/test_emails.json'
            Path('data').mkdir(exist_ok=True)
            
            test_emails = []
            if Path(test_file).exists():
                with open(test_file) as f:
                    test_emails = json.load(f)
            
            test_emails.append(test_email_data)
            with open(test_file, 'w') as f:
                json.dump(test_emails, f, indent=2)
            
            print_success(f"Email saved to {test_file}")
            print_info(f"   Total test emails: {len(test_emails)}")
            
            return {'success': True, 'saved_to_file': test_file}
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return {'success': False, 'error': str(e)}

def save_email_record(name, email, message_id, token, status, error=None):
    """Save email record for tracking"""
    record_file = 'data/email_records.json'
    Path('data').mkdir(exist_ok=True)
    
    record = {
        'name': name,
        'email': email,
        'message_id': message_id,
        'token': token,
        'status': status,
        'timestamp': datetime.now().isoformat(),
        'error': error
    }
    
    records = []
    if Path(record_file).exists():
        with open(record_file) as f:
            records = json.load(f)
    
    records.append(record)
    with open(record_file, 'w') as f:
        json.dump(records, f, indent=2)

def test_with_subscription_api(name, email):
    """Test subscription via API endpoint"""
    print_section(f"TESTING VIA SUBSCRIPTION API")
    
    api_endpoints = [
        'http://localhost:5000/api/subscribe',
        'http://127.0.0.1:5000/api/subscribe',
    ]
    
    payload = {
        'name': name,
        'email': email,
        'channels': ['email', 'telegram', 'twitter']
    }
    
    for api_url in api_endpoints:
        try:
            print_info(f"Trying: {api_url}")
            response = requests.post(
                api_url,
                json=payload,
                timeout=5
            )
            
            if response.status_code in [201, 200]:
                data = response.json()
                print_success(f"Subscription API responded successfully!")
                print_info(f"   Status Code: {response.status_code}")
                print_info(f"   Response: {data.get('message', 'OK')}")
                return True
            else:
                print_warning(f"   Status Code: {response.status_code}")
                print_warning(f"   Response: {response.text[:100]}")
        except Exception as e:
            print_warning(f"   Failed: {str(e)[:60]}")
    
    return False

def main():
    print_header("📧 TEST WELCOME EMAIL")
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test recipient
    test_name = "Victor Kipruto"
    test_email = "kiprutovictor39@gmail.com"
    
    print(f"\n👤 Test Subscriber:")
    print_info(f"   Name: {test_name}")
    print_info(f"   Email: {test_email}")
    
    # Check Resend API configuration
    resend_api_key = os.getenv('RESEND_API_KEY', '')
    print(f"\n🔐 Configuration:")
    
    if resend_api_key:
        print_success(f"Resend API Key: Configured")
        print_info(f"   Key (truncated): {resend_api_key[:20]}...{resend_api_key[-10:]}")
    else:
        print_warning(f"Resend API Key: NOT configured")
        print_info(f"   Will save to test file instead")
    
    # Test 1: Direct email sending
    print_header("TEST 1: DIRECT EMAIL SENDING")
    result1 = send_welcome_email(test_name, test_email)
    
    # Test 2: Via API (if running)
    print_header("TEST 2: SUBSCRIPTION API")
    print("\nChecking if subscription API is running...")
    result2 = test_with_subscription_api(test_name, test_email)
    
    # Summary
    print_header("📊 TEST SUMMARY")
    
    print(f"\n✉️  Email Template: Modern Welcome Email")
    print_info(f"   Template: TEMPLATES['welcome']")
    print_info(f"   Status: Generated successfully")
    
    print(f"\n🚀 Sending Results:")
    if result1['success']:
        print_success(f"Direct sending: SUCCESS")
        if result1.get('message_id'):
            print_info(f"   Message ID: {result1['message_id']}")
    else:
        print_error(f"Direct sending: FAILED")
        if result1.get('error'):
            print_error(f"   Error: {result1['error'][:100]}")
    
    if result2:
        print_success(f"API subscription: SUCCESS")
    else:
        print_warning(f"API subscription: Not available (service may not be running)")
    
    # Next steps
    print_header("🚀 NEXT STEPS")
    
    if not resend_api_key:
        print("""
To enable live email sending:

1. Get Resend API Key:
   - Visit https://resend.com
   - Create an account
   - Verify your email domain
   - Get API key from settings

2. Set environment variable:
   export RESEND_API_KEY='re_xxxxxxxxxxxxxxxx'

3. Run test again:
   python3 test_send_email.py

4. Check email in inbox:
   - From: onboarding@resend.dev (or your verified domain)
   - To: kiprutovictor39@gmail.com
   - Subject: Welcome to Victor Kipruto's Blog! 🚀
        """)
    else:
        print("""
✅ Resend API is configured!

Email should arrive at kiprutovictor39@gmail.com shortly.

Monitor delivery:
1. Check Resend dashboard: https://resend.com
2. Check Gmail inbox and spam folder
3. View email records: data/email_records.json

For production deployment:
1. Set SENDER_EMAIL environment variable:
   export SENDER_EMAIL='noreply@yourdomain.com'

2. Run subscription service:
   python3 subscription_email_service.py

3. Test via form at:
   http://localhost:5500/subscribe.html
        """)
    
    # Show email records
    print_header("📋 EMAIL RECORDS")
    
    if Path('data/email_records.json').exists():
        with open('data/email_records.json') as f:
            records = json.load(f)
        
        print(f"\nTotal emails sent: {len(records)}")
        for i, record in enumerate(records[-5:], 1):  # Show last 5
            status_symbol = "✅" if record['status'] == 'sent' else "⚠️ "
            print(f"\n{i}. {status_symbol} {record['email']}")
            print_info(f"   Status: {record['status']}")
            if record.get('message_id'):
                print_info(f"   Message ID: {record['message_id']}")
            print_info(f"   Time: {record['timestamp']}")
    
    print("\n✅ TEST COMPLETE\n")

if __name__ == '__main__':
    main()
