#!/bin/bash
# Simple deployment script

set -e

echo "Starting deployment process..."

# Environment variables
DEPLOY_ENV=${1:-staging}
APP_NAME="vibe-check-demo"

# Validation
if [[ "$DEPLOY_ENV" != "staging" && "$DEPLOY_ENV" != "production" ]]; then
    echo "Error: Invalid environment. Use 'staging' or 'production'"
    exit 1
fi

# Build
echo "Building application..."
npm run build

# Run tests
echo "Running tests..."
npm test

# Deploy based on environment
if [[ "$DEPLOY_ENV" == "production" ]]; then
    echo "Deploying to production..."
    # Production deployment logic here
    echo "Production deployment complete!"
else
    echo "Deploying to staging..."
    # Staging deployment logic here
    echo "Staging deployment complete!"
fi

echo "Deployment finished successfully!"