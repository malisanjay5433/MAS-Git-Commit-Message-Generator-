# Multi-Agent Git Commit Message Generator
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make scripts executable
RUN chmod +x commit.sh deploy.sh

# Set environment variables
ENV CREWAI_TRACING_ENABLED=false
ENV LLM_PROVIDER=ollama
ENV OLLAMA_MODEL=llama3
ENV OLLAMA_BASE_URL=http://localhost:11434

# Expose port for Ollama
EXPOSE 11434

# Download Ollama model
RUN ollama pull llama3

# Default command
CMD ["python", "commit_generator.py", "--staged", "--copy"]
