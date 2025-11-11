# Design Document

## Overview

This design transforms the monolithic DevOps specialist agent into a modular orchestration system consisting of one orchestrator agent and seven specialized sub-agents. The DevOps Orchestrator will intelligently delegate tasks to domain-specific agents (AWS, Azure, GCP, Terraform, Ansible, CI/CD, Kubernetes, and Monitoring specialists), similar to how the e-commerce-coordinator orchestrates e-commerce specialists.

The design follows the established patterns in the repository while introducing clear separation of concerns across the DevOps landscape. Each sub-agent will have deep expertise in its domain, while the orchestrator maintains the big picture and coordinates multi-agent workflows.

## Architecture

### Agent Hierarchy

```
DevOps Orchestrator (Coordinator)
├── Cloud Provider Agents
│   ├── AWS Specialist
│   ├── Azure Specialist
│   └── GCP Specialist
├── Infrastructure as Code Agents
│   ├── Terraform Specialist
│   └── Ansible Specialist
├── Platform Agents
│   ├── CI/CD Specialist
│   ├── Kubernetes Specialist
│   └── Monitoring Specialist
```

### Orchestration Model

The DevOps Orchestrator follows a delegation pattern:

1. **Request Analysis**: Analyzes user requests to identify required domains
2. **Agent Selection**: Determines which specialist(s) to invoke
3. **Workflow Coordination**: Sequences multi-agent tasks with proper dependencies
4. **Context Management**: Maintains state across specialist invocations
5. **Results Synthesis**: Combines outputs from multiple specialists into cohesive solutions

### Integration with Existing System

- All agents follow the existing markdown format in `.claude/agents/`
- Agents are registered in `AGENTS_REGISTRY.md` with proper categorization
- The orchestrator references existing agents (docker-specialist, observability-specialist, security-specialist) when appropriate
- Maintains consistency with the e-commerce-coordinator orchestration patterns

## Components and Interfaces

### 1. DevOps Orchestrator Agent

**File**: `.claude/agents/devops-orchestrator.md`

**Responsibilities**:
- Analyze DevOps requests and identify required specialists
- Coordinate multi-specialist workflows (e.g., cloud + IaC + monitoring)
- Provide pre-defined workflow patterns for common scenarios
- Maintain context across specialist invocations
- Synthesize results from multiple specialists
- Handle cross-cutting concerns (security, cost optimization, best practices)

**Key Capabilities**:
- Workflow patterns for common scenarios:
  - Full infrastructure setup (cloud + IaC + monitoring)
  - Deployment pipeline (CI/CD + Kubernetes + monitoring)
  - Multi-cloud deployment (multiple cloud specialists + IaC)
  - Migration projects (cloud + IaC + CI/CD)
- Specialist selection logic based on request analysis
- Progress tracking for multi-phase projects
- Integration point recommendations

**Tool Access**: Read, Write, Edit, Bash, Glob, Grep

### 2. AWS Specialist Agent

**File**: `.claude/agents/aws-specialist.md`

**Responsibilities**:
- AWS service expertise (EC2, ECS, EKS, Lambda, RDS, S3, CloudWatch, etc.)
- AWS Well-Architected Framework guidance
- CloudFormation and AWS CDK
- AWS-specific security (IAM, Security Groups, KMS, Secrets Manager)
- Cost optimization for AWS services
- AWS CLI and SDK patterns

**Key Capabilities**:
- Service selection and architecture design
- Infrastructure provisioning with CloudFormation/CDK
- Security best practices (least privilege IAM, VPC design)
- Cost optimization recommendations
- Multi-region deployments
- Disaster recovery and backup strategies

**Tool Access**: Read, Write, Edit, Bash, Glob, Grep

### 3. Azure Specialist Agent

**File**: `.claude/agents/azure-specialist.md`

**Responsibilities**:
- Azure service expertise (VMs, App Service, Functions, AKS, SQL Database, etc.)
- ARM templates and Bicep
- Azure-specific security (Azure AD, RBAC, Key Vault)
- Cost optimization for Azure services
- Azure CLI and PowerShell patterns

**Key Capabilities**:
- Service selection and architecture design
- Infrastructure provisioning with ARM/Bicep
- Azure AD and identity management
- Cost management and optimization
- Hybrid cloud scenarios
- Azure DevOps integration

**Tool Access**: Read, Write, Edit, Bash, Glob, Grep

### 4. GCP Specialist Agent

**File**: `.claude/agents/gcp-specialist.md`

**Responsibilities**:
- GCP service expertise (Compute Engine, Cloud Run, GKE, Cloud SQL, etc.)
- Deployment Manager and Terraform for GCP
- GCP-specific security (IAM, VPC, Secret Manager)
- Cost optimization for GCP services
- gcloud CLI patterns

