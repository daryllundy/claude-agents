# Claude Code Agents

A comprehensive collection of **31 specialized AI agents** and **7 skills** designed for **Claude Code Pro** users. These agents and skills work as intelligent sub-agents that can be invoked within Claude Code to handle specific development, infrastructure, marketing, and e-commerce tasks with deep domain expertise.

## What's New: E-Commerce Orchestration System

The newest and most powerful feature of this collection is the **intelligent orchestration system** for e-commerce transformation:

- **E-Commerce Orchestrator Skill**: Automatically analyzes e-commerce websites, scores them across 6 critical dimensions, and recommends the right specialists at the right time
- **E-Commerce Coordinator Agent**: Orchestrates multi-week transformation projects, tracking progress and coordinating specialist consultations
- **6-Dimensional Scoring**: Design & UX, Platform Optimization, Marketing, Social Media, Automation, and Performance
- **Auto-Discovery**: Simply paste an e-commerce URL and watch the orchestrator identify issues and route to specialists
- **Proven Workflow Patterns**: Pre-configured sequences for new launches, store revivals, scaling, and market expansion

**Example**: "Analyze https://mystore.com" → Orchestrator identifies issues → Routes to web-design-specialist, shopify-specialist, instagram-specialist, and zapier-specialist in the optimal sequence → Tracks results and ROI.

## DevOps Orchestration System

The **DevOps Orchestrator** provides intelligent coordination of infrastructure specialists for complex cloud and platform projects:

- **DevOps Orchestrator Agent**: Analyzes infrastructure requirements and coordinates 8 specialized DevOps sub-agents
- **Cloud Provider Specialists**: Deep expertise in AWS, Azure, and GCP with platform-specific best practices
- **Infrastructure as Code Specialists**: Terraform and Ansible experts for provisioning and configuration management
- **Platform Specialists**: CI/CD, Kubernetes, and monitoring experts for complete infrastructure automation
- **Pre-defined Workflows**: Common patterns for full infrastructure setup, deployment pipelines, multi-cloud migrations, and Kubernetes deployments

**How It Works**: The orchestrator analyzes your infrastructure needs, identifies required specialists (cloud provider, IaC, CI/CD, monitoring), coordinates their work in the optimal sequence, maintains context across specialists, and synthesizes results into cohesive solutions.

**Example Workflows**:
- **Full Infrastructure Setup**: AWS Specialist → Terraform Specialist → Kubernetes Specialist → CI/CD Specialist → Monitoring Specialist
- **Multi-Cloud Migration**: Terraform Specialist → Multiple Cloud Specialists → CI/CD Specialist → Monitoring Specialist
- **Kubernetes Deployment Pipeline**: Kubernetes Specialist → CI/CD Specialist → Monitoring Specialist

**When to Use**:
- Use the **devops-orchestrator** for complex multi-phase infrastructure projects requiring coordination across multiple domains
- Use **individual specialists** directly for focused tasks (e.g., "Use aws-specialist to design a VPC architecture")

## Features

- **31 Specialized Agents** organized into 9 categories (including orchestration)
- **7 Claude Code Skills** for specialized marketing, e-commerce, and orchestration
- **DevOps Orchestration System** - Intelligent coordination of cloud, IaC, CI/CD, and monitoring specialists
- **MCP Code Execution Support** - Enhanced agents leverage Model Context Protocol for efficient data processing
- **Intelligent Orchestration** - Coordinate multi-specialist workflows automatically
- **Ready for Claude Code Pro** - Use as sub-agents via the Task tool or auto-discovered skills
- **Deep Domain Expertise** - Each agent/skill specializes in a specific area
- **No API Keys Required** - Works directly with Claude Code Pro
- **Detailed Agent Prompts** - Pre-configured with best practices and expertise
- **Easy to Invoke** - Simple natural language requests

## Agent Categories

### Orchestration (1 agent)
**NEW!** Intelligent workflow coordination for e-commerce transformation:
- **e-commerce-coordinator** - Orchestrates multi-specialist e-commerce projects, tracks progress across 8-week transformation roadmaps, synthesizes results from design, platform, marketing, and automation specialists

### Infrastructure (11 agents)
**NEW!** Comprehensive DevOps orchestration system with specialized cloud and platform experts:

