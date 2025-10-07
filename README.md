# Git Commit Message Generator - Multi-Agent System

A sophisticated multi-agent system that automatically generates conventional commit messages from git diffs using specialized AI agents for analysis, summarization, and formatting.

## Problem Statement

Writing consistent, descriptive commit messages is crucial for maintaining clean git history and enabling automated tools like changelog generation and semantic versioning. However, developers often struggle to write conventional commit messages that follow standards, especially when dealing with complex changes or time pressure. This system automates the process by using specialized AI agents to analyze code changes and generate properly formatted commit messages.

## Tech Stack

### Programming Language
- **Python 3.11+** - Core implementation language

### Frameworks & Libraries
- **CrewAI** - Multi-agent orchestration framework
- **LangChain** - LLM integration and agent capabilities
- **python-dotenv** - Environment variable management

### LLM
- **Ollama** (default) - Local LLM for privacy and cost-effectiveness
- **OpenAI GPT-4** (optional) - Cloud-based LLM for enhanced capabilities

## Multi-Agent System Design

### The Crew (Agents)

#### 1. Diff Analysis Agent
- **Role**: Diff Analysis Expert
- **Goal**: Analyze git diffs to identify the primary purpose and type of change
- **Backstory**: An expert software engineer with deep experience in code review and version control. Excels at reading git diffs and identifying the nature of changes - whether they are new features, bug fixes, refactoring, documentation updates, or other types of changes. Understands conventional commit standards and can accurately classify changes into appropriate categories.

#### 2. Summary Agent
- **Role**: Technical Writer & Code Summarizer
- **Goal**: Create clear, concise, and human-readable summaries of code changes
- **Backstory**: An experienced technical writer and software engineer who excels at translating complex code changes into clear, understandable summaries. Has a talent for identifying the most important aspects of code changes and explaining them in a way that both technical and non-technical stakeholders can understand. Focuses on business impact and user-facing changes while maintaining technical accuracy.

#### 3. Commit Formatter Agent
- **Role**: Conventional Commit Specialist
- **Goal**: Format commit messages according to Conventional Commits specification
- **Backstory**: An expert in software development best practices and conventional commit standards. Has extensive experience with semantic versioning, automated changelog generation, and maintaining clean git history. Understands the importance of consistent, machine-readable commit messages for automated tools and team collaboration.

### The Process (Tasks & Workflow)

The system follows a sequential workflow where each agent builds upon the previous agent's output:

1. **Diff Analysis Task**: The Diff Analysis Agent examines the git diff and classifies the change type (feat, fix, refactor, docs, style, test, chore, perf, ci, build) and identifies the scope.

2. **Summary Task**: The Summary Agent creates a human-readable summary of the changes, focusing on functionality, affected components, and business impact.

3. **Formatting Task**: The Commit Formatter Agent assembles the final commit message following the Conventional Commits specification, incorporating the analysis and summary from previous agents.

### The Outcome

The system generates conventional commit messages in the format:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Examples:
- `feat(auth): add OAuth2 login support`
- `fix(api): resolve user validation error`
- `refactor(database): optimize query performance`
- `feat!: redesign user interface (BREAKING CHANGE: UI components have new props)`

### Why a Multi-Agent System?

This problem is perfectly suited for a multi-agent approach due to several key factors:

1. **Specialization**: Each agent has a specific expertise - diff analysis, technical writing, and commit formatting. This specialization allows for more accurate and focused processing of each aspect of the task.

2. **Modularity**: The system can be easily extended with additional agents (e.g., security analysis, performance impact assessment) or modified to handle different commit standards.

3. **Fault Tolerance**: If one agent fails or produces suboptimal output, the other agents can still contribute their specialized knowledge, providing a more robust system.

4. **Quality Assurance**: Multiple agents provide different perspectives on the same change, leading to more comprehensive and accurate commit messages.

5. **Maintainability**: Each agent can be updated or replaced independently without affecting the entire system.

6. **Scalability**: The system can be extended to handle more complex scenarios like multi-file changes, cross-repository dependencies, or integration with CI/CD pipelines.

## How to Run

### Requirements

- Python 3.11 or higher
- Git repository with changes to analyze
- Ollama installed and running (for local LLM) OR OpenAI API key (for cloud LLM)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AI-Apps
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Install and configure Ollama (for local LLM)**:
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model (e.g., llama3.1)
   ollama pull llama3.1
   ```

### Execution

#### Basic Usage
```bash
# Run the working demonstration (recommended)
python demo_commit_generator.py

# Run the simple version (no LLM required)
python simple_commit_generator.py

# Generate commit message for last commit (requires LLM setup)
python commit_generator.py

# Generate commit message for staged changes
python commit_generator.py --staged

# Generate commit message for specific commit range
python commit_generator.py HEAD~2 HEAD

# Show help
python commit_generator.py --help
```

#### Advanced Usage

**Using OpenAI instead of Ollama**:
```bash
# Set environment variable
export CREWAI_LLM_PROVIDER=openai
export OPENAI_API_KEY=your_api_key_here

# Run the generator
python commit_generator.py
```

**Custom git diff**:
```python
from commit_generator import CommitMessageGenerator

generator = CommitMessageGenerator()
custom_diff = """
diff --git a/src/auth.py b/src/auth.py
index 1234567..abcdefg 100644
--- a/src/auth.py
+++ b/src/auth.py
@@ -10,6 +10,8 @@ def login(username, password):
     if validate_credentials(username, password):
         return create_session(username)
+    else:
+        log_failed_attempt(username)
     return None
"""

commit_message = generator.generate_commit_message(custom_diff)
print(commit_message)
```

### Example Output

```
🔍 Analyzing git diff with multi-agent system...
📊 Using LLM Provider: ollama
📝 Diff length: 1247 characters

============================================================
🎯 GENERATED COMMIT MESSAGE:
============================================================
feat(auth): add failed login attempt logging

Add logging functionality to track failed authentication attempts
for security monitoring and audit purposes.

============================================================
📋 Commit message copied to clipboard!
```

## Features

- **Conventional Commits Compliance**: Generates messages that follow the Conventional Commits specification
- **Multi-Agent Architecture**: Specialized agents for analysis, summarization, and formatting
- **Flexible Input**: Works with staged changes, specific commits, or custom diffs
- **Multiple LLM Support**: Compatible with Ollama (local) and OpenAI (cloud)
- **Error Handling**: Robust error handling for git operations and agent failures
- **Extensible Design**: Easy to add new agents or modify existing ones

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with various git diffs
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
