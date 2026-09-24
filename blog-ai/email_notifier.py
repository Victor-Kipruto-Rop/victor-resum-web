#!/usr/bin/env python3
"""
Email Notification System
Sends modern HTML emails to blog subscribers
"""

import os
import json
import logging
import requests
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import sqlite3
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import SendGrid, fallback to basic email
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email, To, Content, HtmlContent
    HAS_SENDGRID = True
except ImportError:
    HAS_SENDGRID = False

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent / "config.json"
DB_PATH = Path(__file__).parent.parent / "subscribers.db"

class EmailNotifier:
    def __init__(self):
        """Initialize email notifier"""
        with open(CONFIG_PATH) as f:
            self.config = json.load(f)
        
        self.db_path = DB_PATH
        self._init_database()
        
        # Load API keys and settings from environment
        self.resend_api_key = os.getenv("RESEND_API_KEY")
        self.from_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")
        self.from_name = os.getenv("RESEND_FROM_NAME", "Victor's Technical Blog")
        
        # SMTP settings
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_encryption = os.getenv("SMTP_ENCRYPTION", "tls").lower()

        if self.resend_api_key:
            self.service = "resend"
            logger.info("✅ Resend email service prioritized")
        elif self.smtp_host and self.smtp_user and self.smtp_password:
            self.service = "smtp"
            logger.info("✅ SMTP email service prioritized")
        else:
            self.service = None
            logger.warning("⚠️  No email service configured correctly in .env")

    def _init_database(self):
        """Initialize subscriber database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS subscribers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    name TEXT,
                    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    active BOOLEAN DEFAULT 1,
                    unsubscribe_token TEXT,
                    verification_token TEXT,
                    verified BOOLEAN DEFAULT 0
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS email_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT,
                    message_id TEXT
                )
            """)
            
            conn.commit()

    def subscribe(self, email: str, name: str = "") -> Dict:
        """Add a new subscriber"""
        verification_token = hashlib.sha256(f"{email}{datetime.now()}".encode()).hexdigest()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO subscribers (email, name, verification_token)
                    VALUES (?, ?, ?)
                """, (email, name, verification_token))
                conn.commit()
            
            logger.info(f"✅ New subscriber: {email}")
            
            # Send verification email
            self.send_verification_email(email, verification_token)
            
            return {
                "status": "success",
                "message": "Verification email sent. Please check your inbox.",
                "email": email
            }
        except sqlite3.IntegrityError:
            logger.warning(f"⚠️  Email already subscribed: {email}")
            return {
                "status": "error",
                "message": "This email is already subscribed.",
                "email": email
            }
        except Exception as e:
            logger.error(f"❌ Subscription error: {e}")
            return {
                "status": "error",
                "message": str(e),
                "email": email
            }

    def verify_email(self, token: str) -> Dict:
        """Verify email subscription"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT id, email FROM subscribers WHERE verification_token = ?
                """, (token,))
                result = cursor.fetchone()
                
                if result:
                    conn.execute("""
                        UPDATE subscribers SET verified = 1 WHERE id = ?
                    """, (result[0],))
                    conn.commit()
                    logger.info(f"✅ Email verified: {result[1]}")
                    return {
                        "status": "success",
                        "message": "Email verified! You're now subscribed.",
                        "email": result[1]
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Invalid or expired verification token."
                    }
        except Exception as e:
            logger.error(f"❌ Verification error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def unsubscribe(self, token: str) -> Dict:
        """Unsubscribe from emails"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT id, email FROM subscribers WHERE unsubscribe_token = ?
                """, (token,))
                result = cursor.fetchone()
                
                if result:
                    conn.execute("""
                        UPDATE subscribers SET active = 0 WHERE id = ?
                    """, (result[0],))
                    conn.commit()
                    logger.info(f"✅ Unsubscribed: {result[1]}")
                    return {
                        "status": "success",
                        "message": "You've been unsubscribed.",
                        "email": result[1]
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Invalid unsubscribe token."
                    }
        except Exception as e:
            logger.error(f"❌ Unsubscribe error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def get_active_subscribers(self) -> List[str]:
        """Get all active, verified subscribers"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT email FROM subscribers WHERE active = 1 AND verified = 1
                """)
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"❌ Error fetching subscribers: {e}")
            return []

    def get_subscriber_count(self) -> int:
        """Get count of active subscribers"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM subscribers WHERE active = 1 AND verified = 1
                """)
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"❌ Error counting subscribers: {e}")
            return 0

    def _generate_html_email(self, post_data: Dict) -> str:
        """Generate modern HTML email template"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background: #f5f0e8; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; }}
        .header {{ background: linear-gradient(135deg, #0a0e14 0%, #1a1f2e 100%); color: white; padding: 40px 20px; text-align: center; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header p {{ font-size: 14px; opacity: 0.9; }}
        .content {{ padding: 40px; }}
        .post-title {{ font-size: 24px; color: #0a0e14; margin-bottom: 15px; font-weight: 600; }}
        .metadata {{ display: flex; gap: 20px; margin-bottom: 20px; font-size: 13px; color: #7a7060; }}
        .metadata-item {{ display: flex; align-items: center; }}
        .metadata-item strong {{ color: #0a0e14; }}
        .excerpt {{ font-size: 16px; line-height: 1.6; color: #3a3a3a; margin-bottom: 25px; }}
        .tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 25px; }}
        .tag {{ background: #f0ede8; color: #c8401a; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 500; }}
        .cta-button {{ display: inline-block; background: #c8401a; color: white; padding: 14px 32px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 16px; margin-bottom: 20px; }}
        .cta-button:hover {{ background: #a8300f; }}
        .divider {{ border-top: 1px solid #e0dcd4; margin: 30px 0; }}
        .footer {{ background: #f5f0e8; padding: 20px; text-align: center; font-size: 12px; color: #7a7060; }}
        .footer a {{ color: #c8401a; text-decoration: none; }}
        .author-info {{ background: #f9f7f3; padding: 20px; border-radius: 6px; margin-bottom: 20px; }}
        .author-info strong {{ color: #0a0e14; }}
        @media only screen and (max-width: 600px) {{
            .container {{ width: 100%; }}
            .header {{ padding: 30px 15px; }}
            .content {{ padding: 25px; }}
            .metadata {{ flex-direction: column; gap: 10px; }}
            .tags {{ flex-direction: column; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 New Blog Post</h1>
            <p>{self.config['blog']['title']}</p>
        </div>
        
        <div class="content">
            <div class="post-title">{post_data['title']}</div>
            
            <div class="metadata">
                <div class="metadata-item">
                    <span>📅 <strong>{post_data['published_date']}</strong></span>
                </div>
                <div class="metadata-item">
                    <span>⏱️ <strong>{post_data['read_time']} min read</strong></span>
                </div>
            </div>
            
            <div class="excerpt">{post_data['excerpt']}</div>
            
            <div class="tags">
                {''.join(f'<span class="tag">{tag}</span>' for tag in post_data['tags'][:5])}
            </div>
            
            <a href="{post_data['url']}" class="cta-button">Read Full Article →</a>
            
            <div class="divider"></div>
            
            <div class="author-info">
                <strong>✍️ By {post_data['author']}</strong><br>
                <small>Data Engineer | Building scalable data systems</small>
            </div>
            
            <div style="font-size: 13px; line-height: 1.8; color: #7a7060;">
                <p>You received this email because you're subscribed to {self.config['blog']['title']}.</p>
                <p style="margin-top: 10px;">
                    <a href="https://victorkipruto.com/blog.html">Visit Blog</a> · 
                    <a href="https://victorkipruto.com">Portfolio</a> · 
                    <a href="https://twitter.com/{self.config['author']['twitter'].lstrip('@')}">Follow on Twitter</a>
                </p>
            </div>
        </div>
        
        <div class="footer">
            <p>&copy; 2024-2026 {self.config['author']['name']}. All rights reserved.</p>
            <p style="margin-top: 10px;">
                <a href="UNSUBSCRIBE_LINK">Unsubscribe</a>
            </p>
        </div>
    </div>
</body>
</html>
"""

    def send_verification_email(self, email: str, token: str):
        """Send verification email"""
        subject = f"Verify your subscription to {self.config['blog']['title']}"
        
        verify_url = f"https://victorkipruto.com/api/verify-email?token={token}"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background: #f5f0e8; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; }}
        h2 {{ color: #0a0e14; }}
        .button {{ display: inline-block; background: #c8401a; color: white; padding: 12px 28px; border-radius: 6px; text-decoration: none; font-weight: 600; margin: 20px 0; }}
        .button:hover {{ background: #a8300f; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Verify Your Email</h2>
        <p>Thanks for subscribing to {self.config['blog']['title']}!</p>
        <p>Click the button below to verify your email address:</p>
        <a href="{verify_url}" class="button">Verify Email</a>
        <p style="color: #7a7060; font-size: 12px;">Or copy this link: <br>{verify_url}</p>
    </div>
</body>
</html>
"""
        
        self._send_email(email, subject, html_content)

    def send_new_post_notification(self, post_data: Dict):
        """Send notification to all subscribers about new post"""
        # Get subscribers with their tokens
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT email, unsubscribe_token FROM subscribers WHERE active = 1 AND verified = 1
                """)
                subscribers = cursor.fetchall()
        except Exception as e:
            logger.error(f"❌ Error fetching subscribers: {e}")
            return
        
        if not subscribers:
            logger.warning("⚠️  No active subscribers to notify")
            return
        
        subject = f"📝 New: {post_data['title']}"
        template_html = self._generate_html_email(post_data)
        
        logger.info(f"📧 Sending notification to {len(subscribers)} subscribers...")
        
        success_count = 0
        import hashlib
        for email, token in subscribers:
            try:
                # Fallback token if none exists
                if not token:
                    token = hashlib.sha256(email.encode()).hexdigest()[:16]
                
                unsubscribe_url = f"https://victorkipruto.com/unsubscribe.html?token={token}&email={email}"
                html_content = template_html.replace("UNSUBSCRIBE_LINK", unsubscribe_url)
                
                self._send_email(email, subject, html_content)
                success_count += 1
            except Exception as e:
                logger.error(f"❌ Failed to send to {email}: {e}")
        
        logger.info(f"✅ Sent {success_count}/{len(subscribers)} notifications")

    def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send email with automatic fallback"""
        success = False
        
        # Try Resend first
        if self.resend_api_key:
            success = self._send_via_resend(to_email, subject, html_content)
            if success:
                return True
        
        # Fallback to SMTP
        if not success and self.smtp_host:
            logger.info(f"🔄 Falling back to SMTP for {to_email}")
            return self._send_via_smtp(to_email, subject, html_content)
        
        return False

    def _send_via_resend(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send via Resend API"""
        try:
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {self.resend_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "from": f"{self.from_name} <{self.from_email}>",
                "to": to_email,
                "subject": subject,
                "html": html_content
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                message_id = response.json().get("id", "")
                logger.info(f"✅ Email sent via Resend to {to_email}")
                self._log_email(to_email, subject, "sent_resend", message_id)
                return True
            else:
                logger.error(f"❌ Resend error ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Resend API error: {e}")
            return False

    def _send_via_smtp(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send via SMTP"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.smtp_user}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(html_content, 'html'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.smtp_encryption == "tls":
                    server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
                
            logger.info(f"✅ Email sent via SMTP to {to_email}")
            self._log_email(to_email, subject, "sent_smtp")
            return True
        except Exception as e:
            logger.error(f"❌ SMTP error: {e}")
            return False

    def _log_email(self, email: str, subject: str, status: str, message_id: str = ""):
        """Log email to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO email_logs (email, subject, status, message_id)
                    VALUES (?, ?, ?, ?)
                """, (email, subject, status, message_id))
                conn.commit()
        except Exception as e:
            logger.error(f"❌ Error logging email: {e}")

    def get_stats(self) -> Dict:
        """Get email statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN verified = 1 THEN 1 ELSE 0 END) as verified,
                        SUM(CASE WHEN active = 1 THEN 1 ELSE 0 END) as active
                    FROM subscribers
                """)
                row = cursor.fetchone()
                
                return {
                    "total_subscribers": row[0] or 0,
                    "verified_subscribers": row[1] or 0,
                    "active_subscribers": row[2] or 0
                }
        except Exception as e:
            logger.error(f"❌ Error getting stats: {e}")
            return {
                "total_subscribers": 0,
                "verified_subscribers": 0,
                "active_subscribers": 0
            }
