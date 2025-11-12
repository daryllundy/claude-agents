# Claude Code Agents Registry

This registry contains 30 specialized AI agents that can be invoked as sub-agents within Claude Code Pro.

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

#### 1. devops-orchestrator
- **Category**: Infrastructure (Orchestration)
- **Description**: Coordinates DevOps specialists for complex infrastructure projects, multi-cloud deployments, and end-to-end infrastructure workflows
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Multi-specialist DevOps workflows, infrastructure planning, deployment coordination, orchestrating cloud + IaC + monitoring specialists

#### 2. aws-specialist
- **Category**: Infrastructure (Cloud)
- **Description**: AWS cloud services, architecture, CloudFormation, CDK, and AWS Well-Architected Framework
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: AWS infrastructure, EC2, ECS, EKS, Lambda, RDS, S3, CloudWatch, IAM, VPC, cost optimization

#### 3. azure-specialist
- **Category**: Infrastructure (Cloud)
- **Description**: Azure cloud services, ARM templates, Bicep, and Azure best practices
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Azure infrastructure, VMs, App Service, Functions, AKS, SQL Database, Blob Storage, Azure Monitor, RBAC

#### 4. gcp-specialist
- **Category**: Infrastructure (Cloud)
- **Description**: Google Cloud Platform services, Deployment Manager, and GCP architecture patterns
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: GCP infrastructure, Compute Engine, Cloud Run, GKE, Cloud SQL, Cloud Storage, Cloud Monitoring, IAM

#### 5. terraform-specialist
- **Category**: Infrastructure (IaC)
- **Description**: Terraform configuration, modules, state management, and multi-cloud provisioning
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Terraform modules, state management, multi-cloud IaC, provider configuration, Terraform Cloud/Enterprise

#### 6. ansible-specialist
- **Category**: Infrastructure (IaC)
- **Description**: Ansible playbooks, roles, inventory management, and configuration automation
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Ansible playbooks, role development, configuration management, dynamic inventory, Ansible Vault

#### 7. cicd-specialist
- **Category**: Infrastructure (Platform)
- **Description**: CI/CD pipelines for GitHub Actions, GitLab CI, Jenkins, CircleCI, and Azure DevOps
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Pipeline configuration, build automation, deployment strategies, artifact management, security scanning in CI/CD

#### 8. kubernetes-specialist
- **Category**: Infrastructure (Platform)
- **Description**: Kubernetes orchestration, Helm charts, service mesh, and cloud-native patterns
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Kubernetes manifests, Helm charts, deployments, services, ingress, ConfigMaps, Secrets, RBAC, auto-scaling

#### 9. monitoring-specialist
- **Category**: Infrastructure (Platform)
- **Description**: Observability strategy, Prometheus, Grafana, ELK stack, distributed tracing, and alerting
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Monitoring setup, dashboard design, alerting strategies, SLO/SLI definitions, log aggregation, distributed tracing

#### 10. docker-specialist
- **Category**: Infrastructure
- **Description**: Expert in Docker containerization, Dockerfile optimization, and container orchestration
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Creating Dockerfiles, optimizing containers, multi-stage builds, docker-compose configurations

#### 11. observability-specialist
- **Category**: Infrastructure
- **Description**: Monitoring, logging, alerting, and system observability implementation
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Setting up Prometheus, Grafana, ELK stack, application monitoring, instrumentation

### Development Agents

#### 12. database-specialist
- **Category**: Development
- **Description**: Database design, schema optimization, query performance, and migrations
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Schema design, SQL queries, database migrations, indexing strategies

#### 13. frontend-specialist
- **Category**: Development
- **Description**: Frontend development, UI/UX implementation, React, Vue, Angular
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Component development, state management, responsive design, accessibility

#### 14. mobile-specialist
- **Category**: Development
- **Description**: iOS, Android, React Native, and Flutter development
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Mobile app development, native features, cross-platform solutions

### Quality Agents

#### 15. test-specialist
- **Category**: Quality
- **Description**: Comprehensive test suite generation, unit tests, integration tests
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Writing tests, test coverage, TDD, testing strategies

#### 16. security-specialist
- **Category**: Quality
- **Description**: Security auditing, vulnerability scanning, secure coding practices
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Security reviews, vulnerability fixes, secure authentication

#### 17. code-review-specialist
- **Category**: Quality
- **Description**: Automated code review, best practices, code quality analysis
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Code reviews, identifying issues, suggesting improvements

#### 18. refactoring-specialist
- **Category**: Quality
- **Description**: Code refactoring, modernization, technical debt reduction
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Refactoring code, improving structure, removing duplication

#### 19. performance-specialist
- **Category**: Quality
- **Description**: Performance optimization, profiling, bottleneck identification
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Performance analysis, optimization, caching strategies

### Operations Agents

#### 20. migration-specialist
- **Category**: Operations
- **Description**: Database migrations, code migrations, version upgrades
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Migrating databases, upgrading frameworks, data transformations

#### 21. dependency-specialist
- **Category**: Operations
- **Description**: Dependency management, updates, security patches
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Managing dependencies, resolving conflicts, security updates

