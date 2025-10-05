# Test Results Directory

## Directory Structure

```
results/
├── raw/                        # Raw outputs from frameworks
│   ├── cursor/                 # Cursor test outputs
│   │   ├── control_perfect/    
│   │   ├── baseline_balanced/  
│   │   ├── type1_heavy/       
│   │   ├── type2_heavy/       
│   │   ├── subtle_only/       
│   │   └── distributed/       
│   └── claude-code/            # Claude Code test outputs
│       └── [same structure]
│
├── processed/                  # Scored and validated results
│   ├── cursor/
│   │   └── [branch folders with scored results]
│   └── claude-code/
│       └── [branch folders with scored results]
│
└── analysis/                   # Aggregated analysis and visualizations
    ├── cursor/
    │   └── [branch-level analysis]
    ├── claude-code/
    │   └── [branch-level analysis]
    └── comparisons/            # Framework vs framework comparisons
        ├── overall_performance.json
        ├── hypothesis_tests.json
        └── visualizations/
```

## File Naming Convention

### Raw Results
Pattern: `{branch}_{test_type}_run{N}_{timestamp}.json`

Examples:
- `baseline_balanced_type1_run1_20251005_143022.json`
- `baseline_balanced_type2_run1_20251005_143158.json`
- `baseline_balanced_type3_run1_20251005_143334.json`
- `baseline_balanced_combined_run1_20251005_143512.json`

### Processed Results
Pattern: `{branch}_{test_type}_run{N}_scored.json`

Examples:
- `baseline_balanced_type1_run1_scored.json`
- `baseline_balanced_combined_run1_scored.json`

### Analysis Files
- `{branch}_summary.json` - Aggregated metrics for a branch
- `{branch}_statistics.json` - Statistical analysis (mean, std, etc.)
- `hypothesis_{H#}_results.json` - Hypothesis test results

## Data Flow

1. **Raw Output** → Save framework output to `raw/{framework}/{branch}/`
2. **Scoring** → Process with `score.py` → Save to `processed/{framework}/{branch}/`
3. **Aggregation** → Run `aggregate_results.py` → Save to `analysis/{framework}/{branch}/`
4. **Comparison** → Run `compare_frameworks.py` → Save to `analysis/comparisons/`
5. **Visualization** → Run `visualize_results.py` → Save charts to `analysis/comparisons/visualizations/`

## Test Execution Tracking

### Run Log Format
Each test run should be logged in `test_runs.log` with:
```
{timestamp} | {framework} | {branch} | {test_type} | run_{N} | {status} | {notes}
```

### Progress Tracking
Use `progress.json` to track completion:
```json
{
  "cursor": {
    "control_perfect": {"type1": [1,2,3], "type2": [], ...},
    "baseline_balanced": {...}
  },
  "claude-code": {...}
}
```

## Quality Control

- All raw outputs must be valid JSON
- All raw outputs must match expected schema
- Processed results must include scoring metadata
- Analysis must include statistical significance tests

## Quick Commands

```bash
# Score a single test result
python scripts/score_result.py \
  results/raw/cursor/baseline_balanced/test.json \
  benchmark/branches/baseline_balanced/ground-truth-type1.json

# Aggregate results for a branch
python scripts/aggregate_results.py \
  --framework cursor \
  --branch baseline_balanced

# Compare frameworks on a branch
python scripts/compare_frameworks.py \
  --branch baseline_balanced

# Generate all visualizations
python scripts/visualize_results.py --all
```