**Orchestration:**
- **devops-orchestrator** ⭐ (formerly devops-specialist) - Coordinates DevOps specialists for complex infrastructure projects, manages multi-cloud deployments, and orchestrates full-stack infrastructure workflows

> **Note**: The `devops-specialist` has been transformed into `devops-orchestrator` to better reflect its role as a coordinator of specialized DevOps sub-agents. For focused infrastructure tasks, use the specific cloud or platform specialists directly.

**Cloud Providers:**
- **aws-specialist** - AWS services, CloudFormation, Well-Architected Framework, IAM, and cost optimization
- **azure-specialist** - Azure services, ARM templates, Bicep, Azure AD, and hybrid cloud scenarios
- **gcp-specialist** - Google Cloud services, Deployment Manager, GCP IAM, and multi-region deployments

**Infrastructure as Code:**
- **terraform-specialist** - Terraform configuration, modules, state management, and multi-cloud provisioning
- **ansible-specialist** - Ansible playbooks, roles, inventory management, and configuration automation

**Platform & Operations:**
- **cicd-specialist** - CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure DevOps)
- **kubernetes-specialist** - Kubernetes deployments, Helm charts, service mesh, and auto-scaling
- **monitoring-specialist** - Prometheus, Grafana, ELK stack, distributed tracing, and alerting strategies
- **docker-specialist** - Container configuration and optimization
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

## Skills

In addition to the 24 agents above, this repository includes **7 Claude Code Skills** - a newer format that allows Claude to automatically discover and use specialized capabilities based on context.

### What's the Difference?

- **Agents** (`.claude/agents/`): Explicitly invoked via Task tool with "Use the X-specialist..." syntax
- **Skills** (`.claude/skills/`): Automatically discovered and loaded by Claude based on task context

Think of agents as specialists you call by name, and skills as expertise that activates automatically when needed.

### Available Skills

#### e-commerce-orchestrator (NEW!)
**The Brain of E-Commerce Transformation**

Comprehensive e-commerce website auditor and strategist that analyzes URLs, detects platforms (Shopify, WooCommerce, etc.), scores performance across 6 critical dimensions, and intelligently routes to the right specialists at the right time.

**Capabilities**:
- Platform detection and analysis (Shopify, WooCommerce, BigCommerce, Magento, custom)
- 6-dimensional scoring: Design & UX, Platform Optimization, Marketing, Social Media, Automation, Performance
- Generates 20-30 prioritized findings with impact/effort estimates
- Competitive benchmarking and ROI estimation
- Intelligent specialist routing (recommends shopify-specialist, web-design-specialist, instagram-specialist, etc.)
- Interactive workflow guidance with clear next steps

**Auto-activates when**: Analyzing e-commerce URLs, discussing store audits, asking about conversion optimization

**Example**: "Analyze https://mystore.com and tell me what to fix first"

**Location**: `.claude/skills/e-commerce-orchestrator/SKILL.md`

#### shopify-specialist
Build and optimize Shopify e-commerce stores, customize themes with Liquid, implement conversion optimization strategies, and integrate apps and payment systems. Expert in checkout optimization, product page design, and Shopify-specific best practices.

**Auto-activates when**: Discussing Shopify development, e-commerce optimization, or online store improvements

**Location**: `.claude/skills/shopify-specialist/SKILL.md`

#### web-design-specialist
Create modern, accessible, and conversion-optimized web designs. Expert in UX/UI best practices, responsive design, design systems, and accessibility (WCAG). Focuses on mobile-first approach and user-centered design.

**Auto-activates when**: Discussing web design, user experience, mobile optimization, or design systems

**Location**: `.claude/skills/web-design-specialist/SKILL.md`

#### instagram-specialist
Create Instagram marketing strategies, develop engaging Reels and Stories content, optimize for Instagram's algorithm, and build authentic brand communities. Expert in Instagram Shopping, influencer partnerships, and visual storytelling.

**Auto-activates when**: Discussing Instagram marketing, influencer partnerships, or visual social media strategy

**Location**: `.claude/skills/instagram-specialist/SKILL.md`

#### tiktok-strategist
Create TikTok marketing strategies, develop viral content ideas, plan TikTok campaigns, and optimize for TikTok's algorithm. Expert in reaching Gen Z audiences, creator partnerships, and viral content mechanics.

