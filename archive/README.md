# Archive Directory

This directory contains legacy code and setup scripts that are no longer needed for Claude Code Pro usage.

## Contents

### legacy-python-implementation/
Original Python-based agent implementations that required Anthropic API keys. These are kept for reference but are NOT needed for Claude Code Pro.

**Contents:**
- `agents/` - Original Python agent classes
- `orchestrator/` - Agent orchestration system
- `utils/` - Utility functions
- `setup.py` - Python package configuration
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variable template

### legacy-setup/
Original setup scripts for the Python-based system.

**Contents:**
- `setup_agents_repo.py` - Repository setup script
- `populate_agents.py` - Agent population script
- `quick-start.sh` - Bash quick-start script
- `setup-guide.md` - Original setup guide

## Why Are These Archived?

The repository has been updated to work as **Claude Code Pro sub-agents**, which:
- Don't require API keys
- Don't need Python dependencies
- Work directly within Claude Code
- Are invoked using natural language

The legacy implementations are kept for:
- Historical reference
- Understanding agent logic
- Potential future use cases
- Educational purposes

## Using Current Version

For current Claude Code Pro usage, see the main repository files:
- `README.md` - Quick start and overview
- `GETTING_STARTED.md` - Beginner's guide
- `CLAUDE_CODE_USAGE.md` - Comprehensive usage guide
- `.claude/agents/` - Agent prompt definitions
