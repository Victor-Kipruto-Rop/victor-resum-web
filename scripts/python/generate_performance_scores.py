#!/usr/bin/env python3
"""
DBOS PHASE 3: Performance Scoring Engine
Classifies posts and computes success metrics
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

class PerformanceScoringEngine:
    """Score and classify posts based on performance"""
    
    def __init__(self):
        self.posts_file = Path('blog/assets/shared/posts.json')
        self.analytics_file = Path('analytics/performance.json')
        self.output_file = Path('analytics/performance-scores.json')
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.posts = []
        self.analytics = {}
    
    def load_data(self):
        """Load posts and analytics"""
        with open(self.posts_file) as f:
            self.posts = json.load(f)
        
        # Load or create analytics file
        if self.analytics_file.exists():
            with open(self.analytics_file) as f:
                self.analytics = json.load(f)
        else:
            self.analytics = {}
        
        print(f"✓ Loaded {len(self.posts)} posts")
    
    def compute_traffic_score(self, post: dict, analytics: dict) -> int:
        """Compute traffic score (0-100)"""
        views = analytics.get('views', 0)
        score = 0
        
        # Baseline (10 pts for any views)
        if views > 0:
            score += 10
        
        # Views calculation (70 pts max)
        # 100 views = 10pts, 500 = 35pts, 1000 = 50pts, 5000 = 70pts
        if views < 100:
            score += (views / 100) * 10
        elif views < 500:
            score += 10 + ((views - 100) / 400) * 25
        elif views < 1000:
            score += 35 + ((views - 500) / 500) * 15
        else:
            score += 50 + min((views - 1000) / 100 * 2, 20)
        
        # Viral bonus (20 pts)
        if views > 1000:
            score += min((views - 1000) / 1000 * 5, 20)
        
        return min(int(score), 100)
    
    def compute_engagement_score(self, analytics: dict) -> int:
        """Compute engagement score (0-100)"""
        score = 0
        
        # Scroll depth (40 pts)
        scroll_depth = analytics.get('avgScrollDepth', 0)
        if scroll_depth > 75:
            score += 40
        elif scroll_depth > 50:
            score += 30
        elif scroll_depth > 25:
            score += 15
        
        # Time on page (30 pts) - target 8+ minutes
        time_on_page = analytics.get('avgTimeOnPage', 0)  # in seconds
        minutes = time_on_page / 60
        if minutes > 8:
            score += 30
        elif minutes > 5:
            score += 20
        elif minutes > 2:
            score += 10
        
        # CTA clicks (30 pts)
        ctr = analytics.get('ctr', 0)  # Click-through rate
        if ctr > 0.05:  # 5%
            score += 30
        elif ctr > 0.03:
            score += 20
        elif ctr > 0.01:
            score += 10
        
        return min(score, 100)
    
    def compute_conversion_score(self, analytics: dict) -> int:
        """Compute conversion score (0-100)"""
        score = 0
        
        # GitHub clicks
        gh_clicks = analytics.get('githubClicks', 0)
        score += min(gh_clicks * 5, 30)
        
        # LinkedIn clicks
        li_clicks = analytics.get('linkedinClicks', 0)
        score += min(li_clicks * 3, 30)
        
        # CV downloads
        cv_downloads = analytics.get('cvDownloads', 0)
        score += min(cv_downloads * 10, 40)
        
        return min(score, 100)
    
    def compute_recruiter_score(self, post: dict, analytics: dict) -> int:
        """Compute recruiter interest score (0-100)"""
        score = 50  # Base score
        
        # Topic relevance
        category = post.get('category', '')
        high_value_categories = ['Data Engineering', 'Infrastructure', 'System Design']
        if category in high_value_categories:
            score += 20
        
        # Difficulty level adds credibility
        difficulty_map = {'Advanced': 30, 'Intermediate': 15, 'Beginner': 5}
        for diff, points in difficulty_map.items():
            if any(diff.lower() in tag.lower() for tag in post.get('tags', [])):
                score += points
                break
        
        # Views indicate relevance
        views = analytics.get('views', 0)
        if views > 500:
            score += 10
        
        return min(score, 100)
    
    def classify_post(self, post: dict, scores: dict) -> str:
        """Classify post based on scores"""
        traffic = scores['traffic']
        engagement = scores['engagement']
        views = scores.get('views', 0)
        
        # Viral
        if views > 1000 and traffic > 70:
            return 'Viral'
        
        # High performing
        if traffic > 60 and engagement > 70:
            return 'High Performing'
        
        # Evergreen (consistent performance)
        if traffic > 40 and engagement > 60:
            return 'Evergreen'
        
        # Medium performing
        if traffic > 30 and engagement > 40:
            return 'Medium Performing'
        
        # Failing
        return 'Failing'
    
    def generate_scores(self):
        """Generate performance scores for all posts"""
        scores_data = []
        
        for post in self.posts:
            if post.get('status') != 'published':
                continue
            
            slug = post['slug']
            analytics = self.analytics.get(slug, {})
            
            # Compute scores
            traffic_score = self.compute_traffic_score(post, analytics)
            engagement_score = self.compute_engagement_score(analytics)
            conversion_score = self.compute_conversion_score(analytics)
            recruiter_score = self.compute_recruiter_score(post, analytics)
            
            # Overall score (weighted average)
            overall_score = int(
                traffic_score * 0.3 +
                engagement_score * 0.3 +
                conversion_score * 0.2 +
                recruiter_score * 0.2
            )
            
            classification = self.classify_post(post, {
                'traffic': traffic_score,
                'engagement': engagement_score,
                'views': analytics.get('views', 0)
            })
            
            score_entry = {
                "slug": slug,
                "title": post['title'],
                "category": post.get('category'),
                "publishDate": post['publishDate'],
                "scores": {
                    "overall": overall_score,
                    "traffic": traffic_score,
                    "engagement": engagement_score,
                    "conversion": conversion_score,
                    "recruiter": recruiter_score
                },
                "analytics": {
                    "views": analytics.get('views', 0),
                    "avgScrollDepth": analytics.get('avgScrollDepth', 0),
                    "avgTimeOnPage": analytics.get('avgTimeOnPage', 0),
                    "ctr": analytics.get('ctr', 0)
                },
                "classification": classification,
                "recommendations": self.generate_recommendations(
                    post, traffic_score, engagement_score, conversion_score
                )
            }
            
            scores_data.append(score_entry)
        
        # Sort by overall score
        scores_data.sort(key=lambda x: x['scores']['overall'], reverse=True)
        
        # Save scores
        with open(self.output_file, 'w') as f:
            json.dump(scores_data, f, indent=2)
        
        print(f"✓ Generated performance scores for {len(scores_data)} posts")
        
        # Print summary
        print("\n📊 Performance Summary:")
        viral = [s for s in scores_data if s['classification'] == 'Viral']
        high_perf = [s for s in scores_data if s['classification'] == 'High Performing']
        failing = [s for s in scores_data if s['classification'] == 'Failing']
        
        print(f"  Viral: {len(viral)}")
        print(f"  High Performing: {len(high_perf)}")
        print(f"  Failing: {len(failing)}")
    
    def generate_recommendations(self, post: dict, traffic: int, engagement: int, conversion: int) -> list:
        """Generate recommendations based on scores"""
        recs = []
        
        if traffic < 30:
            recs.append("Low traffic - Consider SEO optimization and promotion")
        
        if engagement < 40:
            recs.append("Low engagement - Add more visuals or restructure content")
        
        if conversion < 20:
            recs.append("Low conversions - Improve CTAs and add more links")
        
        if not recs:
            recs.append("Strong performance - Consider repurposing into other formats")
        
        return recs
    
    def run(self):
        """Execute performance scoring"""
        print("\n🚀 DBOS PHASE 3: Performance Scoring Engine\n")
        self.load_data()
        self.generate_scores()
        print("\n✅ Performance scoring complete!\n")

if __name__ == '__main__':
    engine = PerformanceScoringEngine()
    engine.run()
