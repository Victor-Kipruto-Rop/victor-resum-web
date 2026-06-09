#!/usr/bin/env python3
"""
Resend Email API Server for Blog Operations Center
Handles email notifications, custom messages, and subscriber alerts.
Run: python scripts/python/resend_server.py
"""
import os
import json
import time
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import urllib.error
import ssl

# Load .env
ENV_PATH = Path(__file__).resolve().parent.parent.parent / '.env'
def load_env():
    env = {}
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env

ENV = load_env()
RESEND_API_KEY = ENV.get('RESEND_API_KEY', '')
RESEND_FROM_EMAIL = 'onboarding@resend.dev'
RESEND_FROM_NAME = 'DBOS Notifications'
SUBSCRIBERS_PATH = Path(__file__).resolve().parent.parent.parent / 'subscribers.json'
NOTIFICATION_LOG_PATH = Path(__file__).resolve().parent.parent.parent / 'notification_log.json'

def get_subscribers():
    if SUBSCRIBERS_PATH.exists():
        return json.loads(SUBSCRIBERS_PATH.read_text())
    return []

def log_notification(entry):
    logs = []
    if NOTIFICATION_LOG_PATH.exists():
        logs = json.loads(NOTIFICATION_LOG_PATH.read_text())
    logs.insert(0, entry)
    logs = logs[:200]  # Keep last 200
    NOTIFICATION_LOG_PATH.write_text(json.dumps(logs, indent=2))

