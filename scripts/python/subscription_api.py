#!/usr/bin/env python3
"""
Simple HTTP API Server for Subscriptions
Handles POST requests from subscribe.html form
Can be deployed as serverless function or run locally
"""

import os
import sys
import json
import logging
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from subscription_handler import SubscriptionHandler
    from config import config
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SubscriptionAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Subscription API"""
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
            path = urlparse(self.path).path
            
            # Route requests
            if path == '/api/subscribe':
                self.handle_subscribe(data)
            elif path == '/api/unsubscribe':
                self.handle_unsubscribe(data)
            elif path == '/api/stats':
                self.handle_stats(data)
            else:
                self.send_error_response(404, "Endpoint not found")
        
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
        except Exception as e:
            logger.error(f"Error: {e}")
            self.send_error_response(500, str(e))
    
    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path
        
        try:
            if path == '/api/stats':
                self.handle_stats_get()
            elif path == '/api/subscribers':
                self.handle_subscribers_list()
            else:
                self.send_error_response(404, "Endpoint not found")
        except Exception as e:
            logger.error(f"Error: {e}")
            self.send_error_response(500, str(e))
    
    def handle_subscribe(self, data):
        """Handle subscription request"""
        email = data.get('email', '').strip()
        name = data.get('name', '').strip()
        channels = data.get('channels', ['email'])
        
        # Validation
        if not email or not name:
            return self.send_error_response(400, "Email and name required")
        
        if '@' not in email:
            return self.send_error_response(400, "Invalid email format")
        
        try:
            handler = SubscriptionHandler()
            result = handler.add_subscriber(email, name, channels)
            
            if result.get('success'):
                self.send_success_response(result)
            else:
                self.send_error_response(409, result.get('message', 'Subscription failed'))
        
        except Exception as e:
            logger.error(f"Subscription error: {e}")
            self.send_error_response(500, str(e))
    
    def handle_unsubscribe(self, data):
        """Handle unsubscription request"""
        email = data.get('email', '').strip()
        
        if not email:
            return self.send_error_response(400, "Email required")
        
        try:
            handler = SubscriptionHandler()
            result = handler.unsubscribe(email)
            
            if result.get('success'):
                self.send_success_response(result)
            else:
                self.send_error_response(404, result.get('message', 'Unsubscription failed'))
        
        except Exception as e:
            logger.error(f"Unsubscription error: {e}")
            self.send_error_response(500, str(e))
    
    def handle_stats(self, data=None):
        """Handle stats request"""
        try:
            handler = SubscriptionHandler()
            stats = {
                "total_subscribers": handler.get_subscribers_count(),
                "timestamp": datetime.now().isoformat(),
                "platform": "DBOS Portfolio"
            }
            self.send_success_response(stats)
        except Exception as e:
            logger.error(f"Stats error: {e}")
            self.send_error_response(500, str(e))
    
    def handle_stats_get(self):
        """Handle GET /api/stats"""
        self.handle_stats()
    
    def handle_subscribers_list(self):
        """Handle GET /api/subscribers (admin only)"""
        # In production, would check auth token
        try:
            handler = SubscriptionHandler()
            subscribers = handler.get_subscribers()
            self.send_success_response({
                "subscribers": subscribers,
                "count": len(subscribers)
            })
        except Exception as e:
            logger.error(f"Subscribers list error: {e}")
            self.send_error_response(500, str(e))
    
    def send_success_response(self, data):
        """Send successful JSON response"""
        response = json.dumps(data).encode('utf-8')
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)
    
    def send_error_response(self, status_code, message):
        """Send error JSON response"""
        error = {"error": message, "code": status_code}
        response = json.dumps(error).encode('utf-8')
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)
    
    def log_message(self, format, *args):
        """Custom logging"""
        logger.info(f"{self.address_string()} - {format % args}")


def run_server(host='localhost', port=5000):
    """Run the subscription API server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, SubscriptionAPIHandler)
    
    logger.info(f"Subscription API Server running on http://{host}:{port}")
    logger.info("Available endpoints:")
    logger.info("  POST /api/subscribe - Subscribe to notifications")
    logger.info("  POST /api/unsubscribe - Unsubscribe from notifications")
    logger.info("  GET /api/stats - Get subscription statistics")
    logger.info("  GET /api/subscribers - List all subscribers (admin)")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped")
        httpd.server_close()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Subscription API Server')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    
    args = parser.parse_args()
    run_server(args.host, args.port)
