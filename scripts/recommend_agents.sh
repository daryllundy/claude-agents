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
  --dry-run              Only print recommended agents without downloading.
  --force                Redownload agent files even if they already exist locally.
  --min-confidence NUM   Only recommend agents with confidence >= NUM (0-100).
  --verbose              Display detailed detection results with all patterns checked.
  --interactive          Enter interactive mode to manually select agents.
  --export FILE          Export detection profile to JSON file.
  --import FILE          Import and install agents from a profile JSON file.
  --check-updates        Check for updates to locally installed agents.
  --update-all           Update all locally installed agents to latest versions.
  --branch NAME          Override the claude-agents branch to download from.
  --repo URL             Override the base raw URL for the claude-agents repository.
  -h, --help             Show this help message.

Environment variables:
  CLAUDE_AGENTS_BRANCH  Override the branch (default: main).
  CLAUDE_AGENTS_REPO    Override the raw content base URL.

USAGE
}

FORCE=false
MIN_CONFIDENCE=25  # Default minimum confidence threshold
VERBOSE=false
INTERACTIVE=false
EXPORT_FILE=""
IMPORT_FILE=""
CHECK_UPDATES=false
UPDATE_ALL=false

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
    --verbose)
      VERBOSE=true
      shift
      ;;
    --interactive)
      INTERACTIVE=true
      shift
      ;;
    --export)
      shift
      [[ $# -gt 0 ]] || { echo "Missing value for --export" >&2; exit 1; }
      EXPORT_FILE="$1"
      shift
      ;;
    --import)
      shift
      [[ $# -gt 0 ]] || { echo "Missing value for --import" >&2; exit 1; }
      IMPORT_FILE="$1"
      shift
      ;;
    --check-updates)
      CHECK_UPDATES=true
      shift
      ;;
    --update-all)
      UPDATE_ALL=true
      shift
      ;;
    --min-confidence)
      shift
      [[ $# -gt 0 ]] || { echo "Missing value for --min-confidence" >&2; exit 1; }
      if ! [[ "$1" =~ ^[0-9]+$ ]] || [[ "$1" -lt 0 ]] || [[ "$1" -gt 100 ]]; then
        echo "Error: --min-confidence must be a number between 0 and 100" >&2
        exit 1
      fi
      MIN_CONFIDENCE="$1"
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

# Enhanced error handling (Task 11)

# Network error handling with retry and exponential backoff
fetch_with_retry() {
  local url="$1"
  local output="$2"
  local max_attempts=3
  local attempt=1
  local backoff=2

  while [[ $attempt -le $max_attempts ]]; do
    # Try to fetch with timeout
    if curl -fsSL --max-time 30 "$url" -o "$output" 2>/dev/null; then
      return 0
    fi

    # Get HTTP status code for better error messages
    local http_code=$(curl -fsSL -w "%{http_code}" --max-time 30 -o /dev/null "$url" 2>/dev/null || echo "000")

    if [[ $attempt -lt $max_attempts ]]; then
      log "Attempt $attempt/$max_attempts failed (HTTP $http_code). Retrying in ${backoff}s..."
      sleep $backoff
      ((backoff *= 2))  # Exponential backoff
      ((attempt++))
    else
      echo "Error: Failed to download from $url after $max_attempts attempts (HTTP $http_code)" >&2

      # Provide troubleshooting suggestions based on error code
      case "$http_code" in
        000)
          echo "Troubleshooting: Check your internet connection and try again" >&2
          ;;
        404)
          echo "Troubleshooting: The agent file was not found. It may have been removed or renamed" >&2
          ;;
        403|401)
          echo "Troubleshooting: Access denied. Check if the repository is accessible" >&2
          ;;
        500|502|503|504)
          echo "Troubleshooting: Server error. The repository may be temporarily unavailable" >&2
          ;;
        *)
          echo "Troubleshooting: Unexpected error. Please check the repository URL and try again" >&2
          ;;
      esac

      return 1
    fi
  done

  return 1
}

