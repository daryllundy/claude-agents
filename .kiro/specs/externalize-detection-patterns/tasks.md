# Implementation Plan

- [x] 1. Create pattern file directory structure
  - Create data/patterns/ directory in repository root
  - Set up subdirectory organization for pattern categories
  - Add .gitkeep or README to ensure directory is tracked
  - _Requirements: 2.1, 2.2_

- [x] 2. Define YAML schema and create example pattern files
  - Document YAML schema with version, agents, patterns structure
  - Create example pattern file with all supported fields
  - Define pattern types (file, path, content) and weight guidelines
  - Add schema documentation to repository
  - _Requirements: 1.2, 3.3_

- [x] 3. Extract existing patterns to YAML files
  - Create infrastructure.yml with cloud, IaC, and platform agent patterns
  - Create development.yml with frontend, backend, mobile, and database patterns
  - Create quality.yml with testing, security, and review agent patterns
  - Create operations.yml with migration, dependency, and git patterns
  - Create productivity.yml with scaffolding, documentation, and debugging patterns
  - Create business.yml with validation, architecture, localization, and compliance patterns
  - Create specialized.yml with data science and e-commerce patterns
  - _Requirements: 1.1, 2.1_

- [x] 4. Implement YAML parser detection and wrapper
  - Create check_yaml_parser() function to detect yq or python3 availability
  - Implement parse_yaml_with_yq() for yq-based parsing
  - Implement parse_yaml_with_python() for Python-based parsing
  - Create parse_yaml() wrapper that selects appropriate parser
  - _Requirements: 1.1_

- [x] 5. Implement pattern file discovery
  - Create discover_pattern_files() function to find YAML files in data/patterns directory
  - Add error handling for missing pattern directory
  - Support finding .yml and .yaml extensions
  - Add logging for discovered pattern files
  - _Requirements: 1.1, 2.2_

- [x] 6. Implement schema validation using jq
  - Create validate_pattern_schema() function using jq for JSON validation
  - Add validation for required top-level fields (version, agents)
  - Implement validation for agent fields (name, patterns)
  - Add validation for pattern fields (type, match, weight)
  - Implement pattern type validation (file, path, content only)
  - Add descriptive error messages for validation failures
  - _Requirements: 1.3, 2.4_

- [x] 7. Implement pattern data structure population from JSON
  - Create load_pattern_file() function to process single YAML file
  - Parse JSON output from parse_yaml() using jq
  - Populate AGENT_PATTERNS with pattern strings in format "type:match:weight\n"
  - Populate AGENT_DESCRIPTIONS with agent descriptions
  - Populate AGENT_CATEGORIES with agent categories
  - Add logging for loaded agents and pattern counts
  - _Requirements: 1.1, 1.2_

- [x] 8. Implement pattern loading orchestration
  - Create load_pattern_files() function to discover and load all pattern files
  - Add support for loading multiple pattern files sequentially
  - Merge patterns from multiple files into global associative arrays
  - Implement error aggregation across multiple files
  - Add summary logging of total patterns loaded
  - _Requirements: 1.1, 2.2, 2.3_

- [x] 9. Add custom pattern directory support
  - Add --patterns-dir command-line flag support to argument parsing
  - Implement environment variable support (AGENT_PATTERNS_DIR)
  - Create setup_patterns_directory() for priority resolution (CLI > env > default)
  - Add validation for custom directory existence
  - Update load_pattern_files() to use custom directory when specified
  - _Requirements: 3.1, 3.2, 3.4_

- [x] 10. Implement dependency checking
  - Create check_dependencies() function to verify jq availability
  - Add check for YAML parser (yq or python3 with PyYAML)
  - Implement descriptive error messages with installation instructions
  - Add platform-specific installation guidance (brew, apt, etc.)
  - Call check_dependencies() early in script execution
  - _Requirements: 1.3_

- [x] 11. Add error handling and fallback logic
  - Create safe_load_patterns() wrapper with try-catch error handling
  - Implement fallback to initialize_detection_patterns_hardcoded() on failure
  - Add validation that at least some patterns loaded successfully
  - Implement graceful degradation with warning messages
  - Log when falling back to hardcoded patterns
  - _Requirements: 1.3, 1.4_

- [x] 12. Refactor main script to use pattern loader
  - Replace load_detection_patterns() call with safe_load_patterns()
  - Update script initialization to call pattern loading early (after argument parsing)
  - Ensure detection engine uses populated AGENT_PATTERNS data structures
  - Verify backward compatibility with existing detection logic
  - Test that confidence calculation works with YAML-loaded patterns
  - _Requirements: 1.4, 2.3_

- [x]* 13. Create unit tests for pattern loading
  - Write test for parse_yaml() with valid YAML input
  - Create test for validate_pattern_schema() with valid schema
  - Write test for validate_pattern_schema() rejecting missing version
  - Create test for validate_pattern_schema() rejecting invalid pattern type
  - Write test for load_pattern_file() populating data structures correctly
  - Add test for error handling with malformed YAML
  - Note: Test framework created in test_pattern_loading.sh; manual testing verified all functionality
  - _Requirements: 1.1, 1.3_

- [ ]* 14. Create integration tests for pattern system
  - Write test for load_pattern_files() discovering multiple files
  - Create test for custom patterns overriding defaults
  - Write test for pattern loading with missing dependencies
  - Create test for fallback to legacy patterns on error
  - Add test for environment variable pattern directory override
  - Write test for CLI flag pattern directory override
  - _Requirements: 1.4, 3.1, 3.2_

- [ ]* 15. Add pattern caching for performance
  - Create cache_parsed_patterns() function for JSON caching
  - Implement cache invalidation based on file modification time
  - Add cache directory management (creation, cleanup)
  - Implement lazy loading with ensure_patterns_loaded() function
  - _Requirements: 1.1_

- [ ]* 16. Update documentation
  - Document YAML pattern file schema with examples
  - Add custom pattern usage guide to README
  - Document required dependencies (jq, yq/python3)
  - Create troubleshooting guide for pattern loading issues
  - Add migration guide for converting hardcoded patterns to YAML
  - Document pattern weight guidelines and best practices
  - _Requirements: 3.3_

- [ ]* 17. Create example custom pattern files
  - Create example custom pattern file for AWS-heavy projects
  - Create example custom pattern file for startup/MVP projects
  - Create example custom pattern file for enterprise compliance projects
  - Add examples directory with documented use cases
  - _Requirements: 3.3_