**Key Capabilities**:
- Service selection and architecture design
- Infrastructure provisioning with Deployment Manager
- GCP IAM and organization policies
- Cost optimization and committed use discounts
- Multi-region deployments
- GCP-specific networking (VPC, Cloud Load Balancing)

**Tool Access**: Read, Write, Edit, Bash, Glob, Grep

### 5. Terraform Specialist Agent

**File**: `.claude/agents/terraform-specialist.md`

**Responsibilities**:
- Terraform configuration and best practices
- Module development and reusability
- State management (local, remote, workspaces)
- Multi-cloud provisioning
- Terraform workflow (plan, apply, destroy)

**Key Capabilities**:
- Module structure and organization
- Variable and output management
- Remote state configuration (S3, Azure Storage, GCS)
- Provider configuration for multiple clouds
- Terraform Cloud/Enterprise patterns
- Import existing infrastructure
- Refactoring and module extraction

**Tool Access**: Read, Write, Edit, Bash, Glob, Grep

### 6. Ansible Specialist Agent

**File**: `.claude/agents/ansible-specialist.md`

**Responsibilities**:
- Ansible playbook development
- Role creation and organization
- Inventory management (static, dynamic)
- Configuration management best practices
- Ansible Vault for secrets

**Key Capabilities**:
- Playbook structure and organization
- Role development with proper defaults
- Variable precedence and management
- Idempotent task design
- Dynamic inventory for cloud providers
- Ansible Galaxy integration
- Testing with Molecule

**Tool Access**: Read, Write, Edit, Bash, Glob, Grep

### 7. CI/CD Specialist Agent

**File**: `.claude/agents/cicd-specialist.md`

**Responsibilities**:
- CI/CD pipeline design and implementation
- Platform-specific expertise (GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure DevOps)
- Build automation and optimization
- Deployment strategies (blue-green, canary, rolling)
- Artifact management and caching

**Key Capabilities**:
- Pipeline configuration for multiple platforms
- Build optimization (caching, parallelization)
- Testing integration (unit, integration, e2e)
- Security scanning in pipelines
- Deployment automation
- Pipeline as code best practices
- Secrets management in CI/CD

**Tool Access**: Read, Write, Edit, Bash, Glob, Grep

### 8. Kubernetes Specialist Agent

**File**: `.claude/agents/kubernetes-specialist.md`

**Responsibilities**:
- Kubernetes resource management (Deployments, Services, Ingress, etc.)
- Helm chart development and management
- Cluster configuration and optimization
- Service mesh implementation (Istio, Linkerd)
- Auto-scaling and resource management

**Key Capabilities**:
- Manifest creation and organization
- Helm chart structure and templating
- ConfigMap and Secret management
- RBAC configuration
- Network policies and security
- Resource requests and limits
- HPA and VPA configuration
- StatefulSet and persistent storage

**Tool Access**: Read, Write, Edit, Bash, Glob, Grep

### 9. Monitoring Specialist Agent

**File**: `.claude/agents/monitoring-specialist.md`

**Responsibilities**:
- Observability strategy and implementation
- Metrics collection and visualization (Prometheus, Grafana)
- Log aggregation and analysis (ELK, Loki)
- Distributed tracing (Jaeger, Zipkin)
- Alerting and incident response

**Key Capabilities**:
- Monitoring stack setup and configuration
- Dashboard design and creation
- Alert rule definition and tuning
- SLO/SLI definition and tracking
- Log parsing and analysis
- Distributed tracing implementation
- On-call and incident response workflows

**Tool Access**: Read, Write, Edit, Bash, Glob, Grep

## Data Models

### Agent Metadata Structure

Each agent file follows this structure:

```markdown
# [Agent Name]

You are a [domain] specialist with deep expertise in [specific areas].

## Your Expertise

### [Domain Area 1]
- [Specific capability]
- [Specific capability]

### [Domain Area 2]
- [Specific capability]
- [Specific capability]

## Task Approach

When given a task:
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output Format

Provide:
- [Expected output 1]
- [Expected output 2]

## Example Tasks You Handle

- "[Example task 1]"
- "[Example task 2]"

## MCP Code Execution

[MCP patterns specific to this domain]

## Best Practices

- [Best practice 1]
- [Best practice 2]
```

### Orchestrator Workflow Patterns

The orchestrator maintains pre-defined workflow patterns:

