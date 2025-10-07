"""
Demo Git Commit Message Generator - Multi-Agent System

This demonstration shows how the multi-agent system works with mock responses
to illustrate the complete workflow and agent collaboration.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MockDiffAnalyzerAgent:
    """Mock Diff Analysis Agent for demonstration."""
    
    def __init__(self):
        self.role = "Diff Analysis Expert"
        self.goal = "Analyze git diffs to identify the primary purpose and type of change"
    
    def analyze_diff(self, git_diff: str) -> Dict[str, Any]:
        """Mock analysis of git diff."""
        # Simple heuristic analysis
        if "def " in git_diff and "+" in git_diff:
            if "fix" in git_diff.lower() or "bug" in git_diff.lower() or "pattern" in git_diff.lower():
                return {
                    "change_type": "fix",
                    "scope": "validation",
                    "confidence": "high",
                    "reasoning": "Code changes include bug fix patterns and validation improvements"
                }
            elif "log" in git_diff.lower() or "auth" in git_diff.lower():
                return {
                    "change_type": "feat",
                    "scope": "auth",
                    "confidence": "high", 
                    "reasoning": "New authentication features and logging functionality added"
                }
            else:
                return {
                    "change_type": "refactor",
                    "scope": "database",
                    "confidence": "medium",
                    "reasoning": "Code structure improvements and encapsulation changes"
                }
        return {
            "change_type": "chore",
            "scope": "none",
            "confidence": "low",
            "reasoning": "General maintenance changes detected"
        }


class MockSummaryAgent:
    """Mock Summary Agent for demonstration."""
    
    def __init__(self):
        self.role = "Technical Writer & Code Summarizer"
        self.goal = "Create clear, concise, and human-readable summaries of code changes"
    
    def create_summary(self, git_diff: str, change_type: str = None, scope: str = None) -> str:
        """Mock summary creation."""
        if change_type == "feat":
            return "Add authentication logging and session management features"
        elif change_type == "fix":
            return "Improve email validation regex pattern for better accuracy"
        elif change_type == "refactor":
            return "Refactor database connection handling with proper encapsulation"
        else:
            return "Update codebase with maintenance improvements"


class MockCommitFormatterAgent:
    """Mock Commit Formatter Agent for demonstration."""
    
    def __init__(self):
        self.role = "Conventional Commit Specialist"
        self.goal = "Format commit messages according to Conventional Commits specification"
    
    def format_commit_message(self, change_type: str, summary: str, scope: str = None) -> str:
        """Mock commit message formatting."""
        if scope and scope != "none":
            return f"{change_type}({scope}): {summary.lower()}"
        else:
            return f"{change_type}: {summary.lower()}"


class DemoCommitMessageGenerator:
    """Demo orchestrator for the multi-agent commit message generation system."""
    
    def __init__(self):
        self.diff_analyzer = MockDiffAnalyzerAgent()
        self.summary_agent = MockSummaryAgent()
        self.formatter_agent = MockCommitFormatterAgent()
    
    def generate_commit_message(self, git_diff: str) -> str:
        """Generate commit message using the multi-agent system."""
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


def demo_with_sample_diffs():
    """Demonstrate the multi-agent system with sample git diffs."""
    
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
    
    print("🚀 Git Commit Message Generator - Multi-Agent System Demo")
    print("=" * 60)
    print("This demonstration shows how specialized AI agents collaborate")
    print("to generate conventional commit messages from git diffs.")
    print("=" * 60)
    
    # Initialize the generator
    generator = DemoCommitMessageGenerator()
    
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
    
    print("\n✅ Multi-Agent System Demonstration Complete!")
    print("\nKey Benefits Demonstrated:")
    print("• Specialized agents for different aspects of the task")
    print("• Sequential workflow with each agent building on previous work")
    print("• Clear separation of concerns (analysis, summarization, formatting)")
    print("• Consistent output following conventional commit standards")
    print("• Modular design allowing easy extension or modification")


if __name__ == "__main__":
    demo_with_sample_diffs()
