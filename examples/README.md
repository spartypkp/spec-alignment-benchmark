# Scoring Examples

This directory contains examples showing how the simplified scoring system works.

## Files

- `sample-ground-truth.json` - Example ground truth with known misalignments
- `sample-llm-output.json` - Example LLM output to be scored
- `scored_sample-llm-output.json` - Generated scoring results

## How It Works

### 1. Ground Truth Format

The ground truth is extremely simple:

```json
{
  "type1_missing": [
    "2.1 Authentication & Authorization",  // Section headers only
    "3.3 Rate Limiting"
  ],
  "type2_incorrect": [
    {
      "section": "3.1 Request/Response Format",
      "files": ["middleware/errorHandler.ts"]  // Section + files
    }
  ],
  "type3_extraneous": [
    "app/admin/route.ts"  // File paths only
  ]
}
```

### 2. LLM Output Format

The LLM outputs in the exact same format:

```json
{
  "analysis_type": "combined_all_types",
  "type1_missing": ["2.1 Authentication & Authorization"],
  "type2_incorrect": [{"section": "3.1 Request/Response Format", "files": ["middleware/errorHandler.ts"]}],
  "type3_extraneous": ["app/admin/route.ts"]
}
```

### 3. Scoring Logic

**Type 1 & Type 3**: Simple set operations
- True Positive: Item in both LLM output and ground truth
- False Positive: Item in LLM output but not ground truth  
- False Negative: Item in ground truth but not LLM output

**Type 2**: Section + file matching
- True Positive: Same section AND at least one file matches
- False Positive: Section/files combo not in ground truth
- False Negative: Ground truth combo not found by LLM

**Scoring**:
- Correct detection: +1 point
- False positive: -0.25 points
- Missed detection: 0 points

### 4. Running the Scorer

```bash
python3 scripts/score.py examples/sample-llm-output.json examples/sample-ground-truth.json
```

Output shows:
- Precision, Recall, F1 for each type
- Detailed true/false positives/negatives
- Combined score

## Why This Design?

1. **No Fuzzy Matching**: Exact string comparison only
2. **Minimal Data**: Only what's needed for scoring
3. **Fast Comparison**: Simple set operations
4. **Clear Results**: Binary right/wrong, no ambiguity
5. **Easy to Implement**: Ground truth is trivial to create

This makes the benchmark fully automated and objective.
