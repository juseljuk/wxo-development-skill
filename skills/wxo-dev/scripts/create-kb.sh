#!/bin/bash
# create-kb.sh - Create and import a knowledge base
# Usage: ./create-kb.sh <kb-name> <document-path>
# Example: ./create-kb.sh product-catalog docs/products.txt

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
    print_error "Usage: $0 <kb-name> <document-path> [description]"
    echo ""
    echo "Example:"
    echo "  $0 product-catalog docs/products.txt \"Product catalog KB\""
    echo "  $0 company-policies docs/policies.pdf"
    exit 1
fi

KB_NAME="$1"
DOC_PATH="$2"
DESCRIPTION="${3:-Knowledge base for $KB_NAME}"

# Validate document exists
if [ ! -f "$DOC_PATH" ]; then
    print_error "Document not found: $DOC_PATH"
    exit 1
fi

# Get document filename
DOC_FILENAME=$(basename "$DOC_PATH")

# Validate file extension
EXT="${DOC_FILENAME##*.}"
case "$EXT" in
    txt|pdf|docx|pptx|xlsx|csv|html)
        print_success "Supported file format: .$EXT"
        ;;
    *)
        print_error "Unsupported file format: .$EXT"
        echo "Supported formats: txt, pdf, docx, pptx, xlsx, csv, html"
        exit 1
        ;;
esac

# Check file size
FILE_SIZE=$(stat -f%z "$DOC_PATH" 2>/dev/null || stat -c%s "$DOC_PATH" 2>/dev/null)
MAX_SIZE=26214400  # 25 MB in bytes

if [ "$FILE_SIZE" -gt "$MAX_SIZE" ]; then
    print_error "File too large: $(($FILE_SIZE / 1024 / 1024)) MB (max 25 MB)"
    exit 1
fi

echo "📚 Creating knowledge base: $KB_NAME"
echo ""

# Create knowledge_bases directory if it doesn't exist
mkdir -p knowledge_bases

# Copy document to knowledge_bases directory
KB_DOC_PATH="knowledge_bases/$DOC_FILENAME"
if [ "$DOC_PATH" != "$KB_DOC_PATH" ]; then
    print_info "Copying document to knowledge_bases/..."
    cp "$DOC_PATH" "$KB_DOC_PATH"
    print_success "Document copied"
fi

# Create KB YAML file
KB_YAML="knowledge_bases/${KB_NAME}.yaml"

print_info "Creating KB YAML: $KB_YAML"

cat > "$KB_YAML" << EOF
spec_version: v1
kind: knowledge_base
name: ${KB_NAME}
description: |
  ${DESCRIPTION}

documents:
  - path: ${DOC_FILENAME}

vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
  chunk_size: 400
  chunk_overlap: 50
  extraction_strategy: standard

conversational_search_tool:
  generation:
    prompt_instruction: |
      Answer questions based on the knowledge base content.
      Provide accurate and detailed information.
      If information is not in the knowledge base, clearly state that.
    max_docs_passed_to_llm: 10
    generated_response_length: Moderate
    idk_message: "I don't have information about that in the knowledge base."
  confidence_thresholds:
    retrieval_confidence_threshold: Low
    response_confidence_threshold: Low
  query_rewrite:
    enabled: true
  citations:
    citations_shown: -1
EOF

print_success "KB YAML created"
echo ""

# Import knowledge base
print_info "Importing knowledge base..."
if orchestrate knowledge-bases import -f "$KB_YAML"; then
    print_success "Knowledge base imported"
else
    print_error "Failed to import knowledge base"
    exit 1
fi

echo ""
print_info "Waiting for indexing to complete..."
echo "This may take a few minutes depending on document size..."
echo ""

# Wait for KB to be ready
MAX_WAIT=300  # 5 minutes
WAIT_TIME=0
SLEEP_INTERVAL=5

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    STATUS=$(orchestrate knowledge-bases get -n "$KB_NAME" 2>/dev/null | grep -i "status" | awk '{print $2}' || echo "unknown")
    
    if [ "$STATUS" = "ready" ]; then
        print_success "Knowledge base is ready!"
        break
    elif [ "$STATUS" = "failed" ]; then
        print_error "Knowledge base indexing failed"
        exit 1
    else
        echo -n "."
        sleep $SLEEP_INTERVAL
        WAIT_TIME=$((WAIT_TIME + SLEEP_INTERVAL))
    fi
done

if [ $WAIT_TIME -ge $MAX_WAIT ]; then
    print_warning "Indexing is taking longer than expected"
    echo "Check status with: orchestrate knowledge-bases get -n $KB_NAME"
fi

echo ""
echo ""
print_success "Knowledge base setup complete!"
echo ""
echo "Files created:"
echo "  - $KB_YAML"
echo "  - $KB_DOC_PATH"
echo ""
echo "Use in agent YAML:"
echo "  knowledge_base:"
echo "    - $KB_NAME"
echo ""
echo "Verify with:"
echo "  orchestrate knowledge-bases list"
echo "  orchestrate knowledge-bases get -n $KB_NAME"

# Made with Bob
