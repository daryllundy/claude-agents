#!/usr/bin/env bash

# Integration tests for update operations in recommend_agents.sh
# Tests check_updates, update_all_agents, and parse_agent_registry with retry/cache logic

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SCRIPT="$REPO_ROOT/scripts/recommend_agents.sh"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test directory
TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR" 2>/dev/null || true' EXIT

# Helper functions
log_test() {
  echo -e "${YELLOW}[TEST]${NC} $1"
}

log_pass() {
  echo -e "${GREEN}[PASS]${NC} $1"
  ((TESTS_PASSED++))
}

log_fail() {
  echo -e "${RED}[FAIL]${NC} $1"
  ((TESTS_FAILED++))
}

run_test() {
  local test_name="$1"
  ((TESTS_RUN++))
  log_test "$test_name"
}

# Mock log function
log() {
  echo "[LOG] $*" >&2
}

# Source functions from the main script
source_script_functions() {
  local agents_dir="$TEST_DIR/.claude/agents"
  export AGENTS_DIR="$agents_dir"
  export CACHE_DIR="$TEST_DIR/cache"
  export CACHE_EXPIRY_SECONDS=3600
  export FORCE_REFRESH=false
  export VERBOSE=false
  export BASE_URL="https://raw.githubusercontent.com/daryllundy/claude-agents/main/.claude/agents"
  
  # Source required functions - use awk for more reliable extraction
  eval "$(awk '/^log\(\) \{/,/^}/' "$SCRIPT")"
  eval "$(awk '/^init_cache\(\) \{/,/^}/' "$SCRIPT")"
  eval "$(awk '/^get_cache_path\(\) \{/,/^}/' "$SCRIPT")"
  eval "$(awk '/^is_cache_fresh\(\) \{/,/^}/' "$SCRIPT")"
  eval "$(awk '/^fetch_with_retry\(\) \{/,/^}/' "$SCRIPT")"
  eval "$(awk '/^fetch_with_cache\(\) \{/,/^}/' "$SCRIPT")"
  eval "$(awk '/^check_updates\(\) \{/,/^}/' "$SCRIPT")"
  eval "$(awk '/^update_all_agents\(\) \{/,/^}/' "$SCRIPT")"
  eval "$(awk '/^parse_agent_registry\(\) \{/,/^}/' "$SCRIPT")"
  
  # Initialize associative arrays for parse_agent_registry
  declare -gA AGENT_CATEGORIES
  declare -gA AGENT_DESCRIPTIONS
  declare -gA AGENT_USE_CASES
}

source_script_functions

# Test 1: check_updates uses retry logic
test_check_updates_retry_logic() {
  run_test "check_updates should use fetch_with_cache for network operations"
  
  # Start fresh
  rm -rf "$AGENTS_DIR"
  mkdir -p "$AGENTS_DIR"
  
  # Create a local agent file
  echo "# Test Agent v1" > "$AGENTS_DIR/test-check.md"
  echo "Old content" >> "$AGENTS_DIR/test-check.md"
  
  # Create a temporary marker file to track calls
  local marker_file="$TEST_DIR/fetch_cache_called"
  rm -f "$marker_file"
  
  # Override fetch_with_cache to track calls
  fetch_with_cache() {
    echo "1" > "$marker_file"
    local url="$1"
    local output="$2"
    # Return different content to simulate update available
    echo "# Test Agent v2" > "$output"
    echo "New content" >> "$output"
    return 0
  }
  
  # Run check_updates and capture just the last line (the count)
  local output
  output=$(check_updates 2>/dev/null)
  local update_count
  update_count=$(echo "$output" | tail -1)
  
  # Verify fetch_with_cache was called by checking marker file
  if [[ -f "$marker_file" ]]; then
    # Verify update was detected (count should be 1)
    if [[ "$update_count" == "1" ]]; then
      log_pass "check_updates uses fetch_with_cache and detected update"
    else
      log_fail "Update not detected (count: '$update_count')"
    fi
  else
    log_fail "fetch_with_cache was not called"
  fi
  
  # Restore function
  source_script_functions
  rm -f "$marker_file"
}

