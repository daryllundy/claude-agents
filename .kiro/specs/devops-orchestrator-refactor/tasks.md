# Implementation Plan

- [x] 1. Create AWS Specialist Agent
  - Create `.claude/agents/aws-specialist.md` with comprehensive AWS expertise
  - Include sections: Your Expertise (EC2, ECS, EKS, Lambda, RDS, S3, CloudWatch, IAM, VPC, CloudFormation, CDK), Task Approach, Output Format, Example Tasks, MCP Code Execution patterns, Best Practices
  - Add AWS Well-Architected Framework guidance
  - Include AWS-specific security patterns (IAM policies, Security Groups, KMS)
  - Add cost optimization recommendations specific to AWS pricing
  - Include multi-region deployment patterns
  - Add AWS CLI and SDK usage examples
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 9.3_

- [x] 2. Create Azure Specialist Agent
  - Create `.claude/agents/azure-specialist.md` with comprehensive Azure expertise
  - Include sections: Your Expertise (VMs, App Service, Functions, AKS, SQL Database, Blob Storage, Monitor, ARM templates, Bicep), Task Approach, Output Format, Example Tasks, MCP Code Execution patterns, Best Practices
  - Add Azure best practices and design patterns
  - Include Azure-specific security patterns (Azure AD, RBAC, Key Vault)
  - Add cost optimization recommendations specific to Azure pricing
  - Include hybrid cloud scenarios
  - Add Azure CLI and PowerShell usage examples
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 9.3_

- [x] 3. Create GCP Specialist Agent
  - Create `.claude/agents/gcp-specialist.md` with comprehensive GCP expertise
  - Include sections: Your Expertise (Compute Engine, Cloud Run, GKE, Cloud SQL, Cloud Storage, Cloud Monitoring, Deployment Manager), Task Approach, Output Format, Example Tasks, MCP Code Execution patterns, Best Practices
  - Add Google Cloud best practices and architecture patterns
  - Include GCP-specific security patterns (IAM, VPC, Secret Manager)
  - Add cost optimization recommendations specific to GCP pricing
  - Include multi-region deployment patterns
  - Add gcloud CLI usage examples
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 9.3_

- [x] 4. Create Terraform Specialist Agent
  - Create `.claude/agents/terraform-specialist.md` with comprehensive Terraform expertise
  - Include sections: Your Expertise (configuration, modules, state management, multi-cloud), Task Approach, Output Format, Example Tasks, MCP Code Execution patterns, Best Practices
  - Add module development and structure best practices
  - Include state management patterns (local, remote, workspaces)
  - Add variable and output management guidance
  - Include provider configuration for multiple clouds
  - Add Terraform Cloud/Enterprise patterns
  - Include import and refactoring guidance
  - _Requirements: 5.1, 5.2, 5.5, 9.3_

- [x] 5. Create Ansible Specialist Agent
  - Create `.claude/agents/ansible-specialist.md` with comprehensive Ansible expertise
  - Include sections: Your Expertise (playbooks, roles, inventory, configuration management), Task Approach, Output Format, Example Tasks, MCP Code Execution patterns, Best Practices
  - Add playbook structure and organization patterns
  - Include role development with proper defaults
  - Add variable precedence and management guidance
  - Include idempotent task design patterns
  - Add dynamic inventory for cloud providers
  - Include Ansible Vault usage for secrets
  - Add Ansible Galaxy and Molecule testing patterns
  - _Requirements: 5.3, 5.4, 5.5, 9.3_

- [x] 6. Create CI/CD Specialist Agent
  - Create `.claude/agents/cicd-specialist.md` with comprehensive CI/CD expertise
  - Include sections: Your Expertise (GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure DevOps), Task Approach, Output Format, Example Tasks, MCP Code Execution patterns, Best Practices
  - Add pipeline configuration for multiple platforms
  - Include build automation and optimization patterns (caching, parallelization)
  - Add testing integration guidance (unit, integration, e2e)
  - Include security scanning in pipelines
  - Add deployment automation patterns
  - Include artifact management and secrets management
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 9.3_

- [x] 7. Create Kubernetes Specialist Agent
  - Create `.claude/agents/kubernetes-specialist.md` with comprehensive Kubernetes expertise
  - Include sections: Your Expertise (Deployments, Services, Ingress, ConfigMaps, Secrets, RBAC), Task Approach, Output Format, Example Tasks, MCP Code Execution patterns, Best Practices
  - Add Helm chart creation and management patterns
  - Include auto-scaling guidance (HPA, VPA)
  - Add resource management best practices (requests, limits)
  - Include service mesh patterns (Istio, Linkerd)
  - Add network policies and security guidance
  - Include StatefulSet and persistent storage patterns
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 9.3_

