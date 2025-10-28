#!/usr/bin/env bash
set -euo pipefail

# Script to scan a project and download recommended Claude Code agent prompts.
# Intended usage:
#   curl -sSL https://raw.githubusercontent.com/daryllundy/claude-agents/main/scripts/recommend_agents.sh | bash
# If you clone the claude-agents repository locally you can also run the script directly.

REPO_SLUG="daryllundy/claude-agents"
DEFAULT_BRANCH="main"

CLAUDE_AGENTS_BRANCH="${CLAUDE_AGENTS_BRANCH:-$DEFAULT_BRANCH}"
CLAUDE_AGENTS_REPO="${CLAUDE_AGENTS_REPO:-https://raw.githubusercontent.com/${REPO_SLUG}}"
BASE_URL="${CLAUDE_AGENTS_REPO}/${CLAUDE_AGENTS_BRANCH}/.claude/agents"

AGENTS_DIR=".claude/agents"
DRY_RUN=false

print_help() {
  cat <<'USAGE'
Claude Code Agent Recommender
=============================

Scans the current project and downloads Claude Code agent prompt files that
match the detected technologies.

Usage:
  recommend_agents.sh [options]

Options:
  --dry-run      Only print recommended agents without downloading.
  --force        Redownload agent files even if they already exist locally.
  --branch NAME  Override the claude-agents branch to download from.
  --repo URL     Override the base raw URL for the claude-agents repository.
  -h, --help     Show this help message.

Environment variables:
  CLAUDE_AGENTS_BRANCH  Override the branch (default: main).
  CLAUDE_AGENTS_REPO    Override the raw content base URL.

USAGE
}

