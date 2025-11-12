# Implementation Plan

- [ ] 1. Enhance fetch_with_retry function
  - Add optional max_attempts parameter (default 3)
  - Add optional timeout parameter (default 30 seconds)
  - Implement verbose logging for each attempt
  - Add detailed troubleshooting guidance on final failure
  - Improve HTTP status code diagnostics
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.4_

- [ ] 2. Create cache directory initialization
  - Implement init_cache() function to create cache directory
  - Use XDG_CACHE_HOME or fallback to ~/.cache
  - Add error handling for directory creation failures
  - Return success/failure status
  - _Requirements: 3.1_

- [ ] 3. Implement cache path generation
  - Create get_cache_path() function to generate cache file paths
  - Use SHA256 hash of URL as cache filename
  - Return full path to cache file
  - _Requirements: 3.1_

- [ ] 4. Implement cache freshness checking
  - Create is_cache_fresh() function to check file age
  - Support configurable expiry time in seconds
  - Handle platform differences (macOS vs Linux stat commands)
  - Return true if cache is fresh, false otherwise
  - _Requirements: 3.2, 3.3_

- [ ] 5. Implement fetch_with_cache function
  - Create function that checks cache before fetching
  - Implement cache freshness validation
  - Fall back to fetch_with_retry on cache miss or stale data
  - Store fetched content in cache on success
  - Support force refresh flag to bypass cache
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 6. Add cache management functions
  - Implement clear_cache() function to remove all cached files
  - Add logging for cache operations
  - Handle missing cache directory gracefully
  - _Requirements: 3.4_

- [ ] 7. Refactor check_updates to use fetch_with_cache
  - Replace direct curl calls with fetch_with_cache
  - Use 1-hour cache expiry for update checks
  - Add error handling for failed fetches
  - Log warnings for agents that fail to check
  - Clean up temporary files properly
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 3.1_

- [ ] 8. Refactor update_all_agents to use fetch_with_retry
  - Replace direct curl calls with fetch_with_retry
  - Implement backup creation before updates
  - Add rollback on fetch failure
  - Track updated and failed counts
  - Provide summary of update results
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2_

- [ ] 9. Create fetch_registry function
  - Implement function to fetch AGENTS_REGISTRY.md
  - Use fetch_with_cache with 1-hour expiry
  - Add logging for success/failure
  - Return appropriate exit code
  - _Requirements: 1.1, 2.1_

- [ ] 10. Add command-line flags for cache control
  - Implement --force-refresh flag to bypass cache
  - Add --clear-cache flag to remove cached files
  - Implement --cache-dir flag to specify custom cache location
  - Add --cache-expiry flag to set custom expiry time
  - Parse flags in main script initialization
  - _Requirements: 3.4_

- [ ] 11. Add cache configuration variables
  - Define CACHE_DIR with XDG_CACHE_HOME fallback
  - Set CACHE_EXPIRY_SECONDS default (24 hours)
  - Add FORCE_REFRESH flag (default false)
  - Document configuration options
  - _Requirements: 3.1, 3.2, 3.4_

- [ ] 12. Create unit tests for fetch_with_retry
  - Write test for successful first attempt
  - Create test for retry on failure
  - Write test for exhausted retries
  - Add test for timeout handling
  - Create test for verbose logging
  - _Requirements: 1.1, 1.2, 1.3, 2.4_

- [ ] 13. Create unit tests for caching functions
  - Write test for cache path generation
  - Create test for cache freshness with fresh file
  - Write test for cache freshness with stale file
  - Add test for fetch_with_cache using cached data
  - Create test for fetch_with_cache with stale cache
  - Write test for force refresh bypassing cache
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 14. Create integration tests for update operations
  - Write test for check_updates using retry logic
  - Create test for update_all_agents with backups
  - Write test for update_all_agents rollback on failure
  - Add test for fetch_registry with caching
  - Create test for cache hit/miss scenarios
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1_

- [ ] 15. Add cache statistics tracking
  - Implement CACHE_HITS and CACHE_MISSES counters
  - Create fetch_with_cache_stats wrapper function
  - Implement print_cache_stats function
  - Add optional cache statistics output in verbose mode
  - _Requirements: 3.1, 3.2_

- [ ] 16. Update documentation
  - Document retry behavior (attempts, backoff, timeout)
  - Add caching documentation with examples
  - Document cache control flags
  - Add troubleshooting guide for network failures
  - Document cache location and expiry defaults
  - Add examples of offline workflow usage
  - _Requirements: 2.2, 2.3, 3.1, 3.2, 3.3, 3.4_

- [ ] 17. Test in CI environment
  - Validate retry logic works in automated builds
  - Test cache behavior in CI
  - Verify error messages are helpful
  - Ensure transient failures don't break workflows
  - _Requirements: 1.1, 1.2, 1.4_
