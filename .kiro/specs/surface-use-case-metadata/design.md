# Design Document

## Overview

This document outlines the design for surfacing agent use case metadata throughout the agent recommendation system. Currently, use case information is parsed from AGENTS_REGISTRY.md but never displayed to users. This enhancement adds use case display to CLI output, interactive mode, and exported JSON profiles, helping users understand why specific agents were recommended.

The solution leverages the existing `AGENT_USE_CASES` associative array populated by the registry parser and integrates use case display into all user-facing outputs.

## Architecture

### Current State

```
┌─────────────────────────────────────────────────────────────┐
│              Registry Parser                                 │
│  Extracts: name, category, description, use_cases           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Structures                                 │
│  AGENT_CATEGORIES ✓                                          │
│  AGENT_DESCRIPTIONS ✓                                        │
│  AGENT_USE_CASES ✓ (parsed but not displayed)               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Output Layers                                   │
│  CLI Summary: Shows category, description ✓                  │
│  Interactive Mode: Shows description ✓                       │
│  JSON Export: Includes category, description ✓               │
│                                                              │
│  Missing: Use case metadata ✗                                │
└─────────────────────────────────────────────────────────────┘
```

### Enhanced State

```
┌─────────────────────────────────────────────────────────────┐
│              Registry Parser                                 │
│  Extracts: name, category, description, use_cases           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Structures                                 │
│  AGENT_CATEGORIES ✓                                          │
│  AGENT_DESCRIPTIONS ✓                                        │
│  AGENT_USE_CASES ✓ (parsed and displayed)                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Output Layers                                   │
│  CLI Summary: Shows category, description, use cases ✓       │
│  Interactive Mode: Shows description, use cases ✓            │
│  JSON Export: Includes category, description, use cases ✓    │
└─────────────────────────────────────────────────────────────┘
```

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Registry Parser                             │
│  (Populates AGENT_USE_CASES array)                          │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Use Case Formatter                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  format_use_case()                                   │   │
│  │  - Wrap text to terminal width                       │   │
│  │  - Add indentation                                   │   │
│  │  - Handle missing use cases                          │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ├──────────────┬──────────────┬──────────────┐
                 ▼              ▼              ▼              ▼
         ┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
         │ CLI Output   │ │Interactive│ │  JSON    │ │ Verbose  │
         │              │ │   Mode    │ │  Export  │ │  Mode    │
         └──────────────┘ └──────────┘ └──────────┘ └──────────┘