FORCE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --force)
      FORCE=true
      shift
      ;;
    --branch)
      shift
      [[ $# -gt 0 ]] || { echo "Missing value for --branch" >&2; exit 1; }
      CLAUDE_AGENTS_BRANCH="$1"
      BASE_URL="${CLAUDE_AGENTS_REPO}/${CLAUDE_AGENTS_BRANCH}/.claude/agents"
      shift
      ;;
    --repo)
      shift
      [[ $# -gt 0 ]] || { echo "Missing value for --repo" >&2; exit 1; }
      CLAUDE_AGENTS_REPO="$1"
      BASE_URL="${CLAUDE_AGENTS_REPO}/${CLAUDE_AGENTS_BRANCH}/.claude/agents"
      shift
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      print_help >&2
      exit 1
      ;;
  esac
done

log() {
  printf '[agent-setup] %s\n' "$*"
}

has_file() {
  local pattern="$1"
  find . -path './.git' -prune -o -name "$pattern" -print -quit | grep -q .
}

has_path() {
  local path="$1"
  if [[ -d "$path" ]]; then
    return 0
  fi
  if [[ "$path" == */* ]]; then
    find . -path './.git' -prune -o -path "./$path" -print -quit | grep -q .
  else
    find . -path './.git' -prune -o -type d -name "$path" -print -quit | grep -q .
  fi
}

file_contains() {
  local file="$1"
  local pattern="$2"
  if [[ -f "$file" ]]; then
    if command -v rg >/dev/null 2>&1; then
      rg --quiet --fixed-strings "$pattern" "$file"
      return $?
    else
      grep -qF "$pattern" "$file"
      return $?
    fi
  fi
  return 1
}

search_contents() {
  local pattern="$1"
  if command -v rg >/dev/null 2>&1; then
    rg --quiet --fixed-strings "$pattern" --glob '!*.git/*' .
    return $?
  else
    grep -Rqs --exclude-dir='.git' "$pattern" .
    return $?
  fi
}

recommended_agents=()
add_agent() {
  local agent="$1"
  for existing in "${recommended_agents[@]:-}"; do
    [[ "$existing" == "$agent" ]] && return
  done
  recommended_agents+=("$agent")
}

# Infrastructure
if has_file 'Dockerfile' || has_file 'docker-compose.yml' || has_file 'Containerfile'; then
  add_agent 'docker-specialist'
fi

if has_path '.github/workflows' || has_file '.gitlab-ci.yml' || has_path '.circleci' || has_file 'azure-pipelines.yml'; then
  add_agent 'devops-specialist'
fi

if has_path 'terraform' || search_contents 'prometheus' || search_contents 'grafana' || search_contents 'opentelemetry'; then
  add_agent 'observability-specialist'
fi

# Development
if has_file 'schema.prisma' || has_path 'migrations' || search_contents 'CREATE TABLE' || search_contents 'SELECT *'; then
  add_agent 'database-specialist'
fi

if file_contains 'package.json' 'react' || file_contains 'package.json' 'next' || file_contains 'package.json' 'vue' || has_path 'src/components' || has_path 'frontend'; then
  add_agent 'frontend-specialist'
fi

if has_path 'android' || has_path 'ios' || has_file 'pubspec.yaml' || search_contents 'ReactNative'; then
  add_agent 'mobile-specialist'
fi

# Quality
if has_path 'tests' || has_path '__tests__' || has_path 'spec' || has_file 'pytest.ini' || has_file 'playwright.config.ts'; then
  add_agent 'test-specialist'
fi

if search_contents 'jwt' || search_contents 'bcrypt' || search_contents 'helmet' || search_contents 'csrf'; then
  add_agent 'security-specialist'
fi

if has_file '.codeclimate.yml' || search_contents 'TODO:' || search_contents 'refactor'; then
  add_agent 'code-review-specialist'
fi

if search_contents 'technical debt' || search_contents 'legacy code' || has_path 'src/legacy'; then
  add_agent 'refactoring-specialist'
fi

if search_contents 'performance' || search_contents 'profiling' || search_contents 'latency'; then
  add_agent 'performance-specialist'
fi

# Operations
if has_path 'migrations' || has_path 'db/migrate' || has_path 'prisma/migrations'; then
  add_agent 'migration-specialist'
fi

if has_file 'package-lock.json' || has_file 'yarn.lock' || has_file 'pnpm-lock.yaml' || has_file 'requirements.txt' || has_file 'poetry.lock'; then
  add_agent 'dependency-specialist'
fi

if has_file '.gitmodules' || has_path '.git/hooks'; then
  add_agent 'git-specialist'
fi

# Productivity
if has_path 'scripts/scaffold' || has_path 'templates' || search_contents 'plopfile' || search_contents 'scaffold'; then
  add_agent 'scaffolding-specialist'
fi

if has_path 'docs' || has_file 'mkdocs.yml' || has_file 'docusaurus.config.js'; then
  add_agent 'documentation-specialist'
fi

if search_contents 'sentry' || search_contents 'bugsnag' || search_contents 'logger.error'; then
  add_agent 'debugging-specialist'
fi

# Business
if search_contents 'validation' || search_contents 'schema validation' || search_contents 'yup' || search_contents 'zod'; then
  add_agent 'validation-specialist'
fi

if has_file 'architecture.md' || search_contents 'architecture decision record' || search_contents 'ADR '; then
  add_agent 'architecture-specialist'
fi

if has_path 'i18n' || has_path 'locales' || has_file '.i18nrc' || search_contents 'react-intl'; then
  add_agent 'localization-specialist'
fi

if search_contents 'gdpr' || search_contents 'hipaa' || search_contents 'pci-dss' || search_contents 'soc 2'; then
  add_agent 'compliance-specialist'
fi

# Specialized
if has_path 'notebooks' || has_file 'environment.yml' || search_contents 'pandas' || search_contents 'scikit-learn'; then
  add_agent 'data-science-specialist'
fi

if [[ ${#recommended_agents[@]} -eq 0 ]]; then
  log "No technology-specific signals found. Recommending core agents."
  recommended_agents=(
    'code-review-specialist'
    'refactoring-specialist'
    'test-specialist'
  )
fi

log "Recommended agents: ${recommended_agents[*]}"

if $DRY_RUN; then
  exit 0
fi

mkdir -p "$AGENTS_DIR"

fetch_agent() {
  local agent="$1"
  local url="${BASE_URL}/${agent}.md"
  local dest="${AGENTS_DIR}/${agent}.md"

  if [[ -f "$dest" && $FORCE == false ]]; then
    log "Skipping ${agent} (already exists). Use --force to redownload."
    return
  fi

  log "Downloading ${agent} from ${url}"
  if ! curl -fsSL "$url" -o "$dest"; then
    echo "Failed to download ${agent} from ${url}" >&2
    return 1
  fi
}

for agent in "${recommended_agents[@]}"; do
  fetch_agent "$agent"
done

# Always include the registry for reference
REGISTRY_DEST="${AGENTS_DIR}/AGENTS_REGISTRY.md"
if [[ ! -f "$REGISTRY_DEST" || $FORCE == true ]]; then
  REGISTRY_URL="${BASE_URL}/AGENTS_REGISTRY.md"
  log "Downloading agent registry"
  curl -fsSL "$REGISTRY_URL" -o "$REGISTRY_DEST"
else
  log "Agent registry already present. Use --force to redownload."
fi

log "All done! Agent prompts are located in ${AGENTS_DIR}"
