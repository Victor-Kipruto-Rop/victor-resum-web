#!/usr/bin/env python3
"""
HTML Dashboard Files Verification Script
Checks all dashboard HTML files for:
1. Navigation bar presence
2. Theme toggle button
3. Proper links (Home, Blog, etc.)
4. Correct relative paths
5. Dark mode CSS variables
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class HTMLValidator:
    def __init__(self, dashboard_path: str):
        self.dashboard_path = Path(dashboard_path)
        self.results = {}
        
    def validate_files(self) -> None:
        """Validate all HTML files in dashboard folder"""
        html_files = sorted(self.dashboard_path.glob('*.html'))
        
        print("=" * 80)
        print("🔍 DASHBOARD HTML FILES VERIFICATION")
        print("=" * 80)
        print(f"\nScanning: {self.dashboard_path}")
        print(f"Found: {len(html_files)} HTML files\n")
        
        for html_file in html_files:
            self.validate_file(html_file)
        
        self.print_summary()
        self.print_detailed_report()
    
    def validate_file(self, file_path: Path) -> None:
        """Validate individual HTML file"""
        filename = file_path.name
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        checks = {
            'has_navigation': self._check_navigation(content),
            'has_theme_toggle': self._check_theme_toggle(content),
            'has_home_link': self._check_home_link(content),
            'has_blog_link': self._check_blog_link(content),
            'has_relative_paths': self._check_relative_paths(content),
            'has_dark_mode': self._check_dark_mode(content),
            'valid_body_tag': self._check_body_tag(content),
            'has_proper_head': self._check_head_tag(content),
        }
        
        self.results[filename] = {
            'checks': checks,
            'file_size': len(content),
            'total_passed': sum(1 for v in checks.values() if v),
            'total_checks': len(checks),
        }
    
    def _check_navigation(self, content: str) -> bool:
        """Check if navigation bar exists"""
        nav_patterns = [
            r'<nav',
            r'navigation',
            r'nav-logo',
            r'Victor Kipruto Rop',
        ]
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in nav_patterns)
    
    def _check_theme_toggle(self, content: str) -> bool:
        """Check if theme toggle button exists"""
        toggle_patterns = [
            r'theme-toggle|themeToggle|toggleTheme',
            r'dark-mode|darkMode',
            r'localStorage.*theme',
        ]
        return sum(1 for pattern in toggle_patterns if re.search(pattern, content)) >= 2
    
    def _check_home_link(self, content: str) -> bool:
        """Check if Home link exists with proper path"""
        home_pattern = r'href=["\']\.\.?/?index\.html["\'].*>.*Home'
        return bool(re.search(home_pattern, content, re.IGNORECASE | re.DOTALL))
    
    def _check_blog_link(self, content: str) -> bool:
        """Check if Blog link exists"""
        blog_pattern = r'href=["\']\.\./?blog\.html["\'].*>.*Blog'
        return bool(re.search(blog_pattern, content, re.IGNORECASE | re.DOTALL))
    
    def _check_relative_paths(self, content: str) -> bool:
        """Check if relative paths use ../ correctly"""
        # Should have at least some relative paths with ../
        relative_paths = re.findall(r'href=["\']\.\./', content)
        return len(relative_paths) >= 2
    
    def _check_dark_mode(self, content: str) -> bool:
        """Check if dark mode CSS exists"""
        dark_patterns = [
            r'body\.dark-mode',
            r'--ink|--paper|--accent',
            r':root\s*{',
        ]
        return sum(1 for pattern in dark_patterns if re.search(pattern, content)) >= 2
    
    def _check_body_tag(self, content: str) -> bool:
        """Check if body tag exists"""
        return bool(re.search(r'<body', content, re.IGNORECASE))
    
    def _check_head_tag(self, content: str) -> bool:
        """Check if head tag exists"""
        return bool(re.search(r'<head', content, re.IGNORECASE))
    
    def print_summary(self) -> None:
        """Print summary statistics"""
        total_files = len(self.results)
        perfect_files = sum(1 for r in self.results.values() if r['total_passed'] == r['total_checks'])
        
        print("📊 SUMMARY")
        print("-" * 80)
        print(f"Total Files:        {total_files}")
        print(f"Perfect Score:      {perfect_files} ({perfect_files*100//total_files}%)")
        print(f"Need Updates:       {total_files - perfect_files}")
        print()
    
    def print_detailed_report(self) -> None:
        """Print detailed report for each file"""
        print("📋 DETAILED REPORT")
        print("-" * 80)
        
        for filename in sorted(self.results.keys()):
            result = self.results[filename]
            passed = result['total_passed']
            total = result['total_checks']
            percentage = (passed / total * 100) if total > 0 else 0
            
            # Status indicator
            if passed == total:
                status = "✅ PASS"
            elif passed >= total * 0.75:
                status = "⚠️  PARTIAL"
            else:
                status = "❌ FAIL"
            
            print(f"\n{filename}")
            print(f"  Status: {status} ({passed}/{total} checks passed, {percentage:.0f}%)")
            
            # Show individual checks
            checks = result['checks']
            for check_name, passed_check in checks.items():
                symbol = "✓" if passed_check else "✗"
                clean_name = check_name.replace('_', ' ').title()
                print(f"    {symbol} {clean_name}")
    
    def print_file_status_table(self) -> None:
        """Print a simple table view"""
        print("\n📈 QUICK STATUS TABLE")
        print("-" * 80)
        print(f"{'File':<35} {'Status':<12} {'Score':<10}")
        print("-" * 80)
        
        for filename in sorted(self.results.keys()):
            result = self.results[filename]
            passed = result['total_passed']
            total = result['total_checks']
            score = f"{passed}/{total}"
            
            if passed == total:
                status = "✅ COMPLETE"
            elif passed >= total * 0.75:
                status = "⚠️  PARTIAL"
            else:
                status = "❌ NEEDS WORK"
            
            print(f"{filename:<35} {status:<12} {score:<10}")
        
        print("-" * 80)

def main():
    dashboard_path = str(Path(__file__).resolve().parent / 'dashboard')
    
    if not os.path.exists(dashboard_path):
        print(f"❌ Dashboard path not found: {dashboard_path}")
        return
    
    validator = HTMLValidator(dashboard_path)
    validator.validate_files()
    validator.print_file_status_table()
    
    print("\n✅ Verification complete!")

if __name__ == '__main__':
    main()
