# Code Readability Analysis Prompt

## Objective
Analyze git diff changes to determine how they impact code readability and clarity. Produce a numerical score from **-5 to +5** that represents the change:
- **Negative scores (-5 to -1)**: Decreased readability (harder to understand)
- **Zero (0)**: No significant change in readability
- **Positive scores (+1 to +5)**: Increased readability (easier to understand)

## Philosophy

**Readable code is code that can be understood quickly and correctly by developers.**

Good readability means:
- Clear, descriptive names that reveal intent
- Simple, focused functions that do one thing
- Logical flow that's easy to follow
- Minimal cognitive overhead
- Self-documenting code structure

Poor readability means:
- Cryptic, abbreviated, or misleading names
- Complex, tangled logic
- Unclear flow and sequencing
- High cognitive load
- Code requiring extensive comments to understand

## Context
You will be provided with:
1. Git diff output showing added/removed/modified lines
2. File paths and code structure
3. Programming language context

## Analysis Framework

### 1. Naming Quality

#### Variable Names
Evaluate variable name clarity:
- **Descriptive names**: `userEmail` vs `ue` vs `x`
- **Intent-revealing**: `isAuthenticated` vs `flag` vs `b`
- **Appropriate length**: Not too short, not too long
- **Meaningful context**: `customerOrderCount` vs `count`

**Scoring guidance:**
- Clear, descriptive names replacing cryptic ones: +1 point
- Cryptic abbreviations replacing clear names: -1 point
- Single-letter variables in non-trivial scope: -0.5 points
- Well-named variables in new code: +0.5 points
- Generic names (data, info, value, temp): -0.3 points each

#### Function Names
Evaluate function name quality:
- **Verb-based for actions**: `calculateTotal()` vs `total()`
- **Clear purpose**: `validateUserCredentials()` vs `check()`
- **Accurate description**: Name matches what it does
- **Appropriate specificity**: Not too generic, not over-specific