**Auto-activates when**: Discussing TikTok marketing, viral content, or targeting younger demographics

**Location**: `.claude/skills/tiktok-strategist/SKILL.md`

#### social-media-specialist
Develop comprehensive multi-platform social media strategies, create engaging content, manage communities, and run data-driven campaigns. Expert in cross-platform coordination, content calendars, and community building.

**Auto-activates when**: Discussing multi-platform social media strategy, community management, or content planning

**Location**: `.claude/skills/social-media-specialist/SKILL.md`

#### zapier-specialist
Design and implement powerful workflow automations using Zapier, integrate 6000+ apps without code, and automate business processes. Expert in order processing automation, email sequences, and system integrations.

**Auto-activates when**: Discussing workflow automation, app integrations, or process optimization

**Location**: `.claude/skills/zapier-specialist/SKILL.md`

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
   codebase, recommends relevant specialist agents based on detected technologies,
   and downloads their prompt files into `.claude/agents/`.

   **Enhanced Features**:
   - **Intelligent Detection**: Scans for 30+ technology patterns across cloud providers, IaC tools, frameworks, and more
   - **Confidence Scoring**: Shows confidence levels (0-100%) for each recommendation with visual progress bars
   - **Interactive Mode**: Select which agents to install with keyboard navigation (`--interactive`)
   - **Profile Export/Import**: Save detection results and share agent configurations across projects (`--export`, `--import`)
   - **Update Detection**: Check for and install updates to locally installed agents (`--check-updates`, `--update-all`)
   - **Categorized Output**: Agents grouped by category (Infrastructure, Development, Quality, etc.)
   - **Verbose Mode**: See detailed pattern matching results (`--verbose`)
   - **Confidence Filtering**: Control recommendation threshold (`--min-confidence 50`)

   **Example Usage**:
   ```bash
   # Standard recommendation with default threshold (25%)
   bash scripts/recommend_agents.sh

   # Interactive selection mode
   bash scripts/recommend_agents.sh --interactive

   # Export profile for sharing
   bash scripts/recommend_agents.sh --export my-project-profile.json

   # Import profile in another project
   bash scripts/recommend_agents.sh --import my-project-profile.json

   # Check for updates to installed agents
   bash scripts/recommend_agents.sh --check-updates

   # Update all agents to latest versions
   bash scripts/recommend_agents.sh --update-all

   # Verbose output with higher confidence threshold
   bash scripts/recommend_agents.sh --verbose --min-confidence 50

   # Dry run to see recommendations without downloading
   bash scripts/recommend_agents.sh --dry-run
   ```

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

## Customizing Agent Detection Patterns

The agent recommendation script uses externalized detection patterns stored in `data/agent_patterns.yaml`. This allows you to customize how agents are detected and recommended without modifying the shell script.

### Pattern File Structure

The YAML file defines detection patterns for each agent with three types:
- **file**: Matches file names or extensions (e.g., `*.tf`, `package.json`)
- **path**: Matches directory names (e.g., `terraform/`, `k8s/`)
- **content**: Matches text within files (e.g., `terraform`, `apiVersion`)

Each pattern has a weight (0-25) that contributes to the agent's confidence score.

### Example Pattern Definition

```yaml
agents:
  terraform-specialist:
    category: infrastructure
    description: "Terraform Infrastructure as Code expert"
    patterns:
      - type: file
        pattern: "*.tf"
        weight: 20
      - type: file
        pattern: "terraform.tfstate"
        weight: 25
      - type: content
        pattern: "terraform"
        weight: 10
```

### Customization Options

1. **Adjust pattern weights**: Change weights to fine-tune detection sensitivity
2. **Add new patterns**: Include additional file types or content patterns
3. **Create custom agents**: Define new agents with their own patterns
4. **Override patterns**: Place a customized `agent_patterns.yaml` in your project's `.claude/` directory

### Fallback Mechanism

If the YAML file is not found or fails to parse, the script automatically falls back to hardcoded patterns, ensuring the recommendation system always works.

## Understanding Confidence Scores

The agent recommendation script calculates confidence scores to indicate how well your project matches each agent's expertise area. Understanding how these scores work helps you make informed decisions about which agents to use.

