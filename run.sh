#!/bin/bash
# Sovereign Intelligence Framework - Startup Script

echo "================================"
echo "SOVEREIGN INTELLIGENCE FRAMEWORK"
echo "Tactical Archive Dashboard"
echo "================================"
echo ""

# Check Python
python --version

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "Starting dashboard..."
echo "🎯 Launching on http://localhost:8501"
echo ""

streamlit run app.py
