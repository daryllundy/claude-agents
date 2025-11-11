# Design Document

## Overview

This document outlines the design for enhancing the agent recommendation script to provide comprehensive coverage of all 30 agents, improved detection accuracy, better user experience through interactive features, and team collaboration capabilities through profile export/import.

The enhanced script will maintain backward compatibility while adding new features through optional flags. The core detection engine will be refactored to support confidence scoring and more sophisticated pattern matching.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI Argument Parser                       │
│  (--dry-run, --interactive, --export, --import, --verbose)  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                   Detection Engine                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   File       │  │   Path       │  │   Content    │      │
│  │  Detection   │  │  Detection   │  │  Detection   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Confidence Scoring Engine                       │
│  (Calculates scores based on detection signal strength)     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                 Output Formatter                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Standard    │  │ Interactive  │  │   Export     │      │
│  │   Output     │  │    Mode      │  │   (JSON)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  Download Manager                            │
│  (Fetches agent files from repository with retry logic)     │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **CLI Argument Parser** validates and processes command-line arguments
2. **Detection Engine** scans the project for technology signals
3. **Confidence Scoring Engine** calculates recommendation strength
4. **Output Formatter** presents results based on selected mode
5. **Download Manager** fetches selected agent files

## Components and Interfaces

### 1. Detection Engine

The detection engine is the core component responsible for identifying technologies and practices in a project.

#### Detection Pattern Structure

Each agent will have a detection configuration with multiple patterns:

```bash
# Detection pattern structure
declare -A AGENT_PATTERNS=(
  ["aws-specialist"]="
    file:*.tf:10
    content:aws_:15
    content:provider \"aws\":20
    file:cloudformation.yaml:15
    file:cdk.json:15
    path:.aws:10
  "
  ["terraform-specialist"]="
    file:*.tf:20
    file:*.tfvars:15
    file:terraform.tfstate:25
    path:terraform:15
    content:terraform:10
  "
)
```

Pattern format: `type:pattern:weight`
- **type**: `file`, `path`, or `content`
- **pattern**: The pattern to match
- **weight**: Contribution to confidence score (0-25)

#### Detection Functions

```bash
# Enhanced detection functions with scoring
detect_file_pattern() {
  local pattern="$1"
  local weight="$2"
  if has_file "$pattern"; then
    return $weight
  fi
  return 0
}

detect_path_pattern() {
  local pattern="$1"
  local weight="$2"
  if has_path "$pattern"; then
    return $weight
  fi
  return 0
}

detect_content_pattern() {
  local pattern="$1"
  local weight="$2"
  if search_contents "$pattern"; then
    return $weight
  fi
  return 0
}
```

### 2. Confidence Scoring Engine

Calculates confidence scores (0-100) based on accumulated detection weights.

#### Scoring Algorithm

```bash
calculate_confidence() {
  local agent="$1"
  local total_weight=0
  local max_possible_weight=100
  
  # Parse detection patterns for agent
  local patterns="${AGENT_PATTERNS[$agent]}"
  
  # Execute each pattern and accumulate weights
  while IFS= read -r pattern_line; do
    [[ -z "$pattern_line" ]] && continue
    
    IFS=':' read -r type pattern weight <<< "$pattern_line"
    
    case "$type" in
      file)
        if has_file "$pattern"; then
          ((total_weight += weight))
        fi
        ;;
      path)
        if has_path "$pattern"; then
          ((total_weight += weight))
        fi
        ;;
      content)
        if search_contents "$pattern"; then
          ((total_weight += weight))
        fi
        ;;
    esac
  done <<< "$patterns"
  
  # Calculate percentage score
  local confidence=$((total_weight * 100 / max_possible_weight))
  [[ $confidence -gt 100 ]] && confidence=100
  
  echo "$confidence"
}
```

#### Confidence Thresholds

- **75-100**: Highly Recommended (strong signals)
- **50-74**: Recommended (moderate signals)
- **25-49**: Suggested (weak signals)
- **0-24**: Not recommended (insufficient signals)

### 3. Agent Registry Parser

Parses AGENTS_REGISTRY.md to extract agent metadata.

