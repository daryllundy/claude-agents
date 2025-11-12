# Changelog

All notable changes to the Claude Code Agents project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-11-11

### Added - Agent Recommendation Script Enhancements

#### Intelligent Detection System
- **Comprehensive Pattern Detection**: Added detection patterns for all 30 agents across 9 categories
- **Cloud Provider Detection**: Enhanced detection for AWS (CloudFormation, CDK), Azure (ARM, Bicep), and GCP (Deployment Manager, App Engine)
- **Infrastructure as Code**: Improved detection for Terraform (state files, lock files, modules) and Ansible (playbooks, roles, inventory)
- **CI/CD Detection**: Added support for GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure Pipelines, and Travis CI
- **Kubernetes Detection**: Enhanced detection for Helm charts, Kustomize, and Kubernetes manifests
- **Monitoring Detection**: Added patterns for Prometheus, Grafana, ELK stack, and observability tools
- **Development Tools**: Detection for frontend frameworks (React, Vue, Angular), mobile platforms (iOS, Android, Flutter, React Native), and databases
- **Quality Tools**: Detection for testing frameworks, security tools, code review tools, and performance monitoring
- **Operations Tools**: Detection for migration tools, dependency managers, and Git workflows
- **Productivity Tools**: Detection for scaffolding tools, documentation generators, and debugging tools
- **Business Tools**: Detection for validation libraries, architecture documentation, i18n/l10n, and compliance requirements
- **Specialized Tools**: Detection for data science tools (Jupyter, pandas, scikit-learn, TensorFlow, PyTorch)

#### Confidence Scoring Engine
- **Weighted Pattern Matching**: Each detection pattern has a weight (0-25) contributing to overall confidence score
- **Percentage-Based Scoring**: Confidence scores calculated as percentage (0-100%) of matched patterns
- **Configurable Thresholds**: `--min-confidence` flag to filter recommendations (default: 25%)
- **Intelligent Sorting**: Agents sorted by confidence score in descending order
- **Recommendation Tiers**: Agents categorized as "Recommended" (50%+) or "Suggested" (25-49%)

#### DevOps Orchestrator Logic
- **Multi-Component Detection**: Automatically recommends devops-orchestrator when multiple infrastructure components detected
- **Complexity-Based Boosting**: Confidence boost when detecting:
  - Multiple IaC tools (Terraform + Ansible): +20%
  - Cloud + Terraform + Kubernetes: +30%
  - Full DevOps stack (IaC + CI/CD + K8s + Monitoring): +35%
  - 3+ infrastructure agents: +15%
- **Intelligent Coordination**: Helps users understand when orchestration is beneficial vs. direct specialist usage

#### Enhanced Output Formatting
- **Categorized Display**: Agents grouped by category (Infrastructure, Development, Quality, Operations, Productivity, Business, Specialized)
- **Visual Progress Bars**: ASCII progress bars showing confidence levels (█ for filled, ░ for empty)
- **Confidence Symbols**: ✓ for recommended (50%+), ~ for suggested (25-49%)
- **Agent Descriptions**: Display descriptions from AGENTS_REGISTRY.md
- **Matched Patterns**: Show which patterns triggered each recommendation
- **Professional Layout**: Box-drawing characters for clean, organized output
- **Legend**: Clear explanation of symbols and confidence tiers

#### Network Operations & Caching
- **Automatic Retry with Exponential Backoff**: All network operations retry up to 3 times with 1s, 2s, 4s delays
- **Intelligent Caching**: Downloaded files cached for 24 hours (configurable) to reduce network requests
- **Offline Support**: Works with cached data when network unavailable
- **HTTP Diagnostics**: Logs HTTP status codes for each attempt
- **Troubleshooting Guidance**: Detailed help provided on network failures
- **Cache Control Flags**: `--force-refresh`, `--clear-cache`, `--cache-dir`, `--cache-expiry`
- **Update Safety**: Automatic backup and rollback for update operations
- **Verbose Logging**: `--verbose` flag shows detailed network operations and cache behavior
- **Cache Location**: `$XDG_CACHE_HOME/claude-agents` or `~/.cache/claude-agents`

#### Documentation
- **Network Operations Guide**: Comprehensive documentation in `docs/NETWORK_OPERATIONS.md`
- **Retry Mechanism**: Detailed explanation of retry logic and configuration
- **Caching System**: Cache strategy, expiry, and management documentation
- **Offline Workflows**: Examples and best practices for offline usage
- **Troubleshooting**: Network failures, cache issues, and performance problems
- **Advanced Usage**: Custom retry logic, cache warming, monitoring, and team sharing
- **CI/CD Integration**: Examples for GitHub Actions, GitLab CI, and Jenkins
- **Updated README**: Added "Network Operations & Caching" section with quick reference
- **Updated GETTING_STARTED**: Added network features overview and link to detailed guide
- **Updated CLAUDE_CODE_USAGE**: Added agent recommendation script section with cache control examples

#### Interactive Selection Mode
- **Keyboard Navigation**: Arrow keys to navigate, Space to toggle, Enter to confirm
- **Pre-Selection**: Agents above 50% confidence pre-selected by default
- **Bulk Operations**: 'a' to select all, 'n' to select none, 'q' to quit
- **Category Grouping**: Agents organized by category in interactive UI
- **Live Description**: Shows agent description for currently selected item
- **Selection Counter**: Real-time count of selected agents
- **Visual Feedback**: Checkboxes [✓] for selected, [ ] for unselected, > for current position

