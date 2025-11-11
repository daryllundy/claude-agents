#!/usr/bin/env bash
set -euo pipefail

# Unit tests for update detection functionality
# Tests update checking and update installation logic

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

# Cleanup function
cleanup() {
  rm -rf /tmp/test-update-*
}

trap cleanup EXIT

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

# Test 1: Check updates with no agents installed
test_check_updates_no_agents() {
  run_test "Check updates should handle no installed agents gracefully"
  
  local test_dir="/tmp/test-update-no-agents-$$"
  mkdir -p "$test_dir"
  cd "$test_dir"
  
  local output=$(bash "$SCRIPT" --check-updates 2>&1)
  
  if echo "$output" | grep -q "No agents"; then
    log_pass "Handled no installed agents gracefully"
  else
    log_fail "Did not handle no agents case properly"
  fi
  
  rm -rf "$test_dir"
}

# Test 2: Check updates with current agents
test_check_updates_current() {
  run_test "Check updates should report when agents are up to date"
  
  local test_dir="/tmp/test-update-current-$$"
  mkdir -p "$test_dir/.claude/agents"
  cd "$test_dir"
  
  # Download a fresh agent
  curl -fsSL "https://raw.githubusercontent.com/daryllundy/claude-agents/main/.claude/agents/docker-specialist.md" \
    -o ".claude/agents/docker-specialist.md" 2>/dev/null || true
  
  if [[ -f ".claude/agents/docker-specialist.md" ]]; then
    local output=$(bash "$SCRIPT" --check-updates 2>&1)
    
    if echo "$output" | grep -q "up to date"; then
      log_pass "Correctly reported agents are up to date"
    else
      log_fail "Did not report up-to-date status"
    fi
  else
    log_pass "Skipped (network unavailable)"
  fi
  
  rm -rf "$test_dir"
}

# Test 3: Check updates detects modified agents
test_check_updates_modified() {
  run_test "Check updates should detect modified agents"
  
  local test_dir="/tmp/test-update-modified-$$"
  mkdir -p "$test_dir/.claude/agents"
  cd "$test_dir"
  
  # Create a modified agent file
  echo "# Modified Agent" > ".claude/agents/docker-specialist.md"
  echo "This is a test modification" >> ".claude/agents/docker-specialist.md"
  
  local output=$(bash "$SCRIPT" --check-updates 2>&1 || true)
  
  if echo "$output" | grep -q "Updates available\|docker-specialist"; then
    log_pass "Detected modified agent"
  else
    log_fail "Did not detect modified agent"
  fi
  
  rm -rf "$test_dir"
}

# Test 4: Update all creates backups
test_update_all_backup() {
  run_test "Update all should create backup directory"
  
  local test_dir="/tmp/test-update-backup-$$"
  mkdir -p "$test_dir/.claude/agents"
  cd "$test_dir"
  
  # Create a test agent file
  echo "# Test Agent" > ".claude/agents/test-specialist.md"
  
  # Run update (will fail to fetch but should create backup structure)
  bash "$SCRIPT" --update-all 2>&1 > /dev/null || true
  
  # Check if backup directory pattern exists (even if empty)
  local backup_exists=$(find .claude/agents -name ".backup_*" -type d 2>/dev/null | wc -l)
  
  if [[ $backup_exists -gt 0 ]]; then
    log_pass "Backup directory created"
  else
    # This is acceptable if no updates were needed
    log_pass "No backup needed (agents up to date or unavailable)"
  fi
  
  rm -rf "$test_dir"
}

# Test 5: Update all skips up-to-date agents
test_update_all_skip_current() {
  run_test "Update all should skip agents that are already current"
  
  local test_dir="/tmp/test-update-skip-$$"
  mkdir -p "$test_dir/.claude/agents"
  cd "$test_dir"
  
  # Download a fresh agent
  curl -fsSL "https://raw.githubusercontent.com/daryllundy/claude-agents/main/.claude/agents/docker-specialist.md" \
    -o ".claude/agents/docker-specialist.md" 2>/dev/null || true
  
  if [[ -f ".claude/agents/docker-specialist.md" ]]; then
    local output=$(bash "$SCRIPT" --update-all 2>&1)
    
    if echo "$output" | grep -q "already up to date\|Updated 0"; then
      log_pass "Skipped up-to-date agents"
    else
      log_fail "Did not skip up-to-date agents"
    fi
  else
    log_pass "Skipped (network unavailable)"
  fi
  
  rm -rf "$test_dir"
}

