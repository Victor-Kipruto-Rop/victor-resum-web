#!/usr/bin/env python3
"""
DBOS Webhook Event Handler
Receives events from external sources and triggers notifications
"""

import json
import hmac
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from notification_engine import NotificationEngine

class WebhookHandler:
    """Handle incoming webhook events"""
    
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or "your_secret_key"
        self.engine = NotificationEngine()
        self.webhook_log_file = Path('notifications/webhook-events.json')
        self.webhook_log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def verify_signature(self, payload: str, signature: str) -> bool:
        """Verify webhook signature"""
        expected = hmac.new(
            self.secret_key.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected, signature)
    
    def log_webhook(self, event: Dict):
        """Log webhook event"""
        try:
            logs = []
            if self.webhook_log_file.exists():
                with open(self.webhook_log_file) as f:
                    logs = json.load(f)
            
            logs.append({
                **event,
                "logged_at": datetime.utcnow().isoformat()
            })
            
            with open(self.webhook_log_file, 'w') as f:
                json.dump(logs[-500:], f, indent=2)  # Keep last 500
        except Exception as e:
            print(f"⚠️  Failed to log webhook: {str(e)}")
    
    def handle_blog_event(self, payload: Dict) -> str:
        """Handle blog event webhook"""
        event_type = payload.get("event_type", "blog_published")
        
        if event_type == "blog_published":
            alert_id = self.engine.handle_blog_published({
                "title": payload.get("title"),
                "slug": payload.get("slug"),
                "category": payload.get("category"),
                "seo_score": payload.get("seo_score", 70)
            })
        
        elif event_type == "blog_failed":
            alert_id = self.engine.handle_blog_failed(
                payload.get("title", "Unknown"),
                payload.get("error", "Unknown error")
            )
        
        else:
            alert_id = None
        
        self.log_webhook({
            "type": "blog_event",
            "event_type": event_type,
            "status": "processed",
            "alert_id": alert_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return alert_id
    
    def handle_analytics_event(self, payload: Dict) -> str:
        """Handle analytics event webhook"""
        event_type = payload.get("event_type")
        
        if event_type == "viral_detected":
            alert_id = self.engine.handle_viral_detected({
                "title": payload.get("title"),
                "slug": payload.get("slug"),
                "views": payload.get("views"),
                "growth_rate": payload.get("growth_rate"),
                "engagement_rate": payload.get("engagement_rate"),
                "viral_score": payload.get("viral_score")
            })
        
        elif event_type == "traffic_spike":
            # Could trigger different alert
            alert_id = self.engine.queue_alert(
                "traffic_spike",
                f"Traffic Spike: {payload.get('title')}",
                f"Views: {payload.get('views')}\nSpike Factor: {payload.get('spike_factor')}x",
                "medium"
            )
        
        else:
            alert_id = None
        
        self.log_webhook({
            "type": "analytics_event",
            "event_type": event_type,
            "status": "processed",
            "alert_id": alert_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return alert_id
    
    def handle_recruiter_event(self, payload: Dict) -> str:
        """Handle recruiter event webhook"""
        alert_id = self.engine.handle_recruiter_detected({
            "company": payload.get("company"),
            "recruiter_score": payload.get("recruiter_score"),
            "tier": payload.get("tier"),
            "pages_visited": payload.get("pages_visited"),
            "time_spent_seconds": payload.get("time_spent_seconds"),
            "returning": payload.get("returning", False)
        })
        
        self.log_webhook({
            "type": "recruiter_event",
            "company": payload.get("company"),
            "status": "processed",
            "alert_id": alert_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return alert_id
    
    def handle_seo_event(self, payload: Dict) -> str:
        """Handle SEO event webhook"""
        alert_id = self.engine.handle_seo_warning({
            "post_title": payload.get("post_title"),
            "post_slug": payload.get("post_slug"),
            "seo_score": payload.get("seo_score"),
            "issue_type": payload.get("issue_type"),
            "issues": payload.get("issues", []),
            "recommendations": payload.get("recommendations", [])
        })
        
        self.log_webhook({
            "type": "seo_event",
            "seo_score": payload.get("seo_score"),
            "status": "processed",
            "alert_id": alert_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return alert_id
    
    def handle_github_actions_event(self, payload: Dict) -> str:
        """Handle GitHub Actions event webhook"""
        alert_id = self.engine.handle_github_actions_status({
            "workflow_name": payload.get("workflow_name"),
            "status": payload.get("status"),
            "duration_seconds": payload.get("duration_seconds"),
            "error_message": payload.get("error_message"),
            "timestamp": payload.get("timestamp")
        })
        
        self.log_webhook({
            "type": "github_actions_event",
            "workflow": payload.get("workflow_name"),
            "status": payload.get("status"),
            "alert_id": alert_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return alert_id
    
    def handle_health_event(self, payload: Dict) -> str:
        """Handle system health event webhook"""
        alert_id = self.engine.queue_alert(
            payload.get("event_type", "system_health"),
            payload.get("title", "System Health Alert"),
            payload.get("message", ""),
            payload.get("severity", "medium"),
            payload.get("metadata")
        )
        
        self.log_webhook({
            "type": "health_event",
            "event_type": payload.get("event_type"),
            "severity": payload.get("severity"),
            "status": "processed",
            "alert_id": alert_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return alert_id
    
    def handle_webhook(self, event_source: str, payload: Dict) -> str:
        """Route webhook to appropriate handler"""
        handlers = {
            "blog": self.handle_blog_event,
            "analytics": self.handle_analytics_event,
            "recruiter": self.handle_recruiter_event,
            "seo": self.handle_seo_event,
            "github_actions": self.handle_github_actions_event,
            "health": self.handle_health_event
        }
        
        handler = handlers.get(event_source)
        
        if handler:
            return handler(payload)
        else:
            raise ValueError(f"Unknown event source: {event_source}")
    
    def get_webhook_logs(self) -> list:
        """Get webhook event history"""
        if self.webhook_log_file.exists():
            with open(self.webhook_log_file) as f:
                return json.load(f)
        return []
    
    def get_webhook_stats(self) -> Dict[str, Any]:
        """Get webhook statistics"""
        logs = self.get_webhook_logs()
        
        stats = {
            "total_events": len(logs),
            "by_type": {},
            "by_status": {},
            "last_event": logs[-1].get("logged_at") if logs else None
        }
        
        for log in logs:
            event_type = log.get("type", "unknown")
            status = log.get("status", "unknown")
            
            stats["by_type"][event_type] = stats["by_type"].get(event_type, 0) + 1
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        return stats

# Example webhook payload formats

"""
Blog Event:
{
  "event_source": "blog",
  "event_type": "blog_published",
  "title": "Advanced Kubernetes Patterns",
  "slug": "kubernetes-patterns",
  "category": "Infrastructure",
  "seo_score": 92
}

Viral Event:
{
  "event_source": "analytics",
  "event_type": "viral_detected",
  "title": "Viral Post",
  "slug": "viral-post",
  "views": 850,
  "growth_rate": 3.2,
  "engagement_rate": 0.78,
  "viral_score": 92
}

Recruiter Event:
{
  "event_source": "recruiter",
  "event_type": "recruiter_detected",
  "company": "Google",
  "recruiter_score": 0.92,
  "tier": "FAANG",
  "pages_visited": 8,
  "time_spent_seconds": 1245,
  "returning": false
}

SEO Event:
{
  "event_source": "seo",
  "event_type": "seo_warning",
  "post_title": "Data Engineering",
  "post_slug": "data-engineering",
  "seo_score": 68,
  "issue_type": "missing_metadata",
  "issues": ["Missing alt text", "Short description"],
  "recommendations": ["Add alt text", "Expand description"]
}

GitHub Actions Event:
{
  "event_source": "github_actions",
  "event_type": "workflow_completed",
  "workflow_name": "publish-blog",
  "status": "success",
  "duration_seconds": 125,
  "timestamp": "2026-06-06T14:30:00Z"
}

Health Event:
{
  "event_source": "health",
  "event_type": "system_health",
  "title": "Broken Link Detected",
  "message": "Link /blog/posts/old-post not found",
  "severity": "medium",
  "metadata": {"link": "/blog/posts/old-post"}
}
"""

if __name__ == '__main__':
    handler = WebhookHandler()
    print("\n✅ Webhook Handler initialized")
    print("Ready to receive events!")
