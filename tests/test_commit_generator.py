"""
Comprehensive test suite for Git Commit Message Generator
Tests multi-agent system functionality
"""

import unittest
import tempfile
import os
import subprocess
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commit_generator import (
    DiffAnalyzer, CommitFormatter, GitService, 
    CommitMessageGenerator, ChangeType, Scope
)


class TestDiffAnalyzer(unittest.TestCase):
    """Test the DiffAnalyzer agent."""
    
    def setUp(self):
        self.analyzer = DiffAnalyzer()
    
    def test_extract_files_single_file(self):
        """Test extracting single file from diff."""
        git_diff = """diff --git a/src/main.py b/src/main.py
index 1234567..abcdefg 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,3 +1,4 @@
 def hello():
+    print("Hello World")
     return "Hello"
"""
        files = self.analyzer._extract_files(git_diff)
        self.assertEqual(files, ["src/main.py"])
    
    def test_extract_files_multiple_files(self):
        """Test extracting multiple files from diff."""
        git_diff = """diff --git a/src/main.py b/src/main.py
index 1234567..abcdefg 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,3 +1,4 @@
 def hello():
+    print("Hello World")
     return "Hello"

diff --git a/tests/test_main.py b/tests/test_main.py
new file mode 100644
index 0000000..1234567
--- /dev/null
+++ b/tests/test_main.py
@@ -0,0 +1,5 @@
+def test_hello():
+    assert hello() == "Hello"
+    return True
"""
        files = self.analyzer._extract_files(git_diff)
        self.assertEqual(len(files), 2)
        self.assertIn("src/main.py", files)
        self.assertIn("tests/test_main.py", files)
    
    def test_analyze_python_files(self):
        """Test analysis of Python files."""
        git_diff = """diff --git a/src/main.py b/src/main.py
index 1234567..abcdefg 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,3 +1,4 @@
 def hello():
+    print("Hello World")
     return "Hello"
"""
        result = self.analyzer.analyze(git_diff)
        self.assertEqual(result["change_type"], ChangeType.FEAT.value)
        self.assertEqual(result["scope"], Scope.CODE.value)
        self.assertEqual(result["confidence"], "high")
    
    def test_analyze_markdown_files(self):
        """Test analysis of markdown files."""
        git_diff = """diff --git a/README.md b/README.md
index 1234567..abcdefg 100644
--- a/README.md
+++ b/README.md
@@ -1,3 +1,4 @@
 # Project
+## New Section
 This is a test project.
"""
        result = self.analyzer.analyze(git_diff)
        self.assertEqual(result["change_type"], ChangeType.DOCS.value)
        self.assertEqual(result["scope"], Scope.MARKDOWN.value)
        self.assertEqual(result["confidence"], "high")


class TestCommitFormatter(unittest.TestCase):
    """Test the CommitFormatter agent."""
    
    def setUp(self):
        self.formatter = CommitFormatter()
    
    def test_format_feat_auth(self):
        """Test formatting feature with auth scope."""
        result = self.formatter.format(ChangeType.FEAT.value, Scope.AUTH.value)
        self.assertEqual(result, "feat(auth): add authentication features")
    
    def test_format_fix_validation(self):
        """Test formatting fix with validation scope."""
        result = self.formatter.format(ChangeType.FIX.value, Scope.VALIDATION.value)
        self.assertEqual(result, "fix(validation): fix validation issues")
    
    def test_format_docs_readme(self):
        """Test formatting docs with readme scope."""
        result = self.formatter.format(ChangeType.DOCS.value, Scope.README.value)
        self.assertEqual(result, "docs(readme): update README")
    
    def test_format_chore_maintenance(self):
        """Test formatting chore with maintenance scope."""
        result = self.formatter.format(ChangeType.CHORE.value, Scope.MAINTENANCE.value)
        self.assertEqual(result, "chore: maintain codebase")


class TestGitService(unittest.TestCase):
    """Test the GitService class."""
    
    def setUp(self):
        self.git_service = GitService()
    
    @patch('subprocess.run')
    def test_get_staged_diff_success(self, mock_run):
        """Test successful staged diff retrieval."""
        mock_run.return_value = MagicMock(stdout="diff content", returncode=0)
        result = self.git_service.get_staged_diff()
        self.assertEqual(result, "diff content")
        mock_run.assert_called_once_with(
            ["git", "diff", "--cached"],
            capture_output=True, text=True, check=True
        )
    
    @patch('subprocess.run')
    def test_get_staged_diff_failure(self, mock_run):
        """Test staged diff retrieval failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")
        result = self.git_service.get_staged_diff()
        self.assertEqual(result, "")


class TestCommitMessageGenerator(unittest.TestCase):
    """Test the main CommitMessageGenerator orchestrator."""
    
    def setUp(self):
        self.generator = CommitMessageGenerator()
    
    def test_generate_empty_diff(self):
        """Test generation with empty diff."""
        result = self.generator.generate("")
        self.assertEqual(result, "No changes detected.")
    
    def test_generate_whitespace_diff(self):
        """Test generation with whitespace-only diff."""
        result = self.generator.generate("   \n  \t  ")
        self.assertEqual(result, "No changes detected.")
    
    def test_generate_python_changes(self):
        """Test generation for Python file changes."""
        git_diff = """diff --git a/src/main.py b/src/main.py
index 1234567..abcdefg 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,3 +1,4 @@
 def hello():
+    print("Hello World")
     return "Hello"
"""
        result = self.generator.generate(git_diff)
        self.assertEqual(result, "feat(code): add new functionality")
    
    def test_generate_markdown_changes(self):
        """Test generation for markdown file changes."""
        git_diff = """diff --git a/README.md b/README.md
index 1234567..abcdefg 100644
--- a/README.md
+++ b/README.md
@@ -1,3 +1,4 @@
 # Project
+## New Section
 This is a test project.
"""
        result = self.generator.generate(git_diff)
        self.assertEqual(result, "docs(markdown): update markdown documentation")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete multi-agent system."""
    
    def test_end_to_end_python_changes(self):
        """Test complete flow for Python file changes."""
        git_diff = """diff --git a/src/main.py b/src/main.py
index 1234567..abcdefg 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,3 +1,4 @@
 def hello():
+    print("Hello World")
     return "Hello"
"""
        generator = CommitMessageGenerator()
        result = generator.generate(git_diff)
        self.assertEqual(result, "feat(code): add new functionality")
    
    def test_end_to_end_markdown_changes(self):
        """Test complete flow for markdown file changes."""
        git_diff = """diff --git a/README.md b/README.md
index 1234567..abcdefg 100644
--- a/README.md
+++ b/README.md
@@ -1,3 +1,4 @@
 # Project
+## New Section
 This is a test project.
"""
        generator = CommitMessageGenerator()
        result = generator.generate(git_diff)
        self.assertEqual(result, "docs(markdown): update markdown documentation")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_empty_git_diff(self):
        """Test handling of empty git diff."""
        generator = CommitMessageGenerator()
        result = generator.generate("")
        self.assertEqual(result, "No changes detected.")
    
    def test_malformed_git_diff(self):
        """Test handling of malformed git diff."""
        generator = CommitMessageGenerator()
        result = generator.generate("not a git diff")
        # Should still work with fallback
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_very_large_git_diff(self):
        """Test handling of very large git diff."""
        large_diff = "diff --git a/large_file.py b/large_file.py\n" + "+\n" * 10000
        generator = CommitMessageGenerator()
        result = generator.generate(large_diff)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
