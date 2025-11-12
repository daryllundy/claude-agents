# Design Document

## Overview

This document outlines the design for adding automated test coverage to the interactive selection mode of the agent recommendation script. The solution uses `expect` for simulating user interactions and extracts testable helper functions to enable unit testing of selection logic independently from UI rendering.

The design maintains backward compatibility with the existing interactive mode while making it more testable through separation of concerns and providing comprehensive test coverage for navigation, selection state, and rendering.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Interactive Selection Mode                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Selection State Management                  │    │
│  │  (Testable helper functions)                        │    │
│  │  - init_selection_state()                           │    │
│  │  - toggle_agent_selection()                         │    │
│  │  - select_all_agents()                              │    │
│  │  - select_none_agents()                             │    │
│  │  - get_selected_agents()                            │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │         UI Rendering Functions                      │    │
│  │  (Testable display logic)                           │    │
│  │  - render_agent_list()                              │    │
│  │  - render_category_header()                         │    │
│  │  - render_agent_item()                              │    │
│  │  - render_navigation_footer()                       │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Input Handler                               │    │
│  │  (Keyboard event processing)                        │    │
│  │  - handle_arrow_keys()                              │    │
│  │  - handle_selection_toggle()                        │    │
│  │  - handle_commands()                                │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Test Framework                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │  Unit Tests    │  │  Integration   │  │   Expect     │  │
│  │  (bash/bats)   │  │  Tests (bats)  │  │   Scripts    │  │
│  └────────────────┘  └────────────────┘  └──────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **Selection State Management** maintains agent selection state independently
2. **UI Rendering Functions** generate display output based on state
3. **Input Handler** processes keyboard events and updates state
4. **Test Framework** validates behavior through unit and integration tests

## Components and Interfaces

### 1. Selection State Management

Extract selection logic into testable helper functions that don't depend on terminal I/O.

#### State Data Structure

```bash
# Selection state (associative array)
declare -A SELECTION_STATE

# Initialize selection state with default selections
init_selection_state() {
  local -n agents_ref=$1
  local -n confidence_ref=$2
  local threshold=${3:-50}
  
  SELECTION_STATE=()
  
  for agent in "${agents_ref[@]}"; do
    local confidence="${confidence_ref[$agent]}"
    if [[ $confidence -ge $threshold ]]; then
      SELECTION_STATE[$agent]=1
    else
      SELECTION_STATE[$agent]=0
    fi
  done
}
```

#### Selection Operations

```bash
# Toggle agent selection
toggle_agent_selection() {
  local agent="$1"
  
  if [[ ${SELECTION_STATE[$agent]:-0} -eq 1 ]]; then
    SELECTION_STATE[$agent]=0
    return 1  # Now unselected
  else
    SELECTION_STATE[$agent]=1
    return 0  # Now selected
  fi
}

# Select all agents
select_all_agents() {
  local -n agents_ref=$1
  
  for agent in "${agents_ref[@]}"; do
    SELECTION_STATE[$agent]=1
  done
}

# Select none
select_none_agents() {
  local -n agents_ref=$1
  
  for agent in "${agents_ref[@]}"; do
    SELECTION_STATE[$agent]=0
  done
}

# Get selected agents
get_selected_agents() {
  local -a selected=()
  
  for agent in "${!SELECTION_STATE[@]}"; do
    if [[ ${SELECTION_STATE[$agent]} -eq 1 ]]; then
      selected+=("$agent")
    fi
  done
  
  printf '%s\n' "${selected[@]}"
}

# Get selection count
get_selection_count() {
  local count=0
  
  for agent in "${!SELECTION_STATE[@]}"; do
    if [[ ${SELECTION_STATE[$agent]} -eq 1 ]]; then
      ((count++))
    fi
  done
  
  echo "$count"
}
```

### 2. UI Rendering Functions

Separate rendering logic to enable testing output without terminal interaction.

#### Rendering Functions

