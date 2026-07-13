#!/usr/bin/env python3
"""
DBOS PHASE 2: SEO Engine
Auto-generates SEO metadata and computes SEO scores
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from config import Config

class SEOEngine:
    """Generate SEO metadata and compute SEO scores"""
    
    def __init__(self):
        self.posts_file = Path('blog/assets/shared/posts.json')
        self.output_dir = Path('assets/seo')
        self.base_url = Config.BASE_URL
        self.posts = []
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_posts(self):
        """Load posts from JSON"""
        with open(self.posts_file) as f:
            self.posts = json.load(f)
        print(f"✓ Loaded {len(self.posts)} posts")
    
    def generate_meta_title(self, post: Dict[str, Any]) -> str:
        """Generate SEO-optimized meta title (60 chars ideal)"""
        title = post['title']
        if len(title) > 60:
            # Truncate and add suffix if too long
            title = title[:55] + '...'
        
        # Add brand at end if space permits
        full_title = f"{title} | Victor Kipruto"
        if len(full_title) > 60:
            return title
        return full_title
    
    def generate_meta_description(self, post: Dict[str, Any]) -> str:
        """Generate SEO-optimized meta description (155-160 chars)"""
        desc = post['description']
        
        # Add CTA
        cta = " Learn more on my blog."
        
        full_desc = desc + cta
        if len(full_desc) > 160:
            full_desc = (desc[:155-len(cta)].rsplit(' ', 1)[0] + cta)
        
        return full_desc
    
    def generate_open_graph(self, post: Dict[str, Any]) -> Dict[str, str]:
        """Generate Open Graph tags"""
        return {
            "og:title": post['title'],
            "og:description": post['description'],
            "og:image": f"{self.base_url}/{post.get('image', 'images/default.png')}",
            "og:type": "article",
            "og:url": f"{self.base_url}/blog/posts/{post['slug']}",
            "og:site_name": "Victor Kipruto - Developer",
            "article:published_time": post['publishDate'],
            "article:modified_time": post.get('updatedDate', post['publishDate']),
            "article:author": "Victor Kipruto"
        }
    
    def generate_twitter_card(self, post: Dict[str, Any]) -> Dict[str, str]:
        """Generate Twitter Card tags"""
        return {
            "twitter:card": "summary_large_image",
            "twitter:title": post['title'],
            "twitter:description": post['description'],
            "twitter:image": f"{self.base_url}/{post.get('image', 'images/default.png')}",
            "twitter:creator": "@VictorKipruto",
            "twitter:site": "@VictorKipruto"
        }
    
    def generate_structured_data(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON-LD structured data"""
        publish_date = datetime.fromisoformat(post['publishDate'].replace('Z', '+00:00'))
        
        return {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post['title'],
            "description": post['description'],
            "image": f"{self.base_url}/{post.get('image', 'images/default.png')}",
            "datePublished": post['publishDate'],
            "dateModified": post.get('updatedDate', post['publishDate']),
            "author": {
                "@type": "Person",
                "name": "Victor Kipruto",
                "url": self.base_url
            },
            "publisher": {
                "@type": "Organization",
                "name": "Victor Kipruto",
                "url": self.base_url
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{self.base_url}/blog/posts/{post['slug']}"
            },
            "keywords": ", ".join(post.get('seoKeywords', [])),
            "articleSection": post.get('category', 'General'),
            "articleBody": f"Read the full article at {self.base_url}/blog/posts/{post['slug']}"
        }
    
    def generate_breadcrumb_schema(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Generate breadcrumb structured data"""
        cat_slug = post.get('category', 'General').lower().replace(' ', '-')
        
        return {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": self.base_url
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Blog",
                    "item": f"{self.base_url}/blog"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": post.get('category', 'General'),
                    "item": f"{self.base_url}/blog/categories/{cat_slug}"
                },
                {
                    "@type": "ListItem",
                    "position": 4,
                    "name": post['title'],
                    "item": f"{self.base_url}/blog/posts/{post['slug']}"
                }
            ]
        }
    
    def compute_seo_score(self, post: Dict[str, Any]) -> int:
        """Compute SEO score 0-100"""
        score = 0
        
        # Title optimization (20 pts)
        title_len = len(post['title'])
        if 30 <= title_len <= 70:
            score += 20
        elif 20 <= title_len <= 80:
            score += 15
        else:
            score += 5
        
        # Meta description (15 pts)
        desc_len = len(post['description'])
        if 50 <= desc_len <= 160:
            score += 15
        elif 40 <= desc_len <= 200:
            score += 10
        
        # Content length (15 pts)
        score += 15  # Assume good if in JSON
        
        # Keyword usage (15 pts)
        if post.get('seoKeywords') and len(post['seoKeywords']) >= 3:
            score += 15
        elif post.get('seoKeywords'):
            score += 10
        
        # Category (10 pts)
        if post.get('category'):
            score += 10
        
        # Tags (10 pts)
        if post.get('tags') and len(post['tags']) >= 3:
            score += 10
        elif post.get('tags'):
            score += 5
        
        # Image (10 pts)
        if post.get('image'):
            score += 10
        
        # Read time (5 pts)
        if post.get('readTime'):
            score += 5
        
        return min(score, 100)
    
    def generate_seo_assets(self):
        """Generate SEO assets for all posts"""
        all_metadata = []
        
        for post in self.posts:
            if post.get('status') != 'published':
                continue
            
            seo_score = self.compute_seo_score(post)
            
            seo_asset = {
                "slug": post['slug'],
                "metaTitle": self.generate_meta_title(post),
                "metaDescription": self.generate_meta_description(post),
                "canonicalUrl": f"{self.base_url}/blog/posts/{post['slug']}",
                "openGraph": self.generate_open_graph(post),
                "twitterCard": self.generate_twitter_card(post),
                "structuredData": {
                    "blogPosting": self.generate_structured_data(post),
                    "breadcrumb": self.generate_breadcrumb_schema(post)
                },
                "seoScore": seo_score,
                "keywords": post.get('seoKeywords', []),
                "category": post.get('category'),
                "tags": post.get('tags', [])
            }
            
            # Save individual post SEO file
            output_file = self.output_dir / f"{post['slug']}-seo.json"
            with open(output_file, 'w') as f:
                json.dump(seo_asset, f, indent=2)
            
            all_metadata.append(seo_asset)
        
        # Save combined metadata
        output_file = self.output_dir / 'posts-metadata.json'
        with open(output_file, 'w') as f:
            json.dump(all_metadata, f, indent=2)
        
        print(f"✓ Generated SEO assets for {len(all_metadata)} posts")
    
    def run(self):
        """Execute SEO engine"""
        print("\n🚀 DBOS PHASE 2: SEO Engine\n")
        self.load_posts()
        self.generate_seo_assets()
        print("\n✅ SEO generation complete!\n")

if __name__ == '__main__':
    engine = SEOEngine()
    engine.run()
