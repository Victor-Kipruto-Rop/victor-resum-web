#!/usr/bin/env python3
"""
DBOS Subscriber Segmentation Engine
Segments subscribers by interests, engagement, and preferences
"""

import json
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime

class SubscriberSegmentationEngine:
    """Segments subscribers into groups for targeted notifications"""
    
    # Predefined technology interest groups
    TECHNOLOGY_SEGMENTS = {
        "Python Developers": {
            "keywords": ["python", "backend", "django", "flask", "fastapi"],
            "category": "Programming Language"
        },
        "Data Engineers": {
            "keywords": ["data", "etl", "airflow", "pipelines", "dbt", "sql", "warehouse"],
            "category": "Data Engineering"
        },
        "DevOps Engineers": {
            "keywords": ["devops", "kubernetes", "docker", "ci/cd", "terraform", "infrastructure"],
            "category": "Infrastructure"
        },
        "AI/ML Enthusiasts": {
            "keywords": ["ai", "ml", "neural", "nlp", "deep-learning", "tensorflow", "pytorch"],
            "category": "AI/ML"
        },
        "Cloud Architects": {
            "keywords": ["cloud", "aws", "gcp", "azure", "serverless", "lambda"],
            "category": "Cloud"
        },
        "API Developers": {
            "keywords": ["api", "rest", "graphql", "microservices", "integration"],
            "category": "APIs"
        },
        "Database Specialists": {
            "keywords": ["sql", "database", "postgres", "mongodb", "elasticsearch"],
            "category": "Databases"
        },
        "Testing & QA": {
            "keywords": ["testing", "qa", "pytest", "quality", "validation"],
            "category": "Testing"
        }
    }
    
    def __init__(self):
        self.subscribers_dir = Path("subscribers")
        self.subscribers_dir.mkdir(exist_ok=True)
        
        self.email_file = self.subscribers_dir / "email.json"
        self.telegram_file = self.subscribers_dir / "telegram.json"
        self.segments_file = self.subscribers_dir / "segments.json"
    
    def load_subscribers(self) -> Dict:
        """Load all subscribers"""
        subscribers = {
            "email": [],
            "telegram": []
        }
        
        if self.email_file.exists():
            with open(self.email_file) as f:
                subscribers["email"] = json.load(f).get("subscribers", [])
        
        if self.telegram_file.exists():
            with open(self.telegram_file) as f:
                subscribers["telegram"] = json.load(f).get("subscribers", [])
        
        return subscribers
    
    def segment_by_interest(self, subscribers: Dict) -> Dict[str, Dict]:
        """Segment subscribers by technology interests"""
        segments = {}
        
        # Initialize segments
        for segment_name in self.TECHNOLOGY_SEGMENTS.keys():
            segments[segment_name] = {
                "email": [],
                "telegram": [],
                "total": 0
            }
        
        # Also create catch-all segment
        segments["General Tech"] = {
            "email": [],
            "telegram": [],
            "total": 0
        }
        
        # Segment each subscriber
        for sub_type, subs_list in subscribers.items():
            for subscriber in subs_list:
                interests = subscriber.get("interests", [])
                assigned = False
                
                # Try to match to technology segment
                for segment_name, segment_info in self.TECHNOLOGY_SEGMENTS.items():
                    keywords = segment_info["keywords"]
                    
                    # Check if any interest matches
                    if any(
                        interest.lower() in keywords or
                        any(kw in interest.lower() for kw in keywords)
                        for interest in interests
                    ):
                        segments[segment_name][sub_type].append({
                            "contact": subscriber["contact"],
                            "interests": interests,
                            "engagement": subscriber.get("engagement_level", "moderate")
                        })
                        assigned = True
                        break
                
                # If no match, add to general tech
                if not assigned:
                    segments["General Tech"][sub_type].append({
                        "contact": subscriber["contact"],
                        "interests": interests,
                        "engagement": subscriber.get("engagement_level", "moderate")
                    })
        
        # Calculate totals
        for segment in segments.values():
            segment["total"] = len(segment["email"]) + len(segment["telegram"])
        
        return segments
    
    def segment_by_engagement(self, subscribers: Dict) -> Dict[str, Dict]:
        """Segment subscribers by engagement level"""
        segments = {
            "active": {"email": [], "telegram": [], "total": 0},
            "moderate": {"email": [], "telegram": [], "total": 0},
            "inactive": {"email": [], "telegram": [], "total": 0}
        }
        
        for sub_type, subs_list in subscribers.items():
            for subscriber in subs_list:
                engagement = subscriber.get("engagement_level", "moderate")
                
                if engagement not in segments:
                    engagement = "moderate"
                
                segments[engagement][sub_type].append({
                    "contact": subscriber["contact"],
                    "interests": subscriber.get("interests", [])
                })
        
        # Calculate totals
        for segment in segments.values():
            segment["total"] = len(segment["email"]) + len(segment["telegram"])
        
        return segments
    
    def segment_by_subscription_type(self, subscribers: Dict) -> Dict[str, Dict]:
        """Segment subscribers by subscription type"""
        segments = {
            "email_only": {"total": 0, "contacts": []},
            "telegram_only": {"total": 0, "contacts": []},
            "multi_channel": {"total": 0, "contacts": []}
        }
        
        email_subs = {s["contact"] for s in subscribers.get("email", [])}
        telegram_subs = {s["contact"] for s in subscribers.get("telegram", [])}
        
        segments["email_only"]["total"] = len(email_subs)
        segments["email_only"]["contacts"] = list(email_subs)
        
        segments["telegram_only"]["total"] = len(telegram_subs)
        segments["telegram_only"]["contacts"] = list(telegram_subs)
        
        segments["multi_channel"]["total"] = len(email_subs & telegram_subs)
        segments["multi_channel"]["contacts"] = list(email_subs & telegram_subs)
        
        return segments
    
    def create_segments(self) -> Dict:
        """Create all segment types"""
        subscribers = self.load_subscribers()
        
        segments = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_subscribers": sum(
                len(subs) for subs in subscribers.values()
            ),
            "by_interest": self.segment_by_interest(subscribers),
            "by_engagement": self.segment_by_engagement(subscribers),
            "by_subscription_type": self.segment_by_subscription_type(subscribers)
        }
        
        return segments
    
    def save_segments(self, segments: Dict):
        """Save segment data"""
        with open(self.segments_file, 'w') as f:
            json.dump(segments, f, indent=2)
    
    def get_segment(self, segment_type: str, segment_name: str) -> Dict:
        """Get specific segment"""
        with open(self.segments_file) as f:
            segments = json.load(f)
        
        return segments.get(segment_type, {}).get(segment_name, {})
    
    def get_emails_for_segment(self, segment_type: str, segment_name: str) -> List[str]:
        """Get all emails in a segment"""
        segment = self.get_segment(segment_type, segment_name)
        emails = segment.get("email", [])
        
        if isinstance(emails[0], dict):
            return [e["contact"] for e in emails]
        return emails
    
    def get_telegram_ids_for_segment(self, segment_type: str, segment_name: str) -> List[str]:
        """Get all Telegram IDs in a segment"""
        segment = self.get_segment(segment_type, segment_name)
        tg_ids = segment.get("telegram", [])
        
        if isinstance(tg_ids[0], dict):
            return [t["contact"] for t in tg_ids]
        return tg_ids
    
    def generate_segmentation_report(self, segments: Dict) -> str:
        """Generate segmentation report"""
        report = f"""
📊 SUBSCRIBER SEGMENTATION REPORT

Timestamp: {segments['timestamp']}
Total Subscribers: {segments['total_subscribers']}

BY INTEREST (Technology Focus):
"""
        
        for segment_name, segment_data in segments['by_interest'].items():
            report += f"  • {segment_name}: {segment_data['total']} ({segment_data['email']} email, {segment_data['telegram']} Telegram)\n"
        
        report += f"\nBY ENGAGEMENT LEVEL:\n"
        for engagement, segment_data in segments['by_engagement'].items():
            report += f"  • {engagement.capitalize()}: {segment_data['total']}\n"
        
        report += f"\nBY SUBSCRIPTION TYPE:\n"
        for sub_type, segment_data in segments['by_subscription_type'].items():
            report += f"  • {sub_type.replace('_', ' ').title()}: {segment_data['total']}\n"
        
        return report
    
    def run(self):
        """Execute segmentation"""
        print("\n" + "="*60)
        print("📊 DBOS SUBSCRIBER SEGMENTATION ENGINE")
        print("="*60 + "\n")
        
        # Create segments
        segments = self.create_segments()
        
        # Save segments
        self.save_segments(segments)
        
        # Generate report
        report = self.generate_segmentation_report(segments)
        print(report)
        
        print(f"\n✓ Segments saved: {self.segments_file}")
        print("\n✅ Segmentation complete!\n")

if __name__ == '__main__':
    engine = SubscriberSegmentationEngine()
    engine.run()
