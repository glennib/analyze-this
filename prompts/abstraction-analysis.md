# Abstraction and Concept Analysis Prompt

## Objective
Analyze git diff changes to determine how they impact the number and quality of abstractions and concepts in the codebase. Produce a numerical score from **-5 to +5** that represents the change:
- **Negative scores (-5 to -1)**: Harmful changes (over-abstraction, unnecessary complexity, or concept bloat)
- **Zero (0)**: No significant change in abstraction level
- **Positive scores (+1 to +5)**: Beneficial changes (appropriate abstractions, concept clarity, reduced complexity)

## Context
You will be provided with:
1. Git diff output showing added/removed/modified lines
2. File paths and code structure
3. Programming language context

## Core Philosophy

**Good abstractions:**
- Solve real, recurring problems
- Hide complexity appropriately
- Have clear, focused responsibilities
- Make code more maintainable and understandable
- Follow the "Rule of Three" (abstract after 3rd duplication)

**Bad abstractions:**
- Premature optimization (abstracting before patterns emerge)
- Over-engineering (excessive layers, frameworks within frameworks)
- Leaky abstractions (implementation details bleeding through)
- Wrong abstractions (forced patterns that don't fit)

## Analysis Framework

### 1. New Concepts and Abstractions

#### Classes, Interfaces, Types
Count and evaluate:
- **New classes/interfaces**: Are they justified?
- **New type definitions**: Do they clarify or complicate?
- **Abstract classes/base classes**: Appropriate inheritance?
- **Traits/mixins/protocols**: Proper composition?

**Scoring guidance:**
- Well-named, focused class with clear responsibility: +1 point
- Appropriate interface/protocol defining contract: +1.5 points
- Abstract base class solving genuine duplication: +1 point
- Premature abstraction (only 1-2 uses): -2 points
- God class (too many responsibilities): -2 points
- Unnecessary wrapper class: -1 point
- Type alias improving clarity: +0.5 points

#### Functions and Methods
Evaluate new/modified functions:
- **Pure functions** (no side effects): Generally positive
- **Well-named functions** extracting complex logic: +1 point
- **Single responsibility**: Clear, focused purpose
- **Helper/utility functions**: Reduce duplication

**Scoring guidance:**
- Function extracting duplicated code (3+ occurrences): +1.5 points
- Function extracting complex logic with clear name: +1 point
- Premature function extraction (no duplication): -0.5 points
- Function doing too many things: -1 point
- Well-named helper functions: +0.5 points
- Cryptic or overly generic function names: -0.5 points

### 2. Design Patterns

#### Pattern Introduction
Identify design patterns added:
- **Strategy pattern**: Multiple algorithms/behaviors
- **Factory pattern**: Object creation abstraction
- **Observer pattern**: Event/subscription systems
- **Decorator/Adapter patterns**: Interface compatibility
- **Repository pattern**: Data access abstraction
- **Dependency Injection**: Loose coupling

**Scoring guidance:**
- Appropriate pattern for recurring problem: +2 points
- Pattern solving real complexity: +1.5 points
- Pattern making code more testable: +1 point
- Over-engineered pattern for simple case: -2 points
- Pattern cargo-culting (blindly applying): -2 points
- Wrong pattern for the problem: -1.5 points

#### Anti-Pattern Detection
Watch for problematic patterns:
- **Singleton abuse**: Global state
- **God objects**: Too many responsibilities
- **Yo-yo problem**: Too many inheritance layers
- **Circular dependencies**: Design smell
- **Feature envy**: Method accessing other object's data

**Scoring guidance:**
- Removed singleton/global state: +2 points
- Introduced singleton unnecessarily: -2 points
- Broke up god class: +2 points
- Created god class: -3 points
- Simplified inheritance hierarchy: +1.5 points
- Added excessive inheritance: -2 points

### 3. Conceptual Complexity

#### Cognitive Load Assessment
Evaluate understandability:
- **Cyclomatic complexity**: Branches and paths
- **Nesting levels**: Deep nesting is harder to understand
- **Function length**: Shorter is generally better
- **Parameter count**: Fewer parameters = simpler
- **Boolean parameters**: Often indicate missing abstraction

**Scoring guidance:**
- Reduced cyclomatic complexity: +1 point per significant reduction
- Increased complexity without abstraction: -1 point
- Extracted complex nested logic: +1.5 points
- Added deep nesting (4+ levels): -1 point
- Reduced function parameters (simplified interface): +0.5 points
- Added many parameters (complex interface): -0.5 points
- Replaced boolean parameters with strategy/enum: +1 point

#### Duplication vs. Abstraction
Assess code duplication changes:
- **Duplication removed** through abstraction: Positive
- **Premature abstraction** (not yet duplicated): Negative
- **Inline duplication** (removed abstraction): Context-dependent

**Scoring guidance:**
- Abstracted genuinely duplicated code (3+ places): +2 points
- Abstracted code with only 2 occurrences: +0.5 points
- Premature abstraction (1 use): -1.5 points
- Removed harmful abstraction (inlined): +1 point
- Removed useful abstraction: -2 points

### 4. Domain Modeling

#### Concept Clarity
Evaluate domain representation:
- **Value objects**: Encapsulating domain concepts
- **Entities**: Clear identity and lifecycle
- **Domain services**: Business logic organization
- **Ubiquitous language**: Domain terms in code

**Scoring guidance:**
- Introduced clear domain concept (value object): +1.5 points
- Named classes/types using domain language: +1 point
- Improved domain model clarity: +2 points
- Generic/technical names replacing domain terms: -1 point
- Confused domain concepts: -1.5 points

#### Boundaries and Layers
Assess architectural abstractions:
- **Layer separation** (UI/Business/Data): Clear boundaries
- **Module boundaries**: Well-defined interfaces
- **API abstractions**: Internal vs. external
- **Ports and adapters**: Hexagonal architecture

**Scoring guidance:**
- Clear layer/boundary introduced: +2 points
- Improved separation of concerns: +1.5 points
- Blurred boundaries: -2 points
- Violated layering: -2 points

### 5. Abstraction Removal

#### Simplification
Sometimes removing abstraction is positive:
- **Dead code removal**: Unused abstractions
- **YAGNI violations fixed**: Speculative features removed
- **Over-engineering corrected**: Simplified to needs
- **Inline simple abstractions**: One-liner wrappers removed

**Scoring guidance:**
- Removed unused abstraction: +1 point
- Removed premature abstraction: +1.5 points
- Simplified over-engineered code: +2 points
- Removed necessary abstraction: -2 points
- Created duplication by removing abstraction: -1 point

### 6. Configuration and Flexibility

#### Appropriate Generalization
Evaluate flexibility additions:
- **Configuration options**: Hardcoded → configurable
- **Generic implementations**: Type parameters, generics
- **Plugin systems**: Extensibility points
- **Feature flags**: Runtime behavior control

**Scoring guidance:**
- Useful configuration abstraction: +1 point
- Over-generalized (YAGNI): -1.5 points
- Generic type improving reusability: +1 point
- Unnecessary generic wrapper: -1 point
- Plugin system for genuine extensions: +2 points
- Premature plugin architecture: -2 points

### 7. Language-Specific Idioms

#### Idiomatic Abstractions
Consider language conventions:
- **Iterators/generators** (Python, JavaScript)
- **Traits/impl blocks** (Rust)
- **Higher-order functions** (functional languages)
- **Decorators/annotations** (Python, Java)
- **Extension methods** (C#, Kotlin)

**Scoring guidance:**
- Idiomatic abstraction for the language: +1 point
- Fighting language idioms: -1 point
- Appropriate use of language features: +0.5 points

## Analysis Process

### Step 1: Identify Structural Changes
Parse diff for:
- New classes, interfaces, types
- New functions, methods
- Modified signatures
- Deleted abstractions
- Renamed concepts

### Step 2: Categorize Changes
For each change, determine:
- Is it adding abstraction?
- Is it removing abstraction?
- Is it refining/improving abstraction?
- Is it introducing a pattern?
- Is it simplifying complexity?

### Step 3: Assess Appropriateness
For each abstraction change:
- Is it solving a real problem?
- Does it have 3+ use cases (Rule of Three)?
- Does it make code more understandable?
- Does it reduce or increase cognitive load?
- Is it premature or over-engineered?

### Step 4: Evaluate Naming and Clarity
- Are names clear and domain-appropriate?
- Do abstractions hide the right details?
- Are interfaces clean and focused?

### Step 5: Calculate Complexity Impact
- Did cyclomatic complexity increase/decrease?
- Are there more or fewer concepts to understand?
- Is the overall architecture clearer?

### Step 6: Apply Scoring Rubric
- Sum individual scores
- Weight by impact and scope
- Consider net effect on maintainability

### Step 7: Normalize to -5 to +5 Scale
- Cap at -5 (minimum)
- Cap at +5 (maximum)
- Round to nearest 0.5

### Step 8: Provide Justification
Include specific examples:
- What abstractions were added/removed?
- Why are they appropriate or problematic?
- Impact on code clarity and maintainability

## Example Analysis Output

```json
{
  "score": 2.5,
  "reasoning": "Introduced UserAuthentication strategy pattern to handle 3 different auth methods (OAuth, JWT, API key), replacing duplicated code across 5 files. Created clear AuthStrategy interface and 3 implementations. Extracted complex token validation into separate function. Overall, reduced complexity through appropriate abstraction.",
  "key_factors": [
    "Strategy pattern solves genuine duplication (5 locations)",
    "Clear interface with 3 concrete implementations",
    "Extracted complex validation logic with clear name",
    "Improved testability through dependency injection"
  ],
  "abstraction_changes": {
    "added": ["AuthStrategy interface", "OAuthStrategy class", "JWTStrategy class", "APIKeyStrategy class", "validateToken function"],
    "removed": ["duplicated auth code in 5 files"],
    "complexity_change": -15
  }
}
```

## Example of Over-Abstraction

```json
{
  "score": -3.5,
  "reasoning": "Added AbstractFactoryProviderBuilder with 4 inheritance levels for simple object creation used in only one place. Introduced generic DataProcessor<T, R, E> wrapper around basic transform function. Created unnecessary IUserServiceFactoryInterface for single implementation. Over-engineered for current needs.",
  "key_factors": [
    "4-level inheritance hierarchy for single use case",
    "Premature abstraction with no duplication",
    "Generic wrapper adding complexity without benefit",
    "Interface with only one implementation",
    "Names suggest over-thinking (AbstractFactoryProviderBuilder)"
  ],
  "abstraction_changes": {
    "added": ["AbstractFactoryProviderBuilder", "DataProcessor<T,R,E> generic", "IUserServiceFactoryInterface", "3 intermediate abstract classes"],
    "removed": [],
    "complexity_change": +25
  }
}
```

## Important Considerations

1. **Context is critical**: An abstraction might be premature now but correct in larger context
2. **Rule of Three**: Generally don't abstract until pattern appears 3 times
3. **Locality of behavior**: Good abstractions keep related code together
4. **Wrong abstraction**: Worse than duplication; harder to fix later
5. **Team size and skill**: More abstractions may be appropriate for larger, experienced teams
6. **Domain complexity**: Complex domains benefit from rich domain models

## Common Patterns

### High Positive Score (+4 to +5)
- Major refactoring removing duplication through clear abstractions
- Appropriate design pattern solving recurring problem
- Clear domain modeling improving code clarity
- Significant complexity reduction through good abstractions

### Moderate Positive Score (+1 to +3)
- Extracting duplicated code into functions
- Adding clear interfaces for existing implementations
- Introducing helpful value objects/types
- Simplifying overly complex code

### Neutral Score (0)
- Renaming without structural change
- Minor refactoring with no abstraction change
- Equivalent complexity trade-offs

### Moderate Negative Score (-1 to -3)
- Premature abstraction (before duplication exists)
- Unnecessary wrapper classes
- Over-generic implementations
- Confusing or misnamed abstractions

### High Negative Score (-4 to -5)
- Significant over-engineering
- Multiple layers of unnecessary abstraction
- Wrong abstraction making code harder to understand
- Enterprise FizzBuzz-style complexity

## Red Flags for Over-Abstraction

- Abstract/Base/Factory/Provider/Manager in every name
- Interfaces with single implementation
- Generic types with complex parameter lists
- Deep inheritance hierarchies (4+ levels)
- Many files with <10 lines of code
- Builder pattern for simple objects
- Visitor pattern for non-polymorphic operations

## Green Flags for Good Abstraction

- Clear, domain-driven names
- Single, focused responsibility
- Abstracts recurring pattern (3+ occurrences)
- Reduces cyclomatic complexity
- Improves testability
- Follows language idioms
- Makes code more readable

## Final Output Format

Return a JSON object with:
```json
{
  "dimension": "abstraction",
  "score": <number between -5 and +5>,
  "reasoning": "<concise explanation>",
  "key_factors": ["<factor 1>", "<factor 2>", "..."],
  "abstraction_changes": {
    "added": ["<new abstraction 1>", "<new abstraction 2>"],
    "removed": ["<removed abstraction 1>"],
    "refined": ["<improved abstraction 1>"],
    "complexity_change": <estimated cyclomatic complexity change>
  },
  "confidence": "<high|medium|low>"
}
```

**The score is the most critical output** - it should reflect whether the abstractions added/removed make the codebase more or less maintainable and understandable.
