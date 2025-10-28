# Using Claude Code Agents with Claude Code Pro

This guide shows you how to use the 24 specialized agents as sub-agents within Claude Code Pro.

## Overview

These agents are designed to work as specialized sub-agents that you can invoke using Claude Code's Task tool. Each agent has deep expertise in a specific domain and can handle complex tasks autonomously.

## Prerequisites

- Claude Code Pro subscription
- Basic understanding of Claude Code interface
- This repository cloned or referenced

## How Sub-Agents Work

In Claude Code Pro, you can invoke specialized sub-agents to handle specific tasks. Each agent:
- Has access to relevant tools (Read, Write, Edit, Bash, Glob, Grep)
- Operates autonomously on the given task
- Returns results back to the main conversation
- Can be run sequentially or in parallel

## Agent Invocation Methods

### Method 1: Direct Task Invocation

Ask Claude Code to invoke an agent directly:

```
"Use the docker-specialist agent to create a production-ready Dockerfile for my Python Flask application"
```

Claude Code will use the Task tool to invoke the appropriate agent.

### Method 2: Explicit Task Tool Request

Request specific agent invocation:

```
"Please invoke the security-specialist agent to audit the authentication system in src/auth/"
```

### Method 3: Complex Multi-Agent Workflows

For complex tasks requiring multiple agents:

```
"I need to:
1. Use the scaffolding-specialist to create a new FastAPI project structure
2. Then use the database-specialist to design the schema
3. Then use the test-specialist to add comprehensive tests
4. Finally use the security-specialist to audit the security"
```

## Agent Reference Guide

### Infrastructure Agents

#### docker-specialist
```
"Use docker-specialist to create an optimized multi-stage Dockerfile for my Node.js app"
```
**Use for**: Dockerfiles, container optimization, docker-compose

#### devops-specialist
```
"Use devops-specialist to set up a GitHub Actions CI/CD pipeline for testing and deployment"
```
**Use for**: CI/CD, automation, infrastructure as code

#### observability-specialist
```
"Use observability-specialist to add Prometheus monitoring to my application"
```
**Use for**: Monitoring, logging, alerting, metrics

### Development Agents

#### database-specialist
```
"Use database-specialist to design a normalized schema for an e-commerce platform"
```
**Use for**: Schema design, queries, migrations, optimization

#### frontend-specialist
```
"Use frontend-specialist to create a responsive React dashboard component"
```
**Use for**: React/Vue/Angular development, UI components

#### mobile-specialist
```
"Use mobile-specialist to create a React Native authentication screen"
```
**Use for**: iOS/Android development, cross-platform apps

### Quality Agents

#### test-specialist
```
"Use test-specialist to create comprehensive unit and integration tests for the UserService class"
```
**Use for**: Test generation, TDD, test coverage

#### security-specialist
```
"Use security-specialist to perform a security audit of the payment processing code"
```
**Use for**: Security audits, vulnerability fixes, secure coding

#### code-review-specialist
```
"Use code-review-specialist to review the recent changes in src/api/"
```
**Use for**: Code reviews, quality analysis, improvements

#### refactoring-specialist
```
"Use refactoring-specialist to refactor this legacy code to use modern ES6+ features"
```
**Use for**: Code modernization, technical debt, restructuring

#### performance-specialist
```
"Use performance-specialist to optimize the slow database queries in the reports module"
```
**Use for**: Performance optimization, profiling, caching

### Operations Agents

#### migration-specialist
```
"Use migration-specialist to create a migration plan from MongoDB to PostgreSQL"
```
**Use for**: Database migrations, version upgrades, data transformations

#### dependency-specialist
```
"Use dependency-specialist to update all dependencies and resolve conflicts"
```
**Use for**: Dependency management, version updates, security patches

#### git-specialist
```
"Use git-specialist to help resolve this complex merge conflict"
```
**Use for**: Git operations, branching strategies, repository management

### Productivity Agents

#### scaffolding-specialist
```
"Use scaffolding-specialist to create a new microservice with FastAPI following best practices"
```
**Use for**: Project setup, boilerplate generation, structure

#### documentation-specialist
```
"Use documentation-specialist to generate API documentation from the code"
```
**Use for**: Documentation generation, README files, API docs

#### debugging-specialist
```
"Use debugging-specialist to find why the user authentication is failing intermittently"
```
**Use for**: Bug hunting, debugging, error resolution

### Business Agents

#### validation-specialist
```
"Use validation-specialist to add comprehensive input validation to the registration form"
```
**Use for**: Input validation, business rules, data integrity

#### architecture-specialist
```
"Use architecture-specialist to design a scalable microservices architecture for this monolith"
```
**Use for**: System design, architecture decisions, patterns