# Input validation
validate_arguments() {
  # Check for mutually exclusive flags
  local mode_count=0
  [[ -n "$IMPORT_FILE" ]] && ((mode_count++))
  [[ $CHECK_UPDATES == true ]] && ((mode_count++))
  [[ $UPDATE_ALL == true ]] && ((mode_count++))

  if [[ $mode_count -gt 1 ]]; then
    echo "Error: --import, --check-updates, and --update-all are mutually exclusive" >&2
    echo "Use only one of these flags at a time" >&2
    exit 1
  fi

  # Validate min-confidence already done in argument parsing

  # Validate export file path
  if [[ -n "$EXPORT_FILE" ]]; then
    local export_dir=$(dirname "$EXPORT_FILE")
    if [[ ! -d "$export_dir" ]] && [[ "$export_dir" != "." ]]; then
      echo "Error: Export directory does not exist: $export_dir" >&2
      echo "Please create the directory first or specify a valid path" >&2
      exit 1
    fi
  fi

  # Validate import file existence
  if [[ -n "$IMPORT_FILE" ]] && [[ ! -f "$IMPORT_FILE" ]]; then
    echo "Error: Import file not found: $IMPORT_FILE" >&2
    echo "Please check the file path and try again" >&2
    exit 1
  fi
}

# Call validation after argument parsing
validate_arguments

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

# Enhanced output formatting functions (Task 6)

# Draw a progress bar for confidence visualization
draw_progress_bar() {
  local confidence="$1"
  local bar_length=20
  local filled=$((confidence * bar_length / 100))
  local empty=$((bar_length - filled))

  printf "["
  for ((i=0; i<filled; i++)); do printf "█"; done
  for ((i=0; i<empty; i++)); do printf "░"; done
  printf "]"
}

# Get recommendation symbol based on confidence
get_recommendation_symbol() {
  local confidence="$1"
  if [[ $confidence -ge 50 ]]; then
    echo "✓"  # Recommended
  else
    echo "~"  # Suggested
  fi
}

# Display agent with details
display_agent_details() {
  local agent="$1"
  local confidence="${agent_confidence[$agent]:-0}"
  local symbol=$(get_recommendation_symbol "$confidence")
  local description="${AGENT_DESCRIPTIONS[$agent]:-No description available}"
  local matched_patterns="${agent_matched_patterns[$agent]:-}"

  printf "  %s %s " "$symbol" "$agent"
  draw_progress_bar "$confidence"
  printf " %d%%\n" "$confidence"

  # Show description
  if [[ -n "$description" ]]; then
    printf "    %s\n" "$description"
  fi

  # Show matched patterns if not verbose (verbose shows all patterns later)
  if [[ ! $VERBOSE == true ]] && [[ -n "$matched_patterns" ]]; then
    printf "    Detected: %s\n" "$matched_patterns"
  fi

  echo ""
}

# Display categorized results
display_categorized_results() {
  # Define category order
  local -a categories=(
    "Infrastructure (Cloud)"
    "Infrastructure (IaC)"
    "Infrastructure (Platform)"
    "Infrastructure (Containers)"
    "Infrastructure (Monitoring)"
    "Development"
    "Quality"
    "Operations"
    "Productivity"
    "Business"
    "Specialized"
  )

  echo ""
  echo "═══════════════════════════════════════════════════════════════════════"
  echo "                     Agent Recommendation Results"
  echo "═══════════════════════════════════════════════════════════════════════"
  echo ""
  echo "Found ${#recommended_agents[@]} recommended agents"
  echo ""

  # Group agents by category
  declare -A category_agents
  for agent in "${recommended_agents[@]}"; do
    local category="${AGENT_CATEGORIES[$agent]:-Uncategorized}"
    if [[ -z "${category_agents[$category]}" ]]; then
      category_agents[$category]="$agent"
    else
      category_agents[$category]="${category_agents[$category]} $agent"
    fi
  done

  # Display agents by category
  for category in "${categories[@]}"; do
    if [[ -n "${category_agents[$category]}" ]]; then
      # Split agents string into array
      IFS=' ' read -ra agents <<< "${category_agents[$category]}"

      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      echo "$category (${#agents[@]} agent(s))"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      echo ""

      for agent in "${agents[@]}"; do
        display_agent_details "$agent"
      done
    fi
  done

  # Display uncategorized agents if any
  if [[ -n "${category_agents[Uncategorized]}" ]]; then
    IFS=' ' read -ra agents <<< "${category_agents[Uncategorized]}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Other (${#agents[@]} agent(s))"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    for agent in "${agents[@]}"; do
      display_agent_details "$agent"
    done
  fi

  echo "═══════════════════════════════════════════════════════════════════════"
  echo ""
  echo "Legend:"
  echo "  ✓ = Recommended (50%+)    ~ = Suggested (25-49%)"
  echo ""
}