```markdown
## Common Workflow Patterns

### Pattern 1: Full Infrastructure Setup
Week 1: [Cloud Specialist] - Provision core infrastructure
Week 2: [Terraform Specialist] - Codify infrastructure
Week 3: [Monitoring Specialist] - Set up observability
Week 4: [CI/CD Specialist] - Implement deployment pipeline

### Pattern 2: Kubernetes Deployment
Phase 1: [Kubernetes Specialist] - Cluster setup and configuration
Phase 2: [CI/CD Specialist] - Build and deployment pipeline
Phase 3: [Monitoring Specialist] - Cluster and application monitoring

### Pattern 3: Multi-Cloud Migration
Phase 1: [Terraform Specialist] - Multi-cloud IaC setup
Phase 2: [AWS/Azure/GCP Specialist] - Cloud-specific configurations
Phase 3: [CI/CD Specialist] - Multi-cloud deployment pipeline
Phase 4: [Monitoring Specialist] - Unified monitoring across clouds
```

### Agent Registry Updates

The `AGENTS_REGISTRY.md` will be updated with:

```markdown
### Infrastructure Agents

#### devops-orchestrator
- **Category**: Infrastructure (Orchestration)
- **Description**: Coordinates DevOps specialists for complex infrastructure projects
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: Multi-specialist DevOps workflows, infrastructure planning, deployment coordination

#### aws-specialist
- **Category**: Infrastructure (Cloud)
- **Description**: AWS cloud services, architecture, and best practices
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Use for**: AWS infrastructure, CloudFormation, AWS security, cost optimization

[... similar entries for other specialists]
```

## Error Handling

### Orchestrator Error Handling

1. **Invalid Request**: If request is unclear, ask clarifying questions before delegating
2. **Specialist Unavailable**: Provide alternative approaches or manual guidance
3. **Conflicting Recommendations**: Synthesize conflicts and present options to user
4. **Incomplete Context**: Request additional information before proceeding
5. **Workflow Failures**: Provide rollback guidance and alternative paths

### Specialist Error Handling

1. **Missing Prerequisites**: Clearly state what's needed before proceeding
2. **Platform Limitations**: Explain constraints and suggest workarounds
3. **Configuration Errors**: Provide detailed error messages and fixes
4. **Best Practice Violations**: Warn users and explain risks
5. **Unsupported Scenarios**: Clearly state limitations and suggest alternatives

## Testing Strategy

### Agent Validation

Each agent should be validated for:

1. **Completeness**: All required sections present
2. **Consistency**: Follows established patterns
3. **Clarity**: Clear expertise areas and example tasks
4. **Tool Access**: Appropriate tools specified
5. **MCP Patterns**: Relevant MCP code execution examples

### Orchestrator Validation

The orchestrator should be tested for:

1. **Request Analysis**: Correctly identifies required specialists
2. **Workflow Sequencing**: Proper dependency ordering
3. **Context Maintenance**: Preserves information across invocations
4. **Results Synthesis**: Combines specialist outputs coherently
5. **Error Handling**: Gracefully handles edge cases

### Integration Testing

Test common workflows end-to-end:

1. **Simple Delegation**: Single specialist invocation
2. **Sequential Workflow**: Multi-specialist with dependencies
3. **Parallel Workflow**: Independent specialists working simultaneously
4. **Complex Workflow**: Full infrastructure setup with all specialists
5. **Error Recovery**: Handling failures mid-workflow

### Documentation Validation

Ensure documentation is:

1. **Accurate**: Reflects actual agent capabilities
2. **Complete**: All agents documented in registry
3. **Consistent**: Follows established patterns
4. **Accessible**: Clear invocation examples
5. **Maintainable**: Easy to update as agents evolve

## Design Decisions and Rationales

### Decision 1: Orchestrator vs Monolithic Agent

**Decision**: Split into orchestrator + specialists rather than keeping monolithic agent

**Rationale**:
- Enables deeper expertise in each domain
- Improves maintainability (changes isolated to specific agents)
- Allows parallel evolution of different domains
- Matches user mental model (AWS expert vs GCP expert)
- Follows successful e-commerce-coordinator pattern
- Enables better context management (specialist-specific context)

### Decision 2: Cloud Provider Separation

**Decision**: Create separate agents for AWS, Azure, and GCP

**Rationale**:
- Each cloud has distinct services, APIs, and best practices
- Prevents confusion between cloud-specific patterns
- Allows deeper expertise per platform
- Matches how users think about cloud providers
- Enables cloud-specific MCP patterns
- Reduces cognitive load (focus on one cloud at a time)

### Decision 3: IaC Tool Separation

**Decision**: Separate Terraform and Ansible specialists

**Rationale**:
- Different use cases (provisioning vs configuration)
- Distinct syntax and patterns
- Often used together but serve different purposes
- Allows focused expertise in each tool
- Terraform is multi-cloud, Ansible is configuration-focused
- Users typically specialize in one or the other

