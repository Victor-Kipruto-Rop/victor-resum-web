#!/usr/bin/env python3
"""
DBOS Telegram Notification Engine
Sends real-time alerts via Telegram Bot API
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from urllib.parse import quote

class TelegramNotifier:
    """Send alerts to Telegram"""
    
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHAT_ID')
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        self.log_file = Path('notifications/telegram-log.json')
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def validate_credentials(self) -> bool:
        """Validate Telegram credentials"""
        if not self.bot_token or not self.chat_id:
            print("⚠️  Missing Telegram credentials")
            print("   Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables")
            return False
        return True
    
    def send_alert(self, title: str, message: str, severity: str = "info", 
                   metadata: Optional[Dict] = None, url: Optional[str] = None) -> bool:
        """Send alert to Telegram"""
        if not self.validate_credentials():
            return False
        
        try:
            # Build formatted message
            formatted_msg = self._format_message(title, message, severity, metadata, url)
            
            payload = {
                "chat_id": self.chat_id,
                "text": formatted_msg,
                "parse_mode": "Markdown"
            }
            
            response = requests.post(self.base_url, json=payload, timeout=10)
            
            success = response.status_code == 200
            
            # Log the notification
            self._log_notification({
                "timestamp": datetime.utcnow().isoformat(),
                "title": title,
                "severity": severity,
                "success": success,
                "message_length": len(formatted_msg),
                "status_code": response.status_code
            })
            
            return success
        
        except Exception as e:
            print(f"❌ Telegram notification failed: {str(e)}")
            return False
    
    def send_blog_published(self, title: str, slug: str, seo_score: int, 
                            category: str, url_base: str = "https://victor-kipruto-rop.github.io/victor-resum-web") -> bool:
        """Send blog published alert"""
        message = f"""
*Blog Published Successfully* ✅

📝 *Title:* {title}
📁 *Category:* {category}
📊 *SEO Score:* {seo_score}/100
🔗 *Link:* {url_base}/blog/posts/{slug}

"""
        return self.send_alert("📝 NEW BLOG PUBLISHED", message, "info", {"slug": slug, "seo_score": seo_score})
    
    def send_blog_failed(self, title: str, error: str) -> bool:
        """Send blog publishing failure alert"""
        message = f"""
*Blog Publishing Failed* ❌

📝 *Title:* {title}
🚨 *Error:* {error}

Please check the GitHub Actions workflow and fix the issue.
"""
        return self.send_alert("❌ BLOG PUBLISHING FAILED", message, "critical", {"title": title})
    
    def send_viral_detected(self, title: str, views: int, growth_rate: float, 
                            viral_score: int, url_base: str = "https://victor-kipruto-rop.github.io/victor-resum-web") -> bool:
        """Send viral content alert"""
        message = f"""
*🔥 VIRAL CONTENT DETECTED* 🔥

📝 *Title:* {title}
👀 *Views (24h):* {views}
📈 *Growth Rate:* {growth_rate:.1f}x
🎯 *Viral Score:* {viral_score}/100

This post is trending! Consider amplifying on social media.
"""
        return self.send_alert("🔥 VIRAL CONTENT", message, "high")
    
    def send_recruiter_detected(self, company: str, pages_visited: int, score: float, 
                                time_spent: int, returning: bool = False) -> bool:
        """Send recruiter activity alert"""
        if returning:
            title = "💼 RETURNING RECRUITER DETECTED"
            emoji = "🔄"
        else:
            title = "💼 RECRUITER DETECTED"
            emoji = "👤"
        
        message = f"""
{emoji} *{company} Recruiter Activity Detected* {emoji}

🏢 *Company:* {company}
📊 *Interest Score:* {score:.0%}
📄 *Pages Visited:* {pages_visited}
⏱️ *Time Spent:* {time_spent}s

This could be a recruiting opportunity!
"""
        return self.send_alert(title, message, "high")
    
    def send_seo_warning(self, title: str, score: int, issues: list) -> bool:
        """Send SEO warning alert"""
        issues_text = "\n".join([f"• {issue}" for issue in issues[:3]])
        
        message = f"""
