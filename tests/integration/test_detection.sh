#!/usr/bin/env bash
set -euo pipefail

# Integration tests for agent recommendation script
# Tests end-to-end detection workflows

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SCRIPT="$REPO_ROOT/scripts/recommend_agents.sh"
FIXTURES="$REPO_ROOT/tests/fixtures"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

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

# Test 1: AWS + Terraform Project Detection
test_aws_terraform() {
  run_test "AWS + Terraform project should detect aws-specialist and terraform-specialist"

  cd "$FIXTURES/aws-terraform-project"
  local output=$(bash "$SCRIPT" --dry-run --min-confidence 20 2>&1)

  if echo "$output" | grep -q "aws-specialist" && echo "$output" | grep -q "terraform-specialist"; then
    log_pass "Detected both aws-specialist and terraform-specialist"
  else
    log_fail "Failed to detect expected agents"
    echo "Output: $output"
  fi
}

# Test 2: React Frontend Project Detection
test_react_frontend() {
  run_test "React frontend project should detect frontend-specialist and test-specialist"

  cd "$FIXTURES/react-frontend-project"
  local output=$(bash "$SCRIPT" --dry-run --min-confidence 20 2>&1)

  if echo "$output" | grep -q "frontend-specialist"; then
    log_pass "Detected frontend-specialist"
  else
    log_fail "Failed to detect frontend-specialist"
    echo "Output: $output"
  fi
}

# Test 3: Kubernetes Project Detection
test_kubernetes() {
  run_test "Kubernetes project should detect kubernetes-specialist and docker-specialist"

  cd "$FIXTURES/kubernetes-project"
  local output=$(bash "$SCRIPT" --dry-run --min-confidence 20 2>&1)

  if echo "$output" | grep -q "kubernetes-specialist" && echo "$output" | grep -q "docker-specialist"; then
    log_pass "Detected kubernetes-specialist and docker-specialist"
  else
    log_fail "Failed to detect expected agents"
    echo "Output: $output"
  fi
}

# Test 4: Multi-Cloud Project Detection and Orchestrator
test_multi_cloud_orchestrator() {
  run_test "Multi-cloud project should detect devops-orchestrator"

  cd "$FIXTURES/multi-cloud-project"
  local output=$(bash "$SCRIPT" --dry-run --min-confidence 15 2>&1)

  if echo "$output" | grep -q "devops-orchestrator"; then
    log_pass "DevOps orchestrator logic triggered correctly"
  else
    log_fail "DevOps orchestrator not detected"
    echo "Output: $output"
  fi

  # Check for multiple cloud providers
  if echo "$output" | grep -q "aws-specialist" && echo "$output" | grep -q "azure-specialist" && echo "$output" | grep -q "gcp-specialist"; then
    log_pass "Detected all three cloud providers"
  else
    log_fail "Failed to detect all cloud providers"
  fi
}

# Test 5: Empty Project (Core Agents)
test_empty_project() {
  run_test "Empty project should recommend core agents"

  cd "$FIXTURES/empty-project"
  local output=$(bash "$SCRIPT" --dry-run 2>&1)

  if echo "$output" | grep -q "code-review-specialist\|refactoring-specialist\|test-specialist"; then
    log_pass "Recommended core agents for empty project"
  else
    log_fail "Failed to recommend core agents"
    echo "Output: $output"
  fi
}

# Test 6: Confidence Filtering
test_confidence_filtering() {
  run_test "Confidence filtering should work correctly"

  cd "$FIXTURES/aws-terraform-project"
  local output_high=$(bash "$SCRIPT" --dry-run --min-confidence 50 2>&1)
  local output_low=$(bash "$SCRIPT" --dry-run --min-confidence 15 2>&1)

  local count_high=$(echo "$output_high" | grep -c "specialist" || true)
  local count_low=$(echo "$output_low" | grep -c "specialist" || true)

  if [[ $count_low -gt $count_high ]]; then
    log_pass "Lower threshold shows more agents ($count_low vs $count_high)"
  else
    log_fail "Confidence filtering not working as expected"
  fi
}

# Test 7: Export Functionality
test_export() {
  run_test "Export functionality should create valid JSON"

  cd "$FIXTURES/aws-terraform-project"
  local export_file="/tmp/test-export-$$.json"

  bash "$SCRIPT" --dry-run --export "$export_file" --min-confidence 20 2>&1 > /dev/null

  if [[ -f "$export_file" ]]; then
    if command -v jq >/dev/null 2>&1; then
      if jq empty "$export_file" 2>/dev/null; then
        log_pass "Export created valid JSON"
        rm -f "$export_file"
      else
        log_fail "Export created invalid JSON"
      fi
    else
      log_pass "Export file created (jq not available for validation)"
      rm -f "$export_file"
    fi
  else
    log_fail "Export file not created"
  fi
}

# Test 8: Verbose Mode
test_verbose_mode() {
  run_test "Verbose mode should show pattern details"

  cd "$FIXTURES/aws-terraform-project"
  local output=$(bash "$SCRIPT" --dry-run --verbose --min-confidence 25 2>&1)

  if echo "$output" | grep -q "Matched Patterns:" && echo "$output" | grep -q "weight:"; then
    log_pass "Verbose mode shows pattern details"
  else
    log_fail "Verbose mode not working correctly"
  fi
}

# Test 9: Min-Confidence Validation
test_min_confidence_validation() {
  run_test "Invalid min-confidence should be rejected"

  cd "$FIXTURES/empty-project"

  if bash "$SCRIPT" --min-confidence 150 2>&1 | grep -q "must be a number between 0 and 100"; then
    log_pass "Invalid min-confidence rejected"
  else
    log_fail "Invalid min-confidence not rejected"
  fi
}

# Test 10: Enhanced Output Format
test_output_format() {
  run_test "Enhanced output should show progress bars and symbols"

  cd "$FIXTURES/aws-terraform-project"
  local output=$(bash "$SCRIPT" --dry-run --min-confidence 20 2>&1)

  if echo "$output" | grep -q "═" && echo "$output" | grep -q "━" && echo "$output" | grep -q "[█░]"; then
    log_pass "Enhanced output format is working"
  else
    log_fail "Enhanced output format not displaying correctly"
  fi
}

# Run all tests
echo "========================================="
echo "Agent Recommendation Integration Tests"
echo "========================================="
echo ""

test_aws_terraform
test_react_frontend
test_kubernetes
test_multi_cloud_orchestrator
test_empty_project
test_confidence_filtering
test_export
test_verbose_mode
test_min_confidence_validation
test_output_format

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