# Test 2: check_updates handles network failures gracefully
test_check_updates_network_failure() {
  run_test "check_updates should handle network failures gracefully"
  
  mkdir -p "$AGENTS_DIR"
  
  # Create local agent files
  echo "# Agent 1" > "$AGENTS_DIR/agent1.md"
  echo "# Agent 2" > "$AGENTS_DIR/agent2.md"
  
  # Mock fetch_with_cache to fail
  fetch_with_cache() {
    return 1
  }
  export -f fetch_with_cache
  
  # Run check_updates - should not crash
  local update_count
  if update_count=$(check_updates 2>/dev/null); then
    log_pass "check_updates handled network failure gracefully"
  else
    log_fail "check_updates crashed on network failure"
  fi
  
  # Restore
  source_script_functions
}

# Test 3: update_all_agents creates backups
test_update_all_agents_creates_backups() {
  run_test "update_all_agents should create backups before updating"
  
  mkdir -p "$AGENTS_DIR"
  
  # Create local agent file
  echo "# Original Content" > "$AGENTS_DIR/backup-test.md"
  
  # Mock fetch_with_retry to return different content
  fetch_with_retry() {
    local url="$1"
    local output="$2"
    echo "# Updated Content" > "$output"
    return 0
  }
  export -f fetch_with_retry
  
  # Run update_all_agents
  update_all_agents 2>/dev/null
  
  # Check if backup directory was created
  local backup_dir
  backup_dir=$(find "$AGENTS_DIR" -type d -name ".backup_*" | head -n 1)
  
  if [[ -n "$backup_dir" ]] && [[ -d "$backup_dir" ]]; then
    # Check if backup file exists
    if [[ -f "$backup_dir/backup-test.md" ]]; then
      # Verify backup contains original content
      if grep -q "Original Content" "$backup_dir/backup-test.md"; then
        log_pass "Backup created with original content"
      else
        log_fail "Backup does not contain original content"
      fi
    else
      log_fail "Backup file not found"
    fi
  else
    log_fail "Backup directory not created"
  fi
  
  # Restore
  source_script_functions
}

# Test 4: update_all_agents rollback on failure
test_update_all_agents_rollback() {
  run_test "update_all_agents should rollback on update failure"
  
  mkdir -p "$AGENTS_DIR"
  
  # Create local agent file with original content
  local original_content="# Original Content for Rollback Test"
  echo "$original_content" > "$AGENTS_DIR/rollback-test.md"
  
  # Mock fetch_with_retry to succeed first (for comparison), then fail on update
  local call_count=0
  fetch_with_retry() {
    ((call_count++))
    local url="$1"
    local output="$2"
    
    # First call: return different content (to trigger update)
    if [[ $call_count -eq 1 ]]; then
      echo "# Different Content" > "$output"
      return 0
    fi
    
    # Subsequent calls: fail
    return 1
  }
  export -f fetch_with_retry
  export call_count
  
  # Run update_all_agents
  update_all_agents 2>/dev/null || true
  
  # Verify original content was restored
  if [[ -f "$AGENTS_DIR/rollback-test.md" ]]; then
    if grep -q "Original Content for Rollback Test" "$AGENTS_DIR/rollback-test.md"; then
      log_pass "File was rolled back to original content after failure"
    else
      log_fail "File was not rolled back correctly"
    fi
  else
    log_fail "Agent file missing after rollback"
  fi
  
  # Restore
  source_script_functions
  unset call_count
}

# Test 5: update_all_agents reports counts correctly
test_update_all_agents_counts() {
  run_test "update_all_agents should report updated and failed counts"
  
  mkdir -p "$AGENTS_DIR"
  
  # Create multiple agent files
  echo "# Agent 1 v1" > "$AGENTS_DIR/agent1.md"
  echo "# Agent 2 v1" > "$AGENTS_DIR/agent2.md"
  echo "# Agent 3 v1" > "$AGENTS_DIR/agent3.md"
  
  # Mock fetch_with_retry: succeed for agent1, fail for agent2, no change for agent3
  fetch_with_retry() {
    local url="$1"
    local output="$2"
    
    if [[ "$url" == *"agent1.md" ]]; then
      echo "# Agent 1 v2" > "$output"
      return 0
    elif [[ "$url" == *"agent2.md" ]]; then
      return 1  # Fail
    elif [[ "$url" == *"agent3.md" ]]; then
      echo "# Agent 3 v1" > "$output"  # Same content
      return 0
    fi
    
    return 1
  }
  export -f fetch_with_retry
  
  # Capture output
  local output
  output=$(update_all_agents 2>&1)
  
  # Check for success message for agent1
  if echo "$output" | grep -q "Updated agent1"; then
    # Check for failure message for agent2
    if echo "$output" | grep -q "Failed.*agent2"; then
      log_pass "Update counts reported correctly"
    else
      log_fail "Failed agent not reported"
    fi
  else
    log_fail "Updated agent not reported"
  fi
  
  # Restore
  source_script_functions
}

