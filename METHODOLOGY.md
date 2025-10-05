# Specification Alignment Benchmark Methodology

**Version 1.0.0** - Implementation Complete

## Core Concept

We test how well AI coding assistant frameworks (Cursor, Claude Code) can detect misalignments between code and specifications when using the same AI model (Claude 3.5 Sonnet).

**Key Innovation**: This is the first benchmark to test frameworks rather than models, isolating capabilities like search strategy, context management, and tool use.

## The Three Misalignment Types

Every possible specification misalignment falls into one of these three categories:

### Type 1: Missing Implementation
- **Definition**: Spec requires X, code doesn't have X
- **Example**: Spec requires JWT authentication, code has no authentication
- **Detection**: List section numbers from spec

### Type 2: Incorrect Implementation  
- **Definition**: Spec requires X implemented as A, code implements X as B
- **Example**: Spec requires 15-minute token expiry, code has 60-minute expiry
- **Detection**: Section numbers + affected files

### Type 3: Extraneous Code
- **Definition**: Code has Y, spec doesn't mention Y
- **Example**: Code has admin dashboard, spec doesn't mention admin features
- **Detection**: Feature names or file paths

## Current Implementation: Todo Application

### 6 Test Branches (38 Misalignments)

| Branch | Type 1 | Type 2 | Type 3 | Total | Purpose |
|--------|--------|--------|--------|-------|---------|
| **control_perfect** | 0 | 0 | 0 | 0 | False positive baseline |
| **baseline_balanced** | 3 | 3 | 2 | 8 | Overall capability (H1) |
| **type1_heavy** | 6 | 1 | 1 | 8 | Type 1 specialization (H2a) |
| **type2_heavy** | 1 | 6 | 1 | 8 | Type 2 specialization (H2b) |
| **subtle_only** | 2 | 2 | 2 | 6 | Complexity handling (H3) |
| **distributed** | 3 | 3 | 2 | 8 | Context distribution (H4) |

### Repository Structure

```
todo-app-test/                    # Separate test repository
├── specs/
│   └── todo-specification.md    # Complete specification
├── src/
│   ├── app/                     # Next.js app directory
│   ├── components/              # React components
│   └── lib/                     # Utilities
└── [6 branches with planted misalignments]

spec-alignment-benchmark/         # This repository
├── benchmark/
│   ├── branches/                # Ground truth for each branch
│   ├── prompts/                 # The 4 test prompts
│   └── hypotheses.md            # Scientific predictions
├── scripts/                     # Automated analysis pipeline
└── results/                     # Test outputs
```

## Scientific Hypotheses

We're testing 5 specific hypotheses about framework differences:

### H1: Overall Performance
- **Prediction**: Claude Code > Cursor by ≥15% F1 score
- **Rationale**: Chat interface encourages systematic analysis
- **Test**: baseline_balanced branch

### H2: Type-Specific Specialization
- **H2a**: Cursor better at Type 1 (file visibility advantage)
- **H2b**: Claude Code better at Type 2 (reasoning advantage)
- **H2c**: Cursor better at Type 3 (file explorer advantage)
- **Tests**: type1_heavy, type2_heavy branches

### H3: Complexity Degradation
- **Prediction**: Claude Code degrades less on subtle issues
- **Rationale**: Reasoning approach maintains effectiveness
- **Test**: subtle_only branch

### H4: Context Distribution
- **Prediction**: Cursor better with distributed misalignments
- **Rationale**: IDE navigation advantage
- **Test**: distributed branch

### H5: False Positive Rate
- **Prediction**: Cursor generates 2× more false positives
- **Rationale**: Emphasis on completeness over precision
- **Test**: control_perfect branch

## Test Protocol

### The Four Test Prompts

For each branch, we run 4 prompts with fresh context:

1. **`type1-missing.md`**: Find missing implementations only
2. **`type2-incorrect.md`**: Find incorrect implementations only
3. **`type3-extraneous.md`**: Find extraneous code only
4. **`combined-all-types.md`**: Find all three types in one pass