```bash
# Render category header
render_category_header() {
  local category="$1"
  local count="$2"
  
  echo ""
  echo "  ${category} (${count} agents)"
  echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
}

# Render agent item
render_agent_item() {
  local agent="$1"
  local confidence="$2"
  local description="$3"
  local is_selected="$4"
  local is_current="$5"
  
  local checkbox="[ ]"
  [[ $is_selected -eq 1 ]] && checkbox="[✓]"
  
  local cursor="  "
  [[ $is_current -eq 1 ]] && cursor="→ "
  
  local confidence_bar=$(render_confidence_bar "$confidence")
  
  printf "%s%s %s %s %d%%\n" "$cursor" "$checkbox" "$agent" "$confidence_bar" "$confidence"
  printf "     %s\n" "$description"
}

# Render confidence bar
render_confidence_bar() {
  local confidence="$1"
  local bar_width=20
  local filled=$((confidence * bar_width / 100))
  local empty=$((bar_width - filled))
  
  printf "["
  printf '█%.0s' $(seq 1 $filled)
  printf '░%.0s' $(seq 1 $empty)
  printf "]"
}

# Render navigation footer
render_navigation_footer() {
  local selected_count="$1"
  local total_count="$2"
  
  echo ""
  echo "  ─────────────────────────────────────────────────────────────"
  echo "  Selected: ${selected_count}/${total_count}"
  echo "  Navigation: ↑/↓ to move, SPACE to toggle, ENTER to confirm"
  echo "  Commands: a=select all, n=select none, q=quit"
}

# Render complete agent list
render_agent_list() {
  local current_index="$1"
  local -n agents_ref=$2
  local -n confidence_ref=$3
  local -n descriptions_ref=$4
  local -n categories_ref=$5
  
  clear
  echo "┌─────────────────────────────────────────────────────────────┐"
  echo "│           Agent Recommendation - Interactive Mode            │"
  echo "└─────────────────────────────────────────────────────────────┘"
  
  local current_category=""
  local category_count=0
  local index=0
  
  for agent in "${agents_ref[@]}"; do
    local category="${categories_ref[$agent]}"
    
    # Render category header if changed
    if [[ "$category" != "$current_category" ]]; then
      [[ -n "$current_category" ]] && echo ""
      current_category="$category"
      
      # Count agents in category
      category_count=0
      for a in "${agents_ref[@]}"; do
        [[ "${categories_ref[$a]}" == "$category" ]] && ((category_count++))
      done
      
      render_category_header "$category" "$category_count"
    fi
    
    # Render agent item
    local is_current=0
    [[ $index -eq $current_index ]] && is_current=1
    
    render_agent_item \
      "$agent" \
      "${confidence_ref[$agent]}" \
      "${descriptions_ref[$agent]}" \
      "${SELECTION_STATE[$agent]}" \
      "$is_current"
    
    ((index++))
  done
  
  local selected_count=$(get_selection_count)
  render_navigation_footer "$selected_count" "${#agents_ref[@]}"
}
```

### 3. Input Handler

Process keyboard input and update state accordingly.

```bash
# Handle keyboard input
handle_keyboard_input() {
  local key="$1"
  local current_index="$2"
  local -n agents_ref=$3
  local max_index=$((${#agents_ref[@]} - 1))
  
  case "$key" in
    $'\x1b')  # Escape sequence (arrow keys)
      read -rsn2 -t 0.1 key
      case "$key" in
        '[A')  # Up arrow
          ((current_index > 0)) && ((current_index--))
          ;;
        '[B')  # Down arrow
          ((current_index < max_index)) && ((current_index++))
          ;;
      esac
      ;;
    ' ')  # Space - toggle selection
      local agent="${agents_ref[$current_index]}"
      toggle_agent_selection "$agent"
      ;;
    '')  # Enter - confirm
      return 0
      ;;
    'a')  # Select all
      select_all_agents agents_ref
      ;;
    'n')  # Select none
      select_none_agents agents_ref
      ;;
    'q')  # Quit
      exit 0
      ;;
  esac
  
  echo "$current_index"
}
```

### 4. Refactored Interactive Selection Function

```bash
# Main interactive selection function
interactive_selection() {
  local -n agents_ref=$1
  local -n confidence_ref=$2
  local -n descriptions_ref=$3
  local -n categories_ref=$4
  
  # Initialize state
  init_selection_state agents_ref confidence_ref 50
  
  local current_index=0
  
  # Main interaction loop
  while true; do
    # Render UI
    render_agent_list \
      "$current_index" \
      agents_ref \
      confidence_ref \
      descriptions_ref \
      categories_ref
    
    # Read input
    read -rsn1 key
    
    # Handle input and get new index
    current_index=$(handle_keyboard_input "$key" "$current_index" agents_ref)
    
    # Check if confirmed (Enter pressed)
    [[ $? -eq 0 ]] && break
  done
  
  # Return selected agents
  get_selected_agents
}
```

