# Design Document

## Overview

This document outlines the design for consolidating all network operations in the agent recommendation system to use the existing `fetch_with_retry` function. Currently, update operations and some download paths call `curl` directly, missing out on exponential backoff retry logic and consistent error handling. This refactoring improves reliability, especially in CI environments and for users with intermittent connectivity.

The solution also adds optional caching for remote manifests to support offline workflows and reduce unnecessary network requests.

## Architecture

### Current (Inconsistent) Implementation

```
┌─────────────────────────────────────────────────────────────┐
│              Network Operations                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Agent Downloads:                                            │
│  ├─ fetch_agent() → fetch_with_retry() ✓                    │
│  └─ Has retry logic and error handling                      │
│                                                              │
│  Update Operations:                                          │
│  ├─ check_updates() → curl directly ✗                       │
│  ├─ update_all_agents() → curl directly ✗                   │
│  └─ No retry logic, inconsistent errors                     │
│                                                              │
│  Registry Downloads:                                         │
│  ├─ fetch_registry() → curl directly ✗                      │
│  └─ No retry logic                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### New (Consistent) Implementation

```
┌─────────────────────────────────────────────────────────────┐
│              Network Operations                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  All Operations:                                             │
│  ├─ fetch_agent() → fetch_with_retry() ✓                    │
│  ├─ check_updates() → fetch_with_retry() ✓                  │
│  ├─ update_all_agents() → fetch_with_retry() ✓              │
│  ├─ fetch_registry() → fetch_with_retry() ✓                 │
│  └─ Consistent retry logic and error handling               │
│                                                              │
│  Optional Caching Layer:                                     │
│  ├─ fetch_with_cache() → checks cache first                 │
│  ├─ Falls back to fetch_with_retry()                        │
│  └─ Stores results in cache                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Application Layer                           │
│  (check_updates, update_all_agents, fetch_agent, etc.)      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  Caching Layer (Optional)                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  fetch_with_cache()                                  │   │
│  │  - Check cache validity                              │   │
│  │  - Return cached data if fresh                       │   │
│  │  - Delegate to fetch_with_retry if needed            │   │
│  │  - Store results in cache                            │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  Retry Layer                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  fetch_with_retry()                                  │   │
│  │  - Exponential backoff (3 attempts)                  │   │
│  │  - HTTP status code logging                          │   │
│  │  - Troubleshooting guidance on failure               │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  Network Layer                               │
│  (curl with appropriate flags and timeouts)                  │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Enhanced fetch_with_retry Function

Ensure the existing function supports all use cases.

#### Current Implementation

```bash
fetch_with_retry() {
  local url="$1"
  local output="$2"
  local max_attempts=3
  local attempt=1
  local backoff=1
  
  while [[ $attempt -le $max_attempts ]]; do
    if curl -fsSL "$url" -o "$output"; then
      return 0
    fi
    
    local http_code=$(curl -fsSL -w "%{http_code}" -o /dev/null "$url")
    log "Attempt $attempt failed (HTTP $http_code). Retrying in ${backoff}s..."
    
    sleep $backoff
    ((backoff *= 2))
    ((attempt++))
  done
  
  echo "Error: Failed to download from $url after $max_attempts attempts" >&2
  return 1
}
```

#### Enhanced Implementation

