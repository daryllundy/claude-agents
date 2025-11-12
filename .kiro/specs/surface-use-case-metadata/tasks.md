# Implementation Plan

- [ ] 1. Create use case formatting functions
  - Implement format_use_case() function with text wrapping
  - Add get_terminal_width() function to detect terminal size
  - Create format_use_case_auto() wrapper with automatic width detection
  - Handle empty/missing use cases with placeholder text
  - Add indentation support for formatted output
  - _Requirements: 1.4, 3.3, 3.4_

- [ ] 2. Create safe use case retrieval function
  - Implement get_use_case_safe() function
  - Return placeholder text when use case is missing
  - Add optional verbose logging for missing use cases
  - _Requirements: 3.4_

- [ ] 3. Enhance render_agent_item for CLI output
  - Update render_agent_item() to accept use_case parameter
  - Add "Use for:" label and formatted use case text
  - Maintain existing description and detection pattern display
  - Format use case with appropriate indentation
  - _Requirements: 1.1, 1.2, 1.4_

- [ ] 4. Update display_recommendations to pass use cases
  - Modify display_recommendations() to accept use_cases_ref parameter
  - Pass AGENT_USE_CASES to render_agent_item calls
  - Ensure use cases are displayed for all recommended agents
  - _Requirements: 1.1, 1.3_

- [ ] 5. Enhance interactive mode rendering
  - Update render_agent_item_interactive() to include use_case parameter
  - Display use case only for currently highlighted agent to save space
  - Add conditional display based on is_current flag
  - Format use case with terminal width awareness
  - _Requirements: 3.1, 3.2, 3.3_

- [ ] 6. Update interactive_selection to pass use cases
  - Modify interactive_selection() to pass AGENT_USE_CASES to rendering functions
  - Ensure use case updates when navigating between agents
  - Test use case display in interactive mode
  - _Requirements: 3.1, 3.2_

- [ ] 7. Enhance JSON export with use cases
  - Update export_profile() to include use_cases field
  - Properly escape use case text for JSON format
  - Add use_cases to each agent object in exported JSON
  - Validate JSON structure with use cases included
  - _Requirements: 2.1, 2.2, 2.4_

- [ ] 8. Update JSON import to handle use cases
  - Modify import_profile() to read use_cases field
  - Display use case information when loading profiles
  - Handle profiles with missing use_cases field gracefully
  - _Requirements: 2.3, 2.4_

- [ ] 9. Add verbose mode use case display
  - Create display_agent_verbose() function
  - Include use case in verbose agent information
  - Format output with clear labels and structure
  - Add to verbose mode output
  - _Requirements: 1.2_

- [ ] 10. Implement use case validation
  - Create validate_use_cases() function
  - Check that all agents have use case metadata
  - Log warnings for agents missing use cases
  - Return validation status
  - _Requirements: 2.4, 3.4_

- [ ] 11. Add text wrapping edge case handling
  - Implement format_use_case_safe() with minimum width check
  - Handle very narrow terminals gracefully
  - Add fallback for terminals < 40 columns
  - Test with various terminal widths
  - _Requirements: 1.4, 3.3_

- [ ] 12. Create unit tests for formatting functions
  - Write test for format_use_case() text wrapping
  - Create test for empty use case handling
  - Write test for indentation application
  - Add test for get_use_case_safe() with missing use case
  - Create test for terminal width detection
  - _Requirements: 1.4, 3.3, 3.4_

- [ ] 13. Create integration tests for CLI output
  - Write test verifying use cases appear in CLI output
  - Create test for "Use for:" label presence
  - Write test for use case formatting in output
  - Add test for multiple agents with use cases
  - _Requirements: 1.1, 1.2, 1.3_

- [ ] 14. Create integration tests for JSON export
  - Write test for use_cases field in exported JSON
  - Create test for proper JSON escaping of use case text
  - Write test for profile import with use cases
  - Add test for backward compatibility with profiles without use cases
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ] 15. Create integration tests for interactive mode
  - Write test for use case display for current agent
  - Create test for use case update when navigating
  - Write test for use case truncation in narrow terminals
  - Add test for missing use case placeholder
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 16. Add performance optimization with caching
  - Implement USE_CASE_WRAP_CACHE associative array
  - Create format_use_case_cached() function
  - Cache wrapped text by use case, indent, and width
  - Add cache lookup before formatting
  - _Requirements: 1.4, 3.3_

- [ ] 17. Update documentation
  - Document use case display in CLI output
  - Add examples of use case formatting
  - Document interactive mode use case display
  - Add JSON schema documentation with use_cases field
  - Document how to add use cases to AGENTS_REGISTRY.md
  - _Requirements: 1.1, 2.1, 3.1_

- [ ] 18. Validate all agents have use cases in registry
  - Run validate_use_cases() on current agent set
  - Add missing use cases to AGENTS_REGISTRY.md if needed
  - Verify use case text is clear and helpful
  - Test that all use cases display correctly
  - _Requirements: 2.4, 3.4_