#### Registry Data Structure

```bash
declare -A AGENT_CATEGORIES
declare -A AGENT_DESCRIPTIONS
declare -A AGENT_USE_CASES

parse_agent_registry() {
  local registry_file=".claude/agents/AGENTS_REGISTRY.md"
  local current_agent=""
  local current_category=""
  
  while IFS= read -r line; do
    # Parse agent headers (#### 1. agent-name)
    if [[ $line =~ ^####[[:space:]]+[0-9]+\.[[:space:]]+(.+)$ ]]; then
      current_agent="${BASH_REMATCH[1]}"
    fi
    
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
  done < "$registry_file"
}
```

### 4. Interactive Selection Mode

Provides a terminal-based UI for agent selection using bash built-ins.

#### Interactive UI Flow

```
┌─────────────────────────────────────────────────────────────┐
│           Agent Recommendation - Interactive Mode            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Infrastructure (4 agents)                                   │
│  [✓] aws-specialist (Confidence: 85%)                       │
│      AWS cloud services, CloudFormation, CDK                │
│  [✓] terraform-specialist (Confidence: 92%)                 │
│      Terraform configuration and modules                     │
│  [ ] kubernetes-specialist (Confidence: 45%)                │
│      Kubernetes orchestration and Helm                       │
│  [✓] docker-specialist (Confidence: 78%)                    │
│      Docker containerization                                 │
│                                                              │
│  Development (2 agents)                                      │
│  [✓] frontend-specialist (Confidence: 88%)                  │
│      React, Vue, Angular development                         │
│  [ ] database-specialist (Confidence: 35%)                  │
│      Database design and optimization                        │
│                                                              │
│  Navigation: ↑/↓ to move, SPACE to toggle, ENTER to confirm │
│  Commands: a=select all, n=select none, q=quit              │
└─────────────────────────────────────────────────────────────┘
```

#### Implementation Approach

```bash
interactive_selection() {
  local -a agent_list=("${!recommended_agents[@]}")
  local -A selected_agents
  local current_index=0
  
  # Pre-select agents above threshold
  for agent in "${agent_list[@]}"; do
    local confidence="${agent_confidence[$agent]}"
    if [[ $confidence -ge 50 ]]; then
      selected_agents[$agent]=1
    fi
  done
  
  while true; do
    clear
    display_interactive_ui "$current_index" selected_agents agent_list
    
    read -rsn1 key
    case "$key" in
      $'\x1b')  # Arrow keys
        read -rsn2 key
        case "$key" in
          '[A') ((current_index > 0)) && ((current_index--)) ;;  # Up
          '[B') ((current_index < ${#agent_list[@]} - 1)) && ((current_index++)) ;;  # Down
        esac
        ;;
      ' ')  # Space - toggle selection
        local agent="${agent_list[$current_index]}"
        if [[ ${selected_agents[$agent]:-0} -eq 1 ]]; then
          unset selected_agents[$agent]
        else
          selected_agents[$agent]=1
        fi
        ;;
      '')  # Enter - confirm
        break
        ;;
      'a')  # Select all
        for agent in "${agent_list[@]}"; do
          selected_agents[$agent]=1
        done
        ;;
      'n')  # Select none
        selected_agents=()
        ;;
      'q')  # Quit
        exit 0
        ;;
    esac
  done
  
  # Return selected agents
  for agent in "${!selected_agents[@]}"; do
    echo "$agent"
  done
}
```

### 5. Profile Export/Import

Enables sharing agent configurations across teams.

#### Profile JSON Schema

```json
{
  "version": "1.0",
  "generated_at": "2025-11-10T14:30:00Z",
  "project_name": "my-project",
  "detection_results": {
    "technologies_detected": [
      "terraform",
      "aws",
      "docker",
      "react"
    ],
    "agents_recommended": [
      {
        "name": "terraform-specialist",
        "confidence": 92,
        "category": "Infrastructure (IaC)",
        "patterns_matched": [
          "file:*.tf",
          "file:*.tfvars",
          "content:terraform"
        ]
      },
      {
        "name": "aws-specialist",
        "confidence": 85,
        "category": "Infrastructure (Cloud)",
        "patterns_matched": [
          "content:aws_",
          "content:provider \"aws\""
        ]
      }
    ]
  },
  "selected_agents": [
    "terraform-specialist",
    "aws-specialist",
    "docker-specialist",
    "frontend-specialist"
  ]
}
```

