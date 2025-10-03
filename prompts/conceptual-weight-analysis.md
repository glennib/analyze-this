# Conceptual Weight Analysis Prompt

## Objective
Analyze git diff changes to determine how they impact the number of distinct concepts, abstractions, and entities that developers must understand. Produce a numerical score from **-5 to +5** that represents the change:
- **Negative scores (-5 to -1)**: More concepts added (increased cognitive load, concept bloat)
- **Zero (0)**: No significant change in number of concepts
- **Positive scores (+1 to +5)**: Concepts removed or consolidated (reduced cognitive load)

## Philosophy

**The principle: Fewer concepts = Better code**

Every new class, type, interface, function, module, or abstraction adds to the mental model developers must maintain. While some abstractions reduce complexity, every abstraction itself is a concept to learn and remember.

Conceptual weight measures the **quantity** of things to understand, not their quality (that's covered by the abstraction dimension). This dimension rewards simplification and consolidation.

## Context
You will be provided with:
1. Git diff output showing added/removed/modified lines
2. File paths and code structure
3. Programming language context

## Analysis Framework

### 1. New Named Entities

Count distinct new names introduced:

#### Classes and Types
- **New classes**: Each class is a concept
- **New interfaces/protocols**: Each interface definition
- **New type aliases**: Each named type
- **New enums**: Each enumeration type
- **New structs**: Each structure definition

**Scoring guidance:**
- Each new class/interface/type: -0.5 points
- Each removed class/interface/type: +0.5 points
- Consolidating 2+ types into one: +1 point
- Splitting one type into many: -1 point

#### Functions and Methods
- **New top-level functions**: Each named function
- **New public methods**: Methods in public API
- **New exported functions**: Functions visible to other modules

**Scoring guidance:**
- Each new exported/public function: -0.3 points
- Each removed exported/public function: +0.3 points
- Consolidating multiple functions into one: +0.5 points
- Private/internal functions: -0.1 points each

#### Variables and Constants
- **New global/module variables**: Shared state concepts
- **New exported constants**: Named constant values
- **New configuration options**: Each configurable value

**Scoring guidance:**
- Each new global/exported constant: -0.2 points
- Each removed global/exported constant: +0.2 points
- Consolidating constants into config object: Depends on net change

### 2. Module and Package Structure

#### New Modules
- **New files/modules**: Each new code file
- **New packages/namespaces**: Each organizational unit
- **New directories**: New structural groupings

**Scoring guidance:**
- Each new module/file: -0.4 points
- Each removed module/file: +0.4 points
- Merging multiple modules: +1 point
- Splitting one module into many: -1 point

### 3. Conceptual Consolidation

#### Reducing Concepts
Identify patterns that reduce conceptual count:
- **Merging similar classes**: Combining redundant types
- **Removing duplicate functionality**: DRY improvements
- **Inlining one-use abstractions**: Removing unnecessary indirection
- **Eliminating dead code**: Removing unused concepts

**Scoring guidance:**
- Merged 2+ similar classes: +1.5 points
- Removed dead code (complete concepts): +1 point
- Inlined unnecessary abstraction: +0.5 points
- Eliminated duplicate functionality: +1 point

#### Increasing Concepts
Identify patterns that increase conceptual count:
- **New abstractions**: Each new layer or wrapper
- **Splitting functionality**: One thing becomes many
- **Adding alternative implementations**: New ways to do same thing
- **Feature additions**: Entirely new capabilities

**Scoring guidance:**
- New abstraction layer: -1 point
- Feature addition with new concepts: -1 to -2 points
- Alternative implementation: -0.5 points

### 4. API Surface Area

#### Public Interface Changes
Count changes to what developers interact with:
- **New public API methods**: Each exposed function
- **New configuration options**: Each new setting
- **New event types**: Each new event/message type
- **New error types**: Each distinct error class

**Scoring guidance:**
- Each new API endpoint/method: -0.5 points
- Each removed API endpoint/method: +0.5 points
- API simplification (same capability, fewer methods): +1.5 points
- API expansion (more methods for same thing): -1 point

### 5. Dependencies and Imports

#### External Concepts
Count new external concepts brought in:
- **New library dependencies**: Each new package imported
- **New framework concepts**: Framework-specific abstractions
- **New third-party types**: External type dependencies

**Scoring guidance:**
- Each new external dependency: -1 point
- Each removed external dependency: +1 point
- Replacing library with simpler alternative: +0.5 points
- Adding heavy framework: -2 points

### 6. Domain Concepts

#### Business Logic Entities
Count domain-specific concepts:
- **New domain entities**: User, Order, Payment, etc.
- **New domain services**: Business logic components
- **New workflows**: Distinct process flows
- **New business rules**: Conditional logic representing rules

**Scoring guidance:**
- New core domain concept: -0.8 points
- Removed domain concept: +0.8 points
- Consolidating domain concepts: +1.5 points
- Domain concept proliferation: -1 to -2 points

### 7. Naming and Vocabulary

#### Distinct Names
Count the vocabulary size:
- **New unique names**: Each distinct identifier
- **Renamed concepts**: Old name + new name = 2 concepts temporarily
- **Overloaded names**: Same name, different meanings (confusing)

**Scoring guidance:**
- Large vocabulary expansion (20+ new names): -1 point
- Vocabulary reduction: +1 point
- Consistent naming reducing mental overhead: +0.5 points
- Inconsistent naming increasing confusion: -0.5 points

## Analysis Process

### Step 1: Count New Entities
Parse the diff and count:
- Classes added/removed
- Functions added/removed
- Types added/removed
- Modules added/removed
- Dependencies added/removed
- Constants/variables added/removed

### Step 2: Identify Consolidations
Look for:
- Code merged from multiple places
- Abstractions removed by inlining
- Duplicate functionality eliminated
- Similar classes/functions combined

### Step 3: Identify Expansions
Look for:
- New features with new concepts
- Code split into multiple new pieces
- New abstraction layers
- New alternatives/variations

### Step 4: Calculate Net Change
- Sum up conceptual additions (negative points)
- Sum up conceptual removals (positive points)
- Weight by visibility (public vs private)
- Consider cognitive impact

### Step 5: Normalize to -5 to +5 Scale
- If raw score < -5, cap at -5
- If raw score > +5, cap at +5
- Round to nearest 0.5

### Step 6: Provide Justification
Include:
- Number of new vs removed concepts
- Most significant changes
- Net impact on cognitive load

## Example Analysis Output

```json
{
  "score": -3.5,
  "reasoning": "Introduces 8 new classes (AuthService, TokenValidator, SessionManager, UserRepository, RoleChecker, PermissionService, AuditLogger, SecurityConfig), 15 new public methods, and 2 new external dependencies (jwt-library, crypto-utils). This significantly expands the conceptual surface area developers must understand.",
  "key_factors": [
    "8 new classes added",
    "15 new public methods",
    "2 new external dependencies",
    "No concepts removed or consolidated"
  ],
  "concept_changes": {
    "classes_added": 8,
    "functions_added": 15,
    "modules_added": 3,
    "dependencies_added": 2,
    "concepts_removed": 0
  }
}
```

## Example of Simplification

```json
{
  "score": 3.5,
  "reasoning": "Consolidated 5 separate authentication classes (OAuth, JWT, SAML, Basic, APIKey) into a single AuthenticationStrategy pattern with 5 implementations. Removed 3 duplicate validation functions by extracting common logic. Eliminated 2 unused modules and their 12 associated functions. Net reduction of 10 distinct concepts.",
  "key_factors": [
    "Consolidated 5 classes into cohesive pattern",
    "Removed 3 duplicate functions",
    "Eliminated 2 unused modules (12 functions)",
    "Net reduction of ~10 concepts"
  ],
  "concept_changes": {
    "classes_removed": 5,
    "classes_added": 1,
    "functions_removed": 15,
    "functions_added": 5,
    "net_concept_change": -10
  }
}
```

## Important Considerations

1. **Public vs Private**: Public concepts have higher weight than private ones
2. **Feature vs Refactoring**: New features naturally add concepts; judge reasonably
3. **Necessary vs Unnecessary**: Some concept additions are justified
4. **Context size**: Small projects can handle fewer concepts than large ones
5. **Domain complexity**: Complex domains need more concepts, but minimize where possible

## Common Patterns

### High Positive Score (+4 to +5)
- Major consolidation removing many concepts
- Dead code elimination
- Dependency removal
- Merging duplicate functionality

### Moderate Positive Score (+1 to +3)
- Inlining unnecessary abstractions
- Removing a few classes/modules
- Simplifying API surface area
- Consolidating similar concepts

### Neutral Score (0)
- Renaming without adding concepts
- Refactoring maintaining same conceptual count
- Trading one concept for another

### Moderate Negative Score (-1 to -3)
- Small feature additions
- A few new classes/types
- Some new functions/methods
- Minor dependency additions

### High Negative Score (-4 to -5)
- Major feature with many new concepts
- Many new classes/types/functions
- Significant API expansion
- Multiple new dependencies
- Concept proliferation

## Final Output Format

Return a JSON object with:
```json
{
  "dimension": "conceptual_weight",
  "score": <number between -5 and +5>,
  "reasoning": "<concise explanation>",
  "key_factors": ["<factor 1>", "<factor 2>", "..."],
  "concept_changes": {
    "classes_added": <number>,
    "classes_removed": <number>,
    "functions_added": <number>,
    "functions_removed": <number>,
    "modules_added": <number>,
    "modules_removed": <number>,
    "net_concept_change": <number>
  },
  "confidence": "<high|medium|low>"
}
```

**The score is the most critical output** - it should reflect whether the change increases or decreases the total number of concepts developers must understand.
