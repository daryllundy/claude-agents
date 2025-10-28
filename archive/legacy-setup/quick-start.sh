#!/bin/bash
# Quick Start Script for Claude Code Agents
# This script sets up everything you need in one command

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REPO_NAME="claude-code-agents"
PYTHON_MIN_VERSION="3.8"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Claude Code Agents - Quick Start Setup                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python found: $(python3 --version)"

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${RED}❌ Python version $PYTHON_VERSION is too old${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python version $PYTHON_VERSION is compatible"
echo ""

# Ask for target directory
read -p "Install directory [$REPO_NAME]: " USER_DIR
TARGET_DIR="${USER_DIR:-$REPO_NAME}"

if [ -d "$TARGET_DIR" ]; then
    echo -e "${YELLOW}⚠️  Directory $TARGET_DIR already exists${NC}"
    read -p "Continue and overwrite? (y/N): " OVERWRITE
    if [ "$OVERWRITE" != "y" ] && [ "$OVERWRITE" != "Y" ]; then
        echo "Aborted."
        exit 0
    fi
fi

echo ""
echo -e "${BLUE}Creating repository structure...${NC}"

# Create directory structure
mkdir -p "$TARGET_DIR"/{agents/{infrastructure,development,quality,operations,productivity,business,specialized},orchestrator,utils,examples,tests,config}

echo -e "${GREEN}✓${NC} Directory structure created"

# Create requirements.txt
cat > "$TARGET_DIR/requirements.txt" << 'EOF'
anthropic>=0.40.0
python-dotenv>=1.0.0
pyyaml>=6.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
EOF

echo -e "${GREEN}✓${NC} requirements.txt created"

# Create .env.example
cat > "$TARGET_DIR/.env.example" << 'EOF'
# Anthropic API Key
# Get your key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Model configuration
DEFAULT_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=6000
EOF

echo -e "${GREEN}✓${NC} .env.example created"

# Create .gitignore
cat > "$TARGET_DIR/.gitignore" << 'EOF'
# Python
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

# Environment
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
EOF

echo -e "${GREEN}✓${NC} .gitignore created"

# Create README.md
cat > "$TARGET_DIR/README.md" << 'EOF'
# Claude Code Agents

A comprehensive suite of 24 specialized AI agents for software development.

## Quick Start

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run examples
python examples/basic_usage.py
```

## Available Agents

- **Infrastructure**: Docker, DevOps, Observability
- **Development**: Database, API Design, Frontend, Mobile, Game Dev
- **Quality**: Testing, Security, Code Review, Refactoring, Performance
- **Operations**: Migration, Dependency, Git
- **Productivity**: Scaffolding, Documentation, Debugging
- **Business**: Validation, Architecture, Localization, Compliance
- **Specialized**: Data Science

## Usage

```python
from orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()
result = orchestrator.execute("Create a Dockerfile for Python FastAPI")
print(result['primary_result']['response'])
```

See `/examples` for more usage patterns.
EOF

echo -e "${GREEN}✓${NC} README.md created"

# Create basic example
mkdir -p "$TARGET_DIR/examples"
cat > "$TARGET_DIR/examples/basic_usage.py" << 'EOF'
"""
Basic usage example for Claude Code Agents
Run this after setting up your API key in .env
"""

print("Claude Code Agents - Basic Usage Example")
print("=" * 50)
print()
print("To use the agents, you need to:")
print("1. Add agent implementations to the agents/ directory")
print("2. Set ANTHROPIC_API_KEY in .env file")
print("3. Import and use agents")
print()
print("Example:")
print("""
from agents import DockerAgent

agent = DockerAgent()
result = agent.execute("Create a Dockerfile", {"language": "python"})
print(result['response'])
""")
print()
print("See the README.md for complete setup instructions.")
EOF

echo -e "${GREEN}✓${NC} Example files created"

# Create __init__.py files
touch "$TARGET_DIR/agents/__init__.py"
touch "$TARGET_DIR/agents/infrastructure/__init__.py"
touch "$TARGET_DIR/agents/development/__init__.py"
touch "$TARGET_DIR/agents/quality/__init__.py"
touch "$TARGET_DIR/agents/operations/__init__.py"
touch "$TARGET_DIR/agents/productivity/__init__.py"
touch "$TARGET_DIR/agents/business/__init__.py"
touch "$TARGET_DIR/agents/specialized/__init__.py"
touch "$TARGET_DIR/orchestrator/__init__.py"
touch "$TARGET_DIR/utils/__init__.py"
touch "$TARGET_DIR/tests/__init__.py"

echo -e "${GREEN}✓${NC} Python package files created"

# Copy .env.example to .env
cp "$TARGET_DIR/.env.example" "$TARGET_DIR/.env"
echo -e "${GREEN}✓${NC} .env file created (you need to add your API key)"

echo ""
echo -e "${BLUE}Setting up virtual environment...${NC}"

# Create virtual environment
cd "$TARGET_DIR"
python3 -m venv venv

echo -e "${GREEN}✓${NC} Virtual environment created"

# Activate virtual environment and install dependencies
echo ""
echo -e "${BLUE}Installing dependencies...${NC}"

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    echo -e "${GREEN}✓${NC} Dependencies installed"
else
    echo -e "${YELLOW}⚠️  Virtual environment activation failed${NC}"
    echo "You may need to activate it manually and install requirements"
fi

cd - > /dev/null

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     ✅ Setup Complete!                                     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo -e "  1. Add your Anthropic API key:"
echo -e "     ${YELLOW}cd $TARGET_DIR${NC}"
echo -e "     ${YELLOW}nano .env${NC}  # or use your preferred editor"
echo ""
echo -e "  2. Add agent implementations:"
echo -e "     Copy your agent .py files to the agents/ subdirectories"
echo ""
echo -e "  3. Activate the virtual environment:"
echo -e "     ${YELLOW}source $TARGET_DIR/venv/bin/activate${NC}"
echo ""
echo -e "  4. Test the setup:"
echo -e "     ${YELLOW}python examples/basic_usage.py${NC}"
echo ""
echo -e "${BLUE}Repository structure:${NC}"
echo "  $TARGET_DIR/"
echo "  ├── agents/              # Place agent files here"
echo "  │   ├── infrastructure/"
echo "  │   ├── development/"
echo "  │   ├── quality/"
echo "  │   ├── operations/"
echo "  │   ├── productivity/"
echo "  │   ├── business/"
echo "  │   └── specialized/"
echo "  ├── orchestrator/        # Agent coordinator"
echo "  ├── examples/            # Usage examples"
echo "  ├── tests/               # Test files"
echo "  ├── .env                 # ⚠️  Add your API key here!"
echo "  └── requirements.txt     # Dependencies"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
