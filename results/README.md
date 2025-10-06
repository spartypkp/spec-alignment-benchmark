# Test Results Directory

## Directory Structure

```
results/
├── raw/                        # Raw outputs from frameworks
│   ├── cursor/                 # Cursor test outputs
│   │   ├── control_perfect/    
│   │   │   ├── type1/
│   │   │   │   ├── run1.json
│   │   │   │   ├── run2.json
│   │   │   │   └── ...
│   │   │   ├── type2/
│   │   │   ├── type3/
│   │   │   └── combined/
│   │   ├── baseline_balanced/  
│   │   │   └── [same subdirectory structure]
│   │   └── [other branches]       
│   └── claude-code/            # Claude Code test outputs
│       └── [same structure]
│
├── processed/                  # Scored and validated results
│   ├── cursor/
│   │   └── [same structure as raw, with run{N}_scored.json files]
│   └── claude-code/
│       └── [same structure as raw, with run{N}_scored.json files]
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
Path: `raw/{framework}/{branch}/{test_type}/run{N}.json`

Examples:
- `raw/cursor/baseline_balanced/type1/run1.json`
- `raw/cursor/baseline_balanced/type2/run1.json`
- `raw/cursor/baseline_balanced/type3/run1.json`
- `raw/cursor/baseline_balanced/combined/run1.json`

### Processed Results
Path: `processed/{framework}/{branch}/{test_type}/run{N}_scored.json`

Examples:
- `processed/cursor/baseline_balanced/type1/run1_scored.json`
- `processed/cursor/baseline_balanced/combined/run1_scored.json`

### Analysis Files
- `{branch}_summary.json` - Aggregated metrics for a branch
- `{branch}_statistics.json` - Statistical analysis (mean, std, etc.)
- `hypothesis_{H#}_results.json` - Hypothesis test results

## Data Flow

1. **Raw Output** → Save framework output to `raw/{framework}/{branch}/{test_type}/run{N}.json`
2. **Scoring** → Process with `score_result.py` → Save to `processed/{framework}/{branch}/{test_type}/run{N}_scored.json`
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
