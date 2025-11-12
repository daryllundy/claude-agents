# Design Document

## Overview

This document outlines the design for fixing the confidence score calculation in the agent recommendation system. The current implementation uses a fixed maximum weight of 100, which doesn't reflect the actual sum of pattern weights defined for each agent. This leads to inaccurate confidence percentages and premature score saturation.

The solution dynamically calculates the maximum possible weight for each agent based on its configured patterns, ensuring accurate and comparable confidence scores across all agents.

## Architecture

### Current (Incorrect) Implementation

```
┌─────────────────────────────────────────────────────────────┐
│              calculate_confidence(agent)                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  accumulated_weight = 0                                      │
│  max_possible_weight = 100  ← FIXED CONSTANT (WRONG)        │
│                                                              │
│  for each pattern in agent_patterns:                         │
│    if pattern matches:                                       │
│      accumulated_weight += pattern.weight                    │
│                                                              │
│  confidence = (accumulated_weight / 100) × 100               │
│                                                              │
│  Problem: If agent has patterns totaling 85, max is 85%     │
│           If agent has patterns totaling 150, saturates early│
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### New (Correct) Implementation

```
┌─────────────────────────────────────────────────────────────┐
│              calculate_confidence(agent)                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  accumulated_weight = 0                                      │
│  max_possible_weight = 0                                     │
│                                                              │
│  for each pattern in agent_patterns:                         │
│    max_possible_weight += pattern.weight                     │
│    if pattern matches:                                       │
│      accumulated_weight += pattern.weight                    │
│                                                              │
│  if max_possible_weight == 0:                                │
│    confidence = 0                                            │
│  else:                                                       │
│    confidence = (accumulated_weight / max_possible_weight) × 100│
│    confidence = min(confidence, 100)                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Detection Engine                            │
│  (Evaluates patterns and accumulates weights)                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│            Confidence Calculation                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  1. Calculate Max Possible Weight                    │   │
│  │     Sum all pattern weights for agent                │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  2. Calculate Accumulated Weight                     │   │
│  │     Sum weights of matched patterns                  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  3. Compute Confidence Percentage                    │   │
│  │     (accumulated / max_possible) × 100               │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  4. Cap at 100%                                      │   │
│  │     min(confidence, 100)                             │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Ranking and Display                             │
│  (Sort agents by normalized confidence scores)               │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Enhanced Confidence Calculation Function

Replace the existing `calculate_confidence()` function with a corrected implementation.

#### Current Implementation (Incorrect)

```bash
calculate_confidence() {
  local agent="$1"
  local total_weight=0
  local max_possible_weight=100  # WRONG: Fixed constant
  
  local patterns="${AGENT_PATTERNS[$agent]}"
  
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
  
  local confidence=$((total_weight * 100 / max_possible_weight))
  [[ $confidence -gt 100 ]] && confidence=100
  
  echo "$confidence"
}
```

#### New Implementation (Correct)

```bash
calculate_confidence() {
  local agent="$1"
  local accumulated_weight=0
  local max_possible_weight=0
  
  local patterns="${AGENT_PATTERNS[$agent]}"
  
  # First pass: calculate max possible weight and accumulated weight
  while IFS= read -r pattern_line; do
    [[ -z "$pattern_line" ]] && continue
    
    IFS=':' read -r type pattern weight <<< "$pattern_line"
    
    # Add to max possible weight
    ((max_possible_weight += weight))
    
    # Check if pattern matches and add to accumulated weight
    local matches=false
    case "$type" in
      file)
        has_file "$pattern" && matches=true
        ;;
      path)
        has_path "$pattern" && matches=true
        ;;
      content)
        search_contents "$pattern" && matches=true
        ;;
    esac
    
    if [[ $matches == true ]]; then
      ((accumulated_weight += weight))
    fi
  done <<< "$patterns"
  
  # Calculate confidence percentage
  local confidence=0
  if [[ $max_possible_weight -gt 0 ]]; then
    confidence=$((accumulated_weight * 100 / max_possible_weight))
    
    # Cap at 100%
    [[ $confidence -gt 100 ]] && confidence=100
  fi
  
  # Log in verbose mode
  if [[ ${VERBOSE:-false} == true ]]; then
    log "  $agent: accumulated=$accumulated_weight, max=$max_possible_weight, confidence=$confidence%"
  fi
  
  echo "$confidence"
}
```

### 2. Max Possible Weight Calculation

Extract max weight calculation into a separate function for reusability.

