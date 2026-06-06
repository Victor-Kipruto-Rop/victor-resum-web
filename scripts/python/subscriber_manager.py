#!/usr/bin/env python3
"""
DBOS Subscriber Management System
Manages subscribers across multiple channels (Email, Telegram, RSS)
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class SubscriberStatus(Enum):
    """Subscriber status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNSUBSCRIBED = "unsubscribed"
    BOUNCED = "bounced"

class SubscriptionType(Enum):
    """Subscription channel"""
    EMAIL = "email"
    TELEGRAM = "telegram"
    RSS = "rss"

@dataclass
class Subscriber:
    """Subscriber profile"""
    id: str
    subscription_type: str
    contact: str  # email, telegram_id, or RSS feed URL
    subscribed_at: str
    status: str
    interests: List[str]  # Tags/categories of interest
    engagement_level: str  # active, moderate, inactive
    preferences: Dict
    metadata: Dict

class SubscriberManager:
    """Manages subscriber database and operations"""
    
    def __init__(self):
        self.subscribers_dir = Path("subscribers")
        self.subscribers_dir.mkdir(exist_ok=True)
        
        self.email_file = self.subscribers_dir / "email.json"
        self.telegram_file = self.subscribers_dir / "telegram.json"
        self.rss_file = self.subscribers_dir / "rss.json"
        self.segments_file = self.subscribers_dir / "segments.json"
        self.stats_file = self.subscribers_dir / "stats.json"
        
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize subscriber files if they don't exist"""
        for file_path in [self.email_file, self.telegram_file, self.rss_file]:
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump({"subscribers": [], "last_updated": datetime.utcnow().isoformat()}, f, indent=2)
    
    def add_email_subscriber(self, email: str, interests: List[str] = None) -> bool:
        """Add email subscriber"""
        with open(self.email_file) as f:
            data = json.load(f)
        
        # Check if already exists
        if any(s["contact"] == email for s in data["subscribers"]):
            return False
        
        subscriber = {
            "id": self._generate_id(email),
            "contact": email,
            "subscribed_at": datetime.utcnow().isoformat(),
            "status": "active",
            "interests": interests or [],
            "engagement_level": "moderate",
            "preferences": {
                "digest_frequency": "weekly",
                "allow_marketing": True,
                "allow_weekly_digest": True
            },
            "metadata": {
                "source": "manual",
                "last_opened": None,
                "total_opens": 0,
                "total_clicks": 0
            }
        }
        
        data["subscribers"].append(subscriber)
        data["last_updated"] = datetime.utcnow().isoformat()
        
        with open(self.email_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    
    def add_telegram_subscriber(self, chat_id: str, username: str = None, interests: List[str] = None) -> bool:
        """Add Telegram subscriber"""
        with open(self.telegram_file) as f:
            data = json.load(f)
        
        if any(s["contact"] == str(chat_id) for s in data["subscribers"]):
            return False
        
        subscriber = {
            "id": self._generate_id(f"tg_{chat_id}"),
            "contact": str(chat_id),
            "username": username,
            "subscribed_at": datetime.utcnow().isoformat(),
            "status": "active",
            "interests": interests or [],
            "engagement_level": "active",
            "preferences": {
                "message_frequency": "instant",
                "digest_enabled": False
            },
            "metadata": {
                "total_messages_sent": 0,
                "total_clicks": 0,
                "last_interaction": datetime.utcnow().isoformat()
            }
        }
        
        data["subscribers"].append(subscriber)
        data["last_updated"] = datetime.utcnow().isoformat()
        
        with open(self.telegram_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    
    def get_all_subscribers(self) -> Dict[str, List]:
        """Get all subscribers by type"""
        subscribers = {}
        
        for sub_type, file_path in [("email", self.email_file), ("telegram", self.telegram_file)]:
            with open(file_path) as f:
                data = json.load(f)
            subscribers[sub_type] = data["subscribers"]
        
        return subscribers
    
    def get_active_subscribers(self) -> Dict[str, List]:
        """Get only active subscribers"""
        all_subs = self.get_all_subscribers()
        active = {}
        
        for sub_type, subscribers in all_subs.items():
            active[sub_type] = [s for s in subscribers if s["status"] == "active"]
        
        return active
    
    def get_subscribers_by_interest(self, interest: str) -> Dict[str, List]:
        """Get subscribers interested in specific topic"""
        all_subs = self.get_all_subscribers()
        filtered = {}
        
        for sub_type, subscribers in all_subs.items():
            filtered[sub_type] = [
                s for s in subscribers 
                if interest.lower() in [i.lower() for i in s.get("interests", [])]
            ]
        
        return filtered
    
    def _generate_id(self, unique_str: str) -> str:
        """Generate subscriber ID"""
        return hashlib.sha256(unique_str.encode()).hexdigest()[:16]
    
    def update_subscriber_status(self, contact: str, status: str, sub_type: str = "email") -> bool:
        """Update subscriber status"""
        file_path = self.email_file if sub_type == "email" else self.telegram_file
        
        with open(file_path) as f:
            data = json.load(f)
        
        for subscriber in data["subscribers"]:
            if subscriber["contact"] == contact:
                subscriber["status"] = status
                data["last_updated"] = datetime.utcnow().isoformat()
                
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                return True
        
        return False
    
    def update_subscriber_engagement(self, contact: str, engagement_level: str, sub_type: str = "email") -> bool:
        """Update engagement level"""
        file_path = self.email_file if sub_type == "email" else self.telegram_file
        
        with open(file_path) as f:
            data = json.load(f)
        
        for subscriber in data["subscribers"]:
            if subscriber["contact"] == contact:
                subscriber["engagement_level"] = engagement_level
                data["last_updated"] = datetime.utcnow().isoformat()
                
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                return True
        
        return False
    
    def update_subscriber_interests(self, contact: str, interests: List[str], sub_type: str = "email") -> bool:
        """Update subscriber interests"""
        file_path = self.email_file if sub_type == "email" else self.telegram_file
        
        with open(file_path) as f:
            data = json.load(f)
        
        for subscriber in data["subscribers"]:
            if subscriber["contact"] == contact:
                subscriber["interests"] = interests
                data["last_updated"] = datetime.utcnow().isoformat()
                
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                return True
        
        return False
    
    def get_subscriber_stats(self) -> Dict:
        """Get subscriber statistics"""
        all_subs = self.get_all_subscribers()
        
        stats = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_subscribers": 0,
            "by_type": {},
            "by_status": {},
            "by_engagement": {}
        }
        
        for sub_type, subscribers in all_subs.items():
            stats["by_type"][sub_type] = len(subscribers)
            stats["total_subscribers"] += len(subscribers)
            
            for subscriber in subscribers:
                status = subscriber.get("status", "unknown")
                engagement = subscriber.get("engagement_level", "unknown")
                
                stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
                stats["by_engagement"][engagement] = stats["by_engagement"].get(engagement, 0) + 1
        
        return stats
    
    def save_stats(self):
        """Save statistics"""
        stats = self.get_subscriber_stats()
        
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def export_email_list(self) -> List[str]:
        """Export all active email addresses"""
        with open(self.email_file) as f:
            data = json.load(f)
        
        return [
            s["contact"] for s in data["subscribers"] 
            if s["status"] == "active"
        ]
    
    def export_telegram_ids(self) -> List[str]:
        """Export all active Telegram chat IDs"""
        with open(self.telegram_file) as f:
            data = json.load(f)
        
        return [
            s["contact"] for s in data["subscribers"] 
            if s["status"] == "active"
        ]
    
    def generate_report(self) -> str:
        """Generate subscriber report"""
        stats = self.get_subscriber_stats()
        all_subs = self.get_all_subscribers()
        
        report = f"""
📊 SUBSCRIBER MANAGEMENT REPORT

Timestamp: {stats['timestamp']}

Summary:
  • Total Subscribers: {stats['total_subscribers']}

By Subscription Type:
"""
        
        for sub_type, count in stats['by_type'].items():
            report += f"  • {sub_type.capitalize()}: {count}\n"
        
        report += f"\nBy Status:\n"
        for status, count in stats['by_status'].items():
            report += f"  • {status.capitalize()}: {count}\n"
        
        report += f"\nBy Engagement Level:\n"
        for engagement, count in stats['by_engagement'].items():
            report += f"  • {engagement.capitalize()}: {count}\n"
        
        # Top interests
        all_interests = {}
        for sub_type, subscribers in all_subs.items():
            for subscriber in subscribers:
                for interest in subscriber.get("interests", []):
                    all_interests[interest] = all_interests.get(interest, 0) + 1
        
        if all_interests:
            report += f"\nTop Interests:\n"
            for interest, count in sorted(all_interests.items(), key=lambda x: x[1], reverse=True)[:5]:
                report += f"  • {interest}: {count} subscribers\n"
        
        return report
    
    def run(self):
        """Execute subscriber management"""
        print("\n" + "="*60)
        print("📊 DBOS SUBSCRIBER MANAGER")
        print("="*60 + "\n")
        
        # Generate and print report
        report = self.generate_report()
        print(report)
        
        # Save stats
        self.save_stats()
        print(f"\n✓ Subscriber stats saved: {self.stats_file}")
        print("\n✅ Subscriber management complete!\n")

if __name__ == '__main__':
    manager = SubscriberManager()
    manager.run()
