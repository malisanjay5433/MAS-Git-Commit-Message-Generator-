"""
Git Commit Message Generator - Multi-Agent System

This module orchestrates a team of AI agents to generate conventional commit messages
from git diffs using specialized agents for analysis, summarization, and formatting.
"""

import os
import subprocess
import sys
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

from agents.diff_analyzer import DiffAnalyzerAgent
from agents.summary_agent import SummaryAgent
from agents.commit_formatter import CommitFormatterAgent


class CommitMessageGenerator:
    """Main orchestrator for the multi-agent commit message generation system."""
    
    def __init__(self, llm_provider: str = "ollama"):
        """
        Initialize the commit message generator with specified LLM provider.
        
        Args:
            llm_provider (str): The LLM provider to use (ollama, openai, etc.)
        """
        self.llm_provider = llm_provider
        self.diff_analyzer = DiffAnalyzerAgent(llm_provider)
        self.summary_agent = SummaryAgent(llm_provider)
        self.formatter_agent = CommitFormatterAgent(llm_provider)
        
    def get_git_diff(self, commit_range: str = "HEAD~1 HEAD") -> str:
        """
        Get git diff for the specified commit range.
        
        Args:
            commit_range (str): Git commit range (default: "HEAD~1 HEAD")
            
        Returns:
            str: The git diff content
        """
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
        """
        Get git diff for staged changes.
        
        Returns:
            str: The staged diff content
        """
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
                              use_staged: bool = False) -> str:
        """
        Generate a conventional commit message using the multi-agent system.
        
        Args:
            git_diff (str, optional): Custom git diff content
            use_staged (bool): Whether to use staged changes instead of last commit
            
        Returns:
            str: The generated commit message
        """
        # Get git diff if not provided
        if git_diff is None:
            if use_staged:
                git_diff = self.get_staged_diff()
            else:
                git_diff = self.get_git_diff()
        
        if not git_diff.strip():
            return "No changes detected or git diff is empty."
        
        print("🔍 Analyzing git diff with multi-agent system...")
        print(f"📊 Using LLM Provider: {self.llm_provider}")
        print(f"📝 Diff length: {len(git_diff)} characters")
        
        # Create tasks for each agent
        analysis_task = Task(
            agent=self.diff_analyzer.agent,
            description=self.diff_analyzer.analyze_diff(git_diff)["task_description"],
            expected_output=self.diff_analyzer.analyze_diff(git_diff)["expected_output"]
        )
        
        summary_task = Task(
            agent=self.summary_agent.agent,
            description=self.summary_agent.create_summary(git_diff)["task_description"],
            expected_output=self.summary_agent.create_summary(git_diff)["expected_output"]
        )
        
        format_task = Task(
            agent=self.formatter_agent.agent,
            description=self.formatter_agent.format_commit_message(
                change_type="[from analysis]",
                summary="[from summary]",
                scope="[from analysis]"
            )["task_description"],
            expected_output=self.formatter_agent.format_commit_message(
                change_type="[from analysis]",
                summary="[from summary]",
                scope="[from analysis]"
            )["expected_output"]
        )
        
        # Create and run the crew
        crew = Crew(
            agents=[
                self.diff_analyzer.agent,
                self.summary_agent.agent,
                self.formatter_agent.agent
            ],
            tasks=[analysis_task, summary_task, format_task],
            verbose=True,
            llm_provider=self.llm_provider
        )
        
        try:
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            print(f"Error running multi-agent system: {e}")
            return f"Error: {e}"


def main():
    """Main entry point for the commit message generator."""
    # Load environment variables
    load_dotenv()
    
    # Get LLM provider from environment or use default
    llm_provider = os.getenv("CREWAI_LLM_PROVIDER", "ollama")
    
    # Initialize the generator
    generator = CommitMessageGenerator(llm_provider)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--staged":
            print("📋 Using staged changes...")
            commit_message = generator.generate_commit_message(use_staged=True)
        elif sys.argv[1] == "--help":
            print("Git Commit Message Generator")
            print("Usage:")
            print("  python commit_generator.py           # Use last commit")
            print("  python commit_generator.py --staged   # Use staged changes")
            print("  python commit_generator.py --help     # Show this help")
            return
        else:
            # Custom commit range
            commit_message = generator.generate_commit_message(
                git_diff=generator.get_git_diff(sys.argv[1])
            )
    else:
        # Default: use last commit
        commit_message = generator.generate_commit_message()
    
    # Output the result
    print("\n" + "="*60)
    print("🎯 GENERATED COMMIT MESSAGE:")
    print("="*60)
    print(commit_message)
    print("="*60)
    
    # Offer to copy to clipboard (macOS)
    try:
        import pyperclip
        pyperclip.copy(commit_message)
        print("\n📋 Commit message copied to clipboard!")
    except ImportError:
        print("\n💡 Tip: Install pyperclip to auto-copy to clipboard")


if __name__ == "__main__":
    main()
