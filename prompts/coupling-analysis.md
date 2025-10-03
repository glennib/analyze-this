# Module Coupling Analysis Prompt

## Objective
Analyze git diff changes to determine how they impact module coupling in the codebase. Produce a numerical score from **-5 to +5** that represents the change in coupling:
- **Negative scores (-5 to -1)**: Increased coupling (worse)
- **Zero (0)**: No significant change in coupling
- **Positive scores (+1 to +5)**: Decreased coupling (better)

## Context
You will be provided with:
1. Git diff output showing added/removed/modified lines
2. File paths and names affected by the changes
3. Programming language context

## Analysis Framework

### 1. Dependency Analysis
Examine import/require/include statements:
- **Count new dependencies** added between modules
- **Count removed dependencies** between modules
- **Identify circular dependencies** introduced or removed
- **Track dependency direction changes** (A→B becoming B→A is a red flag)

**Scoring guidance:**
- Each new cross-module dependency: -0.5 points
- Each removed cross-module dependency: +0.5 points
- New circular dependency introduced: -2 points
- Circular dependency broken: +2 points

### 2. Shared State and Global Variables
Look for:
- **New global variables** or shared mutable state
- **New singleton patterns** or global instances
- **Removal of shared state** in favor of parameter passing
- **Introduction of dependency injection** vs. direct global access

**Scoring guidance:**
- New global/shared state: -1 point per occurrence
- Removed global/shared state: +1 point per occurrence
- New dependency injection: +0.5 points
- Hardcoded global access: -0.5 points

### 3. Interface and API Changes
Evaluate:
- **New public APIs** exposed between modules
- **API surface area** expansion or contraction
- **Breaking changes** requiring multiple modules to update together
- **Introduction of abstraction layers** (interfaces, protocols, contracts)

**Scoring guidance:**
- New abstraction layer reducing coupling: +1.5 points
- Removed unnecessary abstraction: +0.5 points
- API expansion requiring changes in multiple modules: -1 point
- API simplification: +1 point

### 4. Data Structure Sharing
Check for:
- **Direct access to internal data structures** from other modules
- **Encapsulation improvements** (getters/setters, immutable objects)
- **Shared complex types** between modules
- **Data transfer objects (DTOs)** introduced or removed

**Scoring guidance:**
- New direct access to internals: -1 point
- Improved encapsulation: +1 point
- New DTO/interface for data exchange: +0.5 points
- Shared mutable complex types: -1.5 points

### 5. Cross-Module Function Calls
Analyze:
- **Fan-out**: How many other modules does a changed module now call?
- **Fan-in**: How many modules now call into the changed module?
- **Temporal coupling**: Functions that must be called in specific order
- **Feature envy**: Methods accessing another module's data extensively

**Scoring guidance:**
- Significant increase in fan-out: -1 point
- Significant increase in fan-in to a specific module: -0.5 points
- Reduced fan-out/fan-in: +0.5 points
- New temporal coupling detected: -1 point
- Temporal coupling eliminated: +1 point

### 6. Module Boundary Violations
Identify:
- **Reaching across layers** (e.g., UI directly accessing database)
- **Violation of separation of concerns**
- **New imports from "internal" packages**
- **Proper layering improvements**

**Scoring guidance:**
- Layer violation: -2 points
- Fixed layer violation: +2 points
- Access to internal packages: -1 point
- Better boundary respect: +1 point

## Analysis Process

### Step 1: Parse the Diff
- Extract all modified files
- Identify added lines (prefixed with `+`)
- Identify removed lines (prefixed with `-`)
- Group changes by file and module

### Step 2: Categorize Changes
For each change, determine:
- Is it an import/dependency change?
- Does it introduce/remove shared state?
- Does it affect public APIs?
- Does it change data structure access patterns?
- Does it modify cross-module call patterns?
- Does it violate or improve architectural boundaries?

### Step 3: Apply Scoring Rubric
- Sum up individual scores from each category
- Weight scores based on severity and scope
- Consider the overall architectural impact

### Step 4: Normalize to -5 to +5 Scale
- If raw score < -5, cap at -5
- If raw score > +5, cap at +5
- Round to nearest 0.5 for clarity

### Step 5: Provide Justification
Include a brief explanation:
- Key factors that influenced the score
- Specific examples from the diff
- Overall coupling trend assessment

## Example Analysis Output

```json
{
  "score": -2.5,
  "reasoning": "This change introduces 3 new dependencies from the UserService to EmailService, NotificationService, and LoggingService (−1.5 points). A new global configuration object is shared across modules (−1 point). However, a circular dependency between AuthModule and UserModule was broken (+2 points). Overall, coupling has increased moderately.",
  "key_factors": [
    "3 new cross-module dependencies added",
    "1 global state introduced",
    "1 circular dependency resolved"
  ],
  "recommendation": "Consider using dependency injection to reduce direct coupling to services."
}
```

## Important Considerations

1. **Context matters**: A new dependency might be justified for proper separation of concerns
2. **Language patterns**: Different languages have different coupling patterns (e.g., Go interfaces vs. Java inheritance)
3. **Scale**: Small projects naturally have different coupling than microservices
4. **Direction**: Focus on the *change* in coupling, not absolute coupling level
5. **Intention**: Sometimes temporary increased coupling is acceptable during refactoring

## Final Output Format

Return a JSON object with:
```json
{
  "dimension": "coupling",
  "score": <number between -5 and +5>,
  "reasoning": "<concise explanation>",
  "key_factors": ["<factor 1>", "<factor 2>", "..."],
  "confidence": "<high|medium|low>"
}
```

**The score is the most critical output** - ensure it accurately reflects the coupling change magnitude and direction.