#### 22. git-specialist
- **Category**: Operations
- **Description**: Git workflow, branching strategies, repository management
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Git operations, merge conflicts, repository organization

### Productivity Agents

#### 23. scaffolding-specialist
- **Category**: Productivity
- **Description**: Project scaffolding, boilerplate generation, project setup
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Creating new projects, generating boilerplate, project structure

#### 24. documentation-specialist
- **Category**: Productivity
- **Description**: Automated documentation generation, API docs, README files
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Generating documentation, writing guides, API documentation

#### 25. debugging-specialist
- **Category**: Productivity
- **Description**: Bug detection, debugging assistance, error resolution
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Finding bugs, debugging issues, error analysis

### Business Agents

#### 26. validation-specialist
- **Category**: Business
- **Description**: Input validation, business rule implementation, data validation
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Adding validation, business logic, data integrity

#### 27. architecture-specialist
- **Category**: Business
- **Description**: System architecture, design patterns, architectural decisions
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Architecture design, pattern selection, system design

#### 28. localization-specialist
- **Category**: Business
- **Description**: Internationalization, localization, multi-language support
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: i18n setup, translation management, locale handling

#### 29. compliance-specialist
- **Category**: Business
- **Description**: Regulatory compliance (GDPR, HIPAA, SOC2), audit trails
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Compliance requirements, audit logging, privacy features

### Specialized Agents

#### 30. data-science-specialist
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

### DevOps Orchestration

The devops-orchestrator coordinates multiple DevOps specialists for complex infrastructure workflows:

```
"Use the devops-orchestrator to set up a complete AWS infrastructure with Terraform, including EKS cluster, RDS database, and comprehensive monitoring with Prometheus and Grafana."
```

The orchestrator will automatically delegate to aws-specialist, terraform-specialist, kubernetes-specialist, and monitoring-specialist as needed.

### Cloud-Specific Tasks

For cloud provider-specific work, use the dedicated cloud specialists:

```
"Use the aws-specialist to design a highly available architecture for a web application using EC2, ALB, RDS Multi-AZ, and S3 with CloudFront. Include IAM roles following least privilege principle."

"Use the azure-specialist to create ARM templates for a microservices architecture using AKS, Azure SQL Database, and Azure Monitor with Application Insights."

"Use the gcp-specialist to set up a Cloud Run service with Cloud SQL, Cloud Storage, and Cloud Monitoring. Include IAM policies and VPC configuration."
```

### Infrastructure as Code

For IaC tasks, use terraform-specialist or ansible-specialist:

```
"Use the terraform-specialist to create reusable Terraform modules for a multi-cloud deployment supporting AWS, Azure, and GCP. Include remote state configuration with S3 backend."

"Use the ansible-specialist to create Ansible playbooks for configuring web servers with Nginx, SSL certificates, and automated security updates. Include dynamic inventory for AWS EC2 instances."
```

### CI/CD and Kubernetes

For pipeline and container orchestration tasks:

```
"Use the cicd-specialist to create a GitHub Actions workflow with build caching, parallel test execution, security scanning with Trivy, and automated deployment to staging and production environments."

"Use the kubernetes-specialist to create Helm charts for a microservices application with proper resource limits, health checks, HPA configuration, and network policies for security."
```

## Best Practices

1. **Be Specific**: Provide detailed context and requirements in the prompt
2. **Single Responsibility**: Each agent invocation should focus on one specific task
3. **Provide Context**: Include relevant file paths, technologies, and constraints
4. **Sequential Dependencies**: If tasks depend on each other, run them sequentially
5. **Review Output**: Always review agent output before proceeding to the next step

## Agent Selection Guide

| Task | Recommended Agent |
|------|------------------|
| **Infrastructure & DevOps** |
| Multi-cloud infrastructure project | devops-orchestrator |
| AWS infrastructure | aws-specialist |
| Azure infrastructure | azure-specialist |
| GCP infrastructure | gcp-specialist |
| Terraform modules | terraform-specialist |
| Ansible playbooks | ansible-specialist |
| CI/CD pipelines | cicd-specialist |
| Kubernetes deployment | kubernetes-specialist |
| Monitoring & alerting strategy | monitoring-specialist |
| Create Dockerfile | docker-specialist |
| Observability implementation | observability-specialist |
| **Development** |
| Design database schema | database-specialist |
| Build React component | frontend-specialist |
| Create mobile app | mobile-specialist |
| **Quality** |
| Write tests | test-specialist |
| Security review | security-specialist |
| Code review | code-review-specialist |
| Refactor code | refactoring-specialist |
| Optimize performance | performance-specialist |
| **Operations** |
| Database migration | migration-specialist |
| Update dependencies | dependency-specialist |
| Git workflow | git-specialist |
| **Productivity** |
| Generate boilerplate | scaffolding-specialist |
| Write documentation | documentation-specialist |
| Debug issues | debugging-specialist |
| **Business** |
| Add validation | validation-specialist |
| System architecture | architecture-specialist |
| Add i18n | localization-specialist |
| GDPR compliance | compliance-specialist |
| **Specialized** |
| ML pipeline | data-science-specialist |
