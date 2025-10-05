# Specification Alignment Benchmark Repository

**Version:** 2.0.0  
**Created:** October 5, 2025  
**Updated:** October 5, 2025  
**Repository:** spec-alignment-benchmark  
**Purpose:** Benchmark AI coding assistant frameworks on specification alignment detection  
**Status:** Implementation complete, ready for test execution

---

## Repository Overview

This repository contains a benchmark for comparing how well AI coding assistant **frameworks** (not models) can detect misalignments between code and specifications. By using the same underlying language model across different tools, we isolate and measure framework-specific capabilities.

### Key Innovation

Unlike existing benchmarks that compare models (GPT-4 vs Claude), this benchmark:
- Holds the model constant (Claude 3.5 Sonnet)
- Tests three fundamental misalignment types
- Uses simplified, objective scoring
- Provides reproducible methodology

---

## The Three Misalignment Types

Every possible specification misalignment falls into exactly one of these categories:

### Type 1: Missing Implementation
- **Definition**: Specification requires X, code doesn't have X
- **Example**: Spec requires JWT authentication, code has no authentication
- **Output**: List of section headers from spec

### Type 2: Incorrect Implementation
- **Definition**: Specification requires X as A, code implements X as B  
- **Example**: Spec requires 15-minute tokens, code has 60-minute tokens
- **Output**: Section headers + affected files

### Type 3: Extraneous Code
- **Definition**: Code contains Y, specification doesn't mention Y
- **Example**: Code has admin dashboard, spec doesn't mention admin features
- **Output**: List of file paths

---

## Repository Structure

```
spec-alignment-benchmark/
├── README.md                    # Quick start and overview
├── METHODOLOGY.md              # Detailed explanation of approach
├── requirements.txt            # Python dependencies
│
├── benchmark/                  # Core benchmark content
│   ├── README.md              # Benchmark documentation
│   ├── hypotheses.md          # Scientific hypotheses (H1-H5)
│   ├── test-summary.md        # Overview of 6 branches, 38 misalignments
│   ├── branches/              # Test branch definitions
│   │   ├── control_perfect/  # Control (0 misalignments)
│   │   │   ├── control_perfect.md
│   │   │   └── [4 ground truth JSON files]
│   │   ├── baseline_balanced/# Balanced (8 misalignments)
│   │   │   ├── baseline_balanced.md
│   │   │   └── [4 ground truth JSON files]
│   │   ├── type1_heavy/      # Type 1 focus (8 misalignments)
│   │   ├── type2_heavy/      # Type 2 focus (8 misalignments)
│   │   ├── subtle_only/      # Subtle issues (6 misalignments)
│   │   └── distributed/      # Distributed (8 misalignments)
│   └── prompts/               # Test prompts
│       ├── README.md
│       ├── type1-missing.md
│       ├── type2-incorrect.md
│       ├── type3-extraneous.md
│       └── combined-all-types.md
│
├── scripts/                    # Analysis and scoring tools
│   ├── README.md              # Script usage guide
│   ├── score_result.py        # Score individual test outputs
│   ├── test_runner.py         # Manage test execution and tracking
│   ├── aggregate_results.py   # Statistical aggregation
│   ├── compare_frameworks.py  # Hypothesis testing
│   └── visualize_results.py   # Generate charts and reports
│
├── examples/                   # Example inputs and outputs
│   ├── README.md
│   ├── sample-ground-truth.json
│   ├── sample-llm-output.json
│   └── scored_sample-llm-output.json
│
├── docs/                       # Documentation
│   ├── ground-truth-format.md
│   └── test-execution-protocol.md
│
├── results/                    # Test outputs (created during testing)
│   ├── README.md              # Results directory documentation
│   ├── raw/                   # Raw framework outputs
│   │   ├── cursor/
│   │   │   └── [branch folders]
│   │   └── claude-code/
│   │       └── [branch folders]
│   ├── processed/             # Scored results
│   │   └── [framework/branch structure]
│   └── analysis/              # Aggregated analysis
│       ├── cursor/
│       ├── claude-code/
│       └── comparisons/
│           └── visualizations/
│
└── specs/                      # Specifications
    ├── benchmark-specification.md  # Main benchmark design
    └── repository-specification.md # This document
```

---

## How It Works

### 1. Test Repository Setup

The test repository (todo application) should have:
```
todo-app-test/
├── specs/
│   └── todo-specification.md    # Complete specification
├── src/
│   ├── app/                     # Next.js app directory
│   ├── components/              # React components
│   └── lib/                     # Utilities
└── README.md
```

