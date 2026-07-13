"""
================================================================================
DBOS - Developer Brand Operating System
INTEGRATED CONFIGURATION MANAGER
================================================================================
Loads and validates all credentials from .env file and initializes all services:
- Analytics (GA4, Mixpanel, Segment)
- Social Media (Twitter, LinkedIn, Dev.to)
- Email & Notifications (Resend, SMTP, Telegram)
- AI & Image Generation (OpenAI, Unsplash, Pexels)
- Database & Security
- GitHub Automation
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging
from typing import Dict, Any, Optional

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DBOS.Config")


# ============================================================================
# CORE CONFIGURATION CLASSES
# ============================================================================

class AppConfig:
    """Core application settings"""
    NAME = os.getenv("APP_NAME", "DBOS")
    ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "production")
    DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
    URL = os.getenv("APP_URL")
    TIMEZONE = os.getenv("APP_TIMEZONE", "UTC")


class PortfolioConfig:
    """Portfolio and blog configuration"""
    URL = os.getenv("PORTFOLIO_URL")
    GITHUB_REPO = os.getenv("PORTFOLIO_GITHUB")
    GITHUB_USERNAME = os.getenv("GITHUB_ACTOR")
    
    BLOG_TITLE = os.getenv("BLOG_TITLE")
    BLOG_DESCRIPTION = os.getenv("BLOG_DESCRIPTION")
    BLOG_URL = os.getenv("BLOG_URL")
    BLOG_POSTS_PATH = os.getenv("BLOG_POSTS_PATH", "blog/assets/shared/posts.json")
    BLOG_IMAGES_PATH = os.getenv("BLOG_IMAGES_PATH", "assets/auto")


class AnalyticsConfig:
    """Analytics services configuration"""
    ENABLED = os.getenv("ANALYTICS_ENABLED", "true").lower() == "true"
    DEBUG = os.getenv("ANALYTICS_DEBUG", "false").lower() == "true"
    
    # Google Analytics
    GA4_ID = os.getenv("GOOGLE_ANALYTICS_ID")
    
    # Mixpanel
    MIXPANEL_TOKEN = os.getenv("MIXPANEL_TOKEN")
    MIXPANEL_API_TOKEN = os.getenv("MIXPANEL_API_TOKEN")
    
    # Segment
    SEGMENT_WRITE_KEY = os.getenv("SEGMENT_WRITE_KEY")


class SocialMediaConfig:
    """Social media automation configuration"""
    
    class Twitter:
        API_KEY = os.getenv("TWITTER_API_KEY")
        API_SECRET = os.getenv("TWITTER_API_SECRET")
        BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
        CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
        CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
        ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
        ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
    
    class LinkedIn:
        CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
        CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
        REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
        PROFILE_URL = os.getenv("LINKEDIN_PROFILE_URL")
    
    class DevTo:
        API_KEY = os.getenv("DEVTO_API_KEY")
        USERNAME = os.getenv("DEVTO_USERNAME")
    
    class Medium:
        ACCESS_TOKEN = os.getenv("MEDIUM_ACCESS_TOKEN")


class EmailConfig:
    """Email and notification configuration"""
    
    class Resend:
        API_KEY = os.getenv("RESEND_API_KEY")
        FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL")
        FROM_NAME = os.getenv("RESEND_FROM_NAME")
    
    class SMTP:
        HOST = os.getenv("SMTP_HOST")
        PORT = int(os.getenv("SMTP_PORT", 587))
        USER = os.getenv("SMTP_USER")
        PASSWORD = os.getenv("SMTP_PASSWORD")
        ENCRYPTION = os.getenv("SMTP_ENCRYPTION", "tls")
    
    class Telegram:
        BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
        BOT_NAME = os.getenv("TELEGRAM_BOT_NAME")
        API_URL = os.getenv("TELEGRAM_API_URL")


class AIConfig:
    """AI and image generation configuration"""
    
    class OpenAI:
        API_KEY = os.getenv("OPENAI_API_KEY")
        MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
    
    class Unsplash:
        ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
        SECRET_KEY = os.getenv("UNSPLASH_SECRET_KEY")
    
    class Pexels:
        API_KEY = os.getenv("PEXELS_API_KEY")
    
    PROVIDER = os.getenv("IMAGE_PROVIDER", "openai")
    IMAGE_SIZE = os.getenv("IMAGE_SIZE", "1024x1024")
    IMAGE_STYLE = os.getenv("IMAGE_STYLE", "modern-tech-dark")
    AUTO_GENERATION = os.getenv("AUTO_IMAGE_GENERATION", "true").lower() == "true"


class DatabaseConfig:
    """Database configuration"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    BACKUP_PATH = os.getenv("DATABASE_BACKUP_PATH", "backups/")
    AUTO_BACKUP = os.getenv("DATABASE_AUTO_BACKUP", "true").lower() == "true"