def send_resend_email(to_email, to_name, subject, html_content):
    """Send email via Resend API using curl (bypasses Cloudflare)"""
    import subprocess
    payload = json.dumps({
        "from": f"{RESEND_FROM_NAME} <{RESEND_FROM_EMAIL}>",
        "to": [to_email],
        "subject": subject,
        "html": html_content
    })
    try:
        result = subprocess.run(
            ["curl", "-s", "-w", "\n__HTTP_CODE__%{http_code}",
             "-X", "POST", "https://api.resend.com/emails",
             "-H", f"Authorization: Bearer {RESEND_API_KEY}",
             "-H", "Content-Type: application/json",
             "-d", payload],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout
        parts = output.rsplit("__HTTP_CODE__", 1)
        body = parts[0].strip() if len(parts) > 1 else output.strip()
        http_code = parts[1].strip() if len(parts) > 1 else "0"
        data = json.loads(body) if body else {}
        if http_code.startswith("2"):
            return True, data.get('id', 'unknown')
        else:
            error_msg = data.get('message', body)
            return False, f"HTTP {http_code}: {error_msg}"
    except Exception as e:
        return False, str(e)

def build_welcome_html(name):
    return f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f1419; color: #e8eef5; border-radius: 16px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #ff4b2b, #ff6d3b); padding: 32px; text-align: center;">
            <h1 style="margin: 0; font-size: 24px; color: white;">Welcome to DBOS!</h1>
        </div>
        <div style="padding: 32px;">
            <p style="font-size: 16px; line-height: 1.7; margin-bottom: 20px;">Hi {name},</p>
            <p style="font-size: 15px; line-height: 1.7; margin-bottom: 20px;">You've been subscribed to Victor Kipruto Rop's Data Engineering blog. You'll receive notifications about:</p>
            <ul style="font-size: 14px; line-height: 2; padding-left: 20px; color: #b0b8c9;">
                <li>New technical blog posts on Data Engineering</li>
                <li>Weekly content digests</li>
                <li>Project updates and announcements</li>
            </ul>
            <div style="text-align: center; margin: 32px 0;">
                <a href="https://victor-kipruto-rop.github.io/victor-resum-web/blog.html" style="display: inline-block; padding: 14px 28px; background: #ff4b2b; color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">Read the Blog →</a>
            </div>
            <p style="font-size: 13px; color: #7a8299; border-top: 1px solid #2d3445; padding-top: 20px; margin-top: 32px;">© 2026 Victor Kipruto Rop · Data Engineer · Nairobi, Kenya</p>
        </div>
    </div>"""

def build_new_post_html(post_title, post_excerpt, post_url):
    return f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f1419; color: #e8eef5; border-radius: 16px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #ff4b2b, #3b82f6); padding: 32px; text-align: center;">
            <h1 style="margin: 0; font-size: 20px; color: white;">New Blog Post</h1>
        </div>
        <div style="padding: 32px;">
            <h2 style="font-size: 22px; margin-bottom: 16px; color: #e8eef5;">{post_title}</h2>
            <p style="font-size: 15px; line-height: 1.7; margin-bottom: 20px; color: #b0b8c9;">{post_excerpt}</p>
            <div style="text-align: center; margin: 32px 0;">
                <a href="{post_url}" style="display: inline-block; padding: 14px 28px; background: #ff4b2b; color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">Read Article →</a>
            </div>
            <p style="font-size: 13px; color: #7a8299; border-top: 1px solid #2d3445; padding-top: 20px; margin-top: 32px;">© 2026 Victor Kipruto Rop · Data Engineer</p>
        </div>
    </div>"""

def build_custom_html(title, message):
    return f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f1419; color: #e8eef5; border-radius: 16px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #ff4b2b, #3b82f6); padding: 32px; text-align: center;">
            <h1 style="margin: 0; font-size: 20px; color: white;">{title}</h1>
        </div>
        <div style="padding: 32px;">
            <div style="font-size: 15px; line-height: 1.8; color: #b0b8c9;">{message}</div>
            <p style="font-size: 13px; color: #7a8299; border-top: 1px solid #2d3445; padding-top: 20px; margin-top: 32px;">© 2026 Victor Kipruto Rop · Data Engineer</p>
        </div>
    </div>"""


class NotificationHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/subscribers':
            subs = get_subscribers()
            self.send_json(200, {'subscribers': subs})
        elif self.path == '/api/notifications':
            logs = []
            if NOTIFICATION_LOG_PATH.exists():
                logs = json.loads(NOTIFICATION_LOG_PATH.read_text())
            self.send_json(200, {'notifications': logs})
        else:
            self.send_json(404, {'error': 'Not found'})

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(content_length)) if content_length > 0 else {}

        if self.path == '/api/subscribe':
            name = body.get('name', '').strip()
            email = body.get('email', '').strip()
            if not name or not email:
                self.send_json(400, {'error': 'Name and email required'})
                return
            
            subs = get_subscribers()
            if any(s.get('email') == email for s in subs):
                self.send_json(409, {'error': 'Already subscribed'})
                return
            
            sub = {
                'name': name,
                'email': email,
                'joined': datetime.now().isoformat(),
                'welcomeSent': False,
                'status': 'active'
            }
            subs.append(sub)
            SUBSCRIBERS_PATH.write_text(json.dumps(subs, indent=2))
            
            # Send welcome email via Resend
            ok, msg = send_resend_email(email, name, 'Welcome to Victor Kipruto\'s Blog!', build_welcome_html(name))
            if ok:
                sub['welcomeSent'] = True
                subs[-1] = sub
                SUBSCRIBERS_PATH.write_text(json.dumps(subs, indent=2))
            
            log_notification({
                'type': 'welcome',
                'title': f'Welcome email sent to {name}',
                'recipients': email,
                'sentAt': datetime.now().isoformat(),
                'status': 'sent' if ok else 'failed',
                'details': msg
            })
            
            self.send_json(200, {'success': ok, 'message': msg})

        elif self.path == '/api/send-notification':
            recipients = body.get('recipients', 'all')  # 'all', 'custom', or email
            title = body.get('title', 'Notification')
            message = body.get('message', '')
            notif_type = body.get('type', 'custom')  # 'custom', 'new_post'
            
            subs = get_subscribers()
            active = [s for s in subs if s.get('status') == 'active']
            
            if recipients == 'all':
                targets = active
            elif recipients == 'custom':
                custom_emails = body.get('customEmails', [])
                targets = [s for s in active if s['email'] in custom_emails]
            else:
                targets = [s for s in active if s['email'] == recipients]
            
            sent = 0
            failed = 0
            errors = []
            
            for sub in targets:
                if notif_type == 'new_post':
                    post_title = body.get('postTitle', 'New Blog Post')
                    post_excerpt = body.get('postExcerpt', 'A new article has been published.')
                    post_url = body.get('postUrl', 'https://victor-kipruto-rop.github.io/victor-resum-web/blog.html')
                    html = build_new_post_html(post_title, post_excerpt, post_url)
                    subject = f'New Post: {post_title}'
                else:
                    html = build_custom_html(title, message)
                    subject = title
                
                ok, msg = send_resend_email(sub['email'], sub['name'], subject, html)
                if ok:
                    sent += 1
                else:
                    failed += 1
                    errors.append(f"{sub['email']}: {msg}")
                time.sleep(0.5)  # Rate limiting
            
            log_notification({
                'type': notif_type,
                'title': title,
                'recipients': f'{sent} sent, {failed} failed',
                'sentAt': datetime.now().isoformat(),
                'status': 'sent' if failed == 0 else 'partial',
                'details': '; '.join(errors) if errors else 'All delivered'
            })
            
            self.send_json(200, {
                'success': failed == 0,
                'sent': sent,
                'failed': failed,
                'errors': errors
            })

        elif self.path == '/api/send-welcome':
            email = body.get('email', '')
            name = body.get('name', '')
            ok, msg = send_resend_email(email, name, 'Welcome to Victor Kipruto\'s Blog!', build_welcome_html(name))
            log_notification({
                'type': 'welcome',
                'title': f'Welcome email to {name}',
                'recipients': email,
                'sentAt': datetime.now().isoformat(),
                'status': 'sent' if ok else 'failed',
                'details': msg
            })
            self.send_json(200, {'success': ok, 'message': msg})

        else:
            self.send_json(404, {'error': 'Not found'})

    def send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


def main():
    port = 8765
    server = HTTPServer(('127.0.0.1', port), NotificationHandler)
    print(f"📧 Resend Notification Server running on http://127.0.0.1:{port}")
    print(f"   From: {RESEND_FROM_NAME} <{RESEND_FROM_EMAIL}>")
    print(f"   API: http://127.0.0.1:{port}/api/subscribers")
    print(f"   POST: /api/subscribe, /api/send-notification, /api/send-welcome")
    server.serve_forever()

if __name__ == '__main__':
    main()