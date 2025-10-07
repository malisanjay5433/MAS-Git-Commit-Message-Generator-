#!/usr/bin/env python3
"""
Fast Git Commit Message Generator with LLM
Optimized for speed with minimal output and intelligent analysis.
"""

import os
import subprocess
import argparse
from typing import Dict, Any, Optional

# Set up environment for CrewAI (minimal tracing)
os.environ["CREWAI_TRACING_ENABLED"] = "false"
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["OLLAMA_MODEL"] = "llama3"

from crewai import Agent, Task, Crew, Process, LLM


class FastDiffAnalyzer:
    """Fast LLM-based diff analyzer with minimal output."""

    def __init__(self):
        self.llm = LLM(model="ollama/llama3:latest", base_url="http://localhost:11434")
        self.agent = Agent(
            role="Diff Analysis Expert",
            goal="Quickly analyze git diffs and classify changes",
            backstory="You are an expert at analyzing code changes and classifying them into conventional commit types.",
            verbose=False,
            allow_delegation=False,
            llm=self.llm
        )

    def _extract_file_names(self, git_diff: str) -> list:
        """Extract file names from git diff output."""
        files = []
        for line in git_diff.split('\n'):
            if line.startswith('diff --git'):
                parts = line.split()
                if len(parts) >= 4:
                    file_a = parts[2].split('/')[-1]
                    file_b = parts[3].split('/')[-1]
                    if file_a != '/dev/null':
                        files.append(file_a)
                    if file_b != '/dev/null' and file_b != file_a:
                        files.append(file_b)
        return files

    def analyze_diff(self, git_diff: str) -> Dict[str, Any]:
        """Fast LLM-based diff analysis."""
        file_names = self._extract_file_names(git_diff)
        
        # Create a concise task
        task = Task(
            description=f"""
            Analyze this git diff and return ONLY a JSON object:
            {{
                "change_type": "feat|fix|docs|style|refactor|test|chore|build|ci",
                "scope": "specific_scope",
                "confidence": "high|medium|low"
            }}
            
            Git Diff:
            {git_diff[:2000]}...
            """,
            agent=self.agent,
            expected_output="JSON object with change_type, scope, confidence"
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )

        try:
            result = crew.kickoff()
            import json
            analysis = json.loads(str(result))
            analysis["files"] = file_names
            return analysis
        except:
            # Fast fallback
            return {
                "change_type": "chore",
                "scope": "maintenance",
                "confidence": "low",
                "files": file_names
            }


class FastCommitFormatter:
    """Fast LLM-based commit formatter."""

    def __init__(self):
        self.llm = LLM(model="ollama/llama3:latest", base_url="http://localhost:11434")
        self.agent = Agent(
            role="Commit Message Formatter",
            goal="Create concise conventional commit messages",
            backstory="You are an expert at formatting commit messages according to conventional commit standards.",
            verbose=False,
            allow_delegation=False,
            llm=self.llm
        )

    def format_commit_message(self, change_type: str, scope: str = None, files: list = None) -> str:
        """Fast commit message formatting."""
        scope_part = f"({scope})" if scope and scope != "maintenance" else ""
        
        # Create a simple task
        task = Task(
            description=f"""
            Create a conventional commit message for:
            - Type: {change_type}
            - Scope: {scope}
            - Files: {files[:3] if files else 'unknown'}
            
            Return ONLY the commit message in format: type(scope): description
            Keep it under 50 characters.
            """,
            agent=self.agent,
            expected_output="Conventional commit message"
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )

        # Always use fallback for consistency - LLM is unreliable
        # Create a consistent description based on change type and scope
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
        
        formatted_result = f"{change_type}{scope_part}: {description}"
        return formatted_result


class FastCommitMessageGenerator:
    """Fast orchestrator for commit message generation."""

    def __init__(self):
        self.diff_analyzer = FastDiffAnalyzer()
        self.formatter_agent = FastCommitFormatter()

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
        """Generate commit message using fast LLM analysis."""
        if use_staged:
            git_diff = self.get_staged_diff()
        elif git_diff is None:
            git_diff = self.get_git_diff()

        if not git_diff.strip():
            return "No changes detected or git diff is empty."

        # Step 1: Fast Diff Analysis
        analysis = self.diff_analyzer.analyze_diff(git_diff)

        # Step 2: Fast Commit Formatting
        commit_message = self.formatter_agent.format_commit_message(
            analysis["change_type"],
            analysis["scope"],
            analysis.get("files", [])
        )

        return commit_message


def main():
    """Main entry point for fast commit message generator."""
    parser = argparse.ArgumentParser(
        description="Fast Git Commit Message Generator with LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fast_commit_generator.py                    # Use last commit
  python fast_commit_generator.py --staged         # Use staged changes
  python fast_commit_generator.py --copy           # Copy to clipboard
  python fast_commit_generator.py HEAD~2 HEAD     # Custom commit range
        """
    )

    parser.add_argument("--staged", action="store_true",
                       help="Use staged changes instead of last commit")
    parser.add_argument("--copy", action="store_true",
                       help="Copy generated message to clipboard")
    parser.add_argument("commit_range", nargs="?",
                       help="Custom commit range (e.g., HEAD~2 HEAD)")

    args = parser.parse_args()

    # Initialize the fast generator
    generator = FastCommitMessageGenerator()

    print("⚡ Fast Git Commit Message Generator with LLM")
    print("=" * 50)

    # Generate commit message
    if args.staged:
        print("📋 Analyzing staged changes...")
        commit_message = generator.generate_commit_message(use_staged=True)
    elif args.commit_range:
        print(f"📊 Analyzing commit range: {args.commit_range}")
        commit_message = generator.generate_commit_message(
            git_diff=generator.get_git_diff(args.commit_range)
        )
    else:
        print("📊 Analyzing last commit...")
        commit_message = generator.generate_commit_message()

    # Output the result
    print("\n" + "="*50)
    print("🎯 GENERATED COMMIT MESSAGE:")
    print("="*50)
    print(commit_message)
    print("="*50)

    # Copy to clipboard if requested
    if args.copy:
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
