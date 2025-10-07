#!/usr/bin/env python3
"""
Quick Git Commit Message Generator
Fast, instant commit message generation without any delays.
"""

import subprocess
import argparse
import sys


def get_staged_diff():
    """Get git diff for staged changes."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""
    except FileNotFoundError:
        print("Git not found. Please ensure git is installed and you're in a git repository.")
        return ""


def get_last_commit_diff():
    """Get git diff for last commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def analyze_changes(diff_content):
    """Quickly analyze changes and determine commit type."""
    if not diff_content.strip():
        return "chore: no changes detected"
    
    diff_lower = diff_content.lower()
    
    # Extract file names
    files = []
    for line in diff_content.split('\n'):
        if line.startswith('diff --git'):
            parts = line.split()
            if len(parts) >= 4:
                file_a = parts[2].split('/')[-1]
                file_b = parts[3].split('/')[-1]
                if file_a != '/dev/null':
                    files.append(file_a)
                if file_b != '/dev/null' and file_b != file_a:
                    files.append(file_b)
    
    # Check for documentation changes
    has_md_files = any('.md' in f for f in files)
    has_doc_patterns = any(keyword in diff_lower for keyword in ['<!--', '-->', 'readme'])
    is_python_code = any('.py' in f for f in files) and any(keyword in diff_lower for keyword in ['def ', 'class ', 'import ', 'return '])
    
    if (has_md_files or has_doc_patterns) and not is_python_code:
        return "docs: update documentation"
    
    # Check for new features
    if any(keyword in diff_lower for keyword in ['def ', 'class ', 'import ', 'return ', 'if ', 'for ', 'while ']):
        if any(keyword in diff_lower for keyword in ['auth', 'login', 'session', 'token', 'jwt']):
            return "feat(auth): add authentication features"
        else:
            return "feat: add new functionality"
    
    # Check for bug fixes
    if any(keyword in diff_lower for keyword in ['fix', 'bug', 'error', 'validation', 'pattern', 'regex']):
        return "fix: resolve issues and bugs"
    
    # Check for refactoring
    if any(keyword in diff_lower for keyword in ['refactor', 'cleanup', 'private', 'encapsulation']):
        return "refactor: improve code structure"
    
    # Check for tests
    if any(keyword in diff_lower for keyword in ['test', 'spec', 'mock', 'stub']):
        return "test: add or update tests"
    
    # Check for style changes
    if any(keyword in diff_lower for keyword in ['style', 'format', 'lint', 'prettier']):
        return "style: improve code formatting"
    
    # Check for build changes
    if any(keyword in diff_lower for keyword in ['build', 'compile', 'package', 'dependencies']):
        return "build: update build configuration"
    
    # Check for CI changes
    if any(keyword in diff_lower for keyword in ['ci', 'pipeline', 'workflow', 'github', 'actions']):
        return "ci: update CI/CD pipeline"
    
    # Default to chore
    return "chore: maintain codebase"


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Quick Git Commit Message Generator")
    parser.add_argument("--staged", action="store_true", help="Use staged changes")
    parser.add_argument("--last", action="store_true", help="Use last commit")
    parser.add_argument("--copy", action="store_true", help="Copy to clipboard")
    
    args = parser.parse_args()
    
    print("⚡ Quick Git Commit Message Generator")
    print("=" * 40)
    
    # Get diff content
    if args.staged:
        print("📋 Analyzing staged changes...")
        diff_content = get_staged_diff()
    elif args.last:
        print("📊 Analyzing last commit...")
        diff_content = get_last_commit_diff()
    else:
        print("📊 Analyzing last commit...")
        diff_content = get_last_commit_diff()
    
    # Generate commit message
    commit_message = analyze_changes(diff_content)
    
    # Output result
    print("\n" + "="*40)
    print("🎯 GENERATED COMMIT MESSAGE:")
    print("="*40)
    print(commit_message)
    print("="*40)
    
    # Copy to clipboard if requested
    if args.copy:
        try:
            import pyperclip
            pyperclip.copy(commit_message)
            print("\n📋 Copied to clipboard!")
        except ImportError:
            print("\n💡 Install pyperclip for auto-copy: pip install pyperclip")
        except Exception as e:
            print(f"\n⚠️  Could not copy: {e}")
    else:
        print("\n💡 Use --copy to auto-copy to clipboard")


if __name__ == "__main__":
    main()
