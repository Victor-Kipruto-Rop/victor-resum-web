#!/usr/bin/env python3
"""
DBOS Master Notification Engine
Orchestrates all notification channels and event sources
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from alert_classifier import AlertClassifier, AlertSeverity, AlertType
from viral_detector import ViralDetector
from recruiter_detector import RecruiterDetector
from telegram_notifier import TelegramNotifier
from email_notifier import EmailNotifier

class NotificationEngine:
    """Master notification engine - orchestrates all channels and events"""
    
    def __init__(self):
        self.classifier = AlertClassifier()
        self.viral_detector = ViralDetector()
        self.recruiter_detector = RecruiterDetector()
        self.telegram = TelegramNotifier()
        self.email = EmailNotifier()
        
        self.logs_file = Path('notifications/notification-logs.json')
        self.alerts_file = Path('notifications/alerts-queue.json')
        self.config_file = Path('notifications/notification-config.json')
        
        self.logs_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.notification_log = self.load_logs()
        self.alerts_queue = self.load_queue()
        self.config = self.load_config()
    
    def load_logs(self) -> List[Dict]:
        """Load notification history"""
        if self.logs_file.exists():
            with open(self.logs_file) as f:
                return json.load(f)
        return []
    
    def load_queue(self) -> List[Dict]:
        """Load queued alerts"""
        if self.alerts_file.exists():
            with open(self.alerts_file) as f:
                return json.load(f)
        return []
    
    def load_config(self) -> Dict:
        """Load notification configuration"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default notification config"""
        return {
            "telegram_enabled": True,
            "email_enabled": True,
            "discord_enabled": False,
            "alert_priorities": {
                "critical": ["telegram", "email"],
                "high": ["telegram", "email"],
                "medium": ["email"],
                "low": ["email"]
            },
            "deduplication_window_minutes": 5,
            "retry_attempts": 3
        }
    
    def save_logs(self):
        """Save notification logs"""
        with open(self.logs_file, 'w') as f:
            json.dump(self.notification_log[-1000:], f, indent=2)  # Keep last 1000
    
    def save_queue(self):
        """Save alert queue"""
        with open(self.alerts_file, 'w') as f:
            json.dump(self.alerts_queue, f, indent=2)
    
    def save_config(self):
        """Save notification config"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def queue_alert(self, alert_type: str, title: str, message: str, 
                   severity: str, metadata: Optional[Dict] = None) -> str:
        """Queue an alert for processing"""
        alert_id = f"alert_{len(self.alerts_queue)}_{datetime.utcnow().timestamp()}"
        
        alert = {
            "id": alert_id,
            "type": alert_type,
            "title": title,
            "message": message,
            "severity": severity,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending",
            "retry_count": 0
        }
        
        self.alerts_queue.append(alert)
        self.save_queue()
        
        return alert_id
    
    def process_alert(self, alert: Dict) -> bool:
        """Process a queued alert through notification channels"""
        severity = alert["severity"]
        channels = self.config["alert_priorities"].get(severity, ["email"])
        
        success = True
        
        # Send through enabled channels
        if "telegram" in channels and self.config.get("telegram_enabled"):
            if not self.telegram.send_alert(
                alert["title"],
                alert["message"],
                severity,
                alert.get("metadata"),
                alert.get("url")
            ):
                success = False
        
        if "email" in channels and self.config.get("email_enabled"):
            if not self.email.send_email(
                None,
                alert["title"],
                self._format_email_body(alert),
                alert["message"]
            ):
                success = False
        
        # Log result
        self._log_notification({
            "alert_id": alert["id"],
            "type": alert["type"],
            "channels": channels,
            "success": success,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return success
    
    def _format_email_body(self, alert: Dict) -> str:
        """Format alert as email HTML body"""
        return f"""
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <h2>{alert['title']}</h2>
            <p>{alert['message']}</p>
            <hr>
            <p style="font-size: 12px; color: #999;">
                {datetime.fromisoformat(alert['timestamp']).strftime('%Y-%m-%d %H:%M:%S UTC')}
            </p>
        </body>
        </html>
        """
    
    def handle_blog_published(self, post_data: Dict[str, Any]) -> str:
        """Handle blog published event"""
        classification = self.classifier.classify_blog_event({
            "status": "published",
            "title": post_data.get("title"),
            "seo_score": post_data.get("seo_score", 70)
        })
        
        alert_id = self.queue_alert(
            AlertType.BLOG_PUBLISHED.value,
            classification["message"],
            f"Blog post '{post_data.get('title')}' has been published successfully.",
            classification["severity"],
            {
                "slug": post_data.get("slug"),
                "category": post_data.get("category"),
                "seo_score": post_data.get("seo_score")
            }
        )
        
        # Send immediately for high priority
        if classification["priority"] <= 2:
            self.process_alert(self.alerts_queue[-1])
        
        return alert_id
    
    def handle_blog_failed(self, post_title: str, error: str) -> str:
        """Handle blog publishing failure"""
        classification = self.classifier.classify_blog_event({
            "status": "failed",
            "title": post_title
        })
        
        alert_id = self.queue_alert(
            AlertType.BLOG_FAILED.value,
            classification["message"],
            f"Error: {error}",
            classification["severity"],
            {"error": error}
        )
        
        # Send immediately - this is critical
        self.process_alert(self.alerts_queue[-1])
        
        return alert_id
    
    def handle_viral_detected(self, post_data: Dict[str, Any]) -> str:
        """Handle viral content detection"""
        classification = self.classifier.classify_analytics_event({
            "post_title": post_data.get("title"),
            "views": post_data.get("views", 0),
            "growth_rate": post_data.get("growth_rate", 2.5),
            "traffic_spike": True,
            "engagement_rate": post_data.get("engagement_rate", 0.75)
        })
        
        message = f"""