**Test Volume**: 6 branches × 4 prompts × 5 runs × 2 frameworks = **240 total tests**

### Execution Process

1. **Setup Phase**
   - Load test repository in framework
   - Switch to test branch
   - Ensure fresh context

2. **Test Phase**
   - Copy prompt from `benchmark/prompts/`
   - Run in framework
   - Save JSON output

3. **Recording Phase**
   ```bash
   python scripts/test_runner.py record \
     cursor baseline_balanced type1 output.json --score
   ```

## Automated Analysis Pipeline

### 1. Test Management (`test_runner.py`)
- Tracks progress across 240 tests
- Validates output format
- Organizes results by framework/branch/type

### 2. Individual Scoring (`score_result.py`)
- Compares output against ground truth
- Calculates precision, recall, F1 score
- Point system: +1 correct, -0.25 false positive

### 3. Statistical Aggregation (`aggregate_results.py`)
- Aggregates multiple runs per test
- Calculates mean, std deviation, min/max
- Generates branch-level summaries

### 4. Framework Comparison (`compare_frameworks.py`)
- Tests all 5 hypotheses
- Performs paired t-tests
- Calculates Cohen's d effect sizes

### 5. Visualization (`visualize_results.py`)
- Overall F1 comparison charts
- Type-specific performance charts
- Hypothesis test results
- Performance heatmaps
- Summary reports

## Measurement Metrics

### Primary Metrics
- **Precision**: Of items reported, how many were correct?
- **Recall**: Of actual misalignments, how many were found?
- **F1 Score**: Harmonic mean of precision and recall
- **Points**: Scoring with penalties for false positives

### Statistical Tests
- **Paired t-test**: Comparing same test across frameworks
- **Cohen's d**: Effect size measurement
- **p < 0.05**: Statistical significance threshold
- **Minimum 3 runs**: Statistical validity (5 preferred)

## Ground Truth Format

Enhanced format with reasoning for transparency:

```json
{
  "test_branch": "baseline_balanced",
  "test_type": "type1_missing",
  "expected_sections": ["4.1", "3.1", "2.4"],
  "ground_truth": {
    "misalignments": [
      {
        "section": "4.1",
        "reasoning": "Password validation (min 6 chars) not implemented"
      },
      {
        "section": "3.1",
        "reasoning": "Session 7-day expiry not implemented"
      }
    ]
  }
}
```

## Why This Methodology?

### Scientific Rigor
- **Controlled Variables**: Same model, prompts, test cases
- **Hypothesis-Driven**: Testing specific predictions
- **Statistical Validity**: Multiple runs, significance tests
- **Automated Pipeline**: Reduces human error

### Practical Value
- **Real Task**: Specification alignment is common need
- **Actionable Results**: Shows specific strengths/weaknesses
- **Fair Comparison**: No framework-specific advantages
- **Reproducible**: Complete automation and documentation

## Key Principles

1. **Simplicity**: Only 3 fundamental misalignment types
2. **Completeness**: These types cover every possible case
3. **Objectivity**: Clear ground truth with reasoning
4. **Reproducibility**: Automated tracking and scoring
5. **Fairness**: Identical conditions for both frameworks
6. **Transparency**: All hypotheses stated upfront

## Expected Outcomes

### If Hypotheses Correct:
- Claude Code wins overall (~15% higher F1)
- Clear specialization patterns by type
- Different degradation on complexity
- Opposite strengths on distribution
- Higher false positive rate for Cursor

### If Hypotheses Wrong:
- Frameworks more similar than expected
- Model dominates framework differences
- Need to revise assumptions
- Still provides empirical comparison

## Current Status

✅ **Implementation Complete**:
- 6 test branches defined (38 misalignments)
- Ground truth files created (24 files)
- Test prompts finalized (4 types)
- Analysis pipeline implemented (5 scripts)
- Hypothesis framework established

⏳ **Ready to Execute**:
- Run control_perfect first (baseline)
- Complete 240 test executions
- Analyze results and test hypotheses
- Generate reports and visualizations

This methodology provides the first rigorous, hypothesis-driven comparison of AI coding frameworks on a practical development task.