```bash
# Enhanced fetch_with_retry with better error handling and logging
fetch_with_retry() {
  local url="$1"
  local output="$2"
  local max_attempts="${3:-3}"
  local timeout="${4:-30}"
  
  local attempt=1
  local backoff=1
  
  while [[ $attempt -le $max_attempts ]]; do
    if [[ ${VERBOSE:-false} == true ]]; then
      log "Attempt $attempt/$max_attempts: Downloading $url"
    fi
    
    # Attempt download
    if curl -fsSL --max-time "$timeout" "$url" -o "$output" 2>/dev/null; then
      if [[ ${VERBOSE:-false} == true ]]; then
        log "Successfully downloaded $url"
      fi
      return 0
    fi
    
    # Get HTTP status code for diagnostics
    local http_code
    http_code=$(curl -fsSL -w "%{http_code}" -o /dev/null --max-time "$timeout" "$url" 2>/dev/null || echo "000")
    
    # Log failure
    if [[ $attempt -lt $max_attempts ]]; then
      log "Attempt $attempt failed (HTTP $http_code). Retrying in ${backoff}s..."
      sleep $backoff
      ((backoff *= 2))
    else
      log "Attempt $attempt failed (HTTP $http_code). No more retries."
    fi
    
    ((attempt++))
  done
  
  # All attempts failed - provide troubleshooting guidance
  echo "Error: Failed to download from $url after $max_attempts attempts" >&2
  echo "" >&2
  echo "Troubleshooting:" >&2
  echo "  1. Check your internet connection" >&2
  echo "  2. Verify the URL is accessible: curl -I $url" >&2
  echo "  3. Check if you're behind a proxy or firewall" >&2
  echo "  4. Try again later if the server is temporarily unavailable" >&2
  
  return 1
}
```

### 2. Caching Layer

Add optional caching for remote manifests and metadata.

#### Cache Configuration

```bash
# Cache configuration
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/agent-recommendation"
CACHE_EXPIRY_SECONDS=$((24 * 60 * 60))  # 24 hours
FORCE_REFRESH=false

# Initialize cache directory
init_cache() {
  if [[ ! -d "$CACHE_DIR" ]]; then
    mkdir -p "$CACHE_DIR" || {
      log "Warning: Failed to create cache directory: $CACHE_DIR"
      return 1
    }
  fi
  return 0
}
```

#### Cache Functions

```bash
# Get cache file path for a URL
get_cache_path() {
  local url="$1"
  local url_hash
  url_hash=$(echo -n "$url" | sha256sum | cut -d' ' -f1)
  echo "$CACHE_DIR/$url_hash"
}

# Check if cached file is fresh
is_cache_fresh() {
  local cache_file="$1"
  local expiry_seconds="${2:-$CACHE_EXPIRY_SECONDS}"
  
  if [[ ! -f "$cache_file" ]]; then
    return 1
  fi
  
  local file_age
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    file_age=$(( $(date +%s) - $(stat -f %m "$cache_file") ))
  else
    # Linux
    file_age=$(( $(date +%s) - $(stat -c %Y "$cache_file") ))
  fi
  
  [[ $file_age -lt $expiry_seconds ]]
}

# Fetch with caching support
fetch_with_cache() {
  local url="$1"
  local output="$2"
  local cache_expiry="${3:-$CACHE_EXPIRY_SECONDS}"
  
  # Skip cache if force refresh is enabled
  if [[ $FORCE_REFRESH == true ]]; then
    if [[ ${VERBOSE:-false} == true ]]; then
      log "Force refresh enabled, bypassing cache"
    fi
    fetch_with_retry "$url" "$output"
    return $?
  fi
  
  # Initialize cache
  init_cache || {
    # Cache unavailable, fetch directly
    fetch_with_retry "$url" "$output"
    return $?
  }
  
  local cache_file
  cache_file=$(get_cache_path "$url")
  
  # Check if cache is fresh
  if is_cache_fresh "$cache_file" "$cache_expiry"; then
    if [[ ${VERBOSE:-false} == true ]]; then
      log "Using cached version of $url"
    fi
    cp "$cache_file" "$output"
    return 0
  fi
  
  # Cache miss or stale - fetch and cache
  if [[ ${VERBOSE:-false} == true ]]; then
    log "Cache miss or stale, fetching $url"
  fi
  
  if fetch_with_retry "$url" "$output"; then
    # Store in cache
    cp "$output" "$cache_file"
    return 0
  fi
  
  return 1
}

# Clear cache
clear_cache() {
  if [[ -d "$CACHE_DIR" ]]; then
    log "Clearing cache: $CACHE_DIR"
    rm -rf "$CACHE_DIR"/*
  fi
}
```

### 3. Refactored Update Operations

Update all network operations to use the retry/cache layer.

#### Check Updates