### Confidence Calculation Formula

```
confidence = (accumulated_weight / max_possible_weight) × 100
```

Where:
- **accumulated_weight**: Sum of weights from patterns that matched in your project
- **max_possible_weight**: Sum of all pattern weights defined for the agent

The confidence score is capped at 100%.

### Why Dynamic Max Weight?

Each agent has a different number and types of detection patterns based on their domain expertise. Using a dynamic max weight (rather than a fixed value) ensures confidence scores accurately reflect how well your project matches each agent's specific area:

- `terraform-specialist` might have patterns totaling 85 weight (5 patterns)
- `docker-specialist` might have patterns totaling 65 weight (4 patterns)
- `aws-specialist` might have patterns totaling 120 weight (8 patterns)

This approach makes confidence scores comparable across all agents, regardless of how many patterns each agent defines.

### Example Calculation

Consider the `terraform-specialist` with these patterns:
- `file:*.tf:20` → **matches** (you have .tf files)
- `file:*.tfvars:15` → **matches** (you have .tfvars files)
- `file:terraform.tfstate:25` → **no match** (no state file)
- `content:terraform:10` → **no match** (keyword not found)

Calculation:
1. **Accumulated weight**: 20 + 15 = 35 (only matched patterns)
2. **Max possible weight**: 20 + 15 + 25 + 10 = 70 (all patterns)
3. **Confidence**: (35 / 70) × 100 = 50%

Result: `terraform-specialist` shows 50% confidence (Recommended tier)

### Confidence Tiers

The script categorizes agents into recommendation tiers:

- **75-100%** (✓✓✓): Highly Recommended - Strong match, primary expertise needed
- **50-74%** (✓✓): Recommended - Good match, likely useful
- **25-49%** (✓): Suggested - Moderate match, potentially helpful
- **0-24%**: Not shown by default (use `--min-confidence 0` to see all)

### Debugging Confidence Scores

If you want to understand why an agent received a specific confidence score, use the debug flags:

```bash
# Show detailed calculation for a specific agent
bash scripts/recommend_agents.sh --debug-confidence terraform-specialist

# Output shows:
# ═══════════════════════════════════════════════════════════════════════
# Confidence Calculation Debug: terraform-specialist
# ═══════════════════════════════════════════════════════════════════════
# 
# Pattern Evaluation:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Match Weight   Type         Pattern
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✓     20       file         *.tf
# ✓     15       file         *.tfvars
# ✗     25       file         terraform.tfstate
# ✗     10       content      terraform
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 
# Calculation:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Accumulated Weight:            35
# Max Possible Weight:           70
# Confidence:                    50%
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```bash
# View max possible weights for all agents
bash scripts/recommend_agents.sh --show-max-weights

# Output shows:
# Agent Max Possible Weights
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Agent                                    Max Weight
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# aws-specialist                                  120
# docker-specialist                                65
# terraform-specialist                             70
# ...
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Troubleshooting Confidence Scores

**Problem**: Agent has unexpectedly low confidence

**Solutions**:
- Use `--debug-confidence <agent-name>` to see which patterns matched
- Check if expected files are in the scanned directory
- Verify file naming matches patterns (e.g., `Dockerfile` vs `dockerfile`)
- Use `--verbose` to see all pattern checks across all agents

**Problem**: Agent has unexpectedly high confidence

**Solutions**:
- Review matched patterns with `--debug-confidence <agent-name>`
- Check if generic patterns are matching unintended files
- Consider adjusting pattern weights in `data/agent_patterns.yaml`

**Problem**: Multiple agents show similar confidence scores

**Solutions**:
- This is normal for projects using multiple related technologies
- Use `--interactive` mode to manually select the most relevant agents
- Review agent descriptions to understand their specific focus areas
- Consider using an orchestrator agent (e.g., `devops-orchestrator`) for complex multi-domain projects

## MCP Code Execution

Several agents now include **Model Context Protocol (MCP) Code Execution** capabilities for enhanced data processing and tool integration:

