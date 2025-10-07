#!/bin/bash
# Add this to your ~/.zshrc or ~/.bashrc file

# Git Commit Message Generator Alias
alias commit-msg="cd /Users/sanjaymali/Documents/AI-Apps && source venv/bin/activate && python production_commit_generator.py --staged"

echo "Add this line to your ~/.zshrc file:"
echo "alias commit-msg=\"cd /Users/sanjaymali/Documents/AI-Apps && source venv/bin/activate && python fast_commit_generator.py --staged --copy\""
echo ""
echo "Then run: source ~/.zshrc"
echo "After that, you can simply use: commit-msg"