```bash
# Old implementation (direct curl)
check_updates_old() {
  local -a local_agents
  mapfile -t local_agents < <(find "$AGENTS_DIR" -name "*.md" -not -name "AGENTS_REGISTRY.md" -exec basename {} .md \;)
  
  local -a updates_available=()
  
  for agent in "${local_agents[@]}"; do
    local local_file="${AGENTS_DIR}/${agent}.md"
    local remote_url="${BASE_URL}/${agent}.md"
    
    # Direct curl - no retry logic ✗
    local remote_hash=$(curl -fsSL "$remote_url" | sha256sum | cut -d' ' -f1)
    local local_hash=$(sha256sum "$local_file" | cut -d' ' -f1)
    
    if [[ "$remote_hash" != "$local_hash" ]]; then
      updates_available+=("$agent")
    fi
  done
  
  echo "${updates_available[@]}"
}

# New implementation (with retry)
check_updates() {
  local -a local_agents
  mapfile -t local_agents < <(find "$AGENTS_DIR" -name "*.md" -not -name "AGENTS_REGISTRY.md" -exec basename {} .md \;)
  
  local -a updates_available=()
  
  for agent in "${local_agents[@]}"; do
    local local_file="${AGENTS_DIR}/${agent}.md"
    local remote_url="${BASE_URL}/${agent}.md"
    local temp_file
    temp_file=$(mktemp)
    
    # Use fetch_with_cache for reliability ✓
    if fetch_with_cache "$remote_url" "$temp_file" 3600; then  # 1 hour cache
      local remote_hash
      remote_hash=$(sha256sum "$temp_file" | cut -d' ' -f1)
      local local_hash
      local_hash=$(sha256sum "$local_file" | cut -d' ' -f1)
      
      if [[ "$remote_hash" != "$local_hash" ]]; then
        updates_available+=("$agent")
      fi
      
      rm -f "$temp_file"
    else
      log "Warning: Failed to check updates for $agent"
      rm -f "$temp_file"
    fi
  done
  
  if [[ ${#updates_available[@]} -eq 0 ]]; then
    log "All agents are up to date"
  else
    log "Updates available for: ${updates_available[*]}"
  fi
  
  printf '%s\n' "${updates_available[@]}"
}
```

#### Update All Agents

```bash
# Old implementation
update_all_agents_old() {
  local -a agents_to_update
  mapfile -t agents_to_update < <(check_updates)
  
  if [[ ${#agents_to_update[@]} -eq 0 ]]; then
    return
  fi
  
  for agent in "${agents_to_update[@]}"; do
    local backup_file="${AGENTS_DIR}/${agent}.md.backup"
    cp "${AGENTS_DIR}/${agent}.md" "$backup_file"
    log "Backed up $agent to $backup_file"
    
    # Direct curl - no retry logic ✗
    local remote_url="${BASE_URL}/${agent}.md"
    curl -fsSL "$remote_url" -o "${AGENTS_DIR}/${agent}.md"
  done
}

# New implementation
update_all_agents() {
  local -a agents_to_update
  mapfile -t agents_to_update < <(check_updates)
  
  if [[ ${#agents_to_update[@]} -eq 0 ]]; then
    return 0
  fi
  
  local updated=0
  local failed=0
  
  for agent in "${agents_to_update[@]}"; do
    local agent_file="${AGENTS_DIR}/${agent}.md"
    local backup_file="${agent_file}.backup"
    local remote_url="${BASE_URL}/${agent}.md"
    
    # Create backup
    if ! cp "$agent_file" "$backup_file"; then
      log "Error: Failed to create backup for $agent"
      ((failed++))
      continue
    fi
    
    log "Updating $agent..."
    
    # Use fetch_with_retry for reliability ✓
    if fetch_with_retry "$remote_url" "$agent_file"; then
      log "✓ Updated $agent"
      ((updated++))
      
      # Remove backup on success
      rm -f "$backup_file"
    else
      log "✗ Failed to update $agent"
      ((failed++))
      
      # Restore from backup
      mv "$backup_file" "$agent_file"
      log "Restored $agent from backup"
    fi
  done
  
  log "Update complete: $updated updated, $failed failed"
  
  [[ $failed -eq 0 ]]
}
```