#### Profile Export/Import
- **JSON Export**: Save detection results to JSON file with `--export <file>`
- **Profile Structure**: Includes version, timestamp, project name, detection results, and selected agents
- **Confidence Preservation**: Exports confidence scores and matched patterns for each agent
- **Cross-Project Sharing**: Import profiles in other projects with `--import <file>`
- **Validation**: Checks that agents exist in registry before importing
- **Fallback Parsing**: Works with or without `jq` installed
- **Overwrite Protection**: Requires `--force` flag to overwrite existing export files

#### Update Detection
- **Update Checking**: `--check-updates` flag to check for agent updates
- **Content Comparison**: Compares local and remote agent files to detect changes
- **Update Listing**: Shows which agents have updates available
- **Batch Updates**: `--update-all` flag to update all agents at once
- **Automatic Backups**: Creates timestamped backup directory before updating
- **Progress Display**: Shows update progress and results

#### Enhanced Error Handling
- **Network Retry Logic**: Automatic retry with exponential backoff (3 attempts, 2s → 4s → 8s)
- **HTTP Status Codes**: Displays specific HTTP error codes (404, 403, 500, etc.)
- **Troubleshooting Suggestions**: Context-specific error messages with actionable advice
- **Timeout Handling**: 30-second timeout for network requests
- **Input Validation**: Validates all command-line arguments before execution
- **Mutually Exclusive Flags**: Prevents conflicting flag combinations
- **File Path Validation**: Checks that export/import paths are valid
- **Confidence Range Validation**: Ensures --min-confidence is between 0-100

#### Verbose Mode
- **Detailed Pattern Display**: `--verbose` flag shows all patterns checked for each agent
- **Match Indicators**: ✓ for matched patterns, ✗ for unmatched patterns
- **Weight Display**: Shows weight value for each pattern
- **Pattern Types**: Clearly indicates file, path, or content patterns
- **Debugging Aid**: Helps understand why agents were or weren't recommended

#### Command-Line Interface
- **New Flags**:
  - `--interactive`: Enter interactive selection mode
  - `--min-confidence NUM`: Set confidence threshold (0-100, default: 25)
  - `--verbose`: Show detailed detection results
  - `--export FILE`: Export detection profile to JSON
  - `--import FILE`: Import and install agents from profile
  - `--check-updates`: Check for updates to installed agents
  - `--update-all`: Update all installed agents
  - `--branch NAME`: Override repository branch
  - `--repo URL`: Override repository URL
- **Existing Flags**:
  - `--dry-run`: Preview recommendations without downloading
  - `--force`: Redownload existing agents
  - `-h, --help`: Show help message

#### Agent Registry Integration
- **Metadata Parsing**: Extracts agent categories, descriptions, and use cases from AGENTS_REGISTRY.md
- **Automatic Fetching**: Downloads registry if not present locally
- **Fallback Support**: Works with built-in metadata if registry unavailable
- **Category Organization**: Uses registry categories for output grouping

### Changed

#### Script Improvements
- **Detection Accuracy**: Improved pattern matching for more accurate recommendations
- **Performance**: Optimized file scanning and pattern matching
- **Code Organization**: Refactored into modular functions for maintainability
- **Error Messages**: More helpful and actionable error messages
- **Help Text**: Updated with comprehensive documentation of all features

#### Core Agent Fallback
- **Empty Project Handling**: Recommends core agents (code-review-specialist, refactoring-specialist, test-specialist) when no technology patterns detected
- **Default Confidence**: Core agents assigned 50% confidence in empty projects

### Fixed
- **Pattern Parsing**: Improved robustness of pattern parsing with whitespace handling
- **File Detection**: More reliable file and path detection across different project structures
- **Content Search**: Better handling of special characters in content patterns
- **JSON Generation**: Proper escaping of special characters in exported profiles

### Technical Details

#### Detection Pattern Format
```
type:pattern:weight
```
- **type**: `file`, `path`, or `content`
- **pattern**: The pattern to match (filename, directory name, or content string)
- **weight**: Contribution to confidence score (0-25)

#### Confidence Calculation
```
confidence = (sum of matched pattern weights / 100) * 100
```
Capped at 100%

#### Profile JSON Schema
```json
{
  "version": "1.0",
  "generated_at": "ISO 8601 timestamp",
  "project_name": "string",
  "detection_results": {
    "agents_recommended": [
      {
        "name": "agent-name",
        "confidence": 0-100,
        "category": "category-name",
        "patterns_matched": ["pattern1", "pattern2"]
      }
    ]
  },
  "selected_agents": ["agent1", "agent2"]
}
```

## [1.0.0] - 2024-10-15

### Added
- Initial release with 31 specialized agents
- 7 Claude Code Skills for auto-discovery
- E-Commerce Orchestration System
- DevOps Orchestration System
- Basic agent recommendation script
- Comprehensive documentation

### Agent Categories
- Orchestration (1 agent)
- Infrastructure (11 agents)
- Development (3 agents)
- Quality (5 agents)
- Operations (3 agents)
- Productivity (3 agents)
- Business (4 agents)
- Specialized (1 agent)

### Skills
- e-commerce-orchestrator
- shopify-specialist
- web-design-specialist
- instagram-specialist
- tiktok-strategist
- social-media-specialist
- zapier-specialist

---

## Version History

- **2.0.0** (2024-11-11): Major enhancement to agent recommendation script with intelligent detection, confidence scoring, interactive mode, profile management, and update detection
- **1.0.0** (2024-10-15): Initial release with 31 agents, 7 skills, and orchestration systems
