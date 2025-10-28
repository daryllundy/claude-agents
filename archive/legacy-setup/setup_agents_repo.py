#!/usr/bin/env python3
"""
Setup script to create a complete Claude Code Agents repository structure.

Usage:
    python setup_agents_repo.py [target_directory]

This will create a fully organized, reusable agents repository.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List


class AgentRepoSetup:
    def __init__(self, target_dir: str = "claude-code-agents"):
        self.target_dir = Path(target_dir)
        self.structure = self._define_structure()
        
    def _define_structure(self) -> Dict[str, List[str]]:
        """Define the complete repository structure"""
        return {
            "agents/infrastructure": [
                "docker_agent.py",
                "devops_agent.py",
                "observability_agent.py",
            ],
            "agents/development": [
                "database_agent.py",
                "api_design_agent.py",
                "frontend_agent.py",
                "mobile_agent.py",
                "game_dev_agent.py",
            ],
            "agents/quality": [
                "test_suite_agent.py",
                "security_agent.py",
                "code_review_agent.py",
                "refactoring_agent.py",
                "performance_agent.py",
            ],
            "agents/operations": [
                "migration_agent.py",
                "dependency_agent.py",
                "git_agent.py",
            ],
            "agents/productivity": [
                "scaffolding_agent.py",
                "documentation_agent.py",
                "debugging_agent.py",
            ],
            "agents/business": [
                "validation_agent.py",
                "architecture_agent.py",
                "localization_agent.py",
                "compliance_agent.py",
            ],
            "agents/specialized": [
                "data_science_agent.py",
            ],
            "orchestrator": [
                "agent_orchestrator.py",
            ],
            "utils": [
                "response_parser.py",
                "context_builder.py",
            ],
            "examples": [
                "basic_usage.py",
                "multi_agent_workflow.py",
                "custom_agent_example.py",
            ],
            "tests": [
                "test_docker_agent.py",
                "test_orchestrator.py",
            ],
            "config": [
                "agent_config.yaml",
            ],
            ".": [
                "README.md",
                "requirements.txt",
                ".env.example",
                ".gitignore",
                "setup.py",
                "LICENSE",
                "CONTRIBUTING.md",
            ]
        }
    
    def create_structure(self):
        """Create the complete directory structure"""
        print(f"Creating Claude Code Agents repository in: {self.target_dir}")
        print("=" * 60)
        
        # Create base directory
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # Create all directories and files
        for directory, files in self.structure.items():
            dir_path = self.target_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py for Python packages
            if directory.startswith("agents") or directory in ["orchestrator", "utils", "tests"]:
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    self._create_init_file(init_file, directory)
            
            # Create each file
            for filename in files:
                file_path = dir_path / filename
                if not file_path.exists():
                    self._create_file(file_path, filename, directory)
                    print(f"✓ Created: {file_path.relative_to(self.target_dir)}")
        
        print("\n" + "=" * 60)
        print("✅ Repository structure created successfully!")
        print(f"\nNext steps:")
        print(f"  1. cd {self.target_dir}")
        print(f"  2. cp .env.example .env")
        print(f"  3. Add your ANTHROPIC_API_KEY to .env")
        print(f"  4. pip install -r requirements.txt")
        print(f"  5. python examples/basic_usage.py")
    
    def _create_init_file(self, file_path: Path, directory: str):
        """Create appropriate __init__.py content"""
        content = '"""' + f'\n{directory.replace("/", " - ").title()} Module\n"""\n\n'
        
        if directory == "agents":
            content = self._get_agents_init()
        elif "agents/" in directory:
            content = self._get_subpackage_init(directory)
        elif directory == "orchestrator":
            content = '"""\nOrchestrator Module\n"""\n\nfrom .agent_orchestrator import AgentOrchestrator\n\n__all__ = ["AgentOrchestrator"]\n'
        
        file_path.write_text(content)
    
    def _get_agents_init(self) -> str:
        """Generate main agents/__init__.py"""
        return '''"""
Claude Code Agents Package

