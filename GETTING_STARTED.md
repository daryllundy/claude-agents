# Getting Started with Claude Code Agents

Welcome! This repository contains 24 specialized AI agents designed for **Claude Code Pro** users.

## What Changed?

This repository has been updated to work as **sub-agents within Claude Code Pro** instead of requiring API keys. This means:

✅ **No API keys needed** - Works directly with your Claude Code Pro subscription
✅ **No Python dependencies** - Agents run natively in Claude Code
✅ **Simple invocation** - Just ask Claude Code to use a specialist
✅ **Full tool access** - Agents can Read, Write, Edit files and run commands

## Quick Start (3 Steps)

### 1. Ensure You Have Claude Code Pro
These agents require a Claude Code Pro subscription to function.

### 2. Reference This Repository
Clone or keep this repository accessible:
```bash
git clone https://github.com/yourusername/claude-code-agents.git
```

### 3. Start Using Agents
In Claude Code, simply request an agent:
```
"Use the docker-specialist to create a production Dockerfile for my Flask app"
```

That's it! No setup, no configuration, no API keys.

## Available Agents

### 🏗️ Infrastructure (3 agents)
- `docker-specialist` - Dockerfile, containers, docker-compose
- `devops-specialist` - CI/CD, GitHub Actions, automation
- `observability-specialist` - Monitoring, logging, Prometheus, Grafana

### 💻 Development (3 agents)
- `database-specialist` - Schema design, SQL, migrations
- `frontend-specialist` - React, Vue, Angular, UI/UX
- `mobile-specialist` - iOS, Android, React Native, Flutter

### ✅ Quality (5 agents)
- `test-specialist` - Unit tests, integration tests, TDD
- `security-specialist` - Security audits, vulnerability fixes
- `code-review-specialist` - Code review, best practices
- `refactoring-specialist` - Code modernization, cleanup
- `performance-specialist` - Performance optimization, profiling

### ⚙️ Operations (3 agents)
- `migration-specialist` - Database migrations, upgrades
- `dependency-specialist` - Dependency updates, security patches
- `git-specialist` - Git workflows, merge conflicts

### 🚀 Productivity (3 agents)
- `scaffolding-specialist` - Project setup, boilerplate
- `documentation-specialist` - Docs, READMEs, API docs
- `debugging-specialist` - Bug hunting, error resolution

### 💼 Business (4 agents)
- `validation-specialist` - Input validation, business rules
- `architecture-specialist` - System design, architecture
- `localization-specialist` - i18n, translations
- `compliance-specialist` - GDPR, HIPAA, compliance

### 🔬 Specialized (1 agent)
- `data-science-specialist` - ML pipelines, data analysis

## Example Usage

### Simple Task
```
"Use the security-specialist to audit the authentication code in src/auth/"
```

### Multi-Step Workflow
```
"I need to build a new API endpoint. Let's:
1. Use architecture-specialist to design the endpoint structure
2. Use scaffolding-specialist to create the files
3. Use test-specialist to add comprehensive tests
4. Use security-specialist to ensure it's secure"
```

### Performance Optimization
```
"Use performance-specialist to analyze and optimize the slow database queries in the reports module"
```

## How It Works

When you request an agent in Claude Code Pro:

1. **You ask** for a specialist (e.g., "Use docker-specialist...")
2. **Claude Code invokes** the agent using the Task tool
3. **Agent works** autonomously with full file access
4. **Results return** to your conversation
5. **You review** and continue

## Documentation

- **[README.md](README.md)** - Overview and quick reference
- **[CLAUDE_CODE_USAGE.md](CLAUDE_CODE_USAGE.md)** - Comprehensive guide with examples
- **[.claude/agents/AGENTS_REGISTRY.md](.claude/agents/AGENTS_REGISTRY.md)** - Complete agent catalog
- **[.claude/agents/*.md](.claude/agents/)** - Individual agent details

## Best Practices

### 1. Be Specific
❌ "Help with Docker"
✅ "Use docker-specialist to create a multi-stage Dockerfile for my Python Flask app with health checks and non-root user"

### 2. Provide Context
Include:
- File paths
- Technologies used
- Requirements/constraints
- Expected outcome

### 3. Sequential for Dependencies
If tasks depend on each other, run them one at a time.

### 4. Review Output
Always review agent work before proceeding.

## Real-World Workflows

### New Feature Development
```
1. architecture-specialist → Design the feature
2. scaffolding-specialist → Create structure
3. database-specialist → Design schema
4. test-specialist → Add tests
5. security-specialist → Security review
6. documentation-specialist → Document it
```

### Security Hardening
```
1. security-specialist → Full security audit
2. security-specialist → Fix critical issues
3. dependency-specialist → Update vulnerable packages
4. docker-specialist → Harden containers
5. compliance-specialist → Ensure compliance
```

### Performance Optimization
```
1. performance-specialist → Identify bottlenecks
2. database-specialist → Optimize queries
3. performance-specialist → Add caching
4. observability-specialist → Add monitoring
```

## Troubleshooting

### "Agent not being invoked?"
- Ensure you have Claude Code Pro
- Be explicit: "Use the [agent-name] to..."
- Use exact agent names from the list above

### "Agent needs more context?"
Provide:
- Specific file paths
- Current state description
- Desired outcome
- Technology stack
- Constraints

## Next Steps

1. ✅ Browse available agents (above)
2. ✅ Try a simple agent request
3. ✅ Review [CLAUDE_CODE_USAGE.md](CLAUDE_CODE_USAGE.md) for advanced patterns
4. ✅ Check [.claude/agents/AGENTS_REGISTRY.md](.claude/agents/AGENTS_REGISTRY.md) for details
5. ✅ Build complex multi-agent workflows

## Legacy Python Implementation

The `agents/` directory contains the original Python implementations for reference. These are NOT needed for Claude Code Pro usage but can be useful to understand agent capabilities.

## Questions?

- Check the documentation files listed above
- Review individual agent prompts in `.claude/agents/`
- Open an issue on GitHub

---

**Ready to build?** Start invoking specialized agents in your Claude Code Pro session! 🚀
