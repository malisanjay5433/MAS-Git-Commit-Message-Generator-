"""
Production Git Commit Message Generator - Multi-Agent System

This is a production-ready version for team deployment that provides
consistent commit message generation across all engineers.
"""

import os
import subprocess
import sys
import argparse
from typing import Dict, Any, Optional
from pathlib import Path


class ProductionDiffAnalyzer:
    """Production-ready Diff Analysis Agent."""
    
    def __init__(self):
        self.role = "Diff Analysis Expert"
        self.goal = "Analyze git diffs to identify the primary purpose and type of change"
    
    def analyze_diff(self, git_diff: str) -> Dict[str, Any]:
        """Analyze git diff using production-ready heuristics."""
        git_diff_lower = git_diff.lower()
        
        # Enhanced analysis for production use
        if any(keyword in git_diff_lower for keyword in ['log', 'auth', 'login', 'session', 'token', 'jwt']):
            return {
                "change_type": "feat",
                "scope": "auth",
                "confidence": "high",
                "reasoning": "Authentication and security features detected"
            }
        elif any(keyword in git_diff_lower for keyword in ['pattern', 'regex', 'validation', 'fix', 'bug', 'error']):
            return {
                "change_type": "fix",
                "scope": "validation",
                "confidence": "high",
                "reasoning": "Bug fixes and validation improvements detected"
            }
        elif any(keyword in git_diff_lower for keyword in ['_', 'private', 'encapsulation', 'refactor', 'cleanup']):
            return {
                "change_type": "refactor",
                "scope": "code",
                "confidence": "medium",
                "reasoning": "Code structure and encapsulation improvements detected"
            }
        elif any(keyword in git_diff_lower for keyword in ['test', 'spec', 'mock', 'stub']):
            return {
                "change_type": "test",
                "scope": "testing",
                "confidence": "high",
                "reasoning": "Test code additions or modifications detected"
            }
        elif any(keyword in git_diff_lower for keyword in ['doc', 'readme', 'comment', 'explanation']):
            return {
                "change_type": "docs",
                "scope": "documentation",
                "confidence": "high",
                "reasoning": "Documentation updates detected"
            }
        elif any(keyword in git_diff_lower for keyword in ['style', 'format', 'lint', 'prettier']):
            return {
                "change_type": "style",
                "scope": "formatting",
                "confidence": "medium",
                "reasoning": "Code formatting and style changes detected"
            }
        elif any(keyword in git_diff_lower for keyword in ['build', 'compile', 'package', 'dependencies']):
            return {
                "change_type": "build",
                "scope": "dependencies",
                "confidence": "high",
                "reasoning": "Build system and dependency changes detected"
            }
        elif any(keyword in git_diff_lower for keyword in ['ci', 'pipeline', 'workflow', 'github', 'actions']):
            return {
                "change_type": "ci",
                "scope": "pipeline",
                "confidence": "high",
                "reasoning": "CI/CD pipeline changes detected"
            }
        else:
            return {
                "change_type": "chore",
                "scope": "maintenance",
                "confidence": "low",
                "reasoning": "General maintenance changes detected"
            }


class ProductionSummaryAgent:
    """Production-ready Summary Agent."""
    
    def __init__(self):
        self.role = "Technical Writer & Code Summarizer"
        self.goal = "Create clear, concise, and human-readable summaries of code changes"
    
    def create_summary(self, git_diff: str, change_type: str = None, scope: str = None) -> str:
        """Create production-quality summary based on change type and scope."""
        if change_type == "feat":
            if scope == "auth":
                return "Add authentication and security features"
            else:
                return "Add new functionality"
        elif change_type == "fix":
            if scope == "validation":
                return "Fix validation and input handling"
            else:
                return "Fix bugs and resolve issues"
        elif change_type == "refactor":
            return "Refactor code for better structure and maintainability"
        elif change_type == "test":
            return "Add or update tests"
        elif change_type == "docs":
            return "Update documentation"
        elif change_type == "style":
            return "Improve code formatting and style"
        elif change_type == "build":
            return "Update build configuration and dependencies"
        elif change_type == "ci":
            return "Update CI/CD pipeline configuration"
        else:
            return "Update codebase with maintenance improvements"


class ProductionCommitFormatter:
    """Production-ready Commit Formatter Agent."""
    
    def __init__(self):
        self.role = "Conventional Commit Specialist"
        self.goal = "Format commit messages according to Conventional Commits specification"
    
    def format_commit_message(self, change_type: str, summary: str, scope: str = None) -> str:
        """Format commit message according to conventional commit standards."""
        if scope and scope != "none" and scope != "maintenance":
            return f"{change_type}({scope}): {summary.lower()}"
        else:
            return f"{change_type}: {summary.lower()}"