```bash
# Calculate maximum possible weight for an agent
calculate_max_possible_weight() {
  local agent="$1"
  local max_weight=0
  
  local patterns="${AGENT_PATTERNS[$agent]}"
  
  while IFS= read -r pattern_line; do
    [[ -z "$pattern_line" ]] && continue
    
    IFS=':' read -r type pattern weight <<< "$pattern_line"
    ((max_weight += weight))
  done <<< "$patterns"
  
  echo "$max_weight"
}

# Get max weights for all agents (useful for debugging)
get_all_max_weights() {
  declare -A max_weights
  
  for agent in "${!AGENT_PATTERNS[@]}"; do
    max_weights[$agent]=$(calculate_max_possible_weight "$agent")
  done
  
  # Print sorted by agent name
  for agent in $(printf '%s\n' "${!max_weights[@]}" | sort); do
    printf "%-30s %3d\n" "$agent" "${max_weights[$agent]}"
  done
}
```

### 3. Validation Function

Validate that all agents have positive max possible weights.

```bash
# Validate pattern weights
validate_pattern_weights() {
  local errors=0
  
  for agent in "${!AGENT_PATTERNS[@]}"; do
    local max_weight
    max_weight=$(calculate_max_possible_weight "$agent")
    
    if [[ $max_weight -eq 0 ]]; then
      echo "Warning: Agent '$agent' has zero total pattern weight" >&2
      ((errors++))
    elif [[ $max_weight -lt 0 ]]; then
      echo "Error: Agent '$agent' has negative total pattern weight: $max_weight" >&2
      ((errors++))
    fi
  done
  
  if [[ $errors -gt 0 ]]; then
    echo "Found $errors agents with invalid pattern weights" >&2
    return 1
  fi
  
  return 0
}
```

### 4. Debug Output

Add debug mode to show confidence calculation details.

```bash
# Debug confidence calculation for an agent
debug_confidence_calculation() {
  local agent="$1"
  
  echo "=== Confidence Calculation Debug: $agent ==="
  echo ""
  
  local patterns="${AGENT_PATTERNS[$agent]}"
  local accumulated_weight=0
  local max_possible_weight=0
  
  echo "Pattern Evaluation:"
  echo "-------------------"
  
  while IFS= read -r pattern_line; do
    [[ -z "$pattern_line" ]] && continue
    
    IFS=':' read -r type pattern weight <<< "$pattern_line"
    
    ((max_possible_weight += weight))
    
    local matches=false
    local match_symbol="✗"
    
    case "$type" in
      file)
        if has_file "$pattern"; then
          matches=true
          match_symbol="✓"
          ((accumulated_weight += weight))
        fi
        ;;
      path)
        if has_path "$pattern"; then
          matches=true
          match_symbol="✓"
          ((accumulated_weight += weight))
        fi
        ;;
      content)
        if search_contents "$pattern"; then
          matches=true
          match_symbol="✓"
          ((accumulated_weight += weight))
        fi
        ;;
    esac
    
    printf "%s [%2d] %-10s %s\n" "$match_symbol" "$weight" "$type" "$pattern"
  done <<< "$patterns"
  
  echo ""
  echo "Calculation:"
  echo "------------"
  echo "Accumulated Weight:    $accumulated_weight"
  echo "Max Possible Weight:   $max_possible_weight"
  
  local confidence=0
  if [[ $max_possible_weight -gt 0 ]]; then
    confidence=$((accumulated_weight * 100 / max_possible_weight))
    [[ $confidence -gt 100 ]] && confidence=100
  fi
  
  echo "Confidence:            $confidence%"
  echo ""
}
```

### 5. Comparison Tool

Tool to compare old vs new confidence calculations.

```bash
# Compare old and new confidence calculations
compare_confidence_methods() {
  echo "Agent Confidence Comparison (Old vs New)"
  echo "========================================"
  echo ""
  printf "%-30s %8s %8s %8s\n" "Agent" "Old" "New" "Diff"
  printf "%-30s %8s %8s %8s\n" "-----" "---" "---" "----"
  
  for agent in $(printf '%s\n' "${!AGENT_PATTERNS[@]}" | sort); do
    # Old method (fixed max=100)
    local old_confidence
    old_confidence=$(calculate_confidence_old "$agent")
    
    # New method (dynamic max)
    local new_confidence
    new_confidence=$(calculate_confidence "$agent")
    
    local diff=$((new_confidence - old_confidence))
    local diff_str
    if [[ $diff -gt 0 ]]; then
      diff_str="+$diff"
    else
      diff_str="$diff"
    fi
    
    printf "%-30s %7d%% %7d%% %7s%%\n" "$agent" "$old_confidence" "$new_confidence" "$diff_str"
  done
}

# Old calculation method for comparison
calculate_confidence_old() {
  local agent="$1"
  local total_weight=0
  local max_possible_weight=100  # Fixed constant
  
  local patterns="${AGENT_PATTERNS[$agent]}"
  
  while IFS= read -r pattern_line; do
    [[ -z "$pattern_line" ]] && continue
    
    IFS=':' read -r type pattern weight <<< "$pattern_line"
    
    case "$type" in
      file)
        has_file "$pattern" && ((total_weight += weight))
        ;;
      path)
        has_path "$pattern" && ((total_weight += weight))
        ;;
      content)
        search_contents "$pattern" && ((total_weight += weight))
        ;;
    esac
  done <<< "$patterns"
  
  local confidence=$((total_weight * 100 / max_possible_weight))
  [[ $confidence -gt 100 ]] && confidence=100
  
  echo "$confidence"
}
```