🔥 {post_data.get('title')}

Views (24h): {post_data.get('views', 0)}
Growth Rate: {post_data.get('growth_rate', 2.5):.1f}x
Engagement: {post_data.get('engagement_rate', 0.75):.0%}

This post is trending! Share it on social media! 🚀
        """
        
        alert_id = self.queue_alert(
            AlertType.VIRAL_DETECTED.value,
            "🔥 VIRAL CONTENT DETECTED",
            message,
            classification["severity"],
            {
                "slug": post_data.get("slug"),
                "views": post_data.get("views"),
                "viral_score": post_data.get("viral_score", 85)
            }
        )
        
        # Send immediately
        self.process_alert(self.alerts_queue[-1])
        
        return alert_id
    
    def handle_recruiter_detected(self, recruiter_data: Dict[str, Any]) -> str:
        """Handle recruiter detection"""
        classification = self.classifier.classify_recruiter_event({
            "company": recruiter_data.get("company"),
            "recruiter_score": recruiter_data.get("recruiter_score", 0.75),
            "returning": recruiter_data.get("returning", False)
        })
        
        alert_type = AlertType.RECRUITER_RETURNING if recruiter_data.get("returning") else AlertType.RECRUITER_DETECTED
        
        message = f"""
💼 {recruiter_data.get('company')} Activity

Interest Score: {recruiter_data.get('recruiter_score', 0.75):.0%}
Pages Visited: {recruiter_data.get('pages_visited', 3)}
Time Spent: {recruiter_data.get('time_spent_seconds', 300)}s

This could be a recruiting opportunity! Make sure your CV is polished. 📄
        """
        
        alert_id = self.queue_alert(
            alert_type.value,
            classification["message"],
            message,
            classification["severity"],
            {
                "company": recruiter_data.get("company"),
                "score": recruiter_data.get("recruiter_score"),
                "tier": recruiter_data.get("tier")
            }
        )
        
        # Send immediately
        self.process_alert(self.alerts_queue[-1])
        
        return alert_id
    
    def handle_seo_warning(self, seo_data: Dict[str, Any]) -> str:
        """Handle SEO warning"""
        classification = self.classifier.classify_seo_event({
            "post_title": seo_data.get("post_title"),
            "seo_score": seo_data.get("seo_score", 65),
            "issue_type": seo_data.get("issue_type", "warning")
        })
        
        issues = seo_data.get("issues", [])
        issues_text = "\n".join([f"• {issue}" for issue in issues[:5]])
        
        message = f"""
