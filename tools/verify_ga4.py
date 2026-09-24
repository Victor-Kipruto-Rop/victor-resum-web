#!/usr/bin/env python3
"""
Verify Google Analytics (GA4) integration across all HTML files
"""

import re
from pathlib import Path

def verify_ga4_integration():
    """Verify GA4 is properly integrated"""
    
    print("=" * 80)
    print("✅ VERIFYING GOOGLE ANALYTICS (GA4) INTEGRATION")
    print("=" * 80)
    
    html_files = list(Path('.').glob('*.html')) + list(Path('dashboard').glob('*.html'))
    
    verified = 0
    missing = 0
    components = 0
    
    results = {
        'verified': [],
        'missing': [],
        'components': []
    }
    
    for file_path in sorted(html_files):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check for GA4 tracking code
        has_ga4 = 'G-D3BGPZ2LCR' in content
        has_head = '</head>' in content
        is_component = not has_head and len(content) < 5000
        
        if has_ga4:
            print(f"✅ {str(file_path):<50} GA4 installed")
            verified += 1
            results['verified'].append(str(file_path))
        elif is_component:
            print(f"📦 {str(file_path):<50} Component file (no tracking needed)")
            components += 1
            results['components'].append(str(file_path))
        else:
            print(f"❌ {str(file_path):<50} GA4 NOT FOUND")
            missing += 1
            results['missing'].append(str(file_path))
    
    print("\n" + "=" * 80)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"✅ GA4 Installed:     {verified}")
    print(f"📦 Component Files:   {components}")
    print(f"❌ Missing GA4:       {missing}")
    print(f"📝 Total Files:       {verified + components + missing}")
    print("=" * 80)
    
    if missing > 0:
        print("\n⚠️  Files missing GA4:")
        for file in results['missing']:
            print(f"  - {file}")
    
    if verified + components == verified + components + missing:
        print("\n✅ GA4 INTEGRATION VERIFIED!")
        print("🔗 View analytics: https://analytics.google.com/")
    
    return results


if __name__ == '__main__':
    verify_ga4_integration()
