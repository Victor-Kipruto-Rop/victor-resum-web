#!/usr/bin/env python3
"""
Notification Logging - Log all notifications for audit trail
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configure logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    filename=log_dir / 'notifications.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log_notification(event_type, details, status='sent'):
    """
    Log notification event
    
    Args:
        event_type: Type of notification (email, telegram, etc.)
        details: Dictionary with event details
        status: Notification status (sent, failed, pending)
    """
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'status': status,
            'details': details
        }
        
        logger.info(f"{event_type}: {json.dumps(log_entry)}")
        print(f"✅ Logged {event_type}: {status}")
        
        # Also save to JSON log
        json_log_file = log_dir / 'notifications.json'
        notifications = []
        
        if json_log_file.exists():
            with open(json_log_file, 'r') as f:
                notifications = json.load(f)
        
        notifications.append(log_entry)
        
        with open(json_log_file, 'w') as f:
            json.dump(notifications, f, indent=2)
        
        return True
    
    except Exception as e:
        logger.error(f"Error logging notification: {e}")
        print(f"❌ Error logging notification: {e}")
        return False

if __name__ == '__main__':
    log_notification(
        event_type='test',
        details={'message': 'Test notification'},
        status='sent'
    )
