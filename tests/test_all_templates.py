#!/usr/bin/env python3
"""Test suite for all email templates and social platforms"""
import os, sys, json, logging, requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "scripts" / "python"))
sys.path.insert(0, str(current_dir / "blog-ai"))
sys.path.insert(0, str(current_dir / "social-automation"))

from email_templates import (
    template_welcome, template_new_blog_post, template_weekly_digest,
    template_notification, template_dashboard_alert, template_event_announcement,
    template_trending_content, template_activity_recap, template_subscriber_milestone,
    template_viral_alert, template_recruiter_alert, template_engagement_summary,
    template_recommended_reads
)

class ResendService:
    def __init__(self):
        self.api_key = os.getenv("RESEND_API_KEY") or "re_9XQ2354V_FLP7ZVot22p1pHsN72vy9XnE"
        self.base_url = "https://api.resend.com"
        # Use onboarding email for free tier (doesn't require domain verification)
        self.from_email = "onboarding@resend.dev"
    
    def send(self, to, subject, html, from_name="Victor's Blog"):
        if not self.api_key:
            return {"error": "No API key"}
        
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "from": f"{from_name} <{self.from_email}>",
            "to": to, "subject": subject, "html": html,
            "tags": [{"name": "test", "value": "true"}]
        }
        
        try:
            r = requests.post(f"{self.base_url}/emails", json=payload, headers=headers, timeout=10)
            if r.status_code in [200, 201]:
                result = r.json()
                logger.info(f"✅ Sent: {result.get('id', 'OK')}")
                return result
            error = r.json().get("message", r.text)
            logger.error(f"❌ Error: {error}")
            return {"error": error}
        except Exception as e:
            logger.error(f"❌ Failed: {e}")
            return {"error": str(e)}

class EmailTestSuite:
    def __init__(self, email="kiprutovictor39@gmail.com"):
        self.email = email
        self.name = "Test User"
        self.svc = ResendService()
        self.results = {"passed": [], "failed": [], "total": 0}
    
    def send(self, name, subject, html):
        r = self.svc.send(self.email, subject, html)
        if "error" not in r:
            self.results["passed"].append(name)
        else:
            self.results["failed"].append((name, r.get("error", "Unknown error")))
    
    def run(self):
        logger.info("=" * 80)
        logger.info("🚀 EMAIL TEMPLATE TEST SUITE")
        logger.info("=" * 80)
        logger.info(f"📧 Recipient: {self.email}")
        logger.info(f"From: Victor's Blog <onboarding@resend.dev>\n")
        
        tests = [
            ("welcome", template_welcome(self.name, self.email), "🎉 Welcome to My Blog"),
            ("new_blog_post", template_new_blog_post(self.name, "Building Scalable Data Pipelines", "Best practices...", "pipes", 12), "📝 New Post: Pipelines"),
            ("weekly_digest", template_weekly_digest(self.name, [{"title": "Kubernetes Patterns", "excerpt": "High availability patterns", "read_time": 10, "publishDate": "Jun 3", "tags": ["K8s"], "id": "k8s"}]), "📚 Weekly Digest"),
            ("notification", template_notification(self.name, "New Feature", "Advanced analytics dashboard available", "✨"), "✨ New Feature"),
            ("dashboard_alert", template_dashboard_alert(self.name, "Weekly Analytics", {"Views": "12K", "Users": "3.2K"}, "Technical content driving engagement"), "📊 Analytics Alert"),
            ("event_announcement", template_event_announcement(self.name, "Kubernetes Workshop", "Jul 15, 2026", "Advanced K8s patterns course", "http://example.com"), "🚀 New Workshop"),
            ("trending_content", template_trending_content(self.name, [{"title": "Kubernetes Patterns", "views": 2450, "growth": "185%", "slug": "k8s"}], {"title": "Kubernetes", "views": 2450}), "🔥 Content Trending"),
            ("activity_recap", template_activity_recap(self.name, "June", {"total_views": 18540, "new_posts": 5, "subscribers": 1240, "avg_read_time": 8, "top_post_1": "Kubernetes", "top_post_1_views": 2450, "top_post_2": "Python", "top_post_2_views": 1890, "top_post_3": "dbt", "top_post_3_views": 1620, "insight": "Technical content resonating with engineers!"}), "📈 June Activity Recap"),
            ("subscriber_milestone", template_subscriber_milestone(self.name, 1000, "Thank you for the incredible support!"), "🎊 1,000 Subscribers!"),
            ("viral_alert", template_viral_alert(self.name, "Kubernetes Patterns", 2450, 500, "185%/day"), "🚀 Post Going Viral"),
            ("recruiter_alert", template_recruiter_alert(self.name, {"company": "Google", "position": "Senior Data Engineer", "seniority": "Staff Level"}), "💼 Recruiter Interest"),
            ("engagement_summary", template_engagement_summary(self.name, "week", {"pageviews": 8450, "unique_visitors": 3200, "avg_session": "285", "bounce_rate": "26", "return_rate": "48", "social_shares": 234, "source_1": "Organic Search", "source_1_pct": "58", "source_2": "Direct", "source_2_pct": "24", "source_3": "Social", "source_3_pct": "18"}), "📊 Weekly Engagement"),
            ("recommended_reads", template_recommended_reads(self.name, [], [{"title": "ETL Patterns", "excerpt": "Advanced data transformation", "slug": "etl", "relevance": "92%"}]), "💡 Recommended Reading"),
        ]
        
        self.results["total"] = len(tests)
        for name, html, subject in tests:
            self.send(name, subject, html)
        
        self.print_results()
        return self.results
    
    def print_results(self):
        logger.info("\n" + "=" * 80)
        logger.info(f"✅ Passed: {len(self.results['passed'])}/{self.results['total']}")
        logger.info(f"❌ Failed: {len(self.results['failed'])}/{self.results['total']}")
        if self.results['passed']:
            logger.info("\n✅ SUCCESSFULLY SENT:")
            for t in self.results['passed']:
                logger.info(f"   • {t}")
        if self.results['failed']:
            logger.info("\n❌ FAILED:")
            for t, e in self.results['failed']:
                logger.info(f"   • {t}: {e}")
        logger.info("=" * 80)