**Test Branches** (6 implemented):
- `main`: Perfectly aligned baseline
- `control_perfect`: No misalignments (false positive test)
- `baseline_balanced`: 3 Type 1, 3 Type 2, 2 Type 3 (8 total)
- `type1_heavy`: 6 Type 1, 1 Type 2, 1 Type 3 (8 total)
- `type2_heavy`: 1 Type 1, 6 Type 2, 1 Type 3 (8 total)
- `subtle_only`: 2 Type 1, 2 Type 2, 2 Type 3 (6 subtle)
- `distributed`: 3 Type 1, 3 Type 2, 2 Type 3 (8 across many files)

### 2. Test Execution

**Using the Test Runner**:
```bash
# Check progress
python scripts/test_runner.py progress

# See next tests to run
python scripts/test_runner.py next cursor

# Record and score a test
python scripts/test_runner.py record cursor baseline_balanced type1 output.json --score
```

**Manual Execution**:
1. Load test repository in framework (Cursor or Claude Code)
2. Switch to test branch (e.g., `git checkout baseline_balanced`)
3. Copy prompt from `benchmark/prompts/[type].md`
4. Paste into framework and run
5. Save JSON output
6. Record with test_runner or score directly

### 3. Analysis Pipeline

```bash
# 1. Score individual test
python scripts/score_result.py \
  results/raw/cursor/baseline_balanced/type1_run1.json \
  benchmark/branches/baseline_balanced/ground-truth-type1.json

# 2. Aggregate results for a branch
python scripts/aggregate_results.py \
  --framework cursor \
  --branch baseline_balanced

# 3. Compare frameworks
python scripts/compare_frameworks.py \
  --branch baseline_balanced

# 4. Generate visualizations
python scripts/visualize_results.py --all
```

---

## Ground Truth Format

**Enhanced Format with Reasoning** (per branch, 4 files):

```json
// ground-truth-type1.json
{
  "test_branch": "baseline_balanced",
  "test_type": "type1_missing",
  "expected_sections": ["4.1", "3.1", "2.4"],
  "ground_truth": {
    "misalignments": [
      {
        "section": "4.1",
        "reasoning": "Password minimum 6 characters validation missing"
      },
      {
        "section": "3.1",
        "reasoning": "Session 7-day expiry not implemented"
      },
      {
        "section": "2.4",
        "reasoning": "Statistics bar with three metrics missing"
      }
    ]
  }
}

// ground-truth-type2.json includes files
{
  "test_branch": "baseline_balanced",
  "test_type": "type2_incorrect",
  "ground_truth": {
    "misalignments": [
      {
        "section": "2.4",
        "reasoning": "Tasks sorted ascending instead of descending",
        "files": ["src/app/api/tasks/route.ts"]
      }
    ]
  }
}

// ground-truth-type3.json
{
  "test_branch": "baseline_balanced",
  "test_type": "type3_extraneous",
  "ground_truth": {
    "misalignments": [
      {
        "feature": "Admin Dashboard",
        "reasoning": "Admin interface not in specification",
        "files": ["src/app/admin/page.tsx"]
      }
    ]
  }
}
```

## LLM Output Format

The prompts ask for this exact format:

### Type 1 Output
```json
{
  "analysis_type": "type1_missing",
  "type1_missing": ["2.1 Authentication & Authorization"]
}
```

### Type 2 Output  
```json
{
  "analysis_type": "type2_incorrect",
  "type2_incorrect": [
    {
      "section": "3.1 Request/Response Format",
      "files": ["middleware/errorHandler.ts"]
    }
  ]
}
```

### Type 3 Output
```json
{
  "analysis_type": "type3_extraneous",
  "type3_extraneous": ["app/admin/route.ts"]
}
```

### Combined Output
All three types in one response.

---

## Scoring System

### Automated Scoring Pipeline

1. **Individual Test Scoring** (`score_result.py`):
   - Handles all 4 test types (type1, type2, type3, combined)
   - Calculates precision, recall, F1 score
   - Point system: +1 for correct, -0.25 for false positive

2. **Statistical Aggregation** (`aggregate_results.py`):
   - Aggregates multiple runs
   - Calculates mean, std deviation, min/max
   - Generates branch-level summaries

3. **Framework Comparison** (`compare_frameworks.py`):
   - Tests all 5 hypotheses (H1-H5)
   - Performs statistical significance tests
   - Uses paired t-tests and Cohen's d

4. **Visualization** (`visualize_results.py`):
   - Overall F1 comparison charts
   - Type-specific performance charts
   - Hypothesis test results
   - Performance heatmaps
   - Summary reports

### Why This Design?

1. **No fuzzy matching**: Exact string comparison only
2. **Minimal data**: Only what's needed for scoring
3. **Fast comparison**: O(n) set operations
4. **Objective scoring**: No subjective interpretation
5. **Easy validation**: Anyone can verify results

