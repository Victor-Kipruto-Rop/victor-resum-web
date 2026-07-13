#!/usr/bin/env python3
import os
import sys
import json
import logging
from dotenv import load_dotenv

# Add social-automation to path
sys.path.append('social-automation')
from linkedin import LinkedInPoster

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_linkedin():
    print("Testing LinkedIn Posting...")
    
    # Get config from env
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        print("❌ Error: LINKEDIN_ACCESS_TOKEN not found in .env")
        return

    config = {
        "platforms": {
            "linkedin": {
                "access_token": token
            }
        }
    }
    
    poster = LinkedInPoster(config)
    
    # Test data
    content = {
        "title": "Test Blog Post Integration",
        "excerpt": "This is a test post to verify LinkedIn API integration for the DBOS platform.",
        "url": "https://victorkirpruto.dev/blog/"
    }
    
    metadata = {
        "author": "Victor Kipruto Rop",
        "tags": ["Testing", "Automation", "Data Engineering"]
    }
    
    print(f"Attempting to post with token starting with: {token[:10]}...")
    result = poster.post(content, metadata)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_linkedin()
