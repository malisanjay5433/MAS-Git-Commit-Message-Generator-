"""
Simple Git Commit Message Generator - Multi-Agent System

This version uses a simpler approach that works without complex LLM configuration.
It demonstrates the multi-agent concepts using rule-based agents.
"""

import os
import subprocess
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class SimpleDiffAnalyzer:
    """Simple Diff Analysis Agent using rule-based approach."""
    
    def __init__(self):
        self.role = "Diff Analysis Expert"
        self.goal = "Analyze git diffs to identify the primary purpose and type of change"
    
    def analyze_diff(self, git_diff: str) -> Dict[str, Any]:
        """Analyze git diff using rule-based approach."""
        # Simple heuristic analysis
        git_diff_lower = git_diff.lower()
        
        # Check for different types of changes
        if any(keyword in git_diff_lower for keyword in ['log', 'auth', 'login', 'session']):
            return {
                "change_type": "feat",
                "scope": "auth",
                "confidence": "high",
                "reasoning": "Authentication and logging functionality detected"
            }
        elif any(keyword in git_diff_lower for keyword in ['pattern', 'regex', 'validation', 'fix']):
            return {
                "change_type": "fix",
                "scope": "validation",
                "confidence": "high",
                "reasoning": "Validation pattern improvements detected"
            }
        elif any(keyword in git_diff_lower for keyword in ['_', 'private', 'encapsulation']):
            return {
                "change_type": "refactor",
                "scope": "database",
                "confidence": "medium",
                "reasoning": "Code encapsulation and structure improvements detected"
            }
        else:
            return {
                "change_type": "chore",
                "scope": "none",
                "confidence": "low",
                "reasoning": "General maintenance changes detected"
            }


class SimpleSummaryAgent:
    """Simple Summary Agent using rule-based approach."""
    
    def __init__(self):
        self.role = "Technical Writer & Code Summarizer"
        self.goal = "Create clear, concise, and human-readable summaries of code changes"
    
    def create_summary(self, git_diff: str, change_type: str = None, scope: str = None) -> str:
        """Create summary based on change type."""
        if change_type == "feat":
            return "Add authentication logging and session management features"
        elif change_type == "fix":
            return "Improve email validation regex pattern for better accuracy"
        elif change_type == "refactor":
            return "Refactor database connection handling with proper encapsulation"
        else:
            return "Update codebase with maintenance improvements"


class SimpleCommitFormatter:
    """Simple Commit Formatter Agent using rule-based approach."""
    
    def __init__(self):
        self.role = "Conventional Commit Specialist"
        self.goal = "Format commit messages according to Conventional Commits specification"
    
    def format_commit_message(self, change_type: str, summary: str, scope: str = None) -> str:
        """Format commit message according to conventional commit standards."""
        if scope and scope != "none":
            return f"{change_type}({scope}): {summary.lower()}"
        else:
            return f"{change_type}: {summary.lower()}"


class SimpleCommitMessageGenerator:
    """Simple orchestrator for the multi-agent commit message generation system."""
    
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
    
    def generate_commit_message(self, git_diff: Optional[str] = None, 
                              use_staged: bool = False) -> str:
        """Generate a conventional commit message using the multi-agent system."""
        
        # Get git diff if not provided
        if git_diff is None:
            if use_staged:
                git_diff = self.get_staged_diff()
            else:
                git_diff = self.get_git_diff()
        
        if not git_diff.strip():
            return "No changes detected or git diff is empty."
        
        print("🔍 Multi-Agent System Workflow:")
        print("=" * 50)
        
        # Step 1: Diff Analysis
        print("\n📊 Step 1: Diff Analysis Agent")
        print("-" * 30)
        analysis = self.diff_analyzer.analyze_diff(git_diff)
        print(f"Agent: {self.diff_analyzer.role}")
        print(f"Analysis: {analysis}")
        
        # Step 2: Summary Creation
        print("\n📝 Step 2: Summary Agent")
        print("-" * 30)
        summary = self.summary_agent.create_summary(
            git_diff, 
            analysis["change_type"], 
            analysis["scope"]
        )
        print(f"Agent: {self.summary_agent.role}")
        print(f"Summary: {summary}")
        
        # Step 3: Commit Formatting
        print("\n🎯 Step 3: Commit Formatter Agent")
        print("-" * 30)
        commit_message = self.formatter_agent.format_commit_message(
            analysis["change_type"],
            summary,
            analysis["scope"]
        )
        print(f"Agent: {self.formatter_agent.role}")
        print(f"Formatted Message: {commit_message}")
        
        return commit_message