A comprehensive suite of specialized AI agents for software development.
"""

# Infrastructure
from .infrastructure.docker_agent import DockerAgent
from .infrastructure.devops_agent import DevOpsAgent
from .infrastructure.observability_agent import ObservabilityAgent

# Development
from .development.database_agent import DatabaseAgent
from .development.api_design_agent import APIDesignAgent
from .development.frontend_agent import FrontendAgent
from .development.mobile_agent import MobileAgent
from .development.game_dev_agent import GameDevelopmentAgent

# Quality
from .quality.test_suite_agent import TestSuiteAgent
from .quality.security_agent import SecurityAgent
from .quality.code_review_agent import CodeReviewAgent
from .quality.refactoring_agent import RefactoringAgent
from .quality.performance_agent import PerformanceAgent

# Operations
from .operations.migration_agent import MigrationAgent
from .operations.dependency_agent import DependencyAgent
from .operations.git_agent import GitAgent

# Productivity
from .productivity.scaffolding_agent import ScaffoldingAgent
from .productivity.documentation_agent import DocumentationAgent
from .productivity.debugging_agent import DebuggingAgent

# Business
from .business.validation_agent import ValidationAgent
from .business.architecture_agent import ArchitectureAgent
from .business.localization_agent import LocalizationAgent
from .business.compliance_agent import ComplianceAgent

# Specialized
from .specialized.data_science_agent import DataScienceAgent

__version__ = "0.1.0"

__all__ = [
    # Infrastructure
    "DockerAgent",
    "DevOpsAgent",
    "ObservabilityAgent",
    
    # Development
    "DatabaseAgent",
    "APIDesignAgent",
    "FrontendAgent",
    "MobileAgent",
    "GameDevelopmentAgent",
    
    # Quality
    "TestSuiteAgent",
    "SecurityAgent",
    "CodeReviewAgent",
    "RefactoringAgent",
    "PerformanceAgent",
    
    # Operations
    "MigrationAgent",
    "DependencyAgent",
    "GitAgent",
    
    # Productivity
    "ScaffoldingAgent",
    "DocumentationAgent",
    "DebuggingAgent",
    
    # Business
    "ValidationAgent",
    "ArchitectureAgent",
    "LocalizationAgent",
    "ComplianceAgent",
    
    # Specialized
    "DataScienceAgent",
]
'''
    
    def _get_subpackage_init(self, directory: str) -> str:
        """Generate __init__.py for subpackages"""
        category = directory.split("/")[-1]
        
        agent_map = {
            "infrastructure": ["DockerAgent", "DevOpsAgent", "ObservabilityAgent"],
            "development": ["DatabaseAgent", "APIDesignAgent", "FrontendAgent", "MobileAgent", "GameDevelopmentAgent"],
            "quality": ["TestSuiteAgent", "SecurityAgent", "CodeReviewAgent", "RefactoringAgent", "PerformanceAgent"],
            "operations": ["MigrationAgent", "DependencyAgent", "GitAgent"],
            "productivity": ["ScaffoldingAgent", "DocumentationAgent", "DebuggingAgent"],
            "business": ["ValidationAgent", "ArchitectureAgent", "LocalizationAgent", "ComplianceAgent"],
            "specialized": ["DataScienceAgent"],
        }
        
        agents = agent_map.get(category, [])
        imports = "\n".join([f"from .{self._class_to_file(a)} import {a}" for a in agents])
        all_list = '", "'.join(agents)
        
        return f'''"""
{category.title()} Agents
"""

{imports}

__all__ = ["{all_list}"]
'''
    
    def _class_to_file(self, class_name: str) -> str:
        """Convert class name to file name (e.g., DockerAgent -> docker_agent)"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _create_file(self, file_path: Path, filename: str, directory: str):
        """Create file with appropriate content"""
        
        content_map = {
            "README.md": self._get_readme(),
            "requirements.txt": self._get_requirements(),
            ".env.example": self._get_env_example(),
            ".gitignore": self._get_gitignore(),
            "setup.py": self._get_setup_py(),
            "LICENSE": self._get_license(),
            "CONTRIBUTING.md": self._get_contributing(),
            "agent_config.yaml": self._get_config_yaml(),
            "basic_usage.py": self._get_basic_usage(),
            "multi_agent_workflow.py": self._get_multi_agent_workflow(),
            "custom_agent_example.py": self._get_custom_agent_example(),
            "response_parser.py": self._get_response_parser(),
            "context_builder.py": self._get_context_builder(),
            "test_docker_agent.py": self._get_test_example(),
            "test_orchestrator.py": self._get_test_orchestrator(),
        }
        
        content = content_map.get(filename, self._get_agent_template(filename, directory))
        file_path.write_text(content)
    
    def _get_readme(self) -> str:
        return '''# Claude Code Agents

A comprehensive, reusable suite of 24 specialized AI agents for software development tasks, powered by Anthropic's Claude.

## 🚀 Features

- **24 Specialized Agents** covering all aspects of software development
- **Intelligent Orchestrator** for automatic task routing
- **Multi-Agent Workflows** for complex tasks
- **Modular Architecture** - use agents individually or together
- **Framework Agnostic** - works with any tech stack
- **Production Ready** - comprehensive error handling and logging

## 📦 Installation

```bash
git clone <your-repo-url>
cd claude-code-agents
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

## 🎯 Quick Start

```python
from orchestrator import AgentOrchestrator

# Initialize orchestrator
orchestrator = AgentOrchestrator()

# Automatic agent routing
result = orchestrator.execute("Create a Dockerfile for a Python FastAPI app")
print(result['primary_result']['response'])
```

### Direct Agent Usage

```python
from agents import DockerAgent, SecurityAgent, TestSuiteAgent

# Use specific agents directly
docker = DockerAgent()
result = docker.execute("Create production Dockerfile", {
    "language": "python",
    "framework": "fastapi"
})
```

## 🤖 Available Agents

### Infrastructure (3)
- **DockerAgent** - Container operations, Dockerfiles, Docker Compose
- **DevOpsAgent** - CI/CD pipelines, Kubernetes, infrastructure
- **ObservabilityAgent** - Monitoring, logging, metrics, tracing

### Development (5)
- **DatabaseAgent** - Schema design, queries, migrations, optimization
- **APIDesignAgent** - REST/GraphQL APIs, OpenAPI specs
- **FrontendAgent** - React/Vue/Angular, UI components, state management
- **MobileAgent** - iOS/Android, React Native, Flutter development
- **GameDevelopmentAgent** - Game loops, physics, rendering, ECS

### Quality (5)
- **TestSuiteAgent** - Unit/integration tests, coverage analysis
- **SecurityAgent** - Vulnerability detection, security audits
- **CodeReviewAgent** - Code quality review, best practices
- **RefactoringAgent** - Code improvements, design patterns
- **PerformanceAgent** - Optimization, profiling, bottleneck analysis

### Operations (3)
- **MigrationAgent** - System migrations, upgrades, data migration
- **DependencyAgent** - Package management, updates, security audits
- **GitAgent** - Commit messages, branching strategies, workflows

### Productivity (3)
- **ScaffoldingAgent** - Project setup, boilerplate generation
- **DocumentationAgent** - Code docs, README, API documentation
- **DebuggingAgent** - Bug analysis, troubleshooting, root cause

### Business (4)
- **ValidationAgent** - Input validation, schemas, error handling
- **ArchitectureAgent** - System design, architectural patterns
- **LocalizationAgent** - i18n, translations, RTL support
- **ComplianceAgent** - GDPR, HIPAA, accessibility standards

### Specialized (1)
- **DataScienceAgent** - ML pipelines, feature engineering, modeling

## 📚 Documentation

See `/examples` directory for detailed usage examples:
- `basic_usage.py` - Single agent examples
- `multi_agent_workflow.py` - Complex multi-agent tasks
- `custom_agent_example.py` - Creating your own agents

## 🔧 Configuration

Edit `config/agent_config.yaml` to customize agent behavior:

```yaml
default_model: "claude-sonnet-4-20250514"
max_tokens: 6000

agents:
  docker:
    max_tokens: 4000
  security:
    severity_threshold: "medium"
```

## 🧪 Testing

```bash
pytest tests/
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

Built with [Anthropic Claude](https://www.anthropic.com/claude) API.

## 📞 Support

- Issues: GitHub Issues
- Documentation: See `/examples` and agent docstrings

---

Made with ❤️ for the developer community
'''

    def _get_requirements(self) -> str:
        return '''anthropic>=0.40.0
python-dotenv>=1.0.0
pyyaml>=6.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
'''

    def _get_env_example(self) -> str:
        return '''# Anthropic API Key
# Get your key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Model configuration
DEFAULT_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=6000
'''

    def _get_gitignore(self) -> str:
        return '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log

