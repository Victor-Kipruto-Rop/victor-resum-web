# Multi-Channel Notification System

This system enables users to subscribe to email notifications with support for Telegram and Twitter distribution.

## Components

### 1. **subscription_handler.py** (Core Manager)
Manages all subscriptions and sends multi-channel notifications.

**Features:**
- Add/remove subscribers
- Send notifications via Email, Telegram, and Twitter
- Store subscriber preferences and settings
- Subscription statistics

**Usage:**
```bash
# Add a subscriber
python subscription_handler.py subscribe user@example.com "John Doe" --channels email telegram twitter

# Send notification to all subscribers
python subscription_handler.py notify "New Blog Post" "Check out my latest article..." --url "https://example.com/post" --channels email telegram twitter

# List subscribers
python subscription_handler.py list

# Get subscriber count
python subscription_handler.py count

# Unsubscribe
python subscription_handler.py unsubscribe user@example.com
```

### 2. **subscription_api.py** (HTTP API Server)
Simple HTTP server that handles subscription requests from the frontend.

**Endpoints:**
- `POST /api/subscribe` - Add new subscriber
- `POST /api/unsubscribe` - Remove subscriber
- `GET /api/stats` - Get subscription statistics
- `GET /api/subscribers` - List all subscribers (admin)

**Example Request:**
```json
POST /api/subscribe
{
  "email": "user@example.com",
  "name": "John Doe",
  "channels": ["email", "telegram", "twitter"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully subscribed",
  "email": "user@example.com",
  "channels": ["email", "telegram", "twitter"]
}
```

**Running the Server:**
```bash
# Local development (localhost:5000)
python subscription_api.py --host localhost --port 5000

# Production (all interfaces)
python subscription_api.py --host 0.0.0.0 --port 5000
```

### 3. **subscribe.html** (Frontend Form)
User-facing subscription form with multi-channel notification preferences.

**Features:**
- Email, name input fields
- Real-time subscriber count
- Success/error messaging
- Fallback to localStorage if API unavailable
- Multi-endpoint discovery (tries local, production, relative URLs)

### 4. **Integration with notify_email.py, notify_telegram.py, distribute_twitter.py**
Existing notification modules used by the subscription system.

**Supported Channels:**
- **Email**: Resend API (primary) + SMTP fallback
- **Telegram**: Bot token + Chat ID configuration
- **Twitter**: OAuth 1.0a + API v2 authenticated posts

## Configuration

All credentials are configured in `config.py`:

```python
# Email configuration
config.email.resend_api_key = "re_xxxxx"
config.email.smtp_server = "smtp.gmail.com"
config.email.smtp_user = "your@email.com"

# Telegram configuration
config.email.telegram_bot_token = "AAEK8FJ8kIOSYnvN5BgQMSB_He_WXC4ztP0"
config.email.telegram_chat_id = "8121654680"

# Twitter configuration
config.social.twitter.api_key = "dCEflE0X1P98u7tX1FhDIHxLo"
config.social.twitter.bearer_token = "AAAAAAAAAAAAAAAAAAAAAM779wEA..."
```

## Workflow

1. **User subscribes** via subscribe.html form
2. **API handler** validates and stores subscription
3. **Confirmation email** is sent to user
4. **User receives notifications** via selected channels when new content is published
5. **Admin can manage** subscribers and send bulk notifications

## Data Storage

Subscribers are stored in `subscribers.json`:

```json
{
  "subscribers": [
    {
      "email": "user@example.com",
      "name": "John Doe",
      "channels": ["email", "telegram", "twitter"],
      "created_at": "2024-01-15T10:30:00",
      "status": "active"
    }
  ]
}
```

## Deployment Options

### 1. **Local Development**
```bash
source venv/bin/activate
python scripts/python/subscription_api.py --host localhost --port 5000
```

### 2. **Production with Gunicorn**
```bash
pip install gunicorn
gunicorn -b 0.0.0.0:5000 scripts.python.subscription_api:run_server()
```

### 3. **Docker Container**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "scripts/python/subscription_api.py", "--host", "0.0.0.0", "--port", "5000"]
```

### 4. **GitHub Actions - Automated Notifications**
Already configured in workflows:
- `notify-blog-published.yml` - Sends notifications when blog post is published
- `notify-subscribers.yml` - Bulk notification to all subscribers

## Error Handling

The system includes comprehensive error handling:

- **Network errors**: Falls back to localStorage
- **API failures**: Tries multiple endpoints (localhost, production, relative)
- **Invalid credentials**: Logs errors and skips failing channels
- **Missing subscribers file**: Auto-creates with empty array

## Security Considerations

- ✅ All credentials in `.env` file (never committed)
- ✅ CORS enabled for frontend requests
- ✅ Email validation on input
- ✅ Rate limiting on API endpoints (60 req/min via config.py)
- ✅ No sensitive data in subscriber logs

## Testing

Test the subscription system:

```bash
# 1. Start API server
python scripts/python/subscription_api.py

# 2. Subscribe via CLI
python scripts/python/subscription_handler.py subscribe test@example.com "Test User" --channels email

# 3. Send test notification
python scripts/python/subscription_handler.py notify "Test Notification" "This is a test" --channels email telegram twitter

# 4. Check subscribers
python scripts/python/subscription_handler.py list
```

## Troubleshooting

**Issue: "Network error. Please try again later"**
- Ensure API server is running: `python subscription_api.py`
- Check CORS headers are sent correctly
- Verify firewall allows connections to port 5000

**Issue: Emails not received**
- Verify Resend API key in `.env`
- Check email address is valid format
- Look for errors in server logs

**Issue: Telegram notifications not working**
- Verify bot token and chat ID in `.env`
- Test with: `python -m telegram_bot "Test message"`
- Check bot has permission to send messages

**Issue: Twitter notifications not posting**
- Verify OAuth credentials in `.env`
- Check Twitter API rate limits
- Ensure tweet is under 280 characters

## Future Enhancements

- [ ] User preferences dashboard (manage notification channels)
- [ ] Scheduled digest emails (daily/weekly)
- [ ] A/B testing for email subject lines
- [ ] Analytics dashboard for subscription metrics
- [ ] Unsubscribe link in email notifications
- [ ] SMS notifications via Twilio
- [ ] Webhook support for external systems