### Enhanced Agents
- **data-science-specialist** - Process large datasets efficiently, train models locally
- **database-specialist** - Execute complex queries and transformations
- **debugging-specialist** - Run diagnostic code and analyze execution traces
- **devops-specialist** - Automate infrastructure operations with code
- **observability-specialist** - Process metrics and logs programmatically
- **performance-specialist** - Run benchmarks and analyze performance data
- **security-specialist** - Execute security scans and vulnerability assessments

### Key Benefits
- **Context-Efficient**: Process large datasets (10,000 rows → 5 relevant rows) before results reach the model
- **Better Control Flow**: Use loops, conditionals, and error handling for complex pipelines
- **Privacy Protection**: Intermediate results and sensitive data stay in the execution environment
- **Reusable Skills**: Save common functions to `./skills/` directory for future use

### When to Use
- Processing large datasets (>100 rows)
- Multi-step data transformations
- Iterative operations (model training, testing)
- Combining data from multiple MCP sources
- Complex analysis requiring multiple operations

### Example
```python
# Instead of making multiple tool calls, write code:
import database_mcp
import pandas as pd

# Fetch and process data locally
data = await database_mcp.query({"sql": "SELECT * FROM users"})
df = pd.DataFrame(data)
filtered = df[df['active'] == True].groupby('region').size()

# Only summary enters model context
print(f"Active users by region: {filtered.to_dict()}")
```

## Project Structure

```
claude-agents/
├── .claude/
│   ├── agents/                      # Agent prompt definitions (Task tool)
│   │   ├── AGENTS_REGISTRY.md       # Complete agent catalog
│   │   ├── e-commerce-coordinator.md # E-commerce orchestration agent
│   │   ├── docker-specialist.md     # Docker agent prompt
│   │   ├── security-specialist.md   # Security agent prompt
│   │   ├── test-specialist.md       # Testing agent prompt
│   │   └── ...                      # Other agent prompts
│   ├── skills/                      # Skill definitions (auto-discovery)
│   │   ├── tiktok-strategist/       # TikTok marketing skill
│   │   │   └── SKILL.md
│   │   ├── instagram-specialist/    # Instagram marketing skill
│   │   │   └── SKILL.md
│   │   ├── web-design-specialist/   # Web design and UX/UI skill
│   │   │   └── SKILL.md
│   │   ├── social-media-specialist/ # Multi-platform social media skill
│   │   │   └── SKILL.md
│   │   ├── shopify-specialist/      # Shopify e-commerce skill
│   │   │   └── SKILL.md
│   │   ├── zapier-specialist/       # Workflow automation skill
│   │   │   └── SKILL.md
│   │   └── e-commerce-orchestrator/ # E-commerce audit and orchestration skill
│   │       └── SKILL.md
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
- **MCP Server Support** (optional) - For enhanced code execution capabilities with compatible agents
- No additional dependencies or API keys needed for basic functionality

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

### Example 5: DevOps Infrastructure Setup
```
# Orchestrated multi-specialist DevOps workflow
Step 1: "Use devops-orchestrator to set up a production infrastructure on AWS"
        → Orchestrator analyzes requirements and coordinates specialists

Step 2: Orchestrator invokes aws-specialist
        → "Setting up VPC, EC2 instances, RDS, and S3 buckets"

Step 3: Orchestrator invokes terraform-specialist
        → "Codifying infrastructure for repeatability and version control"

Step 4: Orchestrator invokes kubernetes-specialist
        → "Deploying application to EKS cluster with auto-scaling"

Step 5: Orchestrator invokes cicd-specialist
        → "Creating GitHub Actions pipeline for automated deployments"

Step 6: Orchestrator invokes monitoring-specialist
        → "Setting up Prometheus, Grafana, and alerting"

Alternative: Direct specialist invocation for focused tasks
"Use aws-specialist to design a highly available architecture for my web application"
"Use terraform-specialist to create reusable modules for our multi-cloud infrastructure"
```

### Example 6: E-Commerce Transformation
```
# Orchestrated multi-specialist workflow
Step 1: "Analyze https://mystore.com"  # e-commerce-orchestrator skill auto-activates
        → Detects platform, scores 6 dimensions, presents priorities

Step 2: User chooses "Mobile UX" (scored 3/10)
        → "Use web-design-specialist to redesign for mobile-first approach"

Step 3: After mobile improvements, return to orchestrator
        → "What should we tackle next?"
        → User chooses "Instagram integration"

