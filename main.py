"""
Main entry point for the Git Commit Message Generator

This uses the working simple multi-agent system.
For demonstration, use demo_commit_generator.py
"""

from commit_generator import ProductionCommitMessageGenerator
import sys

def main():
    """Simple interface to the commit message generator."""
    print("🚀 Git Commit Message Generator - Multi-Agent System")
    print("=" * 60)
    
    # Initialize the production generator
    generator = ProductionCommitMessageGenerator()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--staged":
            print("📋 Using staged changes...")
            commit_message = generator.generate_commit_message(use_staged=True)
        elif sys.argv[1] == "--help":
            print("Git Commit Message Generator")
            print("Usage:")
            print("  python main.py           # Use last commit")
            print("  python main.py --staged  # Use staged changes")
            print("  python main.py --help    # Show this help")
            print("\nFor production usage, run:")
            print("  python commit_generator.py --staged --copy")
            return
        else:
            # Custom commit range
            commit_message = generator.generate_commit_message(
                git_diff=generator.get_git_diff(sys.argv[1])
            )
    else:
        # Default: use last commit
        commit_message = generator.generate_commit_message()
    
    # Output the result
    print("\n" + "="*60)
    print("🎯 GENERATED COMMIT MESSAGE:")
    print("="*60)
    print(commit_message)
    print("="*60)
    
    # Offer to copy to clipboard (macOS)
    try:
        import pyperclip
        pyperclip.copy(commit_message)
        print("\n📋 Commit message copied to clipboard!")
    except ImportError:
        print("\n💡 Tip: Install pyperclip to auto-copy to clipboard")

if __name__ == "__main__":
    main()
