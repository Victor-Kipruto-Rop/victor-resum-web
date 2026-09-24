#!/usr/bin/env python3
"""
DBOS Alert Classification Engine
Classifies events into alert types and severity levels
"""

from enum import Enum
from typing import Dict, Any, List
from datetime import datetime

class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(Enum):
    """Alert event types"""
    # Blog events
    BLOG_PUBLISHED = "blog_published"
    BLOG_UPDATED = "blog_updated"
    BLOG_FAILED = "blog_failed"
    
    # SEO events
    SEO_WARNING = "seo_warning"
    SEO_ERROR = "seo_error"
    SITEMAP_FAILED = "sitemap_failed"
    
    # Analytics events
    TRAFFIC_SPIKE = "traffic_spike"
    VIRAL_DETECTED = "viral_detected"
    HIGH_ENGAGEMENT = "high_engagement"
    
    # Recruiter events
    RECRUITER_DETECTED = "recruiter_detected"
    RECRUITER_RETURNING = "recruiter_returning"
    
    # System events
    GITHUB_ACTIONS_SUCCESS = "github_actions_success"
    GITHUB_ACTIONS_FAILED = "github_actions_failed"
    SYSTEM_ERROR = "system_error"
    HEALTH_WARNING = "health_warning"
    LINK_BROKEN = "link_broken"