Step 4: "Use instagram-specialist to launch Instagram Shopping and Reels strategy"

Step 5: Continue workflow through remaining priorities
        → "Use zapier-specialist to automate order processing"

Alternative: "Use e-commerce-coordinator to execute the full transformation roadmap"
            → Coordinates all specialists through 8-week transformation plan
```

## Best Practices

1. **Be Specific**: Provide clear context and requirements
   - ❌ "Use docker-specialist to help with Docker"
   - ✅ "Use docker-specialist to create a production Dockerfile for my Python Flask app with health checks"

2. **Sequential Tasks**: For dependent tasks, execute one at a time
3. **Provide Context**: Include file paths, technologies, and constraints
4. **Review Output**: Always review agent results before proceeding

## Network Operations & Caching

The agent recommendation script includes robust network handling with automatic retry logic and intelligent caching to ensure reliability in various network conditions.

### Automatic Retry with Exponential Backoff

All network operations automatically retry on failure:

- **Retry Attempts**: 3 attempts per download
- **Backoff Strategy**: Exponential backoff (1s, 2s, 4s between attempts)
- **Timeout**: 30 seconds per attempt
- **Error Diagnostics**: HTTP status codes logged for each attempt
- **Troubleshooting Guidance**: Detailed help provided on final failure

**Example behavior**:
```
Attempt 1 failed (HTTP 503). Retrying in 1s...
Attempt 2 failed (HTTP 503). Retrying in 2s...
Attempt 3 failed (HTTP 503). No more retries.

Error: Failed to download from https://example.com/file after 3 attempts

Troubleshooting:
  1. Check your internet connection
  2. Verify the URL is accessible: curl -I https://example.com/file
  3. Check if you're behind a proxy or firewall
  4. Try again later if the server is temporarily unavailable
```

### Intelligent Caching

The script caches downloaded files to reduce network requests and support offline workflows:

**Cache Behavior**:
- **Location**: `$XDG_CACHE_HOME/claude-agents` or `~/.cache/claude-agents`
- **Default Expiry**: 24 hours (86400 seconds)
- **Cache Strategy**: Check cache first, fetch on miss or stale data
- **Update Operations**: Use 1-hour cache for update checks and registry fetches

**Benefits**:
- Faster repeated operations (no network delay)
- Reduced bandwidth usage
- Offline workflow support (use cached data when network unavailable)
- Improved reliability in CI/CD environments

### Cache Control Flags

Control caching behavior with command-line flags:

```bash
# Force refresh - bypass cache and fetch fresh data
bash scripts/recommend_agents.sh --force-refresh

# Clear all cached files
bash scripts/recommend_agents.sh --clear-cache

# Use custom cache directory
bash scripts/recommend_agents.sh --cache-dir=/tmp/my-cache

# Set custom cache expiry (in seconds)
bash scripts/recommend_agents.sh --cache-expiry=3600  # 1 hour
bash scripts/recommend_agents.sh --cache-expiry=86400  # 24 hours (default)
bash scripts/recommend_agents.sh --cache-expiry=604800  # 1 week
```

### Offline Workflow Example

```bash
# First run - downloads and caches agent files
bash scripts/recommend_agents.sh

# Subsequent runs within 24 hours - uses cached data (instant)
bash scripts/recommend_agents.sh

# After 24 hours - automatically fetches fresh data
bash scripts/recommend_agents.sh

# Force fresh data anytime
bash scripts/recommend_agents.sh --force-refresh

# Work completely offline (uses cached data regardless of age)
# Note: Initial download required before offline use
bash scripts/recommend_agents.sh  # Uses cache if available
```

### Cache Management

```bash
# View cache location
echo ${XDG_CACHE_HOME:-$HOME/.cache}/claude-agents

# Check cache size
du -sh ${XDG_CACHE_HOME:-$HOME/.cache}/claude-agents

# List cached files
ls -lh ${XDG_CACHE_HOME:-$HOME/.cache}/claude-agents

