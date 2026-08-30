#!/usr/bin/env python3
"""Test all email types via Resend API to kiprutovictor39@gmail.com"""
import json
import urllib.request
import urllib.error
import ssl
import time
from pathlib import Path
from datetime import datetime

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
TEST_EMAIL = 'kiprutovictor39@gmail.com'

def send_email(subject, html):
    """Send email via curl (bypasses Cloudflare bot detection on urllib)"""
    import subprocess
    payload = json.dumps({
        "from": f"{RESEND_FROM_NAME} <{RESEND_FROM_EMAIL}>",
        "to": [TEST_EMAIL],
        "subject": subject,
        "html": html
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
        # Split body and HTTP code
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

# ── Email Templates ──

def welcome_html():
    return """
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f1419; color: #e8eef5; border-radius: 16px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #ff4b2b, #ff6d3b); padding: 40px; text-align: center;">
            <h1 style="margin: 0; font-size: 28px; color: white;">🎉 Welcome to DBOS!</h1>
            <p style="color: rgba(255,255,255,0.8); margin-top: 8px;">Your subscription is confirmed</p>
        </div>
        <div style="padding: 40px;">
            <p style="font-size: 16px; line-height: 1.8; margin-bottom: 20px;">Hi Victor,</p>
            <p style="font-size: 15px; line-height: 1.8; margin-bottom: 20px; color: #b0b8c9;">Welcome to my Data Engineering blog! You'll now receive:</p>
            <ul style="font-size: 14px; line-height: 2.2; padding-left: 24px; color: #b0b8c9;">
                <li>✉️ Welcome confirmation (this email)</li>
                <li>📝 New blog post notifications</li>
                <li>📊 Weekly content digests</li>
                <li>🔔 Project updates and announcements</li>
            </ul>
            <div style="text-align: center; margin: 36px 0;">
                <a href="https://victorkipruto.com/blog.html" style="display: inline-block; padding: 16px 32px; background: #ff4b2b; color: white; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 15px;">Read the Blog →</a>
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; margin-bottom: 24px;">
                <p style="font-size: 13px; color: #7a8299; margin: 0;">🏷️ Topics: Data Engineering, ETL Pipelines, Streaming, Cloud Architecture</p>
            </div>
            <p style="font-size: 13px; color: #7a8299; border-top: 1px solid #2d3445; padding-top: 20px;">© 2026 Victor Kipruto Rop · Data Engineer · Nairobi, Kenya<br><a href="https://github.com/Victor-Kipruto-Rop" style="color: #ff4b2b;">GitHub</a> · <a href="https://linkedin.com/in/victor-kipruto-rop" style="color: #ff4b2b;">LinkedIn</a></p>
        </div>
    </div>"""

def new_post_html():
    return """
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f1419; color: #e8eef5; border-radius: 16px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #ff4b2b, #3b82f6); padding: 40px; text-align: center;">
            <h1 style="margin: 0; font-size: 24px; color: white;">📝 New Blog Post</h1>
        </div>
        <div style="padding: 40px;">
            <h2 style="font-size: 24px; margin-bottom: 16px; color: #e8eef5;">Advanced Kubernetes Patterns for Data Engineers</h2>
            <p style="font-size: 15px; line-height: 1.8; margin-bottom: 12px; color: #b0b8c9;">A deep dive into deploying and managing data services on Kubernetes, including Helm charts, StatefulSets for databases, and GitOps workflows for automated deployments.</p>
            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px;">
                <span style="padding: 4px 10px; background: rgba(255,75,43,0.2); color: #ff4b2b; border-radius: 4px; font-size: 12px;">Kubernetes</span>
                <span style="padding: 4px 10px; background: rgba(59,130,246,0.2); color: #3b82f6; border-radius: 4px; font-size: 12px;">Data Engineering</span>
                <span style="padding: 4px 10px; background: rgba(16,185,129,0.2); color: #10b981; border-radius: 4px; font-size: 12px;">Cloud</span>
            </div>
            <div style="text-align: center; margin: 36px 0;">
                <a href="https://victorkipruto.com/blog.html" style="display: inline-block; padding: 16px 32px; background: #ff4b2b; color: white; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 15px;">Read Article →</a>
            </div>
            <p style="font-size: 13px; color: #7a8299; border-top: 1px solid #2d3445; padding-top: 20px;">© 2026 Victor Kipruto Rop · Data Engineer</p>
        </div>
    </div>"""

def custom_html():
    return """
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f1419; color: #e8eef5; border-radius: 16px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #ff4b2b, #3b82f6); padding: 40px; text-align: center;">
            <h1 style="margin: 0; font-size: 24px; color: white;">📢 Custom Notification</h1>
        </div>
        <div style="padding: 40px;">
            <h2 style="font-size: 22px; margin-bottom: 16px; color: #e8eef5;">DBOS System Update</h2>
            <div style="font-size: 15px; line-height: 1.8; color: #b0b8c9;">
                <p>Hi Victor,</p>
                <p>This is a test of the custom notification system. The Blog Operations Center now supports sending custom notifications to subscribers via the Resend API.</p>
                <p><strong>Features:</strong></p>
                <ul style="padding-left: 20px; line-height: 2;">
                    <li>Send to all subscribers at once</li>
                    <li>Custom selection of specific subscribers</li>
                    <li>Real-time delivery status tracking</li>
                    <li>Beautiful HTML email templates</li>
                </ul>
            </div>
            <div style="text-align: center; margin: 36px 0;">
                <a href="https://victorkipruto.com/dashboard/blog-operations-center.html" style="display: inline-block; padding: 16px 32px; background: #3b82f6; color: white; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 15px;">Open Dashboard →</a>
            </div>
            <p style="font-size: 13px; color: #7a8299; border-top: 1px solid #2d3445; padding-top: 20px;">© 2026 Victor Kipruto Rop · DBOS Notifications</p>
        </div>
    </div>"""

def admin_alert_html():
    return """
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f1419; color: #e8eef5; border-radius: 16px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #f59e0b, #ff4b2b); padding: 40px; text-align: center;">
            <h1 style="margin: 0; font-size: 24px; color: white;">🛡️ Admin Alert</h1>
        </div>
        <div style="padding: 40px;">
            <h2 style="font-size: 22px; margin-bottom: 16px; color: #e8eef5;">New Post Published</h2>
            <div style="font-size: 15px; line-height: 1.8; color: #b0b8c9;">
                <p>A new blog post has been published and distributed to all platforms:</p>
                <div style="background: rgba(0,0,0,0.3); padding: 16px; border-radius: 8px; margin: 16px 0;">
                    <p style="margin: 0; color: #ff4b2b; font-weight: 700;">Advanced Kubernetes Patterns for Data Engineers</p>
                </div>
                <p><strong>Platforms:</strong> Twitter/X, LinkedIn, Dev.to, Telegram</p>
                <p><strong>Email Alerts:</strong> Sent to all active subscribers</p>
                <p><strong>Status:</strong> <span style="color: #10b981; font-weight: 700;">✓ All successful</span></p>
            </div>
            <div style="text-align: center; margin: 36px 0;">
                <a href="https://victorkipruto.com/dashboard/blog-operations-center.html" style="display: inline-block; padding: 16px 32px; background: #f59e0b; color: #0f1419; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 15px;">View Dashboard →</a>
            </div>
            <p style="font-size: 13px; color: #7a8299; border-top: 1px solid #2d3445; padding-top: 20px;">© 2026 DBOS · Automated Admin Notification</p>
        </div>
    </div>"""

def weekly_digest_html():
    return """
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f1419; color: #e8eef5; border-radius: 16px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #10b981, #3b82f6); padding: 40px; text-align: center;">
            <h1 style="margin: 0; font-size: 24px; color: white;">📊 Weekly Digest</h1>
            <p style="color: rgba(255,255,255,0.8); margin-top: 8px;">This week's highlights</p>
        </div>
        <div style="padding: 40px;">
            <h2 style="font-size: 22px; margin-bottom: 16px; color: #e8eef5;">Week of June 9, 2026</h2>
            <div style="font-size: 15px; line-height: 1.8; color: #b0b8c9;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
                    <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; text-align: center;">
                        <p style="font-size: 28px; color: #ff4b2b; font-weight: 700; margin: 0;">12</p>
                        <p style="font-size: 12px; color: #7a8299; margin: 4px 0 0;">New Posts</p>
                    </div>
                    <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; text-align: center;">
                        <p style="font-size: 28px; color: #3b82f6; font-weight: 700; margin: 0;">3.2K</p>
                        <p style="font-size: 12px; color: #7a8299; margin: 4px 0 0;">Total Views</p>
                    </div>
                </div>
                <p><strong>🔥 Trending:</strong> "Advanced Kubernetes Patterns" - 890 views this week</p>
                <p><strong>📈 Growth:</strong> Subscriber count grew by 8%</p>
                <p><strong>📝 Top Post:</strong> Data Engineering Full Project Guide</p>
            </div>
            <div style="text-align: center; margin: 36px 0;">
                <a href="https://victorkipruto.com/blog.html" style="display: inline-block; padding: 16px 32px; background: #10b981; color: white; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 15px;">View All Posts →</a>
            </div>
            <p style="font-size: 13px; color: #7a8299; border-top: 1px solid #2d3445; padding-top: 20px;">© 2026 Victor Kipruto Rop · Weekly Digest</p>
        </div>
    </div>"""


# ── Test All Emails ──
def main():
    print(f"📧 Testing email delivery to: {TEST_EMAIL}")
    print(f"   From: {RESEND_FROM_NAME} <{RESEND_FROM_EMAIL}>")
    print(f"   API Key: {RESEND_API_KEY[:10]}...")
    print()
    
    tests = [
        ("1. Welcome Email", "Welcome to Victor Kipruto's Blog!", welcome_html()),
        ("2. New Post Notification", "📝 New Post: Advanced Kubernetes Patterns for Data Engineers", new_post_html()),
        ("3. Custom Notification", "📢 Custom Notification from DBOS", custom_html()),
        ("4. Admin Alert", "🛡️ Admin Alert: New Post Published", admin_alert_html()),
        ("5. Weekly Digest", "📊 Your Weekly Content Digest", weekly_digest_html()),
    ]
    
    results = []
    for name, subject, html in tests:
        print(f"Sending {name}...")
        ok, msg = send_email(subject, html)
        status = "✅ SENT" if ok else "❌ FAILED"
        print(f"  {status}: {msg}")
        results.append((name, ok, msg))
        time.sleep(1)  # Rate limit between emails
    
    print("\n" + "="*50)
    print("RESULTS SUMMARY")
    print("="*50)
    sent = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"Sent: {sent}/{len(results)}")
    print(f"Failed: {failed}/{len(results)}")
    
    if failed > 0:
        print("\nFailed emails:")
        for name, ok, msg in results:
            if not ok:
                print(f"  - {name}: {msg}")

if __name__ == '__main__':
    main()