#!/usr/bin/env python3
"""LinkedIn OAuth 2.0 Helper - Generate access token."""
import os, json, urllib.request, urllib.parse
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")

# Step 1: Generate authorization URL
auth_url = (
    f"https://www.linkedin.com/oauth/v2/authorization"
    f"?response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    f"&scope=w_member_social"
    f"&state=auth_blog"
)

print("=" * 60)
print("LinkedIn OAuth 2.0 - Get Access Token")
print("=" * 60)
print()
print("STEP 1: Open this URL in your browser:")
print()
print(auth_url)
print()
print("STEP 2: After authorizing, you'll be redirected.")
print("Copy the 'code' parameter from the URL bar.")
print("Example: https://linkedin.com/developers/tools/oauth/redirect?code=ABCDEFG&state=auth_blog")
print()

# Step 2: Exchange code for token
import sys
if len(sys.argv) > 1:
    auth_code = sys.argv[1]
    print(f"Exchanging code for access token...")
    
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }).encode()
    
    req = urllib.request.Request(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        access_token = result.get("access_token")
        expires_in = result.get("expires_in")
        
        if access_token:
            print(f"\nAccess Token: {access_token}")
            print(f"Expires in: {expires_in} seconds ({expires_in//86400} days)")
            
            # Save to .env
            env_path = ".env"
            with open(env_path) as f:
                env_content = f.read()
            
            if "LINKEDIN_ACCESS_TOKEN=" in env_content:
                env_content = env_content.replace(
                    "LINKEDIN_ACCESS_TOKEN=", 
                    f"LINKEDIN_ACCESS_TOKEN={access_token}"
                )
            else:
                env_content += f"\nLINKEDIN_ACCESS_TOKEN={access_token}\n"
            
            with open(env_path, 'w') as f:
                f.write(env_content)
            
            print(f"\nToken saved to .env file!")
            print("\nTesting API connection...")
            
            # Test
            test_req = urllib.request.Request(
                "https://api.linkedin.com/v2/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "X-Restli-Protocol-Version": "2.0.0"
                }
            )
            test_resp = urllib.request.urlopen(test_req, timeout=10)
            profile = json.loads(test_resp.read())
            print(f"Connected as: {profile.get('localizedFirstName', 'Unknown')} {profile.get('localizedLastName', '')}")
        else:
            print(f"Error: {result}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("To exchange code, run: python3 linkedin_auth/linkedin_auth.py YOUR_AUTH_CODE")