# Clear cache manually
rm -rf ${XDG_CACHE_HOME:-$HOME/.cache}/claude-agents/*

# Or use the built-in flag
bash scripts/recommend_agents.sh --clear-cache
```

### Network Reliability Features

**Automatic Backup & Rollback**:
- Updates create backups before modifying files
- Failed updates automatically restore from backup
- Backup location: `.claude/agents/.backup_<timestamp>/`

**Update Safety**:
```bash
# Check for updates (uses 1-hour cache)
bash scripts/recommend_agents.sh --check-updates

# Update all agents with automatic backup/rollback
bash scripts/recommend_agents.sh --update-all

# If update fails, original files are automatically restored
```

**Verbose Logging**:
```bash
# See detailed network operations
bash scripts/recommend_agents.sh --verbose

# Output includes:
# - Each download attempt with URL
# - Cache hit/miss information
# - HTTP status codes
# - Retry timing
```

## Troubleshooting

### Network & Connectivity Issues

#### Intermittent network failures
**Problem**: Downloads fail occasionally due to network instability

**Solutions**:
- The script automatically retries 3 times with exponential backoff
- Wait for automatic retry completion before interrupting
- Use `--verbose` to see detailed retry attempts
- Check network stability: `ping -c 5 raw.githubusercontent.com`

#### Slow or timeout errors
**Problem**: Downloads timeout after 30 seconds

**Solutions**:
- Check your internet connection speed
- Verify you're not behind a restrictive firewall
- Try again during off-peak hours
- Use cached data if available (script uses cache automatically)
- Consider using `--cache-expiry=604800` (1 week) for slower connections

#### Proxy or firewall blocking
**Problem**: Downloads fail with connection refused or timeout

**Solutions**:
- Configure proxy settings in your environment:
  ```bash
  export http_proxy=http://proxy.example.com:8080
  export https_proxy=http://proxy.example.com:8080
  bash scripts/recommend_agents.sh
  ```
- Check firewall rules for `raw.githubusercontent.com`
- Contact your network administrator if corporate firewall blocks GitHub
- Use `--cache-dir` to specify a location accessible through your network

#### CI/CD environment failures
**Problem**: Script fails in automated CI/CD pipelines

**Solutions**:
- Use caching to reduce network dependency:
  ```yaml
  # GitHub Actions example
  - name: Cache agent files
    uses: actions/cache@v3
    with:
      path: ~/.cache/claude-agents
      key: claude-agents-${{ hashFiles('**/recommend_agents.sh') }}
  ```
- Set longer cache expiry for CI: `--cache-expiry=604800`
- Use `--force-refresh` only when necessary
- Implement retry logic in CI scripts if needed

### Agent Recommendation Script Issues

#### Script fails to download agents
**Problem**: Network errors or HTTP 404/403 errors

**Solutions**:
- Check your internet connection
- Verify the repository is accessible: `curl -I https://raw.githubusercontent.com/daryllundy/claude-agents/main/.claude/agents/AGENTS_REGISTRY.md`
- Try with `--branch main` to explicitly specify the branch
- Use `--repo` flag to specify an alternative repository URL
- The script automatically retries failed downloads 3 times with exponential backoff
- Check cache for existing data: `ls -lh ~/.cache/claude-agents`
- Use `--verbose` to see detailed error information

#### No agents recommended for my project
**Problem**: Script shows "No agents met the confidence threshold"

