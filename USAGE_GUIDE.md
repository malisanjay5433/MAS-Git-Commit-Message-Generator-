# Git Commit Message Generator - Usage Guide

## Quick Start

### Option 1: Simple Script
```bash
./commit.sh
```

### Option 2: Direct Command
```bash
python fast_commit_generator.py --staged --copy
```

### Option 3: Alias (Recommended)
Add to your `~/.zshrc`:
```bash
alias commit-msg="cd /Users/sanjaymali/Documents/AI-Apps && source venv/bin/activate && python fast_commit_generator.py --staged --copy"
```

Then use:
```bash
commit-msg
```

## Available Commands

### Fast Commit Generator (Recommended)
- **File**: `fast_commit_generator.py`
- **Features**: LLM-powered, fast, clean output
- **Usage**: `python fast_commit_generator.py --staged --copy`

### Simple Commit Generator (No LLM)
- **File**: `simple_commit_generator.py`
- **Features**: Rule-based, instant, no dependencies
- **Usage**: `python simple_commit_generator.py --staged`

### Production Commit Generator (Full LLM)
- **File**: `production_commit_generator.py`
- **Features**: Full multi-agent system, verbose output
- **Usage**: `python production_commit_generator.py --staged --verbose`

## Command Options

- `--staged`: Use staged changes (recommended)
- `--copy`: Copy result to clipboard
- `--verbose`: Show detailed workflow (production only)
- `HEAD~2 HEAD`: Custom commit range

## Examples

```bash
# Analyze staged changes and copy to clipboard
python fast_commit_generator.py --staged --copy

# Analyze last commit
python fast_commit_generator.py

# Analyze specific commit range
python fast_commit_generator.py HEAD~2 HEAD

# Use simple version (no LLM)
python simple_commit_generator.py --staged
```

## Generated Commit Types

- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation updates
- `style`: Code formatting
- `refactor`: Code restructuring
- `test`: Test additions/updates
- `chore`: Maintenance tasks
- `build`: Build system changes
- `ci`: CI/CD pipeline changes

## Performance

- **Fast Generator**: ~2-3 seconds with LLM
- **Simple Generator**: Instant (no LLM)
- **Production Generator**: ~10-15 seconds (full verbose output)

## Troubleshooting

1. **"Git not found"**: Install git
2. **"No changes detected"**: Stage your changes with `git add .`
3. **LLM errors**: Check if Ollama is running (`ollama serve`)
4. **Permission denied**: Run `chmod +x *.py`

## Team Deployment

For team deployment, use the `deploy.sh` script:
```bash
./deploy.sh
```

This will set up the environment for all team members.
