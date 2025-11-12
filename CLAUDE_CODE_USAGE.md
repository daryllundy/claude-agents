# Using Claude Code Agents with Claude Code Pro

This guide shows you how to use the 31 specialized agents as sub-agents within Claude Code Pro.

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

### Orchestration Agents

#### devops-orchestrator
```
"Use devops-orchestrator to coordinate a full infrastructure setup with AWS, Terraform, and monitoring"
```
**Use for**: Multi-specialist DevOps workflows, infrastructure planning, deployment coordination

#### e-commerce-coordinator
```
"Use e-commerce-coordinator to audit and transform my Shopify store"
```
**Use for**: E-commerce projects, multi-specialist coordination, business transformation

## DevOps Orchestration Workflows

The DevOps Orchestrator coordinates multiple specialized agents to handle complex infrastructure and deployment scenarios. It intelligently delegates tasks to cloud provider specialists (AWS, Azure, GCP), infrastructure as code specialists (Terraform, Ansible), platform specialists (CI/CD, Kubernetes, Monitoring), and integrates with existing agents (Docker, Security, Observability).

### When to Use the Orchestrator vs Direct Specialist Invocation

**Use the DevOps Orchestrator when:**
- You need multiple DevOps specialists working together
- You're setting up complete infrastructure from scratch
- You need guidance on which specialists to use and in what order
- You want pre-defined workflow patterns for common scenarios
- You need context maintained across multiple specialist invocations

**Use Direct Specialist Invocation when:**
- You know exactly which specialist you need
- You're making a focused change to one area
- You're working within a single domain (e.g., only AWS, only Kubernetes)
- You want maximum control over the sequence of operations

### Specialist Coordination Patterns

The orchestrator uses several patterns to coordinate specialists:

**Sequential Pattern**: Tasks with dependencies execute in order
```
Cloud Specialist → IaC Specialist → Monitoring Specialist
```

**Parallel Pattern**: Independent tasks execute simultaneously
```
AWS Specialist + Azure Specialist (for multi-cloud)
```

**Iterative Pattern**: Refinement across multiple specialists
```
Terraform Specialist → Review → Terraform Specialist (refinement)
```

**Integration Pattern**: Combining outputs from multiple specialists
```
Kubernetes Specialist + CI/CD Specialist → Unified deployment pipeline
```

### Example 1: Full Infrastructure Setup

**Scenario**: Setting up complete AWS infrastructure with IaC and monitoring

```
"Use devops-orchestrator to set up a production-ready AWS infrastructure for a Node.js application with:
- VPC, subnets, and security groups
- ECS cluster for container orchestration
- RDS PostgreSQL database
- S3 for static assets
- CloudWatch monitoring
- Everything codified in Terraform
- CI/CD pipeline for deployments"

The orchestrator will coordinate:

Week 1: AWS Specialist
- Design VPC architecture with public/private subnets
- Configure security groups and IAM roles
- Set up ECS cluster and RDS instance
- Configure S3 buckets with proper policies

Week 2: Terraform Specialist
- Convert AWS infrastructure to Terraform modules
- Set up remote state in S3 with DynamoDB locking
- Create reusable modules for VPC, ECS, RDS
- Implement proper variable management

Week 3: Monitoring Specialist
- Configure CloudWatch dashboards
- Set up log aggregation from ECS tasks
- Create alerting rules for critical metrics
- Implement distributed tracing

Week 4: CI/CD Specialist
- Create GitHub Actions pipeline
- Implement build and test stages
- Add Docker image building and pushing to ECR
- Configure automated ECS deployments
- Add security scanning and compliance checks
```

### Example 2: Kubernetes Deployment Pipeline

**Scenario**: Setting up a complete Kubernetes deployment pipeline with monitoring

```
"Use devops-orchestrator to create a Kubernetes deployment pipeline for my microservices application with:
- GKE cluster setup
- Helm charts for all services
- CI/CD pipeline with automated deployments
- Prometheus and Grafana monitoring
- Auto-scaling configuration"

The orchestrator will coordinate:

Phase 1: Kubernetes Specialist
- Design GKE cluster architecture
- Create namespace structure
- Configure RBAC and service accounts
- Set up Ingress with TLS
- Create Helm charts for each microservice
- Configure ConfigMaps and Secrets management
- Set up HPA (Horizontal Pod Autoscaler)

Phase 2: CI/CD Specialist
- Create GitLab CI pipeline
- Implement build stage with Docker image creation
- Add automated testing (unit, integration)
- Configure Helm deployment to GKE
- Implement blue-green deployment strategy
- Add rollback capabilities
- Configure environment-specific deployments (dev, staging, prod)

Phase 3: Monitoring Specialist
- Deploy Prometheus operator to cluster
- Configure ServiceMonitors for all microservices
- Create Grafana dashboards for:
  - Cluster health and resource usage
  - Application metrics and SLIs
  - Request rates and error rates
- Set up alerting rules for:
  - Pod failures and restarts
  - High resource usage
  - Application errors
- Configure distributed tracing with Jaeger

Phase 4: Integration (Orchestrator)
- Verify end-to-end deployment flow
- Test monitoring and alerting
- Document deployment procedures
- Create runbooks for common operations
```

