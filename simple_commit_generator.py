#!/usr/bin/env python3
"""
Simple Git Commit Message Generator
Clean, fast, and reliable commit message generation without verbose LLM output.
"""

import subprocess
import argparse
from typing import Dict, Any, Optional


class SimpleDiffAnalyzer:
    """Simple rule-based diff analyzer."""

    def _extract_file_names(self, git_diff: str) -> list:
        """Extract file names from git diff output."""
        files = []
        for line in git_diff.split('\n'):
            if line.startswith('diff --git'):
                # Extract file names from diff --git a/file b/file
                parts = line.split()
                if len(parts) >= 4:
                    file_a = parts[2].split('/')[-1]  # Get just the filename
                    file_b = parts[3].split('/')[-1]  # Get just the filename
                    if file_a != '/dev/null':
                        files.append(file_a)
                    if file_b != '/dev/null' and file_b != file_a:
                        files.append(file_b)
        return files

    def analyze_diff(self, git_diff: str) -> Dict[str, Any]:
        """Analyze git diff using simple heuristics."""
        file_names = self._extract_file_names(git_diff)
        git_diff_lower = git_diff.lower()

        # Check for documentation changes
        has_md_files = any('.md' in f for f in file_names)
        has_doc_patterns = any(keyword in git_diff_lower for keyword in ['<!--', '-->', 'readme'])
        
        # Don't match if it's a .py file with code changes
        is_python_code = any('.py' in f for f in file_names) and any(keyword in git_diff_lower for keyword in ['def ', 'class ', 'import ', 'return '])

        if (has_md_files or has_doc_patterns) and not is_python_code:
            return {
                "change_type": "docs",
                "scope": "documentation",
                "confidence": "high",
                "reasoning": "Documentation changes detected",
                "files": file_names
            }
        # Check for code enhancements and new functionality
        elif any(keyword in git_diff_lower for keyword in ['def ', 'class ', 'import ', 'return ', 'if ', 'for ', 'while ']):
            return {
                "change_type": "feat",
                "scope": "code",
                "confidence": "high",
                "reasoning": "Code enhancements and new functionality detected",
                "files": file_names
            }
        # Check for authentication features
        elif any(keyword in git_diff_lower for keyword in ['log', 'auth', 'login', 'session', 'token', 'jwt']):
            return {
                "change_type": "feat",
                "scope": "auth",
                "confidence": "high",
                "reasoning": "Authentication and security features detected",
                "files": file_names
            }
        elif any(keyword in git_diff_lower for keyword in ['pattern', 'regex', 'validation', 'fix', 'bug', 'error']):
            return {
                "change_type": "fix",
                "scope": "validation",
                "confidence": "high",
                "reasoning": "Bug fixes and validation improvements detected",
                "files": file_names
            }
        elif any(keyword in git_diff_lower for keyword in ['_', 'private', 'encapsulation', 'refactor', 'cleanup']):
            return {
                "change_type": "refactor",
                "scope": "code",
                "confidence": "medium",
                "reasoning": "Code structure and encapsulation improvements detected",
                "files": file_names
            }
        elif any(keyword in git_diff_lower for keyword in ['test', 'spec', 'mock', 'stub']):
            return {
                "change_type": "test",
                "scope": "testing",
                "confidence": "high",
                "reasoning": "Test code additions or modifications detected",
                "files": file_names
            }
        elif any(keyword in git_diff_lower for keyword in ['style', 'format', 'lint', 'prettier']):
            return {
                "change_type": "style",
                "scope": "formatting",
                "confidence": "medium",
                "reasoning": "Code formatting and style changes detected",
                "files": file_names
            }
        elif any(keyword in git_diff_lower for keyword in ['build', 'compile', 'package', 'dependencies']):
            return {
                "change_type": "build",
                "scope": "dependencies",
                "confidence": "high",
                "reasoning": "Build system and dependency changes detected",
                "files": file_names
            }
        elif any(keyword in git_diff_lower for keyword in ['ci', 'pipeline', 'workflow', 'github', 'actions']):
            return {
                "change_type": "ci",
                "scope": "pipeline",
                "confidence": "high",
                "reasoning": "CI/CD pipeline changes detected",
                "files": file_names
            }
        else:
            return {
                "change_type": "chore",
                "scope": "maintenance",
                "confidence": "low",
                "reasoning": "General maintenance changes detected",
                "files": file_names
            }


