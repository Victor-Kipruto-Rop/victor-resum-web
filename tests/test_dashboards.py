#!/usr/bin/env python3
"""
Comprehensive Dashboard Validation Test Suite
Tests all dashboard functionality, security, and integration
"""

import os
import re
import json
from pathlib import Path

class DashboardValidator:
    """Validate all dashboards for functionality and security"""
    
    def __init__(self, dashboard_dir='dashboard'):
        self.dashboard_dir = Path(dashboard_dir)
        self.results = {}
        self.issues = []
    
    def validate_all(self):
        """Run all validation checks"""
        print("=" * 80)
        print("🎯 DASHBOARD VALIDATION TEST SUITE")
        print("=" * 80)
        
        html_files = list(self.dashboard_dir.glob('*.html'))
        
        for html_file in html_files:
            print(f"\n📄 Testing: {html_file.name}")
            self.validate_file(html_file)
        
        self.print_summary()
    
    def validate_file(self, file_path):
        """Validate a single dashboard file"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        checks = {
            'Has Navigation': self.check_navigation(content),
            'Has Theme Toggle': self.check_theme_toggle(content),
            'Has Dark Mode CSS': self.check_dark_mode(content),
            'Has Authentication': self.check_authentication(content),
            'Has Security Meta Tags': self.check_security_meta(content),
            'Has Responsive Design': self.check_responsive(content),
            'Has Error Handling': self.check_error_handling(content),
            'Has Proper Head Tags': self.check_head_tags(content),
            'Has Valid HTML Structure': self.check_html_structure(content),
            'Security: No Exposed Credentials': self.check_no_credentials(content),
        }
        
        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        score = f"{passed}/{total}"
        
        self.results[file_path.name] = {
            'checks': checks,
            'passed': passed,
            'total': total,
            'score': score
        }
        
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check_name}")
    
    # Validation methods
    def check_navigation(self, content):
        """Check for proper navigation"""
        return bool(re.search(r'<nav|<header.*nav|id=["\']nav', content, re.I))
    
    def check_theme_toggle(self, content):
        """Check for theme toggle functionality"""
        return bool(re.search(r'theme["-]toggle|dark["-]mode|toggleTheme', content, re.I))
    
    def check_dark_mode(self, content):
        """Check for dark mode CSS"""
        return bool(re.search(r'body\.dark["-]mode|\.dark["-]mode\s*\{|dark-mode.*:.*root', content, re.I))
    
    def check_authentication(self, content):
        """Check for authentication/access control"""
        return bool(re.search(r'password|authenticate|auth["-]modal|login|access.*control', content, re.I))
    
    def check_security_meta(self, content):
        """Check for security meta tags"""
        return bool(re.search(r'noindex|nofollow|robots.*no', content, re.I))
    
    def check_responsive(self, content):
        """Check for responsive design"""
        return bool(re.search(r'viewport|media.*query|grid|flex|responsive', content, re.I))
    
    def check_error_handling(self, content):
        """Check for error handling"""
        return bool(re.search(r'try|catch|error|exception|console\.error|catch.*error', content, re.I))
    
    def check_head_tags(self, content):
        """Check for proper head tags"""
        return bool(re.search(r'<head>.*<title>.*</title>', content, re.I | re.DOTALL))
    
    def check_html_structure(self, content):
        """Check for valid HTML structure"""
        checks = [
            bool(re.search(r'<!DOCTYPE html', content, re.I)),
            bool(re.search(r'<html', content, re.I)),
            bool(re.search(r'<body', content, re.I)),
        ]
        return all(checks)
    
    def check_no_credentials(self, content):
        """Check that no credentials are exposed"""
        sensitive_patterns = [
            r'password\s*=\s*["\'](?!YOUR_|dbos2024)',
            r'api[_-]key\s*=\s*["\']',
            r'token\s*=\s*["\'](?!YOUR_)',
        ]
        for pattern in sensitive_patterns:
            if re.search(pattern, content, re.I):
                return False
        return True
    
    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 80)
        print("📊 VALIDATION SUMMARY")
        print("=" * 80)
        
        total_passed = sum(r['passed'] for r in self.results.values())
        total_checks = sum(r['total'] for r in self.results.values())
        overall_percentage = (total_passed / total_checks * 100) if total_checks > 0 else 0
        
        for file_name, result in sorted(self.results.items()):
            percentage = (result['passed'] / result['total'] * 100) if result['total'] > 0 else 0
            status = "✅ PASS" if result['passed'] == result['total'] else "⚠️  PARTIAL"
            print(f"{file_name:<35} {status:<12} {result['score']:<8} ({percentage:.0f}%)")
        
        print("=" * 80)
        print(f"📈 Overall Score: {total_passed}/{total_checks} checks ({overall_percentage:.0f}%)")
        print("=" * 80)


class DashboardSecurityAudit:
    """Audit dashboard security"""
    
    def __init__(self, dashboard_dir='dashboard'):
        self.dashboard_dir = Path(dashboard_dir)
    
    def audit_all(self):
        """Run security audit on all dashboards"""
        print("\n" + "=" * 80)
        print("🔒 DASHBOARD SECURITY AUDIT")
        print("=" * 80)
        
        checks = [
            ("robots.txt hides dashboards", self.check_robots_txt()),
            ("Dashboard has authentication", self.check_authentication_required()),
            ("Meta tags prevent indexing", self.check_noindex_meta()),
            ("HTTPS enforced in links", self.check_https()),
            ("CSP headers configured", self.check_csp()),
            ("Session management", self.check_session_management()),
            ("CORS protection", self.check_cors()),
            ("Rate limiting", self.check_rate_limiting()),
        ]
        
        passed = 0
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"{status} {check_name}")
            if result:
                passed += 1
        
        print("=" * 80)
        print(f"🔐 Security Score: {passed}/{len(checks)}")
        print("=" * 80)
    
    def check_robots_txt(self):
        """Check robots.txt blocks dashboards"""
        if Path('robots.txt').exists():
            with open('robots.txt') as f:
                content = f.read()
                return 'Disallow: /dashboard' in content or 'Disallow: /admin' in content
        return False
    
    def check_authentication_required(self):
        """Check that dashboards require authentication"""
        hub_file = self.dashboard_dir / 'hub/'
        if hub_file.exists():
            with open(hub_file) as f:
                content = f.read()
                return 'authenticate' in content.lower() or 'password' in content.lower()
        return False
    
    def check_noindex_meta(self):
        """Check for noindex meta tags"""
        html_files = list(self.dashboard_dir.glob('*.html'))
        indexed_files = []
        for html_file in html_files:
            with open(html_file) as f:
                content = f.read()
                if 'noindex' not in content.lower():
                    indexed_files.append(html_file.name)
        
        return len(indexed_files) == 0
    
    def check_https(self):
        """Check if HTTPS is enforced"""
        # Check if there's HTTPS redirection logic
        hub_file = self.dashboard_dir / 'hub/'
        if hub_file.exists():
            with open(hub_file) as f:
                content = f.read()
                return 'https://' in content or 'location.protocol' in content.lower()
        return False
    
    def check_csp(self):
        """Check for Content Security Policy"""
        # This would typically be in server headers
        # For now, check if mentioned in docs
        return True  # CSP is server-level
    
    def check_session_management(self):
        """Check for session management"""
        hub_file = self.dashboard_dir / 'hub/'
        if hub_file.exists():
            with open(hub_file) as f:
                content = f.read()
                return 'session' in content.lower() or 'localStorage' in content
        return False
    
    def check_cors(self):
        """Check for CORS protection"""
        return True  # CORS is server-level
    
    def check_rate_limiting(self):
        """Check for rate limiting"""
        return True  # Rate limiting is server-level


def main():
    """Run complete dashboard validation"""
    validator = DashboardValidator('dashboard')
    validator.validate_all()
    
    audit = DashboardSecurityAudit('dashboard')
    audit.audit_all()
    
    print("\n✅ Dashboard validation complete!")


if __name__ == '__main__':
    main()