# Interactive selection mode (Task 7)
interactive_selection() {
  local -a agent_list=("${recommended_agents[@]}")
  local -A selected_agents
  local current_index=0

  # Pre-select agents above 50% confidence
  for agent in "${agent_list[@]}"; do
    local confidence="${agent_confidence[$agent]:-0}"
    if [[ $confidence -ge 50 ]]; then
      selected_agents[$agent]=1
    fi
  done

  # Function to display the interactive UI
  display_interactive_ui() {
    clear
    echo "═══════════════════════════════════════════════════════════════════════"
    echo "            Agent Recommendation - Interactive Mode"
    echo "═══════════════════════════════════════════════════════════════════════"
    echo ""
    echo "Use arrow keys to navigate, SPACE to toggle, ENTER to confirm"
    echo "Commands: a=select all, n=select none, q=quit"
    echo ""

    # Group agents by category for display
    declare -A category_agents
    for agent in "${agent_list[@]}"; do
      local category="${AGENT_CATEGORIES[$agent]:-Uncategorized}"
      if [[ -z "${category_agents[$category]}" ]]; then
        category_agents[$category]="$agent"
      else
        category_agents[$category]="${category_agents[$category]} $agent"
      fi
    done

    local display_index=0
    local -a categories=("Infrastructure (Cloud)" "Infrastructure (IaC)" "Infrastructure (Platform)" "Infrastructure (Containers)" "Infrastructure (Monitoring)" "Development" "Quality" "Operations" "Productivity" "Business" "Specialized" "Uncategorized")

    for category in "${categories[@]}"; do
      if [[ -n "${category_agents[$category]}" ]]; then
        echo "━━ $category ━━"

        IFS=' ' read -ra agents <<< "${category_agents[$category]}"
        for agent in "${agents[@]}"; do
          local confidence="${agent_confidence[$agent]:-0}"
          local description="${AGENT_DESCRIPTIONS[$agent]:-}"

          # Determine if this is the current selection
          local cursor=" "
          if [[ $display_index -eq $current_index ]]; then
            cursor=">"
          fi

          # Determine if this agent is selected
          local checkbox="[ ]"
          if [[ ${selected_agents[$agent]:-0} -eq 1 ]]; then
            checkbox="[✓]"
          fi

          # Display the agent
          printf "%s %s %s (%d%%)\n" "$cursor" "$checkbox" "$agent" "$confidence"

          # Show description if it's the current selection
          if [[ $display_index -eq $current_index ]] && [[ -n "$description" ]]; then
            printf "      %s\n" "$description"
          fi

          ((display_index++))
        done
        echo ""
      fi
    done

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    local selected_count=0
    for agent in "${agent_list[@]}"; do
      [[ ${selected_agents[$agent]:-0} -eq 1 ]] && ((selected_count++))
    done
    echo "Selected: $selected_count / ${#agent_list[@]} agents"
  }

  # Main interactive loop
  while true; do
    display_interactive_ui

    # Read single character
    read -rsn1 key

    # Handle special keys (arrow keys start with escape sequence)
    if [[ $key == $'\x1b' ]]; then
      read -rsn2 key
      case "$key" in
        '[A')  # Up arrow
          if [[ $current_index -gt 0 ]]; then
            ((current_index--))
          fi
          ;;
        '[B')  # Down arrow
          if [[ $current_index -lt $((${#agent_list[@]} - 1)) ]]; then
            ((current_index++))
          fi
          ;;
      esac
    else
      case "$key" in
        ' ')  # Space - toggle selection
          local agent="${agent_list[$current_index]}"
          if [[ ${selected_agents[$agent]:-0} -eq 1 ]]; then
            unset selected_agents[$agent]
          else
            selected_agents[$agent]=1
          fi
          ;;
        '')  # Enter - confirm selection
          break
          ;;
        'a'|'A')  # Select all
          for agent in "${agent_list[@]}"; do
            selected_agents[$agent]=1
          done
          ;;
        'n'|'N')  # Select none
          selected_agents=()
          ;;
        'q'|'Q')  # Quit
          echo ""
          log "Cancelled by user"
          exit 0
          ;;
      esac
    fi
  done

  clear

  # Return selected agents by updating recommended_agents array
  recommended_agents=()
  for agent in "${agent_list[@]}"; do
    if [[ ${selected_agents[$agent]:-0} -eq 1 ]]; then
      recommended_agents+=("$agent")
    fi
  done

  log "Selected ${#recommended_agents[@]} agents for installation"
}

