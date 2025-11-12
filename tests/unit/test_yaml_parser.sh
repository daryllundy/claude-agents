#!/usr/bin/env bash
set -euo pipefail

# Extract just the YAML parser functions for testing
check_yaml_parser() {
  if command -v yq &> /dev/null; then
    echo "yq"
    return 0
  elif command -v python3 &> /dev/null; then
    # Check if PyYAML is available
    if python3 -c "import yaml" &> /dev/null; then
      echo "python3"
      return 0
    else
      echo "Error: python3 found but PyYAML module is not installed" >&2
      echo "Install with: pip3 install pyyaml" >&2
      return 1
    fi
  else
    echo "Error: No YAML parser found. Install yq or python3 with PyYAML" >&2
    echo "Install with: brew install yq  (or)  pip3 install pyyaml" >&2
    return 1
  fi
}

parse_yaml_with_yq() {
  local file="$1"
  
  if [[ ! -f "$file" ]]; then
    echo "Error: File not found: $file" >&2
    return 1
  fi
  
  if ! yq eval -o=json "$file" 2>/dev/null; then
    echo "Error: Failed to parse YAML file with yq: $file" >&2
    return 1
  fi
  
  return 0
}

parse_yaml_with_python() {
  local file="$1"
  
  if [[ ! -f "$file" ]]; then
    echo "Error: File not found: $file" >&2
    return 1
  fi
  
  python3 -c "
import yaml
import json
import sys

try:
    with open('$file', 'r') as f:
        data = yaml.safe_load(f)
        if data is None:
            print('Error: Empty or invalid YAML file', file=sys.stderr)
            sys.exit(1)
        print(json.dumps(data))
except yaml.YAMLError as e:
    print(f'Error: YAML parsing failed: {e}', file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f'Error: Failed to parse YAML file: {e}', file=sys.stderr)
    sys.exit(1)
"
  
  return $?
}

parse_yaml() {
  local file="$1"
  local parser
  
  parser=$(check_yaml_parser) || return 1
  
  case "$parser" in
    yq)
      parse_yaml_with_yq "$file"
      ;;
    python3)
      parse_yaml_with_python "$file"
      ;;
    *)
      echo "Error: Unknown parser: $parser" >&2
      return 1
      ;;
  esac
}

# Run tests
echo "=== Testing YAML Parser Functions ==="
echo ""

# Test 1: Check parser detection
echo "Test 1: Detecting available YAML parser..."
parser=$(check_yaml_parser 2>&1)
exit_code=$?
if [[ $exit_code -eq 0 ]]; then
  echo "✓ Parser detected: $parser"
else
  echo "✗ Failed to detect parser"
  echo "  Output: $parser"
  exit 1
fi
echo ""

# Test 2: Check which tools are available
echo "Test 2: Checking available tools..."
command -v yq &>/dev/null && echo "  ✓ yq: $(which yq)"
command -v python3 &>/dev/null && echo "  ✓ python3: $(which python3)"
if command -v python3 &>/dev/null; then
  if python3 -c "import yaml" 2>/dev/null; then
    echo "  ✓ PyYAML: installed"
  else
    echo "  ✗ PyYAML: not installed"
  fi
fi
echo ""

# Test 3: Parse a sample YAML file
echo "Test 3: Parsing sample YAML file..."
cat > /tmp/test_pattern.yml <<'EOF'
version: "1.0"
category: "Test"
agents:
  - name: "test-agent"
    description: "Test description"
    patterns:
      - type: "file"
        match: "*.test"
        weight: 10
EOF

json=$(parse_yaml /tmp/test_pattern.yml 2>&1)
exit_code=$?
if [[ $exit_code -eq 0 ]]; then
  echo "✓ Successfully parsed YAML to JSON"
  echo "  JSON output (first 100 chars): ${json:0:100}..."
  
  # Validate JSON structure
  if command -v jq &>/dev/null; then
    version=$(echo "$json" | jq -r '.version' 2>/dev/null)
    if [[ "$version" == "1.0" ]]; then
      echo "  ✓ JSON structure is valid (version: $version)"
    else
      echo "  ✗ JSON structure validation failed"
    fi
  fi
else
  echo "✗ Failed to parse YAML"
  echo "  Output: $json"
  exit 1
fi
echo ""

# Cleanup
rm -f /tmp/test_pattern.yml

echo "=== All tests passed! ==="
