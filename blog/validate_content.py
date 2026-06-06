#!/usr/bin/env python3
"""
Blog Content Validation Engine
Validates post metadata and content integrity
"""

import json
import os
import re
from datetime import datetime

BLOG_DIR = os.path.dirname(__file__)
POSTS_FILE = os.path.join(BLOG_DIR, "posts.json")
VALIDATION_REPORT = os.path.join(BLOG_DIR, "validation-report.json")

class ContentValidator:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passes = []
        
    def load_posts(self):
        """Load posts from posts.json"""
        with open(POSTS_FILE, 'r') as f:
            self.posts_data = json.load(f)
        self.posts = self.posts_data.get('posts', [])
        
    def validate_post(self, post):
        """Validate individual post"""
        post_id = post.get('id', 'UNKNOWN')
        post_title = post.get('title', 'UNKNOWN')
        
        # Required fields
        required_fields = ['id', 'title', 'slug', 'description', 'author', 'publishDate', 'category']
        for field in required_fields:
            if not post.get(field):
                self.issues.append(f"[{post_id}] Missing required field: {field}")
            else:
                self.passes.append(f"[{post_id}] Has field: {field}")
        
        # Slug format validation
        if post.get('slug'):
            if not re.match(r'^[a-z0-9-]+$', post['slug']):
                self.issues.append(f"[{post_id}] Invalid slug format: {post['slug']}")
        
        # Description length
        desc = post.get('description', '')
        if len(desc) < 50:
            self.warnings.append(f"[{post_id}] Description too short ({len(desc)} chars), recommend 50+")
        elif len(desc) > 500:
            self.warnings.append(f"[{post_id}] Description very long ({len(desc)} chars), consider shortening")
        
        # Date validation
        try:
            datetime.fromisoformat(post.get('publishDate', ''))
            self.passes.append(f"[{post_id}] Valid publish date")
        except:
            self.issues.append(f"[{post_id}] Invalid publish date format")
        
        # Tags validation
        if not post.get('tags') or not isinstance(post.get('tags'), list):
            self.warnings.append(f"[{post_id}] No tags or invalid tags format")
        elif len(post.get('tags', [])) < 3:
            self.warnings.append(f"[{post_id}] Only {len(post['tags'])} tags (recommend 3+)")
        
        # Category exists
        categories = [c['name'] for c in self.posts_data.get('categories', [])]
        if post.get('category') not in categories:
            self.warnings.append(f"[{post_id}] Category '{post.get('category')}' not in registry")
        
        # Image exists
        if not post.get('image'):
            self.warnings.append(f"[{post_id}] No image specified")
        
        # Status validation
        valid_statuses = ['published', 'draft', 'archived']
        if post.get('status') not in valid_statuses:
            self.issues.append(f"[{post_id}] Invalid status: {post.get('status')}")
        
        # Title length
        title = post.get('title', '')
        if len(title) < 30:
            self.warnings.append(f"[{post_id}] Title too short ({len(title)} chars)")
        elif len(title) > 70:
            self.warnings.append(f"[{post_id}] Title too long ({len(title)} chars, SEO recommends <70)")
        
        # Read time validation
        if post.get('readTime') and not isinstance(post.get('readTime'), (int, float)):
            self.issues.append(f"[{post_id}] Invalid readTime format")
        
    def validate_structure(self):
        """Validate overall structure"""
        # Check for duplicate IDs
        ids = [p.get('id') for p in self.posts]
        duplicates = [id for id in set(ids) if ids.count(id) > 1]
        if duplicates:
            self.issues.append(f"Duplicate post IDs: {duplicates}")
        
        # Check for duplicate slugs
        slugs = [p.get('slug') for p in self.posts]
        duplicate_slugs = [s for s in set(slugs) if slugs.count(s) > 1]
        if duplicate_slugs:
            self.issues.append(f"Duplicate slugs: {duplicate_slugs}")
        
        # Check categories
        categories = self.posts_data.get('categories', [])
        if not categories:
            self.warnings.append("No categories defined")
        
        # Check tags
        tags = self.posts_data.get('tags', [])
        if not tags:
            self.warnings.append("No tags defined")
    
    def generate_report(self):
        """Generate validation report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_posts": len(self.posts),
                "pass_checks": len(self.passes),
                "warnings": len(self.warnings),
                "critical_issues": len(self.issues)
            },
            "passes": self.passes,
            "warnings": self.warnings,
            "issues": self.issues,
            "status": "PASS" if not self.issues else "FAIL"
        }
        
        with open(VALIDATION_REPORT, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def print_report(self, report):
        """Print validation report"""
        print("\n" + "="*60)
        print("BLOG CONTENT VALIDATION REPORT")
        print("="*60)
        
        print(f"\nStatus: {report['status']}")
        print(f"Timestamp: {report['timestamp']}")
        print(f"\nSummary:")
        print(f"  • Total Posts: {report['summary']['total_posts']}")
        print(f"  • Passed Checks: {report['summary']['pass_checks']}")
        print(f"  • Warnings: {report['summary']['warnings']}")
        print(f"  • Critical Issues: {report['summary']['critical_issues']}")
        
        if report['issues']:
            print(f"\n⚠ ISSUES ({len(report['issues'])}):")
            for issue in report['issues']:
                print(f"  • {issue}")
        
        if report['warnings']:
            print(f"\n⚠ WARNINGS ({len(report['warnings'])}):")
            for warning in report['warnings']:
                print(f"  • {warning}")
        
        print("\n" + "="*60 + "\n")

def validate():
    """Run complete validation"""
    validator = ContentValidator()
    validator.load_posts()
    
    # Validate structure
    validator.validate_structure()
    
    # Validate each post
    for post in validator.posts:
        validator.validate_post(post)
    
    # Generate and print report
    report = validator.generate_report()
    validator.print_report(report)
    
    return report

if __name__ == "__main__":
    validate()
