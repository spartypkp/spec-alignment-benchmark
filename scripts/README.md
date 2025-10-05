# Benchmark Scripts Usage Guide

## Installation

```bash
# Install required Python packages
pip install -r requirements.txt
```

## Script Overview

### 1. `test_runner.py` - Test Execution Manager
Tracks test progress and manages test execution workflow.

```bash
# Check overall progress
python scripts/test_runner.py progress

# See what tests to run next
python scripts/test_runner.py next cursor
python scripts/test_runner.py next claude-code

# Record a test result
python scripts/test_runner.py record cursor baseline_balanced type1 output.json --score

# Validate output format
python scripts/test_runner.py validate output.json type1
```

### 2. `score_result.py` - Individual Test Scoring
Scores a single test output against ground truth.

```bash
# Score a Type 1 test
python scripts/score_result.py \
  results/raw/cursor/baseline_balanced/type1_run1.json \
  benchmark/branches/baseline_balanced/ground-truth-type1.json

# Score a combined test
python scripts/score_result.py \
  results/raw/cursor/baseline_balanced/combined_run1.json \
  benchmark/branches/baseline_balanced/ground-truth-combined.json
```

### 3. `aggregate_results.py` - Statistical Aggregation
Aggregates multiple runs for statistical analysis.

```bash
# Aggregate results for a specific framework and branch
python scripts/aggregate_results.py \
  --framework cursor \
  --branch baseline_balanced

python scripts/aggregate_results.py \
  --framework claude-code \
  --branch baseline_balanced
```

### 4. `compare_frameworks.py` - Framework Comparison
Compares performance between frameworks and tests hypotheses.

```bash
# Compare frameworks on a specific branch
python scripts/compare_frameworks.py --branch baseline_balanced
python scripts/compare_frameworks.py --branch control_perfect
```

### 5. `visualize_results.py` - Generate Visualizations
Creates charts and visual reports.

```bash
# Generate all visualizations
python scripts/visualize_results.py --all

# Generate specific visualizations
python scripts/visualize_results.py --overall     # Overall F1 comparison
python scripts/visualize_results.py --types       # Type-specific comparison
python scripts/visualize_results.py --hypotheses  # Hypothesis test results
python scripts/visualize_results.py --heatmap     # Performance heatmaps
python scripts/visualize_results.py --report      # Text summary report
```

## Complete Workflow Example

### Step 1: Run Tests in Frameworks

1. Load test repository in Cursor or Claude Code
2. Switch to test branch (e.g., `baseline_balanced`)
3. Run each prompt from `benchmark/prompts/`:
   - `type1-missing.md`
   - `type2-incorrect.md`
   - `type3-extraneous.md`
   - `combined-all-types.md`
4. Save JSON outputs

### Step 2: Record and Score Results

```bash
# Record each test output
python scripts/test_runner.py record cursor baseline_balanced type1 cursor_output_type1.json --score
python scripts/test_runner.py record cursor baseline_balanced type2 cursor_output_type2.json --score
python scripts/test_runner.py record cursor baseline_balanced type3 cursor_output_type3.json --score
python scripts/test_runner.py record cursor baseline_balanced combined cursor_output_combined.json --score

# Check progress
python scripts/test_runner.py progress
```

### Step 3: Aggregate Results

```bash
# After completing multiple runs
python scripts/aggregate_results.py --framework cursor --branch baseline_balanced
python scripts/aggregate_results.py --framework claude-code --branch baseline_balanced
```

### Step 4: Compare Frameworks

```bash
# Generate comparison
python scripts/compare_frameworks.py --branch baseline_balanced
```

### Step 5: Generate Visualizations

```bash
# Create all charts and reports
python scripts/visualize_results.py --all
```

## Directory Structure After Testing

```
results/
├── raw/                          # Raw test outputs
│   ├── cursor/
│   │   └── baseline_balanced/
│   │       ├── baseline_balanced_type1_run1_20251005_143022.json
│   │       ├── baseline_balanced_type2_run1_20251005_143158.json
│   │       └── ...
│   └── claude-code/
│       └── baseline_balanced/
│           └── ...
│
├── processed/                    # Scored results
│   ├── cursor/
│   │   └── baseline_balanced/
│   │       ├── baseline_balanced_type1_run1_scored.json
│   │       └── ...
│   └── claude-code/
│       └── ...
│
├── analysis/                     # Aggregated analysis
│   ├── cursor/
│   │   └── baseline_balanced/
│   │       └── baseline_balanced_summary.json
│   ├── claude-code/
│   │   └── baseline_balanced/
│   │       └── baseline_balanced_summary.json
│   └── comparisons/
│       ├── baseline_balanced_comparison.json
│       └── visualizations/
│           ├── overall_f1_comparison.png
│           ├── type_specific_comparison.png
│           ├── hypothesis_results.png
│           └── summary_report.txt
│
├── progress.json                 # Test completion tracking
└── test_runs.log                # Execution log
```

## Tips

1. **Always validate outputs** before scoring to catch formatting issues early
2. **Run tests in order**: control_perfect first (establishes baseline)
3. **Maintain fresh context**: Each prompt should start with clean context
4. **Be consistent**: Use exact same prompts for both frameworks
5. **Document anomalies**: Note any unusual behavior in test_runs.log

## Troubleshooting

### "No ground truth file found"
- Check that branch name matches exactly
- Verify ground truth files exist in `benchmark/branches/{branch}/`

### "Invalid JSON in output"
- Ensure framework output is valid JSON
- Check for trailing commas or syntax errors
- Use `test_runner.py validate` to check format

### "Missing aggregated results"
- Run `aggregate_results.py` before `compare_frameworks.py`
- Ensure you have scored results in `processed/` directory

### Charts not generating
- Install matplotlib and seaborn: `pip install matplotlib seaborn`
- Check that comparison data exists in `analysis/comparisons/`
