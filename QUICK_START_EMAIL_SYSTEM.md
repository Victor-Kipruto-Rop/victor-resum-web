# 🚀 Email Subscription System - Quick Start Guide

## ⚡ Get Started in 2 Minutes

### 1️⃣ Start the Email Service
```bash
cd ~/Desktop/resume
python3 subscription_email_service.py
```

The service will start on `http://localhost:5000`

### 2️⃣ Send a Test Email
```bash
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Victor Kipruto",
    "email": "kiprutovictor39@gmail.com",
    "channels": ["email"]
  }'
```

**Expected Response:**
```json
{
    "email": "kiprutovictor39@gmail.com",
    "email_sent": true,
    "message": "Successfully subscribed Victor Kipruto!",
    "success": true
}
```

---

## 📧 Available Endpoints

### Subscribe User
```bash
POST /api/subscribe
Content-Type: application/json

{
  "name": "User Name",
  "email": "user@example.com",
  "channels": ["email", "telegram", "twitter"]
}
```

**Response:**
```json
{
  "success": true,
  "email": "user@example.com",
  "email_sent": true,
  "message": "Successfully subscribed!"
}
```

### Get All Subscribers
```bash
GET /api/subscribers
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "subscribers": [
    {
      "name": "Victor Kipruto",
      "email": "kiprutovictor39@gmail.com",
      "subscribed_at": "2026-06-07T18:00:22",
      "email_sent": true,
      "channels": ["email"]
    }
  ]
}
```

### Unsubscribe User
```bash
DELETE /api/subscriber/kiprutovictor39@gmail.com
```

**Response:**
```json
{
  "success": true,
  "message": "Unsubscribed kiprutovictor39@gmail.com"
}
```

### Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "subscription-email-service",
  "resend_configured": false
}
```

---

## 📂 File Locations

| File | Purpose |
|------|---------|
| `subscription_email_service.py` | Flask API service |
| `test_send_email.py` | Email sending test |
| `scripts/python/email_templates_modern.py` | Email templates |
| `subscribe.html` | Subscription form |
| `unsubscribe.html` | Preference management |
| `email-templates-preview.html` | Template gallery |
| `data/subscribers.json` | Subscriber records |
| `data/test_emails.json` | Generated test emails |

---

## 🔑 Configuration

### Default (No Setup Required)
- Emails saved to `data/` directory
- Service runs on localhost:5000
- Perfect for testing

### Live Email Sending (Optional)
```bash
# 1. Get API key from https://resend.com
# 2. Set environment variable
export RESEND_API_KEY='re_xxxxxxxxxxxxxxxx'

# 3. Restart service
python3 subscription_email_service.py
```

---

## ✅ Test the System

### Test 1: Generate Welcome Email
```bash
python3 test_send_email.py
```

### Test 2: Subscribe via API
```bash
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "kiprutovictor39@gmail.com",
    "channels": ["email"]
  }'
```

### Test 3: View Subscribers
```bash
curl http://localhost:5000/api/subscribers
```

### Test 4: Unsubscribe
```bash
curl -X DELETE http://localhost:5000/api/subscriber/kiprutovictor39@gmail.com
```

---

## 📊 Email Templates Available

1. **Welcome** - New subscriber onboarding
2. **New Blog Post** - Post notification
3. **Weekly Digest** - Content summary
4. **Trending Content** - Viral alerts
5. **Activity Recap** - Weekly summary
6. **Subscriber Milestone** - Achievements
7. **Viral Alert** - Viral content
8. **Event Announcement** - Events
9. **Recruiter Alert** - Job opportunities
10. **Recommended Reads** - Content suggestions
11. **Notification** - General alerts
12. **Dashboard Alert** - Dashboard notifications
13. **Engagement Summary** - Engagement metrics

---

## 🎨 View Email Templates

Open in browser:
```
file:///home/kipruto/Desktop/resume/email-templates-preview.html
```

---

## 🔗 Integration Example

### HTML Form
```html
<form method="POST" action="http://localhost:5000/api/subscribe">
  <input type="text" name="name" placeholder="Your Name" required>
  <input type="email" name="email" placeholder="Your Email" required>
  <input type="hidden" name="channels" value="email,telegram,twitter">
  <button type="submit">Subscribe</button>
</form>
```

### JavaScript/Fetch
```javascript
const subscribe = async (name, email) => {
  const response = await fetch('http://localhost:5000/api/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name,
      email,
      channels: ['email']
    })
  });
  return response.json();
};

// Usage
subscribe('John Doe', 'john@example.com');
```

---

## 🚨 Troubleshooting

### Service won't start
```bash
# Kill existing process
pkill -9 -f subscription_email_service

# Try again
python3 subscription_email_service.py
```

### Port already in use
```bash
# Find process on port 5000
lsof -i :5000

# Kill it
kill -9 <PID>
```

### Email not sending
1. Check service is running: `curl http://localhost:5000/health`
2. Check if RESEND_API_KEY is set: `echo $RESEND_API_KEY`
3. View logs: `cat /tmp/email_service.log`
4. Check records: `cat data/email_records.json`

---

## 📈 Monitor Emails

### View Email Records
```bash
# Pretty print JSON
cat data/email_records.json | python3 -m json.tool

# Last 10 emails
cat data/email_records.json | python3 -m json.tool | tail -50
```

### Check Subscribers
```bash
curl http://localhost:5000/api/subscribers | python3 -m json.tool
```

---

## 🎯 Success Criteria

✅ Service starts without errors  
✅ `/health` endpoint returns 200  
✅ Can subscribe users via API  
✅ Welcome emails generated  
✅ Emails saved to `data/` directory  
✅ Subscriber records created  

---

## 🚀 You're All Set!

Your email subscription system is ready to use. For production deployment, configure the Resend API key and you're good to go!

**Questions?** Check `EMAIL_SUBSCRIPTION_SYSTEM_SUMMARY.md` for detailed documentation.