⚠️ SEO Issues Detected

Post: {seo_data.get('post_title')}
SEO Score: {seo_data.get('seo_score', 65)}/100

Issues:
{issues_text}

Recommendations:
{chr(10).join([f"• {rec}" for rec in seo_data.get('recommendations', [])[:3]])}
        """
        
        alert_id = self.queue_alert(
            AlertType.SEO_WARNING.value,
            classification["message"],
            message,
            classification["severity"],
            {
                "post_slug": seo_data.get("post_slug"),
                "seo_score": seo_data.get("seo_score"),
                "issue_count": len(issues)
            }
        )
        
        return alert_id
    
    def handle_github_actions_status(self, workflow_data: Dict[str, Any]) -> str:
        """Handle GitHub Actions status"""
        classification = self.classifier.classify_automation_event({
            "workflow_name": workflow_data.get("workflow_name"),
            "status": workflow_data.get("status", "success")
        })
        
        message = f"""
{workflow_data.get('workflow_name')}

Status: {workflow_data.get('status').upper()}
Duration: {workflow_data.get('duration_seconds', 0)}s
Timestamp: {workflow_data.get('timestamp')}

{f"Error: {workflow_data.get('error_message')}" if workflow_data.get('status') == 'failure' else 'All systems operational!'}
        """
        
        alert_id = self.queue_alert(
            classification["type"],
            classification["message"],
            message,
            classification["severity"],
            {
                "workflow": workflow_data.get("workflow_name"),
                "status": workflow_data.get("status")
            }
        )
        
        # Send immediately for failures
        if workflow_data.get("status") == "failure":
            self.process_alert(self.alerts_queue[-1])
        
        return alert_id
    
    def process_queue(self) -> Dict[str, int]:
        """Process all queued alerts"""
        results = {
            "processed": 0,
            "failed": 0,
            "queued": 0
        }
        
        for alert in self.alerts_queue:
            if alert["status"] == "pending":
                if self.process_alert(alert):
                    alert["status"] = "sent"
                    results["processed"] += 1
                else:
                    alert["retry_count"] += 1
                    if alert["retry_count"] >= self.config.get("retry_attempts", 3):
                        alert["status"] = "failed"
                        results["failed"] += 1
                    else:
                        results["queued"] += 1
        
        self.save_queue()
        return results
    
    def _log_notification(self, log_entry: Dict):
        """Log notification"""
        self.notification_log.append({
            **log_entry,
            "logged_at": datetime.utcnow().isoformat()
        })
        self.save_logs()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get notification system stats"""
        return {
            "total_notifications": len(self.notification_log),
            "queued_alerts": len([a for a in self.alerts_queue if a["status"] == "pending"]),
            "sent_alerts": len([a for a in self.alerts_queue if a["status"] == "sent"]),
            "failed_alerts": len([a for a in self.alerts_queue if a["status"] == "failed"]),
            "critical_alerts": len([a for a in self.alerts_queue if a["severity"] == "critical"]),
            "config": self.config
        }
    
    def run(self):
        """Execute notification engine"""
        print("\n🚀 DBOS Notification Engine\n")
        
        # Process queue
        results = self.process_queue()
        
        print(f"✓ Processed: {results['processed']} alerts")
        print(f"✓ Failed: {results['failed']} alerts")
        print(f"✓ Queued: {results['queued']} alerts")
        
        # Print stats
        stats = self.get_stats()
        print(f"\n📊 Notification Stats:")
        print(f"  Total Notifications: {stats['total_notifications']}")
        print(f"  Queued: {stats['queued_alerts']}")
        print(f"  Sent: {stats['sent_alerts']}")
        print(f"  Failed: {stats['failed_alerts']}")
        print(f"  Critical: {stats['critical_alerts']}")
        
        print("\n✅ Notification engine complete!\n")

if __name__ == '__main__':
    engine = NotificationEngine()
    engine.run()