### Example 3: Multi-Cloud Migration

**Scenario**: Migrating infrastructure from AWS to a multi-cloud setup (AWS + Azure)

```
"Use devops-orchestrator to migrate our application to a multi-cloud architecture:
- Keep primary infrastructure on AWS
- Add Azure as secondary region for disaster recovery
- Use Terraform for all infrastructure
- Maintain unified monitoring across both clouds
- Set up cross-cloud networking"

The orchestrator will coordinate:

Phase 1: Terraform Specialist
- Audit existing AWS infrastructure
- Design multi-cloud Terraform structure
- Create provider configurations for AWS and Azure
- Set up Terraform workspaces for each cloud
- Design module structure for reusability
- Plan state management strategy

Phase 2: AWS Specialist
- Review and optimize existing AWS infrastructure
- Prepare for Terraform import
- Design cross-region connectivity
- Configure AWS Transit Gateway
- Set up VPC peering for multi-region

Phase 3: Azure Specialist
- Design equivalent Azure architecture
- Create Azure Virtual Network
- Set up Azure VPN Gateway for AWS connectivity
- Configure Azure resources (VMs, App Service, SQL Database)
- Implement Azure-specific security (Azure AD, Key Vault)

Phase 4: Terraform Specialist (Implementation)
- Import existing AWS resources to Terraform
- Create Terraform modules for AWS infrastructure
- Implement Azure infrastructure in Terraform
- Set up cross-cloud networking in code
- Configure remote state with locking
- Implement CI/CD for infrastructure changes

Phase 5: Monitoring Specialist
- Deploy unified monitoring solution
- Configure Prometheus federation across clouds
- Set up centralized Grafana instance
- Create cross-cloud dashboards
- Implement alerting for both environments
- Configure log aggregation from both clouds

Phase 6: CI/CD Specialist
- Update deployment pipelines for multi-cloud
- Implement traffic routing logic
- Configure health checks and failover
- Add deployment verification tests
- Create disaster recovery automation
```

### Example 4: Container Migration to Kubernetes

**Scenario**: Migrating Docker Compose application to Kubernetes

```
"Use devops-orchestrator to migrate our Docker Compose application to Kubernetes on AWS EKS with proper CI/CD"

The orchestrator will coordinate:

Phase 1: Docker Specialist + Kubernetes Specialist
- Docker Specialist: Review and optimize existing Dockerfiles
- Docker Specialist: Implement multi-stage builds
- Kubernetes Specialist: Convert docker-compose.yml to K8s manifests
- Kubernetes Specialist: Create Helm chart structure

Phase 2: AWS Specialist + Kubernetes Specialist
- AWS Specialist: Provision EKS cluster with Terraform
- AWS Specialist: Set up ECR for container registry
- AWS Specialist: Configure VPC and security groups
- Kubernetes Specialist: Configure cluster networking and storage

Phase 3: CI/CD Specialist
- Create GitHub Actions workflow
- Implement Docker build and push to ECR
- Add Helm deployment to EKS
- Configure automated testing
- Implement deployment strategies

Phase 4: Monitoring Specialist
- Deploy monitoring stack to cluster
- Configure application metrics collection
- Set up log aggregation
- Create dashboards and alerts
```

### Example 5: Infrastructure as Code Adoption

**Scenario**: Converting manually created infrastructure to Terraform

```
"Use devops-orchestrator to convert our manually created AWS infrastructure to Terraform"

The orchestrator will coordinate:

Phase 1: AWS Specialist
- Audit existing AWS resources
- Document current architecture
- Identify dependencies between resources
- Create architecture diagrams

Phase 2: Terraform Specialist
- Design Terraform module structure
- Set up remote state backend
- Create import plan for existing resources
- Import resources into Terraform state
- Generate Terraform configurations
- Refactor into reusable modules

Phase 3: CI/CD Specialist
- Create Terraform CI/CD pipeline
- Implement terraform plan on pull requests
- Configure terraform apply on merge
- Add state locking and backup
- Implement drift detection

Phase 4: Monitoring Specialist
- Add infrastructure monitoring
- Track Terraform state changes
- Alert on configuration drift
```

### Orchestrator Decision Framework

The DevOps Orchestrator uses this framework to select specialists:

**Cloud Provider Selection:**
- AWS mentioned → aws-specialist
- Azure mentioned → azure-specialist
- GCP/Google Cloud mentioned → gcp-specialist
- Multi-cloud → Multiple cloud specialists

**Infrastructure as Code:**
- Terraform mentioned → terraform-specialist
- Ansible/Configuration management → ansible-specialist
- CloudFormation → aws-specialist
- ARM templates/Bicep → azure-specialist

**Container & Orchestration:**
- Docker/Dockerfile → docker-specialist
- Kubernetes/K8s/Helm → kubernetes-specialist
- ECS/EKS → aws-specialist + kubernetes-specialist