class DashboardConfig:
    """Dashboard security configuration"""
    ENABLED = os.getenv("DASHBOARD_ENABLED", "true").lower() == "true"
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
    SESSION_SECRET = os.getenv("SESSION_SECRET")
    PASSWORD = os.getenv("DASHBOARD_PASSWORD")
    SESSION_HOURS = int(os.getenv("DASHBOARD_SESSION_HOURS", 8))


class BlogConfig:
    """Blog engine configuration"""
    AUTO_PUBLISH = os.getenv("AUTO_PUBLISH_ENABLED", "true").lower() == "true"
    AUTO_RSS_UPDATE = os.getenv("AUTO_RSS_UPDATE", "true").lower() == "true"
    AUTO_SITEMAP_UPDATE = os.getenv("AUTO_SITEMAP_UPDATE", "true").lower() == "true"
    AUTO_SOCIAL_SHARE = os.getenv("AUTO_SOCIAL_SHARE", "true").lower() == "true"


class NotificationConfig:
    """Notification system configuration"""
    AUTO_ENABLED = os.getenv("AUTO_NOTIFICATIONS", "true").lower() == "true"
    TELEGRAM_ENABLED = os.getenv("TELEGRAM_NOTIFICATIONS", "true").lower() == "true"
    EMAIL_ENABLED = os.getenv("EMAIL_NOTIFICATIONS", "true").lower() == "true"
    
    MAX_EMAIL_PER_DAY = int(os.getenv("MAX_EMAIL_PER_DAY", 50))
    MAX_TELEGRAM_ALERTS_PER_HOUR = int(os.getenv("MAX_TELEGRAM_ALERTS_PER_HOUR", 10))
    DEDUPLICATION_ENABLED = os.getenv("DEDUPLICATION_ENABLED", "true").lower() == "true"


class EventConfig:
    """Event and automation engine configuration"""
    BUS_ENABLED = os.getenv("EVENT_BUS_ENABLED", "true").lower() == "true"
    JOB_QUEUE_ENABLED = os.getenv("JOB_QUEUE_ENABLED", "true").lower() == "true"


