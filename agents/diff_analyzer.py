"""
Diff Analysis Agent for Git Commit Message Generator

This agent analyzes git diffs to identify the type of change and categorize it
according to conventional commit standards.
"""

from crewai import Agent
from typing import Dict, Any


class DiffAnalyzerAgent:
    """Agent responsible for analyzing git diffs and identifying change types."""
    
    def __init__(self, llm_provider: str = "ollama"):
        from crewai import LLM
        from langchain_ollama import ChatOllama
        
        # Configure LLM
        if llm_provider == "ollama":
            llm = ChatOllama(model="llama3:latest", base_url="http://localhost:11434")
        else:
            llm = None  # Will use default
        
        self.agent = Agent(
            role="Diff Analysis Expert",
            goal="Analyze git diffs to identify the primary purpose and type of change",
            backstory="""You are an expert software engineer with deep experience in 
            code review and version control. You excel at reading git diffs and 
            identifying the nature of changes - whether they are new features, 
            bug fixes, refactoring, documentation updates, or other types of changes.
            You understand conventional commit standards and can accurately classify 
            changes into appropriate categories.""",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    
    def analyze_diff(self, git_diff: str) -> Dict[str, Any]:
        """
        Analyze a git diff and return structured information about the change.
        
        Args:
            git_diff (str): The git diff content to analyze
            
        Returns:
            Dict containing:
            - change_type: The conventional commit type (feat, fix, refactor, etc.)
            - scope: The scope of the change (optional)
            - confidence: Confidence level in the analysis
            - reasoning: Explanation of the analysis
        """
        task_description = f"""
        Analyze the following git diff and provide a structured analysis:
        
        {git_diff}
        
        Please provide:
        1. The primary type of change (feat, fix, refactor, docs, style, test, chore, perf, ci, build)
        2. The scope of the change (e.g., auth, api, ui, database, etc.)
        3. Your confidence level (high, medium, low)
        4. Brief reasoning for your classification
        
        Format your response as:
        Type: [type]
        Scope: [scope or "none"]
        Confidence: [confidence level]
        Reasoning: [brief explanation]
        """
        
        return {
            "task_description": task_description,
            "expected_output": "Structured analysis of the git diff with type, scope, confidence, and reasoning"
        }
