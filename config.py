"""
Configuration file for Git Commit Message Generator - Multi-Agent System
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for the multi-agent system."""
    
    # CrewAI Configuration
    CREWAI_TRACING_ENABLED = os.getenv("CREWAI_TRACING_ENABLED", "false").lower() == "true"
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3")
    
    # OpenAI Configuration (fallback)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Git Configuration
    GIT_USER_NAME = os.getenv("GIT_USER_NAME", "Git Commit Generator")
    GIT_USER_EMAIL = os.getenv("GIT_USER_EMAIL", "commit-generator@example.com")
    
    # System Configuration
    VERBOSE = os.getenv("VERBOSE", "false").lower() == "true"
    AUTO_COPY = os.getenv("AUTO_COPY", "true").lower() == "true"
    MAX_COMMIT_LENGTH = int(os.getenv("MAX_COMMIT_LENGTH", "50"))
    
    # Agent Configuration
    AGENT_VERBOSE = False
    AGENT_ALLOW_DELEGATION = False
    
    # Fallback Configuration
    ENABLE_FALLBACK = True
    FALLBACK_TIMEOUT = 5  # seconds
    
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """Get LLM configuration based on provider."""
        if cls.LLM_PROVIDER == "ollama":
            return {
                "model": f"ollama/{cls.OLLAMA_MODEL}",
                "base_url": cls.OLLAMA_BASE_URL
            }
        elif cls.LLM_PROVIDER == "openai":
            return {
                "model": cls.OPENAI_MODEL,
                "api_key": cls.OPENAI_API_KEY
            }
        else:
            return {
                "model": f"ollama/{cls.OLLAMA_MODEL}",
                "base_url": cls.OLLAMA_BASE_URL
            }
    
    @classmethod
    def get_agent_config(cls) -> Dict[str, Any]:
        """Get agent configuration."""
        return {
            "verbose": cls.AGENT_VERBOSE,
            "allow_delegation": cls.AGENT_ALLOW_DELEGATION
        }