*SEO Issue Detected* ⚠️

📝 *Post:* {title}
📊 *SEO Score:* {score}/100
🔧 *Issues:*
{issues_text}

Improve your SEO to boost visibility.
"""
        return self.send_alert("⚠️ SEO WARNING", message, "medium")
    
    def send_traffic_spike(self, title: str, views: int, spike_factor: float) -> bool:
        """Send traffic spike alert"""
        message = f"""
*Traffic Spike Detected* 📈

📝 *Post:* {title}
👀 *Views:* {views}
📊 *Spike Factor:* {spike_factor:.1f}x

Your content is getting attention!
"""
        return self.send_alert("📈 TRAFFIC SPIKE", message, "medium")
    
    def send_github_actions_status(self, workflow: str, status: str, details: str = "") -> bool:
        """Send GitHub Actions status alert"""
        if status == "success":
            emoji = "✅"
            severity = "info"
        else:
            emoji = "❌"
            severity = "high"
        
        message = f"""
*GitHub Actions {status.upper()}* {emoji}

🔄 *Workflow:* {workflow}
📊 *Status:* {status.upper()}
"""
        if details:
            message += f"📝 *Details:* {details}\n"
        
        return self.send_alert(f"🔄 GITHUB ACTIONS {status.upper()}", message, severity)
    
    def send_system_health_alert(self, issue: str, severity: str = "medium") -> bool:
        """Send system health alert"""
        severity_emoji = {
            "low": "ℹ️",
            "medium": "⚠️",
            "high": "🚨"
        }.get(severity, "ℹ️")
        
        message = f"""
*System Health Alert* {severity_emoji}

🔧 *Issue:* {issue}
📊 *Severity:* {severity.upper()}

Please investigate and resolve if needed.
"""
        return self.send_alert("🔧 SYSTEM HEALTH", message, severity)
    
    def send_daily_summary(self, stats: Dict[str, Any]) -> bool:
        """Send daily summary alert"""
        message = f"""
*Daily Summary* 📊

📝 *Posts Published:* {stats.get('posts_published', 0)}
👀 *Total Views:* {stats.get('total_views', 0)}
👤 *Unique Visitors:* {stats.get('unique_visitors', 0)}
💼 *Recruiters Detected:* {stats.get('recruiters_detected', 0)}
🔥 *Viral Posts:* {stats.get('viral_posts', 0)}
⚠️ *Issues:* {stats.get('issues_count', 0)}
✅ *Workflow Success Rate:* {stats.get('workflow_success_rate', 0):.0%}
"""
        return self.send_alert("📊 DAILY SUMMARY", message, "info")
    
    def _format_message(self, title: str, message: str, severity: str, 
                       metadata: Optional[Dict], url: Optional[str]) -> str:
        """Format message for Telegram"""
        formatted = f"*{title}*\n\n{message}"
        
        if metadata:
            formatted += "\n_Metadata:_\n"
            for key, value in metadata.items():
                formatted += f"• {key}: {value}\n"
        
        if url:
            formatted += f"\n[View Details]({url})"
        
        return formatted
    
    def _log_notification(self, log_entry: Dict):
        """Log notification for auditing"""
        try:
            logs = []
            if self.log_file.exists():
                with open(self.log_file) as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to log notification: {str(e)}")
    
    def get_notification_log(self) -> list:
        """Get notification history"""
        if self.log_file.exists():
            with open(self.log_file) as f:
                return json.load(f)
        return []
    
    def run_test(self):
        """Run test notification"""
        print("\n🚀 Telegram Notifier Test\n")
        
        if not self.validate_credentials():
            print("⚠️  Skipping test - credentials not configured")
            return
        
        # Send test alert
        test_message = "This is a test alert from DBOS Notification System"
        success = self.send_alert("🧪 TEST ALERT", test_message, "info", 
                                 {"timestamp": datetime.utcnow().isoformat()})
        
        if success:
            print("✅ Test notification sent successfully!")
        else:
            print("❌ Test notification failed!")

if __name__ == '__main__':
    notifier = TelegramNotifier()
    notifier.run_test()