**Solutions**:
- Lower the confidence threshold: `--min-confidence 15`
- Use `--verbose` to see which patterns were checked
- Check if your project files are in the current directory (script scans from where it's run)
- For empty or new projects, the script recommends core agents (code-review, refactoring, test specialists)

#### Interactive mode not working
**Problem**: Arrow keys or keyboard input not responding

**Solutions**:
- Ensure you're running in a terminal that supports ANSI escape sequences
- Try running directly instead of through `curl | bash`: `bash scripts/recommend_agents.sh --interactive`
- Use standard mode without `--interactive` flag

#### Export/Import fails
**Problem**: JSON export or import errors

**Solutions**:
- For export: Ensure the target directory exists
- For import: Verify the JSON file is valid with `cat profile.json | jq` (if jq is installed)
- Use `--force` to overwrite existing export files
- Check file permissions for read/write access

#### Update detection shows false positives
**Problem**: `--check-updates` shows updates when agents are current

**Solutions**:
- This can happen if local files have different line endings or whitespace
- Use `--update-all` to ensure all agents are synchronized
- Backups are automatically created before updates in `.claude/agents/.backup_<timestamp>/`
- Clear cache and force refresh: `bash scripts/recommend_agents.sh --clear-cache && bash scripts/recommend_agents.sh --check-updates --force-refresh`

#### Cache issues or stale data
**Problem**: Script uses outdated cached data

**Solutions**:
- Clear the cache: `bash scripts/recommend_agents.sh --clear-cache`
- Force refresh to bypass cache: `bash scripts/recommend_agents.sh --force-refresh`
- Check cache age: `ls -lh ~/.cache/claude-agents`
- Reduce cache expiry: `bash scripts/recommend_agents.sh --cache-expiry=3600` (1 hour)
- Verify cache location: `echo ${XDG_CACHE_HOME:-$HOME/.cache}/claude-agents`

### Agent Invocation Issues

#### Claude Code doesn't recognize an agent
**Problem**: "Agent not found" or similar error

**Solutions**:
- Verify the agent file exists in `.claude/agents/`
- Check the filename matches the agent name (e.g., `docker-specialist.md`)
- Restart Claude Code to reload agent definitions
- Use exact agent names from AGENTS_REGISTRY.md

#### Agent doesn't have the expected expertise
**Problem**: Agent responses don't match the specialized domain

**Solutions**:
- Verify you're using the correct specialist (check AGENTS_REGISTRY.md)
- Provide more specific context in your request
- Check that the agent file hasn't been modified
- Re-download the agent with `--force` flag

### General Issues

#### Permission denied errors
**Problem**: Cannot create `.claude/agents/` directory

**Solutions**:
- Check write permissions in your project directory
- Run with appropriate permissions (avoid `sudo` unless necessary)
- Verify you're in the correct project directory

#### Script runs but no output
**Problem**: Script completes but shows no recommendations

**Solutions**:
- Remove `--dry-run` flag if you want to download agents
- Check that you're running from your project root directory
- Use `--verbose` to see detailed detection results
- Try `--min-confidence 0` to see all possible agents

For additional help, please open an issue on GitHub with:
- The command you ran
- The error message or unexpected behavior
- Your operating system and shell version
- Output of `bash scripts/recommend_agents.sh --verbose --dry-run` (if applicable)

## Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Beginner's guide to getting started
- **[CLAUDE_CODE_USAGE.md](CLAUDE_CODE_USAGE.md)** - Comprehensive usage guide with examples
- **[docs/NETWORK_OPERATIONS.md](docs/NETWORK_OPERATIONS.md)** - Network operations, retry logic, and caching guide
- **[.claude/agents/AGENTS_REGISTRY.md](.claude/agents/AGENTS_REGISTRY.md)** - Complete agent catalog
- **[examples/README.md](examples/README.md)** - Real-world usage examples and workflows
- **[archive/README.md](archive/README.md)** - Information about legacy implementations

## Testing

The project includes comprehensive test coverage for all functionality:

- **Unit Tests**: Test individual functions (detection, scoring, rendering, selection state)
- **Integration Tests**: Test complete workflows (detection, interactive mode, profiles)
- **Interactive Tests**: Automated testing of the TUI using expect

### Running Tests

```bash
# Run all tests
bash tests/run_all_tests.sh

# Run specific test suites
bash tests/unit/test_selection_state.sh
bash tests/unit/test_rendering.sh
bash tests/integration/test_interactive.sh
```

### Testing Requirements

- **bash** 4.0+ (required)
- **expect** (optional, for interactive mode tests)

Install expect:
```bash
# macOS
brew install expect

# Ubuntu/Debian
sudo apt-get install expect
```

For detailed testing documentation, see [docs/TESTING_INTERACTIVE_MODE.md](docs/TESTING_INTERACTIVE_MODE.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Ideas for contributions:
- Additional specialized agents
- Improved agent prompts
- More usage examples
- Documentation improvements
- Test coverage improvements

### Contribution Guidelines

1. Write tests for new features
2. Ensure all tests pass before submitting PR
3. Update documentation as needed
4. Follow existing code style and patterns

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

Built with Claude Code Pro by Anthropic

---

**Ready to supercharge your development workflow?** Start using these specialized agents in your Claude Code Pro session today!