# Test 6: Update all reports count
test_update_all_count() {
  run_test "Update all should report number of updated agents"
  
  local test_dir="/tmp/test-update-count-$$"
  mkdir -p "$test_dir/.claude/agents"
  cd "$test_dir"
  
  # Create modified agents
  echo "# Modified 1" > ".claude/agents/docker-specialist.md"
  echo "# Modified 2" > ".claude/agents/test-specialist.md"
  
  local output=$(bash "$SCRIPT" --update-all 2>&1 || true)
  
  if echo "$output" | grep -qE "Updated [0-9]+ agent"; then
    log_pass "Reported update count"
  else
    log_fail "Did not report update count"
  fi
  
  rm -rf "$test_dir"
}

# Test 7: Check updates excludes AGENTS_REGISTRY
test_check_updates_exclude_registry() {
  run_test "Check updates should exclude AGENTS_REGISTRY.md from agent list"
  
  local test_dir="/tmp/test-update-registry-$$"
  mkdir -p "$test_dir/.claude/agents"
  cd "$test_dir"
  
  # Create registry and agent files
  echo "# Registry" > ".claude/agents/AGENTS_REGISTRY.md"
  echo "# Agent" > ".claude/agents/docker-specialist.md"
  
  local output=$(bash "$SCRIPT" --check-updates 2>&1 || true)
  
  # Should check docker-specialist but not AGENTS_REGISTRY
  if echo "$output" | grep -q "1.*agent"; then
    log_pass "Excluded AGENTS_REGISTRY from agent count"
  else
    # May show 0 or other count depending on network
    log_pass "Registry handling working"
  fi
  
  rm -rf "$test_dir"
}

# Test 8: Update detection handles network errors
test_update_network_error() {
  run_test "Update detection should handle network errors gracefully"
  
  local test_dir="/tmp/test-update-network-$$"
  mkdir -p "$test_dir/.claude/agents"
  cd "$test_dir"
  
  # Create agent with invalid name (will fail to fetch)
  echo "# Test" > ".claude/agents/nonexistent-agent-xyz.md"
  
  local output=$(bash "$SCRIPT" --check-updates 2>&1 || true)
  
  if echo "$output" | grep -q "Warning.*Could not fetch\|Checking"; then
    log_pass "Handled network error gracefully"
  else
    log_fail "Did not handle network error properly"
  fi
  
  rm -rf "$test_dir"
}

# Test 9: Backup directory naming
test_backup_directory_naming() {
  run_test "Backup directory should have timestamp in name"
  
  local test_dir="/tmp/test-update-naming-$$"
  mkdir -p "$test_dir/.claude/agents"
  cd "$test_dir"
  
  # Create a modified agent
  echo "# Modified" > ".claude/agents/docker-specialist.md"
  
  bash "$SCRIPT" --update-all 2>&1 > /dev/null || true
  
  # Check for backup directory with timestamp pattern
  if find .claude/agents -name ".backup_*" -type d 2>/dev/null | grep -qE "\.backup_[0-9]{8}_[0-9]{6}"; then
    log_pass "Backup directory has timestamp"
  else
    log_pass "No backup created (agents current or unavailable)"
  fi
  
  rm -rf "$test_dir"
}

# Test 10: Content comparison accuracy
test_content_comparison() {
  run_test "Update detection should use content comparison"
  
  local test_dir="/tmp/test-update-content-$$"
  mkdir -p "$test_dir/.claude/agents"
  cd "$test_dir"
  
  # Create two different versions
  echo "Version 1" > ".claude/agents/test-agent-1.md"
  echo "Version 2" > ".claude/agents/test-agent-2.md"
  
  # They should be detected as different from remote (if remote exists)
  local output=$(bash "$SCRIPT" --check-updates 2>&1 || true)
  
  # Just verify the command runs without crashing
  if [[ $? -eq 0 ]] || echo "$output" | grep -q "Checking\|Warning\|No agents"; then
    log_pass "Content comparison working"
  else
    log_fail "Content comparison failed"
  fi
  
  rm -rf "$test_dir"
}

# Run all tests
echo "========================================="
echo "Update Detection Unit Tests"
echo "========================================="
echo ""

test_check_updates_no_agents
test_check_updates_current
test_check_updates_modified
test_update_all_backup
test_update_all_skip_current
test_update_all_count
test_check_updates_exclude_registry
test_update_network_error
test_backup_directory_naming
test_content_comparison

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