# OS
.DS_Store
Thumbs.db
'''

    def _get_setup_py(self) -> str:
        return '''from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-code-agents",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive suite of AI agents for software development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/claude-code-agents",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
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
        "anthropic>=0.40.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
)
'''

    def _get_license(self) -> str:
        return '''MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

    def _get_contributing(self) -> str:
        return '''# Contributing to Claude Code Agents

Thank you for your interest in contributing! 🎉

## How to Contribute

### 1. Fork and Clone

```bash
git fork <repo-url>
git clone <your-fork-url>
cd claude-code-agents
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Follow PEP 8 style guide
- Add docstrings to all functions/classes
- Include type hints
- Write tests for new features
- Update documentation

### 4. Run Tests

```bash
pytest tests/
```

### 5. Submit Pull Request

- Write clear commit messages
- Reference any related issues
- Describe your changes in the PR description

## Adding a New Agent

1. Create agent file in appropriate category directory
2. Follow the existing agent structure
3. Add comprehensive system prompt
4. Implement execute() method
5. Add response parsing
6. Update `agents/__init__.py`
7. Add tests
8. Update README.md

## Code Style

```python
# Good
def execute(self, task: str, context: dict = None) -> dict:
    """Execute the agent task."""
    pass

# Include type hints and docstrings
```

## Questions?

Open an issue for discussion!
'''

    def _get_config_yaml(self) -> str:
        return '''# Claude Code Agents Configuration

# Default settings
default_model: "claude-sonnet-4-20250514"
max_tokens: 6000
temperature: 0.7

# Agent-specific settings
agents:
  docker:
    enabled: true
    max_tokens: 4000
  
  security:
    enabled: true
    max_tokens: 8000
    severity_threshold: "medium"
  
  testing:
    enabled: true
    default_framework: "pytest"
    coverage_target: 80
  
  performance:
    enabled: true
    profiling_enabled: true

# Orchestrator settings
orchestrator:
  enable_parallel_execution: true
  max_concurrent_agents: 3
  enable_result_caching: false
  timeout_seconds: 300
'''

    def _get_basic_usage(self) -> str:
        return '''"""
Basic usage examples for Claude Code Agents
"""

from agents import DockerAgent, SecurityAgent, TestSuiteAgent
from orchestrator import AgentOrchestrator


def example_single_agent():
    """Example: Using a single agent directly"""
    print("=== Single Agent Example ===\\n")
    
    agent = DockerAgent()
    result = agent.execute(
        "Create a production-ready Dockerfile for a Node.js Express application",
        context={
            "language": "javascript",
            "framework": "express",
            "dependencies": "express, pg, redis"
        }
    )
    
    print(result['response'][:500] + "...\\n")


def example_orchestrator():
    """Example: Using the orchestrator for automatic routing"""
    print("=== Orchestrator Example ===\\n")
    
    orchestrator = AgentOrchestrator()
    
    result = orchestrator.execute(
        "Create comprehensive unit tests for a user authentication system"
    )
    
    print(f"Task routed to: {result['routing']['primary_agent']}")
    print(f"Reasoning: {result['routing']['reasoning']}\\n")


def example_with_context():
    """Example: Providing rich context to agents"""
    print("=== Context-Rich Example ===\\n")
    
    security_agent = SecurityAgent()
    
    code = '''
