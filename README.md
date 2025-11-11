# Claude Code Agents

A comprehensive collection of specialized AI agents and skills designed for **Claude Code Pro** users. These agents and skills work as intelligent sub-agents that can be invoked within Claude Code to handle specific development, marketing, and e-commerce tasks with deep domain expertise.

## What's New: E-Commerce Orchestration System

The newest and most powerful feature of this collection is the **intelligent orchestration system** for e-commerce transformation:

- **E-Commerce Orchestrator Skill**: Automatically analyzes e-commerce websites, scores them across 6 critical dimensions, and recommends the right specialists at the right time
- **E-Commerce Coordinator Agent**: Orchestrates multi-week transformation projects, tracking progress and coordinating specialist consultations
- **6-Dimensional Scoring**: Design & UX, Platform Optimization, Marketing, Social Media, Automation, and Performance
- **Auto-Discovery**: Simply paste an e-commerce URL and watch the orchestrator identify issues and route to specialists
- **Proven Workflow Patterns**: Pre-configured sequences for new launches, store revivals, scaling, and market expansion

**Example**: "Analyze https://mystore.com" → Orchestrator identifies issues → Routes to web-design-specialist, shopify-specialist, instagram-specialist, and zapier-specialist in the optimal sequence → Tracks results and ROI.

## Features

- **24 Specialized Agents** organized into 8 categories (including orchestration)
- **7 Claude Code Skills** for specialized marketing, e-commerce, and orchestration
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

### Example 5: E-Commerce Transformation
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