#### Export Function

```bash
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
    
    cat >> "$output_file" <<EOF
      {
        "name": "$agent",
        "confidence": ${agent_confidence[$agent]},
        "category": "${AGENT_CATEGORIES[$agent]}",
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

#### Import Function

```bash
import_profile() {
  local input_file="$1"
  
  if [[ ! -f "$input_file" ]]; then
    echo "Error: Profile file not found: $input_file" >&2
    exit 1
  fi
  
  # Validate JSON
  if ! jq empty "$input_file" 2>/dev/null; then
    echo "Error: Invalid JSON in profile file" >&2
    exit 1
  fi
  
  # Extract selected agents
  local -a agents
  mapfile -t agents < <(jq -r '.selected_agents[]' "$input_file")
  
  log "Importing profile from $input_file"
  log "Selected agents: ${agents[*]}"
  
  # Download agents
  for agent in "${agents[@]}"; do
    fetch_agent "$agent"
  done
}
```

### 6. Update Detection

Checks for updates to locally installed agents.

#### Update Check Function

```bash
check_updates() {
  local -a local_agents
  mapfile -t local_agents < <(find "$AGENTS_DIR" -name "*.md" -not -name "AGENTS_REGISTRY.md" -exec basename {} .md \;)
  
  local -a updates_available=()
  
  for agent in "${local_agents[@]}"; do
    local local_file="${AGENTS_DIR}/${agent}.md"
    local remote_url="${BASE_URL}/${agent}.md"
    
    # Get remote file hash
    local remote_hash=$(curl -fsSL "$remote_url" | sha256sum | cut -d' ' -f1)
    local local_hash=$(sha256sum "$local_file" | cut -d' ' -f1)
    
    if [[ "$remote_hash" != "$local_hash" ]]; then
      updates_available+=("$agent")
    fi
  done
  
  if [[ ${#updates_available[@]} -eq 0 ]]; then
    log "All agents are up to date"
  else
    log "Updates available for: ${updates_available[*]}"
  fi
  
  echo "${updates_available[@]}"
}

update_all_agents() {
  local -a agents_to_update
  mapfile -t agents_to_update < <(check_updates)
  
  if [[ ${#agents_to_update[@]} -eq 0 ]]; then
    return
  fi
  
  for agent in "${agents_to_update[@]}"; do
    local backup_file="${AGENTS_DIR}/${agent}.md.backup"
    cp "${AGENTS_DIR}/${agent}.md" "$backup_file"
    log "Backed up $agent to $backup_file"
    
    fetch_agent "$agent"
  done
}
```

### 7. Enhanced Output Formatter

Provides categorized, descriptive output with confidence indicators.

#### Output Format

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
│    Detected: *.tf files, *.tfvars files, terraform content  │
│                                                              │
│  ✓ aws-specialist [████████████████░░░░] 85%                │
│    AWS cloud services, CloudFormation, CDK                   │
│    Detected: aws_ content, provider "aws" content           │
│                                                              │
│  ✓ docker-specialist [███████████████░░░░░] 78%             │
│    Docker containerization and optimization                  │
│    Detected: Dockerfile, docker-compose.yml                  │
│                                                              │
│  ~ kubernetes-specialist [████████░░░░░░░░░░░░] 45%         │
│    Kubernetes orchestration and Helm charts                  │
│    Detected: k8s directory                                   │
│                                                              │
│  Development Agents (1 recommended)                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                              │
│  ✓ frontend-specialist [█████████████████░░░] 88%           │
│    React, Vue, Angular development                           │
│    Detected: package.json with react, src/components         │
│                                                              │
│  Legend:                                                     │
│  ✓ = Recommended (50%+)  ~ = Suggested (25-49%)             │
│                                                              │
│  Use --interactive to select agents manually                 │
│  Use --export profile.json to save this configuration        │
└─────────────────────────────────────────────────────────────┘
```

## Data Models

### Agent Detection Configuration

```bash
# Agent metadata
declare -A AGENT_CATEGORIES=(
  ["aws-specialist"]="Infrastructure (Cloud)"
  ["terraform-specialist"]="Infrastructure (IaC)"
  ["kubernetes-specialist"]="Infrastructure (Platform)"
  # ... all 30 agents
)

declare -A AGENT_DESCRIPTIONS=(
  ["aws-specialist"]="AWS cloud services, architecture, CloudFormation, CDK"
  ["terraform-specialist"]="Terraform configuration, modules, state management"
  # ... all 30 agents
)

# Detection patterns with weights
declare -A AGENT_PATTERNS=(
  ["aws-specialist"]="
    file:*.tf:10
    content:aws_:15
    content:provider \"aws\":20
    file:cloudformation.yaml:15
    file:cdk.json:15
    path:.aws:10
  "
  # ... all 30 agents
)

# Runtime data
declare -A agent_confidence  # agent_name -> confidence_score (0-100)
declare -A agent_patterns_matched  # agent_name -> array of matched patterns
declare -a recommended_agents  # List of agents above threshold
declare -a suggested_agents  # List of agents below threshold but with some signals
```

## Error Handling

### Error Categories and Responses

1. **Network Errors**
   - Implement exponential backoff retry (3 attempts)
   - Provide offline mode suggestion
   - Display specific HTTP status codes

2. **File System Errors**
   - Check write permissions before creating directories
   - Validate file paths before operations
   - Provide clear error messages for permission issues

3. **Invalid Arguments**
   - Validate all command-line arguments
   - Display help message with error highlighted
   - Suggest correct usage

4. **Invalid Profile Format**
   - Validate JSON schema on import
   - Provide specific error messages for schema violations
   - Suggest profile regeneration

### Error Handling Implementation

```bash
# Network error handling with retry
fetch_with_retry() {
  local url="$1"
  local output="$2"
  local max_attempts=3
  local attempt=1
  local backoff=1
  
  while [[ $attempt -le $max_attempts ]]; do
    if curl -fsSL "$url" -o "$output"; then
      return 0
    fi
    
    local http_code=$(curl -fsSL -w "%{http_code}" -o /dev/null "$url")
    log "Attempt $attempt failed (HTTP $http_code). Retrying in ${backoff}s..."
    
    sleep $backoff
    ((backoff *= 2))
    ((attempt++))
  done
  
  echo "Error: Failed to download from $url after $max_attempts attempts" >&2
  return 1
}

# Argument validation
validate_arguments() {
  if [[ -n "$MIN_CONFIDENCE" ]] && ! [[ "$MIN_CONFIDENCE" =~ ^[0-9]+$ ]]; then
    echo "Error: --min-confidence must be a number (0-100)" >&2
    print_help >&2
    exit 1
  fi
  
  if [[ -n "$EXPORT_FILE" ]] && [[ -f "$EXPORT_FILE" ]] && [[ $FORCE == false ]]; then
    echo "Error: Export file already exists: $EXPORT_FILE (use --force to overwrite)" >&2
    exit 1
  fi
}
```

## Testing Strategy

### Unit Testing Approach

Test individual functions in isolation using bash testing frameworks (bats or shunit2).

#### Test Categories

1. **Detection Function Tests**
   - Test `has_file()` with various file patterns
   - Test `has_path()` with directory structures
   - Test `search_contents()` with different content patterns
   - Test edge cases (empty directories, permission issues)

2. **Confidence Scoring Tests**
   - Test score calculation with various pattern combinations
   - Test threshold boundaries (49%, 50%, 74%, 75%)
   - Test maximum score capping at 100%
   - Test zero-signal scenarios

3. **Profile Export/Import Tests**
   - Test JSON generation and parsing
   - Test schema validation
   - Test invalid profile handling
   - Test agent name validation against registry

4. **Interactive Mode Tests**
   - Test keyboard input handling (mocked)
   - Test selection state management
   - Test UI rendering (snapshot testing)

### Integration Testing

Test complete workflows end-to-end.

#### Test Scenarios

1. **Standard Recommendation Flow**
   - Create test project with known technologies
   - Run script and verify correct agents recommended
   - Verify confidence scores match expectations

2. **Interactive Selection Flow**
   - Simulate user interactions
   - Verify selected agents are downloaded
   - Verify unselected agents are skipped

3. **Export/Import Flow**
   - Export profile from test project
   - Import profile in clean directory
   - Verify same agents are downloaded

4. **Update Detection Flow**
   - Create local agents with known content
   - Mock remote agents with different content
   - Verify updates are detected correctly

### Test Project Structures

Create fixture projects for testing:

```
tests/
  fixtures/
    aws-terraform-project/
      main.tf
      variables.tf
      provider.tf (with aws provider)
    react-frontend-project/
      package.json (with react)
      src/
        components/
    kubernetes-project/
      k8s/
        deployment.yaml
        service.yaml
      Dockerfile
```

### Continuous Testing

```bash
# Test runner script
run_tests() {
  local test_dir="tests"
  local failed=0
  
  for test_file in "$test_dir"/*.bats; do
    echo "Running $(basename "$test_file")..."
    if ! bats "$test_file"; then
      ((failed++))
    fi
  done
  
  if [[ $failed -eq 0 ]]; then
    echo "All tests passed!"
    return 0
  else
    echo "$failed test file(s) failed"
    return 1
  fi
}
```

## Performance Considerations

### Optimization Strategies

1. **Parallel Detection**
   - Run independent detection patterns in parallel using background jobs
   - Collect results and aggregate scores

2. **Caching**
   - Cache file search results to avoid redundant filesystem scans
   - Cache content search results for repeated patterns

3. **Early Termination**
   - Stop detection for an agent once confidence reaches 100%
   - Skip expensive content searches if file/path patterns already provide high confidence

4. **Efficient Content Search**
   - Use `ripgrep` when available (faster than `grep`)
   - Limit search depth for large repositories
   - Exclude common directories (.git, node_modules, vendor)

### Performance Implementation

```bash
# Parallel detection with job control
detect_all_agents_parallel() {
  local -a pids=()
  
  for agent in "${!AGENT_PATTERNS[@]}"; do
    (
      confidence=$(calculate_confidence "$agent")
      echo "$agent:$confidence"
    ) &
    pids+=($!)
  done
  
  # Wait for all background jobs
  for pid in "${pids[@]}"; do
    wait "$pid"
  done
}

# Cached content search
declare -A content_search_cache

cached_search_contents() {
  local pattern="$1"
  
  if [[ -n "${content_search_cache[$pattern]}" ]]; then
    return "${content_search_cache[$pattern]}"
  fi
  
  if search_contents "$pattern"; then
    content_search_cache[$pattern]=0
    return 0
  else
    content_search_cache[$pattern]=1
    return 1
  fi
}
```

## Security Considerations

1. **Input Validation**
   - Sanitize all user inputs (file paths, URLs)
   - Validate JSON schema for imported profiles
   - Prevent path traversal attacks

2. **Network Security**
   - Use HTTPS for all downloads
   - Verify repository URL format
   - Implement timeout for network requests

3. **File System Security**
   - Check write permissions before file operations
   - Create files with appropriate permissions (644 for files, 755 for directories)
   - Avoid following symlinks in detection

4. **Credential Protection**
   - Never log or display sensitive information
   - Don't include credentials in exported profiles
   - Warn users about sharing profiles publicly

## Deployment and Rollout

### Backward Compatibility

- All existing command-line arguments continue to work
- Default behavior (no flags) remains unchanged
- New features are opt-in through flags

### Migration Path

1. **Phase 1**: Add new detection patterns for missing agents
2. **Phase 2**: Implement confidence scoring (non-breaking)
3. **Phase 3**: Add enhanced output formatting
4. **Phase 4**: Implement interactive mode
5. **Phase 5**: Add export/import functionality
6. **Phase 6**: Implement update detection

### Documentation Updates

- Update README with new features and examples
- Add CHANGELOG documenting all enhancements
- Create usage examples for each new feature
- Update help text with new flags
