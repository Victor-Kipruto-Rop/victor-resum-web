#!/usr/bin/env python3
"""
DBOS PHASE 1: RSS Feed Generator
Auto-generates RSS 2.0 feed from assets/shared/posts.json
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from email.utils import formatdate
from config import Config

class RSSGenerator:
    """Generate RSS 2.0 feed automatically"""
    
    def __init__(self):
        self.posts_file = Path('blog/assets/shared/posts.json')
        self.rss_file = Path('feed.xml')
        self.base_url = Config.BASE_URL
        self.posts = []
    
    def load_posts(self):
        """Load posts from JSON"""
        with open(self.posts_file) as f:
            self.posts = json.load(f)
        
        # Filter published posts, sort by date (newest first)
        self.posts = [p for p in self.posts if p.get('status') == 'published']
        self.posts.sort(key=lambda x: x.get('publishDate', ''), reverse=True)
        # Keep only last 20 posts
        self.posts = self.posts[:20]
        print(f"✓ Loaded {len(self.posts)} posts for RSS feed")
    
    def escape_xml(self, text):
        """Escape special XML characters"""
        if not text:
            return ''
        return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;'))
    
    def rfc822_date(self, iso_date):
        """Convert ISO date to RFC 822 format"""
        dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        return formatdate(timeval=dt.timestamp(), localtime=False, usegmt=True)
    
    def generate_rss(self):
        """Generate RSS XML feed"""
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
        
        channel = ET.SubElement(rss, 'channel')
        
        # Channel info
        ET.SubElement(channel, 'title').text = 'Victor Kipruto - Developer Blog'
        ET.SubElement(channel, 'link').text = f'{self.base_url}/blog'
        ET.SubElement(channel, 'description').text = 'Advanced insights on Data Engineering, Analytics Engineering, and System Design'
        ET.SubElement(channel, 'language').text = 'en-us'
        ET.SubElement(channel, 'lastBuildDate').text = self.rfc822_date(datetime.utcnow().isoformat() + 'Z')
        
        atom_link = ET.SubElement(channel, 'atom:link')
        atom_link.set('href', f'{self.base_url}/feed.xml')
        atom_link.set('rel', 'self')
        atom_link.set('type', 'application/rss+xml')
        
        # Add items
        for post in self.posts:
            item = ET.SubElement(channel, 'item')
            
            ET.SubElement(item, 'title').text = self.escape_xml(post['title'])
            ET.SubElement(item, 'link').text = f"{self.base_url}/blog/posts/{post['slug']}"
            ET.SubElement(item, 'guid').text = f"{self.base_url}/blog/posts/{post['slug']}"
            ET.SubElement(item, 'pubDate').text = self.rfc822_date(post['publishDate'])
            ET.SubElement(item, 'description').text = self.escape_xml(post['description'])
            
            # Add category
            category = ET.SubElement(item, 'category')
            category.text = self.escape_xml(post.get('category', 'Uncategorized'))
            
            # Add tags as categories
            for tag in post.get('tags', []):
                tag_elem = ET.SubElement(item, 'category')
                tag_elem.text = self.escape_xml(tag)
            
            # Author
            ET.SubElement(item, 'author').text = 'victor@kipruto.dev'
        
        # Pretty print
        indent_xml(rss)
        
        # Write to file
        tree = ET.ElementTree(rss)
        tree.write(self.rss_file, encoding='utf-8', xml_declaration=True)
        print(f"✓ Generated RSS feed: {self.rss_file}")
    
    def validate_rss(self):
        """Validate RSS feed structure"""
        try:
            tree = ET.parse(self.rss_file)
            root = tree.getroot()
            
            # Check required elements
            channel = root.find('channel')
            assert channel is not None, "Missing <channel>"
            assert channel.find('title') is not None, "Missing <title>"
            assert channel.find('link') is not None, "Missing <link>"
            assert channel.find('description') is not None, "Missing <description>"
            
            # Check items
            items = channel.findall('item')
            print(f"✓ RSS validation passed ({len(items)} items)")
            return True
        except Exception as e:
            print(f"✗ RSS validation failed: {e}")
            return False
    
    def run(self):
        """Execute RSS generation"""
        print("\n🚀 DBOS PHASE 1: RSS Feed Generator\n")
        self.load_posts()
        self.generate_rss()
        self.validate_rss()
        print("\n✅ RSS generation complete!\n")

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
    generator = RSSGenerator()
    generator.run()
