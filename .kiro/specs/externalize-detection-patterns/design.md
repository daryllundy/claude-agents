# Design Document

## Overview

This document outlines the design for externalizing agent detection patterns from hardcoded shell code into declarative YAML data files. The solution enables easier maintenance, version control, and customization of detection patterns while maintaining backward compatibility with existing functionality.

The design introduces a pattern loading system that reads YAML files at runtime, validates schema, and supports custom pattern overrides for team-specific or industry-specific configurations.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Pattern File System                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  data/patterns/                                              │
│  ├── infrastructure.yml    (Cloud, IaC, Platform agents)    │
│  ├── development.yml       (Frontend, Backend, Mobile)      │
│  ├── quality.yml           (Testing, Security, Review)      │
│  ├── operations.yml        (Migration, Dependency, Git)     │
│  ├── productivity.yml      (Scaffolding, Docs, Debug)       │
│  ├── business.yml          (Validation, Architecture, i18n) │
│  └── specialized.yml       (Data Science, E-commerce)       │
│                                                              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  Pattern Loader                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   File       │  │   Schema     │  │   Parser     │      │
│  │  Discovery   │  │  Validation  │  │   (yq/jq)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Pattern Data Structures                         │
│  (Associative arrays populated from YAML)                   │
│  - AGENT_PATTERNS                                            │
│  - AGENT_CATEGORIES                                          │
│  - AGENT_DESCRIPTIONS                                        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                Detection Engine                              │
│  (Unchanged - uses populated data structures)                │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **Pattern Loader** discovers and reads YAML files from data directory
2. **Schema Validator** ensures pattern files conform to expected structure
3. **Parser** converts YAML to bash associative arrays
4. **Detection Engine** uses populated data structures (no changes needed)

## Components and Interfaces

### 1. Pattern File Schema

YAML structure for defining agent detection patterns.

#### Schema Definition

```yaml
# data/patterns/infrastructure.yml

version: "1.0"
category: "Infrastructure"

agents:
  - name: "aws-specialist"
    description: "AWS cloud services, architecture, CloudFormation, CDK"
    category: "Infrastructure (Cloud)"
    patterns:
      - type: "file"
        match: "*.tf"
        weight: 10
      - type: "content"
        match: "aws_"
        weight: 15
      - type: "content"
        match: 'provider "aws"'
        weight: 20
      - type: "file"
        match: "cloudformation.yaml"
        weight: 15
      - type: "file"
        match: "cdk.json"
        weight: 15
      - type: "path"
        match: ".aws"
        weight: 10

  - name: "terraform-specialist"
    description: "Terraform configuration, modules, state management"
    category: "Infrastructure (IaC)"
    patterns:
      - type: "file"
        match: "*.tf"
        weight: 20
      - type: "file"
        match: "*.tfvars"
        weight: 15
      - type: "file"
        match: "terraform.tfstate"
        weight: 25
      - type: "path"
        match: "terraform"
        weight: 15
      - type: "content"
        match: "terraform"
        weight: 10

  - name: "kubernetes-specialist"
    description: "Kubernetes orchestration, Helm charts, manifests"
    category: "Infrastructure (Platform)"
    patterns:
      - type: "path"
        match: "k8s"
        weight: 20
      - type: "path"
        match: "kubernetes"
        weight: 20
      - type: "file"
        match: "Chart.yaml"
        weight: 20
      - type: "file"
        match: "values.yaml"
        weight: 10
      - type: "file"
        match: "kustomization.yaml"
        weight: 15
      - type: "content"
        match: "apiVersion"
        weight: 10
```

#### Pattern Types

- **file**: Match file names or extensions (supports glob patterns)
- **path**: Match directory names or paths
- **content**: Match text content within files (regex supported)

#### Weight Guidelines

- **25**: Strong indicator (e.g., terraform.tfstate for Terraform)
- **20**: Primary indicator (e.g., *.tf files for Terraform)
- **15**: Secondary indicator (e.g., *.tfvars for Terraform)
- **10**: Weak indicator (e.g., terraform in content)

### 2. Pattern Loader

Discovers and loads pattern files from the data directory.

#### File Discovery