class ProductionCommitMessageGenerator:
    """Production-ready orchestrator for the multi-agent commit message generation system."""
    
    def __init__(self):
        self.diff_analyzer = ProductionDiffAnalyzer()
        self.summary_agent = ProductionSummaryAgent()
        self.formatter_agent = ProductionCommitFormatter()
    
    def get_git_diff(self, commit_range: str = "HEAD~1 HEAD") -> str:
        """Get git diff for the specified commit range."""
        try:
            result = subprocess.run(
                ["git", "diff", commit_range],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting git diff: {e}")
            return ""
        except FileNotFoundError:
            print("Git not found. Please ensure git is installed and you're in a git repository.")
            return ""
    
    def get_staged_diff(self) -> str:
        """Get git diff for staged changes."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting staged diff: {e}")
            return ""
    
    def generate_commit_message(self, git_diff: Optional[str] = None, 
                              use_staged: bool = False, verbose: bool = False) -> str:
        """Generate a conventional commit message using the multi-agent system."""
        
        # Get git diff if not provided
        if git_diff is None:
            if use_staged:
                git_diff = self.get_staged_diff()
            else:
                git_diff = self.get_git_diff()
        
        if not git_diff.strip():
            return "No changes detected or git diff is empty."
        
        if verbose:
            print("🔍 Multi-Agent System Workflow:")
            print("=" * 50)
        
        # Step 1: Diff Analysis
        if verbose:
            print("\n📊 Step 1: Diff Analysis Agent")
            print("-" * 30)
        analysis = self.diff_analyzer.analyze_diff(git_diff)
        if verbose:
            print(f"Agent: {self.diff_analyzer.role}")
            print(f"Analysis: {analysis}")
        
        # Step 2: Summary Creation
        if verbose:
            print("\n📝 Step 2: Summary Agent")
            print("-" * 30)
        summary = self.summary_agent.create_summary(
            git_diff, 
            analysis["change_type"], 
            analysis["scope"]
        )
        if verbose:
            print(f"Agent: {self.summary_agent.role}")
            print(f"Summary: {summary}")
        
        # Step 3: Commit Formatting
        if verbose:
            print("\n🎯 Step 3: Commit Formatter Agent")
            print("-" * 30)
        commit_message = self.formatter_agent.format_commit_message(
            analysis["change_type"],
            summary,
            analysis["scope"]
        )
        if verbose:
            print(f"Agent: {self.formatter_agent.role}")
            print(f"Formatted Message: {commit_message}")
        
        return commit_message


def main():
    """Main entry point for production commit message generator."""
    parser = argparse.ArgumentParser(
        description="Production Git Commit Message Generator - Multi-Agent System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python production_commit_generator.py                    # Use last commit
  python production_commit_generator.py --staged         # Use staged changes
  python production_commit_generator.py --verbose       # Show detailed workflow
  python production_commit_generator.py --copy          # Copy to clipboard
  python production_commit_generator.py HEAD~2 HEAD     # Custom commit range
        """
    )
    
    parser.add_argument('--staged', action='store_true', 
                       help='Use staged changes instead of last commit')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed multi-agent workflow')
    parser.add_argument('--copy', '-c', action='store_true',
                       help='Copy generated message to clipboard')
    parser.add_argument('commit_range', nargs='?', default=None,
                       help='Custom commit range (e.g., HEAD~2 HEAD)')
    
    args = parser.parse_args()
    
    print("🚀 Production Git Commit Message Generator")
    print("=" * 60)
    print("Multi-Agent System for Team Consistency")
    print("=" * 60)
    
    # Initialize the production generator
    generator = ProductionCommitMessageGenerator()
    
    # Determine git diff source
    if args.staged:
        print("📋 Using staged changes...")
        commit_message = generator.generate_commit_message(use_staged=True, verbose=args.verbose)
    elif args.commit_range:
        print(f"📊 Using custom commit range: {args.commit_range}")
        commit_message = generator.generate_commit_message(
            git_diff=generator.get_git_diff(args.commit_range), 
            verbose=args.verbose
        )
    else:
        print("📊 Using last commit...")
        commit_message = generator.generate_commit_message(verbose=args.verbose)
    
    # Output the result
    print("\n" + "="*60)
    print("🎯 GENERATED COMMIT MESSAGE:")
    print("="*60)
    print(commit_message)
    print("="*60)
    
    # Copy to clipboard if requested
    if args.copy:
        try:
            import pyperclip
            pyperclip.copy(commit_message)
            print("\n📋 Commit message copied to clipboard!")
        except ImportError:
            print("\n💡 Install pyperclip to enable clipboard functionality: pip install pyperclip")
    
    return commit_message


if __name__ == "__main__":
    main()