```

## Components and Interfaces

### 1. Use Case Formatter

Format use case text for display in various contexts.

```bash
# Format use case text for terminal display
format_use_case() {
  local use_case="$1"
  local indent="${2:-     }"  # Default 5 spaces
  local max_width="${3:-80}"
  
  # Handle missing use case
  if [[ -z "$use_case" ]]; then
    echo "${indent}(No use case information available)"
    return
  fi
  
  # Word wrap to terminal width
  local wrapped
  wrapped=$(echo "$use_case" | fold -s -w $((max_width - ${#indent})))
  
  # Add indentation to each line
  echo "$wrapped" | sed "s/^/$indent/"
}

# Get terminal width
get_terminal_width() {
  local width
  width=$(tput cols 2>/dev/null || echo "80")
  echo "$width"
}

# Format use case with automatic width detection
format_use_case_auto() {
  local use_case="$1"
  local indent="${2:-     }"
  local term_width
  term_width=$(get_terminal_width)
  
  format_use_case "$use_case" "$indent" "$term_width"
}
```

### 2. Enhanced CLI Output

Add use case display to standard recommendation output.

#### Current CLI Output

```
┌─────────────────────────────────────────────────────────────┐
│              Agent Recommendation Results                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Infrastructure Agents (4 recommended)                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                              │
│  ✓ terraform-specialist [████████████████████] 92%          │
│    Terraform configuration, modules, state management        │
│    Detected: *.tf files, *.tfvars files                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Enhanced CLI Output

```
┌─────────────────────────────────────────────────────────────┐
│              Agent Recommendation Results                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Infrastructure Agents (4 recommended)                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                              │
│  ✓ terraform-specialist [████████████████████] 92%          │
│    Terraform configuration, modules, state management        │
│    Use for: Infrastructure as code, cloud resource          │
│             provisioning, multi-environment deployments      │
│    Detected: *.tf files, *.tfvars files                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Implementation

```bash
# Enhanced render_agent_item with use case
render_agent_item() {
  local agent="$1"
  local confidence="$2"
  local description="$3"
  local use_case="$4"
  local is_selected="$5"
  local is_current="$6"
  
  local checkbox="[ ]"
  [[ $is_selected -eq 1 ]] && checkbox="[✓]"
  
  local cursor="  "
  [[ $is_current -eq 1 ]] && cursor="→ "
  
  local confidence_bar=$(render_confidence_bar "$confidence")
  
  # Agent name and confidence
  printf "%s%s %s %s %d%%\n" "$cursor" "$checkbox" "$agent" "$confidence_bar" "$confidence"
  
  # Description
  printf "     %s\n" "$description"
  
  # Use case (new)
  if [[ -n "$use_case" ]]; then
    printf "     Use for: "
    format_use_case "$use_case" "              " | tail -n +1
  fi
  
  # Detection patterns
  printf "     Detected: %s\n" "$(get_matched_patterns "$agent")"
}

# Update display_recommendations to pass use cases
display_recommendations() {
  local -n agents_ref=$1
  local -n confidence_ref=$2
  local -n descriptions_ref=$3
  local -n use_cases_ref=$4  # New parameter
  
  for agent in "${agents_ref[@]}"; do
    render_agent_item \
      "$agent" \
      "${confidence_ref[$agent]}" \
      "${descriptions_ref[$agent]}" \
      "${use_cases_ref[$agent]}" \  # Pass use case
      0 \
      0
  done
}
```

### 3. Enhanced Interactive Mode

Add use case display to interactive selection UI.

#### Interactive Mode Layout

```
┌─────────────────────────────────────────────────────────────┐
│           Agent Recommendation - Interactive Mode            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Infrastructure (4 agents)                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                              │
│→ [✓] terraform-specialist [████████████████████] 92%        │
│     Terraform configuration, modules, state management       │
│     Use for: Infrastructure as code, cloud resource          │
│              provisioning, multi-environment deployments     │
│                                                              │
│  [ ] aws-specialist [████████████████░░░░] 85%              │
│     AWS cloud services, architecture, CloudFormation, CDK    │
│     Use for: AWS infrastructure, serverless applications,    │
│              cloud migrations                                │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│  Selected: 1/4                                               │
│  Navigation: ↑/↓ to move, SPACE to toggle, ENTER to confirm │
└─────────────────────────────────────────────────────────────┘
```

#### Implementation

```bash
# Enhanced render_agent_item for interactive mode
render_agent_item_interactive() {
  local agent="$1"
  local confidence="$2"
  local description="$3"
  local use_case="$4"
  local is_selected="$5"
  local is_current="$6"
  
  local checkbox="[ ]"
  [[ $is_selected -eq 1 ]] && checkbox="[✓]"
  
  local cursor="  "
  [[ $is_current -eq 1 ]] && cursor="→ "
  
  local confidence_bar=$(render_confidence_bar "$confidence")
  
  # Agent name and confidence
  printf "%s%s %s %s %d%%\n" "$cursor" "$checkbox" "$agent" "$confidence_bar" "$confidence"
  
  # Description
  printf "     %s\n" "$description"
  
  # Use case (only show for current item to save space)
  if [[ $is_current -eq 1 ]] && [[ -n "$use_case" ]]; then
    printf "     Use for: "
    local term_width=$(get_terminal_width)
    format_use_case "$use_case" "              " "$term_width" | tail -n +1
  fi
  
  echo ""  # Blank line between agents
}
```

### 4. Enhanced JSON Export

Add use case metadata to exported profiles.

#### Current JSON Schema

```json
{
  "version": "1.0",
  "generated_at": "2025-11-10T14:30:00Z",
  "project_name": "my-project",
  "detection_results": {
    "agents_recommended": [
      {
        "name": "terraform-specialist",
        "confidence": 92,
        "category": "Infrastructure (IaC)",
        "description": "Terraform configuration, modules, state management",
        "patterns_matched": ["file:*.tf", "file:*.tfvars"]
      }
    ]
  }
}
```

#### Enhanced JSON Schema

```json
{
  "version": "1.0",
  "generated_at": "2025-11-10T14:30:00Z",
  "project_name": "my-project",
  "detection_results": {
    "agents_recommended": [
      {
        "name": "terraform-specialist",
        "confidence": 92,
        "category": "Infrastructure (IaC)",
        "description": "Terraform configuration, modules, state management",
        "use_cases": "Infrastructure as code, cloud resource provisioning, multi-environment deployments",
        "patterns_matched": ["file:*.tf", "file:*.tfvars"]
      }
    ]
  }
}
```

#### Implementation

```bash
# Enhanced export_profile with use cases
export_profile() {
  local output_file="$1"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local project_name=$(basename "$PWD")
  
  cat > "$output_file" <<EOF
{
  "version": "1.0",
  "generated_at": "$timestamp",
  "project_name": "$project_name",
  "detection_results": {
    "technologies_detected": $(printf '%s\n' "${detected_technologies[@]}" | jq -R . | jq -s .),
    "agents_recommended": [
EOF
  
  local first=true
  for agent in "${!agent_confidence[@]}"; do
    [[ $first == false ]] && echo "," >> "$output_file"
    first=false
    
    # Escape use case text for JSON
    local use_case="${AGENT_USE_CASES[$agent]:-}"
    local use_case_json
    use_case_json=$(echo "$use_case" | jq -R -s .)
    
    cat >> "$output_file" <<EOF
      {
        "name": "$agent",
        "confidence": ${agent_confidence[$agent]},
        "category": "${AGENT_CATEGORIES[$agent]}",
        "description": "${AGENT_DESCRIPTIONS[$agent]}",
        "use_cases": $use_case_json,
        "patterns_matched": $(get_matched_patterns "$agent" | jq -R . | jq -s .)
      }
EOF
  done
  
  cat >> "$output_file" <<EOF
    ]
  },
  "selected_agents": $(printf '%s\n' "${selected_agents[@]}" | jq -R . | jq -s .)
}
EOF
  
  log "Profile exported to $output_file"
}
```

### 5. Enhanced Verbose Mode

Add use case display to verbose output.

```bash
# Verbose mode agent display
display_agent_verbose() {
  local agent="$1"
  local confidence="$2"
  
  echo "Agent: $agent"
  echo "  Category: ${AGENT_CATEGORIES[$agent]}"
  echo "  Description: ${AGENT_DESCRIPTIONS[$agent]}"
  echo "  Use Cases: ${AGENT_USE_CASES[$agent]:-N/A}"
  echo "  Confidence: $confidence%"
  echo "  Patterns Matched:"
  get_matched_patterns "$agent" | sed 's/^/    - /'
  echo ""
}
```

### 6. Use Case Validation

Validate that use cases are available for all agents.

```bash
# Validate use case metadata
validate_use_cases() {
  local missing=0
  
  for agent in "${!AGENT_PATTERNS[@]}"; do
    if [[ -z "${AGENT_USE_CASES[$agent]}" ]]; then
      log "Warning: Agent '$agent' has no use case metadata"
      ((missing++))
    fi
  done
  
  if [[ $missing -gt 0 ]]; then
    log "Warning: $missing agents missing use case metadata"
    return 1
  fi
  
  log "All agents have use case metadata"
  return 0
}

# Check use case availability before display
get_use_case_safe() {
  local agent="$1"
  local use_case="${AGENT_USE_CASES[$agent]}"
  
  if [[ -z "$use_case" ]]; then
    echo "(No use case information available)"
  else
    echo "$use_case"
  fi
}
```

## Data Models

### Use Case Data Structure

```bash
# Populated by registry parser
declare -A AGENT_USE_CASES=(
  ["terraform-specialist"]="Infrastructure as code, cloud resource provisioning, multi-environment deployments"
  ["aws-specialist"]="AWS infrastructure, serverless applications, cloud migrations"
  ["docker-specialist"]="Container orchestration, microservices architecture, deployment automation"
  # ... all agents
)
```

### Enhanced Profile Schema

```json
{
  "version": "1.0",
  "generated_at": "ISO8601 timestamp",
  "project_name": "string",
  "detection_results": {
    "technologies_detected": ["string"],
    "agents_recommended": [
      {
        "name": "string",
        "confidence": 0-100,
        "category": "string",
        "description": "string",
        "use_cases": "string",  // NEW
        "patterns_matched": ["string"]
      }
    ]
  },
  "selected_agents": ["string"]
}
```

## Error Handling

### Missing Use Cases

```bash
# Handle missing use case gracefully
display_use_case() {
  local agent="$1"
  local use_case="${AGENT_USE_CASES[$agent]}"
  
  if [[ -z "$use_case" ]]; then
    if [[ ${VERBOSE:-false} == true ]]; then
      log "Warning: No use case metadata for $agent"
    fi
    echo "(No use case information available)"
  else
    echo "$use_case"
  fi
}
```

### Text Wrapping Edge Cases

```bash
# Handle very narrow terminals
format_use_case_safe() {
  local use_case="$1"
  local indent="${2:-     }"
  local max_width="${3:-80}"
  
  # Minimum width check
  local min_width=40
  if [[ $max_width -lt $min_width ]]; then
    # Terminal too narrow, don't wrap
    echo "${indent}${use_case}"
    return
  fi
  
  format_use_case "$use_case" "$indent" "$max_width"
}
```

## Testing Strategy

### Unit Tests

```bash
# tests/unit/test_use_case_formatting.bats

@test "format_use_case wraps long text" {
  use_case="This is a very long use case description that should be wrapped to fit within the terminal width"
  
  output=$(format_use_case "$use_case" "  " 40)
  
  # Each line should be <= 40 chars
  while IFS= read -r line; do
    [[ ${#line} -le 40 ]]
  done <<< "$output"
}

@test "format_use_case handles empty use case" {
  output=$(format_use_case "" "  " 80)
  
  [[ "$output" =~ "No use case information" ]]
}

@test "format_use_case adds indentation" {
  use_case="Short text"
  
  output=$(format_use_case "$use_case" "    " 80)
  
  [[ "$output" =~ ^"    " ]]
}

@test "get_use_case_safe returns placeholder for missing" {
  AGENT_USE_CASES[test-agent]=""
  
  output=$(get_use_case_safe "test-agent")
  
  [[ "$output" =~ "No use case information" ]]
}
```

### Integration Tests

```bash
# tests/integration/test_use_case_display.bats

@test "CLI output includes use cases" {
  # Set up test data
  AGENT_USE_CASES[test-agent]="Test use case"
  AGENT_DESCRIPTIONS[test-agent]="Test description"
  agent_confidence[test-agent]=75
  
  output=$(display_recommendations test_agents agent_confidence AGENT_DESCRIPTIONS AGENT_USE_CASES)
  
  [[ "$output" =~ "Use for:" ]]
  [[ "$output" =~ "Test use case" ]]
}

@test "JSON export includes use cases" {
  AGENT_USE_CASES[test-agent]="Test use case"
  agent_confidence[test-agent]=75
  
  export_profile "test_profile.json"
  
  use_case=$(jq -r '.detection_results.agents_recommended[0].use_cases' test_profile.json)
  
  [[ "$use_case" == "Test use case" ]]
}

@test "interactive mode displays use cases for current agent" {
  AGENT_USE_CASES[test-agent]="Test use case"
  
  output=$(render_agent_item_interactive "test-agent" 75 "Description" "Test use case" 1 1)
  
  [[ "$output" =~ "Use for:" ]]
  [[ "$output" =~ "Test use case" ]]
}
```

### Visual Regression Tests

```bash
# tests/visual/test_output_formatting.sh

# Generate reference output
generate_reference_output() {
  ./scripts/recommend_agents.sh --dry-run > reference_output.txt
}

# Compare current output to reference
compare_output() {
  ./scripts/recommend_agents.sh --dry-run > current_output.txt
  
  if diff -u reference_output.txt current_output.txt; then
    echo "Output matches reference"
    return 0
  else
    echo "Output differs from reference"
    return 1
  fi
}
```

## Performance Considerations

### Text Wrapping Performance

```bash
# Cache wrapped text to avoid redundant calculations
declare -A USE_CASE_WRAP_CACHE

format_use_case_cached() {
  local use_case="$1"
  local indent="$2"
  local max_width="$3"
  local cache_key="${use_case}:${indent}:${max_width}"
  
  if [[ -n "${USE_CASE_WRAP_CACHE[$cache_key]}" ]]; then
    echo "${USE_CASE_WRAP_CACHE[$cache_key]}"
    return
  fi
  
  local wrapped
  wrapped=$(format_use_case "$use_case" "$indent" "$max_width")
  USE_CASE_WRAP_CACHE[$cache_key]="$wrapped"
  
  echo "$wrapped"
}
```

## Migration Strategy

### Phase 1: Add Formatting Functions

- Implement format_use_case and helper functions
- Add terminal width detection
- Test text wrapping

### Phase 2: Enhance CLI Output

- Update render_agent_item to include use cases
- Modify display_recommendations to pass use cases
- Test CLI output formatting

### Phase 3: Enhance Interactive Mode

- Update interactive mode rendering
- Add use case display for current agent
- Test interactive UI

### Phase 4: Enhance JSON Export

- Update export_profile to include use cases
- Update import_profile to handle use cases
- Validate JSON schema

### Phase 5: Add Validation

- Implement use case validation
- Add warnings for missing use cases
- Update documentation

## Documentation Updates

```markdown
# Agent Use Cases

Each agent includes use case metadata describing when and why to use it.

## CLI Output

Use cases are displayed in recommendation output:

```
✓ terraform-specialist [████████████████████] 92%
  Terraform configuration, modules, state management
  Use for: Infrastructure as code, cloud resource
           provisioning, multi-environment deployments
  Detected: *.tf files, *.tfvars files
```

## Interactive Mode

Use cases are shown for the currently highlighted agent to help with selection decisions.

## Exported Profiles

Use case metadata is included in exported JSON profiles:

```json
{
  "name": "terraform-specialist",
  "use_cases": "Infrastructure as code, cloud resource provisioning..."
}
```

## Adding Use Cases

Use cases are defined in AGENTS_REGISTRY.md:

```markdown
#### 1. terraform-specialist

**Use for:** Infrastructure as code, cloud resource provisioning, multi-environment deployments
```
```
