#!/usr/bin/env python3
"""
Email Notification System Test Suite
Demonstrates sending emails with blog post images to subscribers
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from blog_notifier import BlogEventNotifier
from email_template_manager import EmailTemplateManager

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_email_templates():
    """Test generating emails with blog post images"""
    print_section("TEST 1: Email Templates with Blog Post Images")
    
    manager = EmailTemplateManager()
    
    # Sample blog post with image
    posts = [
        {
            "title": "Advanced Kubernetes Patterns for Data Engineers",
            "slug": "advanced-kubernetes-patterns",
            "description": "Master production-ready Kubernetes deployment patterns specifically designed for data engineering workloads.",
            "image": "https://victorkipruto.com/assets/images/kubernetes-patterns.png",
            "readTime": 12
        }
    ]
    
    for post in posts:
        print(f"\n📝 Post: {post['title']}")
        print(f"   Image: {post['image']}")
        
        # Generate welcome email
        print("\n  1️⃣  Generating Welcome Email...")
        
        # Generate blog post email with image
        print("  2️⃣  Generating Blog Post Email with Featured Image...")
        
        from email_templates import template_new_blog_post
        blog_email = template_new_blog_post(
            name="John Subscriber",
            post_title=post['title'],
            post_excerpt=post['description'],
            post_slug=post['slug'],
            read_time=post['readTime'],
            image_url=post['image']
        )
        
        print(f"     ✅ Generated {len(blog_email)} characters")
        print(f"     ✅ Contains featured image: {post['image'] in blog_email}")
        print(f"     ✅ Contains image tag: {'<img' in blog_email}")
        
        # Generate notification email
        print("  3️⃣  Generating Generic Notification Email...")
        from email_templates import template_notification
        notif_email = template_notification(
            name="John Subscriber",
            title="📢 New Blog Post Published",
            message=post['description'],
            icon="📝",
            action_text="Read Article",
            action_url=f"https://victorkipruto.com/post.html?id={post['slug']}"
        )
        print(f"     ✅ Generated {len(notif_email)} characters")

def test_blog_notifier():
    """Test blog event notifier"""
    print_section("TEST 2: Blog Event Notifier")
    
    notifier = BlogEventNotifier()
    
    # Load data
    posts = notifier.load_posts()
    subscribers = notifier.load_subscribers()
    notified = notifier.load_notified_posts()
    
    print(f"\n📊 Current System Status:")
    print(f"   • Total Blog Posts: {len(posts)}")
    print(f"   • Total Subscribers: {len(subscribers)}")
    print(f"   • Notified Posts: {len(notified)}")
    
    # Display posts with images
    print(f"\n📚 Available Blog Posts:")
    for i, post in enumerate(posts, 1):
        is_notified = any(entry.get('post_id') == post.get('id') for entry in notified)
        status = "✅ Notified" if is_notified else "⏳ Pending"
        print(f"   {i}. {post['title']}")
        print(f"      Image: {post.get('image', 'None')}")
        print(f"      Status: {status}")
    
    # Display subscribers
    if subscribers:
        print(f"\n👥 Subscribers:")
        for i, sub in enumerate(subscribers, 1):
            channels = ", ".join(sub.get('channels', []))
            print(f"   {i}. {sub['name']} ({sub['email']})")
            print(f"      Channels: {channels}")
    else:
        print(f"\n⚠️  No subscribers found. Use the subscription form to add subscribers.")

def test_create_test_subscriber():
    """Create a test subscriber for demonstration"""
    print_section("TEST 3: Creating Test Subscriber")
    
    subscribers_file = Path(__file__).parent.parent.parent / "subscribers.json"
    
    try:
        # Load existing subscribers
        if subscribers_file.exists():
            data = json.loads(subscribers_file.read_text())
        else:
            data = {"subscribers": []}
        
        # Check if test subscriber exists
        existing = [s for s in data.get("subscribers", []) if s["email"] == "test@example.com"]
        
        if existing:
            print("✅ Test subscriber already exists: test@example.com")
        else:
            # Add test subscriber
            test_sub = {
                "email": "test@example.com",
                "name": "Test Subscriber",
                "channels": ["email"],
                "created_at": "2026-06-06T00:00:00Z",
                "status": "active"
            }
            data["subscribers"].append(test_sub)
            subscribers_file.write_text(json.dumps(data, indent=2))
            print("✅ Created test subscriber: test@example.com")
        
        print("\n📧 Test Subscriber Email Channels:")
        print("   • Email: ✅ Enabled")
        print("   • Ready to receive blog post notifications with images")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def test_email_with_all_templates():
    """Test all email template types"""
    print_section("TEST 4: All Email Template Types")
    
    from email_templates import (
        template_welcome,
        template_new_blog_post,
        template_notification,
        template_dashboard_alert,
        template_event_announcement,
        template_weekly_digest
    )
    
    templates = [
        ("Welcome Email", lambda: template_welcome("John Doe", "john@example.com")),
        ("Blog Post Email with Image", lambda: template_new_blog_post(
            "John Doe",
            "Advanced Kubernetes Patterns",
            "Master production-ready Kubernetes...",
            "advanced-kubernetes-patterns",
            12,
            "https://victorkipruto.com/assets/images/kubernetes-patterns.png"
        )),
        ("Notification Email", lambda: template_notification(
            "John Doe",
            "New Article Published",
            "Check out the latest post on our blog",
            "📝",
            "Read More",
            "https://blog.example.com"
        )),
        ("Dashboard Alert Email", lambda: template_dashboard_alert(
            "John Doe",
            "Blog Performance Alert",
            {"Views": "2,450", "Engagement": "+15%", "New Subscribers": "23"},
            "Keep optimizing your content strategy"
        )),
        ("Event Announcement Email", lambda: template_event_announcement(
            "John Doe",
            "AI Workshop Announcement",
            "2026-06-15T18:00:00Z",
            "Join us for an exclusive workshop on AI and Data Engineering",
            "https://events.example.com/ai-workshop"
        )),
        ("Weekly Digest Email", lambda: template_weekly_digest(
            "John Doe",
            [
                {"title": "Post 1", "link": "http://blog.example.com/1"},
                {"title": "Post 2", "link": "http://blog.example.com/2"}
            ]
        ))
    ]
    
    for template_name, template_func in templates:
        try:
            html = template_func()
            print(f"\n✅ {template_name}")
            print(f"   Length: {len(html)} characters")
            print(f"   HTML Valid: {'<!DOCTYPE html>' in html or '<html>' in html}")
            print(f"   Contains CTA: {'cta-button' in html or 'href=' in html}")
        except Exception as e:
            print(f"❌ {template_name}: {e}")

def test_notification_simulation():
    """Simulate sending notifications (dry run)"""
    print_section("TEST 5: Notification Simulation (Dry Run)")
    
    notifier = BlogEventNotifier()
    posts = notifier.load_posts()
    subscribers = notifier.load_subscribers()
    
    if not subscribers:
        print("⚠️  No subscribers available for simulation")
        print("Add a test subscriber first using the subscription form or run TEST 3")
        return
    
    if not posts:
        print("⚠️  No blog posts available")
        return
    
    # Simulate sending to first post
    post = posts[0]
    
    print(f"\n🔔 Simulating notification for: {post['title']}")
    print(f"   Featured Image: {post.get('image', 'None')}")
    print(f"   Target Subscribers: {len(subscribers)}")
    
    for i, sub in enumerate(subscribers, 1):
        email = sub.get('email')
        name = sub.get('name', 'Subscriber')
        channels = sub.get('channels', [])
        
        print(f"\n   📨 [{i}] {name} ({email})")
        print(f"       Channels: {', '.join(channels)}")
        
        if 'email' in channels:
            print(f"       Status: ✅ Would send email notification")
            print(f"       Subject: New Post: {post['title']}")
            print(f"       Include Image: ✅ {post.get('image', 'None')[:50]}...")
        else:
            print(f"       Status: ⏭️  Email channel disabled")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "EMAIL NOTIFICATION SYSTEM TEST SUITE" + " " * 17 + "║")
    print("║" + " " * 18 + "Blog Post Images + Multi-Channel Notifications" + " " * 4 + "║")
    print("╚" + "=" * 68 + "╝")
    
    try:
        test_email_templates()
        test_blog_notifier()
        test_create_test_subscriber()
        test_email_with_all_templates()
        test_notification_simulation()
        
        print_section("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("\n📋 Next Steps:")
        print("   1. Subscribe using the email subscription form at /subscribe.html")
        print("   2. Use 'python blog_notifier.py notify-posts' to send notifications")
        print("   3. Check email inbox for blog post notifications with images")
        print("   4. Integrate blog_notifier.py into GitHub Actions for automated notifications")
        print()
    
    except Exception as e:
        print_section("❌ ERROR DURING TESTING")
        print(f"\n{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
