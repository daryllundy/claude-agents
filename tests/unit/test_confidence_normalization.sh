#!/usr/bin/env bash
# Unit tests for normalized confidence calculation

set -o pipefail

# Define the functions we're testing

# Mock detection functions for testing
has_file() { [[ "$1" == "*.matched" ]]; }
has_path() { [[ "$1" == "matched_dir" ]]; }
search_contents() { [[ "$1" == "matched_content" ]]; }

# Calculate maximum possible weight for an agent
calculate_max_possible_weight() {
  local agent="$1"
  local max_weight=0
  
  local patterns="${AGENT_PATTERNS[$agent]}"
  
  while IFS= read -r pattern_line; do
    [[ -z "$pattern_line" ]] && continue
    
    pattern_line=$(echo "$pattern_line" | xargs)
    [[ -z "$pattern_line" ]] && continue
    
    local rest="${pattern_line#*:}"
    local weight="${rest##*:}"
    
    if [[ "$weight" =~ ^[0-9]+$ ]]; then
      max_weight=$((max_weight + weight))
    fi
  done <<< "$patterns"
  
  echo "$max_weight"
}

# Simplified confidence calculation for testing
calculate_confidence_test() {
  local agent="$1"
  local accumulated_weight=0
  
  local patterns="${AGENT_PATTERNS[$agent]}"
  
  if [[ -z "$patterns" ]]; then
    echo "0"
    return 0
  fi
  
  local max_possible_weight
  max_possible_weight=$(calculate_max_possible_weight "$agent")
  
  while IFS= read -r pattern_line; do
    [[ -z "$pattern_line" ]] && continue
    
    pattern_line=$(echo "$pattern_line" | xargs)
    [[ -z "$pattern_line" ]] && continue
    
    local type="${pattern_line%%:*}"
    local rest="${pattern_line#*:}"
    local weight="${rest##*:}"
    local pattern="${rest%:*}"
    
    [[ -z "$type" || -z "$pattern" || -z "$weight" ]] && continue
    [[ ! "$weight" =~ ^[0-9]+$ ]] && continue
    
    case "$type" in
      file)
        has_file "$pattern" && accumulated_weight=$((accumulated_weight + weight))
        ;;
      path)
        has_path "$pattern" && accumulated_weight=$((accumulated_weight + weight))
        ;;
      content)
        search_contents "$pattern" && accumulated_weight=$((accumulated_weight + weight))
        ;;
    esac
  done <<< "$patterns"
  
  local confidence=0
  if [[ $max_possible_weight -gt 0 ]]; then
    confidence=$((accumulated_weight * 100 / max_possible_weight))
    [[ $confidence -gt 100 ]] && confidence=100
  fi
  
  echo "$confidence"
}

# Test counter
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
assert_equals() {
  local expected="$1"
  local actual="$2"
  local test_name="$3"
  
  TESTS_RUN=$((TESTS_RUN + 1))
  
  if [[ "$expected" == "$actual" ]]; then
    echo "✓ PASS: $test_name"
    TESTS_PASSED=$((TESTS_PASSED + 1))
  else
    echo "✗ FAIL: $test_name"
    echo "  Expected: $expected"
    echo "  Actual:   $actual"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

declare -A AGENT_PATTERNS

echo "========================================"
echo "Confidence Normalization Tests"
echo "========================================"
echo ""

# Test 1: calculate_max_possible_weight with multiple patterns
echo "Test Suite: calculate_max_possible_weight"
echo "----------------------------------------"

AGENT_PATTERNS[test-agent]="
file:*.matched:20
path:matched_dir:15
content:matched_content:10
"

max_weight=$(calculate_max_possible_weight "test-agent")
assert_equals "45" "$max_weight" "calculate_max_possible_weight sums all weights"

# Test 2: Empty pattern string
AGENT_PATTERNS[empty-agent]=""
max_weight=$(calculate_max_possible_weight "empty-agent")
assert_equals "0" "$max_weight" "calculate_max_possible_weight handles empty patterns"

# Test 3: Single pattern
AGENT_PATTERNS[single-agent]="file:*.test:25"
max_weight=$(calculate_max_possible_weight "single-agent")
assert_equals "25" "$max_weight" "calculate_max_possible_weight handles single pattern"

echo ""

# Test 4: Confidence with all patterns matched
echo "Test Suite: calculate_confidence"
echo "----------------------------------------"

AGENT_PATTERNS[all-match]="
file:*.matched:20
path:matched_dir:15
content:matched_content:10
"

confidence=$(calculate_confidence_test "all-match")
assert_equals "100" "$confidence" "100% confidence when all patterns match"

# Test 5: Partial match
AGENT_PATTERNS[partial-match]="
file:*.matched:20
path:unmatched_dir:15
content:matched_content:10
"

confidence=$(calculate_confidence_test "partial-match")
# (20+10) / (20+15+10) * 100 = 66.666... = 66
assert_equals "66" "$confidence" "Correct confidence for partial match"

# Test 6: No matches
AGENT_PATTERNS[no-match]="
file:*.unmatched:20
path:unmatched_dir:15
content:unmatched_content:10
"

confidence=$(calculate_confidence_test "no-match")
assert_equals "0" "$confidence" "0% confidence when no patterns match"

# Test 7: Zero patterns
AGENT_PATTERNS[zero-patterns]=""
confidence=$(calculate_confidence_test "zero-patterns")
assert_equals "0" "$confidence" "0% confidence for agent with no patterns"

# Test 8: Confidence never exceeds 100%
AGENT_PATTERNS[cap-test]="file:*.matched:50"
confidence=$(calculate_confidence_test "cap-test")
TESTS_RUN=$((TESTS_RUN + 1))
if [[ $confidence -le 100 ]]; then
  echo "✓ PASS: Confidence capped at 100%"
  TESTS_PASSED=$((TESTS_PASSED + 1))
else
  echo "✗ FAIL: Confidence capped at 100%"
  echo "  Expected: <= 100"
  echo "  Actual:   $confidence"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 9: Confidence in valid range
TESTS_RUN=$((TESTS_RUN + 1))
if [[ $confidence -ge 0 ]] && [[ $confidence -le 100 ]]; then
  echo "✓ PASS: Confidence in valid range (0-100)"
  TESTS_PASSED=$((TESTS_PASSED + 1))
else
  echo "✗ FAIL: Confidence in valid range (0-100)"
  echo "  Expected: 0-100"
  echo "  Actual:   $confidence"
  TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Print summary
echo ""
echo "========================================"
echo "Test Summary"
echo "========================================"
echo "Tests run:    $TESTS_RUN"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
  echo "✓ All tests passed!"
  exit 0
else
  echo "✗ Some tests failed"
  exit 1
fi
