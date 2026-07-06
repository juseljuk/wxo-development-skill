#!/bin/bash
# setup-connection.sh - Set up external API connection
# Usage: ./setup-connection.sh <connection-name> <api-key>
# Example: ./setup-connection.sh openai $OPENAI_API_KEY

set -e

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check arguments
if [ $# -lt 2 ]; then
    print_error "Usage: $0 <connection-name> <api-key>"
    echo ""
    echo "Example:"
    echo "  $0 openai \$OPENAI_API_KEY"
    echo "  $0 anthropic \$ANTHROPIC_API_KEY"
    exit 1
fi

APP_ID="$1"
API_KEY="$2"

# Validate API key
if [ -z "$API_KEY" ]; then
    print_error "API key is empty"
    exit 1
fi

echo "🔐 Setting up connection: $APP_ID"
echo ""

# Function to setup connection for an environment
setup_env() {
    local env=$1
    
    print_info "Setting up $env environment..."
    
    # Step 1: Add connection
    echo "  Adding connection..."
    if orchestrate connections add --app-id "$APP_ID" --env "$env" 2>/dev/null; then
        print_success "Connection added"
    else
        print_warning "Connection may already exist"
    fi
    
    # Step 2: Configure connection
    echo "  Configuring connection..."
    if orchestrate connections configure \
        --app-id "$APP_ID" \
        --env "$env" \
        --type team \
        --kind key_value; then
        print_success "Connection configured"
    else
        print_error "Failed to configure connection"
        return 1
    fi
    
    # Step 3: Set credentials
    echo "  Setting credentials..."
    if orchestrate connections set-credentials \
        --app-id "$APP_ID" \
        --env "$env" \
        --entries "api_key=$API_KEY"; then
        print_success "Credentials set"
    else
        print_error "Failed to set credentials"
        return 1
    fi
    
    echo ""
}

# Setup for draft environment
setup_env "draft"

# Setup for live environment
setup_env "live"

# Verify connection
print_info "Verifying connection..."
if orchestrate connections list | grep -q "$APP_ID"; then
    print_success "Connection verified"
else
    print_error "Connection not found in list"
    exit 1
fi

echo ""
print_success "Connection setup complete!"
echo ""
echo "Next steps:"
echo "  1. Import external model (if needed):"
echo "     orchestrate models add --name provider/model-name --app-id $APP_ID"
echo ""
echo "  2. Use connection in tools or agents"
echo ""
echo "Verify with:"
echo "  orchestrate connections list"
echo "  orchestrate connections get -a $APP_ID"

# Made with Bob
