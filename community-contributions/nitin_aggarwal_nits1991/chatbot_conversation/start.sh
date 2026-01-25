#!/bin/bash

# Quick start script for Multi-Model Chatbot Conversation

echo "🤖 Starting Multi-Model Chatbot Conversation..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./setup.sh
fi

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "⚠️  Ollama is not running. Please start it first:"
    echo "   ollama serve"
    exit 1
fi

# Start Streamlit
echo "🚀 Launching application..."
streamlit run app.py
