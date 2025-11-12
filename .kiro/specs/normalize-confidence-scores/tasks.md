# Implementation Plan

- [ ] 1. Create calculate_max_possible_weight helper function
  - Implement function to sum all pattern weights for an agent
  - Add parsing of pattern strings to extract weights
  - Handle empty pattern strings gracefully
  - Return total weight as integer
  - _Requirements: 1.1, 2.1_

- [ ] 2. Refactor calculate_confidence to use dynamic max weight
  - Replace fixed max_possible_weight=100 with dynamic calculation
  - Add loop to sum all pattern weights before evaluation
  - Update confidence calculation to use agent-specific max weight
  - Ensure confidence is capped at 100%
  - Add zero-division protection when max weight is zero
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 3. Add verbose logging for confidence calculations
  - Add logging of accumulated weight in verbose mode
  - Log max possible weight for each agent
  - Log final confidence percentage
  - Add conditional logging based on VERBOSE flag
  - _Requirements: 2.4_

- [ ] 4. Create validation function for pattern weights
  - Implement validate_pattern_weights function
  - Check that all agents have positive max possible weights
  - Add warnings for agents with zero total weight
  - Add errors for agents with negative weights
  - Return error count for validation failures
  - _Requirements: 2.3_

- [ ] 5. Add debug output function for confidence calculation
  - Create debug_confidence_calculation function for detailed output
  - Display each pattern with match status and weight
  - Show accumulated weight and max possible weight
  - Display final confidence calculation
  - Format output with visual indicators (✓/✗)
  - _Requirements: 2.4, 3.3_

- [ ] 6. Create comparison tool for old vs new calculations
  - Implement calculate_confidence_old with fixed max=100
  - Create compare_confidence_methods function
  - Display side-by-side comparison of old and new confidence scores
  - Calculate and display difference between methods
  - Format output as table with agent names and scores
  - _Requirements: 3.1, 3.2_

- [ ] 7. Add get_all_max_weights utility function
  - Implement function to calculate max weights for all agents
  - Sort output by agent name
  - Format as table with agent names and max weights
  - Use for debugging and validation
  - _Requirements: 2.4_

- [ ] 8. Implement max weight caching for performance
  - Create AGENT_MAX_WEIGHTS_CACHE associative array
  - Implement get_max_possible_weight with caching
  - Add cache lookup before calculation
  - Store calculated values in cache
  - _Requirements: 2.1, 2.2_

- [ ] 9. Add error handling for edge cases
  - Handle empty pattern strings (return 0 confidence)
  - Prevent division by zero when max weight is 0
  - Handle integer overflow for large weight sums
  - Add bc-based calculation for weights > 10000
  - _Requirements: 1.3, 1.4_

- [ ] 10. Create unit tests for max weight calculation
  - Write test for calculate_max_possible_weight with multiple patterns
  - Create test for empty pattern string
  - Write test for single pattern
  - Add test for patterns with various weight values
  - _Requirements: 1.1, 2.1_

- [ ] 11. Create unit tests for confidence calculation
  - Write test for all patterns matched (100% confidence)
  - Create test for partial pattern match
  - Write test for no patterns matched (0% confidence)
  - Add test for zero patterns defined
  - Create test for confidence capping at 100%
  - Write test for zero-division protection
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 12. Create integration tests for realistic scenarios
  - Write test for terraform specialist with typical project structure
  - Create test for multiple agents with same project
  - Add test verifying confidence scores are in valid range (0-100)
  - Write test for confidence score comparability across agents
  - _Requirements: 3.1, 3.2, 3.4_

- [ ] 13. Create regression tests
  - Write test ensuring all agents produce valid confidence scores (0-100)
  - Create test for confidence calculation with all agent patterns
  - Add test comparing results before and after changes
  - Verify no agents have invalid or unexpected scores
  - _Requirements: 1.2, 1.3, 3.1_

- [ ] 14. Run comparison tool on test projects
  - Execute compare_confidence_methods on sample projects
  - Document differences between old and new calculations
  - Verify new scores are more accurate
  - Check that ranking order makes sense
  - _Requirements: 3.1, 3.2, 3.4_

- [ ] 15. Update documentation
  - Document confidence calculation formula in README
  - Add examples of confidence score calculations
  - Explain interpretation of confidence percentages (75-100%, 50-74%, etc.)
  - Add troubleshooting guide for unexpected scores
  - Document how pattern weights affect confidence
  - _Requirements: 3.3_

- [ ] 16. Add command-line flag for debug mode
  - Implement --debug-confidence flag parsing
  - Add flag to trigger debug_confidence_calculation output
  - Support agent name argument for specific agent debugging
  - Display detailed calculation for specified agents
  - _Requirements: 2.4, 3.3_
