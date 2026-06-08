#!/usr/bin/env python3
"""
Content Formatter - Format blog posts for different social platforms
"""

import re
import logging
from typing import Dict


class ContentFormatter:
    """Format blog content for different platforms"""

    def __init__(self, config: Dict):
        """Initialize formatter"""
        self.config = config
        self.logger = logging.getLogger(__name__)

    def format_for_all_platforms(self, post_data: Dict) -> Dict:
        """
        Format blog post for all platforms

        Args:
            post_data: Blog post with title, content, metadata

        Returns:
            Dict with formatted content for each platform
        """
        formatted = {
            "linkedin": self.format_for_linkedin(post_data),
            "twitter": self.format_for_twitter(post_data),
            "devto": self.format_for_devto(post_data),
            "medium": self.format_for_medium(post_data),
            "telegram": self.format_for_telegram(post_data)
        }
        return formatted

    def format_for_linkedin(self, post_data: Dict) -> Dict:
        """Format content for LinkedIn"""
        title = post_data.get("title", "")
        content = post_data.get("content", "")
        excerpt = self._extract_excerpt(content, 200)

        return {
            "title": title,
            "excerpt": excerpt,
            "url": post_data.get("url", ""),
            "hashtags": ["#DataEngineering", "#Blog", "#Analytics"],
            "platform": "linkedin"
        }

    def format_for_twitter(self, post_data: Dict) -> Dict:
        """Format content for Twitter/X"""
        title = post_data.get("title", "")
        content = post_data.get("content", "")
        url = post_data.get("url", "")

        # Create main tweet
        main_tweet = f"🚀 New blog post: {title}\n\n{url}"

        # Create thread for longer content
        thread = self._create_twitter_thread(title, content, url)

        return {
            "tweet": main_tweet[:280],
            "thread": thread,
            "hashtags": ["#DataEngineering", "#Python", "#Analytics"],
            "platform": "twitter"
        }

    def format_for_devto(self, post_data: Dict) -> Dict:
        """Format content for Dev.to"""
        markdown = post_data.get("content", "")

        # Add frontmatter if not present
        if not markdown.startswith("---"):
            markdown = self._add_devto_frontmatter(post_data) + markdown

        tags = self._extract_tags(post_data)

        return {
            "title": post_data.get("title", ""),
            "markdown": markdown,
            "tags": tags[:4],  # Max 4 tags for Dev.to
            "canonical_url": post_data.get("url", ""),
            "platform": "devto"
        }

    def format_for_medium(self, post_data: Dict) -> Dict:
        """Format content for Medium"""
        markdown = post_data.get("content", "")
        html = self._markdown_to_html(markdown)
        tags = self._extract_tags(post_data)

        return {
            "title": post_data.get("title", ""),
            "html": html,
            "markdown": markdown,
            "tags": tags[:5],  # Max 5 tags for Medium
            "canonical_url": post_data.get("url", ""),
            "platform": "medium"
        }

    def format_for_telegram(self, post_data: Dict) -> Dict:
        """Format content for Telegram"""
        title = post_data.get("title", "")
        content = post_data.get("content", "")
        excerpt = self._extract_excerpt(content, 300)
        url = post_data.get("url", "")

        return {
            "title": title,
            "excerpt": excerpt,
            "url": url,
            "message": f"📰 {title}\n\n{excerpt}\n\n{url}",
            "platform": "telegram"
        }

    def _extract_excerpt(self, content: str, max_length: int = 200) -> str:
        """Extract excerpt from content"""
        # Remove markdown syntax
        text = re.sub(r'[#*_`]', '', content)
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Get first max_length characters
        excerpt = text[:max_length].strip()
        # Remove incomplete last word
        if len(text) > max_length:
            excerpt = excerpt.rsplit(' ', 1)[0] + "..."

        return excerpt

    def _extract_tags(self, post_data: Dict) -> list:
        """Extract and sanitize tags from post metadata"""
        raw_tags = post_data.get("tags", [])
        if not raw_tags:
            raw_tags = ["dataengineering", "blog", "analytics"]
        
        # Sanitize tags for all platforms (alphanumeric only)
        sanitized = []
        for tag in raw_tags:
            clean = "".join(c for c in tag if c.isalnum()).lower()
            if clean:
                sanitized.append(clean)
        return sanitized

    def _create_twitter_thread(self, title: str, content: str, url: str) -> list:
        """Create Twitter thread from content"""
        tweets = []

        # First tweet with title
        tweets.append(f"🧵 New article: {title}\n\n{url}")

        # Extract key points
        paragraphs = content.split('\n\n')
        for para in paragraphs[:3]:  # Max 3 tweets for thread
            clean_para = self.clean_content(para)
            if len(clean_para.strip()) > 10:
                tweet_text = clean_para.strip()[:280]
                tweets.append(tweet_text)

        return tweets

    def _add_devto_frontmatter(self, post_data: Dict) -> str:
        """Add Dev.to frontmatter to markdown"""
        title = post_data.get("title", "")
        tags = self._extract_tags(post_data)
        url = post_data.get("url", "")

        frontmatter = f"""---
title: {title}
published: true
tags: {', '.join(tags[:4])}
canonical_url: {url}
---

"""
        return frontmatter

    def _markdown_to_html(self, markdown: str) -> str:
        """Simple markdown to HTML conversion"""
        html = markdown

        # Headers
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

        # Bold and Italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)

        # Links
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

        # Code blocks
        html = re.sub(r'```\n(.*?)\n```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)

        # Paragraphs
        html = re.sub(r'\n\n', '</p><p>', html)
        html = f'<p>{html}</p>'

        # Lists
        html = re.sub(r'- (.*?)(?=\n|$)', r'<li>\1</li>', html)
        html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)

        return html

    def clean_content(self, content: str) -> str:
        """Clean and optimize content for sharing"""
        # Remove markdown syntax
        content = re.sub(r'[#*_`]', '', content)
        # Remove code blocks
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        # Fix spacing
        content = re.sub(r'\n+', '\n', content)

        return content.strip()


if __name__ == "__main__":
    # Test
    config = {"blog": {"title": "Tech Blog"}}
    formatter = ContentFormatter(config)

    test_post = {
        "title": "Getting Started with Airflow",
        "content": "# Getting Started\n\nApache Airflow is a **powerful** orchestration tool.\n\n## Features\n- DAGs\n- Scheduling\n- Monitoring",
        "url": "https://victorkirpruto.dev/posts/airflow",
        "tags": ["airflow", "data-engineering"]
    }

    formatted = formatter.format_for_all_platforms(test_post)
    for platform, data in formatted.items():
        print(f"\n{platform.upper()}:")
        print(data)
