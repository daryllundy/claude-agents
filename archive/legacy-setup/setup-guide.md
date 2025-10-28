# Claude Code Agents - Complete Setup Guide

This guide will help you set up and organize all 24 specialized AI agents into a reusable repository.

## 📋 Table of Contents

1. [Quick Setup (Recommended)](#quick-setup)
2. [Manual Setup](#manual-setup)
3. [Adding Agent Code](#adding-agent-code)
4. [Using in Other Projects](#using-in-other-projects)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Setup (Recommended)

The fastest way to get started:

### Option 1: Bash Script (Linux/Mac)

```bash
# Download and run the quick start script
chmod +x quickstart.sh
./quickstart.sh
```

### Option 2: Python Script

```bash
# Run the Python setup script
python3 setup_agents_repo.py

# Navigate to the created directory
cd claude-code-agents

# Set up your API key
cp .env.example .env
nano .env  # Add your ANTHROPIC_API_KEY
```

---

## 🔧 Manual Setup

If you prefer to set up manually:

### Step 1: Create Directory Structure

```bash
mkdir -p claude-code-agents/{agents/{infrastructure,development,quality,operations,productivity,business,specialized},orchestrator,utils,examples,tests,config}
cd claude-code-agents
```

### Step 2: Create Essential Files

Create `requirements.txt`:
```text
anthropic>=0.40.0
python-dotenv>=1.0.0
pyyaml>=6.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

Create `.env.example`:
```bash
ANTHROPIC_API_KEY=your_api_key_here
DEFAULT_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=6000
```

Create `.gitignore`:
```text
__pycache__/
*.py[cod]
venv/
.env
.pytest_cache/
*.log
.DS_Store
```

### Step 3: Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📝 Adding Agent Code

You have the agent code from the artifacts. Here's how to organize it:

### Method 1: Using the Populate Script

```bash
# Create a temporary directory for your agent files
mkdir agent-code

# Save each agent file there with its name (e.g., docker_agent.py)

# Run the populate script
python populate_agents.py --source-dir ./agent-code --target-dir ./claude-code-agents

# Verify
python populate_agents.py --verify
```

### Method 2: Manual File Placement

Place each agent file in its category:

```
claude-code-agents/
├── agents/
│   ├── infrastructure/
│   │   ├── docker_agent.py          ← Copy Docker Agent here
│   │   ├── devops_agent.py          ← Copy DevOps Agent here
│   │   └── observability_agent.py   ← Copy Observability Agent here
│   │
│   ├── development/
│   │   ├── database_agent.py        ← Copy Database Agent here
│   │   ├── api_design_agent.py      ← Copy API Design Agent here
│   │   ├── frontend_agent.py        ← Copy Frontend Agent here
│   │   ├── mobile_agent.py          ← Copy Mobile Agent here
│   │   └── game_dev_agent.py        ← Copy Game Dev Agent here
│   │
│   ├── quality/
│   │   ├── test_suite_agent.py      ← Copy Test Suite Agent here
│   │   ├── security_agent.py        ← Copy Security Agent here
│   │   ├── code_review_agent.py     ← Copy Code Review Agent here
│   │   ├── refactoring_agent.py     ← Copy Refactoring Agent here
│   │   └── performance_agent.py     ← Copy Performance Agent here
│   │
│   ├── operations/
│   │   ├── migration_agent.py       ← Copy Migration Agent here
│   │   ├── dependency_agent.py      ← Copy Dependency Agent here
│   │   └── git_agent.py             ← Copy Git Agent here
│   │
│   ├── productivity/
│   │   ├── scaffolding_agent.py     ← Copy Scaffolding Agent here
│   │   ├── documentation_agent.py   ← Copy Documentation Agent here
│   │   └── debugging_agent.py       ← Copy Debugging Agent here
│   │
│   ├── business/
│   │   ├── validation_agent.py      ← Copy Validation Agent here
│   │   ├── architecture_agent.py    ← Copy Architecture Agent here
│   │   ├── localization_agent.py    ← Copy Localization Agent here
│   │   └── compliance_agent.py      ← Copy Compliance Agent here
│   │
│   └── specialized/
│       └── data_science_agent.py    ← Copy Data Science Agent here
│
└── orchestrator/
    └── agent_orchestrator.py        ← Copy Orchestrator here
```

### Method 3: Direct Copy from Artifacts

If you have all agents in one location:

```bash
# Copy infrastructure agents
cp /path/to/docker_agent.py claude-code-agents/agents/infrastructure/
cp /path/to/devops_agent.py claude-code-agents/agents/infrastructure/
cp /path/to/observability_agent.py claude-code-agents/agents/infrastructure/

# Copy development agents
cp /path/to/database_agent.py claude-code-agents/agents/development/
# ... repeat for all agents
```

---

## 🔗 Using in Other Projects

### Option 1: Install as Python Package

```bash
# From the claude-code-agents directory
pip install -e .

# Now use in any Python project
from agents import DockerAgent, SecurityAgent
from orchestrator import AgentOrchestrator
```

### Option 2: Git Submodule (Recommended for Teams)

```bash
# In your project directory
git submodule add https://github.com/yourusername/claude-code-agents.git

# Use in your code
from claude-code-agents.agents import DockerAgent
```

### Option 3: Copy to Project

```bash
# Copy to your project
cp -r claude-code-agents/agents your-project/
cp -r claude-code-agents/orchestrator your-project/

# Add to requirements
echo "anthropic>=0.40.0" >> your-project/requirements.txt
```

### Option 4: Use as Path

```python
# Add to sys.path
import sys
sys.path.append('/path/to/claude-code-agents')

from agents import DockerAgent
```

---

## 🧪 Testing

### Run All Tests

```bash
cd claude-code-agents
source venv/bin/activate
pytest tests/ -v
```

### Test Single Agent

```bash
pytest tests/test_docker_agent.py -v
```

### Test with Coverage

```bash
pytest --cov=agents --cov=orchestrator tests/
```

### Manual Testing

```python
# Test Docker Agent
from agents import DockerAgent

agent = DockerAgent()
result = agent.execute("Create a Dockerfile for Python", {"language": "python"})
print(result['response'])
```

---

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'anthropic'
```

**Solution:**
```bash
pip install anthropic python-dotenv pyyaml
```

### Issue: API Key Error

```
Error: ANTHROPIC_API_KEY not found
```

**Solution:**
```bash
# Make sure .env file exists
cp .env.example .env

# Edit and add your key
nano .env  # or use any editor
```

### Issue: Import Errors

```
ImportError: cannot import name 'DockerAgent'
```

**Solution:**
```bash
# Ensure all __init__.py files exist
find agents -type d -exec touch {}/__init__.py \;

# Verify file structure
ls -la agents/infrastructure/docker_agent.py
```

### Issue: Permission Denied

```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
chmod +x quickstart.sh
# Or run with python
python3 setup_agents_repo.py
```

---

## 📚 Additional Resources

### File Checklist

✅ All 24 agent files in correct directories
✅ `agent_orchestrator.py` in orchestrator/
✅ All `__init__.py` files created
✅ `.env` file with API key
✅ `requirements.txt` installed
✅ Virtual environment activated

### Directory Structure Reference

```
claude-code-agents/
├── agents/
│   ├── __init__.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── docker_agent.py
│   │   ├── devops_agent.py
│   │   └── observability_agent.py
│   ├── development/ (5 agents)
│   ├── quality/ (5 agents)
│   ├── operations/ (3 agents)
│   ├── productivity/ (3 agents)
│   ├── business/ (4 agents)
│   └── specialized/ (1 agent)
├── orchestrator/
│   ├── __init__.py
│   └── agent_orchestrator.py
├── utils/
├── examples/
├── tests/
├── config/
├── .env
├── requirements.txt
├── README.md
└── setup.py
```

---

## 🎯 Quick Commands Reference

```bash
# Setup
python3 setup_agents_repo.py              # Create structure
python3 populate_agents.py                # Add agent code
cp .env.example .env                      # Create env file

# Install
python3 -m venv venv                      # Create venv
source venv/bin/activate                  # Activate (Unix)
venv\Scripts\activate                     # Activate (Windows)
pip install -r requirements.txt           # Install deps

# Test
pytest tests/                             # Run tests
python examples/basic_usage.py            # Try examples

# Use
python3                                   # Start Python
>>> from agents import DockerAgent        # Import agent
>>> agent = DockerAgent()                 # Create instance
>>> result = agent.execute("...")         # Use agent
```

---

## ✅ Success Checklist

Before considering setup complete:

- [ ] Repository structure created
- [ ] All 24 agent files in place
- [ ] Orchestrator file in place
- [ ] `.env` file with valid API key
- [ ] Dependencies installed
- [ ] Virtual environment working
- [ ] Can import agents successfully
- [ ] Basic test passes
- [ ] Example script runs

---

## 🤝 Need Help?

- Check existing agents for examples
- Review error messages carefully
- Ensure API key is valid
- Verify all files are in correct locations
- Check Python version (3.8+)

---

**You're all set!** Your Claude Code Agents repository is ready to use across all your projects. 🚀