**Scoring guidance:**
- Clear, action-oriented function names: +0.5 points each
- Vague function names (do, handle, process, manage): -0.5 points each
- Misleading names (name doesn't match behavior): -1 point
- Renamed for clarity: +0.8 points

#### Type and Class Names
Evaluate type name clarity:
- **Noun-based**: `UserAccount` vs `UserData` vs `Info`
- **Domain-appropriate**: Business language vs technical jargon
- **Precise**: `EmailAddress` vs `String`
- **Unambiguous**: Clear what it represents

**Scoring guidance:**
- Clear domain type names: +0.5 points
- Generic suffixes (Data, Info, Object): -0.3 points
- Precise type names replacing generic ones: +1 point
- Vague type names: -0.5 points

### 2. Function Clarity

#### Function Size and Focus
Evaluate function complexity:
- **Lines of code**: Shorter functions generally more readable
- **Single responsibility**: Does one thing well
- **Cyclomatic complexity**: Fewer branches = simpler
- **Nesting depth**: Shallow nesting easier to follow

**Scoring guidance:**
- Long function (50+ lines) broken into smaller ones: +1.5 points
- Small, focused function extracted: +1 point
- Function doing too many things: -1 point
- Deep nesting (4+ levels) introduced: -1 point
- Deep nesting reduced: +1 point

#### Function Purity
Evaluate side effects and dependencies:
- **Pure functions**: Same input → same output, no side effects
- **Explicit dependencies**: Parameters vs hidden global state
- **Predictable behavior**: Easy to reason about
- **Testability**: Pure functions easier to test

**Scoring guidance:**
- New pure function: +0.5 points
- Function made pure (removed side effects): +1 point
- Side effects added to previously pure function: -1 point
- Hidden dependencies on global state: -0.8 points
- Explicit parameters replacing globals: +0.8 points

#### Function Sequencing
Evaluate logical flow:
- **Natural order**: Steps follow logical progression
- **Clear dependencies**: Why steps happen in this order
- **Minimal jumping**: Sequential reading vs jumping around
- **Coherent narrative**: Code tells a story

**Scoring guidance:**
- Improved logical flow: +1 point
- Reordered for clarity: +0.5 points
- Confusing sequence: -0.8 points
- Non-obvious ordering requiring comments: -0.5 points

### 3. Code Structure

#### Control Flow Clarity
Evaluate branching and loops:
- **Guard clauses**: Early returns vs deep nesting
- **Clear conditions**: Readable boolean expressions
- **Appropriate constructs**: Right tool for the job
- **Avoid clever tricks**: Straightforward over concise

**Scoring guidance:**
- Guard clauses reducing nesting: +1 point
- Clear if/else replacing ternary chains: +0.5 points
- Complex boolean expressions: -0.8 points
- Clever one-liners replacing clear code: -1 point
- Confusing control flow: -1.5 points

#### Error Handling
Evaluate error handling readability:
- **Clear error cases**: Explicit error handling
- **Meaningful error messages**: Descriptive errors
- **Appropriate level**: Not too granular, not too coarse
- **Obvious recovery**: Clear what happens on error

**Scoring guidance:**
- Clear error handling added: +0.5 points
- Meaningful error messages: +0.3 points
- Silent failures or generic errors: -0.8 points
- Confusing error handling: -0.5 points

### 4. Comments and Documentation

#### Comment Quality
Evaluate comment usefulness:
- **Why over what**: Explain reasoning, not obvious actions
- **Necessary comments**: Complex logic that needs explanation
- **Outdated comments**: Comments contradicting code
- **Self-documenting code**: Code so clear it needs no comments

**Scoring guidance:**
- Code made clear enough to remove comments: +1 point
- Helpful "why" comments added: +0.3 points
- Commented-out code added: -0.5 points
- Comments explaining obvious code: -0.3 points
- Outdated/wrong comments: -1 point

#### Documentation
Evaluate function/class documentation:
- **Clear purpose**: What it does
- **Parameters explained**: Expected inputs
- **Return value explained**: What it returns
- **Examples**: Usage examples where helpful

**Scoring guidance:**
- Good documentation added: +0.5 points
- Missing documentation for public API: -0.5 points
- Improved documentation: +0.3 points

### 5. Code Patterns and Idioms

#### Language Idioms
Evaluate idiomatic usage:
- **Idiomatic code**: Language-appropriate patterns
- **Modern features**: Using current best practices
- **Readable constructs**: Clear over clever
- **Standard patterns**: Familiar vs unusual

**Scoring guidance:**
- Idiomatic code replacing non-idiomatic: +1 point
- Modern, clear constructs: +0.5 points
- Unusual or obscure patterns: -0.8 points
- Fighting language idioms: -1 point

#### Consistency
Evaluate code consistency:
- **Naming conventions**: Consistent style
- **Formatting**: Uniform indentation, spacing
- **Patterns**: Similar problems solved similarly
- **Style adherence**: Following project conventions

**Scoring guidance:**
- Improved consistency: +0.5 points
- Inconsistent naming/style: -0.5 points
- Mixed conventions: -0.8 points

### 6. Complexity and Cognitive Load

#### Mental Model
Evaluate cognitive overhead:
- **Concepts to track**: How many things to remember
- **State mutations**: Tracking state changes
- **Indirection levels**: Layers to trace through
- **Surprises**: Unexpected behavior

**Scoring guidance:**
- Reduced mental juggling: +1 point
- Explicit state changes: +0.5 points
- Hidden state mutations: -1 point
- Surprising behavior: -0.8 points
- Reduced indirection: +0.8 points

#### Code Duplication
Evaluate repetition impact:
- **Obvious duplication**: Repeated code blocks
- **Slight variations**: Almost identical code
- **DRY violations**: Should be abstracted
- **Intentional duplication**: Sometimes clearer than abstraction

**Scoring guidance:**
- Duplication removed improving clarity: +1 point
- Duplication removed hurting clarity: -0.5 points
- New obvious duplication: -0.8 points
- Intentional duplication for clarity: +0.3 points

### 7. Overall Code Organization

#### File Organization
Evaluate structure:
- **Logical grouping**: Related code together
- **Clear sections**: Organized into coherent parts
- **Import organization**: Clean, organized imports
- **File size**: Not too large to navigate

**Scoring guidance:**
- Improved organization: +0.5 points
- Clear sections/grouping: +0.3 points
- Messy organization: -0.5 points
- Huge files with poor organization: -1 point

## Analysis Process

### Step 1: Evaluate Naming
Review all new/changed names:
- Are they descriptive?
- Do they reveal intent?
- Are they consistent?
- Could they be clearer?

### Step 2: Assess Function Quality
For each new/modified function:
- Is it focused and simple?
- Is the logic clear?
- Is it pure or has side effects?
- Is the flow easy to follow?

### Step 3: Examine Structure
Look at overall code structure:
- Is control flow clear?
- Are there unnecessary complexities?
- Is error handling obvious?
- Is organization logical?

### Step 4: Consider Cognitive Load
Evaluate mental overhead:
- How hard is this to understand?
- How much do you need to track?
- Are there surprises?
- Is it predictable?

### Step 5: Apply Scoring Rubric
- Sum improvements (positive points)
- Sum degradations (negative points)
- Weight by impact on readability
- Consider overall effect

### Step 6: Normalize to -5 to +5 Scale
- Cap at -5 (minimum)
- Cap at +5 (maximum)
- Round to nearest 0.5

### Step 7: Provide Justification
Include specific examples:
- Which names improved/worsened?
- Which functions became clearer/muddier?
- What structural changes affected readability?
- Overall readability impact

## Example Analysis Output

```json
{
  "score": 3.5,
  "reasoning": "Significantly improved readability through better naming and function extraction. Renamed variables from single letters (x, y, n) to descriptive names (userId, emailAddress, itemCount). Extracted complex validation logic into well-named helper functions (isValidEmail, hasRequiredPermissions). Reduced nesting depth from 4 to 2 levels using guard clauses.",
  "key_factors": [
    "12 variables renamed from cryptic to descriptive",
    "3 functions extracted with clear names",
    "Reduced nesting depth with guard clauses",
    "Improved boolean expression clarity"
  ]
}
```

## Example of Poor Readability

```json
{
  "score": -3.0,
  "reasoning": "Readability degraded through unclear naming and increased complexity. Renamed descriptive variables to single letters (user → u, order → o). Inlined several focused functions into one 120-line function with deep nesting. Added cryptic boolean expressions and removed helpful comments. Increased cyclomatic complexity from 8 to 25.",
  "key_factors": [
    "Cryptic single-letter variables introduced",
    "Multiple functions combined into 120-line monster",
    "Deep nesting (5 levels) with complex conditions",
    "Helpful comments removed",
    "Cyclomatic complexity increased 3x"
  ]
}
```

## Important Considerations

1. **Context matters**: Domain complexity affects readability standards
2. **Audience**: Consider team experience and conventions
3. **Language idioms**: What's readable varies by language
4. **Balance**: Sometimes brevity aids readability, sometimes it hurts
5. **Subjectivity**: Readability has subjective elements, but principles apply

## Common Patterns

### High Positive Score (+4 to +5)
- Major refactoring improving clarity throughout
- Renaming many unclear names to clear ones
- Breaking complex functions into simple, well-named pieces
- Significant reduction in cognitive overhead

### Moderate Positive Score (+1 to +3)
- Some improved naming
- Function extraction improving clarity
- Reduced nesting or complexity
- Better code organization

### Neutral Score (0)
- Code moves but readability unchanged
- Equivalent trade-offs
- Minor changes with no clear impact

### Moderate Negative Score (-1 to -3)
- Some unclear naming introduced
- Increased complexity or nesting
- Confusing logic added
- Poor code organization

### High Negative Score (-4 to -5)
- Widespread unclear naming
- Massive complex functions
- Deeply nested, hard-to-follow logic
- Code obfuscation or "clever" tricks

## Final Output Format

Return a JSON object with:
```json
{
  "dimension": "readability",
  "score": <number between -5 and +5>,
  "reasoning": "<concise explanation>",
  "key_factors": ["<factor 1>", "<factor 2>", "..."],
  "confidence": "<high|medium|low>"
}
```

**The score is the most critical output** - it should reflect whether the change makes code easier or harder to understand.
