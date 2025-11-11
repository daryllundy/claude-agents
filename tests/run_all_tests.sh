#!/usr/bin/env bash
set -euo pipefail

# Master test runner for all agent recommendation tests
# Runs both unit and integration tests

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test suite counters
SUITES_RUN=0
SUITES_PASSED=0
SUITES_FAILED=0

echo "========================================="
echo "Claude Code Agents - Test Suite"
echo "========================================="
echo ""

# Function to run a test suite
run_suite() {
  local suite_name="$1"
  local suite_script="$2"
  
  ((SUITES_RUN++))
  
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}Running: $suite_name${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  if bash "$suite_script"; then
    ((SUITES_PASSED++))
    echo ""
    echo -e "${GREEN}✓ $suite_name PASSED${NC}"
  else
    ((SUITES_FAILED++))
    echo ""
    echo -e "${RED}✗ $suite_name FAILED${NC}"
  fi
  
  echo ""
}

# Run unit tests
echo -e "${YELLOW}═══════════════════════════════════════${NC}"
echo -e "${YELLOW}UNIT TESTS${NC}"
echo -e "${YELLOW}═══════════════════════════════════════${NC}"
echo ""

run_suite "Detection Functions" "$SCRIPT_DIR/unit/test_detection_functions.sh"
run_suite "Confidence Scoring" "$SCRIPT_DIR/unit/test_confidence_scoring.sh"
run_suite "Profile Management" "$SCRIPT_DIR/unit/test_profile_management.sh"
run_suite "Update Detection" "$SCRIPT_DIR/unit/test_update_detection.sh"

# Run integration tests
echo -e "${YELLOW}═══════════════════════════════════════${NC}"
echo -e "${YELLOW}INTEGRATION TESTS${NC}"
echo -e "${YELLOW}═══════════════════════════════════════${NC}"
echo ""

run_suite "End-to-End Detection" "$SCRIPT_DIR/integration/test_detection.sh"

# Final summary
echo ""
echo "========================================="
echo "FINAL TEST SUMMARY"
echo "========================================="
echo "Test suites run:    $SUITES_RUN"
echo -e "${GREEN}Test suites passed: $SUITES_PASSED${NC}"

if [[ $SUITES_FAILED -gt 0 ]]; then
  echo -e "${RED}Test suites failed: $SUITES_FAILED${NC}"
  echo ""
  echo -e "${RED}❌ SOME TESTS FAILED${NC}"
  exit 1
else
  echo ""
  echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
  exit 0
fi
