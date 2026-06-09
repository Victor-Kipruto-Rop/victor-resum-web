#!/bin/bash
# Daily Blog Auto-Generation Script
# Runs auto_generate.py to create 5 new blog posts every 24 hours
# Add to cron: 0 2 * * * /home/kipruto/Desktop/resume/blog-ai/daily_generate.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$SCRIPT_DIR/auto_generate.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting daily blog generation..." >> "$LOG_FILE"

cd "$PROJECT_DIR" || exit 1

python3 "$SCRIPT_DIR/auto_generate.py" --count 5 --force >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Blog generation completed successfully" >> "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Blog generation failed with exit code $EXIT_CODE" >> "$LOG_FILE"
fi

# Keep only last 100 lines of log
tail -100 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"