#!/usr/bin/env python3
"""
Distribute content to Dev.to
"""

import json
from pathlib import Path

def distribute_to_devto():
    """Prepare Dev.to article content"""
    try:
        if not Path('distribution-content.json').exists():
            print("❌ No distribution content found")
            return False
        
        with open('distribution-content.json', 'r') as f:
            content = json.load(f)
        
        devto_payload = {
            "article": {
                "title": content['title'],
                "body_markdown": f"{content['description']}\n\nRead the full article on my blog: {content['url']}\n\nTags: {', '.join(content['tags'])}",
                "tags": content['tags'][:4],
                "published": True,
                "canonical_url": content['url']
            }
        }
        
        print("Dev.to article prepared:")
        print(json.dumps(devto_payload, indent=2))
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    distribute_to_devto()
