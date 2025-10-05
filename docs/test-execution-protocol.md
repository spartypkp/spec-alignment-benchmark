# Test Execution Protocol

## Overview

This document describes the exact process for testing AI coding assistant frameworks on specification alignment detection using the three misalignment types.

---

## Test Structure

### Repository Setup

Your test repository should have:
- **Main branch**: Perfectly aligned code and specification
- **Test branches**: Each with different planted misalignments
  - `test-set-1`: Mix of all three types
  - `test-set-2`: Different mix and quantities
  - `test-set-3`: Edge cases and subtle misalignments

Each test branch contains:
```
todo-app/
├── specs/
│   └── project-specification.md  # The specification
├── ground-truth.json             # Answer key (remove before testing)
├── app/                          # Implementation with planted misalignments
├── components/
├── lib/
└── ...
```

---

## Test Execution Steps

### 1. Pre-Test Setup

For each framework (Cursor, Claude Code):
1. Clear all caches and history
2. Open fresh session
3. Ensure Claude 3.5 Sonnet is selected
4. Load the test repository branch

### 2. Run Four Tests Per Branch

For each test branch, run these 4 prompts in order:

```
1. type1-missing.md      → Detects missing implementations
2. type2-incorrect.md    → Detects incorrect implementations  
3. type3-extraneous.md   → Detects extraneous code
4. combined-all-types.md → Detects all types together
```

**Critical Rules:**
- Fresh context for each prompt (no carryover)
- Copy and paste prompt exactly
- No modifications or additions
- No intervention during execution
- Save each output separately

### 3. Output Naming Convention

Save outputs with clear naming:
```
results/raw/
├── cursor/
│   ├── test-set-1/
│   │   ├── type1-run1.json
│   │   ├── type2-run1.json
│   │   ├── type3-run1.json
│   │   └── combined-run1.json
│   └── test-set-2/
│       └── ...
└── claude-code/
    └── [same structure]
```

### 4. Multiple Runs

For statistical validity:
- Minimum: 3 runs per test
- Recommended: 5 runs per test
- Each run with fresh context

---

## Test Execution Checklist

For each test:

- [ ] Framework in fresh session
- [ ] Correct model selected (Claude 3.5 Sonnet)
- [ ] Test branch loaded
- [ ] Prompt copied exactly
- [ ] No intervention during run
- [ ] Output saved as JSON
- [ ] Output validated as valid JSON

---

## Data Recording

### Required Metadata

For each test run, record:
```json
{
  "test_id": "cursor-test-set-1-type1-run1",
  "framework": "cursor",
  "test_branch": "test-set-1", 
  "prompt_type": "type1",
  "run_number": 1,
  "timestamp": "2025-10-05T14:30:00Z",
  "duration_seconds": 180,
  "output": { /* framework's JSON output */ }
}
```

### Optional Observations

- Search patterns used
- Files examined order
- Self-corrections made
- Confidence patterns

---

## Scoring Process

After all tests complete:

1. **Restore ground truth files** to test branches
2. **Run scoring script**:
   ```bash
   python scripts/score_results.py \
     --results results/raw/cursor/test-set-1/ \
     --ground-truth repos/todo-app/test-set-1/ground-truth.json
   ```
3. **Generate analysis**:
   ```bash
   python scripts/analyze.py --all-results
   ```

---

## Framework Comparison Protocol

To ensure fair comparison:

### Test Order
- Alternate which framework goes first
- Randomize test branch order
- Vary time of day for tests

### Environmental Controls
- Same machine/browser
- Similar network conditions
- No background processing
- Fresh sessions always

### Statistical Requirements
- Same number of runs per framework
- Complete all tests even if early results seem conclusive
- Document any anomalies

---

## Common Issues and Solutions

### Issue: Framework asks for clarification
**Solution**: Wait 30 seconds, then mark as incomplete if no progress

### Issue: Output not in JSON format
**Solution**: Save raw output, attempt manual extraction, note in metadata

### Issue: Framework explores beyond repo
**Solution**: Normal behavior, let it continue

### Issue: Test exceeds 30 minutes
**Solution**: Stop test, mark as timeout, exclude from analysis

---

## Quality Assurance

### Valid Test Criteria
- ✅ Correct prompt used
- ✅ Fresh context
- ✅ No human intervention
- ✅ JSON output produced
- ✅ Reasonable duration (3-30 minutes)

### Invalid Test Criteria  
- ❌ Wrong model selected
- ❌ Previous context influenced results
- ❌ Human provided hints
- ❌ Framework crashed
- ❌ Network issues affected results

---

## Results Validation

Before analysis, validate:
1. All JSON outputs are parseable
2. All required tests completed
3. Equal runs per framework
4. Metadata is complete
5. Ground truth files match tested branches

---

## Summary

The test protocol ensures:
- **Reproducibility**: Anyone can run the same tests
- **Fairness**: Both frameworks get identical conditions
- **Validity**: Statistical rigor through multiple runs
- **Clarity**: Three distinct misalignment types tested

Follow this protocol exactly for valid, comparable results.