# Profile export functionality (Task 8)
export_profile() {
  local output_file="$1"

  # Check if file exists (unless --force is used)
  if [[ -f "$output_file" ]] && [[ $FORCE == false ]]; then
    echo "Error: File already exists: $output_file (use --force to overwrite)" >&2
    exit 1
  fi

  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local project_name=$(basename "$PWD")

  # Start JSON
  cat > "$output_file" <<EOF
{
  "version": "1.0",
  "generated_at": "$timestamp",
  "project_name": "$project_name",
  "detection_results": {
    "agents_recommended": [
EOF

  # Add agents
  local first=true
  for agent in "${recommended_agents[@]}"; do
    [[ $first == false ]] && echo "," >> "$output_file"
    first=false

    local confidence="${agent_confidence[$agent]:-0}"
    local category="${AGENT_CATEGORIES[$agent]:-Uncategorized}"
    local matched_patterns="${agent_matched_patterns[$agent]:-}"

    # Convert matched patterns to JSON array
    local patterns_json="[]"
    if [[ -n "$matched_patterns" ]]; then
      patterns_json="["
      local first_pattern=true
      for pattern in $matched_patterns; do
        [[ $first_pattern == false ]] && patterns_json="$patterns_json,"
        first_pattern=false
        # Escape quotes in pattern
        pattern=$(echo "$pattern" | sed 's/"/\\"/g')
        patterns_json="$patterns_json\"$pattern\""
      done
      patterns_json="$patterns_json]"
    fi

    cat >> "$output_file" <<EOF
      {
        "name": "$agent",
        "confidence": $confidence,
        "category": "$category",
        "patterns_matched": $patterns_json
      }
EOF
  done

  # Close agents array and add selected agents
  cat >> "$output_file" <<EOF

    ]
  },
  "selected_agents": [
EOF

  # Add selected agents list
  first=true
  for agent in "${recommended_agents[@]}"; do
    [[ $first == false ]] && echo "," >> "$output_file"
    first=false
    echo -n "    \"$agent\"" >> "$output_file"
  done

  # Close JSON
  cat >> "$output_file" <<EOF

  ]
}
EOF

  log "Profile exported to $output_file"
}