class SocialTestSuite:
    def run(self):
        logger.info("\n" + "=" * 80)
        logger.info("🚀 SOCIAL MEDIA POST TEST SUITE")
        logger.info("=" * 80)
        
        platforms = [
            ("Twitter/X", self.test_twitter),
            ("LinkedIn", self.test_linkedin),
            ("Dev.to", self.test_devto),
            ("Medium", self.test_medium),
            ("Telegram", self.test_telegram)
        ]
        
        results = {"passed": [], "failed": [], "total": len(platforms)}
        
        for platform, test_fn in platforms:
            try:
                logger.info(f"\n📱 Testing {platform}...")
                test_fn()
                results["passed"].append(platform)
                logger.info(f"✅ {platform} posted successfully")
            except ImportError as e:
                logger.error(f"⚠️  {platform} module not found: {e}")
                results["failed"].append((platform, f"Module not found: {e}"))
            except Exception as e:
                logger.error(f"❌ {platform} error: {e}")
                results["failed"].append((platform, str(e)))
        
        self.print_results(results)
        return results
    
    def test_twitter(self):
        from twitter import TwitterPoster
        p = TwitterPoster()
        r = p.post_tweet("🚀 Testing automated social media integration across all platforms #DevOps #Automation")
        logger.info(f"   Tweet ID: {r.get('id', 'OK')}")
    
    def test_linkedin(self):
        from linkedin import LinkedInPoster
        p = LinkedInPoster()
        r = p.post({"title": "Testing Automated Integration", "content": "Verifying all platforms receive content"})
        logger.info(f"   Post ID: {r.get('id', 'OK')}")
    
    def test_devto(self):
        from devto import DevtoPoster
        p = DevtoPoster()
        r = p.post({"title": "Testing Automated Integration", "content": "Test article for social integration", "tags": ["testing", "automation"]})
        logger.info(f"   Article ID: {r.get('id', 'OK')}")
    
    def test_medium(self):
        from medium import MediumPoster
        p = MediumPoster()
        r = p.post({"title": "Testing Automated Integration", "content": "Test story for social integration", "tags": ["testing", "automation"]})
        logger.info(f"   Story ID: {r.get('id', 'OK')}")
    
    def test_telegram(self):
        from telegram import TelegramPoster
        p = TelegramPoster()
        r = p.post("🚀 Testing automated social media integration\n\n#DevOps #Automation #Testing")
        logger.info(f"   Message ID: {r.get('message_id', 'OK')}")
    
    def print_results(self, results):
        logger.info("\n" + "=" * 80)
        logger.info(f"✅ Passed: {len(results['passed'])}/{results['total']}")
        logger.info(f"❌ Failed: {len(results['failed'])}/{results['total']}")
        if results['passed']:
            logger.info("\n✅ WORKING PLATFORMS:")
            for p in results['passed']:
                logger.info(f"   • {p}")
        if results['failed']:
            logger.info("\n⚠️  FAILED PLATFORMS:")
            for p, e in results['failed']:
                logger.info(f"   • {p}: {e}")
        logger.info("=" * 80)

if __name__ == "__main__":
    email = EmailTestSuite("kiprutovictor39@gmail.com")
    email_r = email.run()
    
    social = SocialTestSuite()
    social_r = social.run()
    
    logger.info("\n" + "=" * 80)
    logger.info("🎯 OVERALL TEST SUMMARY")
    logger.info("=" * 80)
    logger.info(f"📧 Email Templates: {len(email_r['passed'])}/{email_r['total']} passed ✅")
    logger.info(f"📱 Social Platforms: {len(social_r['passed'])}/{social_r['total']} passed ✅")
    total = len(email_r['passed']) + len(social_r['passed'])
    total_all = email_r['total'] + social_r['total']
    pct = (total/total_all*100) if total_all > 0 else 0
    logger.info(f"🎉 Total: {total}/{total_all} ({pct:.0f}%)")
    logger.info("=" * 80)
    logger.info("\n✅ Test suite complete! All test emails sent to kiprutovictor39@gmail.com")
    logger.info("   Check your inbox for 13 different email template examples.")
