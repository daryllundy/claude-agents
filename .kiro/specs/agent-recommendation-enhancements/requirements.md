# Requirements Document

## Introduction

This document defines requirements for enhancing the agent recommendation script (`scripts/recommend_agents.sh`) to improve its detection capabilities, expand coverage to all 30 available agents, and provide better user experience through interactive features and improved output.

## Glossary

- **Agent Recommendation Script**: The bash script (`recommend_agents.sh`) that scans a project and downloads relevant Claude Code agent prompt files based on detected technologies
- **Detection Pattern**: A set of file, path, or content checks used to identify if a specific technology or practice is present in a project
- **Agent Coverage**: The percentage of available agents (30 total) that have detection patterns in the script
- **Interactive Mode**: A mode where the script prompts users for input to refine recommendations
- **Confidence Score**: A numerical indicator (0-100) representing how strongly a project matches an agent's use case

## Requirements

### Requirement 1: Complete Agent Coverage

**User Story:** As a developer, I want the script to detect and recommend all 30 available agents, so that I can access the full range of specialized expertise for my project.

#### Acceptance Criteria

1. WHEN the Agent Recommendation Script executes, THE Agent Recommendation Script SHALL include detection patterns for all 30 agents listed in AGENTS_REGISTRY.md
2. WHEN the Agent Recommendation Script identifies missing detection patterns, THE Agent Recommendation Script SHALL log which agents lack coverage during development
3. WHERE new agents are added to AGENTS_REGISTRY.md, THE Agent Recommendation Script SHALL support detection patterns for the new agents within the same release cycle

### Requirement 2: Cloud Provider Detection

**User Story:** As a cloud infrastructure developer, I want the script to detect which cloud providers I'm using (AWS, Azure, GCP), so that I receive recommendations for the appropriate cloud specialist agents.

#### Acceptance Criteria

1. WHEN the project contains AWS-specific configuration files (aws-cli config, CloudFormation templates, CDK files), THE Agent Recommendation Script SHALL recommend aws-specialist
2. WHEN the project contains Azure-specific configuration files (ARM templates, Bicep files, azure-pipelines.yml), THE Agent Recommendation Script SHALL recommend azure-specialist
3. WHEN the project contains GCP-specific configuration files (gcloud config, Deployment Manager templates), THE Agent Recommendation Script SHALL recommend gcp-specialist
4. WHEN the project contains configuration for multiple cloud providers, THE Agent Recommendation Script SHALL recommend all applicable cloud specialists

### Requirement 3: Infrastructure as Code Detection

**User Story:** As a DevOps engineer, I want the script to detect IaC tools beyond Terraform, so that I receive recommendations for ansible-specialist and other IaC-related agents.

#### Acceptance Criteria

1. WHEN the project contains Terraform files (*.tf, *.tfvars), THE Agent Recommendation Script SHALL recommend terraform-specialist
2. WHEN the project contains Ansible files (playbooks, roles, inventory files), THE Agent Recommendation Script SHALL recommend ansible-specialist
3. WHEN the project contains both Terraform and cloud provider configurations, THE Agent Recommendation Script SHALL recommend devops-orchestrator for coordinating multi-tool workflows

### Requirement 4: CI/CD and Kubernetes Detection

**User Story:** As a platform engineer, I want the script to distinguish between general DevOps, CI/CD pipelines, and Kubernetes orchestration, so that I receive more precise agent recommendations.

#### Acceptance Criteria

1. WHEN the project contains CI/CD pipeline files (GitHub Actions, GitLab CI, Jenkins, CircleCI), THE Agent Recommendation Script SHALL recommend cicd-specialist
2. WHEN the project contains Kubernetes manifests (*.yaml in k8s directories, Helm charts), THE Agent Recommendation Script SHALL recommend kubernetes-specialist
3. WHEN the project contains monitoring configuration (Prometheus, Grafana, ELK), THE Agent Recommendation Script SHALL recommend monitoring-specialist
4. WHEN the project contains multiple infrastructure components (IaC, CI/CD, Kubernetes, monitoring), THE Agent Recommendation Script SHALL recommend devops-orchestrator

### Requirement 5: Enhanced Output Formatting

**User Story:** As a developer, I want the script to provide clear, categorized output with descriptions, so that I understand why each agent was recommended and what it can help with.

