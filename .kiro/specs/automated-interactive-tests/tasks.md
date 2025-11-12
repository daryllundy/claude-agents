# Implementation Plan

- [x] 1. Extract selection state management into testable functions
  - Create init_selection_state() function that initializes agent selections based on confidence threshold
  - Implement toggle_agent_selection() function for toggling individual agent selection
  - Create select_all_agents() and select_none_agents() functions for bulk operations
  - Implement get_selected_agents() function to retrieve currently selected agents
  - Add get_selection_count() function to count selected agents
  - _Requirements: 2.1, 2.2_
  - _Status: COMPLETED - All functions implemented in scripts/recommend_agents.sh_

- [x] 2. Extract UI rendering into testable functions
  - Create render_category_header() function for category display
  - Implement render_agent_item() function for individual agent display with selection indicator
  - Create render_confidence_bar() function for visual confidence representation
  - Implement render_navigation_footer() function for help text display
  - Create render_agent_list() function that orchestrates complete UI rendering
  - _Requirements: 2.3, 4.1, 4.2_
  - _Status: PARTIALLY COMPLETE - draw_progress_bar() exists but other rendering functions need extraction from interactive_selection()_

- [x] 3. Refactor input handling into testable function
  - Create handle_keyboard_input() function that processes key events and returns new state
  - Implement arrow key navigation logic (up/down)
  - Add space bar toggle logic
  - Implement command key handling (a, n, q)
  - Add enter key confirmation logic
  - _Requirements: 1.2, 2.2_
  - _Status: NOT STARTED - Input handling is inline in interactive_selection()_

- [x] 4. Refactor interactive_selection() to use extracted functions
  - Update interactive_selection() to call init_selection_state()
  - Replace inline rendering with render_agent_list() calls
  - Replace inline input handling with handle_keyboard_input() calls
  - Update to use get_selected_agents() for returning results
  - _Requirements: 1.1, 2.1_
  - _Status: PARTIALLY COMPLETE - Uses init_selection_state() and get_selected_agents(), but rendering and input handling still inline_

- [x] 5. Create unit tests for selection state management
  - Write test for init_selection_state() with various confidence thresholds
  - Create test for toggle_agent_selection() state changes
  - Write test for select_all_agents() functionality
  - Create test for select_none_agents() functionality
  - Write test for get_selection_count() accuracy
  - Add test for get_selected_agents() output
  - _Requirements: 1.1, 2.2_
  - _Status: COMPLETED - tests/unit/test_selection_state.sh fully implemented_

- [ ] 6. Create unit tests for rendering functions
  - Write test for render_confidence_bar() width and format
  - Create test for render_agent_item() output format with selected/unselected states
  - Write test for render_category_header() format
  - Create test for render_navigation_footer() content
  - Add test for terminal width handling in rendering
  - _Requirements: 4.1, 4.2, 4.3, 4.4_
  - _Status: NOT STARTED - Depends on Task 2 completion_

- [ ] 7. Create expect-based integration tests
  - Write expect script for testing navigation (up/down arrow keys)
  - Create expect script for testing selection toggle (space bar)
  - Write expect script for testing select all command (a key)
  - Create expect script for testing select none command (n key)
  - Write expect script for testing confirmation (enter key)
  - Add expect script for testing quit command (q key)
  - _Requirements: 1.1, 1.2, 3.2_
  - _Status: NOT STARTED - No .exp files exist yet_

- [ ] 8. Create bash wrapper for expect tests
  - Implement check for expect availability
  - Create test runner that executes all expect scripts
  - Add proper exit code handling for test results
  - Implement skip logic when expect is unavailable
  - _Requirements: 3.2, 3.3_
  - _Status: NOT STARTED - Depends on Task 7 completion_

- [x] 9. Add terminal capability checks
  - Implement check_terminal_capabilities() function
  - Add terminal size validation (minimum 20x60)
  - Create safe_interactive_selection() wrapper with fallback
  - Add graceful degradation to non-interactive mode
  - _Requirements: 1.4, 3.1_
  - _Status: NOT STARTED_

- [x] 10. Add terminal cleanup and signal handling
  - Implement cleanup_terminal() function to restore terminal state
  - Add trap handlers for EXIT, INT, and TERM signals
  - Ensure cursor visibility is restored on exit
  - Add terminal settings restoration (stty sane)
  - _Requirements: 1.4_
  - _Status: NOT STARTED_

- [ ] 11. Integrate tests into CI pipeline
  - Update test runner script to include interactive tests
  - Add conditional execution based on expect availability
  - Implement test result aggregation and reporting
  - Add skip messages for unavailable test tools
  - _Requirements: 3.1, 3.3, 3.4_
  - _Status: PARTIALLY COMPLETE - tests/run_all_tests.sh exists but needs expect test integration_

- [ ] 12. Create test fixtures for interactive mode
  - Create fixture with multiple agent categories
  - Add fixture with agents at various confidence levels
  - Create fixture with edge cases (single agent, many agents)
  - Add fixture for testing default selections
  - _Requirements: 1.1, 1.3_
  - _Status: NOT STARTED - Existing fixtures are for detection, not interactive mode_

- [ ] 13. Update documentation
  - Document how to run interactive mode tests locally
  - Add troubleshooting guide for test failures
  - Update README with testing requirements (expect installation)
  - Document test coverage for interactive mode
  - Add contribution guidelines for interactive mode changes
  - _Requirements: 2.4, 3.4_
  - _Status: NOT STARTED_