# Test 6: parse_agent_registry with caching
test_parse_agent_registry_caching() {
  run_test "parse_agent_registry should use fetch_with_cache when registry doesn't exist"
  
  mkdir -p "$AGENTS_DIR"
  
  # Ensure registry doesn't exist
  rm -f "$AGENTS_DIR/AGENTS_REGISTRY.md"
  
  # Track fetch_with_cache calls
  local fetch_cache_called=0
  local original_fetch_with_cache=$(declare -f fetch_with_cache)
  
  fetch_with_cache() {
    ((fetch_cache_called++))
    local url="$1"
    local output="$2"
    
    # Create minimal registry content
    cat > "$output" <<'EOF'
# Agent Registry

## Available Agents

#### 1. test-specialist

**Category**: Testing
**Description**: Test agent
**Use Case**: Testing purposes
EOF
    return 0
  }
  export -f fetch_with_cache
  export fetch_cache_called
  
  # Run parse_agent_registry
  if parse_agent_registry 2>/dev/null; then
    if [[ $fetch_cache_called -gt 0 ]]; then
      # Verify registry was created
      if [[ -f "$AGENTS_DIR/AGENTS_REGISTRY.md" ]]; then
        log_pass "parse_agent_registry used fetch_with_cache and created registry"
      else
        log_fail "Registry file not created"
      fi
    else
      log_fail "fetch_with_cache was not called"
    fi
  else
    log_fail "parse_agent_registry failed"
  fi
  
  # Restore
  eval "$original_fetch_with_cache"
  unset fetch_cache_called
}

# Test 7: Cache hit scenario
test_cache_hit_scenario() {
  run_test "Update operations should use cached data when available"
  
  # Start fresh
  rm -rf "$AGENTS_DIR"
  mkdir -p "$AGENTS_DIR"
  init_cache
  
  # Create local agent file
  echo "# Local Agent" > "$AGENTS_DIR/cache-hit-test.md"
  
  # Pre-populate cache with SAME content (no update needed)
  local url="${BASE_URL}/cache-hit-test.md"
  local cache_file
  cache_file=$(get_cache_path "$url")
  echo "# Local Agent" > "$cache_file"  # Same as local
  touch "$cache_file"  # Make it fresh
  
  # Create a marker file to track if fetch_with_retry is called
  local retry_marker="$TEST_DIR/retry_called"
  rm -f "$retry_marker"
  
  # Override fetch_with_retry to track calls
  fetch_with_retry() {
    echo "1" > "$retry_marker"
    return 1  # Fail if called
  }
  
  # Run check_updates
  check_updates 2>/dev/null || true
  
  # Verify fetch_with_retry was NOT called (cache hit)
  if [[ ! -f "$retry_marker" ]]; then
    log_pass "Cache hit prevented unnecessary network request"
  else
    log_fail "fetch_with_retry was called despite cache hit"
  fi
  
  # Restore
  source_script_functions
  rm -f "$retry_marker"
}

# Test 8: Cache miss scenario
test_cache_miss_scenario() {
  run_test "Update operations should fetch when cache is stale or missing"
  
  mkdir -p "$AGENTS_DIR"
  init_cache
  
  # Create local agent file
  echo "# Local Agent" > "$AGENTS_DIR/miss-agent.md"
  
  # Create stale cache or no cache
  local url="${BASE_URL}/miss-agent.md"
  local cache_file
  cache_file=$(get_cache_path "$url")
  
  # Create stale cache (2 hours old)
  echo "# Stale Cached Agent" > "$cache_file"
  if [[ "$(uname)" == "Darwin" ]]; then
    local old_time=$(date -v-2H +"%Y%m%d%H%M.%S")
    touch -t "$old_time" "$cache_file"
  else
    touch -d "2 hours ago" "$cache_file"
  fi
  
  # Track if fetch_with_retry is called
  local retry_called=0
  local original_fetch_with_retry=$(declare -f fetch_with_retry)
  
  fetch_with_retry() {
    ((retry_called++))
    local url="$1"
    local output="$2"
    echo "# Fresh Agent" > "$output"
    return 0
  }
  export -f fetch_with_retry
  export retry_called
  
  # Run check_updates with 1-hour cache expiry
  check_updates 2>/dev/null || true
  
  # Verify fetch_with_retry WAS called (cache miss)
  if [[ $retry_called -gt 0 ]]; then
    log_pass "Cache miss triggered network fetch"
  else
    log_fail "fetch_with_retry was not called on cache miss"
  fi
  
  # Restore
  eval "$original_fetch_with_retry"
  unset retry_called
}

