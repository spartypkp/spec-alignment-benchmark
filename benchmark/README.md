# Benchmark Documentation

This directory contains all documentation for the framework benchmark testing of specification alignment detection.

## Structure

```
benchmark/
├── README.md                    # This file
├── hypotheses.md               # All hypotheses and expected outcomes
├── test-summary.md            # Quick overview of all tests
├── branches/                   # Individual branch documentation
│   ├── control_perfect.md     # CONTROL: No misalignments
│   ├── baseline_balanced.md
│   ├── type1_heavy.md
│   ├── type2_heavy.md
│   ├── subtle_only.md
│   └── distributed.md
└── ground-truth/              # Ground truth JSON files
    ├── control_perfect.json
    ├── baseline_balanced.json
    ├── type1_heavy.json
    ├── type2_heavy.json
    ├── subtle_only.json
    └── distributed.json
```

## Quick Start

1. Review hypotheses in `hypotheses.md`
2. For each branch test:
   - Read the branch documentation in `branches/[branch-name].md`
   - Implement the misalignments as specified
   - Use the ground truth file for scoring

## Test Execution Order

1. **control_perfect** (MUST RUN FIRST - establishes false positive baseline)
2. baseline_balanced (establishes performance baseline)
3. type1_heavy (tests Type 1 specialization)
4. type2_heavy (tests Type 2 specialization)
5. subtle_only (tests complexity handling)
6. distributed (tests context management)

**Important**: The control_perfect branch must be tested first to calibrate false positive rates and establish baseline behavior when code and spec are perfectly aligned.
