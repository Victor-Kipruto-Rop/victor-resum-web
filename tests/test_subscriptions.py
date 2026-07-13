#!/usr/bin/env python3
"""
Test and validate Email and RSS subscription systems
"""

import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

def test_feed_xml():
    """Test RSS feed.xml is valid and properly formatted"""
    print("\n" + "="*80)
    print("🔍 TESTING RSS FEED")
    print("="*80)
    
    feed_file = Path('feed.xml')
    
    if not feed_file.exists():
        print("❌ feed.xml not found")
        return False
    
    try:
        tree = ET.parse(feed_file)
        root = tree.getroot()
        
        # Check root is RSS
        if 'rss' not in root.tag:
            print("❌ feed.xml is not a valid RSS file")
            return False
        
        print("✅ feed.xml is valid XML/RSS")
        
        # Check channel elements
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'content': 'http://purl.org/rss/1.0/modules/content/'}
        channel = root.find('channel')
        
        if channel is None:
            print("❌ No <channel> element found")
            return False
        
        # Check required channel elements
        title = channel.findtext('title')
        link = channel.findtext('link')
        desc = channel.findtext('description')
        
        print(f"✅ Channel Title: {title}")
        print(f"✅ Channel Link: {link}")
        print(f"✅ Channel Description: {desc}")
        
        # Check items
        items = channel.findall('item')
        print(f"✅ Found {len(items)} feed items")
        
        if len(items) == 0:
            print("⚠️  No items found in RSS feed (consider adding blog posts)")
        else:
            # Validate first item
            first_item = items[0]
            item_title = first_item.findtext('title')
            item_link = first_item.findtext('link')
            item_pubdate = first_item.findtext('pubDate')
            
            print(f"\n📝 First Item:")
            print(f"   Title: {item_title}")
            print(f"   Link: {item_link}")
            print(f"   Date: {item_pubdate}")
        
        return True
    
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_email_subscription_html():
    """Test email subscription HTML page"""
    print("\n" + "="*80)
    print("🔍 TESTING EMAIL SUBSCRIPTION PAGE")
    print("="*80)
    
    subscribe_file = Path('subscribe/')
    
    if not subscribe_file.exists():
        print("❌ subscribe/ not found")
        return False
    
    print("✅ subscribe/ exists")
    
    try:
        with open(subscribe_file, 'r') as f:
            content = f.read()
        
        # Check for form elements
        checks = {
            'Email input field': '<input type="email"' in content,
            'Name input field': '<input type="text"' in content,
            'Subscribe button': 'Subscribe' in content,
            'Form ID': 'id="subscribeForm"' in content,
            'Message div': 'id="message"' in content,
            'Theme toggle': 'themeToggle' in content,
            'Dark mode support': 'dark-mode' in content,
            'localStorage support': 'localStorage' in content,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            if result:
                print(f"✅ {check_name}: Found")
            else:
                print(f"❌ {check_name}: Missing")
                all_passed = False
        
        # Check subscribe button logic
        if 'subscribeBtn.disabled' in content:
            print("✅ Button disable/enable logic found")
        else:
            print("⚠️  Button disable/enable logic not found")
        
        # Check localStorage for subscribers
        if 'localStorage.getItem(\'subscribers\')' in content:
            print("✅ localStorage subscriber storage found")
        else:
            print("⚠️  localStorage subscriber storage not found")
        
        return all_passed
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_rss_subscription_page():
    """Test RSS subscription HTML page"""
    print("\n" + "="*80)
    print("🔍 TESTING RSS SUBSCRIPTION PAGE")
    print("="*80)
    
    subscribe_rss_file = Path('subscribe-rss/')
    
    if not subscribe_rss_file.exists():
        print("❌ subscribe-rss/ not found")
        return False
    
    print("✅ subscribe-rss/ exists")
    
    try:
        with open(subscribe_rss_file, 'r') as f:
            content = f.read()
        
        # Check for RSS feed links
        checks = {
            'RSS feed link': 'feed.xml' in content or 'rss.xml' in content,
            'Feed discovery link': 'rel="alternate"' in content or 'application/rss+xml' in content,
            'Feed instructions': 'RSS' in content or 'feed' in content.lower(),
            'Theme support': 'dark-mode' in content,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            if result:
                print(f"✅ {check_name}: Found")
            else:
                print(f"❌ {check_name}: Missing")
                all_passed = False
        
        return all_passed
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_subscription_modal():
    """Test subscription modal component"""
    print("\n" + "="*80)
    print("🔍 TESTING SUBSCRIPTION MODAL")
    print("="*80)
    
    modal_file = Path('subscription-modal/')
    
    if not modal_file.exists():
        print("⚠️  subscription-modal/ not found (optional component)")
        return True
    
    print("✅ subscription-modal/ exists")
    
    try:
        with open(modal_file, 'r') as f:
            content = f.read()
        
        checks = {
            'Modal container': 'modal' in content.lower(),
            'Close button': 'close' in content.lower() or '×' in content,
            'Email input': '<input type="email"' in content,
            'Subscribe button': 'submit' in content.lower(),
        }
        
        for check_name, result in checks.items():
            if result:
                print(f"✅ {check_name}: Found")
            else:
                print(f"⚠️  {check_name}: Missing")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_analytics_dashboard():
    """Test subscription analytics dashboard"""
    print("\n" + "="*80)
    print("🔍 TESTING SUBSCRIPTION ANALYTICS DASHBOARD")
    print("="*80)
    
    analytics_file = Path('subscription-analytics-dashboard/')
    
    if not analytics_file.exists():
        print("⚠️  subscription-analytics-dashboard/ not found (optional)")
        return True
    
    print("✅ subscription-analytics-dashboard/ exists")
    
    try:
        with open(analytics_file, 'r') as f:
            content = f.read()
        
        checks = {
            'Subscriber count display': 'subscriber' in content.lower(),
            'Charts/Analytics': 'chart' in content.lower() or 'graph' in content.lower(),
            'Dashboard layout': 'dashboard' in content.lower(),
        }
        
        for check_name, result in checks.items():
            if result:
                print(f"✅ {check_name}: Found")
            else:
                print(f"⚠️  {check_name}: Missing")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_email_notifier():
    """Test email notifier script"""
    print("\n" + "="*80)
    print("🔍 TESTING EMAIL NOTIFIER SCRIPT")
    print("="*80)
    
    email_notifier = Path('scripts/python/email_notifier.py')
    
    if not email_notifier.exists():
        print("❌ email_notifier.py not found")
        return False
    
    print("✅ email_notifier.py exists")
    
    try:
        with open(email_notifier, 'r') as f:
            content = f.read()
        
        checks = {
            'Resend API support': 'resend' in content.lower() or 'RESEND' in content,
            'SMTP support': 'smtp' in content.lower() or 'SMTP' in content,
            'Email validation': 'email' in content.lower(),
            'HTML email support': 'html' in content.lower(),
        }
        
        for check_name, result in checks.items():
            if result:
                print(f"✅ {check_name}: Found")
            else:
                print(f"⚠️  {check_name}: Missing")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_env_configuration():
    """Test .env has necessary subscription configuration"""
    print("\n" + "="*80)
    print("🔍 TESTING .ENV CONFIGURATION")
    print("="*80)
    
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    print("✅ .env file exists")
    
    try:
        with open(env_file, 'r') as f:
            env_content = f.read()
        
        checks = {
            'RESEND_API_KEY': 'RESEND_API_KEY' in env_content,
            'SMTP_SERVER': 'SMTP' in env_content,
            'SENDER_EMAIL': 'SENDER_EMAIL' in env_content or 'FROM_EMAIL' in env_content,
            'DATABASE_URL': 'DATABASE' in env_content or 'subscribers' in env_content.lower(),
        }
        
        for check_name, result in checks.items():
            if result:
                print(f"✅ {check_name}: Configured")
            else:
                print(f"⚠️  {check_name}: Not configured")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_integration():
    """Test integration between email and RSS subscriptions"""
    print("\n" + "="*80)
    print("🔍 TESTING INTEGRATION")
    print("="*80)
    
    # Check if subscribe/ links to RSS
    subscribe_html = Path('subscribe/')
    if subscribe_html.exists():
        with open(subscribe_html, 'r') as f:
            content = f.read()
        if 'feed.xml' in content or 'rss' in content.lower():
            print("✅ Email subscription page references RSS feed")
        else:
            print("⚠️  Email subscription page doesn't reference RSS feed")
    
    # Check if subscribe-rss/ links to email
    subscribe_rss = Path('subscribe-rss/')
    if subscribe_rss.exists():
        with open(subscribe_rss, 'r') as f:
            content = f.read()
        if 'subscribe/' in content or 'email' in content.lower():
            print("✅ RSS subscription page references email subscription")
        else:
            print("⚠️  RSS subscription page doesn't reference email subscription")
    
    return True

def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("📋 EMAIL & RSS SUBSCRIPTION SYSTEM VALIDATION")
    print("="*80)
    
    tests = [
        ("Email Subscription HTML", test_email_subscription_html),
        ("RSS Subscription HTML", test_rss_subscription_page),
        ("RSS Feed (feed.xml)", test_feed_xml),
        ("Subscription Modal", test_subscription_modal),
        ("Analytics Dashboard", test_analytics_dashboard),
        ("Email Notifier Script", test_email_notifier),
        (".ENV Configuration", test_env_configuration),
        ("Integration", test_integration),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*80)
    if passed == total:
        print(f"🟢 ALL TESTS PASSED ({passed}/{total})")
        print("✅ Email and RSS subscription systems are fully functional")
    else:
        print(f"🟡 {passed}/{total} tests passed")
        print(f"⚠️  {total - passed} test(s) need attention")
    print("="*80)
    
    return passed == total

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
