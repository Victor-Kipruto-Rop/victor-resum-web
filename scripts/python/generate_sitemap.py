#!/usr/bin/env python3
"""
DBOS PHASE 1: Sitemap Generator
Auto-generates XML sitemap from assets/shared/posts.json
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from config import Config

class SitemapGenerator:
    """Generate XML sitemap automatically"""
    
    def __init__(self):
        self.posts_file = Path('blog/assets/shared/posts.json')
        self.sitemap_file = Path('sitemap.xml')
        self.base_url = Config.BASE_URL
        self.posts = []
    
    def load_posts(self):
        """Load posts from JSON"""
        with open(self.posts_file) as f:
            self.posts = json.load(f)
        
        # Filter published posts
        self.posts = [p for p in self.posts if p.get('status') == 'published']
        print(f"✓ Loaded {len(self.posts)} published posts")
    
    def get_categories(self):
        """Get unique categories"""
        categories = set()
        for post in self.posts:
            categories.add(post.get('category', 'Uncategorized'))
        return sorted(list(categories))
    
    def get_tags(self):
        """Get unique tags"""
        tags = set()
        for post in self.posts:
            tags.update(post.get('tags', []))
        return sorted(list(tags))
    
    def format_date(self, iso_date):
        """Format date as ISO 8601 for sitemap"""
        dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d')
    
    def generate_sitemap(self):
        """Generate sitemap XML"""
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        urls = []
        
        # Add homepage
        urls.append({
            'loc': self.base_url,
            'lastmod': self.format_date(datetime.utcnow().isoformat() + 'Z'),
            'changefreq': 'daily',
            'priority': '1.0'
        })
        
        # Add blog main page
        urls.append({
            'loc': f'{self.base_url}/blog',
            'lastmod': self.format_date(datetime.utcnow().isoformat() + 'Z'),
            'changefreq': 'daily',
            'priority': '0.9'
        })
        
        # Add category pages
        for category in self.get_categories():
            cat_slug = category.lower().replace(' ', '-')
            urls.append({
                'loc': f'{self.base_url}/blog/categories/{cat_slug}',
                'changefreq': 'weekly',
                'priority': '0.8'
            })
        
        # Add tag pages
        for tag in self.get_tags():
            tag_slug = tag.lower().replace(' ', '-')
            urls.append({
                'loc': f'{self.base_url}/blog/tags/{tag_slug}',
                'changefreq': 'weekly',
                'priority': '0.7'
            })
        
        # Add post pages
        for post in self.posts:
            urls.append({
                'loc': f"{self.base_url}/blog/posts/{post['slug']}",
                'lastmod': self.format_date(post.get('updatedDate', post['publishDate'])),
                'changefreq': 'monthly',
                'priority': '0.9'
            })
        
        # Build XML
        for url_data in urls:
            url_elem = ET.SubElement(urlset, 'url')
            ET.SubElement(url_elem, 'loc').text = url_data['loc']
            
            if 'lastmod' in url_data:
                ET.SubElement(url_elem, 'lastmod').text = url_data['lastmod']
            
            ET.SubElement(url_elem, 'changefreq').text = url_data['changefreq']
            ET.SubElement(url_elem, 'priority').text = url_data['priority']
        
        # Pretty print
        indent_xml(urlset)
        
        # Write to file
        tree = ET.ElementTree(urlset)
        tree.write(self.sitemap_file, encoding='utf-8', xml_declaration=True)
        print(f"✓ Generated sitemap: {self.sitemap_file} ({len(urls)} URLs)")
    
    def validate_sitemap(self):
        """Validate sitemap structure"""
        try:
            tree = ET.parse(self.sitemap_file)
            root = tree.getroot()
            
            # Check namespace
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = root.findall('sm:url', ns) or root.findall('url')
            
            assert len(urls) > 0, "No URLs found in sitemap"
            
            # Spot-check URL structure
            for url in urls[:3]:
                assert url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc') is not None or url.find('loc') is not None, \
                    "URL missing <loc>"
            
            print(f"✓ Sitemap validation passed ({len(urls)} URLs)")
            return True
        except Exception as e:
            print(f"✗ Sitemap validation failed: {e}")
            return False
    
    def run(self):
        """Execute sitemap generation"""
        print("\n🚀 DBOS PHASE 1: Sitemap Generator\n")
        self.load_posts()
        self.generate_sitemap()
        self.validate_sitemap()
        print("\n✅ Sitemap generation complete!\n")

def indent_xml(elem, level=0):
    """Add pretty-print indentation to XML"""
    indent = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for child in elem:
            indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent

if __name__ == '__main__':
    generator = SitemapGenerator()
    generator.run()
