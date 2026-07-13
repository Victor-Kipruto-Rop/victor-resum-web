"""
Developer Intelligence System - Notification Module
Sends alerts when new blog posts are published via multiple channels
Works with GitHub Actions for automated triggers
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NotificationSystem:
    def __init__(self, config_file='automation/config.json'):
        """Initialize notification system with configuration"""
        self.config = self.load_config(config_file)
        self.timestamp = datetime.now().isoformat()
        self.logger = self.setup_logger()
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            # Resolve environment variables in config
            return self._resolve_env_vars(config)
        except FileNotFoundError:
            print(f"Warning: {config_file} not found. Using default config.")
            return self.get_default_config()
    
    def _resolve_env_vars(self, obj):
        """Recursively resolve environment variables in config"""
        if isinstance(obj, dict):
            return {key: self._resolve_env_vars(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._resolve_env_vars(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            var_name = obj[2:-1]
            return os.getenv(var_name, obj)
        return obj
    
    def get_default_config(self):
        """Default configuration"""
        return {
            "notifications": {
                "telegram": {
                    "enabled": True,
                    "bot_token": os.getenv('TELEGRAM_BOT_TOKEN', ''),
                    "chat_id": os.getenv('TELEGRAM_CHAT_ID', '')
                },
                "email": {
                    "enabled": False,
                    "service": "mailchimp",
                    "api_key": os.getenv('MAILCHIMP_API_KEY', '')
                },
                "discord": {
                    "enabled": False,
                    "webhook_url": os.getenv('DISCORD_WEBHOOK', '')
                }
            },
            "blog": {
                "posts_dir": "blog/posts",
                "posts_json": "blog/assets/shared/posts.json"
            }
        }
    
    def setup_logger(self):
        """Setup logging"""
        class SimpleLogger:
            def __init__(self):
                self.log_file = 'automation/notification.log'
            
            def log(self, message, level='INFO'):
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_msg = f"[{timestamp}] [{level}] {message}"
                print(log_msg)
                
                try:
                    with open(self.log_file, 'a') as f:
                        f.write(log_msg + '\n')
                except:
                    pass
        
        return SimpleLogger()
    
    def detect_new_post(self):
        """Detect if a new post was added"""
        try:
            posts_json = Path(self.config['blog']['posts_json'])
            if not posts_json.exists():
                return None
            
            with open(posts_json, 'r') as f:
                posts = json.load(f)
            
            if not posts:
                return None
            
            # Get most recent post
            latest = max(posts, key=lambda x: x.get('date', ''))
            return latest
        
        except Exception as e:
            self.logger.log(f"Error detecting new post: {str(e)}", 'ERROR')
            return None
    
    def send_telegram_notification(self, post):
        """Send notification via Telegram"""
        try:
            config = self.config['notifications']['telegram']
            
            if not config.get('enabled'):
                self.logger.log("Telegram notifications disabled")
                return False
            
            if not config.get('bot_token') or not config.get('chat_id'):
                self.logger.log("Telegram credentials not configured", 'WARNING')
                return False
            
            # Create message
            message = self.format_telegram_message(post)
            
            # Send via Telegram Bot API
            url = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage"
            payload = {
                'chat_id': config['chat_id'],
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                self.logger.log(f"Telegram notification sent successfully")
                return True
            else:
                self.logger.log(f"Telegram error: {response.text}", 'ERROR')
                return False
        
        except Exception as e:
            self.logger.log(f"Telegram notification failed: {str(e)}", 'ERROR')
            return False
    
    def format_telegram_message(self, post):
        """Format message for Telegram"""
        title = post.get('title', 'New Post')
        slug = post.get('slug', '')
        url = post.get('url', f"blog.html#{slug}")
        excerpt = post.get('excerpt', 'Check out the latest blog post!')
        
        message = (
            f"🚀 <b>New Blog Post Published!</b>\n\n"
            f"📝 <b>{title}</b>\n"
            f"{excerpt}\n\n"
            f"🔗 <a href='{url}'>Read full post</a>\n"
            f"📊 <a href='dashboard/'>View analytics</a>\n\n"
            f"#blog #development"
        )
        
        return message
    
    def send_discord_notification(self, post):
        """Send notification via Discord"""
        try:
            config = self.config['notifications']['discord']
            
            if not config.get('enabled'):
                self.logger.log("Discord notifications disabled")
                return False
            
            if not config.get('webhook_url'):
                self.logger.log("Discord webhook not configured", 'WARNING')
                return False
            
            # Create embed
            embed = {
                "title": f"🚀 {post.get('title', 'New Post')}",
                "description": post.get('excerpt', ''),
                "url": post.get('url', ''),
                "color": 3447003,  # Blue
                "fields": [
                    {
                        "name": "Category",
                        "value": post.get('category', 'Tech'),
                        "inline": True
                    },
                    {
                        "name": "Published",
                        "value": post.get('date', 'Today'),
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Developer Blog Analytics"
                }
            }
            
            payload = {"embeds": [embed]}
            
            response = requests.post(
                config['webhook_url'],
                json=payload,
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                self.logger.log("Discord notification sent successfully")
                return True
            else:
                self.logger.log(f"Discord error: {response.text}", 'ERROR')
                return False
        
        except Exception as e:
            self.logger.log(f"Discord notification failed: {str(e)}", 'ERROR')
            return False
    
    def send_email_notification(self, post):
        """Send notification via email (optional)"""
        try:
            config = self.config['notifications']['email']
            
            if not config.get('enabled'):
                self.logger.log("Email notifications disabled")
                return False
            
            # Integration with Mailchimp/Buttondown would go here
            # For now, just log that it would be sent
            self.logger.log(f"Email notification would be sent: {post.get('title')}")
            return True
        
        except Exception as e:
            self.logger.log(f"Email notification failed: {str(e)}", 'ERROR')
            return False
    
    def notify_all(self, post):
        """Send notifications through all enabled channels"""
        results = {
            'timestamp': self.timestamp,
            'post_title': post.get('title', 'Unknown'),
            'post_slug': post.get('slug', ''),
            'channels': {}
        }
        
        # Telegram
        results['channels']['telegram'] = self.send_telegram_notification(post)
        
        # Discord
        results['channels']['discord'] = self.send_discord_notification(post)
        
        # Email
        results['channels']['email'] = self.send_email_notification(post)
        
        return results
    
    def run(self):
        """Main execution method"""
        self.logger.log("=" * 60)
        self.logger.log("Developer Intelligence - Notification System Started")
        self.logger.log("=" * 60)
        
        # Detect new post
        post = self.detect_new_post()
        
        if not post:
            self.logger.log("No new posts detected")
            return {'status': 'no_posts'}
        
        self.logger.log(f"New post detected: {post.get('title')}")
        
        # Send notifications
        results = self.notify_all(post)
        
        # Log results
        self.logger.log(f"Notification results: {json.dumps(results, indent=2)}")
        
        # Write results to file
        results_file = 'automation/notification_results.json'
        try:
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
        except:
            pass
        
        return results


def main():
    """Main entry point"""
    try:
        notifier = NotificationSystem()
        results = notifier.run()
        
        # Exit with success
        sys.exit(0)
    
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