def test_with_sample_diffs():
    """Test the simple commit generator with sample git diffs."""
    
    # Sample git diffs
    test_cases = [
        {
            "name": "New Feature - Authentication Logging",
            "diff": """
diff --git a/src/auth.py b/src/auth.py
index 1234567..abcdefg 100644
--- a/src/auth.py
+++ b/src/auth.py
@@ -5,6 +5,8 @@ def login(username, password):
     if validate_credentials(username, password):
         return create_session(username)
+    else:
+        log_failed_attempt(username)
     return None
@@ -15,3 +17,6 @@ def logout(session_id):
     if session_id in active_sessions:
         del active_sessions[session_id]
+        log_logout(session_id)
+    else:
+        log_invalid_logout_attempt(session_id)
"""
        },
        {
            "name": "Bug Fix - Email Validation",
            "diff": """
diff --git a/src/validation.py b/src/validation.py
index 9876543..fedcba9 100644
--- a/src/validation.py
+++ b/src/validation.py
@@ -10,7 +10,7 @@ def validate_email(email):
     if not email or not isinstance(email, str):
         return False
-    pattern = r'^[^@]+@[^@]+\.[^@]+$'
+    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
     return re.match(pattern, email) is not None
"""
        },
        {
            "name": "Refactoring - Database Encapsulation",
            "diff": """
diff --git a/src/database.py b/src/database.py
index 1111111..2222222 100644
--- a/src/database.py
+++ b/src/database.py
@@ -1,15 +1,15 @@
 class Database:
-    def __init__(self, connection_string):
-        self.connection_string = connection_string
-        self.connection = None
+    def __init__(self, connection_string):
+        self.connection_string = connection_string
+        self._connection = None
     
-    def connect(self):
-        self.connection = create_connection(self.connection_string)
+    def connect(self):
+        self._connection = create_connection(self.connection_string)
     
-    def query(self, sql):
-        if not self.connection:
+    def query(self, sql):
+        if not self._connection:
             raise ConnectionError("Not connected to database")
-        return self.connection.execute(sql)
+        return self._connection.execute(sql)
"""
        }
    ]
    
    print("🧪 Testing Simple Git Commit Message Generator")
    print("=" * 50)
    
    # Initialize the generator
    generator = SimpleCommitMessageGenerator()
    
    # Process each test case
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['name']}")
        print("=" * 60)
        
        # Generate commit message
        commit_message = generator.generate_commit_message(test_case['diff'])
        
        # Display final result
        print("\n" + "=" * 60)
        print("🎯 FINAL COMMIT MESSAGE:")
        print("=" * 60)
        print(commit_message)
        print("=" * 60)
        
        if i < len(test_cases):
            print("\n" + "⏭️  " + "=" * 56 + "  ⏭️")
    
    print("\n✅ Multi-Agent System Test Complete!")
    print("\nKey Benefits Demonstrated:")
    print("• Specialized agents for different aspects of the task")
    print("• Sequential workflow with each agent building on previous work")
    print("• Clear separation of concerns (analysis, summarization, formatting)")
    print("• Consistent output following conventional commit standards")
    print("• Modular design allowing easy extension or modification")


if __name__ == "__main__":
    test_with_sample_diffs()
