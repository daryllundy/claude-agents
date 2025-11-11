# Project Structure

## Directory Organization

```
claude-agents/
├── .claude/                          # Claude Code configuration
│   ├── agents/                       # Agent prompt definitions (24 agents)
│   │   ├── AGENTS_REGISTRY.md        # Complete agent catalog and reference
│   │   ├── e-commerce-coordinator.md # Orchestration agent
│   │   ├── docker-specialist.md      # Infrastructure agents
│   │   ├── security-specialist.md    # Quality agents
│   │   └── ...                       # Other specialized agents
│   ├── skills/                       # Skill definitions (7 skills)
│   │   ├── e-commerce-orchestrator/  # E-commerce audit and orchestration
│   │   ├── shopify-specialist/       # Shopify development
│   │   ├── web-design-specialist/    # Web design and UX
│   │   ├── instagram-specialist/     # Instagram marketing
│   │   ├── tiktok-strategist/        # TikTok marketing
│   │   ├── social-media-specialist/  # Multi-platform social media
│   │   └── zapier-specialist/        # Workflow automation
│   └── settings.local.json           # Claude Code settings
├── archive/                          # Legacy implementations (reference only)
│   ├── legacy-python-implementation/ # Original Python agents
│   └── legacy-setup/                 # Old setup scripts
├── examples/                         # Usage examples and workflows
├── scripts/                          # Utility scripts
│   └── recommend_agents.sh           # Agent recommendation script
├── README.md                         # Main documentation
├── GETTING_STARTED.md                # Beginner's guide
└── CLAUDE_CODE_USAGE.md              # Comprehensive usage guide
```

## Key Conventions

### Agent Organization (`.claude/agents/`)
- One markdown file per agent
- Naming: `{domain}-specialist.md` (e.g., `docker-specialist.md`)
- Categories: Infrastructure, Development, Quality, Operations, Productivity, Business, Specialized, Orchestration
- Each agent has defined tools: Read, Write, Edit, Bash, Glob, Grep

### Skill Organization (`.claude/skills/`)
- One folder per skill with `SKILL.md` inside
- Naming: `{domain}-specialist/` or `{domain}-strategist/`
- YAML frontmatter required: name, description, allowed-tools
- Auto-discovered by Claude Code based on context

### Documentation Structure
- **README.md**: Overview, quick start, agent categories, skills
- **GETTING_STARTED.md**: Step-by-step beginner guide
- **CLAUDE_CODE_USAGE.md**: Comprehensive usage patterns and examples
- **AGENTS_REGISTRY.md**: Complete agent reference and invocation patterns

### Archive Policy
- Legacy code preserved in `archive/` for reference
- Not required for current functionality
- Includes original Python implementation and setup scripts

## File Naming Patterns

- Agent files: `{specialty}-specialist.md` or `{specialty}-coordinator.md`
- Skill folders: `{specialty}-specialist/` or `{specialty}-strategist/`
- Documentation: Uppercase with underscores (e.g., `GETTING_STARTED.md`)
- Scripts: Lowercase with underscores (e.g., `recommend_agents.sh`)

## Important Files

- `.claude/agents/AGENTS_REGISTRY.md`: Central reference for all 24 agents
- `README.md`: Primary entry point with feature overview
- `CLAUDE_CODE_USAGE.md`: Detailed usage guide with real-world examples
- `.claude/settings.local.json`: Claude Code configuration
