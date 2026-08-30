#!/usr/bin/env python3
"""
DBOS Base Configuration
Central configuration for all generators and services
"""

class Config:
    """Central configuration for DBOS"""
    
    # Base URLs
    BASE_URL = 'https://victorkipruto.com'
    GITHUB_PAGES_URL = 'https://victorkipruto.com'
    
    # Local paths
    BLOG_DIR = 'blog'
    POSTS_FILE = 'blog/posts.json'
    RENDERED_DIR = 'blog/rendered'
    CONTENT_DIR = 'content'
    ASSETS_DIR = 'assets'
    DASHBOARD_DIR = 'dashboard'
    SECURITY_DIR = 'security'
    ANALYTICS_DIR = 'analytics'
    STRATEGY_DIR = 'strategy'
    DISTRIBUTION_DIR = 'distribution'
    
    # Output files
    RSS_FILE = 'feed.xml'
    SITEMAP_FILE = 'sitemap.xml'
    
    # Blog settings
    BLOG_TITLE = 'Victor Kipruto - Developer Blog'
    BLOG_DESCRIPTION = 'Advanced insights on Data Engineering, Analytics Engineering, and System Design'
    AUTHOR_EMAIL = 'victor@kipruto.dev'
    
    # Post settings
    RSS_ITEMS_LIMIT = 20
    FEATURED_POSTS_LIMIT = 5
    
    # SEO settings
    SEO_TITLE_LENGTH = 60
    SEO_DESCRIPTION_LENGTH = 160
    
    # Security
    SESSION_TIMEOUT_HOURS = 8
    TOKEN_EXPIRY_HOURS = 8
    
    @classmethod
    def get_post_url(cls, slug: str) -> str:
        """Get full URL for a post"""
        return f"{cls.BASE_URL}/blog/posts/{slug}"
    
    @classmethod
    def get_category_url(cls, category: str) -> str:
        """Get full URL for a category page"""
        cat_slug = category.lower().replace(' ', '-')
        return f"{cls.BASE_URL}/blog/categories/{cat_slug}"
    
    @classmethod
    def get_tag_url(cls, tag: str) -> str:
        """Get full URL for a tag page"""
        tag_slug = tag.lower().replace(' ', '-')
        return f"{cls.BASE_URL}/blog/tags/{tag_slug}"
    
    @classmethod
    def get_blog_url(cls) -> str:
        """Get full URL for blog home"""
        return f"{cls.BASE_URL}/blog"
    
    @classmethod
    def get_rss_url(cls) -> str:
        """Get full URL for RSS feed"""
        return f"{cls.BASE_URL}/feed.xml"
    
    @classmethod
    def get_sitemap_url(cls) -> str:
        """Get full URL for sitemap"""
        return f"{cls.BASE_URL}/sitemap.xml"
    
    @classmethod
    def get_dashboard_url(cls, dashboard_name: str = 'analytics') -> str:
        """Get full URL for a dashboard"""
        return f"{cls.BASE_URL}/dashboard/{dashboard_name}.html"
    
    @classmethod
    def get_asset_url(cls, asset_path: str) -> str:
        """Get full URL for an asset"""
        return f"{cls.BASE_URL}/{asset_path}"

if __name__ == '__main__':
    # Test configuration
    print("DBOS Configuration Test\n")
    print(f"Base URL: {Config.BASE_URL}")
    print(f"Blog URL: {Config.get_blog_url()}")
    print(f"RSS URL: {Config.get_rss_url()}")
    print(f"Sitemap URL: {Config.get_sitemap_url()}")
    print(f"Post URL: {Config.get_post_url('example-post')}")
    print(f"Dashboard URL: {Config.get_dashboard_url('analytics-dashboard-private')}")
