#!/usr/bin/env python3
"""
Database module for Victor Kipruto's portfolio
Manages subscriber storage, dashboard access logs, and analytics
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / 'victor_portfolio.db'
DATABASE_URL = f"sqlite:///{DB_PATH}"

class Database:
    """SQLite database manager for portfolio application"""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Subscribers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                subscription_type TEXT DEFAULT 'email',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Dashboard access logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dashboard_access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT NOT NULL,
                user_agent TEXT,
                dashboard_name TEXT NOT NULL,
                authenticated BOOLEAN DEFAULT 0,
                accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Analytics events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Blog posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blog_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                content TEXT,
                author TEXT DEFAULT 'Victor Kipruto',
                published_at TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Subscriber methods
    def add_subscriber(self, name, email, subscription_type='email'):
        """Add a new subscriber"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO subscribers (name, email, subscription_type)
                VALUES (?, ?, ?)
            ''', (name, email, subscription_type))
            conn.commit()
            return {'success': True, 'message': 'Subscriber added'}
        except sqlite3.IntegrityError:
            return {'success': False, 'message': 'Email already subscribed'}
        finally:
            conn.close()
    
    def get_subscribers(self, status='active'):
        """Get all subscribers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM subscribers WHERE status = ?', (status,))
        subscribers = cursor.fetchall()
        conn.close()
        return [dict(row) for row in subscribers]
    
    def get_subscriber_count(self):
        """Get total subscriber count"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM subscribers WHERE status = "active"')
        count = cursor.fetchone()['count']
        conn.close()
        return count
    
    def remove_subscriber(self, email):
        """Mark subscriber as inactive"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE subscribers SET status = ? WHERE email = ?', ('inactive', email))
        conn.commit()
        conn.close()
    
    # Dashboard access logging
    def log_dashboard_access(self, ip_address, dashboard_name, authenticated=False, user_agent=None):
        """Log dashboard access attempt"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dashboard_access_logs (ip_address, user_agent, dashboard_name, authenticated)
            VALUES (?, ?, ?, ?)
        ''', (ip_address, user_agent, dashboard_name, authenticated))
        conn.commit()
        conn.close()
    
    def get_access_logs(self, dashboard_name=None, limit=100):
        """Get dashboard access logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if dashboard_name:
            cursor.execute('''
                SELECT * FROM dashboard_access_logs 
                WHERE dashboard_name = ?
                ORDER BY accessed_at DESC
                LIMIT ?
            ''', (dashboard_name, limit))
        else:
            cursor.execute('''
                SELECT * FROM dashboard_access_logs 
                ORDER BY accessed_at DESC
                LIMIT ?
            ''', (limit,))
        logs = cursor.fetchall()
        conn.close()
        return [dict(row) for row in logs]
    
    # Analytics methods
    def log_event(self, event_type, event_data=None):
        """Log an analytics event"""
        conn = self.get_connection()
        cursor = conn.cursor()
        event_data_json = json.dumps(event_data) if event_data else None
        cursor.execute('''
            INSERT INTO analytics_events (event_type, event_data)
            VALUES (?, ?)
        ''', (event_type, event_data_json))
        conn.commit()
        conn.close()
    
    def get_events(self, event_type=None, limit=100):
        """Get analytics events"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if event_type:
            cursor.execute('''
                SELECT * FROM analytics_events 
                WHERE event_type = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (event_type, limit))
        else:
            cursor.execute('''
                SELECT * FROM analytics_events 
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
        events = cursor.fetchall()
        conn.close()
        return [dict(row) for row in events]
    
    # Blog methods
    def add_blog_post(self, title, slug, content, published_at=None):
        """Add a blog post"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if not published_at:
            published_at = datetime.now()
        cursor.execute('''
            INSERT INTO blog_posts (title, slug, content, published_at)
            VALUES (?, ?, ?, ?)
        ''', (title, slug, content, published_at))
        conn.commit()
        conn.close()
    
    def get_blog_posts(self, limit=10):
        """Get recent blog posts"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM blog_posts 
            ORDER BY published_at DESC
            LIMIT ?
        ''', (limit,))
        posts = cursor.fetchall()
        conn.close()
        return [dict(row) for row in posts]
    
    # Statistics
    def get_statistics(self):
        """Get portfolio statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM subscribers WHERE status = "active"')
        subscriber_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM blog_posts')
        blog_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM dashboard_access_logs WHERE authenticated = 1')
        dashboard_visits = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'total_subscribers': subscriber_count,
            'total_blog_posts': blog_count,
            'dashboard_visits': dashboard_visits,
            'generated_at': datetime.now().isoformat()
        }


# Global database instance
db = Database()

if __name__ == '__main__':
    # Initialize and test
    db.init_db()
    print(f"✅ Database initialized at {DB_PATH}")
    print(f"📊 Statistics: {db.get_statistics()}")
