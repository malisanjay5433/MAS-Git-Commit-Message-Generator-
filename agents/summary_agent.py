"""
Summary Agent for Git Commit Message Generator

This agent creates human-readable summaries of code changes from git diffs.
"""

from crewai import Agent
from typing import Dict, Any


class SummaryAgent:
    """Agent responsible for creating clear, human-readable summaries of changes."""
    
    def __init__(self, llm_provider: str = "ollama"):
        from crewai import LLM
        from langchain_ollama import ChatOllama
        
        # Configure LLM
        if llm_provider == "ollama":
            llm = ChatOllama(model="llama3:latest", base_url="http://localhost:11434")
        else:
            llm = None  # Will use default
        
        self.agent = Agent(
            role="Technical Writer & Code Summarizer",
            goal="Create clear, concise, and human-readable summaries of code changes",
            backstory="""You are an experienced technical writer and software engineer 
            who excels at translating complex code changes into clear, understandable 
            summaries. You have a talent for identifying the most important aspects 
            of code changes and explaining them in a way that both technical and 
            non-technical stakeholders can understand. You focus on the business 
            impact and user-facing changes while maintaining technical accuracy.""",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    
    def create_summary(self, git_diff: str, change_type: str = None, scope: str = None) -> Dict[str, Any]:
        """
        Create a human-readable summary of the git diff.
        
        Args:
            git_diff (str): The git diff content
            change_type (str): The identified change type from diff analyzer
            scope (str): The identified scope from diff analyzer
            
        Returns:
            Dict containing task description and expected output
        """
        context = ""
        if change_type:
            context += f"Change Type: {change_type}\n"
        if scope:
            context += f"Scope: {scope}\n"
        
        task_description = f"""
        Create a clear, concise summary of the following code changes:
        
        {context}
        
        Git Diff:
        {git_diff}
        
        Focus on:
        1. What functionality was added, changed, or removed
        2. Key files or components affected
        3. Business impact or user-facing changes
        4. Any breaking changes or important notes
        
        Write the summary in present tense, active voice, and keep it under 50 words.
        Make it suitable for both technical and non-technical team members.
        """
        
        return {
            "task_description": task_description,
            "expected_output": "A clear, concise summary of the code changes in human-readable format"
        }
