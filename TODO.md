## Completed Enhancements

✅ **Externalize detection patterns into data files** (Completed)
Detection patterns have been moved from hardcoded shell literals into a declarative YAML file (`data/agent_patterns.yaml`). The script now loads patterns at runtime with automatic fallback to hardcoded patterns if the YAML file is unavailable. This allows contributors to update weights, add agents, or customize detection patterns without editing shell logic.

✅ **Normalize confidence scores against real pattern weights** (Completed)
Confidence calculation now dynamically computes the maximum possible weight by summing each agent's configured pattern weights, ensuring accurate percentage scores that properly reflect pattern coverage for all agents.

✅ **Reuse the retry-capable downloader for update flows** (Completed)
Update routines now use the `fetch_with_retry` function with exponential backoff, making `--check-updates` and `--update-all` resilient to transient network failures.

✅ **Surface agent "use case" metadata in outputs** (Completed)
Agent use cases from the registry are now included in verbose output, exported JSON profiles, and other user-facing outputs.

✅ **Add automated coverage for interactive selection mode** (Completed)
Comprehensive unit and integration tests have been added for the interactive selection UI, including expect-based tests for navigation, selection toggling, and key bindings.
