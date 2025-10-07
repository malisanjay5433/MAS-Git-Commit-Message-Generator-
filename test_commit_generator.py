"""
Test script for the Git Commit Message Generator

This script tests the multi-agent system with sample git diffs.
"""

from commit_generator import CommitMessageGenerator


def test_with_sample_diffs():
    """Test the commit generator with sample git diffs."""
    
    # Sample git diff for a new feature
    feature_diff = """
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
    
    # Sample git diff for a bug fix
    bugfix_diff = """
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
    
    # Sample git diff for refactoring
    refactor_diff = """
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
    
    print("🧪 Testing Git Commit Message Generator")
    print("=" * 50)
    
    # Initialize generator
    generator = CommitMessageGenerator()
    
    # Test cases
    test_cases = [
        ("New Feature", feature_diff),
        ("Bug Fix", bugfix_diff),
        ("Refactoring", refactor_diff)
    ]
    
    for test_name, diff in test_cases:
        print(f"\n📝 Testing: {test_name}")
        print("-" * 30)
        
        try:
            commit_message = generator.generate_commit_message(diff)
            print(f"Generated: {commit_message}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 30)


if __name__ == "__main__":
    test_with_sample_diffs()
