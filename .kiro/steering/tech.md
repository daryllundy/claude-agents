# Technology Stack

## Project Type

Documentation and configuration repository for Claude Code Pro agents and skills.

## Structure

- **Agents**: Markdown prompt definitions in `.claude/agents/`
- **Skills**: Markdown skill definitions in `.claude/skills/` with YAML frontmatter
- **Documentation**: Markdown files for guides and references
- **Scripts**: Bash scripts for agent recommendation and setup

## File Formats

### Agent Files (`.claude/agents/*.md`)
- Pure markdown format
- Detailed prompt definitions with expertise, responsibilities, and tool access
- No frontmatter required

### Skill Files (`.claude/skills/*/SKILL.md`)
- Markdown with YAML frontmatter
- Frontmatter includes: `name`, `description`, `allowed-tools`
- Auto-discovered by Claude Code based on context

### Configuration
- `.claude/settings.local.json`: Claude Code settings
- No build system or compilation required

## Common Commands

### Agent Recommendation
```bash
# Run from target project root to recommend relevant agents
curl -sSL https://raw.githubusercontent.com/daryllundy/claude-agents/main/scripts/recommend_agents.sh | bash
```

### Repository Setup
```bash
# Clone repository
git clone https://github.com/daryllundy/claude-agents.git

# No installation or build steps required
```

## Dependencies

- **Runtime**: Claude Code Pro subscription (required)
- **No Python dependencies**: Legacy Python implementation archived
- **No API keys**: Works directly with Claude Code Pro
- **No build tools**: Pure markdown and configuration files

## Legacy Stack (Archived)

The `archive/legacy-python-implementation/` contains the original Python-based system:
- Python 3.x
- Anthropic API
- Custom agent classes and orchestrator
- Not required for current usage
