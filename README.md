# Git Commit Message Generator

🤖 **AI-powered commit message generator** that automatically creates conventional commit messages from your git changes.

## ✨ What It Does

Takes your git changes and generates proper commit messages like:
- `feat(auth): add user authentication`
- `fix(api): resolve validation error`
- `docs: update API documentation`
- `refactor: improve code structure`

## 🚀 Quick Start

### One Command Setup
```bash
./commit.sh
```

That's it! Your commit message is generated and copied to clipboard.

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AI-Apps
   ```

2. **Setup environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Install Ollama (for AI)**
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama pull llama3
   ollama serve
   ```

## 🎯 Usage

### Basic Usage
```bash
# Generate commit message for staged changes
./commit.sh

# Or directly
python commit_generator.py --staged --copy
```

### Advanced Usage
```bash
# Analyze last commit
python fast_commit_generator.py

# Analyze specific commit range
python fast_commit_generator.py HEAD~2 HEAD

# Show detailed analysis
python commit_generator.py --staged --verbose
```

## 🛠️ Available Commands

| Command | Description | Speed |
|---------|-------------|-------|
| `./commit.sh` | **Recommended** - Clean SOLID code | ~0.5 seconds |
| `python commit_generator.py --staged --copy` | Direct usage (clean) | ~0.5 seconds |
| `python commit_generator_vanilla.py --staged` | Vanilla multi-agent | ~2-3 seconds |
| `python main.py --staged` | Simple interface | ~2-3 seconds |

## 📁 **File Versions**

| File | Purpose | Code Quality | Best For |
|------|---------|--------------|----------|
| `commit_generator.py` | **Main version** - Clean SOLID code | ⭐⭐⭐⭐⭐ | **Production use** |
| `commit_generator_vanilla.py` | **Vanilla version** - Original multi-agent | ⭐⭐⭐ | Learning, comparison |
| `main.py` | **Simple interface** - Easy to use | ⭐⭐⭐ | Quick testing |

## 📋 Commit Types Generated

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New features | `feat(auth): add login functionality` |
| `fix` | Bug fixes | `fix(api): resolve validation error` |
| `docs` | Documentation | `docs: update README` |
| `style` | Code formatting | `style: fix indentation` |
| `refactor` | Code restructuring | `refactor: optimize database queries` |
| `test` | Tests | `test: add unit tests for auth` |
| `chore` | Maintenance | `chore: update dependencies` |
| `build` | Build system | `build: update webpack config` |
| `ci` | CI/CD | `ci: add GitHub Actions workflow` |

## 👥 Team Setup

### For Your Team
```bash
# Run the deployment script
./deploy.sh
```

This will:
- ✅ Set up virtual environment
- ✅ Install all dependencies
- ✅ Configure git aliases
- ✅ Test the system

### Create Team Alias
Add to your `~/.zshrc` or `~/.bashrc`:
```bash
alias commit-msg="cd /path/to/AI-Apps && source venv/bin/activate && python commit_generator.py --staged --copy"
```

Then use: `commit-msg`

## 🌍 Deployment to Existing Projects

### 🏆 **Recommended: Global Installation**

**Best for most users** - Install once, use everywhere:

```bash
# 1. Install globally (one-time setup)
git clone <this-repo-url> ~/.commit-generator
cd ~/.commit-generator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3

# 2. Add global alias
echo 'alias commit-msg="cd ~/.commit-generator && source venv/bin/activate && python commit_generator.py --staged --copy"' >> ~/.zshrc
source ~/.zshrc

# 3. Use in ANY project
cd /path/to/any/project
git add .
commit-msg  # 🎉 Done!
```

### 📦 **Alternative: Project-Specific Installation**

For individual projects:

```bash
# In your existing project
git clone <this-repo-url> commit-generator
cd commit-generator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3

# Create project script
cat > ../generate-commit.sh << 'EOF'
#!/bin/bash
cd commit-generator
source venv/bin/activate
python commit_generator.py --staged --copy
EOF

chmod +x ../generate-commit.sh

# Use it
cd ..
git add .
./generate-commit.sh
```

### 🐳 **Docker Deployment**

For containerized environments:

```bash
# Build Docker image
docker build -t commit-generator .

# Use in any project
docker run -v $(pwd):/workspace -w /workspace commit-generator
```

### 📊 **Deployment Comparison**

| Method | Setup Time | Usage | Best For |
|--------|------------|-------|----------|
| **Global** | ⭐⭐⭐ One-time | `commit-msg` | **Most users** |
| Project-specific | ⭐⭐ Per project | `./script.sh` | Single projects |
| Docker | ⭐⭐⭐ One-time | `docker run` | DevOps teams |

### 🚀 **Quick Global Setup**

```bash
# One-command installation
git clone <this-repo-url> ~/.commit-generator && \
cd ~/.commit-generator && \
python -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
ollama pull llama3 && \
echo 'alias commit-msg="cd ~/.commit-generator && source venv/bin/activate && python commit_generator.py --staged --copy"' >> ~/.zshrc && \
echo "✅ Ready! Use 'commit-msg' in any git project."
```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Git not found" | Install git |
| "No changes detected" | Run `git add .` first |
| "LLM errors" | Check if Ollama is running: `ollama serve` |
| "Permission denied" | Run `chmod +x *.py` |

## 📁 Project Structure

```
AI-Apps/
├── fast_commit_generator.py    # ⚡ Fast AI-powered generator
├── production_commit_generator.py  # 🔬 Full multi-agent system
├── main.py                     # 🎯 Simple interface
├── commit.sh                   # 🚀 One-command script
├── deploy.sh                   # 👥 Team setup script
├── requirements.txt            # 📦 Dependencies
└── README.md                   # 📖 This file
```

## 🎨 Example Output

```
⚡ Fast Git Commit Message Generator with LLM
==================================================
📋 Analyzing staged changes...

==================================================
🎯 GENERATED COMMIT MESSAGE:
==================================================
feat(auth): add user authentication
==================================================

📋 Commit message copied to clipboard!
```

## 🏗️ How It Works

1. **Analyzes** your git changes
2. **Classifies** the type of change (feat, fix, docs, etc.)
3. **Generates** a proper conventional commit message
4. **Copies** to clipboard for easy pasting

## 🚀 Features

- ✅ **AI-powered** - Uses LLM for intelligent analysis
- ✅ **Fast** - 2-3 seconds processing time
- ✅ **Clean output** - No verbose logs
- ✅ **Auto-copy** - Ready to paste
- ✅ **Team ready** - Easy deployment
- ✅ **Conventional commits** - Follows standards
- ✅ **Multiple options** - Fast or detailed analysis

## 📄 License

MIT License - Free to use and modify.

---

**Ready to use?** Just run `./commit.sh` and start generating better commit messages! 🎉# Test comment