**CI/CD & Automation:**
- Pipeline/CI/CD → cicd-specialist
- GitHub Actions/GitLab CI/Jenkins → cicd-specialist

**Observability:**
- Monitoring/Metrics/Logs → monitoring-specialist
- Prometheus/Grafana → monitoring-specialist
- Distributed tracing → monitoring-specialist

**Cross-Cutting Concerns:**
- Security → security-specialist
- Performance → performance-specialist
- Documentation → documentation-specialist

### Tips for Working with the Orchestrator

1. **Be Clear About Your Goal**: Describe the end state you want, not just the first step
2. **Mention All Technologies**: List all cloud providers, tools, and platforms involved
3. **Specify Constraints**: Budget, timeline, compliance requirements, existing infrastructure
4. **Ask for Workflow Planning**: Request a phased approach for complex projects
5. **Review Each Phase**: Approve each phase before moving to the next
6. **Iterate as Needed**: The orchestrator can adjust the plan based on your feedback

### Example Orchestrator Invocations

**Simple Coordination:**
```
"Use devops-orchestrator to set up AWS infrastructure with Terraform and monitoring"
```

**Complex Multi-Phase:**
```
"Use devops-orchestrator to plan and execute a migration from Heroku to AWS EKS with:
- Containerized microservices
- PostgreSQL on RDS
- Redis on ElastiCache
- CI/CD with GitHub Actions
- Full observability stack
- Zero-downtime migration"
```

**Workflow Planning:**
```
"Use devops-orchestrator to create a 4-week plan for implementing infrastructure as code for our existing Azure resources"
```

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

## Agent Recommendation Script

The repository includes a powerful agent recommendation script that automatically detects your project's technologies and recommends relevant agents.

### Basic Usage

```bash
# Run from your project root
curl -sSL https://raw.githubusercontent.com/daryllundy/claude-agents/main/scripts/recommend_agents.sh | bash

# Or clone the repo and run locally
bash scripts/recommend_agents.sh
```

### Network Operations & Reliability

The script includes robust network handling:

**Automatic Retry**:
- 3 retry attempts per download
- Exponential backoff (1s, 2s, 4s)
- 30-second timeout per attempt
- Detailed error diagnostics

**Intelligent Caching**:
- Downloads cached for 24 hours
- Reduces network requests
- Supports offline workflows
- Cache location: `~/.cache/claude-agents`

### Cache Control

```bash
# Force fresh download (bypass cache)
bash scripts/recommend_agents.sh --force-refresh

# Clear all cached files
bash scripts/recommend_agents.sh --clear-cache

# Custom cache directory
bash scripts/recommend_agents.sh --cache-dir=/tmp/my-cache

# Custom cache expiry (in seconds)
bash scripts/recommend_agents.sh --cache-expiry=3600  # 1 hour
bash scripts/recommend_agents.sh --cache-expiry=604800  # 1 week
```

### Offline Workflow

```bash
# First run (online) - downloads and caches
bash scripts/recommend_agents.sh

# Subsequent runs - uses cache (instant, works offline)
bash scripts/recommend_agents.sh

# Force refresh when back online
bash scripts/recommend_agents.sh --force-refresh
```

### Update Management

```bash
# Check for agent updates
bash scripts/recommend_agents.sh --check-updates

# Update all agents (with automatic backup)
bash scripts/recommend_agents.sh --update-all
```

### Advanced Features

```bash
# Interactive selection mode
bash scripts/recommend_agents.sh --interactive

# Export profile for sharing
bash scripts/recommend_agents.sh --export my-project.json

# Import profile in another project
bash scripts/recommend_agents.sh --import my-project.json

# Verbose output with detailed logging
bash scripts/recommend_agents.sh --verbose

# Adjust confidence threshold
bash scripts/recommend_agents.sh --min-confidence 50

# Dry run (see recommendations without downloading)
bash scripts/recommend_agents.sh --dry-run
```

For comprehensive documentation on network operations, caching, and troubleshooting, see [docs/NETWORK_OPERATIONS.md](docs/NETWORK_OPERATIONS.md).

## Getting Help

If you're unsure which agent to use:
- Check `.claude/agents/AGENTS_REGISTRY.md` for full agent list
- Review agent-specific files in `.claude/agents/` for details
- Start with a general request and Claude Code can suggest the appropriate agent
- Use the recommendation script to auto-detect relevant agents

## Documentation

- **[README.md](README.md)** - Overview and quick reference
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Beginner's guide
- **[docs/NETWORK_OPERATIONS.md](docs/NETWORK_OPERATIONS.md)** - Network operations and caching
- **[.claude/agents/AGENTS_REGISTRY.md](.claude/agents/AGENTS_REGISTRY.md)** - Complete agent catalog

## Next Steps

1. Browse the agent registry: `.claude/agents/AGENTS_REGISTRY.md`
2. Review individual agent capabilities in `.claude/agents/`
3. Try the recommendation script on your project
4. Try simple agent invocations with your project
5. Build complex multi-agent workflows
6. Customize agent prompts for your needs

---

Happy building with Claude Code Agents! 🚀