class SimpleSummaryAgent:
    """Simple rule-based summary agent."""

    def create_summary(self, git_diff: str, change_type: str = None, scope: str = None, files: list = None) -> str:
        """Create simple summary based on change type and scope."""
        # Create file context for summary
        file_context = ""
        if files:
            if len(files) == 1:
                file_context = f" in {files[0]}"
            elif len(files) == 2:
                file_context = f" in {files[0]} and {files[1]}"
            else:
                file_context = f" in {files[0]} and {len(files)-1} other files"

        if change_type == "feat":
            if scope == "auth":
                return f"Add authentication and security features{file_context}"
            else:
                return f"Add new functionality{file_context}"
        elif change_type == "fix":
            if scope == "validation":
                return f"Fix validation and input handling{file_context}"
            else:
                return f"Fix bugs and resolve issues{file_context}"
        elif change_type == "refactor":
            return f"Refactor code for better structure and maintainability{file_context}"
        elif change_type == "test":
            return f"Add or update tests{file_context}"
        elif change_type == "docs":
            if scope == "documentation":
                return f"Update API documentation{file_context}"
            elif scope == "code":
                return f"Comment out code sections{file_context}"
            else:
                return f"Update documentation{file_context}"
        elif change_type == "style":
            return "Improve code formatting and style"
        elif change_type == "build":
            return "Update build configuration and dependencies"
        elif change_type == "ci":
            return "Update CI/CD pipeline configuration"
        else:
            return "Update codebase with maintenance improvements"


class SimpleCommitFormatter:
    """Simple rule-based commit formatter."""

    def format_commit_message(self, change_type: str, summary: str, scope: str = None) -> str:
        """Format commit message using simple rules."""
        scope_part = f"({scope})" if scope and scope != "maintenance" else ""
        
        # Create a clean description based on change type and scope
        if change_type == "feat":
            if scope == "auth":
                description = "add authentication features"
            elif scope == "api":
                description = "add new API endpoints"
            elif scope == "ui":
                description = "add new user interface"
            else:
                description = "add new functionality"
        elif change_type == "fix":
            if scope == "validation":
                description = "fix validation issues"
            elif scope == "bug":
                description = "fix critical bugs"
            else:
                description = "fix issues and bugs"
        elif change_type == "docs":
            if scope == "api":
                description = "update API documentation"
            elif scope == "readme":
                description = "update README"
            else:
                description = "update documentation"
        elif change_type == "refactor":
            description = "refactor code structure"
        elif change_type == "test":
            description = "add or update tests"
        elif change_type == "style":
            description = "improve code formatting"
        elif change_type == "build":
            description = "update build configuration"
        elif change_type == "ci":
            description = "update CI/CD pipeline"
        else:
            description = "maintain codebase"
        
        return f"{change_type}{scope_part}: {description}"


class SimpleCommitMessageGenerator:
    """Simple orchestrator for commit message generation."""

    def __init__(self):
        self.diff_analyzer = SimpleDiffAnalyzer()
        self.summary_agent = SimpleSummaryAgent()
        self.formatter_agent = SimpleCommitFormatter()

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

    def generate_commit_message(self, git_diff: Optional[str] = None, use_staged: bool = False) -> str:
        """Generate commit message using simple multi-agent system."""
        if use_staged:
            git_diff = self.get_staged_diff()
        elif git_diff is None:
            git_diff = self.get_git_diff()

        if not git_diff.strip():
            return "No changes detected or git diff is empty."

        # Step 1: Diff Analysis
        analysis = self.diff_analyzer.analyze_diff(git_diff)

        # Step 2: Summary Creation
        summary = self.summary_agent.create_summary(
            git_diff,
            analysis["change_type"],
            analysis["scope"],
            analysis.get("files", [])
        )

        # Step 3: Commit Formatting
        commit_message = self.formatter_agent.format_commit_message(
            analysis["change_type"],
            summary,
            analysis["scope"]
        )

        return commit_message


def main():
    """Main entry point for simple commit message generator."""
    parser = argparse.ArgumentParser(
        description="Simple Git Commit Message Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simple_commit_generator.py                    # Use last commit
  python simple_commit_generator.py --staged         # Use staged changes
  python simple_commit_generator.py HEAD~2 HEAD     # Custom commit range
        """
    )

    parser.add_argument("--staged", action="store_true",
                       help="Use staged changes instead of last commit")
    parser.add_argument("commit_range", nargs="?",
                       help="Custom commit range (e.g., HEAD~2 HEAD)")

    args = parser.parse_args()

    # Initialize the simple generator
    generator = SimpleCommitMessageGenerator()

    print("🚀 Simple Git Commit Message Generator")
    print("=" * 50)

    # Generate commit message
    if args.staged:
        print("📋 Using staged changes...")
        commit_message = generator.generate_commit_message(use_staged=True)
    elif args.commit_range:
        print(f"📊 Using commit range: {args.commit_range}")
        commit_message = generator.generate_commit_message(
            git_diff=generator.get_git_diff(args.commit_range)
        )
    else:
        print("📊 Using last commit...")
        commit_message = generator.generate_commit_message()

    # Output the result
    print("\n" + "="*50)
    print("🎯 GENERATED COMMIT MESSAGE:")
    print("="*50)
    print(commit_message)
    print("="*50)

    # Copy to clipboard if possible
    try:
        import pyperclip
        pyperclip.copy(commit_message)
        print("\n📋 Commit message copied to clipboard!")
    except ImportError:
        print("\n💡 Tip: Install pyperclip to auto-copy to clipboard")
    except Exception as e:
        print(f"\n⚠️  Could not copy to clipboard: {e}")


if __name__ == "__main__":
    main()
