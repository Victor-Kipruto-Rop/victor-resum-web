# 🤖 Blog AI Engine - Complete Setup & Automation Guide

Victor Kipruto Rop's AI-powered blog generation and email notification system.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Automation & Scheduling](#automation--scheduling)
- [Email Notifications](#email-notifications)
- [GitHub Auto-Deploy](#github-auto-deploy)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### AI Post Generation
- **Claude AI Integration**: Uses Claude 3 Sonnet for intelligent blog post generation
- **Multi-turn Conversations**: Outline → Content → Metadata extraction
- **Smart Structuring**: Automatically creates well-organized posts with code examples
- **Topic Management**: Choose from predefined data engineering topics or specify custom titles

### Email Notifications
- **Subscriber Management**: SQLite database for subscriber tracking
- **Verification System**: Double opt-in with email verification
- **HTML Email Templates**: Modern, responsive email designs
- **SendGrid Integration**: Professional email delivery (with SMTP fallback)
- **Batch Notifications**: Send to all active subscribers

### Automation
- **Scheduled Generation**: Generate posts on a regular schedule (e.g., every Monday at 9 AM)
- **Auto-Push to GitHub**: Automatically commit and push new posts
- **Logging**: Comprehensive logging for debugging
- **State Management**: Tracks last generation time and statistics

### Web Interface
- **Subscription Page**: `subscribe.html` - Modern subscription interface
- **Blog Hub**: `blog.html` - Browse all posts with search and filtering
- **Post Template**: `post.html` - Individual post display
- **Dark/Light Theme**: Theme toggle with localStorage persistence

---

## 🏗️ Architecture

```
blog-ai/
├── generate.py              # AI post generator (Claude API)
├── email_notifier.py        # Email management and sending
├── scheduler.py             # Automated scheduling
├── api_server.py            # Flask API backend
├── config.json              # Configuration and settings
├── prompts.json             # AI writing instructions
├── template.md              # Post template for AI
├── requirements.txt         # Python dependencies
├── .env.example              # Environment variables template
├── push.sh                  # GitHub auto-deploy script
└── templates/
    └── (email templates)

blog-ai-posts/              # Generated blog post markdown files
├── post-id-1.md            # Generated markdown content
├── post-id-1.meta.json     # Post metadata (title, tags, etc)
├── post-id-2.md
└── post-id-2.meta.json

subscribers.db              # SQLite database for subscribers
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Git
- Anthropic API key (Claude)
- SendGrid API key (for email)
- GitHub token (for auto-deploy)

### Step 1: Install Dependencies

```bash
cd ~/Desktop/resume/blog-ai
pip install -r requirements.txt
```

**If you get permission errors**, use:
```bash
pip install --user -r requirements.txt
```

### Step 2: Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```bash
nano .env
```

Required values:
```env
ANTHROPIC_API_KEY=sk-ant-...
SENDGRID_API_KEY=SG....
GITHUB_TOKEN=ghp_...
```

### Step 3: Initialize Database

```bash
python3 -c "from email_notifier import EmailNotifier; EmailNotifier()"
```

This creates `subscribers.db` in the parent directory.

---

## ⚙️ Configuration

### config.json

Main configuration file with author info, blog settings, and AI parameters.

```json
{
  "author": {
    "name": "Victor Kipruto Rop",
    "email": "kiprutovictor39@gmail.com",
    "bio": "Data Engineer...",
    "twitter": "@kiprutovictor39",
    "linkedin": "victor-kipruto-rop",
    "github": "Victor-Kipruto-Rop"
  },
  "blog": {
    "title": "Technical Blog - Victor Kipruto Rop",
    "posts_per_month": 2,
    "publish_day": "monday",
    "publish_time": "09:00"
  },
  "ai": {
    "model": "claude-3-sonnet-20240229",
    "temperature": 0.7,
    "max_tokens": 2000
  },
  "email": {
    "service": "sendgrid",
    "from_email": "blog@victorkirpruto.dev"
  },
  "github": {
    "repo": "Victor-Kipruto-Rop/portfolio",
    "auto_push": true
  }
}
```

### prompts.json

AI writing instructions and quality guidelines:
- System prompt and tone
- Post structure requirements
- Content rules
- SEO optimization
- Quality checks

### template.md

Markdown template that AI uses as a structure guide for generating posts.

---

## 🎯 Quick Start

### Generate a Single Post

```bash
python3 generate.py
```

Or specify a title:
```bash
python3 generate.py --title "Advanced Kafka Patterns for Real-time Data"
```

**Output:**
- `blog-ai-posts/post-id.md` - Generated markdown content
- `blog-ai-posts/post-id.meta.json` - Post metadata

### Generate Multiple Posts

```bash
python3 generate.py --count 3
```

### Start Email API Server

```bash
python3 api_server.py --port 5000
```

**Endpoints:**
- `POST /api/subscribe` - Subscribe to blog
- `GET /api/verify-email?token=...` - Verify subscription
- `GET /api/stats` - Get blog statistics

### Start Scheduler (Daemon Mode)

```bash
python3 scheduler.py
```

**Options:**
- `--now` - Generate post immediately
- `--test` - Test email notifications

---

## 🔌 API Endpoints

### Subscribe to Blog
**POST** `/api/subscribe`

```bash
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

Response:
```json
{
  "status": "success",
  "message": "Verification email sent. Please check your inbox.",
  "email": "john@example.com"
}
```

### Verify Email
**GET** `/api/verify-email?token=ABC123...`

Redirects to confirmation page with status.

### Get Stats
**GET** `/api/stats`

```json
{
  "total_subscribers": 42,
  "verified_subscribers": 38,
  "active_subscribers": 35,
  "blog": {
    "title": "Technical Blog - Victor Kipruto Rop",
    "author": "Victor Kipruto Rop",
    "topics": 10
  }
}
```

### Health Check
**GET** `/api/health`

```json
{
  "status": "healthy",
  "timestamp": "2024-06-06T12:00:00",
  "service": "Blog API Server"
}
```

---

## 📅 Automation & Scheduling

### Run Scheduler Continuously

```bash
python3 scheduler.py
```

The scheduler will:
1. ✅ Generate a blog post at the configured time
2. 📧 Notify all subscribers via email
3. 📤 Auto-push to GitHub (if enabled)
4. 📝 Log all activities

### Manual Post Generation

```bash
# Generate immediately without scheduling
python3 scheduler.py --now

# Test email notifications
python3 scheduler.py --test
```

### Systemd Service (Linux)

Create `/etc/systemd/system/blog-scheduler.service`:

```ini
[Unit]
Description=Blog AI Scheduler
After=network.target

[Service]
Type=simple
User=kipruto
WorkingDirectory=/home/kipruto/Desktop/resume/blog-ai
ExecStart=/usr/bin/python3 scheduler.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable blog-scheduler.service
sudo systemctl start blog-scheduler.service

# Check status
sudo systemctl status blog-scheduler.service
```

### Cron Job (Any OS)

```bash
# Edit crontab
crontab -e

# Add this line to generate posts every Monday at 9 AM
0 9 * * 1 cd /home/kipruto/Desktop/resume/blog-ai && python3 scheduler.py --now
```

---

## 📧 Email Notifications

### Email Template Features

✅ Modern HTML design
✅ Responsive (mobile-friendly)
✅ Post metadata (date, read time)
✅ Tags display
✅ Direct link to article
✅ Author information
✅ Unsubscribe link

### Subscriber Database

The system uses SQLite to track:
- Email address
- Name
- Subscription date
- Verification status
- Unsubscribe token
- Activity status

**Database path:** `/home/kipruto/Desktop/resume/subscribers.db`

### Managing Subscribers

```python
from email_notifier import EmailNotifier

notifier = EmailNotifier()

# Get stats
stats = notifier.get_stats()
print(f"Active subscribers: {stats['active_subscribers']}")

# Get all subscribers
subscribers = notifier.get_active_subscribers()

# Manually send notification
post_data = {
    "title": "New Post Title",
    "excerpt": "Short excerpt...",
    "read_time": 10,
    "tags": ["python", "data"],
    "url": "https://victorkirpruto.dev/post.html?id=post-id",
    "published_date": "June 6, 2024",
    "author": "Victor Kipruto Rop"
}
notifier.send_new_post_notification(post_data)
```

---

## 🚀 GitHub Auto-Deploy

### Setup

1. **Generate GitHub Token:**
   - Go to https://github.com/settings/tokens
   - Create token with `repo` and `workflow` scopes
   - Add to `.env`: `GITHUB_TOKEN=ghp_...`

2. **Enable Auto-Push:**
   - In `config.json`: `"auto_push": true`

3. **Configure Repository:**
   - In `config.json`: `"repo": "Victor-Kipruto-Rop/portfolio"`

### Manual Deployment

```bash
bash push.sh "📝 New blog post"
```

### Automatic Deployment

When scheduler generates a post and `auto_push` is enabled:

1. ✅ Commits all changes with AI post files
2. ✅ Pushes to GitHub main branch
3. ✅ Updates feed.xml automatically
4. ✅ Logs deployment status

**What gets committed:**
- `blog-ai-posts/*.md` - Markdown content
- `blog-ai-posts/*.meta.json` - Post metadata
- `blog.html` - Updated blog hub
- `posts.js` - Updated post list (auto-generated)
- `feed.xml` - Updated RSS feed

---

## 🐛 Troubleshooting

### API Key Issues

**Problem:** `AuthenticationError: Invalid API key`

**Solution:**
1. Check `.env` file exists: `ls -la .env`
2. Verify key is correct: `head -1 .env`
3. Test API: `python3 -c "from anthropic import Anthropic; print(Anthropic())"`

### Database Issues

**Problem:** `sqlite3.OperationalError: database is locked`

**Solution:**
1. Close any other processes accessing the database
2. Delete and recreate: `rm subscribers.db && python3 -c "from email_notifier import EmailNotifier; EmailNotifier()"`

### Email Not Sending

**Problem:** Emails not arriving in subscriber inboxes

**Solutions:**
1. **Test SendGrid connection:**
   ```bash
   python3 scheduler.py --test
   ```

2. **Check SENDGRID_API_KEY:**
   ```bash
   grep SENDGRID .env
   ```

3. **Verify email address:**
   - Check `subscribers.db` for verified status
   - Is subscriber marked as `verified = 1`?

4. **Check logs:**
   ```bash
   tail -50 blog_scheduler.log
   ```

### Git Push Fails

**Problem:** `Failed to push to GitHub`

**Solutions:**
1. **Verify git config:**
   ```bash
   git config --global user.name
   git config --global user.email
   ```

2. **Test git access:**
   ```bash
   git status
   cd .. && git push --dry-run
   ```

3. **Update token:**
   - Regenerate at https://github.com/settings/tokens
   - Update `.env` with new token

---

## 📊 Monitoring

### Check Scheduler Status

```bash
ps aux | grep scheduler.py
```

### View Logs

```bash
# Last 50 lines
tail -50 blog_scheduler.log

# Watch live
tail -f blog_scheduler.log

# Search for errors
grep "ERROR" blog_scheduler.log
```

### Database Statistics

```bash
sqlite3 subscribers.db << EOF
SELECT 'Total Subscribers:' as Metric, COUNT(*) as Count FROM subscribers
UNION
SELECT 'Verified:', COUNT(*) FROM subscribers WHERE verified = 1
UNION
SELECT 'Active:', COUNT(*) FROM subscribers WHERE active = 1
UNION
SELECT 'Email Sent:', COUNT(*) FROM email_logs;
EOF
```

---

## 📚 Example Workflows

### Workflow 1: Manual Generation

```bash
# Generate one post
python3 generate.py

# Check output
ls blog-ai-posts/

# Push to GitHub
cd .. && bash blog-ai/push.sh "📝 New blog post"

# Check website
# Visit https://victorkirpruto.dev/blog.html
```

### Workflow 2: Scheduled Automation

```bash
# Start scheduler (runs in background)
nohup python3 scheduler.py > scheduler.log 2>&1 &

# Start API server (for subscriptions)
nohup python3 api_server.py --port 5000 > api.log 2>&1 &

# Share subscribe link
# Send: https://victorkirpruto.dev/subscribe.html
```

### Workflow 3: Batch Generation

```bash
# Generate 3 posts
python3 generate.py --count 3

# Save posts to JSON
python3 generate.py --count 3 --output posts.json

# Manually add to posts.js
# Open posts.js and paste generated posts
```

---

## 🔐 Security Considerations

1. **Never commit .env file** - Use `.env.example` template only
2. **API Keys** - Store in `.env`, not in version control
3. **Database backups** - Regularly backup `subscribers.db`
4. **Rate limiting** - Implement on `/api/subscribe` endpoint in production
5. **HTTPS only** - Ensure subscription page uses HTTPS in production

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review logs: `tail -50 blog_scheduler.log`
3. Test API endpoints manually with curl
4. Verify all environment variables are set

---

## 📄 License

All generated blog posts are owned by Victor Kipruto Rop. Use and share according to the blog's terms.

---

**Last Updated:** June 6, 2024
**Version:** 1.0.0
**Status:** Production Ready ✅