```bash
# Pattern file locations
PATTERNS_DIR="${PATTERNS_DIR:-data/patterns}"
CUSTOM_PATTERNS_DIR="${CUSTOM_PATTERNS_DIR:-}"

# Discover pattern files
discover_pattern_files() {
  local pattern_dir="$1"
  local -a files=()
  
  if [[ ! -d "$pattern_dir" ]]; then
    echo "Error: Pattern directory not found: $pattern_dir" >&2
    return 1
  fi
  
  # Find all YAML files
  while IFS= read -r -d '' file; do
    files+=("$file")
  done < <(find "$pattern_dir" -name "*.yml" -o -name "*.yaml" -print0)
  
  if [[ ${#files[@]} -eq 0 ]]; then
    echo "Error: No pattern files found in $pattern_dir" >&2
    return 1
  fi
  
  printf '%s\n' "${files[@]}"
}

# Load patterns with custom override support
load_pattern_files() {
  local -a pattern_files=()
  
  # Use custom patterns if specified
  if [[ -n "$CUSTOM_PATTERNS_DIR" ]]; then
    log "Loading custom patterns from: $CUSTOM_PATTERNS_DIR"
    mapfile -t pattern_files < <(discover_pattern_files "$CUSTOM_PATTERNS_DIR")
  else
    log "Loading default patterns from: $PATTERNS_DIR"
    mapfile -t pattern_files < <(discover_pattern_files "$PATTERNS_DIR")
  fi
  
  # Load each file
  for file in "${pattern_files[@]}"; do
    load_pattern_file "$file"
  done
}
```

#### YAML Parser

```bash
# Check for YAML parser availability
check_yaml_parser() {
  if command -v yq &> /dev/null; then
    echo "yq"
  elif command -v python3 &> /dev/null; then
    echo "python3"
  else
    echo "Error: No YAML parser found. Install yq or python3 with PyYAML" >&2
    return 1
  fi
}

# Parse YAML using yq
parse_yaml_with_yq() {
  local file="$1"
  yq eval -o=json "$file"
}

# Parse YAML using Python
parse_yaml_with_python() {
  local file="$1"
  python3 -c "
import yaml
import json
import sys

try:
    with open('$file', 'r') as f:
        data = yaml.safe_load(f)
        print(json.dumps(data))
except Exception as e:
    print(f'Error parsing YAML: {e}', file=sys.stderr)
    sys.exit(1)
"
}

# Parse YAML file to JSON
parse_yaml() {
  local file="$1"
  local parser
  
  parser=$(check_yaml_parser) || return 1
  
  case "$parser" in
    yq)
      parse_yaml_with_yq "$file"
      ;;
    python3)
      parse_yaml_with_python "$file"
      ;;
  esac
}
```

### 3. Schema Validator

Validates pattern file structure before loading.

```bash
# Validate pattern file schema
validate_pattern_schema() {
  local json="$1"
  local file="$2"
  
  # Check required top-level fields
  if ! echo "$json" | jq -e '.version' &> /dev/null; then
    echo "Error: Missing 'version' field in $file" >&2
    return 1
  fi
  
  if ! echo "$json" | jq -e '.agents' &> /dev/null; then
    echo "Error: Missing 'agents' array in $file" >&2
    return 1
  fi
  
  # Validate each agent
  local agent_count
  agent_count=$(echo "$json" | jq '.agents | length')
  
  for ((i=0; i<agent_count; i++)); do
    local agent_json
    agent_json=$(echo "$json" | jq ".agents[$i]")
    
    # Check required agent fields
    if ! echo "$agent_json" | jq -e '.name' &> /dev/null; then
      echo "Error: Agent at index $i missing 'name' in $file" >&2
      return 1
    fi
    
    if ! echo "$agent_json" | jq -e '.patterns' &> /dev/null; then
      echo "Error: Agent at index $i missing 'patterns' in $file" >&2
      return 1
    fi
    
    # Validate patterns
    local pattern_count
    pattern_count=$(echo "$agent_json" | jq '.patterns | length')
    
    for ((j=0; j<pattern_count; j++)); do
      local pattern_json
      pattern_json=$(echo "$agent_json" | jq ".patterns[$j]")
      
      # Check required pattern fields
      if ! echo "$pattern_json" | jq -e '.type' &> /dev/null; then
        echo "Error: Pattern at index $j for agent $i missing 'type' in $file" >&2
        return 1
      fi
      
      if ! echo "$pattern_json" | jq -e '.match' &> /dev/null; then
        echo "Error: Pattern at index $j for agent $i missing 'match' in $file" >&2
        return 1
      fi
      
      if ! echo "$pattern_json" | jq -e '.weight' &> /dev/null; then
        echo "Error: Pattern at index $j for agent $i missing 'weight' in $file" >&2
        return 1
      fi
      
      # Validate pattern type
      local pattern_type
      pattern_type=$(echo "$pattern_json" | jq -r '.type')
      
      if [[ ! "$pattern_type" =~ ^(file|path|content)$ ]]; then
        echo "Error: Invalid pattern type '$pattern_type' in $file" >&2
        echo "Valid types: file, path, content" >&2
        return 1
      fi
    done
  done
  
  return 0
}
```