## Data Models

### Pattern Weight Data

```bash
# Pattern definition (unchanged)
declare -A AGENT_PATTERNS=(
  ["agent-name"]="
    file:*.ext:weight
    path:dirname:weight
    content:regex:weight
  "
)

# Calculated max weights (new, for caching)
declare -A AGENT_MAX_WEIGHTS=(
  ["agent-name"]=sum_of_all_weights
)

# Confidence scores (unchanged)
declare -A agent_confidence=(
  ["agent-name"]=percentage_0_to_100
)
```

## Error Handling

### Zero Weight Agents

```bash
# Handle agents with no patterns gracefully
calculate_confidence() {
  local agent="$1"
  local accumulated_weight=0
  local max_possible_weight=0
  
  local patterns="${AGENT_PATTERNS[$agent]}"
  
  # Handle empty patterns
  if [[ -z "$patterns" ]]; then
    if [[ ${VERBOSE:-false} == true ]]; then
      log "  $agent: no patterns defined, confidence=0%"
    fi
    echo "0"
    return 0
  fi
  
  # ... rest of calculation ...
}
```

### Division by Zero

```bash
# Prevent division by zero
if [[ $max_possible_weight -gt 0 ]]; then
  confidence=$((accumulated_weight * 100 / max_possible_weight))
else
  confidence=0
  if [[ ${VERBOSE:-false} == true ]]; then
    log "  Warning: $agent has zero max possible weight"
  fi
fi
```

### Integer Overflow

```bash
# Handle large weight sums safely
calculate_confidence() {
  # ... pattern evaluation ...
  
  # Use bc for large numbers if needed
  if [[ $max_possible_weight -gt 10000 ]]; then
    confidence=$(echo "scale=0; $accumulated_weight * 100 / $max_possible_weight" | bc)
  else
    confidence=$((accumulated_weight * 100 / max_possible_weight))
  fi
  
  [[ $confidence -gt 100 ]] && confidence=100
  
  echo "$confidence"
}
```

## Testing Strategy

### Unit Tests

Test confidence calculation with various pattern configurations.

```bash
# tests/unit/test_confidence_calculation.bats

setup() {
  source scripts/recommend_agents.sh
  
  # Mock detection functions
  has_file() { [[ "$1" == "*.matched" ]]; }
  has_path() { [[ "$1" == "matched_dir" ]]; }
  search_contents() { [[ "$1" == "matched_content" ]]; }
}

@test "calculate_confidence with all patterns matched" {
  AGENT_PATTERNS[test-agent]="
file:*.matched:20
path:matched_dir:15
content:matched_content:10
"
  
  confidence=$(calculate_confidence "test-agent")
  
  # All patterns match: (20+15+10) / (20+15+10) * 100 = 100%
  [[ $confidence -eq 100 ]]
}

@test "calculate_confidence with partial match" {
  AGENT_PATTERNS[test-agent]="
file:*.matched:20
path:unmatched_dir:15
content:matched_content:10
"
  
  confidence=$(calculate_confidence "test-agent")
  
  # Two patterns match: (20+10) / (20+15+10) * 100 = 66%
  [[ $confidence -eq 66 ]]
}

@test "calculate_confidence with no matches" {
  AGENT_PATTERNS[test-agent]="
file:*.unmatched:20
path:unmatched_dir:15
content:unmatched_content:10
"
  
  confidence=$(calculate_confidence "test-agent")
  
  # No patterns match: 0 / 45 * 100 = 0%
  [[ $confidence -eq 0 ]]
}

@test "calculate_confidence with zero patterns" {
  AGENT_PATTERNS[test-agent]=""
  
  confidence=$(calculate_confidence "test-agent")
  
  # No patterns: 0%
  [[ $confidence -eq 0 ]]
}

@test "calculate_max_possible_weight sums all weights" {
  AGENT_PATTERNS[test-agent]="
file:*.test:20
path:test_dir:15
content:test:10
"
  
  max_weight=$(calculate_max_possible_weight "test-agent")
  
  [[ $max_weight -eq 45 ]]
}

@test "confidence never exceeds 100 percent" {
  # Edge case: accumulated weight somehow exceeds max
  AGENT_PATTERNS[test-agent]="
file:*.matched:50
"
  
  # Mock to return true multiple times (shouldn't happen, but test safety)
  confidence=$(calculate_confidence "test-agent")
  
  [[ $confidence -le 100 ]]
}
```