#### Fetch Registry

```bash
# Fetch agent registry with retry
fetch_registry() {
  local registry_url="${BASE_URL}/AGENTS_REGISTRY.md"
  local registry_file="${AGENTS_DIR}/AGENTS_REGISTRY.md"
  
  log "Fetching agent registry..."
  
  if fetch_with_cache "$registry_url" "$registry_file" 3600; then  # 1 hour cache
    log "✓ Registry updated"
    return 0
  else
    log "✗ Failed to fetch registry"
    return 1
  fi
}
```

### 4. Command-Line Flags

Add flags for cache control.

```bash
# Parse cache-related flags
parse_cache_flags() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --force-refresh)
        FORCE_REFRESH=true
        shift
        ;;
      --clear-cache)
        clear_cache
        exit 0
        ;;
      --cache-dir)
        CACHE_DIR="$2"
        shift 2
        ;;
      --cache-dir=*)
        CACHE_DIR="${1#*=}"
        shift
        ;;
      --cache-expiry)
        CACHE_EXPIRY_SECONDS="$2"
        shift 2
        ;;
      --cache-expiry=*)
        CACHE_EXPIRY_SECONDS="${1#*=}"
        shift
        ;;
      *)
        shift
        ;;
    esac
  done
}
```

## Data Models

### Cache Metadata

```bash
# Cache directory structure
$CACHE_DIR/
├── <url_hash_1>           # Cached file for URL 1
├── <url_hash_2>           # Cached file for URL 2
└── ...

# Cache metadata (file modification time used for expiry)
```

### Configuration

```bash
# Network configuration
MAX_RETRY_ATTEMPTS=3
NETWORK_TIMEOUT=30

# Cache configuration
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/agent-recommendation"
CACHE_EXPIRY_SECONDS=$((24 * 60 * 60))
FORCE_REFRESH=false
```

## Error Handling

### Network Failures

```bash
# Graceful handling of network failures
safe_network_operation() {
  local url="$1"
  local output="$2"
  local operation_name="$3"
  
  if fetch_with_retry "$url" "$output"; then
    return 0
  else
    log "Warning: $operation_name failed, continuing with cached/existing data"
    return 1
  fi
}
```

### Cache Failures

```bash
# Fallback when cache is unavailable
fetch_with_cache_fallback() {
  local url="$1"
  local output="$2"
  
  # Try with cache
  if fetch_with_cache "$url" "$output"; then
    return 0
  fi
  
  # Cache failed, try direct fetch
  log "Cache unavailable, attempting direct fetch"
  fetch_with_retry "$url" "$output"
}
```

## Testing Strategy

### Unit Tests

```bash
# tests/unit/test_fetch_with_retry.bats

@test "fetch_with_retry succeeds on first attempt" {
  # Mock successful curl
  curl() { echo "success" > "$3"; return 0; }
  export -f curl
  
  run fetch_with_retry "http://example.com/file" "output.txt"
  
  [[ $status -eq 0 ]]
  [[ -f "output.txt" ]]
}

@test "fetch_with_retry retries on failure" {
  # Mock curl that fails twice then succeeds
  attempt=0
  curl() {
    ((attempt++))
    if [[ $attempt -lt 3 ]]; then
      return 1
    fi
    echo "success" > "$3"
    return 0
  }
  export -f curl
  
  run fetch_with_retry "http://example.com/file" "output.txt"
  
  [[ $status -eq 0 ]]
  [[ $attempt -eq 3 ]]
}

@test "fetch_with_cache uses cached file when fresh" {
  init_cache
  
  local url="http://example.com/test"
  local cache_file=$(get_cache_path "$url")
  
  # Create fresh cache file
  echo "cached content" > "$cache_file"
  touch "$cache_file"
  
  fetch_with_cache "$url" "output.txt" 3600
  
  [[ "$(cat output.txt)" == "cached content" ]]
}

@test "fetch_with_cache fetches when cache is stale" {
  init_cache
  
  local url="http://example.com/test"
  local cache_file=$(get_cache_path "$url")
  
  # Create stale cache file
  echo "old content" > "$cache_file"
  touch -t 202001010000 "$cache_file"  # Set to old date
  
  # Mock fetch_with_retry
  fetch_with_retry() {
    echo "new content" > "$2"
    return 0
  }
  export -f fetch_with_retry
  
  fetch_with_cache "$url" "output.txt" 3600
  
  [[ "$(cat output.txt)" == "new content" ]]
}
```

