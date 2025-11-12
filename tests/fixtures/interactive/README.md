# Interactive Mode Test Fixtures

This directory contains test fixtures for interactive mode testing.

## Fixture Types

### Multiple Categories
- **Purpose**: Test rendering and navigation across multiple agent categories
- **Location**: `multi-category/`
- **Contains**: Agents from Infrastructure, Development, Quality, and Operations categories

### Various Confidence Levels
- **Purpose**: Test default selection behavior based on confidence thresholds
- **Location**: `confidence-levels/`
- **Contains**: Agents with confidence scores ranging from 25% to 100%

### Edge Cases
- **Purpose**: Test handling of unusual scenarios
- **Location**: `edge-cases/`
- **Contains**: 
  - Single agent scenario
  - Many agents scenario (20+)
  - All agents below threshold
  - All agents above threshold

### Default Selections
- **Purpose**: Test that agents above 50% confidence are pre-selected
- **Location**: `default-selections/`
- **Contains**: Mix of agents above and below 50% threshold

## Usage

These fixtures are used by the expect-based integration tests to verify:
- Navigation works correctly across categories
- Selection state is maintained properly
- Default selections are applied correctly
- UI renders properly with different data sets
- Edge cases are handled gracefully

## Creating New Fixtures

To create a new fixture:

1. Create a directory under `tests/fixtures/interactive/`
2. Add necessary files to trigger agent detection
3. Document the fixture purpose in this README
4. Update test scripts to use the new fixture if needed