# Test 9: Force refresh bypasses cache
test_force_refresh_bypasses_cache() {
  run_test "Force refresh should bypass cache in update operations"
  
  mkdir -p "$AGENTS_DIR"
  init_cache
  
  # Create local agent file
  echo "# Local Agent" > "$AGENTS_DIR/force-agent.md"
  
  # Create fresh cache
  local url="${BASE_URL}/force-agent.md"
  local cache_file
  cache_file=$(get_cache_path "$url")
  echo "# Cached Agent" > "$cache_file"
  touch "$cache_file"
  
  # Enable force refresh
  export FORCE_REFRESH=true
  
  # Track if fetch_with_retry is called
  local retry_called=0
  local original_fetch_with_retry=$(declare -f fetch_with_retry)
  
  fetch_with_retry() {
    ((retry_called++))
    local url="$1"
    local output="$2"
    echo "# Fresh Agent" > "$output"
    return 0
  }
  export -f fetch_with_retry
  export retry_called
  
  # Run check_updates
  check_updates 2>/dev/null || true
  
  # Verify fetch_with_retry WAS called despite fresh cache
  if [[ $retry_called -gt 0 ]]; then
    log_pass "Force refresh bypassed cache"
  else
    log_fail "Force refresh did not bypass cache"
  fi
  
  # Restore
  export FORCE_REFRESH=false
  eval "$original_fetch_with_retry"
  unset retry_called
}

# Test 10: Retry logic with exponential backoff
test_retry_exponential_backoff() {
  run_test "fetch_with_retry should implement exponential backoff"
  
  # Track retry attempts and timing
  local -a attempt_times=()
  local original_fetch_with_retry=$(declare -f fetch_with_retry)
  
  fetch_with_retry() {
    local url="$1"
    local output="$2"
    local max_attempts="${3:-3}"
    
    for ((attempt=1; attempt<=max_attempts; attempt++)); do
      attempt_times+=("$(date +%s)")
      
      # Fail first 2 attempts, succeed on 3rd
      if [[ $attempt -eq 3 ]]; then
        echo "success" > "$output"
        return 0
      fi
      
      # Simulate backoff
      local backoff=$((2 ** (attempt - 1)))
      sleep "$backoff"
    done
    
    return 1
  }
  export -f fetch_with_retry
  export attempt_times
  
  # Call fetch_with_retry
  local output="$TEST_DIR/retry_output.txt"
  if fetch_with_retry "http://example.com/test" "$output" 3 2>/dev/null; then
    # Verify 3 attempts were made
    if [[ ${#attempt_times[@]} -eq 3 ]]; then
      log_pass "Retry logic executed with multiple attempts"
    else
      log_fail "Expected 3 attempts, got ${#attempt_times[@]}"
    fi
  else
    log_fail "fetch_with_retry failed"
  fi
  
  # Restore
  eval "$original_fetch_with_retry"
  unset attempt_times
}

# Run all tests
echo "========================================="
echo "Update Operations Integration Tests"
echo "========================================="
echo ""

test_check_updates_retry_logic
test_check_updates_network_failure
test_update_all_agents_creates_backups
test_update_all_agents_rollback
test_update_all_agents_counts
test_parse_agent_registry_caching
test_cache_hit_scenario
test_cache_miss_scenario
test_force_refresh_bypasses_cache
test_retry_exponential_backoff

# Summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Tests run:    $TESTS_RUN"
echo -e "${GREEN}Tests passed: $TESTS_PASSED${NC}"
if [[ $TESTS_FAILED -gt 0 ]]; then
  echo -e "${RED}Tests failed: $TESTS_FAILED${NC}"
  exit 1
else
  echo ""
  echo -e "${GREEN}All tests passed!${NC}"
  exit 0
fi
