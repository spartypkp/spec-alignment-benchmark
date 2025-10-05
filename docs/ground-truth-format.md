# Ground Truth Format

## Overview

Ground truth should be as simple as possible for programmatic comparison. Each type has exactly the data needed for scoring, nothing more.

## Simplified Schema

```json
{
  "test_branch": "test-set-1",
  "specification_file": "specs/project-specification.md",
  "type1_missing": [
    "2.1 Authentication & Authorization",
    "3.3 Rate Limiting", 
    "6.1 API Documentation"
  ],
  "type2_incorrect": [
    {
      "section": "3.1 Request/Response Format",
      "files": ["middleware/errorHandler.ts"]
    },
    {
      "section": "4.3 Data Protection",
      "files": ["api/tasks/route.ts", "api/users/route.ts"]
    },
    {
      "section": "5.1 Coverage Requirements",
      "files": ["package.json", "jest.config.js"]
    }
  ],
  "type3_extraneous": [
    "app/admin/route.ts",
    "app/admin/dashboard/page.tsx",
    "api/debug/route.ts",
    "components/Analytics.tsx"
  ]
}
```

## Type Definitions

### Type 1: Missing Implementation
- **Data needed**: Specification section headers only
- **Format**: Array of strings (section headers)
- **Example**: `["2.1 Authentication & Authorization", "3.3 Rate Limiting"]`
- **Comparison**: Simple set intersection

### Type 2: Incorrect Implementation  
- **Data needed**: Specification section + affected files
- **Format**: Array of objects with section and files
- **Example**: `{"section": "3.1 Request/Response Format", "files": ["middleware/errorHandler.ts"]}`
- **Comparison**: Match both section AND at least one file

### Type 3: Extraneous Code
- **Data needed**: Files containing unspecified code
- **Format**: Array of file paths
- **Example**: `["app/admin/route.ts", "api/debug/route.ts"]`
- **Comparison**: Simple set intersection

## Programmatic Comparison

```python
def score_type1(llm_output, ground_truth):
    """Score Type 1: Missing implementations"""
    found = set(llm_output["type1_missing"])
    expected = set(ground_truth["type1_missing"])
    
    true_positives = found & expected
    false_positives = found - expected
    false_negatives = expected - found
    
    return {
        "precision": len(true_positives) / len(found) if found else 0,
        "recall": len(true_positives) / len(expected) if expected else 0,
        "tp": list(true_positives),
        "fp": list(false_positives),
        "fn": list(false_negatives)
    }

def score_type2(llm_output, ground_truth):
    """Score Type 2: Incorrect implementations"""
    score = 0
    for gt_item in ground_truth["type2_incorrect"]:
        for llm_item in llm_output["type2_incorrect"]:
            if gt_item["section"] == llm_item["section"]:
                # Check if at least one file matches
                if set(gt_item["files"]) & set(llm_item["files"]):
                    score += 1
                    break
    return score

def score_type3(llm_output, ground_truth):
    """Score Type 3: Extraneous code"""
    found = set(llm_output["type3_extraneous"])
    expected = set(ground_truth["type3_extraneous"])
    
    true_positives = found & expected
    false_positives = found - expected
    false_negatives = expected - found
    
    return {
        "precision": len(true_positives) / len(found) if found else 0,
        "recall": len(true_positives) / len(expected) if expected else 0
    }
```

## Expected LLM Output Format

The prompts should ask for this exact format:

### Type 1 Output
```json
{
  "analysis_type": "type1_missing",
  "type1_missing": [
    "2.1 Authentication & Authorization",
    "3.3 Rate Limiting"
  ]
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
  "type3_extraneous": [
    "app/admin/route.ts",
    "api/debug/route.ts"
  ]
}
```

### Combined Output
```json
{
  "analysis_type": "combined_all_types",
  "type1_missing": ["2.1 Authentication & Authorization"],
  "type2_incorrect": [{"section": "3.1 Request/Response Format", "files": ["middleware/errorHandler.ts"]}],
  "type3_extraneous": ["app/admin/route.ts"]
}
```

## Why This Design?

1. **Simple Comparison**: Set operations for Type 1 & 3, simple matching for Type 2
2. **No Ambiguity**: Section headers and file paths are exact strings
3. **Easy Scoring**: Direct comparison without fuzzy matching
4. **Minimal Data**: Only what's needed for scoring
5. **Clear Success**: Match = correct, no match = incorrect

## Creating Ground Truth

When planting misalignments:

1. **Type 1**: Note exact section headers from spec that aren't implemented
2. **Type 2**: Note section header + files where implementation differs  
3. **Type 3**: List files that contain features not in spec

Keep it simple - no descriptions, no explanations, just the data needed for scoring.