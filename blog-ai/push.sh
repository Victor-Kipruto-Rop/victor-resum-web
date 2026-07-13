#!/bin/bash

# GitHub Auto-Deploy Script
# Automatically commits and pushes new blog posts to GitHub

set -e  # Exit on error

# Configuration
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
BLOG_AI_DIR="$REPO_DIR/blog-ai"
POSTS_DIR="$REPO_DIR/blog-ai-posts"
GIT_USER=$(git config user.name)
GIT_EMAIL=$(git config user.email)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ️${NC} $1"
}

# Main script
main() {
    print_info "GitHub Auto-Deploy Script"
    print_info "Repository: $REPO_DIR"
    
    # Check if git is initialized
    if [ ! -d "$REPO_DIR/.git" ]; then
        print_error "Not a git repository: $REPO_DIR"
        exit 1
    fi
    
    # Navigate to repo
    cd "$REPO_DIR"
    
    # Get commit message
    COMMIT_MSG="${1:-"🤖 Auto-generated blog post"}"
    if [ "$#" -gt 1 ]; then
        # If second argument provided, use it as the title
        COMMIT_MSG="📝 New blog post: $2"
    fi
    
    print_info "Checking git status..."
    
    # Check if there are changes
    if git diff-index --quiet HEAD --; then
        print_info "No changes to commit"
        exit 0
    fi
    
    # Add blog-related files
    print_info "Staging blog files..."
    git add blog-ai-posts/ 2>/dev/null || true
    git add blog/ 2>/dev/null || true
    git add assets/shared/posts.js 2>/dev/null || true
    git add feed.xml 2>/dev/null || true
    git add blog-ai/config.json 2>/dev/null || true
    
    # Check if there are staged changes
    if ! git diff --cached --quiet; then
        print_info "Committing changes..."
        git commit -m "$COMMIT_MSG" \
            -m "Generated at: $(date '+%Y-%m-%d %H:%M:%S')" \
            --quiet
        
        print_status "Committed with message: '$COMMIT_MSG'"
        
        # Push to remote
        print_info "Pushing to remote..."
        if git push origin main --quiet 2>/dev/null; then
            print_status "Successfully pushed to GitHub"
        elif git push origin master --quiet 2>/dev/null; then
            print_status "Successfully pushed to GitHub"
        else
            print_error "Failed to push to GitHub"
            print_info "Make sure you have push access and the correct branch"
            exit 1
        fi
    else
        print_info "No staged changes to commit"
    fi
    
    print_status "Deploy complete!"
}

# Deployment summary function
print_summary() {
    echo ""
    echo "📊 Deployment Summary"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Count posts
    POSTS_COUNT=$(find "$POSTS_DIR" -name "*.md" 2>/dev/null | wc -l)
    echo "📝 Total AI Posts: $POSTS_COUNT"
    
    # Git info
    COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null || echo "unknown")
    echo "📚 Total Commits: $COMMIT_COUNT"
    
    # Last commit
    LAST_COMMIT=$(git log -1 --pretty=format:"%s" 2>/dev/null || echo "unknown")
    echo "📌 Last Commit: $LAST_COMMIT"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Run main function
main "$@"

# Print summary
if [ $? -eq 0 ]; then
    print_summary
fi
