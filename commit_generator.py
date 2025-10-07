"""
Git Commit Message Generator - Multi-Agent System using CrewAI
Implements the three-agent system as described in the README
"""

import os
import subprocess
import argparse
from typing import Dict, Any, Optional
from enum import Enum

# Set up environment for CrewAI
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


class DiffAnalysisAgent:
    """
    Agent 1: Diff Analysis Agent
    Role: Expert at analyzing git diffs and identifying change patterns
    Goal: Classify changes into appropriate conventional commit types
    """
    
    def __init__(self):
        self.llm = LLM(model="ollama/llama3:latest", base_url="http://localhost:11434")
        self.agent = Agent(
            role="Diff Analysis Expert",
            goal="Analyze git diffs to identify the primary purpose and type of change",
            backstory="""You are an expert software engineer with deep experience in
            code review and version control. You excel at reading git diffs and
            identifying the nature of changes - whether they are new features,
            bug fixes, refactoring, documentation updates, or other types of changes.
            You understand conventional commit standards and can accurately classify
            changes into appropriate categories.""",
            verbose=False,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _extract_file_names(self, git_diff: str) -> list:
        """Extract file names from git diff output."""
        import re
        file_pattern = r'^diff --git a/(.+?) b/(.+?)$'
        files = []
        for line in git_diff.split('\n'):
            match = re.match(file_pattern, line)
            if match:
                file_path = match.group(2)  # Use the 'b/' path (new file path)
                files.append(file_path)
        return files
    
    def analyze_diff(self, git_diff: str) -> Dict[str, Any]:
        """Analyze git diff using CrewAI agent."""
        file_names = self._extract_file_names(git_diff)
        
        # Create task for diff analysis
        task = Task(
            description=f"""
            Analyze the following git diff and determine:
            1. The primary type of change (feat, fix, docs, style, refactor, test, chore, build, ci)
            2. The scope/domain of the change (auth, validation, code, documentation, etc.)
            3. The confidence level (high, medium, low)
            4. Brief reasoning for the classification

            Special rules:
            - If .md files are changed, use "docs" type and "markdown" scope
            - If README.md is changed, use "docs" type and "readme" scope
            - If API documentation is changed, use "docs" type and "api" scope
            - If .py files are changed, use "feat" type and "code" scope
            - If function/class definitions are added, use "feat" type
            - If bugs are fixed, use "fix" type
            - If code is refactored, use "refactor" type

            Git Diff:
            {git_diff}

            Return your analysis in this exact JSON format:
            {{
                "change_type": "feat|fix|docs|style|refactor|test|chore|build|ci",
                "scope": "specific_scope",
                "confidence": "high|medium|low",
                "reasoning": "brief explanation"
            }}
            """,
            agent=self.agent,
            expected_output="JSON object with change_type, scope, confidence, and reasoning"
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        try:
            import json
            result = crew.kickoff()
            analysis = json.loads(str(result))
            analysis["files"] = file_names
            return analysis
        except:
            # Fallback: analyze based on file types if LLM fails
            if any('README.md' in f for f in file_names):
                return {"change_type": "docs", "scope": "readme", "confidence": "high", "files": file_names}
            elif any('.md' in f for f in file_names):
                return {"change_type": "docs", "scope": "markdown", "confidence": "high", "files": file_names}
            elif any('.py' in f for f in file_names):
                return {"change_type": "feat", "scope": "code", "confidence": "high", "files": file_names}
            else:
                return {"change_type": "chore", "scope": "maintenance", "confidence": "low", "files": file_names}


class SummaryAgent:
    """
    Agent 2: Summary Agent
    Role: Specialized in creating clear, human-readable summaries
    Goal: Generate concise summaries of changes for commit messages
    """
    
    def __init__(self):
        self.llm = LLM(model="ollama/llama3:latest", base_url="http://localhost:11434")
        self.agent = Agent(
            role="Technical Summary Specialist",
            goal="Create clear, concise summaries of code changes",
            backstory="""You are a technical writer with expertise in clear communication.
            You excel at creating brief, informative summaries of code changes that
            help developers understand what was modified and why. You focus on the
            key functionality and impact of changes.""",
            verbose=False,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_summary(self, git_diff: str, analysis: Dict[str, Any]) -> str:
        """Create summary using CrewAI agent."""
        # Create task for summary generation
        task = Task(
            description=f"""
            Create a concise, human-readable summary of the code changes.
            
            Analysis Results:
            - Change Type: {analysis.get('change_type', 'unknown')}
            - Scope: {analysis.get('scope', 'unknown')}
            - Files: {', '.join(analysis.get('files', []))}
            
            Git Diff:
            {git_diff[:1000]}...
            
            Create a brief summary (1-2 sentences) that captures:
            1. What was changed
            2. Why it was changed (if apparent)
            
            Focus on the key functionality and impact.
            """,
            agent=self.agent,
            expected_output="Brief summary of the changes (1-2 sentences)"
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        try:
            result = crew.kickoff()
            return str(result).strip()
        except:
            # Fallback: create simple summary based on analysis
            change_type = analysis.get('change_type', 'chore')
            scope = analysis.get('scope', 'maintenance')
            files = analysis.get('files', [])
            
            if change_type == "feat":
                return f"Add new {scope} functionality"
            elif change_type == "fix":
                return f"Fix {scope} issues"
            elif change_type == "docs":
                return f"Update {scope} documentation"
            else:
                return f"Update {scope} components"


class CommitFormatterAgent:
    """
    Agent 3: Commit Formatter Agent
    Role: Expert in conventional commit standards and formatting
    Goal: Format messages according to conventional commit specification
    """
    
    def __init__(self):
        self.llm = LLM(model="ollama/llama3:latest", base_url="http://localhost:11434")
        self.agent = Agent(
            role="Conventional Commit Specialist",
            goal="Format commit messages according to Conventional Commits specification",
            backstory="""You are an expert in conventional commit standards and best practices.
            You understand the importance of consistent, clear commit messages for
            team collaboration, automated tooling, and project maintenance. You
            excel at formatting commit messages that follow conventional commit
            standards while being clear and informative.""",
            verbose=False,
            allow_delegation=False,
            llm=self.llm
        )
    
    def format_commit_message(self, change_type: str, scope: str, summary: str) -> str:
        """Format commit message using CrewAI agent."""
        # Create task for commit formatting
        task = Task(
            description=f"""
            You are a Conventional Commit Specialist. Create a proper commit message.

            Input Details:
            - Change Type: {change_type}
            - Scope: {scope}
            - Summary: {summary}

            Requirements:
            1. Format: type(scope): description
            2. Use the provided change_type and scope
            3. Create a clear, concise description based on the summary
            4. Keep under 50 characters
            5. Follow conventional commit standards

            Examples:
            - feat(auth): add user authentication
            - fix(validation): resolve email validation error
            - docs(api): update API documentation

            Output ONLY the commit message in the format: type(scope): description
            Do not include any other text, explanations, or formatting.
            """,
            agent=self.agent,
            expected_output="Conventional commit message in format: type(scope): description"
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        try:
            result = crew.kickoff()
            formatted_result = str(result).strip()
            
            # Validate the result
            if ':' in formatted_result and len(formatted_result) <= 50:
                return formatted_result
            else:
                # Fallback: create proper conventional commit message manually
                scope_part = f"({scope})" if scope and scope != "maintenance" else ""
                
                # Create a clean description based on change type and scope
                if change_type == "feat":
                    if scope == "auth":
                        description = "add authentication features"
                    elif scope == "api":
                        description = "add new API endpoints"
                    elif scope == "ui":
                        description = "add new user interface"
                    elif scope == "code":
                        description = "add new functionality"
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
                    elif scope == "markdown":
                        description = "update markdown documentation"
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
        except:
            # Fallback: create proper conventional commit message manually
            scope_part = f"({scope})" if scope and scope != "maintenance" else ""
            
            if change_type == "feat":
                description = "add new functionality"
            elif change_type == "fix":
                description = "fix issues and bugs"
            elif change_type == "docs":
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


class GitService:
    """Service class for git operations."""
    
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
    """
    Main orchestrator for the multi-agent system.
    Coordinates the three agents: Diff Analysis, Summary, and Commit Formatter.
    """
    
    def __init__(self):
        self.diff_analyzer = DiffAnalysisAgent()
        self.summary_agent = SummaryAgent()
        self.formatter_agent = CommitFormatterAgent()
        self.git_service = GitService()
    
    def generate(self, git_diff: Optional[str] = None, use_staged: bool = False) -> str:
        """Generate commit message using the multi-agent system."""
        if use_staged:
            git_diff = self.git_service.get_staged_diff()
        elif git_diff is None:
            git_diff = self.git_service.get_commit_diff()
        
        if not git_diff.strip():
            return "No changes detected."
        
        # Step 1: Diff Analysis Agent
        analysis = self.diff_analyzer.analyze_diff(git_diff)
        
        # Step 2: Summary Agent
        summary = self.summary_agent.create_summary(git_diff, analysis)
        
        # Step 3: Commit Formatter Agent
        commit_message = self.formatter_agent.format_commit_message(
            analysis["change_type"],
            analysis["scope"],
            summary
        )
        
        return commit_message


def main():
    """CLI interface for the multi-agent system."""
    parser = argparse.ArgumentParser(
        description="Git Commit Message Generator - Multi-Agent System with CrewAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python commit_generator.py                    # Use last commit
  python commit_generator.py --staged          # Use staged changes
  python commit_generator.py HEAD~2 HEAD      # Custom commit range
        """
    )
    
    parser.add_argument("--staged", action="store_true",
                        help="Use staged changes instead of last commit")
    parser.add_argument("--copy", action="store_true",
                        help="Copy generated message to clipboard")
    parser.add_argument("commit_range", nargs="?",
                        help="Custom commit range (e.g., HEAD~2 HEAD)")
    
    args = parser.parse_args()
    
    generator = CommitMessageGenerator()
    
    commit_message = generator.generate(
        use_staged=args.staged,
        git_diff=generator.git_service.get_commit_diff(args.commit_range) if args.commit_range else None
    )
    
    print("🎯 GENERATED COMMIT MESSAGE:")
    print("=" * 50)
    print(commit_message)
    print("=" * 50)
    
    if args.copy:
        try:
            import pyperclip
            pyperclip.copy(commit_message)
            print("📋 Copied to clipboard!")
        except ImportError:
            print("💡 Tip: Install pyperclip to auto-copy to clipboard")
        except Exception as e:
            print(f"⚠️  Could not copy to clipboard: {e}")


if __name__ == "__main__":
    main()