### 4. Pattern Data Structure Population

Convert JSON to bash associative arrays.

```bash
# Global data structures
declare -A AGENT_PATTERNS
declare -A AGENT_CATEGORIES
declare -A AGENT_DESCRIPTIONS

# Load single pattern file
load_pattern_file() {
  local file="$1"
  
  log "Loading patterns from: $file"
  
  # Parse YAML to JSON
  local json
  json=$(parse_yaml "$file") || return 1
  
  # Validate schema
  validate_pattern_schema "$json" "$file" || return 1
  
  # Extract agents
  local agent_count
  agent_count=$(echo "$json" | jq '.agents | length')
  
  for ((i=0; i<agent_count; i++)); do
    local agent_json
    agent_json=$(echo "$json" | jq ".agents[$i]")
    
    # Extract agent metadata
    local agent_name
    agent_name=$(echo "$agent_json" | jq -r '.name')
    
    local description
    description=$(echo "$agent_json" | jq -r '.description // ""')
    
    local category
    category=$(echo "$agent_json" | jq -r '.category // ""')
    
    # Store metadata
    AGENT_DESCRIPTIONS[$agent_name]="$description"
    AGENT_CATEGORIES[$agent_name]="$category"
    
    # Extract patterns
    local patterns=""
    local pattern_count
    pattern_count=$(echo "$agent_json" | jq '.patterns | length')
    
    for ((j=0; j<pattern_count; j++)); do
      local pattern_json
      pattern_json=$(echo "$agent_json" | jq ".patterns[$j]")
      
      local type
      type=$(echo "$pattern_json" | jq -r '.type')
      
      local match
      match=$(echo "$pattern_json" | jq -r '.match')
      
      local weight
      weight=$(echo "$pattern_json" | jq -r '.weight')
      
      # Append to patterns string
      patterns+="${type}:${match}:${weight}"$'\n'
    done
    
    # Store patterns
    AGENT_PATTERNS[$agent_name]="$patterns"
    
    log "  Loaded agent: $agent_name (${pattern_count} patterns)"
  done
}
```

### 5. Custom Pattern Override

Support for custom pattern files via environment variables or flags.

```bash
# Command-line flag parsing
parse_custom_patterns_flag() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --patterns-dir)
        CUSTOM_PATTERNS_DIR="$2"
        shift 2
        ;;
      --patterns-dir=*)
        CUSTOM_PATTERNS_DIR="${1#*=}"
        shift
        ;;
      *)
        shift
        ;;
    esac
  done
}

# Environment variable support
setup_patterns_directory() {
  # Priority: CLI flag > Environment variable > Default
  if [[ -z "$CUSTOM_PATTERNS_DIR" ]]; then
    CUSTOM_PATTERNS_DIR="${AGENT_PATTERNS_DIR:-}"
  fi
  
  if [[ -n "$CUSTOM_PATTERNS_DIR" ]]; then
    if [[ ! -d "$CUSTOM_PATTERNS_DIR" ]]; then
      echo "Error: Custom patterns directory not found: $CUSTOM_PATTERNS_DIR" >&2
      exit 1
    fi
    
    log "Using custom patterns from: $CUSTOM_PATTERNS_DIR"
  else
    log "Using default patterns from: $PATTERNS_DIR"
  fi
}
```

## Data Models

### Pattern File Structure

