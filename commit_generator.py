"""
Git Commit Message Generator - Clean Architecture
Following SOLID, DRY, KISS, YAGNI principles
"""

import os
import subprocess
import argparse
from typing import Dict, Any, Optional
from enum import Enum

# Set up environment
os.environ["CREWAI_TRACING_ENABLED"] = "false"
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["OLLAMA_MODEL"] = "llama3"

from crewai import Agent, Task, Crew, Process, LLM


class ChangeType(Enum):
    """Enum for commit types following conventional commits."""
    FEAT = "feat"
    FIX = "fix"
    DOCS = "docs"
    STYLE = "style"
    REFACTOR = "refactor"
    TEST = "test"
    CHORE = "chore"
    BUILD = "build"
    CI = "ci"


class Scope(Enum):
    """Enum for commit scopes."""
    CODE = "code"
    MARKDOWN = "markdown"
    README = "readme"
    API = "api"
    AUTH = "auth"
    UI = "ui"
    VALIDATION = "validation"
    MAINTENANCE = "maintenance"


class BaseAgent:
    """Base class for all agents following DRY principle."""
    
    def __init__(self, role: str, goal: str, backstory: str):
        self.llm = LLM(model="ollama/llama3:latest", base_url="http://localhost:11434")
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=False,
            allow_delegation=False,
            llm=self.llm
        )


class DiffAnalyzer(BaseAgent):
    """Single responsibility: Analyze git diffs."""
    
    def __init__(self):
        super().__init__(
            role="Diff Analysis Expert",
            goal="Analyze git diffs to identify change type and scope",
            backstory="Expert at reading git diffs and classifying changes."
        )
    
    def _extract_files(self, git_diff: str) -> list:
        """Extract file names from git diff."""
        import re
        pattern = r'^diff --git a/(.+?) b/(.+?)$'
        return [match.group(2) for line in git_diff.split('\n') 
                for match in [re.match(pattern, line)] if match]
    
    def analyze(self, git_diff: str) -> Dict[str, Any]:
        """Analyze diff and return structured data."""
        files = self._extract_files(git_diff)
        
        # Simple rule-based analysis (KISS principle)
        if any('.md' in f for f in files):
            return {
                "change_type": ChangeType.DOCS.value,
                "scope": Scope.MARKDOWN.value,
                "confidence": "high",
                "files": files
            }
        elif any('.py' in f for f in files):
            return {
                "change_type": ChangeType.FEAT.value,
                "scope": Scope.CODE.value,
                "confidence": "high",
                "files": files
            }
        else:
            return {
                "change_type": ChangeType.CHORE.value,
                "scope": Scope.MAINTENANCE.value,
                "confidence": "low",
                "files": files
            }


class CommitFormatter:
    """Single responsibility: Format commit messages."""
    
    def __init__(self):
        self.descriptions = {
            ChangeType.FEAT.value: {
                Scope.AUTH.value: "add authentication features",
                Scope.API.value: "add new API endpoints",
                Scope.UI.value: "add new user interface",
                Scope.CODE.value: "add new functionality"
            },
            ChangeType.FIX.value: {
                Scope.VALIDATION.value: "fix validation issues",
                "bug": "fix critical bugs"
            },
            ChangeType.DOCS.value: {
                Scope.API.value: "update API documentation",
                Scope.README.value: "update README",
                Scope.MARKDOWN.value: "update markdown documentation"
            }
        }
    
    def format(self, change_type: str, scope: str) -> str:
        """Format commit message following conventional commits."""
        scope_part = f"({scope})" if scope != Scope.MAINTENANCE.value else ""
        
        # Get description with fallback
        description = (self.descriptions
                      .get(change_type, {})
                      .get(scope, self._get_default_description(change_type)))
        
        return f"{change_type}{scope_part}: {description}"
    
    def _get_default_description(self, change_type: str) -> str:
        """Get default description for change type."""
        defaults = {
            ChangeType.FEAT.value: "add new functionality",
            ChangeType.FIX.value: "fix issues and bugs",
            ChangeType.DOCS.value: "update documentation",
            ChangeType.REFACTOR.value: "refactor code structure",
            ChangeType.TEST.value: "add or update tests",
            ChangeType.STYLE.value: "improve code formatting",
            ChangeType.CHORE.value: "maintain codebase"
        }
        return defaults.get(change_type, "update codebase")


class GitService:
    """Single responsibility: Handle git operations."""
    
    @staticmethod
    def get_staged_diff() -> str:
        """Get staged changes."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached"],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""
    
    @staticmethod
    def get_commit_diff(commit_range: str = "HEAD~1 HEAD") -> str:
        """Get commit diff."""
        try:
            result = subprocess.run(
                ["git", "diff", commit_range],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""


class CommitMessageGenerator:
    """Main orchestrator following Single Responsibility Principle."""
    
    def __init__(self):
        self.diff_analyzer = DiffAnalyzer()
        self.formatter = CommitFormatter()
        self.git_service = GitService()
    
    def generate(self, git_diff: Optional[str] = None, use_staged: bool = False) -> str:
        """Generate commit message - simple and focused."""
        if use_staged:
            git_diff = self.git_service.get_staged_diff()
        elif git_diff is None:
            git_diff = self.git_service.get_commit_diff()
        
        if not git_diff.strip():
            return "No changes detected."
        
        # Analyze diff
        analysis = self.diff_analyzer.analyze(git_diff)
        
        # Format message
        return self.formatter.format(
            analysis["change_type"],
            analysis["scope"]
        )


def main():
    """Simple CLI interface."""
    parser = argparse.ArgumentParser(description="Git Commit Message Generator")
    parser.add_argument("--staged", action="store_true", help="Use staged changes")
    parser.add_argument("--copy", action="store_true", help="Copy to clipboard")
    args = parser.parse_args()
    
    generator = CommitMessageGenerator()
    message = generator.generate(use_staged=args.staged)
    
    print("🎯 GENERATED COMMIT MESSAGE:")
    print("=" * 50)
    print(message)
    print("=" * 50)
    
    if args.copy:
        try:
            import pyperclip
            pyperclip.copy(message)
            print("📋 Copied to clipboard!")
        except ImportError:
            print("💡 Install pyperclip for auto-copy")


if __name__ == "__main__":
    main()
