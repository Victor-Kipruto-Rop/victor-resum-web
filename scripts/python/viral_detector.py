#!/usr/bin/env python3
"""
DBOS Viral Detection Engine
Detects viral and high-performing content
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List

class ViralDetector:
    """Detect viral content patterns"""
    
    def __init__(self):
        self.performance_file = Path('analytics/performance-scores.json')
        self.viral_history_file = Path('analytics/viral-history.json')
        self.viral_history = self.load_viral_history()
        
        # Thresholds
        self.thresholds = {
            "viral_views_24h": 500,
            "viral_growth_rate": 2.0,  # 2x
            "viral_engagement": 0.75,  # 75%+
            "high_performer_views": 300,
            "high_performer_engagement": 0.60,
        }
    
    def load_viral_history(self) -> Dict:
        """Load viral detection history"""
        if self.viral_history_file.exists():
            with open(self.viral_history_file) as f:
                return json.load(f)
        return {"viral_posts": [], "high_performers": []}
    
    def save_viral_history(self):
        """Save viral detection history"""
        with open(self.viral_history_file, 'w') as f:
            json.dump(self.viral_history, f, indent=2)
    
    def analyze_post_performance(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze post for viral characteristics"""
        analysis = {
            "slug": post.get("slug"),
            "title": post.get("title"),
            "views": post.get("views", 0),
            "engagement_score": post.get("engagementScore", 0),
            "category": post.get("category"),
            "publish_date": post.get("publishDate"),
            "is_viral": False,
            "is_high_performer": False,
            "viral_score": 0,
            "growth_indicators": {},
            "recommendations": []
        }
        
        views = analysis["views"]
        engagement = analysis["engagement_score"] / 100 if analysis["engagement_score"] else 0
        
        # Calculate age (days since publish)
        pub_date = datetime.fromisoformat(post.get("publishDate", "").replace('Z', '+00:00'))
        days_old = (datetime.utcnow().replace(tzinfo=pub_date.tzinfo) - pub_date).days
        
        # Estimate 24h growth rate
        growth_rate = self._estimate_growth_rate(views, days_old)
        analysis["growth_indicators"]["estimated_24h_rate"] = growth_rate
        
        # Viral detection
        if views > self.thresholds["viral_views_24h"] and growth_rate > self.thresholds["viral_growth_rate"]:
            analysis["is_viral"] = True
            analysis["viral_score"] = self._calculate_viral_score(views, growth_rate, engagement)
            analysis["recommendations"].append("🔥 VIRAL MOMENTUM - Consider amplifying on social media")
        
        # High performer detection
        elif views > self.thresholds["high_performer_views"] and engagement > self.thresholds["high_performer_engagement"]:
            analysis["is_high_performer"] = True
            analysis["viral_score"] = self._calculate_viral_score(views, growth_rate, engagement)
            analysis["recommendations"].append("⭐ High performer - Potential for growth")
        
        # Growth tracking
        analysis["growth_indicators"]["current_views"] = views
        analysis["growth_indicators"]["engagement_rate"] = engagement
        analysis["growth_indicators"]["traffic_quality"] = self._assess_traffic_quality(engagement)
        
        return analysis
    
    def _estimate_growth_rate(self, views: int, days_old: int) -> float:
        """Estimate 24h growth rate"""
        if days_old <= 0:
            days_old = 1
        
        # Average views per day
        avg_per_day = views / max(1, days_old)
        
        # If very new (< 2 days), assume current growth rate
        if days_old <= 2:
            return avg_per_day / max(1, avg_per_day / 2)
        
        return avg_per_day / max(1, views / (days_old * 2))
    
    def _calculate_viral_score(self, views: int, growth_rate: float, engagement: float) -> int:
        """Calculate viral score 0-100"""
        score = 0
        
        # Views component (40 points)
        if views > 1000:
            score += 40
        elif views > 500:
            score += 30
        elif views > 300:
            score += 20
        
        # Growth rate component (40 points)
        if growth_rate > 5.0:
            score += 40
        elif growth_rate > 3.0:
            score += 30
        elif growth_rate > 2.0:
            score += 20
        
        # Engagement component (20 points)
        if engagement > 0.8:
            score += 20
        elif engagement > 0.7:
            score += 15
        elif engagement > 0.6:
            score += 10
        
        return min(score, 100)
    
    def _assess_traffic_quality(self, engagement_rate: float) -> str:
        """Assess quality of traffic"""
        if engagement_rate > 0.8:
            return "Excellent"
        elif engagement_rate > 0.6:
            return "Good"
        elif engagement_rate > 0.4:
            return "Fair"
        else:
            return "Poor"
    
    def detect_viral_posts(self, posts: List[Dict]) -> Dict[str, Any]:
        """Detect all viral posts in current data"""
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "viral_posts": [],
            "high_performers": [],
            "growth_tracking": [],
            "alerts": []
        }
        
        for post in posts:
            if post.get("status") != "published":
                continue
            
            analysis = self.analyze_post_performance(post)
            results["growth_tracking"].append(analysis)
            
            if analysis["is_viral"]:
                results["viral_posts"].append(analysis)
                results["alerts"].append({
                    "type": "viral_detected",
                    "title": analysis["title"],
                    "views": analysis["views"],
                    "viral_score": analysis["viral_score"],
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            elif analysis["is_high_performer"]:
                results["high_performers"].append(analysis)
        
        # Check for returning viral posts (previously detected)
        for viral_post in results["viral_posts"]:
            slug = viral_post["slug"]
            for historic in self.viral_history.get("viral_posts", []):
                if historic.get("slug") == slug:
                    results["alerts"].append({
                        "type": "viral_sustained",
                        "title": viral_post["title"],
                        "view_increase": viral_post["views"] - historic.get("views", 0),
                        "timestamp": datetime.utcnow().isoformat()
                    })
        
        # Update history
        self.viral_history["viral_posts"] = results["viral_posts"]
        self.viral_history["high_performers"] = results["high_performers"]
        self.viral_history["last_check"] = datetime.utcnow().isoformat()
        self.save_viral_history()
        
        return results
    
    def get_viral_metrics(self) -> Dict[str, Any]:
        """Get viral detection metrics"""
        return {
            "viral_threshold_views_24h": self.thresholds["viral_views_24h"],
            "viral_threshold_growth": self.thresholds["viral_growth_rate"],
            "high_performer_threshold_views": self.thresholds["high_performer_views"],
            "high_performer_threshold_engagement": self.thresholds["high_performer_engagement"],
            "current_viral_posts": len(self.viral_history.get("viral_posts", [])),
            "current_high_performers": len(self.viral_history.get("high_performers", []))
        }
    
    def generate_viral_report(self) -> Dict[str, Any]:
        """Generate comprehensive viral detection report"""
        history = self.viral_history
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "title": "Viral Detection Report",
            "summary": {
                "viral_posts": len(history.get("viral_posts", [])),
                "high_performers": len(history.get("high_performers", [])),
                "last_check": history.get("last_check")
            },
            "viral_posts": history.get("viral_posts", []),
            "high_performers": history.get("high_performers", []),
            "top_viral": sorted(
                history.get("viral_posts", []),
                key=lambda x: x.get("viral_score", 0),
                reverse=True
            )[:5],
            "recommendations": self._generate_recommendations(history)
        }
    
    def _generate_recommendations(self, history: Dict) -> List[str]:
        """Generate recommendations based on viral data"""
        recommendations = []
        
        viral_count = len(history.get("viral_posts", []))
        high_performer_count = len(history.get("high_performers", []))
        
        if viral_count > 0:
            recommendations.append(f"🔥 {viral_count} viral post(s) detected - Amplify on social media")
        
        if high_performer_count > 3:
            recommendations.append("⭐ Multiple high performers - Consider content series")
        
        if viral_count == 0 and high_performer_count == 0:
            recommendations.append("💡 No viral content yet - Focus on engagement optimization")
        
        return recommendations
    
    def run(self):
        """Execute viral detection"""
        print("\n🚀 DBOS Viral Detection Engine\n")
        
        if not self.performance_file.exists():
            print("⚠️  Performance data not found. Run performance scorer first.")
            return
        
        with open(self.performance_file) as f:
            posts = json.load(f)
        
        results = self.detect_viral_posts(posts)
        
        print(f"✓ Detected {len(results['viral_posts'])} viral posts")
        print(f"✓ Detected {len(results['high_performers'])} high performers")
        print(f"✓ Found {len(results['alerts'])} alerts")
        
        # Save results
        output_file = Path('analytics/viral-analysis.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Generate report
        report = self.generate_viral_report()
        report_file = Path('analytics/viral-report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Saved viral analysis: {output_file}")
        print(f"✓ Saved viral report: {report_file}")
        print("\n✅ Viral detection complete!\n")

if __name__ == '__main__':
    detector = ViralDetector()
    detector.run()
