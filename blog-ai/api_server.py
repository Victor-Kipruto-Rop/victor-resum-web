#!/usr/bin/env python3
"""
Simple Flask API Server
Provides endpoints for email subscriptions and blog management
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from pathlib import Path
import os
from datetime import datetime
import sys

# Add necessary directories to path for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "social-automation"))

from email_notifier import EmailNotifier
from generate import BlogPostGenerator
from trend_scraper import TrendScraper
from dispatcher import SocialDispatcher
from keyword_research import KeywordResearcher

app = Flask(__name__)
CORS(app)

# Initialize services
email_notifier = EmailNotifier()
blog_generator = BlogPostGenerator()
trend_scraper = TrendScraper()
social_dispatcher = SocialDispatcher()
keyword_researcher = KeywordResearcher()

# Configuration
CONFIG_PATH = Path(__file__).parent / "blog-ai" / "config.json"

@app.route('/api/generate-post', methods=['POST'])
def generate_post():
    """Generate a new AI blog post"""
    try:
        data = request.json or {}
        title = data.get('title')
        
        # Use trend if requested
        if not title and data.get('use_trend'):
            report = trend_scraper.compile_trends_report()
            if report['data']['trending_technologies']:
                tech = report['data']['trending_technologies'][0]['name']
                title = f"The Future of {tech}: A Data Engineer's Perspective"

        title, content, metadata = blog_generator.generate_post(title)
        md_file, meta_file = blog_generator.save_post(title, content, metadata)
        
        # Format for posts.json (simulating updates to posts.js)
        post_entry = blog_generator.format_for_posts_js(title, content, metadata)
        
        return jsonify({
            "status": "success",
            "message": "Post generated successfully",
            "title": title,
            "files": {
                "markdown": md_file,
                "metadata": meta_file
            },
            "post_data": post_entry
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/trends', methods=['GET'])
def get_trends():
    """Get latest tech trends"""
    try:
        report = trend_scraper.compile_trends_report()
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/research-keyword', methods=['POST'])
def research_keyword():
    """Research a keyword for SEO"""
    try:
        data = request.json
        keyword = data.get('keyword', '')
        if not keyword:
            return jsonify({"status": "error", "message": "Keyword is required"}), 400
            
        analysis = keyword_researcher.analyze_keyword(keyword)
        return jsonify(analysis), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/dispatch-post', methods=['POST'])
def dispatch_post():
    """Dispatch a post to social media"""
    try:
        data = request.json
        metadata_path = data.get('metadata_path')
        
        if not metadata_path:
            return jsonify({"status": "error", "message": "Metadata path is required"}), 400
            
        results = social_dispatcher.dispatch_from_metadata(metadata_path)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """Subscribe a new user to the blog"""
    try:
        data = request.json
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        
        if not email:
            return jsonify({"status": "error", "message": "Email is required"}), 400
        
        result = email_notifier.subscribe(email, name)
        
        status_code = 200 if result['status'] == 'success' else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/verify-email', methods=['GET'])
def verify_email():
    """Verify email subscription"""
    try:
        token = request.args.get('token', '')
        
        if not token:
            return jsonify({"status": "error", "message": "Token is required"}), 400
        
        result = email_notifier.verify_email(token)
        
        # Redirect to blog with status
        status = "success" if result['status'] == 'success' else "error"
        return f"""
        <html>
            <body style="font-family: system-ui; text-align: center; padding: 40px;">
                <h2>{'✅ Email Verified!' if status == 'success' else '❌ Verification Failed'}</h2>
                <p>{result['message']}</p>
                <a href="blog.html">← Back to Blog</a>
                <script>
                    setTimeout(() => window.location.href = 'blog.html', 3000);
                </script>
            </body>
        </html>
        """, 200 if status == 'success' else 400
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/unsubscribe', methods=['GET'])
def unsubscribe():
    """Unsubscribe from emails"""
    try:
        token = request.args.get('token', '')
        
        if not token:
            return jsonify({"status": "error", "message": "Token is required"}), 400
        
        result = email_notifier.unsubscribe(token)
        
        status = "success" if result['status'] == 'success' else "error"
        return f"""
        <html>
            <body style="font-family: system-ui; text-align: center; padding: 40px;">
                <h2>{'✅ Unsubscribed' if status == 'success' else '❌ Unsubscribe Failed'}</h2>
                <p>{result['message']}</p>
                <a href="subscribe.html">← Back to Subscribe</a>
            </body>
        </html>
        """, 200 if status == 'success' else 400
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get blog statistics"""
    try:
        stats = email_notifier.get_stats()
        
        # Add blog config info
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        
        stats['blog'] = {
            'title': config['blog']['title'],
            'author': config['author']['name'],
            'topics': len(config['topics'])
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Blog API Server"
    }), 200

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get public blog configuration"""
    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        
        # Return only public information
        public_config = {
            'author': config['author'],
            'blog': config['blog'],
            'topics': config['topics']
        }
        
        return jsonify(public_config), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    """500 error handler"""
    return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Blog API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    
    args = parser.parse_args()
    
    print(f"🚀 Starting Blog API Server")
    print(f"📍 Running on http://{args.host}:{args.port}")
    print(f"📧 Email notifications enabled")
    
    app.run(host=args.host, port=args.port, debug=args.debug)