def login(username, password):
    user = db.query(f"SELECT * FROM users WHERE username='{username}'")
    if user and user.password == password:
        return user
    return None
'''
    
    result = security_agent.analyze_code(code, "python", "flask")
    
    print(f"Vulnerabilities found: {len(result['vulnerabilities'])}")
    for vuln in result['vulnerabilities'][:2]:
        print(f"  - {vuln['severity']}: {vuln['title']}")


if __name__ == "__main__":
    example_single_agent()
    example_orchestrator()
    example_with_context()
'''

    def _get_multi_agent_workflow(self) -> str:
        return '''"""
Multi-agent workflow examples
"""

from orchestrator import AgentOrchestrator
from agents import (
    ScaffoldingAgent, SecurityAgent, TestSuiteAgent,
    DocumentationAgent, DockerAgent
)


def complete_project_setup():
    """Example: Complete new project setup with multiple agents"""
    print("=== Complete Project Setup ===\\n")
    
    orchestrator = AgentOrchestrator()
    
    # This task will use multiple agents
    result = orchestrator.execute(
        "Create a new REST API project with authentication, database, tests, Docker setup, and documentation",
        context={
            "language": "python",
            "framework": "fastapi",
            "database": "postgresql",
            "auth": "JWT"
        }
    )
    
    print(f"Primary agent: {result['routing']['primary_agent']}")
    print(f"Secondary agents involved: {len(result['routing'].get('secondary_agents', []))}")
    print(f"\\nWorkflow: {result['routing']['workflow']}")


def security_audit_workflow():
    """Example: Complete security audit workflow"""
    print("\\n=== Security Audit Workflow ===\\n")
    
    # Step 1: Code review
    from agents import CodeReviewAgent
    reviewer = CodeReviewAgent()
    review_result = reviewer.execute("Review code for issues")
    
    # Step 2: Security analysis
    security = SecurityAgent()
    security_result = security.execute("Perform security audit")
    
    # Step 3: Generate tests for found issues
    testing = TestSuiteAgent()
    test_result = testing.execute("Create security tests")
    
    print("✓ Code review completed")
    print("✓ Security analysis completed")
    print("✓ Security tests generated")


def deployment_pipeline():
    """Example: Complete deployment pipeline"""
    print("\\n=== Deployment Pipeline ===\\n")
    
    from agents import DockerAgent, DevOpsAgent
    
    # Step 1: Create Docker configuration
    docker = DockerAgent()
    docker_result = docker.execute("Create production Docker setup")
    
    # Step 2: Create CI/CD pipeline
    devops = DevOpsAgent()
    pipeline_result = devops.create_pipeline(
        language="python",
        ci_tool="GitHub Actions",
        test_command="pytest",
        build_command="docker build"
    )
    
    print("✓ Docker configuration created")
    print("✓ CI/CD pipeline configured")


if __name__ == "__main__":
    complete_project_setup()
    security_audit_workflow()
    deployment_pipeline()
'''

    def _get_custom_agent_example(self) -> str:
        return '''"""
Example of creating a custom agent
"""

from anthropic import Anthropic
import os


class CustomAgent:
    """
    Template for creating your own custom agent.
    
    Follow this pattern to create specialized agents for your needs.
    """
    
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        # Define your agent's expertise and behavior
        self.system_prompt = """You are a [YOUR SPECIALIZATION] specialist with expertise in:

1. [Core Competency 1]:
   - [Skill 1]
   - [Skill 2]

2. [Core Competency 2]:
   - [Skill 1]
   - [Skill 2]

Best practices:
- [Practice 1]
- [Practice 2]
"""

    def execute(self, task: str, context: dict = None) -> dict:
        """Execute the agent's task"""
        messages = [{"role": "user", "content": self._build_prompt(task, context)}]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=6000,
            system=self.system_prompt,
            messages=messages
        )
        
        return self._parse_response(response)
    
    def _build_prompt(self, task: str, context: dict = None) -> str:
        """Build the prompt with task and context"""
        prompt = f"Task: {task}\\n\\n"
        
        if context:
            prompt += "Context:\\n"
            for key, value in context.items():
                prompt += f"- {key}: {value}\\n"
            prompt += "\\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        """Parse Claude's response"""
        text_content = "".join(
            block.text for block in response.content if block.type == "text"
        )
        
        # Add custom parsing logic here
        
        return {
            "response": text_content,
            # Add custom fields
        }


if __name__ == "__main__":
    agent = CustomAgent()
    result = agent.execute("Your task here", {"key": "value"})
    print(result['response'])
'''

    def _get_response_parser(self) -> str:
        return '''"""
Utility functions for parsing agent responses
"""

import re
from typing import List, Dict, Any


def extract_code_blocks(text: str) -> List[Dict[str, str]]:
    """Extract code blocks from markdown text"""
    pattern = r"```(\\w+)\\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    
    return [
        {"language": lang, "content": code.strip()}
        for lang, code in matches
    ]


def extract_json_objects(text: str) -> List[Dict]:
    """Extract JSON objects from text"""
    import json
    
    pattern = r"\\{[^{}]*(?:\\{[^{}]*\\}[^{}]*)*\\}"
    matches = re.findall(pattern, text, re.DOTALL)
    
    objects = []
    for match in matches:
        try:
            objects.append(json.loads(match))
        except json.JSONDecodeError:
            continue
    
    return objects


def extract_lists(text: str) -> List[str]:
    """Extract bullet point lists from text"""
    lines = text.split('\\n')
    items = []
    
    for line in lines:
        # Match various list formats
        match = re.match(r'^[\\s]*[•\\-\\*]\\s+(.+), line)
        if match:
            items.append(match.group(1).strip())
    
    return items


def parse_severity_levels(text: str) -> Dict[str, List[str]]:
    """Parse items by severity level"""
    levels = {
        "critical": [],
        "high": [],
        "medium": [],
        "low": []
    }
    
    lines = text.split('\\n')
    for line in lines:
        line_lower = line.lower()
        for level in levels.keys():
            if level in line_lower or f"🔴" in line and level == "critical":
                levels[level].append(line.strip())
    
    return levels
'''

    def _get_context_builder(self) -> str:
        return '''"""
Utility functions for building agent context
"""

from typing import Dict, Any, List
from pathlib import Path


def build_code_context(
    code: str,
    language: str,
    file_path: str = None,
    dependencies: List[str] = None
) -> Dict[str, Any]:
    """Build context for code-related tasks"""
    context = {
        "code": code,
        "language": language
    }
    
    if file_path:
        context["file_path"] = file_path
    
    if dependencies:
        context["dependencies"] = ", ".join(dependencies)
    
    return context


def