### Integration Tests

```bash
# tests/integration/test_update_operations.bats

@test "check_updates uses retry logic" {
  # Set up test environment
  mkdir -p "$AGENTS_DIR"
  echo "old content" > "$AGENTS_DIR/test-agent.md"
  
  # Mock BASE_URL
  BASE_URL="http://example.com/agents"
  
  # Mock fetch_with_cache to return different content
  fetch_with_cache() {
    echo "new content" > "$2"
    return 0
  }
  export -f fetch_with_cache
  
  updates=$(check_updates)
  
  [[ "$updates" == "test-agent" ]]
}

@test "update_all_agents creates backups" {
  mkdir -p "$AGENTS_DIR"
  echo "original" > "$AGENTS_DIR/test-agent.md"
  
  # Mock check_updates
  check_updates() { echo "test-agent"; }
  export -f check_updates
  
  # Mock fetch_with_retry to fail
  fetch_with_retry() { return 1; }
  export -f fetch_with_retry
  
  update_all_agents
  
  # Original file should be restored
  [[ "$(cat "$AGENTS_DIR/test-agent.md")" == "original" ]]
}
```

## Performance Considerations

### Cache Hit Rate

```bash
# Track cache statistics
declare -g CACHE_HITS=0
declare -g CACHE_MISSES=0

fetch_with_cache_stats() {
  local url="$1"
  local output="$2"
  
  local cache_file=$(get_cache_path "$url")
  
  if is_cache_fresh "$cache_file"; then
    ((CACHE_HITS++))
  else
    ((CACHE_MISSES++))
  fi
  
  fetch_with_cache "$url" "$output"
}

print_cache_stats() {
  local total=$((CACHE_HITS + CACHE_MISSES))
  if [[ $total -gt 0 ]]; then
    local hit_rate=$((CACHE_HITS * 100 / total))
    log "Cache statistics: $CACHE_HITS hits, $CACHE_MISSES misses ($hit_rate% hit rate)"
  fi
}
```

## Migration Strategy

### Phase 1: Add Caching Layer

- Implement cache functions
- Add cache configuration
- Test caching independently

### Phase 2: Refactor Update Operations

- Update check_updates to use fetch_with_cache
- Update update_all_agents to use fetch_with_retry
- Add fetch_registry function

### Phase 3: Add Command-Line Flags

- Implement --force-refresh flag
- Add --clear-cache flag
- Add --cache-dir and --cache-expiry flags

### Phase 4: Testing and Validation

- Run integration tests
- Test in CI environment
- Validate offline workflow

## Documentation Updates

```markdown
# Network Operations

All network operations use automatic retry with exponential backoff.

## Retry Behavior

- **Attempts**: 3 attempts with exponential backoff (1s, 2s, 4s)
- **Timeout**: 30 seconds per attempt
- **Error Handling**: Detailed troubleshooting guidance on failure

## Caching

Update operations cache remote manifests for 24 hours by default.

### Cache Control

```bash
# Force refresh (bypass cache)
./scripts/recommend_agents.sh --check-updates --force-refresh

# Clear cache
./scripts/recommend_agents.sh --clear-cache

# Custom cache directory
./scripts/recommend_agents.sh --cache-dir=/tmp/my-cache

# Custom cache expiry (in seconds)
./scripts/recommend_agents.sh --cache-expiry=3600  # 1 hour
```

### Cache Location

Default: `$XDG_CACHE_HOME/agent-recommendation` or `~/.cache/agent-recommendation`
```
