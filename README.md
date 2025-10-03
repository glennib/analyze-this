# analyze-this

A tool that analyzes changes in a git repository's history and creates visualizations classifying changes along three dimensions:

1. **Module Coupling** - Increase or decrease in coupling between modules
2. **Test Coverage** - Increase or decrease in test coverage
3. **Abstractions & Concepts** - Increase or decrease in number of abstractions

Each dimension is scored from **-5 to +5** for spider graph visualization.

## Usage

### 1. Analyze Changes

```bash
./analyze-changes <git-ref-a> <git-ref-b> > analysis.json
```

**Examples:**
```bash
./analyze-changes main feature-branch > analysis.json
./analyze-changes HEAD~10 HEAD > analysis.json
./analyze-changes v1.0.0 v2.0.0 > analysis.json
```

### 2. Visualize Results

```bash
./visualize analysis.json [output.html]
```

**Examples:**
```bash
./visualize analysis.json report.html
./visualize analysis.json  # Creates analysis-report.html by default
```

Then open the HTML file in your browser to see an interactive spider graph with detailed analysis.

### Quick Workflow

```bash
# Analyze and visualize in one go
./analyze-changes HEAD~10 HEAD > analysis.json && ./visualize analysis.json
```

## Setup

### Prerequisites

- Python 3.7+ installed
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Environment Variables

Set your Google Gemini API key:

```bash
export GEMINI_API_KEY=your-api-key-here
```

Optional: Specify a different model (defaults to `gemini-2.0-flash-exp`):

```bash
export MODEL=gemini-2.0-flash-exp
```

Available models: `gemini-2.0-flash-exp`, `gemini-1.5-pro`, `gemini-1.5-flash`

## Output Format

The script outputs JSON to stdout:

```json
{
  "metadata": {
    "ref_a": "main",
    "ref_b": "feature-branch",
    "analyzed_at": "2025-10-03T12:00:00.000Z",
    "model": "gemini-2.0-flash-exp"
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

### Analysis (`analyze-changes`)
1. Extracts git diff between two refs
2. Loads detailed analysis prompts for each dimension
3. Sends diff + prompt to Google Gemini API for analysis
4. Aggregates scores into JSON output

### Visualization (`visualize`)
1. Reads JSON analysis output
2. Generates interactive HTML report with:
   - **Spider/Radar chart** showing scores across all dimensions
   - **Detailed breakdown** for each dimension with reasoning
   - **Color-coded scores** (green = positive, red = negative)
   - **Key factors** and confidence levels
3. Uses Chart.js for interactive visualization
4. Self-contained HTML (works offline after generation)

## Analysis Prompts

Each dimension has a detailed prompt in `prompts/`:

- `coupling-analysis.md` - Analyzes module dependencies, shared state, and architectural boundaries
- `test-coverage-analysis.md` - Analyzes test quantity, quality, and coverage gaps
- `abstraction-analysis.md` - Analyzes design patterns, complexity, and appropriate abstraction levels

These prompts provide detailed scoring rubrics and guidelines for the LLM to follow.

## Visualization Features

The generated HTML report includes:

- **Interactive spider/radar chart** with -5 to +5 scale
- **Color-coded data points** based on score magnitude
- **Summary statistics** (average and total scores)
- **Detailed analysis cards** for each dimension
- **Reasoning and key factors** from the LLM analysis
- **Confidence levels** for each dimension
- **Responsive design** that works on all devices
- **No external dependencies** after generation (works offline)

## Future Enhancements

- Support for analyzing multiple commit ranges
- Comparison view (multiple analyses side-by-side)
- Caching of analysis results
- Custom dimension prompts
- Export to PDF
- Trend analysis over time