class AlertClassifier:
    """Classify and categorize alerts"""
    
    def __init__(self):
        self.thresholds = {
            "viral_views_24h": 500,
            "viral_growth_rate": 2.0,  # 2x growth
            "high_engagement_rate": 0.75,  # 75%
            "seo_score_minimum": 70,
            "traffic_spike_factor": 3.0,  # 3x normal
        }
    
    def classify_blog_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Classify blog publishing event"""
        severity = AlertSeverity.LOW
        alert_type = AlertType.BLOG_PUBLISHED
        
        if event.get("status") == "failed":
            alert_type = AlertType.BLOG_FAILED
            severity = AlertSeverity.HIGH
        elif event.get("status") == "updated":
            alert_type = AlertType.BLOG_UPDATED
            severity = AlertSeverity.LOW
        
        # Check SEO score
        seo_score = event.get("seo_score", 100)
        if seo_score < self.thresholds["seo_score_minimum"]:
            severity = AlertSeverity.MEDIUM
        
        return {
            "type": alert_type.value,
            "severity": severity.value,
            "priority": self._severity_to_priority(severity),
            "message": self._generate_blog_message(event, alert_type)
        }
    
    def classify_seo_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Classify SEO event"""
        severity = AlertSeverity.LOW
        alert_type = AlertType.SEO_WARNING
        
        if event.get("issue_type") == "critical":
            severity = AlertSeverity.CRITICAL
            alert_type = AlertType.SEO_ERROR
        elif event.get("issue_type") == "missing_metadata":
            severity = AlertSeverity.MEDIUM
        
        return {
            "type": alert_type.value,
            "severity": severity.value,
            "priority": self._severity_to_priority(severity),
            "message": self._generate_seo_message(event)
        }
    
    def classify_analytics_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Classify analytics event"""
        severity = AlertSeverity.LOW
        alert_type = AlertType.HIGH_ENGAGEMENT
        
        # Check for viral
        views = event.get("views", 0)
        growth_rate = event.get("growth_rate", 1.0)
        
        if views > self.thresholds["viral_views_24h"] and growth_rate > self.thresholds["viral_growth_rate"]:
            alert_type = AlertType.VIRAL_DETECTED
            severity = AlertSeverity.HIGH
        elif event.get("traffic_spike"):
            alert_type = AlertType.TRAFFIC_SPIKE
            severity = AlertSeverity.MEDIUM
        
        engagement = event.get("engagement_rate", 0)
        if engagement > self.thresholds["high_engagement_rate"]:
            severity = max(severity, AlertSeverity.MEDIUM)
        
        return {
            "type": alert_type.value,
            "severity": severity.value,
            "priority": self._severity_to_priority(severity),
            "message": self._generate_analytics_message(event, alert_type)
        }
    
    def classify_recruiter_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Classify recruiter activity event"""
        severity = AlertSeverity.MEDIUM
        alert_type = AlertType.RECRUITER_DETECTED
        
        if event.get("returning"):
            alert_type = AlertType.RECRUITER_RETURNING
            severity = AlertSeverity.MEDIUM
        
        score = event.get("recruiter_score", 0)
        if score > 0.8:  # 80%+
            severity = AlertSeverity.HIGH
        
        return {
            "type": alert_type.value,
            "severity": severity.value,
            "priority": self._severity_to_priority(severity),
            "message": self._generate_recruiter_message(event, alert_type)
        }
    
    def classify_automation_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Classify GitHub Actions event"""
        severity = AlertSeverity.LOW
        alert_type = AlertType.GITHUB_ACTIONS_SUCCESS
        
        if event.get("status") == "failure":
            alert_type = AlertType.GITHUB_ACTIONS_FAILED
            severity = AlertSeverity.HIGH
        
        return {
            "type": alert_type.value,
            "severity": severity.value,
            "priority": self._severity_to_priority(severity),
            "message": self._generate_automation_message(event)
        }
    
    def classify_health_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Classify system health event"""
        severity = AlertSeverity.LOW
        alert_type = AlertType.HEALTH_WARNING
        
        issue_type = event.get("issue_type")
        if issue_type == "broken_link":
            alert_type = AlertType.LINK_BROKEN
            severity = AlertSeverity.MEDIUM
        elif issue_type == "missing_image":
            severity = AlertSeverity.LOW
        elif issue_type == "error":
            alert_type = AlertType.SYSTEM_ERROR
            severity = AlertSeverity.HIGH
        
        return {
            "type": alert_type.value,
            "severity": severity.value,
            "priority": self._severity_to_priority(severity),
            "message": self._generate_health_message(event)
        }
    
    def _severity_to_priority(self, severity: AlertSeverity) -> int:
        """Convert severity to priority number (1=highest)"""
        severity_map = {
            AlertSeverity.CRITICAL: 1,
            AlertSeverity.HIGH: 2,
            AlertSeverity.MEDIUM: 3,
            AlertSeverity.LOW: 4
        }
        return severity_map.get(severity, 4)
    
    def _generate_blog_message(self, event: Dict, alert_type: AlertType) -> str:
        """Generate blog event message"""
        title = event.get("title", "Unknown")
        
        if alert_type == AlertType.BLOG_PUBLISHED:
            return f"✅ Blog Published: {title}"
        elif alert_type == AlertType.BLOG_UPDATED:
            return f"🔄 Blog Updated: {title}"
        elif alert_type == AlertType.BLOG_FAILED:
            return f"❌ Blog Publishing Failed: {title}"
        return f"📝 Blog Event: {title}"
    
    def _generate_seo_message(self, event: Dict) -> str:
        """Generate SEO event message"""
        title = event.get("post_title", "Post")
        score = event.get("seo_score", 0)
        
        if score < 50:
            return f"🚨 Critical SEO Issue: {title} (Score: {score}/100)"
        elif score < 70:
            return f"⚠️ SEO Warning: {title} (Score: {score}/100)"
        return f"📊 SEO Update: {title} (Score: {score}/100)"
    
    def _generate_analytics_message(self, event: Dict, alert_type: AlertType) -> str:
        """Generate analytics event message"""
        title = event.get("post_title", "Post")
        views = event.get("views", 0)
        
        if alert_type == AlertType.VIRAL_DETECTED:
            return f"🔥 VIRAL DETECTED: {title} ({views} views in 24h)"
        elif alert_type == AlertType.TRAFFIC_SPIKE:
            return f"📈 Traffic Spike: {title} ({views} views)"
        else:
            return f"👍 High Engagement: {title} ({event.get('engagement_rate', 0):.1%})"
    
    def _generate_recruiter_message(self, event: Dict, alert_type: AlertType) -> str:
        """Generate recruiter event message"""
        company = event.get("company", "Unknown Company")
        
        if alert_type == AlertType.RECRUITER_RETURNING:
            return f"💼 Returning Recruiter: {company}"
        return f"💼 Recruiter Detected: {company}"
    
    def _generate_automation_message(self, event: Dict) -> str:
        """Generate automation event message"""
        workflow = event.get("workflow_name", "Workflow")
        
        if event.get("status") == "success":
            return f"✅ GitHub Actions Success: {workflow}"
        else:
            return f"❌ GitHub Actions Failed: {workflow}"
    
    def _generate_health_message(self, event: Dict) -> str:
        """Generate health event message"""
        issue = event.get("issue_type", "Unknown")
        detail = event.get("detail", "")
        
        if issue == "broken_link":
            return f"🔗 Broken Link Detected: {detail}"
        elif issue == "missing_image":
            return f"🖼️ Missing Image: {detail}"
        else:
            return f"⚠️ System Health: {detail}"

if __name__ == '__main__':
    classifier = AlertClassifier()
    
    # Test blog event
    blog_event = {
        "status": "published",
        "title": "Test Post",
        "seo_score": 85
    }
    print("Blog Event:", classifier.classify_blog_event(blog_event))
    
    # Test viral event
    viral_event = {
        "post_title": "Viral Post",
        "views": 750,
        "growth_rate": 2.5,
        "engagement_rate": 0.82,
        "traffic_spike": True
    }
    print("Viral Event:", classifier.classify_analytics_event(viral_event))
    
    # Test recruiter event
    recruiter_event = {
        "company": "Google",
        "recruiter_score": 0.85,
        "returning": True
    }
    print("Recruiter Event:", classifier.classify_recruiter_event(recruiter_event))
