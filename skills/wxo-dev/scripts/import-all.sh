#!/bin/bash
# import-all.sh - Import all watsonx Orchestrate artifacts
# Usage: ./import-all.sh

set -e

echo "🚀 Importing watsonx Orchestrate artifacts..."
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Import connections (if any)
if [ -d "connections" ] && [ "$(ls -A connections/*.yaml 2>/dev/null)" ]; then
    print_step "📡 Importing connections..."
    for file in connections/*.yaml; do
        if [ -f "$file" ]; then
            echo "  Importing $(basename "$file")..."
            if orchestrate connections import -f "$file"; then
                print_success "Imported $(basename "$file")"
            else
                print_error "Failed to import $(basename "$file")"
            fi
        fi
    done
    echo ""
fi

# Import toolkits
if [ -d "toolkits" ] && [ "$(ls -A toolkits/*.yaml 2>/dev/null)" ]; then
    print_step "🧰 Importing MCP toolkits..."
    for file in toolkits/*.yaml; do
        if [ -f "$file" ]; then
            echo "  Importing $(basename "$file")..."
            if orchestrate toolkits import -f "$file"; then
                print_success "Imported $(basename "$file")"
            else
                print_error "Failed to import $(basename "$file")"
            fi
        fi
    done
    echo ""
fi

# Import Python tools (excluding workflows)
if [ -d "tools" ] && [ "$(ls -A tools/*.py 2>/dev/null)" ]; then
    print_step "🔧 Importing Python tools..."
    for file in tools/*.py; do
        if [ -f "$file" ] && [[ ! "$file" =~ _workflow\.py$ ]]; then
            echo "  Importing $(basename "$file")..."
            if orchestrate tools import -k python -f "$file"; then
                print_success "Imported $(basename "$file")"
            else
                print_error "Failed to import $(basename "$file")"
            fi
        fi
    done
    echo ""
fi

# Import workflows
if [ -d "tools" ] && [ "$(ls -A tools/*_workflow.py 2>/dev/null)" ]; then
    print_step "🔄 Importing agentic workflows..."
    for file in tools/*_workflow.py; do
        if [ -f "$file" ]; then
            echo "  Importing $(basename "$file")..."
            if orchestrate tools import -k flow -f "$file"; then
                print_success "Imported $(basename "$file")"
            else
                print_error "Failed to import $(basename "$file")"
            fi
        fi
    done
    echo ""
fi

# Import knowledge bases
if [ -d "knowledge_bases" ] && [ "$(ls -A knowledge_bases/*.yaml 2>/dev/null)" ]; then
    print_step "📚 Importing knowledge bases..."
    for file in knowledge_bases/*.yaml; do
        if [ -f "$file" ]; then
            echo "  Importing $(basename "$file")..."
            if orchestrate knowledge-bases import -f "$file"; then
                print_success "Imported $(basename "$file")"
            else
                print_error "Failed to import $(basename "$file")"
            fi
        fi
    done
    echo ""
fi

# Import plugins/guardrails
if [ -d "plugins" ] && [ "$(ls -A plugins/*.py 2>/dev/null)" ]; then
    print_step "🛡️  Importing guardrail plugins..."
    for file in plugins/*.py; do
        if [ -f "$file" ]; then
            echo "  Importing $(basename "$file")..."
            if orchestrate tools import -k python -f "$file"; then
                print_success "Imported $(basename "$file")"
            else
                print_error "Failed to import $(basename "$file")"
            fi
        fi
    done
    echo ""
fi

# Import agents
if [ -d "agents" ] && [ "$(ls -A agents/*.yaml 2>/dev/null)" ]; then
    print_step "📦 Importing agents..."
    for file in agents/*.yaml; do
        if [ -f "$file" ]; then
            echo "  Importing $(basename "$file")..."
            if orchestrate agents import -f "$file"; then
                print_success "Imported $(basename "$file")"
            else
                print_error "Failed to import $(basename "$file")"
            fi
        fi
    done
    echo ""
fi

# Summary
echo ""
echo "✅ Import complete!"
echo ""
echo "Verify imports with:"
echo "  orchestrate agents list"
echo "  orchestrate tools list"
echo "  orchestrate toolkits list"
echo "  orchestrate knowledge-bases list"
echo "  orchestrate connections list"

# Made with Bob
