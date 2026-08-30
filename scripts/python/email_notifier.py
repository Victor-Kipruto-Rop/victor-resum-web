#!/usr/bin/env python3
"""
DBOS Email Notification System
Sends emails via Resend API or SMTP
"""

import os
import json
import smtplib
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotifier:
    """Send notifications via email"""
    
    def __init__(self, smtp_host: Optional[str] = None, smtp_port: Optional[int] = None,
                 smtp_user: Optional[str] = None, smtp_password: Optional[str] = None,
                 from_email: Optional[str] = None, to_emails: Optional[List[str]] = None):
        self.smtp_host = smtp_host or os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = smtp_port or int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = smtp_user or os.getenv('SMTP_USER')
        self.smtp_password = smtp_password or os.getenv('SMTP_PASSWORD')
        self.from_email = from_email or os.getenv('NOTIFICATION_FROM_EMAIL')
        self.to_emails = to_emails or [os.getenv('NOTIFICATION_TO_EMAIL', 'victor@kipruto.dev')]
        self.log_file = Path('notifications/email-log.json')
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def validate_credentials(self) -> bool:
        """Validate email credentials"""
        if not self.smtp_user or not self.smtp_password or not self.from_email:
            print("⚠️  Missing email credentials")
            print("   Set SMTP_USER, SMTP_PASSWORD, NOTIFICATION_FROM_EMAIL env vars")
            return False
        return True
    
    def send_email(self, to_emails: Optional[List[str]], subject: str, 
                   html_body: str, text_body: str = "") -> bool:
        """Send email via SMTP"""
        if not self.validate_credentials():
            return False
        
        try:
            to_emails = to_emails or self.to_emails
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)
            
            # Attach text and HTML
            if text_body:
                msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send via SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            # Log success
            self._log_email({
                "timestamp": datetime.utcnow().isoformat(),
                "subject": subject,
                "to": to_emails,
                "success": True
            })
            
            return True
        
        except Exception as e:
            print(f"❌ Email sending failed: {str(e)}")
            self._log_email({
                "timestamp": datetime.utcnow().isoformat(),
                "subject": subject,
                "to": to_emails,
                "success": False,
                "error": str(e)
            })
            return False
    
    def send_blog_published(self, title: str, slug: str, summary: str, 
                           category: str, url_base: str = "https://victorkipruto.com") -> bool:
        """Send blog published email"""
        blog_url = f"{url_base}/blog/posts/{slug}"
        
        html_body = f"""
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white;">
                <h2 style="margin-top: 0;">📝 New Blog Post Published</h2>
                <p style="font-size: 16px;"><strong>{title}</strong></p>
                <p style="opacity: 0.9;">Category: <strong>{category}</strong></p>
                <p style="opacity: 0.9;">{summary}</p>
                <a href="{blog_url}" style="display: inline-block; background: white; color: #667eea; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin-top: 10px; font-weight: bold;">Read Full Article</a>
            </div>
            <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #999;">
                DBOS Notification System | Do not reply to this email
            </p>
        </body>
        </html>
        """
        
        text_body = f"""
New Blog Post Published

Title: {title}
Category: {category}
Summary: {summary}

Read: {blog_url}
        """
        
        return self.send_email(None, f"📝 New Blog: {title}", html_body, text_body)
    
    def send_viral_alert(self, title: str, views: int, engagement: float) -> bool:
        """Send viral content email"""
        html_body = f"""
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 8px; color: white;">
                <h2 style="margin-top: 0;">🔥 Viral Content Detected!</h2>
                <p style="font-size: 18px; font-weight: bold;">{title}</p>
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 4px; margin: 15px 0;">
                    <p style="margin: 5px 0;">👀 Views: <strong>{views}</strong></p>
                    <p style="margin: 5px 0;">💬 Engagement: <strong>{engagement:.1%}</strong></p>
                </div>
                <p>Your content is trending! Consider amplifying it on social media.</p>
            </div>
            <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #999;">
                DBOS Notification System
            </p>
        </body>
        </html>
        """
        
        return self.send_email(None, f"🔥 Viral Content: {title}", html_body)
    
    def send_recruiter_alert(self, company: str, pages: int, score: float) -> bool:
        """Send recruiter activity email"""
        html_body = f"""
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 8px; color: white;">
                <h2 style="margin-top: 0;">💼 Recruiter Activity Detected</h2>
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 4px; margin: 15px 0;">
                    <p style="margin: 5px 0;">🏢 Company: <strong>{company}</strong></p>
                    <p style="margin: 5px 0;">📄 Pages Visited: <strong>{pages}</strong></p>
                    <p style="margin: 5px 0;">📊 Interest Score: <strong>{score:.0%}</strong></p>
                </div>
                <p>This could be a recruiting opportunity. Make sure your CV/portfolio is up to date!</p>
            </div>
            <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #999;">
                DBOS Notification System
            </p>
        </body>
        </html>
        """
        
        return self.send_email(None, f"💼 Recruiter: {company}", html_body)
    
    def send_weekly_summary(self, stats: Dict[str, Any]) -> bool:
        """Send weekly summary email"""
        html_body = f"""
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white;">
                <h2 style="margin-top: 0;">📊 Weekly Summary</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0;">
                    <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 4px;">
                        <p style="margin: 0; opacity: 0.9;">Posts Published</p>
                        <p style="margin: 5px 0; font-size: 24px; font-weight: bold;">{stats.get('posts_published', 0)}</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 4px;">
                        <p style="margin: 0; opacity: 0.9;">Total Views</p>
                        <p style="margin: 5px 0; font-size: 24px; font-weight: bold;">{stats.get('total_views', 0)}</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 4px;">
                        <p style="margin: 0; opacity: 0.9;">Visitors</p>
                        <p style="margin: 5px 0; font-size: 24px; font-weight: bold;">{stats.get('unique_visitors', 0)}</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 4px;">
                        <p style="margin: 0; opacity: 0.9;">Recruiters</p>
                        <p style="margin: 5px 0; font-size: 24px; font-weight: bold;">{stats.get('recruiters_detected', 0)}</p>
                    </div>
                </div>
                <p style="margin-top: 20px; margin-bottom: 0;">Keep creating great content! 🚀</p>
            </div>
            <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #999;">
                DBOS Notification System
            </p>
        </body>
        </html>
        """
        
        return self.send_email(None, "📊 Weekly Summary Report", html_body)
    
    def send_error_alert(self, error_type: str, message: str, details: str = "") -> bool:
        """Send error alert email"""
        html_body = f"""
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #eb3b5a 0(), #fc5c65 100%); border-radius: 8px; color: white;">
                <h2 style="margin-top: 0;">❌ Error Alert</h2>
                <p style="font-size: 16px;"><strong>{error_type}</strong></p>
                <p>{message}</p>
                {f'<p style="background: rgba(0,0,0,0.2); padding: 10px; border-radius: 4px; white-space: pre-wrap; font-family: monospace;">{details}</p>' if details else ''}
                <p style="margin-bottom: 0;">Please check your system and investigate.</p>
            </div>
            <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #999;">
                DBOS Notification System
            </p>
        </body>
        </html>
        """
        
        return self.send_email(None, f"❌ Error: {error_type}", html_body)
    
    def _log_email(self, log_entry: Dict):
        """Log email for auditing"""
        try:
            logs = []
            if self.log_file.exists():
                with open(self.log_file) as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to log email: {str(e)}")
    
    def get_email_log(self) -> list:
        """Get email history"""
        if self.log_file.exists():
            with open(self.log_file) as f:
                return json.load(f)
        return []
    
    def run_test(self):
        """Run test email"""
        print("\n🚀 Email Notifier Test\n")
        
        if not self.validate_credentials():
            print("⚠️  Skipping test - credentials not configured")
            print("   Configure: SMTP_USER, SMTP_PASSWORD, NOTIFICATION_FROM_EMAIL")
            return
        
        html_body = """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>🧪 Test Email from DBOS</h2>
            <p>This is a test notification from the DBOS Notification System.</p>
            <p>If you're reading this, email notifications are working correctly!</p>
        </body>
        </html>
        """
        
        success = self.send_email(None, "🧪 Test Email from DBOS", html_body)
        
        if success:
            print("✅ Test email sent successfully!")
        else:
            print("❌ Test email failed!")

if __name__ == '__main__':
    notifier = EmailNotifier()
    notifier.run_test()
