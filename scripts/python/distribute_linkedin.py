#!/usr/bin/env python3
"""
Distribute content to LinkedIn
"""

import json
from pathlib import Path

def distribute_to_linkedin():
    """Prepare LinkedIn post content"""
    try:
        if not Path('distribution-content.json').exists():
            print("❌ No distribution content found")
            return False
        
        with open('distribution-content.json', 'r') as f:
            content = json.load(f)
        
        linkedin_post = f"🚀 New Blog Post: {content['title']}\n\n{content['description']}\n\n📂 Category: {content['category']}\n🏷️ Tags: {', '.join(content['tags'])}\n\nRead the full article: {content['url']}\n\n#DataEngineering #Python #Blog"
        
        print("LinkedIn post preview:")
        print(linkedin_post)
        print(f"\nLength: {len(linkedin_post)} chars")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    distribute_to_linkedin()
