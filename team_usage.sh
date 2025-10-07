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
