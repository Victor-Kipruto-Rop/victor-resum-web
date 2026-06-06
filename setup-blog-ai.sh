#!/bin/bash

# 🤖 Blog AI System - Setup & Deployment Script
# Complete automation setup for Victor Kipruto Rop's blog

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
}

print_step() {
    echo -e "${GREEN}✅${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Main setup
main() {
    print_header "🤖 Blog AI System - Setup & Deployment"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    RESUME_DIR="$(cd "$SCRIPT_DIR" && pwd)"
    BLOG_AI_DIR="$RESUME_DIR/blog-ai"
    VENV_DIR="$RESUME_DIR/venv"
    
    print_info "Working directory: $RESUME_DIR"
    
    # Step 1: Check virtual environment
    print_header "Step 1: Virtual Environment"
    
    if [ ! -d "$VENV_DIR" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
        print_step "Virtual environment created"
    else
        print_step "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    print_step "Virtual environment activated"
    
    # Step 2: Install dependencies
    print_header "Step 2: Installing Dependencies"
    
    if [ -f "$BLOG_AI_DIR/requirements.txt" ]; then
        print_info "Installing Python packages..."
        pip install --upgrade pip setuptools wheel > /dev/null 2>&1
        pip install -r "$BLOG_AI_DIR/requirements.txt" > /dev/null 2>&1
        print_step "Dependencies installed"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
    
    # Step 3: Setup environment variables
    print_header "Step 3: Environment Configuration"
    
    if [ ! -f "$BLOG_AI_DIR/.env" ]; then
        print_info ".env file not found. Creating from template..."
        cp "$BLOG_AI_DIR/.env.example" "$BLOG_AI_DIR/.env"
        print_step ".env file created from template"
        
        echo -e "\n${YELLOW}⚠️  IMPORTANT: Update your API keys in .env${NC}"
        echo "Edit: $BLOG_AI_DIR/.env"
        echo ""
        echo "Required keys:"
        echo "  1. ANTHROPIC_API_KEY - Get from https://console.anthropic.com"
        echo "  2. SENDGRID_API_KEY  - Get from https://app.sendgrid.com"
        echo "  3. GITHUB_TOKEN      - Get from https://github.com/settings/tokens"
        echo ""
        read -p "Press Enter once you've updated .env, or Ctrl+C to exit..."
    else
        print_step ".env file already configured"
    fi
    
    # Step 4: Initialize database
    print_header "Step 4: Database Initialization"
    
    print_info "Initializing subscriber database..."
    python3 << 'EOF'
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "blog-ai"))
from email_notifier import EmailNotifier
notifier = EmailNotifier()
stats = notifier.get_stats()
print(f"✅ Database ready: {stats}")
EOF
    
    print_step "Database initialized"
    
    # Step 5: Test system
    print_header "Step 5: System Test"
    
    python3 "$RESUME_DIR/test_system.py"
    
    # Step 6: Show next steps
    print_header "🚀 Setup Complete!"
    
    echo ""
    echo -e "${GREEN}What's Next?${NC}"
    echo ""
    echo "1. Test Post Generation:"
    echo "   cd $BLOG_AI_DIR"
    echo "   python3 generate.py --count 1"
    echo ""
    echo "2. Start API Server (Terminal 1):"
    echo "   cd $BLOG_AI_DIR"
    echo "   python3 api_server.py --port 5000"
    echo ""
    echo "3. Start Scheduler (Terminal 2):"
    echo "   cd $BLOG_AI_DIR"
    echo "   python3 scheduler.py"
    echo ""
    echo "4. Visit Subscribe Page:"
    echo "   file://$RESUME_DIR/subscribe.html"
    echo ""
    echo "5. Deploy to GitHub:"
    echo "   cd $RESUME_DIR"
    echo "   bash blog-ai/push.sh 'Initial Blog AI setup'"
    echo ""
    echo "6. View Documentation:"
    echo "   cat $BLOG_AI_DIR/README.md"
    echo ""
    
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
    print_step "All systems ready!"
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
}

# Run main function
main "$@"
