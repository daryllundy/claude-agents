# Claude Code Agents

A comprehensive collection of 24 specialized AI agents designed for **Claude Code Pro** users. These agents work as intelligent sub-agents that can be invoked within Claude Code to handle specific development tasks with deep domain expertise.

## Features

- **24 Specialized Agents** organized into 6 categories
- **Ready for Claude Code Pro** - Use as sub-agents via the Task tool
- **Deep Domain Expertise** - Each agent specializes in a specific area
- **No API Keys Required** - Works directly with Claude Code Pro
- **Detailed Agent Prompts** - Pre-configured with best practices and expertise
- **Easy to Invoke** - Simple natural language requests

## Agent Categories

### Infrastructure (3 agents)
- **docker-specialist** - Container configuration and optimization
- **devops-specialist** - CI/CD, automation, and infrastructure as code
- **observability-specialist** - Monitoring, logging, and alerting

### Development (3 agents)
- **database-specialist** - Schema design, queries, and optimization
- **frontend-specialist** - UI/UX implementation and optimization
- **mobile-specialist** - iOS, Android, and cross-platform development

### Quality (5 agents)
- **test-specialist** - Comprehensive test generation
- **security-specialist** - Vulnerability scanning and secure coding
- **code-review-specialist** - Automated code review and suggestions
- **refactoring-specialist** - Code improvement and modernization
- **performance-specialist** - Performance analysis and optimization

### Operations (3 agents)
- **migration-specialist** - Database and codebase migrations
- **dependency-specialist** - Dependency management and updates
- **git-specialist** - Git workflow and repository management

### Productivity (3 agents)
- **scaffolding-specialist** - Project and component scaffolding
- **documentation-specialist** - Automated documentation generation
- **debugging-specialist** - Bug detection and resolution

### Business (4 agents)
- **validation-specialist** - Input validation and business rules
- **architecture-specialist** - System design and architecture decisions
- **localization-specialist** - Internationalization and localization
- **compliance-specialist** - Regulatory compliance (GDPR, HIPAA, etc.)

### Specialized (1 agent)
- **data-science-specialist** - ML pipelines, data analysis, and visualization

## Quick Start

### Prerequisites

- **Claude Code Pro subscription** - These agents require Claude Code Pro to function
- Access to your project in Claude Code

### Setup

1. **Clone or reference this repository**:
   ```bash
   git clone https://github.com/daryllundy/claude-agents.git
   ```

2. **(Optional) Auto-install recommended agents in another project**:
   ```bash
   curl -sSL https://raw.githubusercontent.com/daryllundy/claude-agents/main/scripts/recommend_agents.sh | bash
   ```
   Run the command from the root of your project repository. The script scans the
   codebase, recommends relevant specialist agents, and downloads their prompt
   files into `.claude/agents/`.

3. **That's it!** No API keys or dependencies needed. The agents work directly within Claude Code Pro.

### Basic Usage

Simply ask Claude Code to invoke a specialist agent:

```
"Use the docker-specialist to create a production-ready Dockerfile for my Python Flask application"
```

Claude Code will automatically invoke the appropriate sub-agent to handle the task.

### Example Invocations

#### Single Agent Task
```
"Use the security-specialist to audit the authentication system in src/auth/"
```

#### Multi-Step Workflow
```
"I need to:
1. Use scaffolding-specialist to create a FastAPI project structure
2. Then use database-specialist to design a user schema
3. Then use test-specialist to add comprehensive tests"
```

#### Complex Task
```
"Use the performance-specialist to analyze and optimize the slow queries in the reports module"
```

## How It Works

These agents are specialized prompts designed for Claude Code Pro's Task tool. When you request an agent:

1. **Claude Code identifies** the appropriate specialist agent
2. **Invokes the agent** as a sub-agent with the Task tool
3. **Agent executes** with full access to Read, Write, Edit, Bash, Glob, and Grep tools
4. **Results return** to your main conversation
5. **You review and proceed** with the next step

## Project Structure

```
claude-agents/
├── .claude/
│   ├── agents/                      # Agent prompt definitions
│   │   ├── AGENTS_REGISTRY.md       # Complete agent catalog
│   │   ├── docker-specialist.md     # Docker agent prompt
│   │   ├── security-specialist.md   # Security agent prompt
│   │   ├── test-specialist.md       # Testing agent prompt
│   │   └── ...                      # Other agent prompts
│   └── settings.local.json          # Claude Code settings
├── archive/                         # Legacy code (reference only)
│   ├── legacy-python-implementation/ # Original Python agents
│   ├── legacy-setup/                # Old setup scripts
│   └── README.md                    # Archive documentation
├── examples/                        # Usage examples
│   └── README.md                    # Example workflows
├── scripts/                         # Utility scripts
│   └── recommend_agents.sh          # Agent recommendation script
├── CLAUDE_CODE_USAGE.md            # Comprehensive usage guide
├── GETTING_STARTED.md              # Beginner's guide
└── README.md                        # This file
```

## Agent Reference

For detailed information about each agent, see:
- **Quick Reference**: `.claude/agents/AGENTS_REGISTRY.md`
- **Comprehensive Guide**: `CLAUDE_CODE_USAGE.md`
- **Individual Agents**: `.claude/agents/*.md`

## Requirements

- **Claude Code Pro subscription** (required)
- No additional dependencies or API keys needed

## Real-World Examples

### Example 1: Building a Secure API
```
Step 1: "Use architecture-specialist to design a RESTful API architecture for a todo app"
Step 2: "Use scaffolding-specialist to create the project structure"
Step 3: "Use security-specialist to implement JWT authentication"
Step 4: "Use test-specialist to add comprehensive API tests"
Step 5: "Use documentation-specialist to generate API documentation"
```

### Example 2: Optimizing Performance
```
"Use performance-specialist to identify and fix performance bottlenecks in the user dashboard"
```

### Example 3: Security Audit
```
"Use security-specialist to perform a comprehensive security audit of the payment processing code"
```

### Example 4: Containerization
```
"Use docker-specialist to create an optimized multi-stage Dockerfile for this Node.js application"
```

## Best Practices

1. **Be Specific**: Provide clear context and requirements
   - ❌ "Use docker-specialist to help with Docker"
   - ✅ "Use docker-specialist to create a production Dockerfile for my Python Flask app with health checks"

2. **Sequential Tasks**: For dependent tasks, execute one at a time
3. **Provide Context**: Include file paths, technologies, and constraints
4. **Review Output**: Always review agent results before proceeding

## Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Beginner's guide to getting started
- **[CLAUDE_CODE_USAGE.md](CLAUDE_CODE_USAGE.md)** - Comprehensive usage guide with examples
- **[.claude/agents/AGENTS_REGISTRY.md](.claude/agents/AGENTS_REGISTRY.md)** - Complete agent catalog
- **[examples/README.md](examples/README.md)** - Real-world usage examples and workflows
- **[archive/README.md](archive/README.md)** - Information about legacy implementations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Ideas for contributions:
- Additional specialized agents
- Improved agent prompts
- More usage examples
- Documentation improvements

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

Built with Claude Code Pro by Anthropic

---

**Ready to supercharge your development workflow?** Start using these specialized agents in your Claude Code Pro session today!
