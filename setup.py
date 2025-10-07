"""
Setup script for Git Commit Message Generator - Multi-Agent System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="git-commit-generator",
    version="1.0.0",
    author="Sanjay Mali",
    author_email="malisanjay5433@gmail.com",
    description="Multi-agent system for generating conventional commit messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/malisanjay5433/MAS-Git-Commit-Message-Generator-",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)
