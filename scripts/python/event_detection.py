#!/usr/bin/env python3
"""
DBOS Event Detection & Notification Engine
Detects blog events and triggers notifications
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
import hashlib

@dataclass
class BlogEvent:
    """Represents a blog event"""
    event_type: str  # new_post, updated_post, viral, error, etc.
    post_slug: str
    post_title: str
    timestamp: str
    category: str
    tags: List[str]
    priority: str  # low, medium, high, critical
    message: str
    recipients_count: int = 0
    notification_channels: List[str] = None

class EventDetectionEngine:
    """Detects blog events and determines notification requirements"""
    
    # Event thresholds
    VIRAL_THRESHOLD_VIEWS = 1000
    HIGH_ENGAGEMENT_CTR = 0.15  # 15% click-through rate
    SEO_CRITICAL_SCORE = 50
    
    def __init__(self):
        self.posts_file = Path("blog/assets/shared/posts.json")
        self.events_file = Path("notifications/events.json")
        self.previous_state_file = Path("notifications/.previous_state.json")
        
        self.events_file.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_state()
    
    def _initialize_state(self):
        """Initialize event tracking state"""
        if not self.events_file.exists():
            with open(self.events_file, 'w') as f:
                json.dump({"events": [], "last_check": None}, f, indent=2)
    
    def load_posts(self) -> List[Dict]:
        """Load blog posts"""
        if self.posts_file.exists():
            with open(self.posts_file) as f:
                return json.load(f)
        return []
    
    def load_previous_state(self) -> Dict:
        """Load previous blog state"""
        if self.previous_state_file.exists():
            with open(self.previous_state_file) as f:
                return json.load(f)
        return {}
    
    def save_current_state(self, posts: List[Dict]):
        """Save current blog state for next comparison"""
        state = {}
        
        for post in posts:
            state[post["slug"]] = {
                "title": post.get("title"),
                "category": post.get("category"),
                "views": post.get("views", 0),
                "engagementScore": post.get("engagementScore", 0),
                "publishDate": post.get("publishDate"),
                "updatedDate": post.get("updatedDate")
            }
        
        with open(self.previous_state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def detect_new_posts(self, current: List[Dict], previous: Dict) -> List[BlogEvent]:
        """Detect newly published posts"""
        events = []
        
        current_slugs = {p["slug"] for p in current}
        previous_slugs = set(previous.keys())
        
        new_posts = current_slugs - previous_slugs
        
        for post in current:
            if post["slug"] in new_posts and post.get("status") == "published":
                event = BlogEvent(
                    event_type="new_post",
                    post_slug=post["slug"],
                    post_title=post["title"],
                    timestamp=datetime.utcnow().isoformat(),
                    category=post.get("category", "Technology"),
                    tags=post.get("tags", []),
                    priority="medium",
                    message=f"📰 New blog post published: {post['title']}",
                    notification_channels=["email", "telegram"]
                )
                events.append(event)
        
        return events
    
    def detect_post_updates(self, current: List[Dict], previous: Dict) -> List[BlogEvent]:
        """Detect updated posts"""
        events = []
        
        for post in current:
            slug = post["slug"]
            
            if slug in previous:
                prev_state = previous[slug]
                current_updated = post.get("updatedDate")
                prev_updated = prev_state.get("updatedDate")
                
                # Check if post was significantly updated
                if current_updated and prev_updated and current_updated > prev_updated:
                    event = BlogEvent(
                        event_type="post_updated",
                        post_slug=slug,
                        post_title=post["title"],
                        timestamp=datetime.utcnow().isoformat(),
                        category=post.get("category", "Technology"),
                        tags=post.get("tags", []),
                        priority="low",
                        message=f"📝 Blog post updated: {post['title']}",
                        notification_channels=["email"]
                    )
                    events.append(event)
        
        return events
    
    def detect_viral_posts(self, current: List[Dict], previous: Dict) -> List[BlogEvent]:
        """Detect posts going viral"""
        events = []
        
        for post in current:
            slug = post["slug"]
            current_views = post.get("views", 0)
            
            if slug in previous:
                prev_views = previous[slug].get("views", 0)
                
                # Detect viral spike (doubled views)
                if current_views > self.VIRAL_THRESHOLD_VIEWS and current_views >= prev_views * 2:
                    event = BlogEvent(
                        event_type="viral_post",
                        post_slug=slug,
                        post_title=post["title"],
                        timestamp=datetime.utcnow().isoformat(),
                        category=post.get("category", "Technology"),
                        tags=post.get("tags", []),
                        priority="high",
                        message=f"🔥 Viral post detected: {post['title']} ({current_views} views)",
                        notification_channels=["email", "telegram"]
                    )
                    events.append(event)
        
        return events
    
    def detect_high_engagement(self, current: List[Dict], previous: Dict) -> List[BlogEvent]:
        """Detect posts with high engagement"""
        events = []
        
        for post in current:
            slug = post["slug"]
            engagement = post.get("engagementScore", 0)
            
            if slug in previous:
                prev_engagement = previous[slug].get("engagementScore", 0)
                
                # Large engagement increase
                if engagement > prev_engagement * 1.5 and engagement > 100:
                    event = BlogEvent(
                        event_type="high_engagement",
                        post_slug=slug,
                        post_title=post["title"],
                        timestamp=datetime.utcnow().isoformat(),
                        category=post.get("category", "Technology"),
                        tags=post.get("tags", []),
                        priority="medium",
                        message=f"📈 High engagement detected: {post['title']} (score: {engagement})",
                        notification_channels=["telegram"]
                    )
                    events.append(event)
        
        return events
    
    def detect_trending_posts(self, current: List[Dict]) -> List[BlogEvent]:
        """Detect trending posts"""
        events = []
        
        trending_posts = [p for p in current if p.get("trending", False)]
        
        for post in trending_posts:
            event = BlogEvent(
                event_type="trending_post",
                post_slug=post["slug"],
                post_title=post["title"],
                timestamp=datetime.utcnow().isoformat(),
                category=post.get("category", "Technology"),
                tags=post.get("tags", []),
                priority="medium",
                message=f"🚀 Trending post: {post['title']}",
                notification_channels=["telegram"]
            )
            events.append(event)
        
        return events
    
    def detect_all_events(self) -> List[BlogEvent]:
        """Detect all blog events"""
        print("🔍 Detecting blog events...\n")
        
        current_posts = self.load_posts()
        previous_state = self.load_previous_state()
        
        all_events = []
        
        # Run all detection methods
        detectors = [
            ("New Posts", self.detect_new_posts),
            ("Post Updates", self.detect_post_updates),
            ("Viral Posts", self.detect_viral_posts),
            ("High Engagement", self.detect_high_engagement),
            ("Trending Posts", self.detect_trending_posts)
        ]
        
        for detector_name, detector_func in detectors:
            if detector_name == "Trending Posts":
                events = detector_func(current_posts)
            else:
                events = detector_func(current_posts, previous_state)
            
            if events:
                print(f"✓ {detector_name}: {len(events)} detected")
                all_events.extend(events)
        
        # Save current state for next run
        self.save_current_state(current_posts)
        
        return all_events
    
    def dedup_events(self, events: List[BlogEvent]) -> List[BlogEvent]:
        """Remove duplicate events"""
        seen = set()
        deduped = []
        
        for event in events:
            # Create event hash
            event_hash = hashlib.sha256(
                f"{event.event_type}:{event.post_slug}:{event.timestamp}".encode()
            ).hexdigest()
            
            if event_hash not in seen:
                seen.add(event_hash)
                deduped.append(event)
        
        return deduped
    
    def save_events(self, events: List[BlogEvent]):
        """Save detected events"""
        with open(self.events_file) as f:
            data = json.load(f)
        
        # Convert events to dict
        events_dict = []
        for event in events:
            events_dict.append({
                "event_type": event.event_type,
                "post_slug": event.post_slug,
                "post_title": event.post_title,
                "timestamp": event.timestamp,
                "category": event.category,
                "tags": event.tags,
                "priority": event.priority,
                "message": event.message,
                "notification_channels": event.notification_channels or [],
                "status": "pending"
            })
        
        data["events"] = events_dict
        data["last_check"] = datetime.utcnow().isoformat()
        
        with open(self.events_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_event_report(self, events: List[BlogEvent]) -> str:
        """Generate event report"""
        report = f"""
