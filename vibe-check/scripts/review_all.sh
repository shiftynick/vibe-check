#!/bin/bash

# Vibe-Check Review All Files
# This script runs reviews for all unreviewed files using run_single_review.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SINGLE_REVIEW_SCRIPT="$SCRIPT_DIR/run_single_review.sh"
MASTER_FILE="vibe-check/reviews/_MASTER.json"

# Function to print colored messages
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Check if single review script exists
if [[ ! -x "$SINGLE_REVIEW_SCRIPT" ]]; then
    print_status "$RED" "Error: $SINGLE_REVIEW_SCRIPT not found or not executable!"
    exit 1
fi

# Check authentication method
if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
    print_status "$GREEN" "✓ Using Anthropic API key from environment"
else
    print_status "$YELLOW" "No ANTHROPIC_API_KEY found - will use Claude subscription"
    echo "Make sure you're signed into Claude CLI"
fi

print_status "$BLUE" "=== Vibe-Check Batch Review Process ==="
echo ""

# Counter for tracking
TOTAL_REVIEWED=0
FAILED_REVIEWS=0

# Loop until all files are reviewed or an error occurs
while true; do
    # Check remaining files
    if [[ ! -f "$MASTER_FILE" ]]; then
        print_status "$RED" "Error: $MASTER_FILE not found!"
        exit 1
    fi
    
    REMAINING=$(python3 -c "
import json
with open('$MASTER_FILE', 'r') as f:
    data = json.load(f)
    unreviewed = [f for f, info in data['files'].items() if info['status'] == 'not_reviewed']
    print(len(unreviewed))
")
    
    if [[ "$REMAINING" -eq 0 ]]; then
        print_status "$GREEN" "✓ All files have been reviewed!"
        break
    fi
    
    print_status "$YELLOW" "Files remaining: $REMAINING"
    print_status "$BLUE" "Starting review #$((TOTAL_REVIEWED + 1))..."
    echo ""
    
    # Run single review
    if "$SINGLE_REVIEW_SCRIPT"; then
        ((TOTAL_REVIEWED++))
        print_status "$GREEN" "✓ Review #$TOTAL_REVIEWED completed successfully"
    else
        ((FAILED_REVIEWS++))
        print_status "$RED" "✗ Review failed! Stopping batch process."
        break
    fi
    
    # Add a small delay between reviews to avoid rate limiting
    if [[ "$REMAINING" -gt 1 ]]; then
        print_status "$YELLOW" "Waiting 5 seconds before next review..."
        sleep 5
    fi
    
    echo ""
    echo "========================================"
    echo ""
done

# Final summary
echo ""
print_status "$BLUE" "=== Batch Review Summary ==="
print_status "$GREEN" "Total files reviewed: $TOTAL_REVIEWED"
if [[ "$FAILED_REVIEWS" -gt 0 ]]; then
    print_status "$RED" "Failed reviews: $FAILED_REVIEWS"
    exit 1
else
    print_status "$GREEN" "All reviews completed successfully!"
    exit 0
fi