---

## Running Tests

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt
# Requires: numpy, scipy, matplotlib, seaborn
```

### Test Workflow

```bash
# 1. Check current progress
python scripts/test_runner.py progress

# 2. See what tests to run next
python scripts/test_runner.py next cursor

# 3. Run test in framework (manual)
# - Load test repository in framework
# - Switch to branch (e.g., baseline_balanced)
# - Copy prompt from benchmark/prompts/
# - Save JSON output

# 4. Record and score test
python scripts/test_runner.py record \
  cursor baseline_balanced type1 output.json --score

# 5. After multiple runs, aggregate
python scripts/aggregate_results.py \
  --framework cursor --branch baseline_balanced

# 6. Compare frameworks
python scripts/compare_frameworks.py \
  --branch baseline_balanced

# 7. Generate visualizations
python scripts/visualize_results.py --all
```

### Test Management

**Test Runner Features**:
- Progress tracking across 240 total tests
- Automatic file naming and organization
- Validation of output format
- Integration with scoring pipeline
- Test run logging

**Quality Control**:
- Always run `control_perfect` branch first
- Use fresh context for each prompt
- Validate outputs before scoring
- Run minimum 3 times per test (5 preferred)
- Document anomalies in test_runs.log

---

## Key Principles

1. **Simplicity**: Only 3 fundamental misalignment types
2. **Completeness**: These 3 types cover every possible case
3. **Objectivity**: Clear ground truth with reasoning for transparency
4. **Reproducibility**: Automated tracking ensures consistent testing
5. **Fairness**: Identical prompts and conditions for all frameworks
6. **Scientific Rigor**: Hypothesis-driven with statistical validation

---

## Next Steps

### Immediate Testing Plan

1. **Create Todo Test Repository**:
   - Implement todo app matching specification
   - Create 6 branches with defined misalignments
   - Verify ground truth files match implementation

2. **Execute Benchmark**:
   - Run control_perfect first (establish baseline)
   - Complete 5 runs × 4 prompts × 6 branches × 2 frameworks
   - Total: 240 test executions

3. **Analyze Results**:
   - Test all 5 hypotheses
   - Generate visualizations
   - Publish findings

### Future Enhancements

1. **Additional Test Cases**: Beyond todo app
2. **More Frameworks**: GitHub Copilot, Windsurf, etc.
3. **Complexity Levels**: Simple to complex codebases
4. **Language Coverage**: TypeScript, Python, Go, etc.

### Contribution Process

1. Fork repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request
5. Participate in review

---

## Results Interpretation

### Metrics Explained

**Precision**: Of items reported, how many were correct?
- High precision = few false positives
- Low precision = many false alarms

**Recall**: Of actual misalignments, how many were found?
- High recall = found most issues
- Low recall = missed many issues

**F1 Score**: Harmonic mean of precision and recall
- Balances both metrics
- Single score for comparison

### Understanding Scores

```
Example Output:
TYPE1 Results:
  Precision: 66.7%  (2 correct out of 3 reported)
  Recall:    66.7%  (2 found out of 3 actual)
  F1 Score:  0.667
  Score:     1.75   (2 correct - 0.25 penalty)
```

This means the framework:
- Found 2/3 missing implementations
- Had 1 false positive (penalty applied)
- Achieved moderate performance on Type 1 detection

---

## FAQ

**Q: Why test frameworks instead of models?**  
A: Frameworks add search, context management, and tool use on top of models. Testing with the same model isolates these framework capabilities.

**Q: Why these three types?**  
A: They're exhaustive - every possible misalignment must be one of: missing (Type 1), wrong (Type 2), or extra (Type 3).

**Q: What are the 5 hypotheses?**  
A: H1 (overall performance), H2 (type specialization), H3 (complexity handling), H4 (context distribution), H5 (false positive rate).

**Q: How is scoring automated?**  
A: Scripts handle scoring, aggregation, comparison, and visualization automatically.

**Q: Can I test other frameworks?**  
A: Yes! Use the same prompts and ground truth format for any framework.

**Q: How many test runs are needed?**  
A: Minimum 3 runs per test, 5 preferred. Total: 240 tests across both frameworks.

---

## License

MIT License - See LICENSE file

---

## Contact

- Issues: [GitHub Issues](https://github.com/[username]/spec-alignment-benchmark/issues)
- Discussions: [GitHub Discussions](https://github.com/[username]/spec-alignment-benchmark/discussions)

---

## Acknowledgments

This benchmark addresses a critical gap in AI tool evaluation. By testing frameworks rather than models, we can finally understand which tools best help developers maintain specification alignment.