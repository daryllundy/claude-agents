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

# Agent metadata storage
declare -A AGENT_CATEGORIES
declare -A AGENT_DESCRIPTIONS
declare -A AGENT_USE_CASES

# Detection pattern storage (format: "type:pattern:weight" per line)
declare -A AGENT_PATTERNS

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

# Parse AGENTS_REGISTRY.md to extract agent metadata
parse_agent_registry() {
  local registry_file="${AGENTS_DIR}/AGENTS_REGISTRY.md"
  
  # If registry doesn't exist locally, try to fetch it
  if [[ ! -f "$registry_file" ]]; then
    log "Agent registry not found locally, attempting to fetch..."
    mkdir -p "$AGENTS_DIR"
    local registry_url="${BASE_URL}/AGENTS_REGISTRY.md"
    if ! curl -fsSL "$registry_url" -o "$registry_file" 2>/dev/null; then
      log "Warning: Could not fetch agent registry. Using built-in metadata."
      return 1
    fi
  fi
  
  local current_agent=""
  local in_agent_section=false
  
  while IFS= read -r line; do
    # Parse agent headers (#### N. agent-name)
    if [[ $line =~ ^####[[:space:]]+[0-9]+\.[[:space:]]+(.+)$ ]]; then
      current_agent="${BASH_REMATCH[1]}"
      in_agent_section=true
      continue
    fi
    
    # Exit agent section when we hit a new major section
    if [[ $line =~ ^##[[:space:]]+ ]] && [[ ! $line =~ ^####[[:space:]]+ ]]; then
      in_agent_section=false
      current_agent=""
      continue
    fi
    
    # Only parse metadata if we're in an agent section
    if [[ -n "$current_agent" ]] && [[ "$in_agent_section" == true ]]; then
      # Parse category
      if [[ $line =~ ^\*\*Category\*\*:[[:space:]]+(.+)$ ]]; then
        AGENT_CATEGORIES[$current_agent]="${BASH_REMATCH[1]}"
      fi
      
      # Parse description
      if [[ $line =~ ^\*\*Description\*\*:[[:space:]]+(.+)$ ]]; then
        AGENT_DESCRIPTIONS[$current_agent]="${BASH_REMATCH[1]}"
      fi
      
      # Parse use cases
      if [[ $line =~ ^\*\*Use\ for\*\*:[[:space:]]+(.+)$ ]]; then
        AGENT_USE_CASES[$current_agent]="${BASH_REMATCH[1]}"
      fi
    fi
  done < "$registry_file"
  
  return 0
}

# Initialize detection patterns for all 30 agents
# Pattern format: "type:pattern:weight" (one per line)
# Types: file, path, content
# Weight: 0-25 (contribution to confidence score)
initialize_detection_patterns() {
  # Infrastructure Agents
  
  AGENT_PATTERNS["devops-orchestrator"]="
path:.github/workflows:5
path:.gitlab-ci:5
file:Jenkinsfile:5
path:terraform:5
file:*.tf:5
path:k8s:5
path:kubernetes:5
file:prometheus.yml:5
path:ansible:5
"

  AGENT_PATTERNS["aws-specialist"]="
file:*.tf:10
content:provider \"aws\":20
content:aws_:15
file:cloudformation.yaml:15
file:cloudformation.yml:15
file:cdk.json:15
path:.aws:10
content:AWS::CloudFormation:15
"

  AGENT_PATTERNS["azure-specialist"]="
file:*.bicep:20
file:azuredeploy.json:15
content:deploymentTemplate:15
file:azure-pipelines.yml:15
content:azurerm:15
content:Microsoft.Compute:10
"

  AGENT_PATTERNS["gcp-specialist"]="
file:app.yaml:15
path:.config/gcloud:10
content:provider \"google\":20
content:google_:15
file:deployment-manager.yaml:15
content:gcp.googleapis.com:10
"

  AGENT_PATTERNS["terraform-specialist"]="
file:*.tf:20
file:*.tfvars:15
file:terraform.tfstate:25
file:.terraform.lock.hcl:15
path:.terraform:15
content:terraform:10
"

  AGENT_PATTERNS["ansible-specialist"]="
file:ansible.cfg:20
file:playbook.yml:15
file:playbook.yaml:15
path:roles:15
path:inventory:10
file:requirements.yml:10
content:ansible.builtin:15
"

  AGENT_PATTERNS["cicd-specialist"]="
path:.github/workflows:20
file:.gitlab-ci.yml:20
file:Jenkinsfile:20
path:.circleci:20
file:azure-pipelines.yml:20
file:.travis.yml:15
content:pipeline:10
"

  AGENT_PATTERNS["kubernetes-specialist"]="
path:k8s:20
path:kubernetes:20
file:Chart.yaml:20
file:values.yaml:15
file:kustomization.yaml:20
content:apiVersion:10
content:kind: Deployment:15
"

  AGENT_PATTERNS["monitoring-specialist"]="
file:prometheus.yml:20
path:prometheus:15
path:grafana:15
file:grafana.ini:15
file:elasticsearch.yml:15
file:logstash.conf:15
file:kibana.yml:15
content:metrics:10
"

  AGENT_PATTERNS["docker-specialist"]="
file:Dockerfile:25
file:docker-compose.yml:20
file:docker-compose.yaml:20
file:.dockerignore:10
file:Containerfile:20
content:FROM:10
"

  AGENT_PATTERNS["observability-specialist"]="
content:prometheus:15
content:grafana:15
content:opentelemetry:20
content:jaeger:15
content:zipkin:15
path:monitoring:10
"

  # Development Agents
  
  AGENT_PATTERNS["database-specialist"]="
file:schema.prisma:20
path:migrations:15
path:db/migrate:15
file:*.sql:10
content:CREATE TABLE:15
content:SELECT:5
content:prisma:10
"

  AGENT_PATTERNS["frontend-specialist"]="
content:react:15
content:vue:15
content:angular:15
content:next:15
path:src/components:15
path:components:10
path:frontend:10
file:package.json:5
"

  AGENT_PATTERNS["mobile-specialist"]="
path:android:20
path:ios:20
file:pubspec.yaml:20
content:ReactNative:20
content:Flutter:15
file:Podfile:15
file:build.gradle:10
"

  # Quality Agents
  
  AGENT_PATTERNS["test-specialist"]="
path:tests:15
path:__tests__:15
path:spec:15
file:pytest.ini:15
file:jest.config.js:15
file:vitest.config.ts:15
file:playwright.config.ts:15
content:describe(:10
"

  AGENT_PATTERNS["security-specialist"]="
content:jwt:10
content:bcrypt:10
content:helmet:10
content:csrf:10
content:authentication:10
content:authorization:10
file:security.yml:15
"

  AGENT_PATTERNS["code-review-specialist"]="
file:.codeclimate.yml:15
content:TODO::10
content:FIXME::10
content:refactor:10
file:.eslintrc:10
file:.prettierrc:10
"

  AGENT_PATTERNS["refactoring-specialist"]="
content:technical debt:15
content:legacy code:15
path:src/legacy:20
path:legacy:15
content:deprecated:10
content:refactor:10
"

  AGENT_PATTERNS["performance-specialist"]="
content:performance:15
content:profiling:15
content:latency:10
content:optimization:10
content:cache:10
file:lighthouse.config.js:15
"

  # Operations Agents
  
  AGENT_PATTERNS["migration-specialist"]="
path:migrations:20
path:db/migrate:20
path:prisma/migrations:20
file:*migration*.sql:15
content:ALTER TABLE:15
content:migration:10
"

  AGENT_PATTERNS["dependency-specialist"]="
file:package-lock.json:15
file:yarn.lock:15
file:pnpm-lock.yaml:15
file:requirements.txt:15
file:poetry.lock:15
file:Gemfile.lock:15
file:go.sum:15
"

  AGENT_PATTERNS["git-specialist"]="
file:.gitmodules:20
path:.git/hooks:15
file:.gitattributes:10
content:submodule:15
file:.gitmessage:10
"

  # Productivity Agents
  
  AGENT_PATTERNS["scaffolding-specialist"]="
path:scripts/scaffold:20
path:templates:15
content:plopfile:20
content:scaffold:15
file:generator.js:15
path:blueprints:15
"

  AGENT_PATTERNS["documentation-specialist"]="
path:docs:15
file:mkdocs.yml:20
file:docusaurus.config.js:20
file:README.md:5
path:documentation:15
file:.readthedocs.yml:15
"

  AGENT_PATTERNS["debugging-specialist"]="
content:sentry:15
content:bugsnag:15
content:logger.error:10
content:console.error:5
content:debugger:10
file:.sentryclirc:15
"

  # Business Agents
  
  AGENT_PATTERNS["validation-specialist"]="
content:validation:15
content:schema validation:15
content:yup:15
content:zod:15
content:joi:15
content:validator:10
"

  AGENT_PATTERNS["architecture-specialist"]="
file:architecture.md:20
content:architecture decision record:20
content:ADR:15
path:docs/architecture:15
path:adr:20
"

  AGENT_PATTERNS["localization-specialist"]="
path:i18n:20
path:locales:20
file:.i18nrc:15
content:react-intl:15
content:i18next:15
content:translation:10
"

  AGENT_PATTERNS["compliance-specialist"]="
content:gdpr:15
content:hipaa:15
content:pci-dss:15
content:soc 2:15
content:compliance:10
path:compliance:15
"

  # Specialized Agents
  
  AGENT_PATTERNS["data-science-specialist"]="
path:notebooks:20
file:environment.yml:15
content:pandas:15
content:scikit-learn:15
content:tensorflow:15
content:pytorch:15
file:*.ipynb:20
"
}

recommended_agents=()
add_agent() {
  local agent="$1"
  for existing in "${recommended_agents[@]:-}"; do
    [[ "$existing" == "$agent" ]] && return
  done
  recommended_agents+=("$agent")
}

# Calculate confidence score for an agent (0-100)
declare -A agent_confidence
declare -A agent_matched_patterns

calculate_confidence() {
  local agent="$1"
  local total_weight=0
  local max_possible_weight=100
  local matched_patterns=()
  
  # Get detection patterns for this agent
  local patterns="${AGENT_PATTERNS[$agent]}"
  
  # Parse and execute each pattern
  while IFS= read -r pattern_line; do
    # Skip empty lines
    [[ -z "$pattern_line" ]] && continue
    
    # Trim whitespace from line
    pattern_line=$(echo "$pattern_line" | xargs)
    [[ -z "$pattern_line" ]] && continue
    
    # Parse pattern: type:pattern:weight
    # Extract type (first field before :)
    type="${pattern_line%%:*}"
    # Remove type and first colon
    rest="${pattern_line#*:}"
    # Extract weight (last field after last :)
    weight="${rest##*:}"
    # Extract pattern (everything between type and weight)
    pattern="${rest%:*}"
    
    # Skip if any field is empty
    [[ -z "$type" || -z "$pattern" || -z "$weight" ]] && continue
    
    # Validate weight is a number
    if ! [[ "$weight" =~ ^[0-9]+$ ]]; then
      continue
    fi
    
    # Execute detection based on type
    case "$type" in
      file)
        if has_file "$pattern"; then
          total_weight=$((total_weight + weight))
          matched_patterns+=("file:$pattern")
        fi
        ;;
      path)
        if has_path "$pattern"; then
          total_weight=$((total_weight + weight))
          matched_patterns+=("path:$pattern")
        fi
        ;;
      content)
        if search_contents "$pattern"; then
          total_weight=$((total_weight + weight))
          matched_patterns+=("content:$pattern")
        fi
        ;;
    esac
  done <<< "$patterns"
  
  # Calculate percentage score
  local confidence=0
  if [[ $max_possible_weight -gt 0 ]]; then
    confidence=$((total_weight * 100 / max_possible_weight))
  fi
  
  # Cap at 100
  [[ $confidence -gt 100 ]] && confidence=100
  
  # Store results
  agent_confidence[$agent]=$confidence
  agent_matched_patterns[$agent]="${matched_patterns[*]}"
  
  echo "$confidence"
}

# Initialize detection patterns
initialize_detection_patterns

# Parse agent registry for metadata
parse_agent_registry

# Run detection for all agents
log "Scanning project for technology signals..."

for agent in "${!AGENT_PATTERNS[@]}"; do
  # Calculate confidence (stores in agent_confidence array)
  calculate_confidence "$agent" > /dev/null
  
  # Get the stored confidence
  confidence="${agent_confidence[$agent]:-0}"
  
  # Add agents with confidence >= 25% (suggested threshold)
  if [[ $confidence -ge 25 ]]; then
    add_agent "$agent"
  fi
done

# If no agents detected, recommend core agents
if [[ ${#recommended_agents[@]} -eq 0 ]]; then
  log "No technology-specific signals found. Recommending core agents."
  recommended_agents=(
    'code-review-specialist'
    'refactoring-specialist'
    'test-specialist'
  )
  # Set default confidence for core agents
  agent_confidence['code-review-specialist']=50
  agent_confidence['refactoring-specialist']=50
  agent_confidence['test-specialist']=50
fi

# Sort agents by confidence score (descending)
IFS=$'\n' sorted_agents=($(
  for agent in "${recommended_agents[@]}"; do
    echo "${agent_confidence[$agent]:-0}:$agent"
  done | sort -rn | cut -d: -f2
))
unset IFS

recommended_agents=("${sorted_agents[@]}")

log "Recommended agents (${#recommended_agents[@]} total):"
for agent in "${recommended_agents[@]}"; do
  confidence="${agent_confidence[$agent]:-0}"
  log "  - $agent (confidence: ${confidence}%)"
done

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