## Data Models

### Selection State

```bash
# Global selection state
declare -A SELECTION_STATE  # agent_name -> 0|1 (unselected|selected)

# Agent metadata (passed to functions)
declare -a agent_list       # Ordered list of agent names
declare -A agent_confidence # agent_name -> confidence_score (0-100)
declare -A agent_descriptions # agent_name -> description_text
declare -A agent_categories # agent_name -> category_name

# UI state
current_index=0  # Currently highlighted agent index
```

## Error Handling

### Terminal Compatibility

```bash
# Check terminal capabilities
check_terminal_capabilities() {
  # Check if terminal supports required features
  if [[ ! -t 0 ]] || [[ ! -t 1 ]]; then
    echo "Error: Interactive mode requires a terminal" >&2
    return 1
  fi
  
  # Check terminal size
  local rows cols
  read rows cols < <(stty size 2>/dev/null || echo "24 80")
  
  if [[ $rows -lt 20 ]] || [[ $cols -lt 60 ]]; then
    echo "Warning: Terminal size (${rows}x${cols}) may be too small for optimal display" >&2
    echo "Recommended minimum: 20 rows x 60 columns" >&2
  fi
  
  return 0
}
```

### Graceful Degradation

```bash
# Fallback to non-interactive mode
safe_interactive_selection() {
  if ! check_terminal_capabilities; then
    echo "Falling back to automatic selection (confidence >= 50%)" >&2
    
    for agent in "${!agent_confidence[@]}"; do
      if [[ ${agent_confidence[$agent]} -ge 50 ]]; then
        echo "$agent"
      fi
    done
    return 0
  fi
  
  interactive_selection agent_list agent_confidence agent_descriptions agent_categories
}
```

## Testing Strategy

### Unit Testing with bats

Test individual helper functions in isolation.

#### Test Structure

```bash
# tests/unit/test_selection_state.bats

setup() {
  # Source the script to get functions
  source scripts/recommend_agents.sh
  
  # Set up test data
  declare -g -a test_agents=("agent1" "agent2" "agent3")
  declare -g -A test_confidence=(
    ["agent1"]=75
    ["agent2"]=45
    ["agent3"]=90
  )
}

@test "init_selection_state selects agents above threshold" {
  init_selection_state test_agents test_confidence 50
  
  [[ ${SELECTION_STATE[agent1]} -eq 1 ]]
  [[ ${SELECTION_STATE[agent2]} -eq 0 ]]
  [[ ${SELECTION_STATE[agent3]} -eq 1 ]]
}

@test "toggle_agent_selection changes state" {
  SELECTION_STATE[agent1]=0
  
  toggle_agent_selection "agent1"
  [[ ${SELECTION_STATE[agent1]} -eq 1 ]]
  
  toggle_agent_selection "agent1"
  [[ ${SELECTION_STATE[agent1]} -eq 0 ]]
}

@test "select_all_agents selects all" {
  init_selection_state test_agents test_confidence 50
  select_all_agents test_agents
  
  [[ ${SELECTION_STATE[agent1]} -eq 1 ]]
  [[ ${SELECTION_STATE[agent2]} -eq 1 ]]
  [[ ${SELECTION_STATE[agent3]} -eq 1 ]]
}

@test "get_selection_count returns correct count" {
  SELECTION_STATE[agent1]=1
  SELECTION_STATE[agent2]=0
  SELECTION_STATE[agent3]=1
  
  count=$(get_selection_count)
  [[ $count -eq 2 ]]
}
```

### Rendering Tests

Test output formatting without terminal interaction.

```bash
# tests/unit/test_rendering.bats

@test "render_confidence_bar generates correct width" {
  bar=$(render_confidence_bar 50)
  
  # Should have 10 filled and 10 empty characters (20 total)
  [[ ${#bar} -eq 22 ]]  # 20 chars + 2 brackets
}

@test "render_agent_item formats correctly" {
  output=$(render_agent_item "test-agent" 75 "Test description" 1 0)
  
  [[ "$output" =~ \[✓\] ]]
  [[ "$output" =~ test-agent ]]
  [[ "$output" =~ 75% ]]
  [[ "$output" =~ "Test description" ]]
}

@test "render_category_header includes count" {
  output=$(render_category_header "Infrastructure" 5)
  
  [[ "$output" =~ Infrastructure ]]
  [[ "$output" =~ "5 agents" ]]
}
```

