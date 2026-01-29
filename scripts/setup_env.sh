#!/bin/bash

# Job Application Tracker - Environment Setup Script
# This script generates a .env file from .env.example with auto-generated secrets

set -e

ENV_FILE=".env"
ENV_EXAMPLE=".env.example"

echo "=================================="
echo "Job Application Tracker Setup"
echo "=================================="
echo

# Check if .env already exists
if [ -f "$ENV_FILE" ]; then
    echo "❌ ERROR: $ENV_FILE already exists!"
    echo "To regenerate, please delete or rename the existing .env file first."
    exit 1
fi

# Check if .env.example exists
if [ ! -f "$ENV_EXAMPLE" ]; then
    echo "❌ ERROR: $ENV_EXAMPLE not found!"
    exit 1
fi

echo "Generating environment configuration..."
echo

# Generate secrets
echo "🔐 Generating secure secrets..."
POSTGRES_PASSWORD=$(openssl rand -base64 32)
SECRET_KEY=$(openssl rand -base64 32)

# Prompt for user-configurable values
echo
echo "📝 Configuration prompts (press Enter for defaults):"
echo

read -p "Enter APP_HOST [localhost:8080]: " APP_HOST
APP_HOST=${APP_HOST:-localhost:8080}

read -p "Enter Google Tag Manager ID (optional) []: " GTM_ID
GTM_ID=${GTM_ID:-}

echo
echo "✅ Creating .env file..."

# Create .env file from .env.example
cp "$ENV_EXAMPLE" "$ENV_FILE"

# Replace values using sed (cross-platform compatible)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|APP_HOST=.*|APP_HOST=$APP_HOST|" "$ENV_FILE"
    sed -i '' "s|POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=$POSTGRES_PASSWORD|" "$ENV_FILE"
    sed -i '' "s|SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" "$ENV_FILE"
    sed -i '' "s|GTM_ID=.*|GTM_ID=$GTM_ID|" "$ENV_FILE"
    sed -i '' "s|BACKEND_CORS_ORIGIN=.*|BACKEND_CORS_ORIGIN=http://$APP_HOST|" "$ENV_FILE"
else
    # Linux
    sed -i "s|APP_HOST=.*|APP_HOST=$APP_HOST|" "$ENV_FILE"
    sed -i "s|POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=$POSTGRES_PASSWORD|" "$ENV_FILE"
    sed -i "s|SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" "$ENV_FILE"
    sed -i "s|GTM_ID=.*|GTM_ID=$GTM_ID|" "$ENV_FILE"
    sed -i "s|BACKEND_CORS_ORIGIN=.*|BACKEND_CORS_ORIGIN=http://$APP_HOST|" "$ENV_FILE"
fi

echo
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo
echo "Environment file created: $ENV_FILE"
echo
echo "Next steps:"
echo "  1. Review the .env file if needed"
echo "  2. Start the application:"
echo "     docker compose up --build"
echo
echo "  3. Access the application:"
echo "     http://$APP_HOST"
echo
