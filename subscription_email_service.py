#!/usr/bin/env python3
"""
Subscription Email Service - Sends welcome emails to new subscribers
Integrates with modern email templates and Resend API
"""

import os
import sys
import json
import hashlib
import requests
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts', 'python'))

from email_templates_modern import TEMPLATES, generate_unsubscribe_token

app = Flask(__name__)
CORS(app)

# Configuration
RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'onboarding@resend.dev')
SUBSCRIBERS_FILE = 'data/subscribers.json'

# Ensure data directory exists
Path('data').mkdir(exist_ok=True)

def load_subscribers():
    """Load subscribers from file"""
    if Path(SUBSCRIBERS_FILE).exists():
        with open(SUBSCRIBERS_FILE) as f:
            return json.load(f)
    return {'subscribers': []}

def save_subscribers(data):
    """Save subscribers to file"""
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def send_email_via_resend(to_email, name, subject, html_content):
    """Send email via Resend API"""
    if not RESEND_API_KEY:
        return {
            'success': False,
            'error': 'Resend API key not configured',
            'message_id': None
        }
    
    try:
        response = requests.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {RESEND_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'from': SENDER_EMAIL,
                'to': to_email,
                'subject': subject,
                'html': html_content,
                'tags': [
                    {'name': 'type', 'value': 'welcome'},
                    {'name': 'template', 'value': 'modern_welcome'}
                ]
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'message_id': data.get('id'),
                'error': None
            }
        else:
            return {
                'success': False,
                'error': response.text,
                'message_id': None
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message_id': None
        }

def send_email_via_test(to_email, name, subject, html_content):
    """Save email to file for testing (when Resend API not available)"""
    try:
        email_data = {
            'to': to_email,
            'from': SENDER_EMAIL,
            'subject': subject,
            'name': name,
            'html': html_content[:500] + '...' if len(html_content) > 500 else html_content,
            'timestamp': datetime.now().isoformat(),
            'status': 'test_saved'
        }
        
        # Save to test emails file
        test_file = 'data/test_emails.json'
        test_emails = []
        if Path(test_file).exists():
            with open(test_file) as f:
                test_emails = json.load(f)
        
        test_emails.append(email_data)
        with open(test_file, 'w') as f:
            json.dump(test_emails, f, indent=2)
        
        return {
            'success': True,
            'message_id': hashlib.md5(f"{to_email}{datetime.now().isoformat()}".encode()).hexdigest(),
            'error': None,
            'note': 'Email saved to test file (Resend API not configured)'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message_id': None
        }

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """Handle subscription requests"""
    try:
        data = request.json
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        
        if not name or not email:
            return jsonify({
                'success': False,
                'error': 'Name and email are required'
            }), 400
        
        # Validate email format
        if '@' not in email:
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400
        
        # Load existing subscribers
        subscribers_data = load_subscribers()
        subscribers = subscribers_data.get('subscribers', [])
        
        # Check if already subscribed
        existing = next((s for s in subscribers if s['email'].lower() == email.lower()), None)
        if existing:
            return jsonify({
                'success': False,
                'error': 'Already subscribed',
                'email': email
            }), 409
        
        # Generate welcome email
        try:
            token = generate_unsubscribe_token(email)
            welcome_html = TEMPLATES['welcome'](name, email)
            
            # Send email
            if RESEND_API_KEY:
                email_result = send_email_via_resend(
                    email,
                    name,
                    f"Welcome to Victor Kipruto's Blog! 🚀",
                    welcome_html
                )
            else:
                email_result = send_email_via_test(
                    email,
                    name,
                    f"Welcome to Victor Kipruto's Blog! 🚀",
                    welcome_html
                )
            
            # Add subscriber record
            subscriber = {
                'name': name,
                'email': email,
                'subscribed_at': datetime.now().isoformat(),
                'token': token,
                'email_sent': email_result['success'],
                'email_message_id': email_result.get('message_id'),
                'channels': data.get('channels', ['email'])
            }
            
            subscribers.append(subscriber)
            subscribers_data['subscribers'] = subscribers
            subscribers_data['last_updated'] = datetime.now().isoformat()
            save_subscribers(subscribers_data)
            
            response_data = {
                'success': True,
                'message': f'Successfully subscribed {name}!',
                'email': email,
                'email_sent': email_result['success']
            }
            
            if not email_result['success']:
                response_data['email_error'] = email_result.get('error')
                response_data['note'] = email_result.get('note')
            
            return jsonify(response_data), 201
            
        except Exception as e:
            print(f"Error generating/sending welcome email: {e}")
            # Still save subscriber even if email fails
            subscriber = {
                'name': name,
                'email': email,
                'subscribed_at': datetime.now().isoformat(),
                'token': generate_unsubscribe_token(email),
                'email_sent': False,
                'email_error': str(e),
                'channels': data.get('channels', ['email'])
            }
            
            subscribers.append(subscriber)
            subscribers_data['subscribers'] = subscribers
            subscribers_data['last_updated'] = datetime.now().isoformat()
            save_subscribers(subscribers_data)
            
            return jsonify({
                'success': True,
                'message': f'Subscribed {name} but email delivery failed',
                'email': email,
                'email_sent': False,
                'email_error': str(e)
            }), 201
    
    except Exception as e:
        print(f"Subscription error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/subscribers', methods=['GET'])
def get_subscribers():
    """Get all subscribers (admin endpoint)"""
    try:
        data = load_subscribers()
        subscribers = data.get('subscribers', [])
        
        return jsonify({
            'success': True,
            'count': len(subscribers),
            'subscribers': [
                {
                    'name': s['name'],
                    'email': s['email'],
                    'subscribed_at': s['subscribed_at'],
                    'email_sent': s.get('email_sent', False)
                }
                for s in subscribers
            ]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/subscriber/<email>', methods=['DELETE'])
def unsubscribe(email):
    """Handle unsubscribe requests"""
    try:
        data = load_subscribers()
        subscribers = data.get('subscribers', [])
        
        # Remove subscriber
        original_count = len(subscribers)
        data['subscribers'] = [s for s in subscribers if s['email'].lower() != email.lower()]
        
        if len(data['subscribers']) < original_count:
            data['last_updated'] = datetime.now().isoformat()
            save_subscribers(data)
            
            return jsonify({
                'success': True,
                'message': f'Unsubscribed {email}'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Subscriber not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'resend_configured': bool(RESEND_API_KEY),
        'service': 'subscription-email-service'
    }), 200

if __name__ == '__main__':
    print("🚀 Starting Subscription Email Service...")
    print(f"   Resend API: {'✓ Configured' if RESEND_API_KEY else '✗ Not configured'}")
    print(f"   Sender: {SENDER_EMAIL}")
    print(f"   Port: 5000")
    print()
    
    app.run(debug=True, port=5000)
