#!/usr/bin/env bash
set -euo pipefail

# Unit tests for confidence scoring calculation
# Tests the calculate_confidence function with various pattern combinations

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
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

# Test 1: Zero confidence for no matches
test_zero_confidence() {
  run_test "Empty project should have zero confidence for specialized agents"
  
  cd "$FIXTURES/empty-project"
  local output=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run --min-confidence 0 2>&1)
  
  # Empty project should not detect aws-specialist
  if echo "$output" | grep -q "aws-specialist"; then
    log_fail "aws-specialist detected in empty project"
  else
    log_pass "No false positives in empty project"
  fi
}

# Test 2: High confidence for strong matches
test_high_confidence() {
  run_test "AWS + Terraform project should have high confidence for both specialists"
  
  cd "$FIXTURES/aws-terraform-project"
  local output=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run --verbose 2>&1)
  
  # Check for high confidence (should be > 50%)
  local aws_confidence=$(echo "$output" | grep "aws-specialist" | grep -oP '\d+%' | head -1 | tr -d '%')
  local tf_confidence=$(echo "$output" | grep "terraform-specialist" | grep -oP '\d+%' | head -1 | tr -d '%')
  
  if [[ -n "$aws_confidence" ]] && [[ $aws_confidence -ge 50 ]]; then
    log_pass "aws-specialist has high confidence ($aws_confidence%)"
  else
    log_fail "aws-specialist confidence too low (${aws_confidence:-0}%)"
  fi
  
  if [[ -n "$tf_confidence" ]] && [[ $tf_confidence -ge 50 ]]; then
    log_pass "terraform-specialist has high confidence ($tf_confidence%)"
  else
    log_fail "terraform-specialist confidence too low (${tf_confidence:-0}%)"
  fi
}

# Test 3: Confidence sorting
test_confidence_sorting() {
  run_test "Agents should be sorted by confidence (descending)"
  
  cd "$FIXTURES/multi-cloud-project"
  local output=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run --min-confidence 15 2>&1)
  
  # Extract confidence scores in order
  local -a confidences
  while IFS= read -r line; do
    if [[ $line =~ ([0-9]+)% ]]; then
      confidences+=("${BASH_REMATCH[1]}")
    fi
  done <<< "$(echo "$output" | grep -E "specialist.*[0-9]+%")"
  
  # Check if sorted in descending order
  local sorted=true
  for ((i=0; i<${#confidences[@]}-1; i++)); do
    if [[ ${confidences[i]} -lt ${confidences[i+1]} ]]; then
      sorted=false
      break
    fi
  done
  
  if [[ $sorted == true ]] && [[ ${#confidences[@]} -gt 1 ]]; then
    log_pass "Agents sorted by confidence (descending)"
  else
    log_fail "Agents not properly sorted by confidence"
  fi
}

# Test 4: Confidence threshold filtering
test_confidence_threshold() {
  run_test "Confidence threshold should filter agents correctly"
  
  cd "$FIXTURES/aws-terraform-project"
  
  # Get count with low threshold
  local count_low=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run --min-confidence 15 2>&1 | grep -c "specialist" || true)
  
  # Get count with high threshold
  local count_high=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run --min-confidence 60 2>&1 | grep -c "specialist" || true)
  
  if [[ $count_low -gt $count_high ]]; then
    log_pass "Higher threshold filters more agents ($count_low agents at 15% vs $count_high at 60%)"
  else
    log_fail "Threshold filtering not working correctly"
  fi
}

# Test 5: Multiple pattern accumulation
test_pattern_accumulation() {
  run_test "Multiple matching patterns should accumulate confidence"
  
  cd "$FIXTURES/kubernetes-project"
  local output=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run --verbose 2>&1)
  
  # kubernetes-specialist should match multiple patterns (k8s/, Chart.yaml, Dockerfile)
  local k8s_section=$(echo "$output" | sed -n '/Agent: kubernetes-specialist/,/^$/p')
  local matched_count=$(echo "$k8s_section" | grep -c "✓" || true)
  
  if [[ $matched_count -ge 2 ]]; then
    log_pass "Multiple patterns matched for kubernetes-specialist ($matched_count patterns)"
  else
    log_fail "Pattern accumulation not working ($matched_count patterns)"
  fi
}

# Test 6: Confidence capping at 100%
test_confidence_cap() {
  run_test "Confidence should be capped at 100%"
  
  cd "$FIXTURES/multi-cloud-project"
  local output=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run 2>&1)
  
  # Extract all confidence percentages
  local max_confidence=0
  while IFS= read -r line; do
    if [[ $line =~ ([0-9]+)% ]]; then
      local conf="${BASH_REMATCH[1]}"
      if [[ $conf -gt $max_confidence ]]; then
        max_confidence=$conf
      fi
    fi
  done <<< "$(echo "$output" | grep -E "specialist.*[0-9]+%")"
  
  if [[ $max_confidence -le 100 ]]; then
    log_pass "Confidence properly capped at 100% (max found: $max_confidence%)"
  else
    log_fail "Confidence exceeded 100% (found: $max_confidence%)"
  fi
}

# Test 7: DevOps orchestrator boost logic
test_devops_orchestrator_boost() {
  run_test "DevOps orchestrator should get confidence boost with multiple infrastructure components"
  
  cd "$FIXTURES/multi-cloud-project"
  local output=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run --min-confidence 15 2>&1)
  
  # Should detect devops-orchestrator due to multiple cloud providers + terraform + monitoring
  if echo "$output" | grep -q "devops-orchestrator"; then
    log_pass "DevOps orchestrator detected with infrastructure complexity"
  else
    log_fail "DevOps orchestrator not detected despite infrastructure complexity"
  fi
}