### Integration Tests with expect

Test complete interactive workflows using `expect` to simulate user input.

#### expect Test Script

```tcl
#!/usr/bin/expect -f
# tests/integration/test_interactive_navigation.exp

set timeout 5

# Start the script in interactive mode
spawn bash scripts/recommend_agents.sh --interactive

# Wait for interactive mode to load
expect "Interactive Mode"

# Test navigation down
send "\033\[B"
sleep 0.5

# Test navigation up
send "\033\[A"
sleep 0.5

# Test space to toggle
send " "
sleep 0.5

# Test select all
send "a"
sleep 0.5

# Test select none
send "n"
sleep 0.5

# Test confirm with enter
send "\r"

# Wait for completion
expect eof

# Check exit code
catch wait result
set exit_code [lindex $result 3]

if {$exit_code == 0} {
    puts "PASS: Interactive navigation test"
    exit 0
} else {
    puts "FAIL: Interactive navigation test (exit code: $exit_code)"
    exit 1
}
```

#### Bash Wrapper for expect Tests

```bash
# tests/integration/test_interactive.sh

#!/bin/bash

# Check if expect is available
if ! command -v expect &> /dev/null; then
  echo "SKIP: expect not installed"
  exit 0
fi

# Run expect tests
test_dir="$(dirname "$0")"
failed=0

for test_file in "$test_dir"/*.exp; do
  echo "Running $(basename "$test_file")..."
  
  if expect "$test_file"; then
    echo "✓ PASS"
  else
    echo "✗ FAIL"
    ((failed++))
  fi
done

exit $failed
```

### CI Integration

```bash
# tests/run_all_tests.sh

#!/bin/bash

set -e

echo "Running unit tests..."
bats tests/unit/*.bats

echo "Running integration tests..."
bash tests/integration/test_detection.sh

# Run interactive tests if expect is available
if command -v expect &> /dev/null; then
  echo "Running interactive tests..."
  bash tests/integration/test_interactive.sh
else
  echo "SKIP: Interactive tests (expect not installed)"
fi

echo "All tests passed!"
```

## Performance Considerations

### Rendering Optimization

```bash
# Cache rendered output to avoid redundant calculations
declare -A RENDER_CACHE

render_with_cache() {
  local cache_key="$1"
  shift
  local render_func="$1"
  shift
  
  if [[ -z "${RENDER_CACHE[$cache_key]}" ]]; then
    RENDER_CACHE[$cache_key]=$("$render_func" "$@")
  fi
  
  echo "${RENDER_CACHE[$cache_key]}"
}

# Clear cache when state changes
clear_render_cache() {
  RENDER_CACHE=()
}
```

### Input Debouncing

```bash
# Prevent rapid key repeat from causing issues
declare -g LAST_INPUT_TIME=0

debounce_input() {
  local current_time=$(date +%s%N)
  local elapsed=$((current_time - LAST_INPUT_TIME))
  local min_interval=50000000  # 50ms in nanoseconds
  
  if [[ $elapsed -lt $min_interval ]]; then
    return 1  # Too soon, ignore input
  fi
  
  LAST_INPUT_TIME=$current_time
  return 0
}
```

## Security Considerations

1. **Input Sanitization**
   - Validate all keyboard input
   - Prevent escape sequence injection
   - Limit input buffer size

2. **Terminal State Management**
   - Restore terminal settings on exit
   - Handle SIGINT/SIGTERM gracefully
   - Clean up on unexpected termination

```bash
# Trap signals to restore terminal
cleanup_terminal() {
  # Restore terminal settings
  stty sane
  
  # Show cursor
  tput cnorm
  
  # Clear screen
  clear
}

trap cleanup_terminal EXIT INT TERM
```

## Deployment and Rollout

### Backward Compatibility

- All existing interactive mode functionality remains unchanged
- New helper functions are internal implementation details
- No changes to command-line interface

### Testing Requirements

- All unit tests must pass before merge
- Integration tests must pass on Linux and macOS
- Interactive tests run in CI when expect is available
- Manual testing checklist for interactive mode

### Documentation Updates

- Add testing documentation to README
- Document how to run interactive tests locally
- Add troubleshooting guide for test failures
- Update contribution guidelines with testing requirements
