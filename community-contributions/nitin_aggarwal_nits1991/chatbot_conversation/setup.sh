#!/bin/bash

# Multi-Model Chatbot Conversation - Setup Script
# This script helps you set up the application quickly

set -e  # Exit on error

echo "🤖 Multi-Model Chatbot Conversation - Setup Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check Python
echo "📋 Step 1: Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 is not installed!"
    echo "Please install Python 3.8 or higher from https://www.python.org"
    exit 1
fi
echo ""

# Step 2: Check Ollama
echo "📋 Step 2: Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓${NC} Ollama is installed"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo -e "${GREEN}✓${NC} Ollama is running"
    else
        echo -e "${YELLOW}⚠${NC} Ollama is installed but not running"
        echo "Starting Ollama..."
        ollama serve &
        sleep 3
        
        if curl -s http://localhost:11434/api/tags &> /dev/null; then
            echo -e "${GREEN}✓${NC} Ollama started successfully"
        else
            echo -e "${RED}✗${NC} Failed to start Ollama"
            echo "Please start Ollama manually: ollama serve"
            exit 1
        fi
    fi
else
    echo -e "${RED}✗${NC} Ollama is not installed!"
    echo ""
    echo "Please install Ollama:"
    echo "  macOS:   brew install ollama"
    echo "  Linux:   curl -fsSL https://ollama.com/install.sh | sh"
    echo "  Windows: Download from https://ollama.com"
    exit 1
fi
echo ""

# Step 3: Check for models
echo "📋 Step 3: Checking for Ollama models..."
MODEL_COUNT=$(curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('models', [])))" 2>/dev/null || echo "0")

if [ "$MODEL_COUNT" -ge 2 ]; then
    echo -e "${GREEN}✓${NC} Found $MODEL_COUNT model(s)"
    echo "Available models:"
    curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; [print(f'  • {m[\"name\"]}') for m in json.load(sys.stdin).get('models', [])]" 2>/dev/null
else
    echo -e "${YELLOW}⚠${NC} Only $MODEL_COUNT model(s) found. Need at least 2."
    echo ""
    echo "Recommended models to download:"
    echo "  • llama3.2   (Fast, good quality, ~2GB)"
    echo "  • mistral    (Very capable, ~4GB)"
    echo "  • phi3       (Small and fast, ~2GB)"
    echo ""
    read -p "Would you like to download llama3.2 and mistral now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Downloading llama3.2..."
        ollama pull llama3.2
        echo "Downloading mistral..."
        ollama pull mistral
        echo -e "${GREEN}✓${NC} Models downloaded successfully"
    else
        echo "Please download models manually:"
        echo "  ollama pull llama3.2"
        echo "  ollama pull mistral"
        exit 1
    fi
fi
echo ""

# Step 4: Check if virtual environment exists
echo "📋 Step 4: Setting up Python virtual environment..."
if [ -d "venv" ]; then
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
fi
echo ""

# Step 5: Activate virtual environment and install dependencies
echo "📋 Step 5: Installing dependencies..."
source venv/bin/activate

if pip install -r requirements.txt > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Dependencies installed successfully"
else
    echo -e "${RED}✗${NC} Failed to install dependencies"
    echo "Please install manually: pip install -r requirements.txt"
    exit 1
fi
echo ""

# Step 6: Final check
echo "📋 Step 6: Final verification..."

# Check Streamlit
if python3 -c "import streamlit" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Streamlit is installed"
else
    echo -e "${RED}✗${NC} Streamlit not found"
    exit 1
fi

# Check requests
if python3 -c "import requests" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Requests library is installed"
else
    echo -e "${RED}✗${NC} Requests not found"
    exit 1
fi

echo ""
echo "=================================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "🚀 To start the application, run:"
echo ""
echo -e "   ${BLUE}source venv/bin/activate${NC}"
echo -e "   ${BLUE}streamlit run app.py${NC}"
echo ""
echo "Or use the quick start script:"
echo -e "   ${BLUE}./start.sh${NC}"
echo ""
echo "📚 Documentation:"
echo "   • README.md      - Full documentation"
echo "   • QUICKSTART.md  - 3-minute guide"
echo "   • TECHNICAL.md   - Technical details"
echo ""
echo "💡 Tips:"
echo "   • Start with 3 chatbots and 5 turns"
echo "   • Try the example topic: 'Why did the chicken cross the road?'"
echo "   • Mix different personas for interesting conversations"
echo ""
echo "Happy chatting! 🤖💬"
