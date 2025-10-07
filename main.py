"""
Main entry point for the Git Commit Message Generator

This is a simplified interface to the multi-agent system.
For full functionality, use commit_generator.py
"""

from commit_generator import CommitMessageGenerator
import os
from dotenv import load_dotenv

def main():
    """Simple interface to the commit message generator."""
    # Load environment variables
    load_dotenv()
    
    # Get LLM provider from environment
    llm_provider = os.getenv("CREWAI_LLM_PROVIDER", "ollama")
    
    # Initialize and run the generator
    generator = CommitMessageGenerator(llm_provider)
    commit_message = generator.generate_commit_message()
    
    print("\n✅ Final Commit Message:\n", commit_message)

if __name__ == "__main__":
    main()