### Integration Tests

Test confidence calculation in realistic scenarios.

```bash
# tests/integration/test_confidence_accuracy.bats

@test "terraform specialist confidence with typical project" {
  # Create test project
  mkdir -p test_project
  cd test_project
  
  touch main.tf
  touch variables.tf
  touch terraform.tfstate
  
  # Load patterns
  source scripts/recommend_agents.sh
  initialize_detection_patterns
  
  # Calculate confidence
  confidence=$(calculate_confidence "terraform-specialist")
  
  # Should be high but not necessarily 100%
  [[ $confidence -ge 50 ]]
  [[ $confidence -le 100 ]]
}

@test "confidence scores are comparable across agents" {
  # Create project with multiple technologies
  mkdir -p test_project
  cd test_project
  
  touch main.tf
  touch Dockerfile
  touch package.json
  
  source scripts/recommend_agents.sh
  initialize_detection_patterns
  
  # Calculate confidence for multiple agents
  tf_confidence=$(calculate_confidence "terraform-specialist")
  docker_confidence=$(calculate_confidence "docker-specialist")
  frontend_confidence=$(calculate_confidence "frontend-specialist")
  
  # All should be in valid range
  [[ $tf_confidence -ge 0 && $tf_confidence -le 100 ]]
  [[ $docker_confidence -ge 0 && $docker_confidence -le 100 ]]
  [[ $frontend_confidence -ge 0 && $frontend_confidence -le 100 ]]
}
```

### Regression Tests

Ensure new calculation doesn't break existing behavior.

```bash
# tests/regression/test_confidence_changes.bats

@test "confidence calculation produces reasonable results" {
  # Test with known project structures
  # Ensure results are within expected ranges
  
  source scripts/recommend_agents.sh
  initialize_detection_patterns
  
  # Test each agent category
  for agent in "${!AGENT_PATTERNS[@]}"; do
    confidence=$(calculate_confidence "$agent")
    
    # Confidence must be 0-100
    [[ $confidence -ge 0 ]]
    [[ $confidence -le 100 ]]
  done
}
```

## Performance Considerations

### Caching Max Weights

```bash
# Cache max weights to avoid recalculation
declare -A AGENT_MAX_WEIGHTS_CACHE

get_max_possible_weight() {
  local agent="$1"
  
  if [[ -z "${AGENT_MAX_WEIGHTS_CACHE[$agent]}" ]]; then
    AGENT_MAX_WEIGHTS_CACHE[$agent]=$(calculate_max_possible_weight "$agent")
  fi
  
  echo "${AGENT_MAX_WEIGHTS_CACHE[$agent]}"
}

# Use cached version in confidence calculation
calculate_confidence_cached() {
  local agent="$1"
  local accumulated_weight=0
  local max_possible_weight
  
  max_possible_weight=$(get_max_possible_weight "$agent")
  
  # ... rest of calculation using cached max weight ...
}
```

## Migration and Deployment

### Backward Compatibility

- Function signature remains unchanged
- Return value format unchanged (integer 0-100)
- No changes to calling code required

### Testing Before Deployment

1. Run comparison tool on test projects
2. Verify confidence scores are more accurate
3. Check that ranking order makes sense
4. Ensure no agents have invalid scores

### Rollout Plan

1. **Phase 1**: Implement new calculation in separate function
2. **Phase 2**: Add comparison tool and validate results
3. **Phase 3**: Replace old function with new implementation
4. **Phase 4**: Add validation and debug tools
5. **Phase 5**: Update documentation

## Documentation Updates

### Confidence Calculation Documentation

```markdown
# Confidence Score Calculation

Confidence scores indicate how well a project matches an agent's expertise area.

## Formula

```
confidence = (accumulated_weight / max_possible_weight) × 100
```

Where:
- **accumulated_weight**: Sum of weights from matched patterns
- **max_possible_weight**: Sum of all pattern weights for the agent

## Example

Agent with patterns:
- `file:*.tf:20` (matches)
- `file:*.tfvars:15` (matches)
- `content:terraform:10` (no match)

Calculation:
- Accumulated: 20 + 15 = 35
- Max Possible: 20 + 15 + 10 = 45
- Confidence: (35 / 45) × 100 = 77.78% ≈ 78%

## Interpretation

- **75-100%**: Highly recommended (strong match)
- **50-74%**: Recommended (moderate match)
- **25-49%**: Suggested (weak match)
- **0-24%**: Not recommended (insufficient match)
```

### README Updates

- Document confidence calculation methodology
- Add examples of confidence scores
- Explain how to interpret confidence percentages
- Add troubleshooting for unexpected scores
