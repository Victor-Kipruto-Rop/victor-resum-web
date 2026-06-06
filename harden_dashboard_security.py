#!/usr/bin/env python3
"""
Dashboard Security Hardening - Add security meta tags to all dashboards
"""

import re
from pathlib import Path

def add_security_meta_tags(dashboard_dir='dashboard'):
    """Add security meta tags to all dashboard HTML files"""
    
    dashboard_dir = Path(dashboard_dir)
    meta_tag = '    <meta name="robots" content="noindex, nofollow">'
    
    print("=" * 80)
    print("🔒 ADDING SECURITY META TAGS TO DASHBOARDS")
    print("=" * 80)
    
    for html_file in sorted(dashboard_dir.glob('*.html')):
        with open(html_file, 'r') as f:
            content = f.read()
        
        # Check if already has the meta tag
        if 'noindex' in content and 'nofollow' in content:
            print(f"✅ {html_file.name:<35} Already has security meta tags")
            continue
        
        # Find the closing </head> tag and insert before it
        if '</head>' in content:
            # Find the position of </head>
            head_close_pos = content.find('</head>')
            
            # Insert the meta tag before </head>
            new_content = content[:head_close_pos] + meta_tag + '\n    ' + content[head_close_pos:]
            
            with open(html_file, 'w') as f:
                f.write(new_content)
            
            print(f"✨ {html_file.name:<35} Security meta tags added")
        else:
            print(f"⚠️  {html_file.name:<35} No closing </head> tag found")
    
    print("=" * 80)
    print("✅ Security hardening complete!")
    print("=" * 80)


if __name__ == '__main__':
    add_security_meta_tags()