📡 EVENT DETECTION REPORT

Total Events: {len(events)}

Events by Type:
"""
        
        type_counts = {}
        for event in events:
            event_type = event.event_type.replace("_", " ").title()
            type_counts[event_type] = type_counts.get(event_type, 0) + 1
        
        for event_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"  • {event_type}: {count}\n"
        
        report += f"\nEvents by Priority:\n"
        priority_counts = {}
        for event in events:
            priority = event.priority.capitalize()
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        for priority in ["Critical", "High", "Medium", "Low"]:
            count = priority_counts.get(priority, 0)
            if count > 0:
                report += f"  • {priority}: {count}\n"
        
        return report
    
    def run(self):
        """Execute event detection"""
        print("\n" + "="*60)
        print("📡 DBOS EVENT DETECTION ENGINE")
        print("="*60 + "\n")
        
        # Detect events
        events = self.detect_all_events()
        
        if events:
            print()
            # Dedup events
            events = self.dedup_events(events)
            
            # Save events
            self.save_events(events)
            
            # Generate report
            report = self.generate_event_report(events)
            print(report)
            
            print(f"\n✓ Events saved: {self.events_file}")
            print(f"✅ Event detection complete! {len(events)} events ready for notification\n")
        else:
            print("✓ No new events detected\n")

if __name__ == '__main__':
    engine = EventDetectionEngine()
    engine.run()
