#!/bin/bash

# Paper2Data Web Demo Quick Start Script

echo "🚀 Starting Paper2Data Web Demo..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo "🌐 Starting web server..."
echo "📍 Open your browser to: http://localhost:8000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python3 main_simple.py