```yaml
version: "1.0"           # Schema version
category: "string"       # Optional category grouping

agents:
  - name: "agent-name"   # Agent identifier (required)
    description: "text"  # Human-readable description (optional)
    category: "text"     # Agent category (optional)
    patterns:            # Detection patterns (required)
      - type: "file|path|content"  # Pattern type (required)
        match: "pattern"           # Match criteria (required)
        weight: 0-25               # Importance weight (required)
```

### Runtime Data Structures

```bash
# Populated from YAML files
declare -A AGENT_PATTERNS=(
  ["agent-name"]="
    file:*.ext:weight
    path:dirname:weight
    content:regex:weight
  "
)

declare -A AGENT_DESCRIPTIONS=(
  ["agent-name"]="Description text"
)

declare -A AGENT_CATEGORIES=(
  ["agent-name"]="Category name"
)
```

## Error Handling

### Missing Dependencies

```bash
# Check for required tools
check_dependencies() {
  local missing=()
  
  # Check for jq (required)
  if ! command -v jq &> /dev/null; then
    missing+=("jq")
  fi
  
  # Check for YAML parser (yq or python3)
  if ! command -v yq &> /dev/null && ! command -v python3 &> /dev/null; then
    missing+=("yq or python3")
  fi
  
  if [[ ${#missing[@]} -gt 0 ]]; then
    echo "Error: Missing required dependencies: ${missing[*]}" >&2
    echo "Install with: brew install jq yq" >&2
    return 1
  fi
  
  return 0
}
```

### Invalid Pattern Files

```bash
# Graceful error handling for pattern loading
safe_load_patterns() {
  if ! check_dependencies; then
    echo "Error: Cannot load patterns without required tools" >&2
    exit 1
  fi
  
  if ! load_pattern_files; then
    echo "Error: Failed to load pattern files" >&2
    echo "Falling back to hardcoded patterns..." >&2
    initialize_detection_patterns_legacy
    return 1
  fi
  
  # Verify at least some patterns loaded
  if [[ ${#AGENT_PATTERNS[@]} -eq 0 ]]; then
    echo "Error: No patterns loaded from files" >&2
    echo "Falling back to hardcoded patterns..." >&2
    initialize_detection_patterns_legacy
    return 1
  fi
  
  log "Successfully loaded ${#AGENT_PATTERNS[@]} agent patterns"
  return 0
}
```

## Testing Strategy

### Unit Tests

Test pattern loading and validation functions.

```bash
# tests/unit/test_pattern_loading.bats

@test "parse_yaml converts YAML to JSON" {
  cat > test_pattern.yml <<EOF
version: "1.0"
agents:
  - name: "test-agent"
    patterns:
      - type: "file"
        match: "*.test"
        weight: 10
EOF
  
  json=$(parse_yaml test_pattern.yml)
  
  [[ $(echo "$json" | jq -r '.version') == "1.0" ]]
  [[ $(echo "$json" | jq -r '.agents[0].name') == "test-agent" ]]
}

@test "validate_pattern_schema rejects missing version" {
  json='{"agents": []}'
  
  run validate_pattern_schema "$json" "test.yml"
  
  [[ $status -ne 0 ]]
  [[ "$output" =~ "Missing 'version'" ]]
}

@test "validate_pattern_schema rejects invalid pattern type" {
  json='{
    "version": "1.0",
    "agents": [{
      "name": "test",
      "patterns": [{
        "type": "invalid",
        "match": "test",
        "weight": 10
      }]
    }]
  }'
  
  run validate_pattern_schema "$json" "test.yml"
  
  [[ $status -ne 0 ]]
  [[ "$output" =~ "Invalid pattern type" ]]
}

@test "load_pattern_file populates data structures" {
  cat > test_pattern.yml <<EOF
version: "1.0"
agents:
  - name: "test-agent"
    description: "Test description"
    category: "Test"
    patterns:
      - type: "file"
        match: "*.test"
        weight: 10
EOF
  
  load_pattern_file test_pattern.yml
  
  [[ -n "${AGENT_PATTERNS[test-agent]}" ]]
  [[ "${AGENT_DESCRIPTIONS[test-agent]}" == "Test description" ]]
  [[ "${AGENT_CATEGORIES[test-agent]}" == "Test" ]]
}
```

### Integration Tests

Test complete pattern loading workflow.

