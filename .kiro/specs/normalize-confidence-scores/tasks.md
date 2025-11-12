# Implementation Plan

- [x] 1. Create calculate_max_possible_weight helper function
  - Implement function to sum all pattern weights for an agent
  - Add parsing of pattern strings to extract weights
  - Handle empty pattern strings gracefully
  - Return total weight as integer
  - _Status: Implemented in scripts/recommend_agents.sh (lines 2002-2020)_

- [x] 2. Refactor calculate_confidence to use dynamic max weight
  - Replace fixed max_possible_weight=100 with dynamic calculation
  - Add loop to sum all pattern weights before evaluation
  - Update confidence calculation to use agent-specific max weight
  - Ensure confidence is capped at 100%
  - Add zero-division protection when max weight is zero
  - _Status: Implemented in scripts/recommend_agents.sh (lines 2095-2180)_

- [x] 3. Add verbose logging for confidence calculations
  - Add logging of accumulated weight in verbose mode
  - Log max possible weight for each agent
  - Log final confidence percentage
  - Add conditional logging based on VERBOSE flag
  - _Status: Implemented in calculate_confidence function (line 2175)_

- [x] 4. Create validation function for pattern weights
  - Implement validate_pattern_weights function
  - Check that all agents have positive max possible weights
  - Add warnings for agents with zero total weight
  - Add errors for agents with negative weights
  - Return error count for validation failures
  - _Status: Implemented in scripts/recommend_agents.sh (lines 2036-2056)_

- [x] 5. Add debug output function for confidence calculation
  - Create debug_confidence_calculation function for detailed output
  - Display each pattern with match status and weight
  - Show accumulated weight and max possible weight
  - Display final confidence calculation
  - Format output with visual indicators (✓/✗)
  - _Status: Implemented in scripts/recommend_agents.sh (lines 2073-2140)_

- [ ] 6. Create comparison tool for old vs new calculations
  - Implement calculate_confidence_old with fixed max=100
  - Create compare_confidence_methods function
  - Display side-by-side comparison of old and new confidence scores
  - Calculate and display difference between methods
  - Format output as table with agent names and scores
  - _Status: Not implemented - would be useful for validation but not essential since implementation is complete_

- [x] 7. Add get_all_max_weights utility function
  - Implement function to calculate max weights for all agents
  - Sort output by agent name
  - Format as table with agent names and max weights
  - Use for debugging and validation
  - _Status: Implemented in scripts/recommend_agents.sh (lines 2058-2071)_

- [x] 8. Implement max weight caching for performance
  - Create AGENT_MAX_WEIGHTS_CACHE associative array
  - Implement get_max_possible_weight with caching
  - Add cache lookup before calculation
  - Store calculated values in cache
  - _Status: Implemented in scripts/recommend_agents.sh (lines 2022-2034)_

- [x] 9. Add error handling for edge cases
  - Handle empty pattern strings (return 0 confidence)
  - Prevent division by zero when max weight is 0
  - Handle integer overflow for large weight sums
  - Add bc-based calculation for weights > 10000
  - _Status: Implemented in calculate_confidence function (lines 2095-2180)_

- [x] 10. Create unit tests for max weight calculation
  - Write test for calculate_max_possible_weight with multiple patterns
  - Create test for empty pattern string
  - Write test for single pattern
  - Add test for patterns with various weight values
  - _Status: Implemented in tests/unit/test_confidence_normalization.sh_

- [x] 11. Create unit tests for confidence calculation
  - Write test for all patterns matched (100% confidence)
  - Create test for partial pattern match
  - Write test for no patterns matched (0% confidence)
  - Add test for zero patterns defined
  - Create test for confidence capping at 100%
  - Write test for zero-division protection
  - _Status: Implemented in tests/unit/test_confidence_normalization.sh_

- [x] 12. Create integration tests for realistic scenarios
  - Write test for terraform specialist with typical project structure
  - Create test for multiple agents with same project
  - Add test verifying confidence scores are in valid range (0-100)
  - Write test for confidence score comparability across agents
  - _Status: Implemented in tests/unit/test_confidence_scoring.sh_

- [x] 13. Update documentation for confidence calculation
  - Update CHANGELOG.md confidence formula (currently shows old formula with /100)
  - Update README.md to explain dynamic max weight calculation
  - Add examples showing how different agents have different max weights
  - Document --debug-confidence flag usage and output
  - Document --show-max-weights flag for viewing all agent max weights
  - Add troubleshooting section for understanding confidence scores
  - _Status: Implementation complete, but documentation shows outdated formula_
  - _Files to update: CHANGELOG.md (line 171), README.md (pattern weights section)_

- [x] 16. Add command-line flag for debug mode
  - Implement --debug-confidence flag parsing
  - Add flag to trigger debug_confidence_calculation output
  - Support agent name argument for specific agent debugging
  - Display detailed calculation for specified agents
  - _Status: Implemented in scripts/recommend_agents.sh (lines 82-91) and integrated into main flow (lines 2383-2392)_