# Profile import functionality (Task 9)
import_profile() {
  local input_file="$1"

  # Validate file exists
  if [[ ! -f "$input_file" ]]; then
    echo "Error: Profile file not found: $input_file" >&2
    exit 1
  fi

  log "Importing profile from $input_file"

  # Check if we have jq for JSON parsing, otherwise use grep/sed
  if ! command -v jq >/dev/null 2>&1; then
    # Basic JSON parsing without jq
    log "Warning: jq not found, using basic JSON parsing"

    # Extract selected_agents array (simple parsing)
    local agents_json=$(grep -A 100 '"selected_agents"' "$input_file" | sed -n '/\[/,/\]/p' | grep '"' | sed 's/.*"\([^"]*\)".*/\1/')

    if [[ -z "$agents_json" ]]; then
      echo "Error: Could not parse selected_agents from profile" >&2
      exit 1
    fi

    # Download each agent
    local count=0
    while IFS= read -r agent; do
      [[ -z "$agent" ]] && continue
      log "Installing agent: $agent"
      fetch_agent "$agent"
      ((count++))
    done <<< "$agents_json"

    log "Successfully installed $count agents from profile"
  else
    # Use jq for proper JSON parsing
    # Validate JSON
    if ! jq empty "$input_file" 2>/dev/null; then
      echo "Error: Invalid JSON in profile file" >&2
      exit 1
    fi

    # Extract selected agents
    local -a agents
    mapfile -t agents < <(jq -r '.selected_agents[]?' "$input_file")

    if [[ ${#agents[@]} -eq 0 ]]; then
      echo "Error: No agents found in profile" >&2
      exit 1
    fi

    log "Found ${#agents[@]} agents in profile"

    # Fetch agent registry to validate agents exist
    parse_agent_registry

    # Download agents
    local count=0
    for agent in "${agents[@]}"; do
      [[ -z "$agent" ]] && continue

      # Validate agent exists in registry (if registry was parsed)
      if [[ ${#AGENT_DESCRIPTIONS[@]} -gt 0 ]] && [[ -z "${AGENT_DESCRIPTIONS[$agent]}" ]]; then
        log "Warning: Agent '$agent' not found in registry, attempting to download anyway"
      fi

      log "Installing agent: $agent"
      fetch_agent "$agent"
      ((count++))
    done

    log "Successfully installed $count agents from profile"
  fi
}

# Update detection functionality (Task 10)
check_updates() {
  # Find all local agent files
  local -a local_agents
  if [[ ! -d "$AGENTS_DIR" ]]; then
    log "No agents directory found. No agents to check."
    return 0
  fi

  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    local agent=$(basename "$file" .md)
    [[ "$agent" == "AGENTS_REGISTRY" ]] && continue
    local_agents+=("$agent")
  done < <(find "$AGENTS_DIR" -name "*.md" -type f)

  if [[ ${#local_agents[@]} -eq 0 ]]; then
    log "No agents installed locally"
    return 0
  fi

  log "Checking for updates to ${#local_agents[@]} locally installed agents..."

  local -a updates_available=()

  for agent in "${local_agents[@]}"; do
    local local_file="${AGENTS_DIR}/${agent}.md"
    local remote_url="${BASE_URL}/${agent}.md"

    # Get remote file and compare with local
    local remote_content=$(curl -fsSL "$remote_url" 2>/dev/null)

    if [[ -z "$remote_content" ]]; then
      log "Warning: Could not fetch remote version of $agent"
      continue
    fi

    # Compare content
    local local_content=$(cat "$local_file")

    if [[ "$remote_content" != "$local_content" ]]; then
      updates_available+=("$agent")
    fi
  done

  if [[ ${#updates_available[@]} -eq 0 ]]; then
    log "All agents are up to date ✓"
  else
    log "Updates available for ${#updates_available[@]} agent(s):"
    for agent in "${updates_available[@]}"; do
      log "  - $agent"
    done
    log ""
    log "Run with --update-all to update all agents"
  fi

  # Return count of updates
  echo "${#updates_available[@]}"
}

update_all_agents() {
  # Find all local agent files
  local -a local_agents
  if [[ ! -d "$AGENTS_DIR" ]]; then
    log "No agents directory found. No agents to update."
    return 0
  fi

  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    local agent=$(basename "$file" .md)
    [[ "$agent" == "AGENTS_REGISTRY" ]] && continue
    local_agents+=("$agent")
  done < <(find "$AGENTS_DIR" -name "*.md" -type f)

  if [[ ${#local_agents[@]} -eq 0 ]]; then
    log "No agents installed locally"
    return 0
  fi

  log "Checking and updating ${#local_agents[@]} agents..."

  local updated_count=0
  local backup_dir="${AGENTS_DIR}/.backup_$(date +%Y%m%d_%H%M%S)"

  for agent in "${local_agents[@]}"; do
    local local_file="${AGENTS_DIR}/${agent}.md"
    local remote_url="${BASE_URL}/${agent}.md"

    # Get remote file and compare with local
    local remote_content=$(curl -fsSL "$remote_url" 2>/dev/null)

    if [[ -z "$remote_content" ]]; then
      log "Warning: Could not fetch remote version of $agent, skipping"
      continue
    fi

    # Compare content
    local local_content=$(cat "$local_file")

    if [[ "$remote_content" != "$local_content" ]]; then
      # Create backup directory if needed
      if [[ ! -d "$backup_dir" ]]; then
        mkdir -p "$backup_dir"
      fi

      # Backup existing file
      cp "$local_file" "${backup_dir}/${agent}.md"
      log "Backed up $agent to ${backup_dir}/${agent}.md"

      # Download updated version
      log "Updating $agent..."
      echo "$remote_content" > "$local_file"
      ((updated_count++))
    fi
  done

  if [[ $updated_count -eq 0 ]]; then
    log "All agents were already up to date ✓"
  else
    log "Updated $updated_count agent(s)"
    if [[ -d "$backup_dir" ]]; then
      log "Backups saved to $backup_dir"
    fi
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
file:cdk.context.json:15
path:.aws:10
path:cloudformation:15
content:AWS::CloudFormation:15
content:aws-cdk:10
content:@aws-cdk:10
"

  AGENT_PATTERNS["azure-specialist"]="
file:*.bicep:20
file:azuredeploy.json:15
file:azuredeploy.parameters.json:10
content:deploymentTemplate:15
content:\$schema.*deploymentTemplate:15
file:azure-pipelines.yml:15
file:azure-pipelines.yaml:15
content:provider \"azurerm\":20
content:azurerm_:15
content:Microsoft.Compute:10
content:Microsoft.Resources:10
path:.azure:10
"

  AGENT_PATTERNS["gcp-specialist"]="
file:app.yaml:15
path:.config/gcloud:10
content:provider \"google\":20
content:google_:15
file:deployment-manager.yaml:15
file:*.jinja:10
path:deployment:10
content:gcp.googleapis.com:10
content:googleapis.com:10
content:gcloud:10
file:cloudbuild.yaml:15
"

  AGENT_PATTERNS["terraform-specialist"]="
file:*.tf:20
file:*.tfvars:15
file:terraform.tfstate:25
file:terraform.tfstate.backup:20
file:.terraform.lock.hcl:15
path:.terraform:15
content:terraform:10
content:module:10
content:resource:5
"

  AGENT_PATTERNS["ansible-specialist"]="
file:ansible.cfg:20
file:playbook.yml:15
file:playbook.yaml:15
path:roles:15
path:inventory:10
file:requirements.yml:10
content:ansible.builtin:15
content:hosts::10
content:tasks::10
"

  AGENT_PATTERNS["cicd-specialist"]="
path:.github/workflows:20
file:.gitlab-ci.yml:20
file:Jenkinsfile:20
path:.circleci:20
file:circle.yml:15
file:azure-pipelines.yml:20
file:.travis.yml:15
file:buildspec.yml:15
content:pipeline:10
content:ci/cd:10
content:continuous integration:10
"

  AGENT_PATTERNS["kubernetes-specialist"]="
path:k8s:20
path:kubernetes:20
file:Chart.yaml:20
file:values.yaml:15
file:kustomization.yaml:20
content:apiVersion:10
content:kind: Deployment:15
content:kind: Service:10
content:kind: StatefulSet:10
content:kubectl:10
file:skaffold.yaml:15
"

  AGENT_PATTERNS["monitoring-specialist"]="
file:prometheus.yml:20
file:prometheus.yaml:20
path:prometheus:15
path:grafana:15
file:grafana.ini:15
file:elasticsearch.yml:15
file:logstash.conf:15
file:kibana.yml:15
content:metrics:10
content:observability:10
content:alertmanager:10
path:monitoring:15
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

# Handle import mode - skip detection and install agents from profile (Task 9)
if [[ -n "$IMPORT_FILE" ]]; then
  mkdir -p "$AGENTS_DIR"

  # Define fetch_agent function here for import mode
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

  # Parse agent registry before importing
  parse_agent_registry

  # Import and install agents from profile
  import_profile "$IMPORT_FILE"

  # Always include the registry for reference
  REGISTRY_DEST="${AGENTS_DIR}/AGENTS_REGISTRY.md"
  if [[ ! -f "$REGISTRY_DEST" || $FORCE == true ]]; then
    REGISTRY_URL="${BASE_URL}/AGENTS_REGISTRY.md"
    log "Downloading agent registry"
    curl -fsSL "$REGISTRY_URL" -o "$REGISTRY_DEST"
  fi

  log "All done! Agent prompts are located in ${AGENTS_DIR}"
  exit 0
fi

# Handle update detection mode (Task 10)
if [[ $CHECK_UPDATES == true ]] || [[ $UPDATE_ALL == true ]]; then
  if [[ $CHECK_UPDATES == true ]]; then
    check_updates
    exit 0
  fi

  if [[ $UPDATE_ALL == true ]]; then
    update_all_agents
    exit 0
  fi
fi

# Parse agent registry for metadata
parse_agent_registry

# Run detection for all agents
log "Scanning project for technology signals..."

for agent in "${!AGENT_PATTERNS[@]}"; do
  # Calculate confidence (stores in agent_confidence array)
  calculate_confidence "$agent" > /dev/null

  # Get the stored confidence
  confidence="${agent_confidence[$agent]:-0}"

  # Add agents with confidence >= MIN_CONFIDENCE threshold
  if [[ $confidence -ge $MIN_CONFIDENCE ]]; then
    add_agent "$agent"
  fi
done

# DevOps Orchestrator Logic (Task 3.3)
# Boost devops-orchestrator confidence when multiple infrastructure components detected
detect_devops_orchestrator() {
  local infra_agents=()
  local cloud_detected=false
  local iac_detected=false
  local k8s_detected=false
  local cicd_detected=false

  # Check for cloud providers
  for cloud_agent in "aws-specialist" "azure-specialist" "gcp-specialist"; do
    if [[ ${agent_confidence[$cloud_agent]:-0} -ge $MIN_CONFIDENCE ]]; then
      cloud_detected=true
      infra_agents+=("$cloud_agent")
    fi
  done

  # Check for IaC tools
  for iac_agent in "terraform-specialist" "ansible-specialist"; do
    if [[ ${agent_confidence[$iac_agent]:-0} -ge $MIN_CONFIDENCE ]]; then
      iac_detected=true
      infra_agents+=("$iac_agent")
    fi
  done

  # Check for Kubernetes
  if [[ ${agent_confidence["kubernetes-specialist"]:-0} -ge $MIN_CONFIDENCE ]]; then
    k8s_detected=true
    infra_agents+=("kubernetes-specialist")
  fi

  # Check for CI/CD
  if [[ ${agent_confidence["cicd-specialist"]:-0} -ge $MIN_CONFIDENCE ]]; then
    cicd_detected=true
    infra_agents+=("cicd-specialist")
  fi

  # Check for monitoring
  if [[ ${agent_confidence["monitoring-specialist"]:-0} -ge $MIN_CONFIDENCE ]]; then
    infra_agents+=("monitoring-specialist")
  fi

  # Boost orchestrator confidence based on complexity
  local current_confidence=${agent_confidence["devops-orchestrator"]:-0}
  local boost=0

  # Condition 1: Multiple IaC tools (Terraform + Ansible)
  if [[ $iac_detected == true ]] && [[ ${agent_confidence["terraform-specialist"]:-0} -ge $MIN_CONFIDENCE ]] && [[ ${agent_confidence["ansible-specialist"]:-0} -ge $MIN_CONFIDENCE ]]; then
    boost=$((boost + 20))
  fi

  # Condition 2: Cloud + Terraform + Kubernetes all detected
  if [[ $cloud_detected == true ]] && [[ $iac_detected == true ]] && [[ $k8s_detected == true ]]; then
    boost=$((boost + 30))
  fi

  # Condition 3: IaC + CI/CD + Kubernetes + Monitoring (full DevOps stack)
  if [[ $iac_detected == true ]] && [[ $cicd_detected == true ]] && [[ $k8s_detected == true ]] && [[ ${agent_confidence["monitoring-specialist"]:-0} -ge $MIN_CONFIDENCE ]]; then
    boost=$((boost + 35))
  fi

  # Condition 4: 3+ infrastructure agents detected
  if [[ ${#infra_agents[@]} -ge 3 ]]; then
    boost=$((boost + 15))
  fi

  # Apply boost
  if [[ $boost -gt 0 ]]; then
    local new_confidence=$((current_confidence + boost))
    [[ $new_confidence -gt 100 ]] && new_confidence=100
    agent_confidence["devops-orchestrator"]=$new_confidence

    # Add to recommended agents if not already present and meets threshold
    if [[ $new_confidence -ge $MIN_CONFIDENCE ]]; then
      add_agent "devops-orchestrator"
    fi
  fi
}

# Run DevOps orchestrator detection logic
detect_devops_orchestrator

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

# Display results using enhanced formatting
if [[ ${#recommended_agents[@]} -gt 0 ]]; then
  # If interactive mode, let user select agents
  if [[ $INTERACTIVE == true ]]; then
    display_categorized_results
    echo ""
    log "Entering interactive mode..."
    sleep 1
    interactive_selection
  else
    display_categorized_results
  fi
else
  log "No agents met the confidence threshold of ${MIN_CONFIDENCE}%"
fi

# Verbose mode: show detailed detection patterns
if [[ $VERBOSE == true ]]; then
  echo ""
  echo "═══════════════════════════════════════════════════════════════════════"
  echo "                     Detailed Detection Results (Verbose)"
  echo "═══════════════════════════════════════════════════════════════════════"
  echo ""

  for agent in "${recommended_agents[@]}"; do
    echo "Agent: $agent (Confidence: ${agent_confidence[$agent]:-0}%)"
    echo "Matched Patterns:"

    local patterns="${AGENT_PATTERNS[$agent]}"
    while IFS= read -r pattern_line; do
      [[ -z "$pattern_line" ]] && continue
      pattern_line=$(echo "$pattern_line" | xargs)
      [[ -z "$pattern_line" ]] && continue

      type="${pattern_line%%:*}"
      rest="${pattern_line#*:}"
      weight="${rest##*:}"
      pattern="${rest%:*}"

      [[ -z "$type" || -z "$pattern" || -z "$weight" ]] && continue

      # Check if pattern matched
      local matched=false
      case "$type" in
        file) has_file "$pattern" && matched=true ;;
        path) has_path "$pattern" && matched=true ;;
        content) search_contents "$pattern" && matched=true ;;
      esac

      if [[ $matched == true ]]; then
        echo "  ✓ $type:$pattern (weight: $weight)"
      else
        echo "  ✗ $type:$pattern (weight: $weight)"
      fi
    done <<< "$patterns"

    echo ""
  done

  echo "═══════════════════════════════════════════════════════════════════════"
  echo ""
fi

# Export profile if requested
if [[ -n "$EXPORT_FILE" ]]; then
  export_profile "$EXPORT_FILE"

  # If dry-run or only exporting, exit
  if $DRY_RUN; then
    exit 0
  fi
fi

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

  log "Downloading ${agent}..."
  if ! fetch_with_retry "$url" "$dest"; then
    echo "Failed to download ${agent}" >&2
    echo "You can try again with --force to retry failed downloads" >&2
    return 1
  fi

  log "Successfully downloaded ${agent}"
}

for agent in "${recommended_agents[@]}"; do
  fetch_agent "$agent"
done

# Always include the registry for reference
REGISTRY_DEST="${AGENTS_DIR}/AGENTS_REGISTRY.md"
if [[ ! -f "$REGISTRY_DEST" || $FORCE == true ]]; then
  REGISTRY_URL="${BASE_URL}/AGENTS_REGISTRY.md"
  log "Downloading agent registry..."
  if ! fetch_with_retry "$REGISTRY_URL" "$REGISTRY_DEST"; then
    echo "Warning: Failed to download agent registry" >&2
  else
    log "Successfully downloaded agent registry"
  fi
else
  log "Agent registry already present. Use --force to redownload."
fi

log "All done! Agent prompts are located in ${AGENTS_DIR}"