class SecurityConfig:
    """Security configuration"""
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_REQUESTS_PER_MINUTE = int(os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", 60))
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")


class LoggingConfig:
    """Logging and monitoring configuration"""
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.getenv("LOG_FORMAT", "json")
    SYSTEM_HEALTH_ENABLED = os.getenv("SYSTEM_HEALTH_ENABLED", "true").lower() == "true"
    SENTRY_DSN = os.getenv("SENTRY_DSN")


class GitHubConfig:
    """GitHub automation configuration"""
    TOKEN = os.getenv("GITHUB_TOKEN")
    ACTOR = os.getenv("GITHUB_ACTOR")
    WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
    WORKFLOW_RUN_SCHEDULE = os.getenv("WORKFLOW_RUN_SCHEDULE", "0 8 * * *")
    DAILY_MAINTENANCE_SCHEDULE = os.getenv("DAILY_MAINTENANCE_SCHEDULE", "0 2 * * *")


# ============================================================================
# MASTER CONFIGURATION INTEGRATOR
# ============================================================================

class DBOSConfig:
    """Master configuration integrator for all services"""
    
    def __init__(self):
        self.app = AppConfig()
        self.portfolio = PortfolioConfig()
        self.analytics = AnalyticsConfig()
        self.social = SocialMediaConfig()
        self.email = EmailConfig()
        self.ai = AIConfig()
        self.database = DatabaseConfig()
        self.dashboard = DashboardConfig()
        self.blog = BlogConfig()
        self.notifications = NotificationConfig()
        self.events = EventConfig()
        self.security = SecurityConfig()
        self.logging = LoggingConfig()
        self.github = GitHubConfig()
    
    def get_service_status(self) -> Dict[str, bool]:
        """Get status of all configured services"""
        return {
            "analytics": bool(self.analytics.MIXPANEL_TOKEN and self.analytics.GA4_ID),
            "twitter": bool(self.social.Twitter.API_KEY and self.social.Twitter.API_SECRET),
            "linkedin": bool(self.social.LinkedIn.CLIENT_ID),
            "devto": bool(self.social.DevTo.API_KEY),
            "email_resend": bool(self.email.Resend.API_KEY),
            "email_smtp": bool(self.email.SMTP.HOST and self.email.SMTP.USER),
            "telegram": bool(self.email.Telegram.BOT_TOKEN),
            "openai": bool(self.ai.OpenAI.API_KEY),
            "unsplash": bool(self.ai.Unsplash.ACCESS_KEY),
            "pexels": bool(self.ai.Pexels.API_KEY),
            "database": bool(self.database.DATABASE_URL),
            "github": bool(self.github.TOKEN),
            "security": bool(self.security.ENCRYPTION_KEY),
        }
    
    def validate_critical_services(self) -> tuple[bool, list]:
        """Validate all critical services are configured"""
        errors = []
        
        # Critical: Analytics
        if not self.analytics.MIXPANEL_TOKEN:
            errors.append("❌ Mixpanel token not configured")
        if not self.analytics.GA4_ID:
            errors.append("❌ Google Analytics ID not configured")
        
        # Critical: Email
        if not self.email.Resend.API_KEY:
            errors.append("❌ Resend API key not configured")
        
        # Critical: Database
        if not self.database.DATABASE_URL:
            errors.append("❌ Database URL not configured")
        
        # Critical: Security
        if not self.security.ENCRYPTION_KEY:
            errors.append("❌ Encryption key not configured")
        
        # Critical: GitHub
        if not self.github.TOKEN:
            errors.append("❌ GitHub token not configured")
        
        return len(errors) == 0, errors
    
    def print_status(self):
        """Print comprehensive configuration status"""
        print("\n" + "="*80)
        print("DBOS - INTEGRATED CONFIGURATION STATUS")
        print("="*80)
        
        # App info
        print(f"\n📱 APPLICATION")
        print(f"   Name: {self.app.NAME}")
        print(f"   Environment: {self.app.ENVIRONMENT}")
        print(f"   Debug: {self.app.DEBUG}")
        print(f"   URL: {self.app.URL}")
        
        # Service status
        print(f"\n🔌 SERVICE STATUS")
        services = self.get_service_status()
        for service, enabled in services.items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {service.replace('_', ' ').title()}")
        
        # Validation
        print(f"\n✔️  VALIDATION")
        valid, errors = self.validate_critical_services()
        if valid:
            print("   ✅ All critical services configured")
        else:
            for error in errors:
                print(f"   {error}")
        
        # Analytics configuration
        print(f"\n📊 ANALYTICS")
        print(f"   GA4 ID: {self.analytics.GA4_ID}")
        print(f"   Mixpanel Token: {self.analytics.MIXPANEL_TOKEN[:8]}***")
        print(f"   Segment Key: {self.analytics.SEGMENT_WRITE_KEY[:8] if self.analytics.SEGMENT_WRITE_KEY else 'Not configured'}***")
        
        # Social media
        print(f"\n📱 SOCIAL MEDIA")
        print(f"   Twitter: {'✅ Configured' if self.social.Twitter.API_KEY else '❌ Not configured'}")
        print(f"   LinkedIn: {'✅ Configured' if self.social.LinkedIn.CLIENT_ID else '❌ Not configured'}")
        print(f"   Dev.to: {'✅ Configured' if self.social.DevTo.API_KEY else '❌ Not configured'}")
        print(f"   LinkedIn Profile: {self.social.LinkedIn.PROFILE_URL}")
        
        # Email
        print(f"\n📧 EMAIL & NOTIFICATIONS")
        print(f"   Resend API: {'✅ Configured' if self.email.Resend.API_KEY else '❌ Not configured'}")
        print(f"   SMTP: {'✅ Configured' if self.email.SMTP.HOST else '❌ Not configured'}")
        print(f"   From Email: {self.email.Resend.FROM_EMAIL}")
        print(f"   Telegram Bot: {'✅ Configured' if self.email.Telegram.BOT_TOKEN else '❌ Not configured'}")
        
        # AI & Images
        print(f"\n🤖 AI & IMAGE GENERATION")
        print(f"   OpenAI: {'✅ Configured' if self.ai.OpenAI.API_KEY else '❌ Not configured'}")
        print(f"   Model: {self.ai.OpenAI.MODEL}")
        print(f"   Unsplash: {'✅ Configured' if self.ai.Unsplash.ACCESS_KEY else '❌ Not configured'}")
        print(f"   Pexels: {'✅ Configured' if self.ai.Pexels.API_KEY else '❌ Not configured'}")
        print(f"   Provider: {self.ai.PROVIDER}")
        print(f"   Auto Generation: {self.ai.AUTO_GENERATION}")
        
        # Database
        print(f"\n💾 DATABASE & STORAGE")
        print(f"   Database URL: {self.database.DATABASE_URL.split('/')[-1] if self.database.DATABASE_URL else 'Not configured'}")
        print(f"   Auto Backup: {self.database.AUTO_BACKUP}")
        print(f"   Storage Path: {self.database.BACKUP_PATH}")
        
        # Security
        print(f"\n🔒 SECURITY")
        print(f"   Encryption Key: {'✅ Configured' if self.security.ENCRYPTION_KEY else '❌ Not configured'}")
        print(f"   Rate Limiting: {self.security.RATE_LIMIT_ENABLED} ({self.security.RATE_LIMIT_REQUESTS_PER_MINUTE} req/min)")
        print(f"   Dashboard Password: {'✅ Configured' if self.dashboard.PASSWORD else '❌ Not configured'}")
        print(f"   Session Hours: {self.dashboard.SESSION_HOURS}")
        
        # GitHub
        print(f"\n🐙 GITHUB AUTOMATION")
        print(f"   Token: {'✅ Configured' if self.github.TOKEN else '❌ Not configured'}")
        print(f"   Actor: {self.github.ACTOR}")
        print(f"   Workflow Schedule: {self.github.WORKFLOW_RUN_SCHEDULE}")
        
        # Blog
        print(f"\n📝 BLOG ENGINE")
        print(f"   Title: {self.portfolio.BLOG_TITLE}")
        print(f"   Auto Publish: {self.blog.AUTO_PUBLISH}")
        print(f"   Auto RSS Update: {self.blog.AUTO_RSS_UPDATE}")
        print(f"   Auto Social Share: {self.blog.AUTO_SOCIAL_SHARE}")
        
        print("\n" + "="*80)
        print("INTEGRATION COMPLETE ✅\n")


# ============================================================================
# INITIALIZATION
# ============================================================================

# Create global config instance
config = DBOSConfig()


def init_config():
    """Initialize and validate all configuration"""
    logger.info(f"Initializing {AppConfig.NAME} configuration...")
    config.print_status()
    return config


# Auto-initialize on import
if __name__ == "__main__":
    init_config()