```bash
# tests/integration/test_pattern_system.bats

@test "load_pattern_files discovers and loads all files" {
  mkdir -p test_patterns
  
  cat > test_patterns/infrastructure.yml <<EOF
version: "1.0"
agents:
  - name: "agent1"
    patterns:
      - type: "file"
        match: "*.tf"
        weight: 20
EOF
  
  cat > test_patterns/development.yml <<EOF
version: "1.0"
agents:
  - name: "agent2"
    patterns:
      - type: "file"
        match: "package.json"
        weight: 15
EOF
  
  PATTERNS_DIR="test_patterns" load_pattern_files
  
  [[ -n "${AGENT_PATTERNS[agent1]}" ]]
  [[ -n "${AGENT_PATTERNS[agent2]}" ]]
}

@test "custom patterns override defaults" {
  mkdir -p default_patterns custom_patterns
  
  cat > default_patterns/test.yml <<EOF
version: "1.0"
agents:
  - name: "test-agent"
    patterns:
      - type: "file"
        match: "*.default"
        weight: 10
EOF
  
  cat > custom_patterns/test.yml <<EOF
version: "1.0"
agents:
  - name: "test-agent"
    patterns:
      - type: "file"
        match: "*.custom"
        weight: 20
EOF
  
  PATTERNS_DIR="default_patterns"
  CUSTOM_PATTERNS_DIR="custom_patterns"
  
  load_pattern_files
  
  [[ "${AGENT_PATTERNS[test-agent]}" =~ "custom" ]]
  [[ ! "${AGENT_PATTERNS[test-agent]}" =~ "default" ]]
}
```

## Performance Considerations

### Caching Parsed Patterns

```bash
# Cache parsed patterns to avoid re-parsing
PATTERN_CACHE_DIR="${TMPDIR:-/tmp}/agent_patterns_cache"

cache_parsed_patterns() {
  local file="$1"
  local cache_file="$PATTERN_CACHE_DIR/$(basename "$file").json"
  
  mkdir -p "$PATTERN_CACHE_DIR"
  
  # Check if cache is valid
  if [[ -f "$cache_file" ]] && [[ "$cache_file" -nt "$file" ]]; then
    cat "$cache_file"
    return 0
  fi
  
  # Parse and cache
  local json
  json=$(parse_yaml "$file")
  echo "$json" > "$cache_file"
  echo "$json"
}
```

### Lazy Loading

```bash
# Load patterns only when needed
PATTERNS_LOADED=false

ensure_patterns_loaded() {
  if [[ $PATTERNS_LOADED == false ]]; then
    safe_load_patterns
    PATTERNS_LOADED=true
  fi
}
```

## Migration Strategy

### Phase 1: Create Pattern Files

- Extract existing patterns from shell code to YAML files
- Organize by category (infrastructure, development, etc.)
- Validate all patterns load correctly

### Phase 2: Add Loading System

- Implement pattern loader and validator
- Add fallback to legacy hardcoded patterns
- Test with existing test suite

### Phase 3: Enable Custom Patterns

- Add CLI flag and environment variable support
- Document custom pattern usage
- Provide example custom pattern files

### Phase 4: Deprecate Hardcoded Patterns

- Remove legacy initialization function
- Make external patterns required
- Update documentation

## Documentation Updates

### Pattern File Documentation

```markdown
# Pattern File Format

Pattern files define detection rules for agent recommendations.

## Schema

```yaml
version: "1.0"
category: "Category Name"  # Optional

agents:
  - name: "agent-name"
    description: "Agent description"
    category: "Agent category"
    patterns:
      - type: "file"      # file, path, or content
        match: "*.ext"    # Pattern to match
        weight: 10        # Importance (0-25)
```

## Pattern Types

- **file**: Match file names (supports glob patterns like `*.tf`)
- **path**: Match directory names or paths
- **content**: Match text within files (supports regex)

## Custom Patterns

Override default patterns:

```bash
# Via environment variable
export AGENT_PATTERNS_DIR=/path/to/custom/patterns
./scripts/recommend_agents.sh

# Via command-line flag
./scripts/recommend_agents.sh --patterns-dir=/path/to/custom/patterns
```
```

### README Updates

- Add section on pattern customization
- Document required dependencies (jq, yq/python3)
- Provide examples of custom pattern files
- Add troubleshooting for pattern loading issues