# Test 8: Recommended vs Suggested categorization
test_recommendation_tiers() {
  run_test "Agents should be categorized as Recommended (50%+) or Suggested (25-49%)"
  
  cd "$FIXTURES/aws-terraform-project"
  local output=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run 2>&1)
  
  # Check for recommendation symbols
  local has_recommended=$(echo "$output" | grep -c "✓" || true)
  local has_suggested=$(echo "$output" | grep -c "~" || true)
  
  if [[ $has_recommended -gt 0 ]]; then
    log_pass "Found recommended agents (✓ symbol)"
  else
    log_fail "No recommended agents found"
  fi
  
  # Suggested agents may or may not be present, so we just check the logic works
  if [[ $has_recommended -gt 0 ]] || [[ $has_suggested -gt 0 ]]; then
    log_pass "Recommendation tier system working"
  else
    log_fail "No tier symbols found"
  fi
}

# Test 9: Pattern weight contribution
test_pattern_weights() {
  run_test "Higher weight patterns should contribute more to confidence"
  
  cd "$FIXTURES/aws-terraform-project"
  local output=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run --verbose 2>&1)
  
  # Check that weights are displayed in verbose mode
  if echo "$output" | grep -q "weight:"; then
    log_pass "Pattern weights displayed in verbose mode"
  else
    log_fail "Pattern weights not displayed"
  fi
}

# Test 10: Confidence calculation consistency
test_confidence_consistency() {
  run_test "Running detection twice should produce consistent results"
  
  cd "$FIXTURES/kubernetes-project"
  
  local output1=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run 2>&1)
  local output2=$(bash "$REPO_ROOT/scripts/recommend_agents.sh" --dry-run 2>&1)
  
  # Extract agent lists
  local agents1=$(echo "$output1" | grep "specialist" | sort)
  local agents2=$(echo "$output2" | grep "specialist" | sort)
  
  if [[ "$agents1" == "$agents2" ]]; then
    log_pass "Detection results are consistent across runs"
  else
    log_fail "Detection results inconsistent"
  fi
}

# Run all tests
echo "========================================="
echo "Confidence Scoring Unit Tests"
echo "========================================="
echo ""

test_zero_confidence
test_high_confidence
test_confidence_sorting
test_confidence_threshold
test_pattern_accumulation
test_confidence_cap
test_devops_orchestrator_boost
test_recommendation_tiers
test_pattern_weights
test_confidence_consistency

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