### Decision 4: Kubernetes as Separate Specialist

**Decision**: Extract Kubernetes from cloud specialists into dedicated agent

**Rationale**:
- Kubernetes is platform-agnostic (runs on all clouds)
- Complex enough to warrant dedicated expertise
- Often managed separately from cloud infrastructure
- Helm and service mesh are specialized domains
- Allows focus on cloud-native patterns
- Reduces overlap between cloud specialists

### Decision 5: Monitoring as Separate Specialist

**Decision**: Keep monitoring as dedicated specialist (not merge with observability-specialist)

**Rationale**:
- Observability-specialist already exists and focuses on implementation
- Monitoring specialist focuses on strategy and tool selection
- Allows coordination between DevOps orchestrator and observability specialist
- Maintains consistency with existing agent structure
- Provides flexibility in orchestration patterns

### Decision 6: CI/CD as Single Specialist

**Decision**: One CI/CD specialist covering multiple platforms

**Rationale**:
- CI/CD concepts are similar across platforms
- Users often need to compare platforms
- Prevents fragmentation (GitHub Actions vs GitLab CI specialists)
- Allows cross-platform best practices
- Reduces total number of agents
- Specialist can recommend best platform for use case

### Decision 7: MCP Code Execution Patterns

**Decision**: Include MCP patterns in each specialist

**Rationale**:
- Follows established pattern from existing agents
- Enables privacy-preserving operations
- Allows batch processing of cloud resources
- Supports complex multi-step workflows
- Provides concrete examples for users
- Maintains consistency with security-specialist and devops-specialist patterns

### Decision 8: Tool Access Consistency

**Decision**: All agents have Read, Write, Edit, Bash, Glob, Grep access

**Rationale**:
- DevOps work requires full file system access
- Need to create configuration files (Write)
- Need to modify existing configs (Edit)
- Need to run CLI commands (Bash)
- Need to search codebases (Glob, Grep)
- Consistent with existing DevOps-related agents
- Enables complete workflow execution

## Migration Strategy

### Phase 1: Create New Agents

1. Create all 8 new agent files
2. Ensure consistency with existing patterns
3. Include comprehensive MCP examples
4. Add detailed expertise sections

### Phase 2: Update Registry

1. Add new agents to AGENTS_REGISTRY.md
2. Update devops-specialist entry to devops-orchestrator
3. Add clear categorization (Orchestration, Cloud, IaC, Platform)
4. Include invocation examples

### Phase 3: Update Documentation

1. Update README.md with new agent count
2. Add DevOps orchestration examples to CLAUDE_CODE_USAGE.md
3. Update GETTING_STARTED.md with orchestrator patterns
4. Add workflow examples to documentation

### Phase 4: Deprecate Old Agent

1. Rename devops-specialist.md to devops-orchestrator.md
2. Update content to orchestration focus
3. Add references to new specialists
4. Maintain backward compatibility in registry

## Future Enhancements

### Potential Additional Specialists

- **Serverless Specialist**: Lambda, Cloud Functions, Azure Functions
- **Database Specialist**: RDS, Cloud SQL, managed databases (may coordinate with existing database-specialist)
- **Networking Specialist**: VPC, subnets, load balancers, CDN
- **Security Specialist**: Cloud security, compliance, IAM (coordinate with existing security-specialist)
- **Cost Optimization Specialist**: FinOps, cost analysis, optimization recommendations

### Orchestrator Enhancements

- **Project Templates**: Pre-defined multi-week project plans
- **Progress Tracking**: Milestone tracking across specialists
- **Impact Measurement**: Before/after metrics for infrastructure changes
- **Rollback Procedures**: Automated rollback guidance for failed changes
- **Compliance Checking**: Ensure configurations meet compliance requirements

### Integration Opportunities

- **Docker Specialist**: Coordinate for containerization before Kubernetes deployment
- **Security Specialist**: Integrate security reviews into infrastructure workflows
- **Observability Specialist**: Coordinate monitoring implementation
- **Test Specialist**: Integrate infrastructure testing (Terratest, etc.)

## Success Criteria

The design will be considered successful if:

1. **Clear Separation**: Each specialist has distinct, non-overlapping expertise
2. **Effective Orchestration**: Orchestrator successfully coordinates multi-specialist workflows
3. **User Clarity**: Users understand which specialist to invoke for their needs
4. **Consistency**: All agents follow established patterns and conventions
5. **Completeness**: All major DevOps domains are covered
6. **Maintainability**: Easy to update individual specialists without affecting others
7. **Integration**: Seamlessly integrates with existing agent ecosystem
8. **Documentation**: Clear documentation and examples for all agents
