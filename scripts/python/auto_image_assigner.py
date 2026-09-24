#!/usr/bin/env python3
"""
DBOS Auto Image Assigner
Automatically assigns images to blog posts and generates social media assets
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from image_selector import ImageSelector
from config import Config

class AutoImageAssigner:
    """Automatically assign images to all blog posts"""
    
    def __init__(self):
        self.selector = ImageSelector()
        self.posts_file = Path('blog/posts.json')
        self.assignment_log_file = Path('assets/auto/assignment-log.json')
        self.social_metadata_file = Path('assets/auto/social-metadata.json')
        self.assignment_log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load_posts(self) -> List[Dict]:
        """Load blog posts"""
        if self.posts_file.exists():
            with open(self.posts_file) as f:
                return json.load(f)
        return []
    
    def save_posts(self, posts: List[Dict]):
        """Save blog posts with updated images"""
        with open(self.posts_file, 'w') as f:
            json.dump(posts, f, indent=2)
    
    def assign_images_to_posts(self, posts: List[Dict]) -> Dict[str, Dict]:
        """Assign images to all posts"""
        results = {}
        
        print("📝 Assigning images to posts...\n")
        
        for post in posts:
            slug = post.get("slug")
            
            # Skip if already has manual image
            if post.get("image") and not post.get("image").startswith("assets/auto/"):
                print(f"⊘ {slug}: Already has manual image")
                continue
            
            # Select best image
            image, details = self.selector.select_image(post)
            
            # Update post
            post["image"] = image.path
            post["image_assignment"] = {
                "timestamp": datetime.utcnow().isoformat(),
                "method": "auto_selected",
                "image_name": image.name,
                "score": details["score"],
                "matches": details["matches"]
            }
            
            results[slug] = {
                "image": image.path,
                "details": details,
                "status": "assigned"
            }
            
            print(f"✓ {slug}")
            print(f"  → Image: {image.name}")
            print(f"  → Score: {details['score']:.1f}")
        
        return results
    
    def generate_social_metadata(self, posts: List[Dict]) -> Dict[str, Dict]:
        """Generate Open Graph and social media metadata for posts"""
        social_metadata = {}
        base_url = Config.BASE_URL
        
        print("\n🌐 Generating social media metadata...\n")
        
        for post in posts:
            if post.get("status") != "published":
                continue
            
            slug = post.get("slug")
            image_path = post.get("image", "assets/auto/default-tech.png")
            
            # Ensure absolute URLs for social sharing
            if not image_path.startswith("http"):
                image_url = f"{base_url}/{image_path}"
            else:
                image_url = image_path
            
            # Generate metadata
            metadata = {
                "title": post.get("title"),
                "description": post.get("description", ""),
                "url": f"{base_url}/blog/posts/{slug}",
                "image": image_url,
                "type": "article",
                "author": "Victor Kipruto",
                "publish_date": post.get("publishDate"),
                "update_date": post.get("updatedDate"),
                "category": post.get("category"),
                "tags": post.get("tags", []),
                "read_time": post.get("readTime"),
                
                # Open Graph
                "og": {
                    "title": post.get("title"),
                    "description": post.get("description", ""),
                    "image": image_url,
                    "url": f"{base_url}/blog/posts/{slug}",
                    "type": "article",
                    "site_name": "Victor Kipruto - Developer"
                },
                
                # Twitter Card
                "twitter": {
                    "card": "summary_large_image",
                    "title": post.get("title")[:70],  # Twitter limit
                    "description": post.get("description", "")[:200],
                    "image": image_url,
                    "creator": "@victor_kipruto",
                    "site": "@victor_kipruto"
                },
                
                # LinkedIn
                "linkedin": {
                    "title": post.get("title"),
                    "description": post.get("description", ""),
                    "image": image_url,
                    "url": f"{base_url}/blog/posts/{slug}"
                },
                
                # Telegram
                "telegram": {
                    "title": post.get("title"),
                    "description": post.get("description", ""),
                    "image": image_url
                }
            }
            
            social_metadata[slug] = metadata
            print(f"✓ {slug} - Social metadata generated")
        
        return social_metadata
    
    def save_social_metadata(self, metadata: Dict[str, Dict]):
        """Save social media metadata"""
        with open(self.social_metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n✓ Saved social metadata: {self.social_metadata_file}")
    
    def generate_social_preview_html(self, post: Dict) -> str:
        """Generate HTML meta tags for social sharing"""
        slug = post.get("slug")
        title = post.get("title", "")
        description = post.get("description", "")
        image = post.get("image", "assets/auto/default-tech.png")
        url = f"{Config.BASE_URL}/blog/posts/{slug}"
        
        if not image.startswith("http"):
            image_url = f"{Config.BASE_URL}/{image}"
        else:
            image_url = image
        
        html = f"""
<!-- Open Graph Meta Tags -->
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:image" content="{image_url}" />
<meta property="og:url" content="{url}" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Victor Kipruto - Developer" />

<!-- Twitter Card Meta Tags -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title[:70]}" />
<meta name="twitter:description" content="{description[:200]}" />
<meta name="twitter:image" content="{image_url}" />
<meta name="twitter:creator" content="@victor_kipruto" />
<meta name="twitter:site" content="@victor_kipruto" />

<!-- Additional Meta Tags -->
<meta name="image" content="{image_url}" />
<meta name="description" content="{description}" />
"""
        
        return html
    
    def log_assignment(self, results: Dict[str, Dict], social_metadata: Dict[str, Dict]):
        """Log image assignments"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "posts_processed": len(results),
            "assignments": results,
            "social_metadata_count": len(social_metadata)
        }
        
        logs = []
        if self.assignment_log_file.exists():
            with open(self.assignment_log_file) as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(self.assignment_log_file, 'w') as f:
            json.dump(logs[-100:], f, indent=2)  # Keep last 100
    
    def generate_assignment_report(self, results: Dict[str, Dict]) -> str:
        """Generate report of assignments"""
        report = f"""
📊 IMAGE ASSIGNMENT REPORT

Timestamp: {datetime.utcnow().isoformat()}
Posts Processed: {len(results)}

Results by Status:
"""
        
        status_counts = {}
        for result in results.values():
            status = result.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in sorted(status_counts.items()):
            report += f"  • {status}: {count}\n"
        
        # Show sample assignments
        report += f"\nSample Assignments:\n"
        for i, (slug, result) in enumerate(list(results.items())[:5]):
            image = result.get("image", "unknown")
            score = result.get("details", {}).get("score", 0)
            report += f"  {i+1}. {slug}\n     Image: {image} (Score: {score:.1f})\n"
        
        return report
    
    def run(self):
        """Execute auto image assignment"""
        print("\n🎨 DBOS Auto Image Assigner\n")
        
        # Load posts
        posts = self.load_posts()
        if not posts:
            print("⚠️  No posts found")
            return
        
        print(f"Found {len(posts)} posts\n")
        
        # Assign images
        assignment_results = self.assign_images_to_posts(posts)
        
        # Save updated posts
        self.save_posts(posts)
        print(f"\n✓ Saved updated posts: {self.posts_file}")
        
        # Generate social metadata
        social_metadata = self.generate_social_metadata(posts)
        self.save_social_metadata(social_metadata)
        
        # Log assignments
        self.log_assignment(assignment_results, social_metadata)
        
        # Generate and print report
        report = self.generate_assignment_report(assignment_results)
        print(report)
        
        print("\n✅ Auto image assignment complete!\n")

if __name__ == '__main__':
    assigner = AutoImageAssigner()
    assigner.run()