- [x] 8. Create Monitoring Specialist Agent
  - Create `.claude/agents/monitoring-specialist.md` with comprehensive monitoring expertise
  - Include sections: Your Expertise (Prometheus, Grafana, ELK stack, distributed tracing), Task Approach, Output Format, Example Tasks, MCP Code Execution patterns, Best Practices
  - Add log aggregation and metric collection patterns
  - Include dashboard design and visualization guidance
  - Add alerting strategies and SLO/SLI definitions
  - Include distributed tracing implementation (Jaeger, Zipkin)
  - Add on-call and incident response workflows
  - Include cloud-native monitoring solutions
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 9.3_

- [x] 9. Transform DevOps Specialist into DevOps Orchestrator
  - Rename `.claude/agents/devops-specialist.md` to `.claude/agents/devops-orchestrator.md`
  - Rewrite content to focus on orchestration and coordination
  - Add specialist awareness section listing all DevOps sub-agents and their capabilities
  - Include workflow patterns for common scenarios (full infrastructure setup, deployment pipeline, multi-cloud deployment, migration projects)
  - Add request analysis guidance to identify required specialists
  - Include context management patterns for multi-agent workflows
  - Add results synthesis guidance for combining specialist outputs
  - Include cross-cutting concerns handling (security, cost optimization)
  - Add progress tracking patterns for multi-phase projects
  - Include specialist briefing templates
  - Add decision framework for specialist selection
  - Include integration patterns with existing agents (docker-specialist, security-specialist, observability-specialist)
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 10.1, 10.2, 10.3, 10.4, 10.5, 9.1, 9.3_

- [x] 10. Update AGENTS_REGISTRY.md
  - Add devops-orchestrator entry in Infrastructure Agents section with category "Infrastructure (Orchestration)"
  - Add aws-specialist entry in Infrastructure Agents section with category "Infrastructure (Cloud)"
  - Add azure-specialist entry in Infrastructure Agents section with category "Infrastructure (Cloud)"
  - Add gcp-specialist entry in Infrastructure Agents section with category "Infrastructure (Cloud)"
  - Add terraform-specialist entry in Infrastructure Agents section with category "Infrastructure (IaC)"
  - Add ansible-specialist entry in Infrastructure Agents section with category "Infrastructure (IaC)"
  - Add cicd-specialist entry in Infrastructure Agents section with category "Infrastructure (Platform)"
  - Add kubernetes-specialist entry in Infrastructure Agents section with category "Infrastructure (Platform)"
  - Add monitoring-specialist entry in Infrastructure Agents section with category "Infrastructure (Platform)"
  - Update agent count in header from 22 to 30 agents
  - Add invocation examples for orchestrator and specialists
  - Update Agent Selection Guide table with new specialists
  - _Requirements: 9.2, 9.5_

- [x] 11. Update README.md
  - Update agent count from 24 to 32 agents in overview section
  - Add DevOps Orchestration section explaining the orchestrator pattern
  - Add examples of multi-specialist DevOps workflows
  - Update Infrastructure Agents section to list new specialists
  - Add note about devops-specialist being renamed to devops-orchestrator
  - _Requirements: 9.2, 9.5_

- [x] 12. Update CLAUDE_CODE_USAGE.md
  - Add DevOps Orchestration Workflows section with examples
  - Include example: "Full Infrastructure Setup" workflow using orchestrator + cloud + IaC + monitoring specialists
  - Include example: "Kubernetes Deployment Pipeline" workflow using orchestrator + Kubernetes + CI/CD + monitoring specialists
  - Include example: "Multi-Cloud Migration" workflow using orchestrator + multiple cloud specialists + Terraform
  - Add guidance on when to use orchestrator vs direct specialist invocation
  - Include specialist coordination patterns
  - _Requirements: 9.5, 10.1, 10.2, 10.3_

- [x] 13. Update GETTING_STARTED.md
  - Add section on DevOps orchestration patterns
  - Include simple example of using devops-orchestrator for infrastructure setup
  - Add guidance on choosing between orchestrator and direct specialist invocation
  - Include example of sequential specialist invocation
  - _Requirements: 9.5_

- [x] 14. Validate agent consistency
  - Review all 8 new agent files for consistent structure and formatting
  - Verify all agents follow the established markdown pattern
  - Check that MCP code execution sections are relevant and comprehensive
  - Ensure tool access is correctly specified for all agents
  - Verify example tasks are clear and actionable
  - Confirm best practices sections are complete
  - _Requirements: 9.1, 9.4_

- [x] 15. Validate orchestrator functionality
  - Review devops-orchestrator.md for complete workflow patterns
  - Verify specialist selection logic is clear and comprehensive
  - Check that integration patterns with existing agents are documented
  - Ensure context management guidance is included
  - Verify results synthesis patterns are clear
  - Confirm error handling guidance is comprehensive
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 10.4_

- [x] 16. Validate documentation updates
  - Review AGENTS_REGISTRY.md for accuracy and completeness
  - Verify README.md updates are clear and accurate
  - Check CLAUDE_CODE_USAGE.md examples are comprehensive and actionable
  - Ensure GETTING_STARTED.md guidance is beginner-friendly
  - Verify all agent counts are updated consistently across documentation
  - Confirm invocation examples are clear and follow established patterns
  - _Requirements: 9.2, 9.5_