#### Acceptance Criteria

1. WHEN the Agent Recommendation Script completes detection, THE Agent Recommendation Script SHALL display recommended agents grouped by category (Infrastructure, Development, Quality, Operations, Productivity, Business, Specialized)
2. WHEN the Agent Recommendation Script displays an agent recommendation, THE Agent Recommendation Script SHALL include a brief description of the agent's purpose
3. WHEN the Agent Recommendation Script displays recommendations, THE Agent Recommendation Script SHALL indicate which detection patterns triggered each recommendation
4. WHERE the --verbose flag is provided, THE Agent Recommendation Script SHALL display detailed detection results including all patterns checked and matched

### Requirement 6: Confidence Scoring

**User Story:** As a developer, I want to see confidence scores for each recommendation, so that I can prioritize which agents are most relevant to my project.

#### Acceptance Criteria

1. WHEN the Agent Recommendation Script detects multiple signals for an agent, THE Agent Recommendation Script SHALL calculate a confidence score between 0 and 100
2. WHEN the Agent Recommendation Script displays recommendations, THE Agent Recommendation Script SHALL sort agents by confidence score in descending order
3. WHEN the confidence score is below 50, THE Agent Recommendation Script SHALL mark the recommendation as "suggested" rather than "recommended"
4. WHERE the --min-confidence flag is provided with a value, THE Agent Recommendation Script SHALL only recommend agents with confidence scores at or above the specified value

### Requirement 7: Interactive Selection Mode

**User Story:** As a developer, I want an interactive mode where I can review and select which agents to download, so that I have control over which agents are added to my project.

#### Acceptance Criteria

1. WHERE the --interactive flag is provided, THE Agent Recommendation Script SHALL display all recommended agents with checkboxes for selection
2. WHILE in interactive mode, THE Agent Recommendation Script SHALL allow users to toggle agent selection using keyboard input
3. WHEN the user confirms selections in interactive mode, THE Agent Recommendation Script SHALL download only the selected agents
4. WHERE the --interactive flag is provided, THE Agent Recommendation Script SHALL display agent descriptions and confidence scores to inform selection

### Requirement 8: Project Profile Export

**User Story:** As a team lead, I want to export my project's technology profile and agent recommendations, so that I can share standardized agent configurations across my team.

#### Acceptance Criteria

1. WHERE the --export flag is provided with a file path, THE Agent Recommendation Script SHALL write detection results to a JSON file at the specified path
2. WHEN exporting project profile, THE Agent Recommendation Script SHALL include detected technologies, recommended agents, confidence scores, and detection patterns matched
3. WHERE the --import flag is provided with a file path, THE Agent Recommendation Script SHALL read agent recommendations from the JSON file and download the specified agents
4. WHEN importing from a profile, THE Agent Recommendation Script SHALL validate that all agents in the profile exist in AGENTS_REGISTRY.md

### Requirement 9: Improved Error Handling

**User Story:** As a developer, I want clear error messages when the script encounters issues, so that I can troubleshoot problems quickly.

#### Acceptance Criteria

1. WHEN the Agent Recommendation Script fails to download an agent file, THE Agent Recommendation Script SHALL log the specific agent name and HTTP status code
2. WHEN the Agent Recommendation Script cannot access the repository, THE Agent Recommendation Script SHALL provide a clear error message with troubleshooting steps
3. WHEN the Agent Recommendation Script encounters invalid command-line arguments, THE Agent Recommendation Script SHALL display the help message with the specific error highlighted
4. IF network connectivity fails during download, THEN THE Agent Recommendation Script SHALL retry up to 3 times with exponential backoff before failing

### Requirement 10: Update Detection

**User Story:** As a developer with existing agents, I want to know when agent files have been updated in the repository, so that I can keep my local agents current.

#### Acceptance Criteria

1. WHERE the --check-updates flag is provided, THE Agent Recommendation Script SHALL compare local agent file checksums with remote versions
2. WHEN local agent files differ from remote versions, THE Agent Recommendation Script SHALL display which agents have updates available
3. WHERE the --update-all flag is provided, THE Agent Recommendation Script SHALL download updated versions of all locally installed agents
4. WHEN updating agents, THE Agent Recommendation Script SHALL create backups of existing agent files before overwriting them
