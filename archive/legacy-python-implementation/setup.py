"""Setup configuration for Claude Code Agents (Legacy Python Implementation)

NOTE: For Claude Code Pro users, this setup.py is NOT required.
The agents work directly within Claude Code without any installation.

This file is only needed if you want to use the legacy Python API implementations.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-code-agents",
    version="2.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="24 specialized AI agents for Claude Code Pro - Legacy Python reference implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/claude-code-agents",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Commented out - not needed for Claude Code Pro usage
        # "anthropic>=0.40.0",
        # "python-dotenv>=1.0.0",
        # "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            # "pytest>=7.4.0",
            # "pytest-asyncio>=0.21.0",
        ],
    },
)
