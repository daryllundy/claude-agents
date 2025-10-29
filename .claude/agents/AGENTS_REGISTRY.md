# Claude Code Agents Registry

This registry contains 22 specialized AI agents that can be invoked as sub-agents within Claude Code Pro.

## How to Use These Agents

These agents are designed to be invoked using natural language within Claude Code Pro. Simply tell Claude Code to "use" a specific agent for your task. Each agent is a specialized sub-agent with specific expertise.

**Important:** You don't need to write code to use these agents. Just use natural language to describe your task and mention which specialist agent you want.

### Invoking an Agent

To invoke an agent, use natural language like:

```
"Use the docker-specialist to create a production-ready Dockerfile for a Python Flask application with the following requirements: Python 3.11, gunicorn, health checks, and multi-stage build for optimization."
```

Claude Code Pro will automatically invoke the docker-specialist sub-agent to handle this task.

## Available Agents

### Infrastructure Agents

#### 1. docker-specialist
- **Category**: Infrastructure
- **Description**: Expert in Docker containerization, Dockerfile optimization, and container orchestration
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Creating Dockerfiles, optimizing containers, multi-stage builds, docker-compose configurations

#### 2. devops-specialist
- **Category**: Infrastructure
- **Description**: CI/CD pipelines, infrastructure as code, automation, and deployment strategies
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Setting up CI/CD, GitHub Actions, GitLab CI, Terraform, Ansible configurations

#### 3. observability-specialist
- **Category**: Infrastructure
- **Description**: Monitoring, logging, alerting, and system observability
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Setting up Prometheus, Grafana, ELK stack, application monitoring

### Development Agents

#### 4. database-specialist
- **Category**: Development
- **Description**: Database design, schema optimization, query performance, and migrations
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Schema design, SQL queries, database migrations, indexing strategies

#### 5. frontend-specialist
- **Category**: Development
- **Description**: Frontend development, UI/UX implementation, React, Vue, Angular
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Component development, state management, responsive design, accessibility

#### 6. mobile-specialist
- **Category**: Development
- **Description**: iOS, Android, React Native, and Flutter development
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Mobile app development, native features, cross-platform solutions

### Quality Agents

#### 7. test-specialist
- **Category**: Quality
- **Description**: Comprehensive test suite generation, unit tests, integration tests
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Writing tests, test coverage, TDD, testing strategies

#### 8. security-specialist
- **Category**: Quality
- **Description**: Security auditing, vulnerability scanning, secure coding practices
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Security reviews, vulnerability fixes, secure authentication

#### 9. code-review-specialist
- **Category**: Quality
- **Description**: Automated code review, best practices, code quality analysis
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Code reviews, identifying issues, suggesting improvements

#### 10. refactoring-specialist
- **Category**: Quality
- **Description**: Code refactoring, modernization, technical debt reduction
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Refactoring code, improving structure, removing duplication

#### 11. performance-specialist
- **Category**: Quality
- **Description**: Performance optimization, profiling, bottleneck identification
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Performance analysis, optimization, caching strategies

### Operations Agents

#### 12. migration-specialist
- **Category**: Operations
- **Description**: Database migrations, code migrations, version upgrades
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Migrating databases, upgrading frameworks, data transformations

#### 13. dependency-specialist
- **Category**: Operations
- **Description**: Dependency management, updates, security patches
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Managing dependencies, resolving conflicts, security updates

#### 14. git-specialist
- **Category**: Operations
- **Description**: Git workflow, branching strategies, repository management
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Git operations, merge conflicts, repository organization

### Productivity Agents

#### 15. scaffolding-specialist
- **Category**: Productivity
- **Description**: Project scaffolding, boilerplate generation, project setup
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Creating new projects, generating boilerplate, project structure

#### 16. documentation-specialist
- **Category**: Productivity
- **Description**: Automated documentation generation, API docs, README files
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Generating documentation, writing guides, API documentation

#### 17. debugging-specialist
- **Category**: Productivity
- **Description**: Bug detection, debugging assistance, error resolution
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Finding bugs, debugging issues, error analysis

### Business Agents

#### 18. validation-specialist
- **Category**: Business
- **Description**: Input validation, business rule implementation, data validation
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Adding validation, business logic, data integrity

#### 19. architecture-specialist
- **Category**: Business
- **Description**: System architecture, design patterns, architectural decisions
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Architecture design, pattern selection, system design

#### 20. localization-specialist
- **Category**: Business
- **Description**: Internationalization, localization, multi-language support
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: i18n setup, translation management, locale handling

#### 21. compliance-specialist
- **Category**: Business
- **Description**: Regulatory compliance (GDPR, HIPAA, SOC2), audit trails
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Compliance requirements, audit logging, privacy features

### Specialized Agents

#### 22. data-science-specialist
- **Category**: Specialized
- **Description**: ML pipelines, data analysis, visualization, model training
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Data analysis, ML models, data visualization, pipelines

## Agent Invocation Patterns

### Single Agent Task

Simply ask Claude Code to use a specific agent for your task:

```
"Use the security-specialist to perform a comprehensive security audit of the authentication system in the codebase. Check for SQL injection, XSS, CSRF, and authentication vulnerabilities."
```

### Sequential Agent Tasks

For tasks that need to happen in sequence, describe them naturally and Claude Code will handle them in order:

```
"First, use the scaffolding-specialist to create a new FastAPI project structure with best practices. Then, use the test-specialist to create comprehensive tests for the FastAPI project that was just created."
```

Alternatively, you can ask for each task separately after the previous one completes.

### Parallel Agent Tasks

For independent tasks that can run in parallel, describe them together:

```
"Use the documentation-specialist to generate OpenAPI documentation for all API endpoints, and also use the test-specialist to create integration tests for all API endpoints."
```

Claude Code Pro will intelligently handle running these agents as appropriate for your workflow.

## Best Practices

1. **Be Specific**: Provide detailed context and requirements in the prompt
2. **Single Responsibility**: Each agent invocation should focus on one specific task
3. **Provide Context**: Include relevant file paths, technologies, and constraints
4. **Sequential Dependencies**: If tasks depend on each other, run them sequentially
5. **Review Output**: Always review agent output before proceeding to the next step

## Agent Selection Guide

| Task | Recommended Agent |
|------|------------------|
| Create Dockerfile | docker-specialist |
| Setup CI/CD | devops-specialist |
| Add monitoring | observability-specialist |
| Design database schema | database-specialist |
| Build React component | frontend-specialist |
| Create mobile app | mobile-specialist |
| Write tests | test-specialist |
| Security review | security-specialist |
| Code review | code-review-specialist |
| Refactor code | refactoring-specialist |
| Optimize performance | performance-specialist |
| Database migration | migration-specialist |
| Update dependencies | dependency-specialist |
| Git workflow | git-specialist |
| Generate boilerplate | scaffolding-specialist |
| Write documentation | documentation-specialist |
| Debug issues | debugging-specialist |
| Add validation | validation-specialist |
| System architecture | architecture-specialist |
| Add i18n | localization-specialist |
| GDPR compliance | compliance-specialist |
| ML pipeline | data-science-specialist |
