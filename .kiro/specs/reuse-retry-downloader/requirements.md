# Requirements Document

## Introduction

This document specifies the requirements for consolidating all network operations in the agent recommendation system to use a unified retry mechanism with exponential backoff. Currently, the system has inconsistent network handling where some operations use the `fetch_with_retry` function while others call `curl` directly, leading to reliability issues in CI environments and for users with intermittent connectivity. This feature will standardize all network operations and add optional caching to support offline workflows.

## Glossary

- **Agent Recommendation System**: The bash script system that analyzes project files and recommends relevant Claude Code agents
- **fetch_with_retry**: An existing function that downloads files with exponential backoff retry logic
- **Network Operation**: Any operation that fetches data from remote URLs (agent downloads, update checks, registry fetches)
- **Exponential Backoff**: A retry strategy where wait time doubles after each failed attempt (1s, 2s, 4s)
- **Cache**: Local storage of previously fetched remote content to reduce network requests
- **Update Operation**: Functions that check for and apply updates to local agent files
- **Registry**: The AGENTS_REGISTRY.md file that catalogs all available agents
- **CI Environment**: Continuous Integration systems where automated builds and tests run

## Requirements

### Requirement 1: Unified Retry Mechanism

**User Story:** As a developer using the agent recommendation system, I want all network operations to automatically retry on failure, so that transient network issues do not cause the tool to fail.

#### Acceptance Criteria

1. WHEN the Agent Recommendation System performs any network operation, THE Agent Recommendation System SHALL use the fetch_with_retry function
2. WHEN fetch_with_retry attempts a download, THE Agent Recommendation System SHALL retry up to 3 times with exponential backoff delays of 1 second, 2 seconds, and 4 seconds
3. WHEN fetch_with_retry performs a retry attempt, THE Agent Recommendation System SHALL log the HTTP status code and attempt number
4. WHEN fetch_with_retry exhausts all retry attempts, THE Agent Recommendation System SHALL provide troubleshooting guidance including connectivity checks and URL verification

### Requirement 2: Enhanced Error Handling

**User Story:** As a developer troubleshooting network failures, I want detailed error messages and diagnostic information, so that I can quickly identify and resolve connectivity issues.

#### Acceptance Criteria

1. WHEN a network operation fails, THE Agent Recommendation System SHALL log the HTTP status code received from the server
2. WHEN all retry attempts fail, THE Agent Recommendation System SHALL display troubleshooting steps including internet connection verification, URL accessibility check, proxy detection, and retry timing guidance
3. IF verbose mode is enabled, THEN THE Agent Recommendation System SHALL log each download attempt with the URL and attempt number
4. WHEN a network timeout occurs, THE Agent Recommendation System SHALL apply a 30-second timeout per attempt

### Requirement 3: Optional Caching Layer

**User Story:** As a developer working offline or in a CI environment, I want previously fetched remote content to be cached locally, so that I can continue working without constant network access.

#### Acceptance Criteria

1. WHEN the Agent Recommendation System fetches remote content, THE Agent Recommendation System SHALL store the content in a cache directory at $XDG_CACHE_HOME/agent-recommendation or ~/.cache/agent-recommendation
2. WHEN the Agent Recommendation System needs remote content, THE Agent Recommendation System SHALL check if a cached version exists and is less than 24 hours old
3. WHILE a cached file is fresh, THE Agent Recommendation System SHALL use the cached content without making a network request
4. WHERE the user provides a force-refresh flag, THE Agent Recommendation System SHALL bypass the cache and fetch fresh content from the network

### Requirement 4: Refactored Update Operations

**User Story:** As a developer maintaining agent definitions, I want update operations to use reliable network handling with automatic backups, so that failed updates do not corrupt my local agent files.

#### Acceptance Criteria

1. WHEN check_updates function executes, THE Agent Recommendation System SHALL use fetch_with_retry to download remote agent files for comparison
2. WHEN update_all_agents function updates an agent file, THE Agent Recommendation System SHALL create a backup of the existing file before attempting the update
3. IF an update operation fails, THEN THE Agent Recommendation System SHALL restore the agent file from the backup
4. WHEN update_all_agents completes, THE Agent Recommendation System SHALL report the count of successfully updated agents and failed updates

### Requirement 5: Cache Management

**User Story:** As a developer managing disk space and ensuring fresh data, I want control over the cache behavior, so that I can clear stale data or force fresh downloads when needed.

#### Acceptance Criteria

1. WHERE the user provides a clear-cache flag, THE Agent Recommendation System SHALL remove all cached files from the cache directory
2. WHERE the user provides a cache-dir flag with a directory path, THE Agent Recommendation System SHALL use the specified directory for caching instead of the default location
3. WHERE the user provides a cache-expiry flag with a duration in seconds, THE Agent Recommendation System SHALL use the specified duration instead of the default 24-hour expiry
4. WHEN the cache directory does not exist, THE Agent Recommendation System SHALL create the directory with appropriate permissions