#### localization-specialist
```
"Use localization-specialist to add i18n support for English, Spanish, and French"
```
**Use for**: Internationalization, translation, locale handling

#### compliance-specialist
```
"Use compliance-specialist to make this application GDPR compliant"
```
**Use for**: Regulatory compliance, audit trails, privacy

### Specialized Agents

#### data-science-specialist
```
"Use data-science-specialist to create a customer churn prediction model"
```
**Use for**: ML pipelines, data analysis, model training

## Real-World Examples

### Example 1: New Feature Development

**Scenario**: Building a new user authentication system

```
Step 1: Architecture
"Use architecture-specialist to design a secure, scalable authentication system with JWT tokens"

Step 2: Implementation
"Use scaffolding-specialist to create the authentication module structure"

Step 3: Security
"Use security-specialist to implement secure password hashing and token management"

Step 4: Testing
"Use test-specialist to create comprehensive tests for the authentication flow"

Step 5: Documentation
"Use documentation-specialist to document the authentication API endpoints"
```

### Example 2: Production Optimization

**Scenario**: Optimizing a slow application

```
Step 1: Analysis
"Use performance-specialist to identify bottlenecks in the application"

Step 2: Database
"Use database-specialist to optimize the slow queries identified"

Step 3: Caching
"Use performance-specialist to implement Redis caching for frequently accessed data"

Step 4: Monitoring
"Use observability-specialist to add performance monitoring"
```

### Example 3: Security Hardening

**Scenario**: Preparing for security audit

```
Step 1: Code Audit
"Use security-specialist to perform a comprehensive security audit of the codebase"

Step 2: Fix Vulnerabilities
"Use security-specialist to fix the critical and high-priority issues found"

Step 3: Dependency Security
"Use dependency-specialist to update dependencies with known vulnerabilities"

Step 4: Container Security
"Use docker-specialist to harden the Docker containers following security best practices"

Step 5: Compliance
"Use compliance-specialist to ensure GDPR compliance for user data handling"
```

## Best Practices

### 1. Be Specific in Your Requests
❌ Bad: "Use docker-specialist to help with Docker"
✅ Good: "Use docker-specialist to create a multi-stage Dockerfile for my Python app that minimizes image size and follows security best practices"

### 2. Provide Context
Include relevant information:
- File paths
- Technologies used
- Requirements and constraints
- Expected outcomes

### 3. Use Sequential Tasks for Dependencies
If tasks depend on each other, execute them one at a time:
```
First: "Use scaffolding-specialist to create project structure"
Wait for completion
Then: "Use test-specialist to add tests to the project created"
```

### 4. Use Parallel Tasks for Independent Work
For independent tasks, you can request them together:
```
"Please do these in parallel:
1. Use documentation-specialist to update the README
2. Use test-specialist to add missing tests
3. Use security-specialist to scan for vulnerabilities"
```

### 5. Review Agent Output
Always review what the agent produces before proceeding to the next step.

### 6. Iterative Refinement
You can ask agents to refine their output:
```
"Use docker-specialist to optimize this Dockerfile further for production use"
```

## Troubleshooting

### Agent Not Being Invoked?
- Make sure you're using Claude Code Pro
- Be explicit about which agent you want to use
- Use clear agent names from the registry

### Agent Doesn't Have Enough Context?
- Provide file paths
- Explain the current state
- Describe the desired outcome
- Include relevant constraints

### Need Multiple Agents?
- Execute sequentially if tasks depend on each other
- Consider requesting parallel execution for independent tasks
- Break complex tasks into smaller steps

## Advanced Patterns

### Pattern 1: Iterative Development
```
1. scaffolding-specialist → Create structure
2. frontend-specialist → Build UI
3. test-specialist → Add tests
4. code-review-specialist → Review code
5. refactoring-specialist → Improve based on review
```

### Pattern 2: Quality Pipeline
```
1. code-review-specialist → Initial review
2. security-specialist → Security scan
3. performance-specialist → Performance check
4. test-specialist → Verify coverage
```

### Pattern 3: Deployment Pipeline
```
1. test-specialist → Run all tests
2. security-specialist → Security scan
3. docker-specialist → Create optimized container
4. devops-specialist → Update CI/CD
5. observability-specialist → Add monitoring
```

## Getting Help

If you're unsure which agent to use:
- Check `.claude/agents/AGENTS_REGISTRY.md` for full agent list
- Review agent-specific files in `.claude/agents/` for details
- Start with a general request and Claude Code can suggest the appropriate agent

## Next Steps

1. Browse the agent registry: `.claude/agents/AGENTS_REGISTRY.md`
2. Review individual agent capabilities in `.claude/agents/`
3. Try simple agent invocations with your project
4. Build complex multi-agent workflows
5. Customize agent prompts for your needs

---

Happy building with Claude Code Agents! 🚀
