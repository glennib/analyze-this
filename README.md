# analyze-this

A tool that analyzes changes in a git repository's history and creates visualizations classifying changes along three dimensions:

1. **Module Coupling** - Increase or decrease in coupling between modules
2. **Test Coverage** - Increase or decrease in test coverage
3. **Abstractions & Concepts** - Increase or decrease in number of abstractions

Each dimension is scored from **-5 to +5** for spider graph visualization.

## Usage

```bash
./analyze-changes <git-ref-a> <git-ref-b>
```

### Example

```bash
./analyze-changes main feature-branch
./analyze-changes HEAD~10 HEAD
./analyze-changes v1.0.0 v2.0.0
```

## Setup

### Prerequisites

- Node.js installed
- Anthropic API key

### Environment Variables

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

Optional: Specify a different model (defaults to `claude-sonnet-4-20250514`):

```bash
export MODEL=claude-sonnet-4-20250514
```

## Output Format

The script outputs JSON to stdout:

```json
{
  "metadata": {
    "ref_a": "main",
    "ref_b": "feature-branch",
    "analyzed_at": "2025-10-03T12:00:00.000Z",
    "model": "claude-sonnet-4-20250514"
  },
  "dimensions": {
    "coupling": {
      "dimension": "coupling",
      "score": -2.5,
      "reasoning": "...",
      "key_factors": ["..."],
      "confidence": "high"
    },
    "test_coverage": {
      "dimension": "test_coverage",
      "score": 3.5,
      "reasoning": "...",
      "key_factors": ["..."],
      "confidence": "high"
    },
    "abstraction": {
      "dimension": "abstraction",
      "score": 1.0,
      "reasoning": "...",
      "key_factors": ["..."],
      "confidence": "medium"
    }
  },
  "summary": {
    "total_score": 2.0,
    "average_score": "0.67"
  }
}
```

## How It Works

1. Extracts git diff between two refs
2. Loads detailed analysis prompts for each dimension
3. Sends diff + prompt to Claude API for analysis
4. Aggregates scores into JSON output
5. Output can be used for spider graph visualization

## Analysis Prompts

Each dimension has a detailed prompt in `prompts/`:

- `coupling-analysis.md` - Analyzes module dependencies, shared state, and architectural boundaries
- `test-coverage-analysis.md` - Analyzes test quantity, quality, and coverage gaps
- `abstraction-analysis.md` - Analyzes design patterns, complexity, and appropriate abstraction levels

These prompts provide detailed scoring rubrics and guidelines for the LLM to follow.

## Future Enhancements

- Spider graph visualization generation
- Support for analyzing multiple commit ranges
- HTML report output
- Caching of analysis results
- Custom dimension prompts
