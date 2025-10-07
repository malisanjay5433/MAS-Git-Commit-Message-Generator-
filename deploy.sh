#!/bin/bash

# Production Git Commit Message Generator - Deployment Script
# This script sets up the multi-agent system for team-wide usage

echo "🚀 Deploying Git Commit Message Generator for Team Consistency"
echo "=============================================================="

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Make the production script executable
chmod +x production_commit_generator.py

# Create team configuration
echo "⚙️  Setting up team configuration..."

# Create git alias for easy usage
echo "🔗 Setting up git alias..."
git config --global alias.commit-msg '!python3 $(pwd)/production_commit_generator.py --staged'

# Create team usage script
cat > team_usage.sh << 'EOF'
#!/bin/bash
# Team Usage Script for Git Commit Message Generator

echo "🎯 Git Commit Message Generator - Team Usage"
echo "============================================="
echo ""
echo "Available commands:"
echo "  ./production_commit_generator.py --staged    # Generate from staged changes"
echo "  ./production_commit_generator.py --verbose  # Show detailed workflow"
echo "  ./production_commit_generator.py --copy     # Copy to clipboard"
echo "  ./production_commit_generator.py --help     # Show all options"
echo ""
echo "Quick usage:"
echo "  1. Stage your changes: git add ."
echo "  2. Generate commit message: ./production_commit_generator.py --staged --copy"
echo "  3. Commit with generated message: git commit -m \"[generated message]\""
echo ""
echo "For team consistency, all engineers should use this system!"
EOF

chmod +x team_usage.sh

echo ""
echo "✅ Deployment Complete!"
echo "======================"
echo ""
echo "🎯 For Team Usage:"
echo "  ./team_usage.sh                    # Show usage instructions"
echo "  ./production_commit_generator.py --help  # Show all options"
echo ""
echo "📋 Quick Start:"
echo "  1. Stage changes: git add ."
echo "  2. Generate message: ./production_commit_generator.py --staged --copy"
echo "  3. Commit: git commit -m \"[generated message]\""
echo ""
echo "🔧 Team Setup:"
echo "  - Share this repository with your team"
echo "  - Run this deploy script on each engineer's machine"
echo "  - Use the production generator for consistent commit messages"
echo ""
echo "🎉 Your team now has consistent commit message generation!"
