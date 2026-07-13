#!/usr/bin/env python3
"""
Add Google Analytics (GA4) tracking to all HTML files
Measurement ID: G-D3BGPZ2LCR
"""

import re
from pathlib import Path

GA4_SCRIPT = '''<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-D3BGPZ2LCR"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-D3BGPZ2LCR');
</script>'''

def add_ga4_to_html_files():
    """Add GA4 tracking to all HTML files"""
    
    print("=" * 80)
    print("📊 ADDING GOOGLE ANALYTICS (GA4) TO ALL HTML FILES")
    print("=" * 80)
    print(f"Measurement ID: G-D3BGPZ2LCR\n")
    
    # Files to add GA4 to
    html_files = [
        # Root pages
        'index/',
        'blog/',
        'subscribe/',
        'subscribe-rss/',
        'post/',
        'resume/',
        'success/',
        'dashboard-hub/',
        'subscription-modal/',
        'subscription-analytics-dashboard/',
        'blog-ai-dashboard/',
        
        # Dashboard pages
        'dashboard/alerts-center.html',
        'dashboard/analytics-dashboard-private.html',
        'dashboard/blog-analytics.html',
        'dashboard/blog-operations-center.html',
        'dashboard/blog-success-optimizer.html',
        'dashboard/d8k4p2x9n6m.html',
        'dashboard/hub.html',
        'dashboard/image-library.html',
        'dashboard/index-enhanced.html',
        'dashboard/index-saas.html',
        'dashboard/index-themed.html',
        'dashboard/index.html',
        'dashboard/login.html',
        'dashboard/notifications-center.html',
    ]
    
    added = 0
    skipped = 0
    errors = 0
    
    for file_path in html_files:
        path = Path(file_path)
        
        if not path.exists():
            print(f"⏭️  {file_path:<40} File not found")
            continue
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if GA4 already exists
            if 'G-D3BGPZ2LCR' in content or 'googletagmanager.com' in content:
                print(f"✅ {file_path:<40} Already has GA4")
                skipped += 1
                continue
            
            # Find the closing </head> tag
            if '</head>' not in content:
                print(f"❌ {file_path:<40} No closing </head> tag")
                errors += 1
                continue
            
            # Insert GA4 script before </head>
            new_content = content.replace('</head>', f'{GA4_SCRIPT}\n</head>', 1)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✨ {file_path:<40} GA4 tracking added")
            added += 1
            
        except Exception as e:
            print(f"❌ {file_path:<40} Error: {str(e)}")
            errors += 1
    
    print("\n" + "=" * 80)
    print(f"📊 SUMMARY")
    print("=" * 80)
    print(f"  ✨ Added:   {added}")
    print(f"  ✅ Skipped: {skipped} (already has GA4)")
    print(f"  ❌ Errors:  {errors}")
    print(f"  📝 Total:   {added + skipped + errors}")
    print("=" * 80)
    print("\n✅ Google Analytics integration complete!")
    print("🔗 View reports: https://analytics.google.com/")
    

if __name__ == '__main__':
    add_ga4_to_html_files()
