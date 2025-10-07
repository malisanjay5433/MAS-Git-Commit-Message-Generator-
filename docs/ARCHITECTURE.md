# Multi-Agent System Architecture

## Overview

The Git Commit Message Generator uses a sophisticated multi-agent system architecture to analyze git changes and generate conventional commit messages. The system is built using CrewAI framework and follows SOLID principles.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Multi-Agent System                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │ Diff        │    │ Summary     │    │ Commit      │    │
│  │ Analysis    │───▶│ Agent       │───▶│ Formatter   │    │
│  │ Agent       │    │             │    │ Agent       │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │ File        │    │ Change      │    │ Conventional│    │
│  │ Extraction  │    │ Summary     │    │ Commit      │    │
│  │ & Analysis  │    │ Generation  │    │ Formatting  │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Agent Responsibilities

### 1. Diff Analysis Agent
- **Primary Role**: Analyze git diffs and identify change patterns
- **Responsibilities**:
  - Extract file names from git diff
  - Analyze file types and extensions
  - Identify change patterns (new functions, bug fixes, etc.)
  - Classify change type (feat, fix, docs, etc.)
  - Determine scope (auth, api, ui, etc.)
  - Provide confidence level

### 2. Summary Agent
- **Primary Role**: Generate human-readable summaries
- **Responsibilities**:
  - Create concise summaries of changes
  - Focus on key functionality
  - Ensure clarity and readability
  - Maintain consistent tone

### 3. Commit Formatter Agent
- **Primary Role**: Format messages according to conventional commit standards
- **Responsibilities**:
  - Apply conventional commit formatting
  - Validate message structure
  - Ensure proper length and format
  - Handle edge cases and fallbacks

## Data Flow

1. **Input**: Git diff string
2. **Diff Analysis**: Extract files, analyze patterns, classify changes
3. **Summary Generation**: Create human-readable summary
4. **Commit Formatting**: Apply conventional commit formatting
5. **Output**: Formatted commit message

## Error Handling

- **Fallback Mechanisms**: Rule-based fallbacks when LLM fails
- **Graceful Degradation**: System continues with reduced functionality
- **Error Recovery**: Automatic retry with different strategies
- **Logging**: Comprehensive error logging for debugging

## Performance Optimization

- **Caching**: LLM response caching for similar diffs
- **Parallel Processing**: Concurrent agent execution where possible
- **Resource Management**: Efficient memory and CPU usage
- **Timeout Handling**: Configurable timeouts for LLM calls

## Security Considerations

- **Input Validation**: Sanitize git diff input
- **Output Validation**: Validate generated commit messages
- **Access Control**: Secure LLM API access
- **Data Privacy**: Local processing with Ollama option
