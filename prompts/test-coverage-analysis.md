# Test Coverage Analysis Prompt

## Objective
Analyze git diff changes to determine how they impact test coverage in the codebase. Produce a numerical score from **-5 to +5** that represents the change in test coverage:
- **Negative scores (-5 to -1)**: Decreased coverage or test quality (worse)
- **Zero (0)**: No significant change in test coverage
- **Positive scores (+1 to +5)**: Increased coverage or test quality (better)

## Context
You will be provided with:
1. Git diff output showing added/removed/modified lines
2. File paths distinguishing production code from test code
3. Programming language and testing framework context

## Analysis Framework

### 1. Quantitative Test Coverage Changes

#### Test File Identification
Identify test files by:
- Naming patterns: `*_test.js`, `*.test.ts`, `*_spec.rb`, `test_*.py`, `*Test.java`
- Directory patterns: `/test/`, `/tests/`, `/__tests__/`, `/spec/`
- Framework-specific patterns: `*.spec.tsx`, `*.cy.js` (Cypress)

#### Lines of Code Ratio
Calculate the test-to-production code ratio change:
- **Count added/removed lines in production code**
- **Count added/removed lines in test code**
- **Compare ratio before and after**

**Scoring guidance:**
- Test lines added > production lines added: +1 to +3 points (based on ratio)
- Production code added without corresponding tests: -1 to -3 points
- Tests removed while production code remains: -2 points
- Dead test code removed (for deleted features): 0 points (neutral)

### 2. Test Coverage Breadth

#### New Functionality Testing
Analyze if new features are tested:
- **New functions/methods without tests**: Major red flag
- **New API endpoints without integration tests**: -2 points
- **New UI components without component tests**: -1.5 points
- **New business logic with comprehensive tests**: +2 points

**Scoring guidance:**
- New public function with tests: +1 point
- New public function without tests: -1.5 points
- New complex logic (loops, conditionals) without tests: -2 points
- New error handling paths tested: +1 point

### 3. Test Coverage Depth

#### Test Quality Indicators
Evaluate the thoroughness of tests:

**Positive indicators (+):**
- Edge case testing (boundary values, null, empty)
- Error/exception handling tests
- Integration/end-to-end tests added
- Parameterized/property-based tests
- Mock/stub usage showing isolation
- Assertion variety (not just truthy checks)

**Negative indicators (-):**
- Trivial tests (testing getters/setters only)
- Tests without assertions
- Commented-out tests
- Skipped/ignored tests introduced
- Tests that only verify happy path

**Scoring guidance:**
- Comprehensive test suite for new feature: +3 points
- Edge cases and error scenarios covered: +1.5 points
- Only happy-path tests: +0.5 points
- Trivial or meaningless tests: 0 points
- Skipped tests introduced: -1 point per skip
- Tests without meaningful assertions: -0.5 points

### 4. Test Maintenance and Quality

#### Test Code Changes
Evaluate modifications to existing tests:
- **Fixed broken tests**: +1 point (improves reliability)
- **Tests disabled/commented out**: -2 points
- **Flaky test fixes** (removed sleeps, better waits): +1.5 points
- **Test refactoring** (DRY, helper functions): +0.5 points
- **Increased test timeout** (potential flakiness): -0.5 points

**Scoring guidance:**
- Improved test readability/maintainability: +0.5 points
- Test helper/utility functions added: +1 point
- Reduced test duplication: +0.5 points
- Tests made more brittle (tight coupling to implementation): -1 point

### 5. Test Types and Pyramid Balance

#### Test Category Distribution
Consider the testing pyramid (unit → integration → e2e):

**Ideal additions (+):**
- Many unit tests for new logic
- Some integration tests for module interaction
- Few e2e tests for critical user flows

**Problematic patterns (-):**
- Only e2e tests for new features (slow, brittle)
- No integration tests for complex interactions
- Missing unit tests for algorithmic code

**Scoring guidance:**
- Balanced test pyramid additions: +2 points
- Only unit tests for complex integration: -1 point
- Only e2e tests without unit coverage: -1.5 points
- New integration tests for APIs/services: +1.5 points

### 6. Coverage Regression Detection

#### Code Modification Without Test Updates
Critical warning signs:
- **Business logic modified without test changes**: -3 points
- **Function signature changed without test updates**: -2 points
- **New parameters/fields untested**: -1 point
- **Tests updated to match new behavior**: +1 point

**Scoring guidance:**
- Production code change with proportional test updates: +1 point
- Production code change with no test updates: -2 to -3 points
- Refactoring with tests maintained/improved: +0.5 points
- Breaking changes with comprehensive test coverage: +1 point

### 7. Framework and Tooling Improvements

