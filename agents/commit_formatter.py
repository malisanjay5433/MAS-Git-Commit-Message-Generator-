"""
Commit Formatter Agent for Git Commit Message Generator

This agent formats the final commit message according to conventional commit standards.
"""

from crewai import Agent
from typing import Dict, Any


class CommitFormatterAgent:
    """Agent responsible for formatting commit messages according to conventional commit standards."""
    
    def __init__(self, llm_provider: str = "ollama"):
        from crewai import LLM
        from langchain_ollama import ChatOllama
        
        # Configure LLM
        if llm_provider == "ollama":
            llm = ChatOllama(model="llama3:latest", base_url="http://localhost:11434")
        else:
            llm = None  # Will use default
        
        self.agent = Agent(
            role="Conventional Commit Specialist",
            goal="Format commit messages according to Conventional Commits specification",
            backstory="""You are an expert in software development best practices and 
            conventional commit standards. You have extensive experience with 
            semantic versioning, automated changelog generation, and maintaining 
            clean git history. You understand the importance of consistent, 
            machine-readable commit messages for automated tools and team 
            collaboration. You ensure all commit messages follow the 
            Conventional Commits specification (https://conventionalcommits.org/).""",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    
    def format_commit_message(self, change_type: str, summary: str, scope: str = None, 
                            is_breaking: bool = False, body: str = None) -> Dict[str, Any]:
        """
        Format the final commit message according to conventional commit standards.
        
        Args:
            change_type (str): The type of change (feat, fix, refactor, etc.)
            summary (str): The human-readable summary
            scope (str): The scope of the change (optional)
            is_breaking (bool): Whether this is a breaking change
            body (str): Additional details (optional)
            
        Returns:
            Dict containing task description and expected output
        """
        task_description = f"""
        Format a conventional commit message with the following information:
        
        Change Type: {change_type}
        Summary: {summary}
        Scope: {scope or "none"}
        Breaking Change: {is_breaking}
        Additional Details: {body or "none"}
        
        Follow the Conventional Commits specification:
        - Format: <type>[optional scope]: <description>
        - Use lowercase for type and scope
        - Use imperative mood for description
        - Add "BREAKING CHANGE:" footer if applicable
        - Keep description under 50 characters
        - Add body if additional context is needed
        
        Examples:
        - feat(auth): add OAuth2 login support
        - fix(api): resolve user validation error
        - refactor(database): optimize query performance
        - feat!: redesign user interface (BREAKING CHANGE: UI components have new props)
        """
        
        return {
            "task_description": task_description,
            "expected_output": "A properly formatted conventional commit message"
        }
