# Test Prompts for Framework Benchmark

This directory contains the exact prompts to be used for testing AI coding assistant frameworks on specification alignment detection.

## The Four Tests

1. **type1-missing.md** - Detects missing implementations
2. **type2-incorrect.md** - Detects incorrect implementations  
3. **type3-extraneous.md** - Detects extraneous code
4. **combined-all-types.md** - Detects all three types in one analysis

## Expected Output Formats

### Type 1 Output
```json
{
  "misalignments": [
    {
      "section": "4.1",
      "reasoning": "Password validation for 6-character minimum not implemented"
    }
  ]
}
```

### Type 2 Output
```json
{
  "misalignments": [
    {
      "section": "2.4",
      "reasoning": "Tasks sorted ASC instead of DESC",
      "files": ["src/app/api/tasks/route.ts"]
    }
  ]
}
```

### Type 3 Output
```json
{
  "misalignments": [
    {
      "feature": "Admin Dashboard",
      "reasoning": "Admin interface not mentioned in specification",
      "files": ["src/app/admin/page.tsx"]
    }
  ]
}
```

### Combined Output
```json
{
  "type1_missing": [
    {"section": "4.1", "reasoning": "..."}
  ],
  "type2_incorrect": [
    {"section": "2.4", "reasoning": "...", "files": [...]}
  ],
  "type3_extraneous": [
    {"feature": "Admin Dashboard", "reasoning": "...", "files": [...]}
  ]
}
```

## How to Use These Prompts

For each test branch:
1. Switch to the test branch in your repository
2. For each framework (Cursor, Claude Code):
   - Copy and paste each prompt exactly as written
   - Save the JSON output from each test
   - Run each test with fresh context (no carryover between tests)
3. Compare outputs against ground truth for scoring

## Scoring Focus

- **Primary**: Match on `section` numbers (Type 1 & 2) or `feature` names (Type 3)
- **Secondary**: Review reasoning quality for insights
- **Files**: Verify at least one file matches for Type 2 & 3

## Important Notes

- Copy prompts EXACTLY as written - do not modify
- Each test should start with fresh context
- Save outputs as JSON for automated scoring
- Run multiple times (3-5) for statistical validity
- Reasoning field is for debugging/analysis, not primary scoring