#### Testing Infrastructure
Changes that improve testing capability:
- **New testing libraries/frameworks**: +1 point
- **Code coverage tooling added**: +1.5 points
- **CI/CD test automation**: +2 points
- **Test data factories/fixtures**: +1 point
- **Mocking/stubbing infrastructure**: +0.5 points

**Scoring guidance:**
- Better test setup/teardown utilities: +0.5 points
- Test database/environment improvements: +1 point
- Removed outdated testing dependencies: +0.5 points

## Analysis Process

### Step 1: Categorize Files
Separate diff into:
- Production code files
- Test code files
- Configuration/tooling files

### Step 2: Calculate Basic Metrics
- Lines added/removed in production code
- Lines added/removed in test code
- New functions/classes in production
- New tests added
- Tests removed or disabled

### Step 3: Assess Test Quality
For each new/modified test:
- What does it test?
- Does it have meaningful assertions?
- Does it cover edge cases?
- Is it well-structured and maintainable?

### Step 4: Identify Coverage Gaps
For each production change:
- Is there a corresponding test change?
- Are new code paths tested?
- Are error cases covered?

### Step 5: Apply Scoring Rubric
- Sum scores from all categories
- Weight based on change magnitude
- Consider overall impact on test suite health

### Step 6: Normalize to -5 to +5 Scale
- Cap at -5 (minimum)
- Cap at +5 (maximum)
- Round to nearest 0.5

### Step 7: Provide Justification
Include specific evidence:
- Ratio of test to production code changes
- Number of new tests vs. new functionality
- Test quality observations
- Coverage gaps identified

## Example Analysis Output

```json
{
  "score": 3.5,
  "reasoning": "Added 45 lines of production code with 120 lines of comprehensive tests (2.7:1 ratio). New UserValidator class has 8 unit tests covering edge cases and error scenarios. Added integration tests for API endpoints. All tests include meaningful assertions and error case handling.",
  "key_factors": [
    "Excellent test-to-code ratio (2.7:1)",
    "8 new unit tests with edge case coverage",
    "3 integration tests for API endpoints",
    "Error handling comprehensively tested"
  ],
  "metrics": {
    "production_lines_added": 45,
    "test_lines_added": 120,
    "new_test_files": 1,
    "new_test_cases": 11,
    "edge_cases_covered": true
  }
}
```

## Example of Poor Coverage

```json
{
  "score": -3.0,
  "reasoning": "Added 200 lines of complex authentication logic without any tests. Modified existing token validation function but did not update tests. Two existing tests were commented out. Critical security-related code is untested.",
  "key_factors": [
    "200 lines of production code added with 0 tests",
    "Complex authentication logic untested",
    "2 existing tests disabled",
    "Security-critical code without coverage"
  ],
  "metrics": {
    "production_lines_added": 200,
    "test_lines_added": 0,
    "tests_disabled": 2,
    "coverage_gaps": ["authentication flow", "token validation", "error handling"]
  }
}
```

## Important Considerations

1. **Context of changes**: Refactoring may not need new tests if existing tests cover behavior
2. **Language conventions**: Different languages have different test patterns
3. **Test quality > quantity**: 10 meaningful tests beat 100 trivial tests
4. **Coverage percentage**: If available from tools, use it to inform scoring
5. **Feature type**: UI changes might legitimately have different test ratios than backend logic
6. **Legacy code**: Adding tests to previously untested code is highly positive

## Common Patterns

### High Positive Score (+4 to +5)
- New feature with comprehensive test suite
- Major test infrastructure improvements
- Fixing significant coverage gaps
- Adding integration test coverage

### Moderate Positive Score (+1 to +3)
- Good test coverage for new code
- Test improvements and refactoring
- Reasonable test-to-code ratio

### Neutral Score (0)
- Removing dead code and its tests
- Test-only refactoring
- Minor test adjustments

### Moderate Negative Score (-1 to -3)
- New code with insufficient tests
- Tests disabled without good reason
- Production changes without test updates

### High Negative Score (-4 to -5)
- Complex critical code without any tests
- Mass disabling of tests
- Large production changes with zero test updates
- Security/safety-critical code untested

## Final Output Format

Return a JSON object with:
```json
{
  "dimension": "test_coverage",
  "score": <number between -5 and +5>,
  "reasoning": "<concise explanation>",
  "key_factors": ["<factor 1>", "<factor 2>", "..."],
  "metrics": {
    "production_lines_added": <number>,
    "production_lines_removed": <number>,
    "test_lines_added": <number>,
    "test_lines_removed": <number>,
    "new_test_cases_estimated": <number>
  },
  "confidence": "<high|medium|low>"
}
```

**The score is the most critical output** - it should accurately reflect whether test coverage improved or degraded with this change.
